#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
遊戲選單系統
處理主選單的顯示和交互
"""

import pygame
import math
from config.game_config import Difficulty, DIFFICULTY_SETTINGS, get_color_palette


class MenuSystem:
    """主選單系統"""

    def __init__(self, screen_width, screen_height, fonts):
        """
        初始化選單系統

        Args:
            screen_width (int): 螢幕寬度
            screen_height (int): 螢幕高度
            fonts (dict): 字體字典
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.colors = get_color_palette()
        self.fonts = fonts
        self.selected_difficulty = Difficulty.EASY
        self.selected_index = 0
        self.animation_timer = 0

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
                self.selected_index = (self.selected_index - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.menu_options)
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self.selected_difficulty = self.menu_options[self.selected_index][
                    "difficulty"
                ]
                return True  # 開始遊戲
        return False

    def update(self):
        """更新選單動畫"""
        self.animation_timer += 1

    def draw(self, screen):
        """繪製主選單"""
        # 背景
        screen.fill(self.colors["BLACK"])

        # 繪製背景星空效果
        self._draw_starfield(screen)

        # 遊戲標題
        self._draw_title(screen)

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

    def _draw_menu_options(self, screen):
        """繪製選單選項"""
        start_y = int(self.screen_height * 0.25)
        option_spacing = int(self.screen_height * 0.15)  # 增加間距從 0.12 到 0.15
        selection_width = min(400, int(self.screen_width * 0.5))

        for i, option in enumerate(self.menu_options):
            y_pos = start_y + i * option_spacing

            # 選中效果
            if i == self.selected_index:
                # 選中背景
                selection_rect = pygame.Rect(
                    self.screen_width // 2 - selection_width // 2,
                    y_pos - int(option_spacing * 0.35),  # 增加背景高度
                    selection_width,
                    int(option_spacing * 0.7),  # 增加背景高度
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

            option_rect = option_surface.get_rect(
                center=(self.screen_width // 2, y_pos)
            )
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
            desc_y = y_pos + int(option_spacing * 0.3)  # 調整描述位置
            desc_rect = desc_surface.get_rect(center=(self.screen_width // 2, desc_y))
            screen.blit(desc_surface, desc_rect)

    def _draw_controls(self, screen):
        """繪製控制說明"""
        control_text = "↑↓ 選擇難度  |  空白鍵/Enter 開始遊戲  |  F11 全螢幕"
        control_surface = self.fonts["small"].render(
            control_text, True, self.colors["WHITE"]
        )
        control_y = int(self.screen_height * 0.9)
        control_rect = control_surface.get_rect(
            center=(self.screen_width // 2, control_y)
        )
        screen.blit(control_surface, control_rect)

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
            preview_start_y = int(self.screen_height * 0.7)
            preview_line_spacing = int(self.screen_height * 0.025)

            for j, preview_text in enumerate(
                preview_texts[selected_option["difficulty"]]
            ):
                preview_surface = self.fonts["small"].render(
                    preview_text, True, self.colors["ORANGE"]
                )
                preview_y = preview_start_y + j * preview_line_spacing
                preview_rect = preview_surface.get_rect(
                    center=(self.screen_width // 2, preview_y)
                )
                screen.blit(preview_surface, preview_rect)

    def update_screen_size(self, screen_width, screen_height):
        """
        更新螢幕尺寸

        Args:
            screen_width (int): 新的螢幕寬度
            screen_height (int): 新的螢幕高度
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
