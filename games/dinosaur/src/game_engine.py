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
)
from dinosaur import Dinosaur
from obstacles import ObstacleManager
from menu_system import MenuSystem


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
        self.game_over = False
        self.cloud_timer = 0
        self.game_speed = 5
        self.speed_increase_timer = 0
        self.obstacle_spawn_rate = 1.0
        self.speed_increase_rate = 0.1

        # 遊戲效果
        self.combo_count = 0
        self.screen_shake = 0

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

        # 根據難度設定遊戲參數
        settings = DIFFICULTY_SETTINGS[difficulty]
        self.game_speed = settings["game_speed"]
        self.obstacle_spawn_rate = settings["obstacle_spawn_rate"]
        self.speed_increase_rate = settings["speed_increase_rate"]

        print(f"🚀 遊戲開始！難度等級: {settings['name']}")

    def return_to_menu(self):
        """返回主選單"""
        self.game_state = GameState.MENU
        self.menu_system.selected_index = 0

    def handle_events(self):
        """處理遊戲事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # 全域快捷鍵
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                elif event.key == pygame.K_F4 and (
                    pygame.key.get_pressed()[pygame.K_LALT]
                    or pygame.key.get_pressed()[pygame.K_RALT]
                ):
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
                    return False

            # 處理遊戲中事件
            elif self.game_state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.return_to_menu()
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        if not self.game_over:
                            if (
                                hasattr(self.dinosaur, "is_control_inverted")
                                and self.dinosaur.is_control_inverted
                            ):
                                self.dinosaur.duck()
                            else:
                                self.dinosaur.jump()
                        else:
                            self.start_game(self.selected_difficulty)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if not self.game_over:
                            if (
                                hasattr(self.dinosaur, "is_control_inverted")
                                and self.dinosaur.is_control_inverted
                            ):
                                self.dinosaur.jump()
                            else:
                                self.dinosaur.duck()
                    elif event.key == pygame.K_x:
                        if not self.game_over:
                            self.dinosaur.dash()
                    elif event.key == pygame.K_z:
                        if not self.game_over:
                            self.dinosaur.activate_shield()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if not self.game_over:
                            if not (
                                hasattr(self.dinosaur, "is_control_inverted")
                                and self.dinosaur.is_control_inverted
                            ):
                                self.dinosaur.stand_up()
        return True

    def update(self):
        """更新遊戲邏輯"""
        if self.game_state == GameState.MENU:
            self.menu_system.update()

        elif self.game_state == GameState.PLAYING:
            if not self.game_over:
                # 噩夢模式的特殊效果
                if self.selected_difficulty >= Difficulty.NIGHTMARE:
                    self.apply_nightmare_effects()

                # 更新恐龍
                self.dinosaur.update()

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
                )
                self.obstacle_manager.update(self.game_speed)

                # 生成雲朵
                self.spawn_cloud()
                self.update_clouds()

                # 檢查碰撞
                if self.check_collision():
                    self.game_over = True
                    if self.score > self.high_score:
                        self.high_score = self.score
                        print(f"🎉 新紀錄！分數: {self.high_score}")

            # 減少螢幕震動
            if self.screen_shake > 0:
                self.screen_shake -= 1

    def apply_nightmare_effects(self):
        """應用噩夢模式的特殊效果"""
        if not self.dinosaur:
            return

        # 螢幕閃爍效果
        if random.randint(1, 300) == 1:
            self.screen_shake = random.randint(5, 15)

        # 重力異常
        if random.randint(1, 600) == 1:
            self.dinosaur.apply_nightmare_effect(
                "gravity_reversal", random.randint(180, 300)
            )
            print("⚠️ 重力異常發生！")

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
            obstacle_rect = obstacle.get_collision_rect()

            if dino_rect.colliderect(obstacle_rect):
                # 檢查特殊情況
                if obstacle.can_walk_through():
                    self.combo_count += 1
                    self.score += 5
                    continue
                elif obstacle.can_duck_under() and self.dinosaur.is_ducking:
                    self.combo_count += 1
                    self.score += 10
                    continue
                elif self.dinosaur.has_shield:
                    self.dinosaur.has_shield = False
                    self.dinosaur.shield_time = 0
                    self.screen_shake = 10

                    if obstacle.obstacle_type == "explosive":
                        obstacle.trigger_explosion()

                    if obstacle in self.obstacle_manager.obstacles:
                        self.obstacle_manager.obstacles.remove(obstacle)
                    self.score += 20
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
            score_multiplier = {
                Difficulty.EASY: 1,
                Difficulty.MEDIUM: 1.5,
                Difficulty.HARD: 2,
                Difficulty.NIGHTMARE: 4,
            }
            self.score += int(
                10 * removed_count * score_multiplier.get(self.selected_difficulty, 1)
            )

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

            # 根據難度調整背景色
            bg_colors = {
                Difficulty.EASY: self.colors["WHITE"],
                Difficulty.MEDIUM: (250, 250, 250),
                Difficulty.HARD: (240, 240, 240),
                Difficulty.NIGHTMARE: (200, 200, 200),
            }
            current_bg = bg_colors.get(self.selected_difficulty, self.colors["WHITE"])
            self.screen.fill(current_bg)

            # 畫地面
            pygame.draw.line(
                self.screen,
                self.colors["BLACK"],
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

        # 更新顯示
        pygame.display.flip()

    def draw_game_info(self):
        """繪製遊戲資訊"""
        margin = int(self.screen_width * 0.0125)
        line_height = int(self.screen_height * 0.04)

        # 分數顯示
        score_text = f"分數: {self.score}"
        score_surface = self.font_medium.render(score_text, True, self.colors["BLACK"])
        self.screen.blit(score_surface, (margin, margin))

        # 最高分顯示
        if self.high_score > 0:
            high_score_text = f"最高分: {self.high_score}"
            high_score_surface = self.font_small.render(
                high_score_text, True, self.colors["PURPLE"]
            )
            self.screen.blit(high_score_surface, (margin, margin + line_height))

        # 遊戲速度顯示
        speed_text = f"速度: {self.game_speed:.1f}x"
        speed_surface = self.font_small.render(speed_text, True, self.colors["BLUE"])
        self.screen.blit(speed_surface, (margin, margin + line_height * 2))

        # 難度等級顯示
        difficulty_names = {
            Difficulty.EASY: "簡單",
            Difficulty.MEDIUM: "中等",
            Difficulty.HARD: "困難",
            Difficulty.NIGHTMARE: "噩夢",
        }
        difficulty_text = (
            f"難度: {difficulty_names.get(self.selected_difficulty, '未知')}"
        )
        difficulty_surface = self.font_small.render(
            difficulty_text, True, self.colors["PURPLE"]
        )
        self.screen.blit(difficulty_surface, (margin, margin + line_height * 3))

        # 連擊數顯示
        current_line = 4
        if self.combo_count > 0:
            combo_text = f"連擊: {self.combo_count}"
            combo_surface = self.font_small.render(
                combo_text, True, self.colors["ORANGE"]
            )
            self.screen.blit(
                combo_surface, (margin, margin + line_height * current_line)
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

            if self.dinosaur.dash_cooldown > 0:
                dash_text = f"衝刺冷卻: {self.dinosaur.dash_cooldown // 60 + 1}秒"
                dash_surface = self.font_small.render(
                    dash_text, True, self.colors["YELLOW"]
                )
                self.screen.blit(
                    dash_surface, (margin, margin + line_height * current_line)
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
            center=(self.screen_width // 2, self.screen_height // 2 - 80)
        )
        self.screen.blit(game_over_surface, game_over_rect)

        # 分數顯示
        final_score_text = f"最終分數: {self.score}"
        final_score_surface = self.font_medium.render(
            final_score_text, True, self.colors["YELLOW"]
        )
        final_score_rect = final_score_surface.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 - 30)
        )
        self.screen.blit(final_score_surface, final_score_rect)

        # 最高分顯示
        if self.score == self.high_score and self.high_score > 0:
            new_record_text = "🎉 新紀錄！New Record!"
            new_record_surface = self.font_medium.render(
                new_record_text, True, self.colors["PINK"]
            )
            new_record_rect = new_record_surface.get_rect(
                center=(self.screen_width // 2, self.screen_height // 2 + 20)
            )
            self.screen.blit(new_record_surface, new_record_rect)

        # 重新開始提示
        restart_text = "空白鍵: 重新開始同難度  |  ESC: 返回主選單"
        restart_surface = self.font_medium.render(
            restart_text, True, self.colors["WHITE"]
        )
        restart_rect = restart_surface.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 + 70)
        )
        self.screen.blit(restart_surface, restart_rect)

    def draw_start_instructions(self):
        """繪製開始遊戲的操作說明"""
        center_x = self.screen_width // 2
        instruction_y = int(self.screen_height * 0.15)
        line_spacing = int(self.screen_height * 0.04)

        # 主要操作說明
        instruction_text = (
            "↑/空白鍵:跳躍  ↓/S鍵:蹲下  X:衝刺  Z:護盾  F11:全螢幕  ESC:返回選單"
        )
        instruction_surface = self.font_medium.render(
            instruction_text, True, self.colors["GRAY"]
        )
        instruction_rect = instruction_surface.get_rect(
            center=(center_x, instruction_y)
        )
        self.screen.blit(instruction_surface, instruction_rect)

        # 障礙物說明
        if self.selected_difficulty <= Difficulty.MEDIUM:
            obstacles_text = "🌵 仙人掌需跳躍  🪨 石頭可走過  🐦 鳥類需蹲下"
        else:
            obstacles_text = "⚡ 高難度！注意隱形、爆炸、移動障礙物！"

        obstacles_surface = self.font_small.render(
            obstacles_text, True, self.colors["BLUE"]
        )
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
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

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
