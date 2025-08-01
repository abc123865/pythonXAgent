#!/usr/bin/env python3
"""
Jump King 渲染器
處理遊戲的視覺效果和繪製
"""
import pygame
import time
from game_config import *


class Renderer:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.camera_y = 0

    def update_camera(self, player):
        """更新相機位置"""
        if player:
            target_y = player.y - SCREEN_HEIGHT // 2
            self.camera_y += (target_y - self.camera_y) * 0.1

    def draw_platforms(self, screen, platforms, goal_y):
        """繪製平台"""
        for platform in platforms:
            color = BROWN
            if platform["y"] <= goal_y:  # 目標平台
                color = YELLOW

            pygame.draw.rect(
                screen,
                color,
                (
                    platform["x"],
                    platform["y"] - self.camera_y,
                    platform["width"],
                    platform["height"],
                ),
            )

    def draw_death_zones(self, screen, death_zones):
        """繪製死亡區域"""
        for zone in death_zones:
            pygame.draw.rect(
                screen,
                RED,
                (
                    zone["x"],
                    zone["y"] - self.camera_y,
                    zone["width"],
                    zone["height"],
                ),
            )

    def draw_level11_effects(self, screen):
        """繪製第11關特殊視覺效果"""
        danger_zones = [
            (90, 160, 480, 20),  # x_min, x_max, y, height
            (240, 310, 380, 20),
            (490, 560, 280, 20),
            (740, 810, 200, 20),
        ]

        # 讓警告區域閃爍
        alpha = int(128 + 127 * abs((time.time() * 3) % 2 - 1))

        for min_x, max_x, y, height in danger_zones:
            # 創建一個有透明度的表面
            warning_surface = pygame.Surface((max_x - min_x, height))
            warning_surface.set_alpha(alpha)
            warning_surface.fill(ORANGE)
            screen.blit(warning_surface, (min_x, y - self.camera_y))

    def draw_screen_boundaries(self, screen):
        """繪製屏幕邊界牆壁"""
        wall_width = 10
        # 左邊界牆壁
        pygame.draw.rect(screen, GRAY, (0, 0, wall_width, SCREEN_HEIGHT))
        # 右邊界牆壁
        pygame.draw.rect(
            screen, GRAY, (SCREEN_WIDTH - wall_width, 0, wall_width, SCREEN_HEIGHT)
        )

    def draw_game_scene(self, screen, level_data, player, current_level):
        """繪製遊戲場景"""
        screen.fill(DARK_BLUE)

        # 繪製屏幕邊界
        self.draw_screen_boundaries(screen)

        # 繪製平台
        self.draw_platforms(screen, level_data["platforms"], level_data["goal_y"])

        # 繪製死亡區域
        self.draw_death_zones(screen, level_data["death_zones"])

        # 第11關特殊效果
        if current_level == 11:
            self.draw_level11_effects(screen)

        # 更新相機
        self.update_camera(player)

        # 繪製玩家
        if player:
            player.draw(screen, self.camera_y)

    def check_goal_completion(self, player, level_data):
        """檢查玩家是否踩在目標平台上"""
        if not player or not player.on_ground:
            return False

        # 找到目標平台
        goal_platforms = []
        for platform in level_data["platforms"]:
            if platform["y"] <= level_data["goal_y"]:
                goal_platforms.append(platform)

        # 檢查玩家是否踩在任何目標平台上
        for platform in goal_platforms:
            # 檢查玩家底部是否接觸平台頂部
            if (
                player.x < platform["x"] + platform["width"]
                and player.x + player.width > platform["x"]
                and abs((player.y + player.height) - platform["y"]) <= 3
                and player.on_ground
            ):
                return True

        return False
