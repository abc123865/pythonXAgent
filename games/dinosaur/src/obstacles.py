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
            # 矮仙人掌（不需要跳躍）
            self.width = int(30 * scale_factor)
            self.height = int(15 * scale_factor)
            self.y = self.ground_height - self.height
            self.color = self.colors["DARK_GREEN"]

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

    def draw(self, screen):
        """繪製障礙物"""
        if self.obstacle_type == "flying":
            self._draw_flying_obstacle(screen)
        elif self.obstacle_type == "short":
            self._draw_short_obstacle(screen)
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

    def can_walk_through(self):
        """檢查是否可以直接走過"""
        return self.obstacle_type in ["short"]

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
            obstacle_types = ["normal", "tall", "wide", "short", "flying"]
            if is_gravity_reversed:
                obstacle_types = ["flying", "flying", "short", "normal", "wide"]
        elif difficulty == Difficulty.MEDIUM:
            obstacle_types = ["normal", "tall", "wide", "short", "flying", "double"]
            if is_gravity_reversed:
                obstacle_types = [
                    "flying",
                    "flying",
                    "flying",
                    "double",
                    "short",
                    "normal",
                ]
        elif difficulty == Difficulty.HARD:
            obstacle_types = [
                "normal",
                "tall",
                "wide",
                "short",
                "flying",
                "double",
                "moving_up",
                "explosive",
            ]
            if is_gravity_reversed:
                obstacle_types = [
                    "flying",
                    "flying",
                    "flying",
                    "double",
                    "moving_up",
                    "explosive",
                    "short",
                    "normal",
                ]
        else:  # NIGHTMARE
            obstacle_types = [
                "normal",
                "tall",
                "wide",
                "short",
                "flying",
                "double",
                "moving_up",
                "invisible",
                "explosive",
                "armored",
            ]
            if is_gravity_reversed:
                obstacle_types = [
                    "flying",
                    "flying",
                    "flying",
                    "flying",
                    "double",
                    "moving_up",
                    "invisible",
                    "explosive",
                    "armored",
                    "short",
                ]

        return obstacle_types

    def spawn_obstacle(
        self, difficulty, obstacle_spawn_rate, is_gravity_reversed=False
    ):
        """
        生成新的障礙物

        Args:
            difficulty (int): 難度等級
            obstacle_spawn_rate (float): 障礙物生成速率
            is_gravity_reversed (bool): 是否重力反轉
        """
        if self.spawn_timer <= 0:
            obstacle_types = self.get_obstacle_types_for_difficulty(
                difficulty, is_gravity_reversed
            )
            obstacle_type = random.choice(obstacle_types)

            # 在重力反轉時，有機會同時生成多個空中障礙物
            if is_gravity_reversed and random.randint(1, 3) == 1:
                self.obstacles.append(
                    Obstacle(
                        obstacle_type="flying",
                        screen_width=self.screen_width,
                        screen_height=self.screen_height,
                        ground_height=self.ground_height,
                        is_gravity_reversed=is_gravity_reversed,
                    )
                )

            self.obstacles.append(
                Obstacle(
                    obstacle_type=obstacle_type,
                    screen_width=self.screen_width,
                    screen_height=self.screen_height,
                    ground_height=self.ground_height,
                    is_gravity_reversed=is_gravity_reversed,
                )
            )  # 根據難度調整生成間隔
            base_interval = max(15, int(120 / obstacle_spawn_rate))
            interval_variation = max(5, int(40 / obstacle_spawn_rate))

            # 重力反轉時縮短生成間隔
            if is_gravity_reversed:
                base_interval = int(base_interval * 0.7)
                interval_variation = int(interval_variation * 0.7)

            self.spawn_timer = random.randint(
                base_interval, base_interval + interval_variation
            )
        else:
            self.spawn_timer -= 1

    def update(self, game_speed):
        """
        更新所有障礙物

        Args:
            game_speed (float): 遊戲速度
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
