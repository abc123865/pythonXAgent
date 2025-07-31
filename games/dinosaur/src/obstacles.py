#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
障礙物系統
包含各種類型的障礙物和其行為
"""

import pygame
import random
import math
from config.game_config import get_color_palette


class Obstacle:
    """基礎障礙物類別"""

    def __init__(
        self,
        x=None,
        obstacle_type="normal",
        screen_width=800,
        screen_height=400,
        ground_height=350,
        is_gravity_reversed=False,
    ):
        """
        初始化障礙物

        Args:
            x (int): 障礙物的 x 座標
            obstacle_type (str): 障礙物類型
            screen_width (int): 螢幕寬度
            screen_height (int): 螢幕高度
            ground_height (int): 地面高度
            is_gravity_reversed (bool): 是否重力反轉
        """
        self.colors = get_color_palette()
        self.x = x if x is not None else screen_width
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ground_height = ground_height
        self.speed = 5
        self.obstacle_type = obstacle_type
        self.animation_counter = 0
        self.warning_time = 0
        self.is_warned = False
        self.health = 1
        self.setup_obstacle(is_gravity_reversed)

    def setup_obstacle(self, is_gravity_reversed=False):
        """根據障礙物類型設置屬性"""
        # 計算縮放因子
        scale_factor = min(self.screen_width / 800, self.screen_height / 400)

        if self.obstacle_type == "normal":
            # 普通仙人掌
            self.width = int(20 * scale_factor)
            self.height = int(30 * scale_factor)
            self.y = self.ground_height - self.height
            self.color = self.colors["BLACK"]

        elif self.obstacle_type == "tall":
            # 高仙人掌
            self.width = int(25 * scale_factor)
            self.height = int(50 * scale_factor)
            self.y = self.ground_height - self.height
            self.color = self.colors["BLACK"]

        elif self.obstacle_type == "wide":
            # 寬仙人掌
            self.width = int(35 * scale_factor)
            self.height = int(35 * scale_factor)
            self.y = self.ground_height - self.height
            self.color = self.colors["BLACK"]

        elif self.obstacle_type == "short":
            # 矮仙人掌（不需要跳躍，但噩夢模式下會變高）
            self.width = int(30 * scale_factor)
            # 根據螢幕高度動態調整 - 噩夢模式需要更高的石頭
            base_height = int(25 * scale_factor)  # 從15增加到25
            self.height = base_height
            self.y = self.ground_height - self.height
            self.color = self.colors["DARK_GREEN"]

        elif self.obstacle_type == "tall_rock":
            # 高石頭（需要蹲下才能通過）
            self.width = int(25 * scale_factor)
            self.height = int(55 * scale_factor)  # 比恐龍高，需要蹲下
            self.y = self.ground_height - self.height
            self.color = self.colors["GRAY"]

        elif self.obstacle_type == "hanging_rock":
            # 懸浮石頭（跳起來會撞到）
            self.width = int(30 * scale_factor)
            self.height = int(20 * scale_factor)
            if is_gravity_reversed:
                # 重力反轉時，懸浮石頭在地面附近
                self.y = self.ground_height - int(60 * scale_factor)
            else:
                # 正常重力時，懸浮石頭在空中低位置
                self.y = self.ground_height - int(90 * scale_factor)
            self.color = self.colors["DARK_GRAY"]

        elif self.obstacle_type == "flying":
            # 飛行障礙物（鳥類）
            self.width = int(25 * scale_factor)
            self.height = int(15 * scale_factor)
            if is_gravity_reversed:
                # 重力反轉時，飛行障礙物出現在天花板附近
                self.y = int(50 + random.randint(0, 30) * scale_factor)
            else:
                # 正常重力時，飛行障礙物在空中
                self.y = self.ground_height - int(80 * scale_factor)
            self.color = self.colors["GRAY"]

        elif self.obstacle_type == "double":
            # 雙重障礙物（上下兩個）
            self.width = int(20 * scale_factor)
            self.height = int(30 * scale_factor)
            self.y = self.ground_height - self.height
            self.color = self.colors["PURPLE"]
            if is_gravity_reversed:
                # 重力反轉時，雙重障礙物的上下位置對調
                self.upper_y = self.ground_height - int(60 * scale_factor)
                self.upper_height = int(25 * scale_factor)
                # 下方障礙物移到天花板附近
                self.lower_y = int(50 * scale_factor)
                self.lower_height = int(25 * scale_factor)
            else:
                self.upper_y = self.ground_height - int(100 * scale_factor)
                self.upper_height = int(25 * scale_factor)

        elif self.obstacle_type == "moving_up":
            # 上下移動的障礙物
            self.width = int(22 * scale_factor)
            self.height = int(40 * scale_factor)
            if is_gravity_reversed:
                # 重力反轉時，移動障礙物在天花板附近移動
                self.y = int(50 * scale_factor)
                self.original_y = self.y
                self.move_range = int(40 * scale_factor)
            else:
                self.y = self.ground_height - self.height
                self.original_y = self.y
                self.move_range = int(30 * scale_factor)
            self.color = self.colors["ORANGE"]
            self.move_speed = 2

        elif self.obstacle_type == "invisible":
            # 隱形障礙物（只在警告時可見）
            self.width = int(25 * scale_factor)
            self.height = int(35 * scale_factor)
            if is_gravity_reversed:
                # 重力反轉時，隱形障礙物在天花板附近
                self.y = int(50 * scale_factor)
            else:
                self.y = self.ground_height - self.height
            self.color = self.colors["RED"]
            self.warning_time = 90  # 1.5秒警告時間

        elif self.obstacle_type == "explosive":
            # 爆炸障礙物（碰撞後會擴散）
            self.width = int(30 * scale_factor)
            self.height = int(40 * scale_factor)
            if is_gravity_reversed:
                # 重力反轉時，爆炸障礙物在天花板附近
                self.y = int(50 * scale_factor)
            else:
                self.y = self.ground_height - self.height
            self.color = self.colors["RED"]
            self.explosion_radius = 0
            self.is_exploding = False

        elif self.obstacle_type == "armored":
            # 裝甲障礙物（需要多次攻擊）
            self.width = int(35 * scale_factor)
            self.height = int(45 * scale_factor)
            if is_gravity_reversed:
                # 重力反轉時，裝甲障礙物在天花板附近
                self.y = int(50 * scale_factor)
            else:
                self.y = self.ground_height - self.height
            self.color = self.colors["BLUE"]
            self.health = 3
            self.original_color = self.colors["BLUE"]

        elif self.obstacle_type == "meteor":
            # 隕石障礙物（從天而降，非常危險但可被護盾阻擋）
            self.width = int(50 * scale_factor)  # 增大隕石尺寸
            self.height = int(55 * scale_factor)
            if is_gravity_reversed:
                # 重力反轉時，隕石從地面向上飛
                self.y = self.ground_height
                self.fall_speed = -6 * scale_factor  # 稍微慢一點，更容易躲避
            else:
                # 正常重力時，隕石從天空墜落
                self.y = int(-60 * scale_factor)
                self.fall_speed = 6 * scale_factor  # 稍微慢一點，更容易躲避
            self.color = self.colors["ORANGE"]
            self.warning_time = 200  # 增加到3.3秒警告時間，讓玩家有更多反應時間
            self.is_warned = True
            self.warning_sound_played = False  # 確保警告音效只播放一次
            self.fire_trail = []  # 火焰尾跡
            self.impact_effect = 0  # 撞擊效果
            self.has_landed = False
            # 為隕石生成固定的裂紋圖案
            random.seed(hash((self.x, self.obstacle_type)) % 1000)  # 使用位置作為種子
            self.crack_pattern = []
            for i in range(4):
                start_x = 5 + random.randint(0, self.width - 10)
                start_y = 5 + random.randint(0, self.height - 10)
                end_x = start_x + random.randint(-8, 8)
                end_y = start_y + random.randint(-8, 8)
                self.crack_pattern.append(((start_x, start_y), (end_x, end_y)))
            random.seed()  # 重置隨機種子

    def update(self):
        """更新障礙物狀態"""
        self.animation_counter += 1
        self.x -= self.speed

        # 特殊障礙物的更新邏輯
        if self.obstacle_type == "moving_up":
            # 上下移動邏輯
            move_offset = math.sin(self.animation_counter * 0.1) * self.move_range

            # 根據是否在天花板附近調整移動方向
            if self.original_y <= 100:  # 天花板附近（重力反轉）
                # 向下移動
                self.y = self.original_y + abs(move_offset)
            else:  # 地面附近（正常重力）
                # 向上移動
                self.y = self.original_y - abs(move_offset)

        elif self.obstacle_type == "invisible":
            # 隱形障礙物警告邏輯
            if self.warning_time > 0:
                self.warning_time -= 1
                self.is_warned = True
            else:
                self.is_warned = False

        elif self.obstacle_type == "explosive" and self.is_exploding:
            # 爆炸效果
            self.explosion_radius += 3
            if self.explosion_radius > 60:
                self.is_exploding = False

        elif self.obstacle_type == "meteor":
            # 隕石墜落邏輯
            if self.warning_time > 0:
                self.warning_time -= 1
            else:
                # 開始墜落/上升
                self.y += self.fall_speed

                # 更新火焰尾跡
                self.fire_trail.append(
                    (self.x + self.width // 2, self.y + self.height // 2)
                )
                if len(self.fire_trail) > 8:
                    self.fire_trail.pop(0)

                # 檢查是否撞擊地面/天花板
                if not self.has_landed:
                    if (
                        not hasattr(self, "fall_speed") or self.fall_speed > 0
                    ):  # 向下墜落
                        if self.y >= self.ground_height - self.height:
                            self.y = self.ground_height - self.height
                            self.has_landed = True
                            self.impact_effect = 30  # 撞擊效果持續時間
                            # 隕石撞擊需要通過外部方式播放音效，這裡只設置標記
                            self.just_landed = True
                    else:  # 向上飛行（重力反轉）
                        if self.y <= 50:
                            self.y = 50
                            self.has_landed = True
                            self.impact_effect = 30
                            self.just_landed = True

                # 撞擊效果遞減
                if self.impact_effect > 0:
                    self.impact_effect -= 1

    def draw(self, screen):
        """繪製障礙物"""
        if self.obstacle_type == "flying":
            self._draw_flying_obstacle(screen)
        elif self.obstacle_type == "short":
            self._draw_short_obstacle(screen)
        elif self.obstacle_type == "tall_rock":
            self._draw_tall_rock(screen)
        elif self.obstacle_type == "hanging_rock":
            self._draw_hanging_rock(screen)
        elif self.obstacle_type == "double":
            self._draw_double_obstacle(screen)
        elif self.obstacle_type == "moving_up":
            self._draw_moving_obstacle(screen)
        elif self.obstacle_type == "invisible":
            self._draw_invisible_obstacle(screen)
        elif self.obstacle_type == "explosive":
            self._draw_explosive_obstacle(screen)
        elif self.obstacle_type == "armored":
            self._draw_armored_obstacle(screen)
        elif self.obstacle_type == "meteor":
            self._draw_meteor_obstacle(screen)
        else:
            self._draw_normal_obstacle(screen)

    def _draw_flying_obstacle(self, screen):
        """繪製飛行障礙物"""
        # 鳥形
        pygame.draw.ellipse(
            screen, self.color, (self.x, self.y, self.width, self.height)
        )
        # 翅膀
        pygame.draw.ellipse(screen, self.color, (self.x - 5, self.y + 3, 15, 8))
        pygame.draw.ellipse(screen, self.color, (self.x + 15, self.y + 3, 15, 8))

    def _draw_short_obstacle(self, screen):
        """繪製矮障礙物"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # 石頭細節
        pygame.draw.circle(screen, self.colors["GREEN"], (self.x + 5, self.y + 5), 3)
        pygame.draw.circle(screen, self.colors["GREEN"], (self.x + 20, self.y + 8), 2)

    def _draw_tall_rock(self, screen):
        """繪製高石頭（需要蹲下通過）"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # 高石頭的紋理
        for i in range(3):
            y_offset = i * (self.height // 3)
            pygame.draw.line(
                screen,
                self.colors["WHITE"],
                (self.x, self.y + y_offset + 5),
                (self.x + self.width, self.y + y_offset + 5),
                1,
            )
        # 頂部標記
        pygame.draw.rect(
            screen, self.colors["DARK_GRAY"], (self.x + 5, self.y, self.width - 10, 8)
        )

    def _draw_hanging_rock(self, screen):
        """繪製懸浮石頭（跳起來會撞到）"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # 懸浮效果 - 陰影
        shadow_y = self.y + self.height + 5
        pygame.draw.ellipse(
            screen,
            self.colors["BLACK"],
            (self.x + 3, shadow_y, self.width - 6, 8),
        )
        # 懸浮石頭的邊框
        pygame.draw.rect(
            screen, self.colors["WHITE"], (self.x, self.y, self.width, self.height), 2
        )
        # 危險標記
        pygame.draw.polygon(
            screen,
            self.colors["RED"],
            [
                (self.x + self.width // 2, self.y - 8),
                (self.x + self.width // 2 - 5, self.y - 3),
                (self.x + self.width // 2 + 5, self.y - 3),
            ],
        )

    def _draw_double_obstacle(self, screen):
        """繪製雙重障礙物"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(
            screen, self.color, (self.x, self.upper_y, self.width, self.upper_height)
        )

        # 如果有下方障礙物（重力反轉模式）
        if hasattr(self, "lower_y"):
            pygame.draw.rect(
                screen,
                self.color,
                (self.x, self.lower_y, self.width, self.lower_height),
            )

        # 連接線
        pygame.draw.line(
            screen,
            self.color,
            (self.x + self.width // 2, self.y),
            (self.x + self.width // 2, self.upper_y + self.upper_height),
            3,
        )

    def _draw_moving_obstacle(self, screen):
        """繪製移動障礙物"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # 移動指示器
        pygame.draw.polygon(
            screen,
            self.colors["YELLOW"],
            [
                (self.x + self.width // 2, self.y - 10),
                (self.x + self.width // 2 - 5, self.y - 5),
                (self.x + self.width // 2 + 5, self.y - 5),
            ],
        )

    def _draw_invisible_obstacle(self, screen):
        """繪製隱形障礙物"""
        if self.is_warned:
            # 閃爍效果
            alpha = 100 + int(50 * math.sin(self.animation_counter * 0.3))
            warning_surface = pygame.Surface((self.width + 10, self.height + 10))
            warning_surface.set_alpha(alpha)
            warning_surface.fill(self.colors["RED"])
            screen.blit(warning_surface, (self.x - 5, self.y - 5))
            # 警告標記
            pygame.draw.rect(
                screen,
                self.colors["YELLOW"],
                (self.x, self.y, self.width, self.height),
                3,
            )

    def _draw_explosive_obstacle(self, screen):
        """繪製爆炸障礙物"""
        if self.is_exploding:
            # 爆炸效果
            for i in range(5):
                radius = self.explosion_radius - i * 10
                if radius > 0:
                    alpha = max(0, 255 - i * 50)
                    explosion_surface = pygame.Surface((radius * 2, radius * 2))
                    explosion_surface.set_alpha(alpha)
                    explosion_surface.fill(self.colors["ORANGE"])
                    screen.blit(
                        explosion_surface,
                        (
                            self.x + self.width // 2 - radius,
                            self.y + self.height // 2 - radius,
                        ),
                    )
        else:
            pygame.draw.rect(
                screen, self.color, (self.x, self.y, self.width, self.height)
            )
            # 爆炸符號
            pygame.draw.circle(
                screen,
                self.colors["YELLOW"],
                (self.x + self.width // 2, self.y + self.height // 2),
                8,
            )
            pygame.draw.circle(
                screen,
                self.colors["RED"],
                (self.x + self.width // 2, self.y + self.height // 2),
                5,
            )

    def _draw_armored_obstacle(self, screen):
        """繪製裝甲障礙物"""
        # 根據生命值改變顏色
        if self.health == 3:
            current_color = self.colors["BLUE"]
        elif self.health == 2:
            current_color = self.colors["PURPLE"]
        else:
            current_color = self.colors["RED"]

        pygame.draw.rect(
            screen, current_color, (self.x, self.y, self.width, self.height)
        )

        # 裝甲線條
        for i in range(3):
            y_offset = i * (self.height // 3)
            pygame.draw.line(
                screen,
                self.colors["WHITE"],
                (self.x, self.y + y_offset),
                (self.x + self.width, self.y + y_offset),
                2,
            )

        # 生命值顯示
        for i in range(self.health):
            pygame.draw.circle(
                screen, self.colors["WHITE"], (self.x + 5 + i * 8, self.y + 5), 3
            )

    def _draw_meteor_obstacle(self, screen):
        """繪製隕石障礙物"""
        if self.warning_time > 0:
            # 警告階段 - 顯示隕石即將墜落的位置，效果更明顯

            # 多層警告效果
            for layer in range(3):
                warning_alpha = int(
                    80 + 150 * math.sin(self.animation_counter * 0.3 + layer * 0.5)
                )
                warning_size = (
                    self.width + 30 + layer * 10,
                    self.height + 30 + layer * 10,
                )
                warning_surface = pygame.Surface(warning_size)
                warning_surface.set_alpha(warning_alpha)
                warning_surface.fill(
                    self.colors["RED"] if layer % 2 == 0 else self.colors["ORANGE"]
                )

                # 計算警告位置
                if hasattr(self, "fall_speed") and self.fall_speed < 0:  # 重力反轉
                    warning_y = 50 - 15 - layer * 5
                else:  # 正常重力
                    warning_y = self.ground_height - self.height - 15 - layer * 5

                warning_x = self.x - 15 - layer * 5
                screen.blit(warning_surface, (warning_x, warning_y))

            # 更大更明顯的警告文字
            warning_text = "☄️ 危險！"
            font = pygame.font.Font(None, 48)  # 更大的字體
            text_surface = font.render(warning_text, True, self.colors["YELLOW"])
            text_x = self.x + self.width // 2 - text_surface.get_width() // 2
            if hasattr(self, "fall_speed") and self.fall_speed < 0:
                text_y = 60
            else:
                text_y = self.ground_height - self.height - 50
            screen.blit(text_surface, (text_x, text_y))

            # 添加閃爍的邊框
            if int(self.animation_counter / 10) % 2 == 0:
                border_rect = pygame.Rect(
                    self.x - 20,
                    (
                        warning_y
                        if hasattr(self, "fall_speed") and self.fall_speed >= 0
                        else 40
                    ),
                    self.width + 40,
                    self.height + 40,
                )
                pygame.draw.rect(screen, self.colors["YELLOW"], border_rect, 5)
        else:
            # 墜落階段 - 繪製隕石本體

            # 繪製火焰尾跡
            for i, (trail_x, trail_y) in enumerate(self.fire_trail):
                trail_alpha = int(255 * (i + 1) / len(self.fire_trail))
                trail_size = max(4, (i + 1) * 3)  # 更大的火焰尾跡

                # 創建帶透明度的火焰效果
                trail_surface = pygame.Surface((trail_size * 2, trail_size * 2))
                trail_surface.set_alpha(trail_alpha)
                trail_surface.fill(
                    self.colors["ORANGE"] if i % 2 == 0 else self.colors["RED"]
                )
                screen.blit(trail_surface, (trail_x - trail_size, trail_y - trail_size))

            # 隕石本體 - 石頭質感
            pygame.draw.ellipse(
                screen,
                self.colors["DARK_GRAY"],
                (self.x, self.y, self.width, self.height),
            )

            # 隕石的發光邊緣
            pygame.draw.ellipse(
                screen,
                self.colors["ORANGE"],
                (self.x, self.y, self.width, self.height),
                3,
            )

            # 隕石表面的裂紋
            if hasattr(self, "crack_pattern"):
                for (start_x, start_y), (end_x, end_y) in self.crack_pattern:
                    pygame.draw.line(
                        screen,
                        self.colors["BLACK"],
                        (self.x + start_x, self.y + start_y),
                        (self.x + end_x, self.y + end_y),
                        2,
                    )

            # 撞擊效果
            if self.impact_effect > 0:
                impact_radius = int((30 - self.impact_effect) * 2)
                if impact_radius > 0:
                    impact_surface = pygame.Surface(
                        (impact_radius * 2, impact_radius * 2)
                    )
                    impact_alpha = int(self.impact_effect * 8)
                    impact_surface.set_alpha(impact_alpha)
                    impact_surface.fill(self.colors["YELLOW"])
                    screen.blit(
                        impact_surface,
                        (
                            self.x + self.width // 2 - impact_radius,
                            self.y + self.height // 2 - impact_radius,
                        ),
                    )

    def _draw_normal_obstacle(self, screen):
        """繪製普通障礙物"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        if self.obstacle_type == "tall":
            # 高仙人掌添加分支
            pygame.draw.rect(screen, self.color, (self.x - 8, self.y + 15, 15, 8))
            pygame.draw.rect(screen, self.color, (self.x + 18, self.y + 20, 15, 8))
        elif self.obstacle_type == "wide":
            # 寬仙人掌添加更多分支
            pygame.draw.rect(screen, self.color, (self.x - 5, self.y + 10, 12, 6))
            pygame.draw.rect(screen, self.color, (self.x + 28, self.y + 15, 12, 6))

    def get_collision_rect(self):
        """獲取碰撞檢測矩形"""
        if self.obstacle_type == "double":
            # 雙重障礙物需要返回多個碰撞矩形
            rects = [pygame.Rect(self.x, self.y, self.width, self.height)]
            rects.append(
                pygame.Rect(self.x, self.upper_y, self.width, self.upper_height)
            )

            # 重力反轉時的下方障礙物
            if hasattr(self, "lower_y"):
                rects.append(
                    pygame.Rect(self.x, self.lower_y, self.width, self.lower_height)
                )

            return rects
        else:
            return pygame.Rect(self.x, self.y, self.width, self.height)

    def can_duck_under(self):
        """檢查是否可以蹲下通過"""
        return self.obstacle_type in ["flying"]

    def can_walk_through(self, difficulty=None):
        """
        檢查是否可以直接走過

        Args:
            difficulty: 當前遊戲難度，噩夢模式下矮障礙物不能走過
        """
        from config.game_config import Difficulty

        if self.obstacle_type == "short":
            # 噩夢模式下，矮障礙物變高，不能直接走過
            if difficulty == Difficulty.NIGHTMARE:
                return False
            else:
                return True
        elif self.obstacle_type == "hanging_rock":
            # 懸浮石頭可以直接走過（不跳躍的情況下）
            return True
        return False

    def trigger_explosion(self):
        """觸發爆炸效果"""
        if self.obstacle_type == "explosive":
            self.is_exploding = True

    def take_damage(self):
        """受到傷害"""
        if self.obstacle_type == "armored":
            self.health -= 1
            return self.health <= 0
        return True


class ObstacleManager:
    """障礙物管理器"""

    def __init__(self, screen_width, screen_height, ground_height):
        """
        初始化障礙物管理器

        Args:
            screen_width (int): 螢幕寬度
            screen_height (int): 螢幕高度
            ground_height (int): 地面高度
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ground_height = ground_height
        self.obstacles = []
        self.spawn_timer = 0

    def get_obstacle_types_for_difficulty(self, difficulty, is_gravity_reversed=False):
        """
        根據難度獲取可用的障礙物類型

        Args:
            difficulty (int): 難度等級
            is_gravity_reversed (bool): 是否重力反轉

        Returns:
            list: 可用的障礙物類型列表
        """
        from config.game_config import Difficulty

        if difficulty == Difficulty.EASY:
            obstacle_types = ["normal", "tall", "wide", "short"]  # 移除隕石
            if is_gravity_reversed:
                obstacle_types = ["flying", "short", "normal"]
        elif difficulty == Difficulty.MEDIUM:
            obstacle_types = [
                "normal",
                "tall",
                "wide",
                "short",
                "flying",
                "tall_rock",
            ]  # 移除隕石
            if is_gravity_reversed:
                obstacle_types = ["flying", "flying", "short", "normal"]
        elif difficulty == Difficulty.HARD:
            obstacle_types = [
                "normal",
                "tall",
                "wide",
                "short",
                "flying",
                "double",
                "tall_rock",
                "hanging_rock",
                # 移除所有隕石
            ]
            if is_gravity_reversed:
                obstacle_types = [
                    "flying",
                    "flying",
                    "double",
                    "short",
                    "normal",
                    "hanging_rock",
                    # 移除隕石
                ]
        else:  # NIGHTMARE - 保持簡單但速度極快
            obstacle_types = [
                "normal",
                "tall",
                "wide",
                "flying",
                "double",
                "tall_rock",
                "hanging_rock",
                # 移除所有隕石
            ]
            if is_gravity_reversed:
                obstacle_types = [
                    "flying",
                    "flying",
                    "flying",
                    "double",
                    "normal",
                    "hanging_rock",
                    # 移除隕石
                ]

        return obstacle_types

    def spawn_obstacle(
        self,
        difficulty,
        obstacle_spawn_rate,
        is_gravity_reversed=False,
        sound_manager=None,
    ):
        """
        生成新的障礙物

        Args:
            difficulty (int): 難度等級
            obstacle_spawn_rate (float): 障礙物生成速率
            is_gravity_reversed (bool): 是否重力反轉
            sound_manager: 音效管理器（可選）
        """
        if self.spawn_timer <= 0:
            obstacle_types = self.get_obstacle_types_for_difficulty(
                difficulty, is_gravity_reversed
            )
            obstacle_type = random.choice(obstacle_types)

            new_obstacle = Obstacle(
                obstacle_type=obstacle_type,
                screen_width=self.screen_width,
                screen_height=self.screen_height,
                ground_height=self.ground_height,
                is_gravity_reversed=is_gravity_reversed,
            )

            self.obstacles.append(new_obstacle)

            # 如果生成的是隕石，不在這裡播放音效，而是在更新時播放
            # 這樣可以讓音效和視覺效果同步

            # 根據難度調整生成間隔，簡化邏輯
            base_interval = max(20, int(100 / obstacle_spawn_rate))
            interval_variation = max(10, int(30 / obstacle_spawn_rate))

            self.spawn_timer = random.randint(
                base_interval, base_interval + interval_variation
            )
        else:
            self.spawn_timer -= 1

    def update(self, game_speed, sound_manager=None):
        """
        更新所有障礙物

        Args:
            game_speed (float): 遊戲速度
            sound_manager: 音效管理器（可選）
        """
        for obstacle in self.obstacles[:]:
            obstacle.speed = game_speed
            obstacle.update()

            if obstacle.x + obstacle.width < 0:
                self.obstacles.remove(obstacle)

    def draw(self, screen):
        """繪製所有障礙物"""
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def clear(self):
        """清除所有障礙物"""
        self.obstacles.clear()
        self.spawn_timer = 0
