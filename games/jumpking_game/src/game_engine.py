#!/usr/bin/env python3
"""
Jump King 遊戲引擎
整合所有遊戲組件的主要控制器
"""
import pygame
import sys
import os

# 添加必要的路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
levels_dir = os.path.join(parent_dir, "levels")
data_dir = os.path.join(parent_dir, "data")
sys.path.insert(0, current_dir)
sys.path.insert(0, levels_dir)
sys.path.insert(0, data_dir)

from game_config import *
from player import Player
from ui_manager import UIManager
from renderer import Renderer
from level_manager import LevelManager
from save_manager import SaveManager


class Game:
    def __init__(self):
        # 初始化 Pygame
        pygame.init()

        # 視窗設定
        self.fullscreen = False
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.ui_scale_x = 1.0
        self.ui_scale_y = 1.0
        self.ui_scale = 1.0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jump King - 十一關挑戰")
        self.clock = pygame.time.Clock()
        self.running = True

        # 遊戲狀態
        self.state = MENU
        self.current_level = 1

        # 初始化組件
        self.save_manager = SaveManager()
        self.level_manager = LevelManager()
        self.ui_manager = UIManager()
        self.renderer = Renderer(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player = None

        # 選單狀態
        self.menu_selection = 0
        self.level_select_selection = 1

    def toggle_fullscreen(self):
        """切換全屏模式"""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            # 獲取螢幕解析度
            info = pygame.display.Info()
            self.screen_width = info.current_w
            self.screen_height = info.current_h
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            # 計算UI縮放比例
            self.ui_scale_x = self.screen_width / SCREEN_WIDTH
            self.ui_scale_y = self.screen_height / SCREEN_HEIGHT
            self.ui_scale = min(self.ui_scale_x, self.ui_scale_y)
        else:
            self.screen_width = SCREEN_WIDTH
            self.screen_height = SCREEN_HEIGHT
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.ui_scale_x = 1.0
            self.ui_scale_y = 1.0
            self.ui_scale = 1.0

        # 重新載入字體
        self.ui_manager.load_fonts()
        pygame.display.set_caption("Jump King - 十一關挑戰")

    def start_level(self, level_num):
        """開始指定關卡"""
        level_data = self.level_manager.get_level(level_num)
        if not level_data:
            print(f"找不到第{level_num}關的資料")
            return

        self.current_level = level_num
        start_x, start_y = level_data["start_pos"]
        self.player = Player(start_x, start_y)

        # 確保玩家正確地站在起始平台上
        self.player.on_ground = True
        self.player.vel_x = 0
        self.player.vel_y = 0

        self.renderer.camera_y = 0
        self.state = PLAYING

        # 初始化關卡統計
        if str(level_num) not in self.save_manager.level_stats:
            self.save_manager.level_stats[str(level_num)] = {
                "deaths": 0,
                "completed": False,
                "best_deaths": None,
            }

        print(f"開始第{level_num}關: {level_data['name']}")

    def complete_level(self):
        """完成關卡"""
        deaths = self.player.death_count

        # 更新統計資料
        self.save_manager.update_level_stats(self.current_level, deaths, completed=True)

        # 解鎖下一關
        self.save_manager.unlock_next_level(self.current_level)

        # 儲存進度
        self.save_manager.save_progress()

        self.state = VICTORY
        print(f"完成第{self.current_level}關！死亡次數: {deaths}")

    def handle_menu_events(self, event):
        """處理主選單事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu_selection = (self.menu_selection - 1) % 3
            elif event.key == pygame.K_DOWN:
                self.menu_selection = (self.menu_selection + 1) % 3
            elif event.key == pygame.K_RETURN:
                if self.menu_selection == 0:  # 開始遊戲
                    self.state = LEVEL_SELECT
                elif self.menu_selection == 1:  # 繼續遊戲
                    level_to_start = self.save_manager.get_next_unfinished_level()
                    self.start_level(level_to_start)
                elif self.menu_selection == 2:  # 退出
                    self.running = False

    def handle_level_select_events(self, event):
        """處理關卡選擇事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if self.level_select_selection > 1:
                    self.level_select_selection -= 1
            elif event.key == pygame.K_RIGHT:
                if self.level_select_selection < self.save_manager.unlocked_levels:
                    self.level_select_selection += 1
            elif event.key == pygame.K_RETURN:
                self.start_level(self.level_select_selection)
            elif event.key == pygame.K_ESCAPE:
                self.state = MENU

    def handle_playing_events(self, event):
        """處理遊戲中的事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.start_jump_charge()
            elif event.key == pygame.K_r:
                # 重置玩家位置
                self.player.reset_position()
                self.save_manager.update_level_stats(
                    self.current_level, self.player.death_count
                )
                self.save_manager.save_progress()
            elif event.key == pygame.K_ESCAPE:
                self.state = MENU
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                # 決定跳躍方向
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.player.execute_jump("left")
                elif keys[pygame.K_RIGHT]:
                    self.player.execute_jump("right")
                else:
                    self.player.execute_jump("up")

    def handle_events(self):
        """處理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_manager.save_progress()
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # 全域按鍵處理
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE and self.fullscreen:
                    # 在全屏模式下按ESC退出全屏
                    self.toggle_fullscreen()
                else:
                    # 處理其他按鍵事件
                    if self.state == MENU:
                        self.handle_menu_events(event)
                    elif self.state == LEVEL_SELECT:
                        self.handle_level_select_events(event)
                    elif self.state == PLAYING:
                        self.handle_playing_events(event)
                    elif self.state in [VICTORY, GAME_OVER]:
                        if event.key == pygame.K_RETURN:
                            if self.current_level < TOTAL_LEVELS:
                                # 進入下一關
                                self.start_level(self.current_level + 1)
                            else:
                                self.state = LEVEL_SELECT
                        elif event.key == pygame.K_ESCAPE:
                            self.state = MENU
            else:
                if self.state == MENU:
                    self.handle_menu_events(event)
                elif self.state == LEVEL_SELECT:
                    self.handle_level_select_events(event)
                elif self.state == PLAYING:
                    self.handle_playing_events(event)

    def update_playing(self):
        """更新遊戲中的邏輯"""
        if not self.player:
            return

        # 更新跳躍蓄力
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.player.update_jump_charge()

        # 獲取當前關卡資料
        level_data = self.level_manager.get_level(self.current_level)
        if not level_data:
            return

        # 更新玩家
        result = self.player.update(
            level_data["platforms"], level_data["death_zones"], self.current_level
        )

        # 檢查死亡
        if result == "death":
            self.player.reset_position()
            self.save_manager.update_level_stats(
                self.current_level, self.player.death_count
            )
            self.save_manager.save_progress()
        elif result == "fall_trap":
            # 掉落陷阱的特殊處理
            self.save_manager.update_level_stats(
                self.current_level, self.player.death_count
            )
            self.save_manager.save_progress()

        # 檢查是否完成關卡
        if self.renderer.check_goal_completion(self.player, level_data):
            self.complete_level()

    def update(self):
        """更新遊戲邏輯"""
        if self.state == PLAYING:
            self.update_playing()

    def draw(self):
        """繪製畫面"""
        if self.fullscreen:
            # 全屏模式下，先繪製到虛擬畫布
            virtual_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.draw_content(virtual_screen)
            self.scale_and_blit_virtual_screen(virtual_screen)
        else:
            # 視窗模式直接繪製
            self.draw_content(self.screen)

        pygame.display.flip()

    def draw_content(self, screen):
        """繪製畫面內容"""
        if self.state == MENU:
            self.ui_manager.draw_menu(
                screen, self.menu_selection, self.save_manager.unlocked_levels
            )
        elif self.state == LEVEL_SELECT:
            self.ui_manager.draw_level_select(
                screen,
                self.level_select_selection,
                self.save_manager.unlocked_levels,
                self.save_manager.level_stats,
                self.level_manager,
            )
        elif self.state == PLAYING:
            level_data = self.level_manager.get_level(self.current_level)
            if level_data and self.player:
                self.renderer.draw_game_scene(
                    screen, level_data, self.player, self.current_level
                )
                self.ui_manager.draw_playing_ui(
                    screen, self.current_level, level_data, self.player
                )
        elif self.state == VICTORY:
            level_data = self.level_manager.get_level(self.current_level)
            self.ui_manager.draw_victory(
                screen, self.current_level, level_data, self.player
            )

    def scale_and_blit_virtual_screen(self, virtual_screen):
        """縮放虛擬畫布並繪製到實際螢幕"""
        # 縮放並居中顯示虛擬畫布
        scaled_surface = pygame.transform.scale(
            virtual_screen,
            (int(SCREEN_WIDTH * self.ui_scale), int(SCREEN_HEIGHT * self.ui_scale)),
        )

        # 計算居中位置
        offset_x = (self.screen_width - SCREEN_WIDTH * self.ui_scale) // 2
        offset_y = (self.screen_height - SCREEN_HEIGHT * self.ui_scale) // 2

        # 清除螢幕並繪製縮放後的畫面
        self.screen.fill(BLACK)
        self.screen.blit(scaled_surface, (offset_x, offset_y))

    def run(self):
        """主遊戲循環"""
        print("Jump King 遊戲啟動")
        print(f"已解鎖關卡: {self.save_manager.unlocked_levels}/{TOTAL_LEVELS}")

        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        print("遊戲結束")
        self.save_manager.save_progress()
        pygame.quit()
