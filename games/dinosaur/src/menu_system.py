#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
遊戲選單系統
處理主選單的顯示和交互
"""

import pygame
import math
from config.game_config import Difficulty, DIFFICULTY_SETTINGS, get_color_palette
from sound_manager import get_sound_manager


class MenuSystem:
    """主選單系統"""

    def __init__(self, screen_width, screen_height, fonts, high_score=0):
        """
        初始化選單系統

        Args:
            screen_width (int): 螢幕寬度
            screen_height (int): 螢幕高度
            fonts (dict): 字體字典
            high_score (int): 最高分記錄
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.colors = get_color_palette()
        self.fonts = fonts
        self.selected_difficulty = Difficulty.EASY
        self.selected_index = 0
        self.animation_timer = 0
        self.high_score = high_score

        # 音效管理器
        self.sound_manager = get_sound_manager()

        # 建立選單選項
        self.menu_options = []
        for difficulty, settings in DIFFICULTY_SETTINGS.items():
            self.menu_options.append(
                {
                    "name": settings["name"],
                    "difficulty": difficulty,
                    "description": settings["description"],
                }
            )

        # 調試輸出：確認所有難度選項都已加載
        print(f"📋 選單選項已載入，共 {len(self.menu_options)} 個難度:")
        for i, option in enumerate(self.menu_options):
            print(f"   {i+1}. {option['name']} - {option['description']}")
        print(f"📌 目前選中: {self.menu_options[self.selected_index]['name']}")

    def handle_menu_input(self, event):
        """
        處理選單輸入

        Args:
            event: pygame事件

        Returns:
            bool: 是否開始遊戲
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.sound_manager.play_menu_move()
                self.selected_index = (self.selected_index - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.sound_manager.play_menu_move()
                self.selected_index = (self.selected_index + 1) % len(self.menu_options)
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self.sound_manager.play_menu_select()
                self.selected_difficulty = self.menu_options[self.selected_index][
                    "difficulty"
                ]
                return True  # 開始遊戲
            else:
                # 其他任何按鍵都播放一般音效
                self.sound_manager.play_key_press()
        return False

    def update(self):
        """更新選單動畫"""
        self.animation_timer += 1

    def update_high_score(self, high_score):
        """更新最高分記錄"""
        self.high_score = high_score

    def draw(self, screen):
        """繪製主選單"""
        # 背景
        screen.fill(self.colors["BLACK"])

        # 繪製背景星空效果
        self._draw_starfield(screen)

        # 遊戲標題
        self._draw_title(screen)

        # 最高分顯示
        self._draw_high_score(screen)

        # 選單選項
        self._draw_menu_options(screen)

        # 控制說明
        self._draw_controls(screen)

        # 難度預覽
        self._draw_difficulty_preview(screen)

    def _draw_starfield(self, screen):
        """繪製星空背景"""
        star_count = max(50, self.screen_width * self.screen_height // 10000)
        for i in range(star_count):
            x = (i * 157) % self.screen_width
            y = (i * 211) % self.screen_height
            brightness = int(100 + 50 * math.sin(self.animation_timer * 0.01 + i))
            color = (brightness, brightness, brightness)
            star_size = max(1, int(self.screen_width / 800))
            pygame.draw.circle(screen, color, (x, y), star_size)

    def _draw_title(self, screen):
        """繪製遊戲標題"""
        title_text = "🦕 超級進階小恐龍遊戲 🦕"
        title_surface = self.fonts["large"].render(
            title_text, True, self.colors["YELLOW"]
        )
        title_y = int(self.screen_height * 0.08)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, title_y))
        screen.blit(title_surface, title_rect)

        # 副標題
        subtitle_text = "選擇您的挑戰等級"
        subtitle_surface = self.fonts["medium"].render(
            subtitle_text, True, self.colors["WHITE"]
        )
        subtitle_y = int(self.screen_height * 0.15)
        subtitle_rect = subtitle_surface.get_rect(
            center=(self.screen_width // 2, subtitle_y)
        )
        screen.blit(subtitle_surface, subtitle_rect)

    def _draw_high_score(self, screen):
        """繪製最高分記錄"""
        if self.high_score > 0:
            # 主要最高分文字
            high_score_text = f"🏆 最高分記錄: {self.high_score:,}"
            high_score_surface = self.fonts["medium"].render(
                high_score_text, True, self.colors["YELLOW"]
            )

            # 添加發光效果
            glow_surface = self.fonts["medium"].render(
                high_score_text, True, self.colors["ORANGE"]
            )

            # 位置設定
            high_score_y = int(self.screen_height * 0.20)
            high_score_rect = high_score_surface.get_rect(
                center=(self.screen_width // 2, high_score_y)
            )
            glow_rect = glow_surface.get_rect(
                center=(self.screen_width // 2 + 2, high_score_y + 2)
            )

            # 繪製發光效果（稍微偏移）
            screen.blit(glow_surface, glow_rect)
            # 繪製主要文字
            screen.blit(high_score_surface, high_score_rect)

            # 添加閃爍效果
            if int(self.animation_timer / 30) % 2 == 0:
                sparkle_text = "✨"
                sparkle_surface = self.fonts["small"].render(
                    sparkle_text, True, self.colors["YELLOW"]
                )
                sparkle_x = high_score_rect.right + 10
                screen.blit(sparkle_surface, (sparkle_x, high_score_y - 10))
        else:
            # 當沒有記錄時顯示鼓勵文字
            no_record_text = "開始您的第一次挑戰！"
            no_record_surface = self.fonts["small"].render(
                no_record_text, True, self.colors["GRAY"]
            )
            no_record_y = int(self.screen_height * 0.20)
            no_record_rect = no_record_surface.get_rect(
                center=(self.screen_width // 2, no_record_y)
            )
            screen.blit(no_record_surface, no_record_rect)

    def _draw_menu_options(self, screen):
        """繪製選單選項"""
        start_y = int(self.screen_height * 0.30)  # 向下調整，為高分顯示留空間
        option_spacing = int(self.screen_height * 0.15)  # 恢復合理的間距
        selection_width = min(400, int(self.screen_width * 0.4))

        # 將選單選項移到畫面右側
        menu_center_x = int(self.screen_width * 0.7)

        for i, option in enumerate(self.menu_options):
            y_pos = start_y + i * option_spacing

            # 選中效果
            if i == self.selected_index:
                # 選中背景
                selection_rect = pygame.Rect(
                    menu_center_x - selection_width // 2,
                    y_pos - int(option_spacing * 0.35),
                    selection_width,
                    int(option_spacing * 0.7),
                )
                pygame.draw.rect(screen, self.colors["BLUE"], selection_rect)
                pygame.draw.rect(screen, self.colors["YELLOW"], selection_rect, 3)

                # 選項文字 (選中時為白色)
                option_surface = self.fonts["medium"].render(
                    option["name"], True, self.colors["WHITE"]
                )
            else:
                # 選項文字 (未選中時為灰色)
                option_surface = self.fonts["medium"].render(
                    option["name"], True, self.colors["GRAY"]
                )

            option_rect = option_surface.get_rect(center=(menu_center_x, y_pos))
            screen.blit(option_surface, option_rect)

            # 難度描述
            desc_color = (
                self.colors["YELLOW"]
                if i == self.selected_index
                else self.colors["DARK_GRAY"]
            )
            desc_surface = self.fonts["small"].render(
                option["description"], True, desc_color
            )
            desc_y = y_pos + int(option_spacing * 0.3)
            desc_rect = desc_surface.get_rect(center=(menu_center_x, desc_y))
            screen.blit(desc_surface, desc_rect)

    def _draw_controls(self, screen):
        """繪製控制說明"""
        # 主要控制說明（更醒目）
        main_control_text = "🕹️ ↑↓ 選擇難度  |  空白鍵/Enter 開始遊戲"
        main_control_surface = self.fonts["medium"].render(
            main_control_text, True, self.colors["YELLOW"]
        )
        main_control_y = int(self.screen_height * 0.87)
        main_control_rect = main_control_surface.get_rect(
            center=(self.screen_width // 2, main_control_y)
        )
        screen.blit(main_control_surface, main_control_rect)

        # 次要控制說明
        sub_control_text = "F1 音效開關  |  F11 全螢幕  |  ESC 退出"
        sub_control_surface = self.fonts["small"].render(
            sub_control_text, True, self.colors["WHITE"]
        )
        sub_control_y = int(self.screen_height * 0.93)
        sub_control_rect = sub_control_surface.get_rect(
            center=(self.screen_width // 2, sub_control_y)
        )
        screen.blit(sub_control_surface, sub_control_rect)

    def _draw_difficulty_preview(self, screen):
        """繪製難度預覽"""
        preview_texts = {
            Difficulty.EASY: [
                "• 慢速障礙物",
                "• 簡單的跳躍和蹲下",
                "• 適合學習基本操作",
            ],
            Difficulty.MEDIUM: ["• 中等速度", "• 基本障礙物組合", "• 需要一定反應能力"],
            Difficulty.HARD: ["• 快速移動", "• 複雜障礙物", "• 需要高度集中"],
            Difficulty.NIGHTMARE: [
                "• 超極速模式 + 重力異常",
                "• 隱形&爆炸&分裂障礙物",
                "• 能力冷卻時間大幅增加",
                "• 螢幕會隨機閃爍干擾",
            ],
        }

        selected_option = self.menu_options[self.selected_index]
        if selected_option["difficulty"] in preview_texts:
            # 難度預覽標題
            preview_title = "難度特色："
            title_surface = self.fonts["medium"].render(
                preview_title, True, self.colors["YELLOW"]
            )
            title_x = int(self.screen_width * 0.05)  # 左邊距離邊緣 5%
            title_y = int(self.screen_height * 0.3)
            screen.blit(title_surface, (title_x, title_y))

            # 預覽內容
            preview_start_y = title_y + int(self.screen_height * 0.08)
            preview_line_spacing = int(self.screen_height * 0.05)  # 調整行間距

            for j, preview_text in enumerate(
                preview_texts[selected_option["difficulty"]]
            ):
                preview_surface = self.fonts["small"].render(
                    preview_text, True, self.colors["ORANGE"]
                )
                preview_x = title_x + int(self.screen_width * 0.02)  # 稍微向右縮進
                preview_y = preview_start_y + j * preview_line_spacing
                screen.blit(preview_surface, (preview_x, preview_y))

    def update_screen_size(self, screen_width, screen_height):
        """
        更新螢幕尺寸

        Args:
            screen_width (int): 新的螢幕寬度
            screen_height (int): 新的螢幕高度
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
