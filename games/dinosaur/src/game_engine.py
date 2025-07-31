#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
遊戲主引擎
協調所有遊戲系統的運作
"""

import pygame
import sys
import random
import os
import json
from config.game_config import (
    DEFAULT_SCREEN_WIDTH,
    DEFAULT_SCREEN_HEIGHT,
    FPS,
    FULLSCREEN_MODE,
    WINDOW_MODE,
    GameState,
    Difficulty,
    DIFFICULTY_SETTINGS,
    get_color_palette,
    FONT_PATH,
    ScoreSystem,
)
from dinosaur import Dinosaur
from obstacles import ObstacleManager
from menu_system import MenuSystem
from sound_manager import get_sound_manager


class Game:
    """主遊戲類別"""

    def __init__(self):
        """初始化遊戲"""
        # 初始化 pygame
        pygame.init()

        # 螢幕設定
        self.fullscreen_mode = FULLSCREEN_MODE
        self.screen_width = DEFAULT_SCREEN_WIDTH
        self.screen_height = DEFAULT_SCREEN_HEIGHT
        self.ground_height = int(self.screen_height * 0.875)

        # 設定顯示模式
        self.setup_display()
        pygame.display.set_caption("🦕 超級進階小恐龍遊戲 - 重構版本")
        self.clock = pygame.time.Clock()

        # 遊戲狀態
        self.game_state = GameState.MENU
        self.selected_difficulty = Difficulty.EASY

        # 載入顏色調色板
        self.colors = get_color_palette()

        # 字體設定
        self.setup_fonts()

        # 音效系統
        self.sound_manager = get_sound_manager()

        # 主選單系統
        self.menu_system = MenuSystem(
            self.screen_width,
            self.screen_height,
            {
                "large": self.font_large,
                "medium": self.font_medium,
                "small": self.font_small,
            },
        )

        # 遊戲物件
        self.dinosaur = None
        self.obstacle_manager = None
        self.clouds = []

        # 遊戲狀態
        self.score = 0
        self.high_score = 0
        self.high_score_file = "high_score.json"  # 高分記錄檔案
        self.load_high_score()  # 載入高分記錄

        # 更新選單系統的高分顯示
        self.menu_system.update_high_score(self.high_score)
        self.game_over = False
        self.cloud_timer = 0
        self.game_speed = 5
        self.speed_increase_timer = 0
        self.obstacle_spawn_rate = 1.0
        self.speed_increase_rate = 0.1

        # 距離追蹤系統
        self.total_distance = 0
        self.distance_score_accumulator = 0
        self.last_speed_bonus_score = 0

        # 遊戲效果
        self.combo_count = 0
        self.screen_shake = 0

        # 噩夢模式螢幕閃爍效果
        self.screen_flicker_timer = 0
        self.screen_flicker_duration = 0
        self.next_flicker_time = random.randint(120, 480)  # 隨機 2-8秒

        # 日夜轉換動畫效果
        self.transition_progress = 0  # 0-1之間，0=完全白天，1=完全夜晚
        self.transition_speed = 0.02  # 每幀的轉換速度
        self.current_cycle = 0  # 當前的日夜週期
        self.is_transitioning = False  # 是否正在轉換

        # 遊戲開始視覺反饋
        self.game_start_flash_timer = 0
        self.game_start_flash_duration = 90  # 1.5秒的閃爍提示
        self.is_game_starting = False

        print("🎮 遊戲引擎初始化完成")

    def setup_display(self):
        """設定遊戲顯示模式"""
        if self.fullscreen_mode:
            # 全螢幕模式
            display_info = pygame.display.Info()
            self.screen_width = display_info.current_w
            self.screen_height = display_info.current_h
            self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height), pygame.FULLSCREEN
            )
            print(f"🖥️ 全螢幕模式: {self.screen_width}x{self.screen_height}")
        else:
            # 視窗模式
            self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height), WINDOW_MODE
            )
            print(f"🪟 視窗模式: {self.screen_width}x{self.screen_height}")

        # 更新地面高度
        self.ground_height = int(self.screen_height * 0.875)

    def setup_fonts(self):
        """設定遊戲字體"""
        # 根據螢幕大小調整字體大小
        scale_factor = min(
            self.screen_width / DEFAULT_SCREEN_WIDTH,
            self.screen_height / DEFAULT_SCREEN_HEIGHT,
        )
        large_size = int(36 * scale_factor)
        medium_size = int(24 * scale_factor)
        small_size = int(18 * scale_factor)

        # 嘗試載入微軟正黑體
        try:
            self.font_large = pygame.font.Font(FONT_PATH, large_size)
            self.font_medium = pygame.font.Font(FONT_PATH, medium_size)
            self.font_small = pygame.font.Font(FONT_PATH, small_size)
            print(f"✅ 成功載入微軟正黑體 (縮放: {scale_factor:.2f}x)")
        except (FileNotFoundError, OSError):
            # 如果找不到微軟正黑體，使用系統預設字體
            print("⚠️ 找不到微軟正黑體，使用系統預設字體")
            self.font_large = pygame.font.Font(None, large_size)
            self.font_medium = pygame.font.Font(None, medium_size)
            self.font_small = pygame.font.Font(None, small_size)

    def toggle_fullscreen(self):
        """切換全螢幕模式"""
        self.fullscreen_mode = not self.fullscreen_mode
        if self.fullscreen_mode:
            # 進入全螢幕
            display_info = pygame.display.Info()
            self.screen_width = display_info.current_w
            self.screen_height = display_info.current_h
            self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height), pygame.FULLSCREEN
            )
            print(f"🖥️ 切換到全螢幕模式: {self.screen_width}x{self.screen_height}")
        else:
            # 回到視窗模式
            self.screen_width = DEFAULT_SCREEN_WIDTH
            self.screen_height = DEFAULT_SCREEN_HEIGHT
            self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height), WINDOW_MODE
            )
            print(f"🪟 切換到視窗模式: {self.screen_width}x{self.screen_height}")

        # 更新相關設定
        self.ground_height = int(self.screen_height * 0.875)

        # 更新選單系統
        self.menu_system.update_screen_size(self.screen_width, self.screen_height)

        # 重新設定字體
        self.setup_fonts()
        self.menu_system.fonts = {
            "large": self.font_large,
            "medium": self.font_medium,
            "small": self.font_small,
        }

        # 重新設定恐龍位置
        if self.dinosaur:
            self.dinosaur.screen_width = self.screen_width
            self.dinosaur.screen_height = self.screen_height
            self.dinosaur.ground_height = self.ground_height
            self.dinosaur.y = self.ground_height - self.dinosaur.height

    def start_game(self, difficulty):
        """
        根據選擇的難度開始遊戲

        Args:
            difficulty (int): 難度等級
        """
        self.selected_difficulty = difficulty
        self.game_state = GameState.PLAYING

        # 重新初始化遊戲物件
        self.dinosaur = Dinosaur(
            self.screen_width, self.screen_height, self.ground_height
        )
        self.obstacle_manager = ObstacleManager(
            self.screen_width, self.screen_height, self.ground_height
        )
        self.clouds = []

        # 重置遊戲狀態
        self.score = 0
        self.game_over = False
        self.cloud_timer = 0
        self.combo_count = 0
        self.screen_shake = 0
        self.speed_increase_timer = 0

        # 重置螢幕閃爍效果
        self.screen_flicker_timer = 0
        self.screen_flicker_duration = 0
        self.next_flicker_time = random.randint(120, 480)  # 隨機 2-8秒

        # 啟動遊戲開始視覺反饋
        self.is_game_starting = True
        self.game_start_flash_timer = 0

        # 播放遊戲開始音效
        self.sound_manager.play_game_start_sound()

        # 重置日夜轉換效果
        self.transition_progress = 0
        self.current_cycle = 0
        self.is_transitioning = False

        # 重置距離追蹤
        self.total_distance = 0
        self.distance_score_accumulator = 0
        self.last_speed_bonus_score = 0

        # 根據難度設定遊戲參數
        settings = DIFFICULTY_SETTINGS[difficulty]
        self.game_speed = settings["game_speed"]
        self.obstacle_spawn_rate = settings["obstacle_spawn_rate"]
        self.speed_increase_rate = settings["speed_increase_rate"]

        print(f"🚀 遊戲開始！難度等級: {settings['name']}")

        # 播放遊戲開始音效
        self.sound_manager.play_menu_select()

        # 開始背景音樂
        self.sound_manager.start_background_music()

    def return_to_menu(self):
        """返回主選單"""
        self.game_state = GameState.MENU
        self.menu_system.selected_index = 0

    def load_high_score(self):
        """載入高分記錄檔案"""
        try:
            if os.path.exists(self.high_score_file):
                with open(self.high_score_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # 支援舊版本和新版本的資料格式
                    if isinstance(data, dict):
                        self.high_score = data.get("high_score", 0)
                        print(f"📊 載入最高分記錄: {self.high_score}")
                    else:
                        # 舊版本格式，只有一個數字
                        self.high_score = data
                        print(f"📊 載入最高分記錄 (舊格式): {self.high_score}")
            else:
                self.high_score = 0
                print("📊 未找到高分記錄檔案，初始化為 0")
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"⚠️ 載入高分記錄時發生錯誤: {e}")
            self.high_score = 0

    def save_high_score(self):
        """儲存高分記錄到檔案"""
        try:
            # 準備要儲存的資料
            data = {
                "high_score": self.high_score,
                "last_updated": pygame.time.get_ticks(),  # 儲存時間戳
                "version": "2.0",  # 標記版本
            }

            with open(self.high_score_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"💾 高分記錄已儲存: {self.high_score}")
        except Exception as e:
            print(f"⚠️ 儲存高分記錄時發生錯誤: {e}")

    def update_high_score(self, new_score):
        """
        更新最高分記錄

        Args:
            new_score (int): 新的分數

        Returns:
            bool: 是否創造了新記錄
        """
        if new_score > self.high_score:
            self.high_score = new_score
            self.save_high_score()
            # 同時更新選單系統的高分顯示
            if hasattr(self, "menu_system"):
                self.menu_system.update_high_score(self.high_score)
            return True
        return False

    def handle_events(self):
        """處理遊戲事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # 全域快捷鍵
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.sound_manager.play_key_press()
                    self.toggle_fullscreen()
                elif event.key == pygame.K_F1:
                    # F1 切換音效開關
                    self.sound_manager.toggle_sound()
                elif event.key == pygame.K_F2:
                    # F2 切換背景音樂開關
                    self.sound_manager.toggle_background_music()
                elif event.key == pygame.K_F4 and (
                    pygame.key.get_pressed()[pygame.K_LALT]
                    or pygame.key.get_pressed()[pygame.K_RALT]
                ):
                    self.sound_manager.play_key_press()
                    return False

            # 處理視窗大小改變
            if event.type == pygame.VIDEORESIZE and not self.fullscreen_mode:
                self.screen_width = event.w
                self.screen_height = event.h
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height), WINDOW_MODE
                )
                self.ground_height = int(self.screen_height * 0.875)

                # 更新選單系統
                self.menu_system.update_screen_size(
                    self.screen_width, self.screen_height
                )

                # 重新設定字體
                self.setup_fonts()
                self.menu_system.fonts = {
                    "large": self.font_large,
                    "medium": self.font_medium,
                    "small": self.font_small,
                }
                print(f"🔄 視窗大小調整: {self.screen_width}x{self.screen_height}")

            # 處理主選單事件
            if self.game_state == GameState.MENU:
                if self.menu_system.handle_menu_input(event):
                    self.start_game(self.menu_system.selected_difficulty)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.sound_manager.play_key_press()
                    return False

            # 處理遊戲中事件
            elif self.game_state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.sound_manager.play_key_press()
                        self.return_to_menu()
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        if not self.game_over:
                            self.sound_manager.play_jump()
                            if (
                                hasattr(self.dinosaur, "is_control_inverted")
                                and self.dinosaur.is_control_inverted
                            ):
                                pass  # 控制反轉時跳躍鍵無效
                            else:
                                self.dinosaur.jump()
                        else:
                            self.sound_manager.play_menu_select()
                            self.start_game(self.selected_difficulty)
                    elif event.key == pygame.K_z:
                        if not self.game_over:
                            self.sound_manager.play_shield()
                            self.dinosaur.activate_shield()
                    elif event.key == pygame.K_F11:
                        # F11 已在全域處理，但我們仍可以添加音效
                        self.sound_manager.play_key_press()
                    else:
                        # 其他任何按鍵都播放一般音效
                        self.sound_manager.play_key_press()

                elif event.type == pygame.KEYUP:
                    pass  # 移除蹲下按鍵抬起處理
        return True

    def update(self):
        """更新遊戲邏輯"""
        if self.game_state == GameState.MENU:
            self.menu_system.update()

        elif self.game_state == GameState.PLAYING:
            # 更新遊戲開始視覺反饋
            if self.is_game_starting:
                self.game_start_flash_timer += 1
                if self.game_start_flash_timer >= self.game_start_flash_duration:
                    self.is_game_starting = False
                    self.game_start_flash_timer = 0

            if not self.game_over:
                # 噩夢模式的特殊效果
                if self.selected_difficulty >= Difficulty.NIGHTMARE:
                    self.apply_nightmare_effects()

                # 更新恐龍
                self.dinosaur.update()

                # 更新距離和分數
                self.update_distance_and_score()

                # 更新日夜轉換效果
                self.update_day_night_transition()

                # 增加遊戲速度
                self.speed_increase_timer += 1
                speed_increase_interval = max(120, 600 - self.selected_difficulty * 80)
                if self.speed_increase_timer >= speed_increase_interval:
                    self.game_speed += self.speed_increase_rate
                    self.speed_increase_timer = 0
                    print(f"🚀 遊戲速度提升！當前速度: {self.game_speed:.1f}")

                # 更新障礙物
                is_gravity_reversed = (
                    hasattr(self.dinosaur, "is_gravity_reversed")
                    and self.dinosaur.is_gravity_reversed
                )
                self.obstacle_manager.spawn_obstacle(
                    self.selected_difficulty,
                    self.obstacle_spawn_rate,
                    is_gravity_reversed,
                    self.sound_manager,  # 傳入音效管理器
                )
                self.obstacle_manager.update(self.game_speed, self.sound_manager)

                # 生成雲朵
                self.spawn_cloud()
                self.update_clouds()

                # 檢查碰撞
                if self.check_collision():
                    self.game_over = True
                    # 播放死亡音效
                    self.sound_manager.play_death_sound()
                    # 檢查並更新最高分記錄
                    if self.update_high_score(self.score):
                        print(f"🎉 新紀錄！分數: {self.high_score}")

            # 減少螢幕震動
            if self.screen_shake > 0:
                self.screen_shake -= 1

    def update_distance_and_score(self):
        """更新距離追蹤和分數系統"""
        if self.game_over:
            return

        # 累積距離（基於遊戲速度）
        distance_increment = self.game_speed
        self.total_distance += distance_increment
        self.distance_score_accumulator += distance_increment

        # 每走過指定距離給予分數
        if self.distance_score_accumulator >= ScoreSystem.DISTANCE_SCORE_INTERVAL:
            # 計算基礎距離分數
            base_score = ScoreSystem.BASE_DISTANCE_SCORE

            # 計算速度獎勵倍數
            speed_multiplier = self.calculate_speed_multiplier()

            # 計算難度倍數
            difficulty_multiplier = ScoreSystem.DIFFICULTY_MULTIPLIERS.get(
                self.selected_difficulty, 1.0
            )

            # 計算最終分數
            distance_score = int(base_score * speed_multiplier * difficulty_multiplier)

            # 添加分數
            self.score += distance_score

            # 記錄速度獎勵分數用於顯示
            if speed_multiplier > 1.0:
                self.last_speed_bonus_score = distance_score - base_score
            else:
                self.last_speed_bonus_score = 0

            # 重置累積器
            self.distance_score_accumulator = 0

            # 顯示分數獲得資訊（較低頻率）
            if self.total_distance % (ScoreSystem.DISTANCE_SCORE_INTERVAL * 5) == 0:
                print(
                    f"📊 距離分數: +{distance_score} (速度倍數: {speed_multiplier:.1f}x, 難度倍數: {difficulty_multiplier:.1f}x)"
                )

    def calculate_speed_multiplier(self):
        """計算基於速度的分數倍數"""
        if self.game_speed <= ScoreSystem.SPEED_BONUS_THRESHOLD:
            return 1.0

        # 計算超過閾值的速度
        excess_speed = self.game_speed - ScoreSystem.SPEED_BONUS_THRESHOLD

        # 計算倍數
        multiplier = 1.0 + (excess_speed * ScoreSystem.SPEED_BONUS_MULTIPLIER)

        # 限制最大倍數
        return min(multiplier, ScoreSystem.MAX_SPEED_MULTIPLIER)

    def update_day_night_transition(self):
        """更新日夜轉換動畫效果"""
        if self.game_over:
            return

        # 計算目標的日夜週期
        target_cycle = self.score // 2000

        # 檢查是否需要開始新的轉換
        if target_cycle != self.current_cycle:
            if not self.is_transitioning:
                self.is_transitioning = True
                print(
                    f"🌅 開始日夜轉換動畫：週期 {self.current_cycle} → {target_cycle}"
                )

        # 處理轉換動畫
        if self.is_transitioning:
            # 計算轉換方向
            target_is_night = (target_cycle % 2) == 1
            current_is_night = (self.current_cycle % 2) == 1

            if target_is_night and not current_is_night:
                # 白天→夜晚：增加轉換進度
                self.transition_progress += self.transition_speed
                if self.transition_progress >= 1.0:
                    self.transition_progress = 1.0
                    self.current_cycle = target_cycle
                    self.is_transitioning = False
                    print("🌙 轉換完成：進入夜晚模式")

            elif not target_is_night and current_is_night:
                # 夜晚→白天：減少轉換進度
                self.transition_progress -= self.transition_speed
                if self.transition_progress <= 0.0:
                    self.transition_progress = 0.0
                    self.current_cycle = target_cycle
                    self.is_transitioning = False
                    print("☀️ 轉換完成：進入白天模式")

    def calculate_obstacle_score(self, base_score):
        """計算障礙物分數（包含速度和難度獎勵）"""
        # 計算速度倍數
        speed_multiplier = self.calculate_speed_multiplier()

        # 計算難度倍數
        difficulty_multiplier = ScoreSystem.DIFFICULTY_MULTIPLIERS.get(
            self.selected_difficulty, 1.0
        )

        # 計算連擊倍數
        combo_multiplier = 1.0 + (
            self.combo_count * (ScoreSystem.COMBO_BONUS_MULTIPLIER - 1.0) * 0.1
        )
        combo_multiplier = min(combo_multiplier, 3.0)  # 最大3倍連擊獎勵

        # 計算最終分數
        final_score = int(
            base_score * speed_multiplier * difficulty_multiplier * combo_multiplier
        )

        return final_score

    def apply_nightmare_effects(self):
        """應用噩夢模式的特殊效果"""
        if not self.dinosaur:
            return

        # 更新螢幕閃爍計時器
        self.screen_flicker_timer += 1

        # 檢查是否到達下一次閃爍時間
        if (
            self.screen_flicker_timer >= self.next_flicker_time
            and self.screen_flicker_duration <= 0
        ):
            # 開始新的閃爍效果
            self.screen_flicker_duration = random.randint(30, 90)  # 0.5-1.5秒閃爍
            self.screen_flicker_timer = 0
            # 設定下一次閃爍時間 (隨機 2-8秒後)
            self.next_flicker_time = random.randint(120, 480)  # 隨機 2-8秒
            print("💥 噩夢模式：螢幕閃爍開始！")

            # 播放閃電音效
            self.sound_manager.play_lightning_sound()

        # 減少閃爍持續時間
        if self.screen_flicker_duration > 0:
            self.screen_flicker_duration -= 1

        # 原有的螢幕震動效果 (保持較低頻率)
        if random.randint(1, 500) == 1:
            self.screen_shake = random.randint(3, 8)

        # 重力異常 - 自動觸發，無需跳躍
        if random.randint(1, 400) == 1:
            # 如果恐龍目前沒有重力反轉效果，立即啟動
            if self.dinosaur.gravity_reversal_time <= 0:
                self.dinosaur.apply_nightmare_effect(
                    "gravity_reversal", random.randint(180, 300)
                )
                # 立即將恐龍設為跳躍狀態以適應重力變化
                if not self.dinosaur.is_jumping:
                    self.dinosaur.is_jumping = True
                    self.dinosaur.jump_speed = (
                        2 if not self.dinosaur.is_gravity_reversed else -2
                    )
                print("⚠️ 重力異常發生！")

    def apply_screen_flicker(self):
        """應用螢幕閃爍效果"""
        # 創建閃爍覆蓋層
        flicker_intensity = random.uniform(0.1, 0.4)  # 閃爍強度
        flicker_color = random.choice(
            [
                (255, 255, 255),  # 白色閃爍
                (255, 200, 200),  # 淡紅色閃爍
                (200, 200, 255),  # 淡藍色閃爍
                (255, 255, 200),  # 淡黃色閃爍
            ]
        )

        # 隨機決定閃爍模式
        flicker_mode = random.randint(1, 3)

        if flicker_mode == 1:
            # 全螢幕閃爍
            flicker_surface = pygame.Surface((self.screen_width, self.screen_height))
            flicker_surface.set_alpha(int(255 * flicker_intensity))
            flicker_surface.fill(flicker_color)
            self.screen.blit(flicker_surface, (0, 0))

        elif flicker_mode == 2:
            # 邊緣閃爍
            edge_width = random.randint(10, 30)
            flicker_surface = pygame.Surface((self.screen_width, self.screen_height))
            flicker_surface.set_alpha(int(255 * flicker_intensity))
            flicker_surface.fill(flicker_color)

            # 創建中心透明區域
            center_surface = pygame.Surface(
                (
                    self.screen_width - edge_width * 2,
                    self.screen_height - edge_width * 2,
                )
            )
            center_surface.set_alpha(0)
            center_surface.fill((0, 0, 0))
            flicker_surface.blit(center_surface, (edge_width, edge_width))

            self.screen.blit(flicker_surface, (0, 0))

        elif flicker_mode == 3:
            # 隨機條紋閃爍
            stripe_count = random.randint(3, 8)
            stripe_height = self.screen_height // stripe_count

            for i in range(stripe_count):
                if random.random() < 0.5:  # 50% 機率顯示條紋
                    stripe_surface = pygame.Surface((self.screen_width, stripe_height))
                    stripe_surface.set_alpha(int(255 * flicker_intensity))
                    stripe_surface.fill(flicker_color)
                    self.screen.blit(stripe_surface, (0, i * stripe_height))

    def draw_game_start_flash(self):
        """繪製遊戲開始的閃爍效果"""
        # 計算閃爍進度 (0-1)
        flash_progress = self.game_start_flash_timer / self.game_start_flash_duration

        # 使用正弦波創造平滑的脈衝效果
        import math

        pulse_intensity = (math.sin(flash_progress * math.pi * 6) + 1) / 2

        # 從強烈開始逐漸減弱
        fade_factor = 1 - flash_progress
        final_intensity = pulse_intensity * fade_factor

        # 創建彩色邊框閃爍效果
        if final_intensity > 0.1:
            border_width = int(20 * final_intensity)
            alpha = int(150 * final_intensity)

            # 彩色邊框 - 使用綠色表示開始
            for i in range(border_width):
                color_intensity = 1 - (i / border_width)
                green_value = int(255 * color_intensity * final_intensity)
                border_color = (0, green_value, int(green_value * 0.5))

                # 畫邊框矩形
                pygame.draw.rect(
                    self.screen,
                    border_color,
                    (i, i, self.screen_width - i * 2, self.screen_height - i * 2),
                    2,
                )

            # 中央文字提示
            if flash_progress < 0.8:  # 前80%時間顯示文字
                center_x = self.screen_width // 2
                center_y = self.screen_height // 3

                # 根據難度顯示不同的開始文字
                difficulty_names = {
                    Difficulty.EASY: "🌟 簡單模式開始！",
                    Difficulty.MEDIUM: "⚡ 中等模式開始！",
                    Difficulty.HARD: "🔥 困難模式開始！",
                    Difficulty.NIGHTMARE: "💀 噩夢模式開始！",
                }

                start_text = difficulty_names.get(
                    self.selected_difficulty, "🎮 遊戲開始！"
                )
                text_alpha = int(255 * (1 - flash_progress / 0.8))

                # 創建文字表面
                text_surface = self.font_large.render(start_text, True, (0, 255, 0))
                text_surface.set_alpha(text_alpha)

                # 居中顯示
                text_rect = text_surface.get_rect(center=(center_x, center_y))
                self.screen.blit(text_surface, text_rect)

                # 添加副標題
                subtitle_text = "準備好了嗎？"
                subtitle_alpha = int(200 * (1 - flash_progress / 0.8))
                subtitle_surface = self.font_medium.render(
                    subtitle_text, True, (255, 255, 255)
                )
                subtitle_surface.set_alpha(subtitle_alpha)
                subtitle_rect = subtitle_surface.get_rect(
                    center=(center_x, center_y + 50)
                )
                self.screen.blit(subtitle_surface, subtitle_rect)

    def get_background_color(self):
        """根據分數和難度計算背景顏色 (平滑的日夜轉換效果)"""
        # 定義白天和夜晚的顏色
        day_colors = {
            Difficulty.EASY: self.colors["WHITE"],
            Difficulty.MEDIUM: (250, 250, 250),
            Difficulty.HARD: (240, 240, 240),
            Difficulty.NIGHTMARE: (200, 200, 200),
        }

        night_colors = {
            Difficulty.EASY: self.colors["BLACK"],
            Difficulty.MEDIUM: (20, 20, 20),
            Difficulty.HARD: (40, 40, 40),
            Difficulty.NIGHTMARE: (60, 60, 60),
        }

        day_color = day_colors.get(self.selected_difficulty, self.colors["WHITE"])
        night_color = night_colors.get(self.selected_difficulty, self.colors["BLACK"])

        # 使用轉換進度來混合顏色
        if self.transition_progress <= 0:
            return day_color
        elif self.transition_progress >= 1:
            return night_color
        else:
            # 線性插值混合顏色
            return self.lerp_color(day_color, night_color, self.transition_progress)

    def lerp_color(self, color1, color2, t):
        """線性插值兩個顏色

        Args:
            color1: 起始顏色 (r, g, b)
            color2: 目標顏色 (r, g, b)
            t: 插值參數 (0-1)

        Returns:
            tuple: 插值後的顏色 (r, g, b)
        """
        r1, g1, b1 = color1
        r2, g2, b2 = color2

        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)

        return (r, g, b)

    def spawn_cloud(self):
        """生成雲朵"""
        if self.cloud_timer <= 0:
            self.clouds.append(Cloud(self.screen_width))
            self.cloud_timer = random.randint(180, 300)
        else:
            self.cloud_timer -= 1

    def update_clouds(self):
        """更新雲朵"""
        for cloud in self.clouds[:]:
            cloud.update()
            if cloud.x + 40 < 0:
                self.clouds.remove(cloud)

    def check_collision(self):
        """檢查碰撞"""
        if not self.dinosaur or not self.obstacle_manager:
            return False

        dino_rect = self.dinosaur.get_collision_rect()

        for obstacle in self.obstacle_manager.obstacles[:]:
            obstacle_rects = obstacle.get_collision_rect()

            # 處理單一矩形或多個矩形的情況
            if isinstance(obstacle_rects, list):
                collision_detected = any(
                    dino_rect.colliderect(rect) for rect in obstacle_rects
                )
            else:
                collision_detected = dino_rect.colliderect(obstacle_rects)

            if collision_detected:
                # 檢查特殊情況
                if obstacle.can_walk_through(self.selected_difficulty):
                    self.combo_count += 1
                    obstacle_score = self.calculate_obstacle_score(5)
                    self.score += obstacle_score
                    continue
                elif (
                    obstacle.obstacle_type == "hanging_rock"
                    and not self.dinosaur.is_jumping
                ):
                    # 懸浮石頭：不跳躍時可以安全通過
                    self.combo_count += 1
                    obstacle_score = self.calculate_obstacle_score(8)
                    self.score += obstacle_score
                    continue
                elif self.dinosaur.has_shield:
                    self.dinosaur.has_shield = False
                    self.dinosaur.shield_time = 0
                    self.screen_shake = 10

                    # 爆炸障礙物的特殊處理
                    if obstacle.obstacle_type == "explosive":
                        obstacle.trigger_explosion()

                    if obstacle in self.obstacle_manager.obstacles:
                        self.obstacle_manager.obstacles.remove(obstacle)

                    # 統一的護盾分數獎勵
                    obstacle_score = self.calculate_obstacle_score(20)
                    self.score += obstacle_score
                    continue
                elif obstacle.obstacle_type == "invisible" and not obstacle.is_warned:
                    continue
                else:
                    # 處理裝甲障礙物
                    if obstacle.obstacle_type == "armored":
                        if not obstacle.take_damage():
                            self.screen_shake = 5
                            continue

                    # 重置連擊
                    self.combo_count = 0
                    return True

        # 移除超出螢幕的障礙物並計分
        initial_count = len(self.obstacle_manager.obstacles)
        self.obstacle_manager.obstacles = [
            obs for obs in self.obstacle_manager.obstacles if obs.x + obs.width >= 0
        ]
        removed_count = initial_count - len(self.obstacle_manager.obstacles)

        if removed_count > 0:
            # 使用新的分數計算系統
            obstacle_score = self.calculate_obstacle_score(
                ScoreSystem.OBSTACLE_BASE_SCORE * removed_count
            )
            self.score += obstacle_score

        return False

    def draw(self):
        """繪製遊戲畫面"""
        if self.game_state == GameState.MENU:
            self.menu_system.draw(self.screen)

        elif self.game_state == GameState.PLAYING:
            # 螢幕震動效果
            screen_offset_x = (
                random.randint(-self.screen_shake, self.screen_shake)
                if self.screen_shake > 0
                else 0
            )
            screen_offset_y = (
                random.randint(-self.screen_shake, self.screen_shake)
                if self.screen_shake > 0
                else 0
            )

            # 根據難度和分數調整背景色 (日夜反轉效果)
            current_bg = self.get_background_color()
            self.screen.fill(current_bg)

            # 畫地面
            # 使用轉換進度來決定地面顏色
            if self.transition_progress <= 0:
                ground_color = self.colors["BLACK"]  # 白天時地面是黑色
            elif self.transition_progress >= 1:
                ground_color = self.colors["WHITE"]  # 夜晚時地面是白色
            else:
                # 平滑轉換地面顏色
                ground_color = self.lerp_color(
                    self.colors["BLACK"], self.colors["WHITE"], self.transition_progress
                )
            pygame.draw.line(
                self.screen,
                ground_color,
                (screen_offset_x, self.ground_height + screen_offset_y),
                (
                    self.screen_width + screen_offset_x,
                    self.ground_height + screen_offset_y,
                ),
                2,
            )

            # 畫雲朵
            for cloud in self.clouds:
                cloud.draw(self.screen)

            # 畫恐龍
            if self.dinosaur:
                self.dinosaur.draw(self.screen)

            # 畫障礙物
            if self.obstacle_manager:
                self.obstacle_manager.draw(self.screen)

            # 顯示遊戲資訊
            self.draw_game_info()

            # 顯示控制說明 (只在遊戲開始時)
            if self.score == 0 and not self.game_over:
                self.draw_start_instructions()

            # 遊戲結束畫面
            if self.game_over:
                self.draw_game_over_screen()

            # 遊戲開始閃爍效果
            if self.is_game_starting and self.game_start_flash_timer > 0:
                self.draw_game_start_flash()

            # 噩夢模式螢幕閃爍效果
            if (
                self.selected_difficulty == Difficulty.NIGHTMARE
                and self.screen_flicker_duration > 0
                and not self.game_over
            ):
                self.apply_screen_flicker()

        # 更新顯示
        pygame.display.flip()

    def draw_game_info(self):
        """繪製遊戲資訊"""
        margin = int(self.screen_width * 0.0125)
        line_height = int(self.screen_height * 0.04)

        # 根據日夜轉換進度選擇文字顏色
        if self.transition_progress <= 0:
            # 白天模式
            text_color = self.colors["BLACK"]
            accent_color = self.colors["BLUE"]
            special_color = self.colors["PURPLE"]
        elif self.transition_progress >= 1:
            # 夜晚模式
            text_color = self.colors["WHITE"]
            accent_color = self.colors["LIGHT_BLUE"]
            special_color = self.colors["PINK"]
        else:
            # 轉換中，混合顏色
            text_color = self.lerp_color(
                self.colors["BLACK"], self.colors["WHITE"], self.transition_progress
            )
            accent_color = self.lerp_color(
                self.colors["BLUE"], self.colors["LIGHT_BLUE"], self.transition_progress
            )
            special_color = self.lerp_color(
                self.colors["PURPLE"], self.colors["PINK"], self.transition_progress
            )

        # 分數顯示
        score_text = f"分數: {self.score}"

        # 檢查是否在轉換期間顯示特殊訊息
        if self.is_transitioning:
            target_cycle = self.score // 2000
            target_is_night = (target_cycle % 2) == 1
            if target_is_night:
                score_text += " 🌙→ 轉入夜晚"
            else:
                score_text += " ☀️→ 轉入白天"
        elif self.transition_progress >= 1.0 and self.score % 2000 < 100:
            score_text += " 🌙 夜晚模式"
        elif (
            self.transition_progress <= 0.0
            and self.score % 2000 < 100
            and self.score >= 2000
        ):
            score_text += " ☀️ 白天模式"
        score_surface = self.font_medium.render(score_text, True, text_color)
        self.screen.blit(score_surface, (margin, margin))

        # 距離顯示
        distance_km = self.total_distance / 1000
        distance_text = f"距離: {distance_km:.1f}km"
        distance_surface = self.font_small.render(distance_text, True, accent_color)
        self.screen.blit(distance_surface, (margin, margin + line_height))

        # 最高分顯示
        if self.high_score > 0:
            high_score_text = f"最高分: {self.high_score}"
            high_score_surface = self.font_small.render(
                high_score_text, True, special_color
            )
            self.screen.blit(high_score_surface, (margin, margin + line_height * 2))

        # 遊戲速度顯示與速度獎勵
        speed_multiplier = self.calculate_speed_multiplier()
        if speed_multiplier > 1.0:
            speed_text = f"速度: {self.game_speed:.1f}x (獎勵: {speed_multiplier:.1f}x)"
            speed_color = self.colors["ORANGE"]
        else:
            speed_text = f"速度: {self.game_speed:.1f}x"
            speed_color = self.colors["BLUE"]

        speed_surface = self.font_small.render(speed_text, True, speed_color)
        self.screen.blit(speed_surface, (margin, margin + line_height * 3))

        # 難度等級顯示
        difficulty_names = {
            Difficulty.EASY: "簡單",
            Difficulty.MEDIUM: "中等",
            Difficulty.HARD: "困難",
            Difficulty.NIGHTMARE: "噩夢",
        }
        difficulty_multiplier = ScoreSystem.DIFFICULTY_MULTIPLIERS.get(
            self.selected_difficulty, 1.0
        )
        difficulty_text = f"難度: {difficulty_names.get(self.selected_difficulty, '未知')} ({difficulty_multiplier:.1f}x)"
        difficulty_surface = self.font_small.render(
            difficulty_text, True, self.colors["PURPLE"]
        )
        self.screen.blit(difficulty_surface, (margin, margin + line_height * 4))

        # 連擊數顯示
        current_line = 5
        if self.combo_count > 0:
            combo_text = f"連擊: {self.combo_count}x"
            combo_surface = self.font_small.render(
                combo_text, True, self.colors["ORANGE"]
            )
            self.screen.blit(
                combo_surface, (margin, margin + line_height * current_line)
            )
            current_line += 1

        # 速度獎勵分數顯示（當有速度獎勵時）
        if self.last_speed_bonus_score > 0:
            bonus_text = f"速度獎勵: +{self.last_speed_bonus_score}"
            bonus_surface = self.font_small.render(
                bonus_text, True, self.colors["YELLOW"]
            )
            self.screen.blit(
                bonus_surface, (margin, margin + line_height * current_line)
            )
            current_line += 1

        # 恐龍狀態顯示
        if self.dinosaur:
            if self.dinosaur.has_shield:
                shield_text = f"護盾: {self.dinosaur.shield_time // 60 + 1}秒"
                shield_surface = self.font_small.render(
                    shield_text, True, self.colors["LIGHT_BLUE"]
                )
                self.screen.blit(
                    shield_surface, (margin, margin + line_height * current_line)
                )
                current_line += 1

            # 噩夢模式效果顯示
            if self.selected_difficulty >= Difficulty.NIGHTMARE:
                if (
                    hasattr(self.dinosaur, "is_gravity_reversed")
                    and self.dinosaur.is_gravity_reversed
                ):
                    gravity_text = "⚠️ 重力反轉中！"
                    gravity_surface = self.font_small.render(
                        gravity_text, True, self.colors["RED"]
                    )
                    self.screen.blit(
                        gravity_surface, (margin, margin + line_height * current_line)
                    )
                    current_line += 1

                if (
                    hasattr(self.dinosaur, "is_control_inverted")
                    and self.dinosaur.is_control_inverted
                ):
                    control_text = "💀 控制反轉中！"
                    control_surface = self.font_small.render(
                        control_text, True, self.colors["RED"]
                    )
                    self.screen.blit(
                        control_surface, (margin, margin + line_height * current_line)
                    )
                    current_line += 1

    def draw_game_over_screen(self):
        """繪製遊戲結束畫面"""
        # 半透明背景
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill(self.colors["BLACK"])
        self.screen.blit(overlay, (0, 0))

        # 遊戲結束標題
        game_over_text = "遊戲結束！Game Over!"
        game_over_surface = self.font_large.render(
            game_over_text, True, self.colors["RED"]
        )
        game_over_rect = game_over_surface.get_rect(
            center=(
                self.screen_width // 2,
                self.screen_height // 2 - 240,
            )  # 原來 -120，現在 -240
        )
        self.screen.blit(game_over_surface, game_over_rect)

        # 分數顯示
        final_score_text = f"最終分數: {self.score}"
        final_score_surface = self.font_medium.render(
            final_score_text, True, self.colors["YELLOW"]
        )
        final_score_rect = final_score_surface.get_rect(
            center=(
                self.screen_width // 2,
                self.screen_height // 2 - 140,
            )  # 原來 -70，現在 -140
        )
        self.screen.blit(final_score_surface, final_score_rect)

        # 距離統計
        distance_km = self.total_distance / 1000
        distance_text = f"總距離: {distance_km:.1f} 公里"
        distance_surface = self.font_medium.render(
            distance_text, True, self.colors["LIGHT_BLUE"]
        )
        distance_rect = distance_surface.get_rect(
            center=(
                self.screen_width // 2,
                self.screen_height // 2 - 80,
            )  # 原來 -40，現在 -80
        )
        self.screen.blit(distance_surface, distance_rect)

        # 最大速度統計
        max_speed_text = f"最高速度: {self.game_speed:.1f}x"
        max_speed_surface = self.font_medium.render(
            max_speed_text, True, self.colors["ORANGE"]
        )
        max_speed_rect = max_speed_surface.get_rect(
            center=(
                self.screen_width // 2,
                self.screen_height // 2 - 20,
            )  # 原來 -10，現在 -20
        )
        self.screen.blit(max_speed_surface, max_speed_rect)

        # 最高分顯示
        if self.score == self.high_score and self.high_score > 0:
            new_record_text = "🎉 新紀錄！New Record!"
            new_record_surface = self.font_medium.render(
                new_record_text, True, self.colors["PINK"]
            )
            new_record_rect = new_record_surface.get_rect(
                center=(
                    self.screen_width // 2,
                    self.screen_height // 2 + 40,
                )  # 原來 +20，現在 +40
            )
            self.screen.blit(new_record_surface, new_record_rect)

        # 重新開始提示
        restart_text = "空白鍵: 重新開始同難度  |  ESC: 返回主選單"
        restart_surface = self.font_medium.render(
            restart_text, True, self.colors["WHITE"]
        )
        restart_rect = restart_surface.get_rect(
            center=(
                self.screen_width // 2,
                self.screen_height // 2 + 140,
            )  # 原來 +70，現在 +140
        )
        self.screen.blit(restart_surface, restart_rect)

    def draw_start_instructions(self):
        """繪製開始遊戲的操作說明"""
        center_x = self.screen_width // 2
        instruction_y = int(self.screen_height * 0.15)
        line_spacing = int(self.screen_height * 0.04)

        # 根據日夜轉換進度選擇文字顏色
        if self.transition_progress <= 0:
            # 白天模式
            instruction_color = self.colors["GRAY"]
            accent_color = self.colors["BLUE"]
        elif self.transition_progress >= 1:
            # 夜晚模式
            instruction_color = self.colors["WHITE"]
            accent_color = self.colors["LIGHT_BLUE"]
        else:
            # 轉換中，混合顏色
            instruction_color = self.lerp_color(
                self.colors["GRAY"], self.colors["WHITE"], self.transition_progress
            )
            accent_color = self.lerp_color(
                self.colors["BLUE"], self.colors["LIGHT_BLUE"], self.transition_progress
            )

        # 主要操作說明
        instruction_text = (
            "↑/空白鍵:跳躍  Z:護盾  F1:音效  F2:音樂  F11:全螢幕  ESC:返回選單"
        )
        instruction_surface = self.font_medium.render(
            instruction_text, True, instruction_color
        )
        instruction_rect = instruction_surface.get_rect(
            center=(center_x, instruction_y)
        )
        self.screen.blit(instruction_surface, instruction_rect)

        # 障礙物說明
        if self.selected_difficulty <= Difficulty.MEDIUM:
            obstacles_text = "🌵 仙人掌需跳躍  🪨 石頭可走過"
        else:
            obstacles_text = "⚡ 高難度！注意隱形、爆炸、移動障礙物！"

        obstacles_surface = self.font_small.render(obstacles_text, True, accent_color)
        obstacles_rect = obstacles_surface.get_rect(
            center=(center_x, instruction_y + line_spacing)
        )
        self.screen.blit(obstacles_surface, obstacles_rect)

        # 難度提示
        difficulty_names = {
            Difficulty.EASY: "輕鬆享受遊戲樂趣！",
            Difficulty.MEDIUM: "保持專注，挑戰自我！",
            Difficulty.HARD: "高速挑戰，考驗反應！",
            Difficulty.NIGHTMARE: "極限模式，生存挑戰！",
        }
        subtitle_text = (
            f"當前難度: {difficulty_names.get(self.selected_difficulty, '未知難度')}"
        )
        subtitle_surface = self.font_small.render(
            subtitle_text, True, self.colors["GREEN"]
        )
        subtitle_rect = subtitle_surface.get_rect(
            center=(center_x, instruction_y + line_spacing * 2)
        )
        self.screen.blit(subtitle_surface, subtitle_rect)

    def run(self):
        """執行遊戲主迴圈"""
        running = True
        try:
            while running:
                running = self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(FPS)
        finally:
            # 清理音效系統
            self.sound_manager.cleanup()
            pygame.quit()
            sys.exit()


class Cloud:
    """雲朵類別"""

    def __init__(self, screen_width):
        """初始化雲朵"""
        self.x = screen_width + random.randint(0, 200)
        self.y = random.randint(50, 150)
        self.speed = 1
        self.colors = get_color_palette()

    def update(self):
        """更新雲朵位置"""
        self.x -= self.speed

    def draw(self, screen):
        """繪製雲朵"""
        pygame.draw.ellipse(screen, self.colors["GRAY"], (self.x, self.y, 40, 20))
        pygame.draw.ellipse(
            screen, self.colors["GRAY"], (self.x + 10, self.y - 5, 30, 20)
        )
