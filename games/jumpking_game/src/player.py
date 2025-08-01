#!/usr/bin/env python3
"""
Jump King 玩家類別
處理玩家的移動、跳躍和碰撞檢測
"""
import pygame
import math
import random
from game_config import *


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = True
        self.jump_charging = False
        self.jump_power = 0
        self.facing_right = True
        self.start_x = x
        self.start_y = y
        self.death_count = 0

    def reset_position(self):
        """重置玩家位置到關卡起點"""
        self.x = self.start_x
        self.y = self.start_y
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = True
        self.jump_charging = False
        self.jump_power = 0
        self.death_count += 1

    def set_start_position(self, x, y):
        """設置新的起點位置"""
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = True

    def update(self, platforms, death_zones=None, level_num=None):
        """更新玩家狀態"""
        # 處理重力
        if not self.on_ground:
            self.vel_y += GRAVITY
            if self.vel_y > MAX_FALL_SPEED:
                self.vel_y = MAX_FALL_SPEED

        # 更新位置
        self.x += self.vel_x
        self.y += self.vel_y

        # 檢查屏幕邊界並反彈
        self.check_screen_boundaries()

        # 特殊處理第11關的掉落機制
        if level_num == 11 and self.y > 400:
            if self.vel_y > 10:  # 高速墜落時
                danger_zones = [
                    (90, 160),  # 第一個危險區域
                    (240, 310),  # 第二個危險區域
                    (490, 560),  # 第三個危險區域
                    (740, 810),  # 第四個危險區域
                ]

                for min_x, max_x in danger_zones:
                    if min_x <= self.x + self.width / 2 <= max_x:
                        if random.random() < 0.15:  # 15%機率
                            # 直接掉到底部
                            self.y = 500
                            self.vel_y = 0
                            self.reset_position()
                            return "fall_trap"

        # 檢查死亡區域
        if death_zones:
            for zone in death_zones:
                if (
                    self.x < zone["x"] + zone["width"]
                    and self.x + self.width > zone["x"]
                    and self.y < zone["y"] + zone["height"]
                    and self.y + self.height > zone["y"]
                ):
                    return "death"

        # 檢查平台碰撞
        self.check_platform_collision(platforms)

        # 減少水平速度（摩擦力）
        if self.on_ground:
            self.vel_x *= 0.8
        else:
            self.vel_x *= 0.95

        return None

    def check_screen_boundaries(self):
        """檢查屏幕邊界並處理反彈"""
        wall_width = 10

        # 左邊界
        if self.x <= wall_width:
            self.x = wall_width
            if self.vel_x < 0:
                self.vel_x = -self.vel_x * 0.7

        # 右邊界
        if self.x + self.width >= SCREEN_WIDTH - wall_width:
            self.x = SCREEN_WIDTH - wall_width - self.width
            if self.vel_x > 0:
                self.vel_x = -self.vel_x * 0.7

    def check_platform_collision(self, platforms):
        """檢查平台碰撞"""
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        ground_detected = False

        for platform in platforms:
            platform_rect = pygame.Rect(
                platform["x"], platform["y"], platform["width"], platform["height"]
            )

            if player_rect.colliderect(platform_rect):
                # 計算重疊
                overlap_left = (self.x + self.width) - platform["x"]
                overlap_right = (platform["x"] + platform["width"]) - self.x
                overlap_top = (self.y + self.height) - platform["y"]
                overlap_bottom = (platform["y"] + platform["height"]) - self.y

                # 找出最小重疊方向
                min_overlap = min(
                    overlap_left, overlap_right, overlap_top, overlap_bottom
                )

                if min_overlap == overlap_top and self.vel_y >= 0:
                    # 從上方落下
                    self.y = platform["y"] - self.height
                    self.vel_y = 0
                    ground_detected = True
                elif min_overlap == overlap_bottom and self.vel_y <= 0:
                    # 從下方撞擊
                    self.y = platform["y"] + platform["height"]
                    self.vel_y = 0
                elif min_overlap == overlap_left and self.vel_x >= 0:
                    # 從左側撞擊平台
                    self.x = platform["x"] - self.width
                    self.vel_x = -self.vel_x * 0.6
                elif min_overlap == overlap_right and self.vel_x <= 0:
                    # 從右側撞擊平台
                    self.x = platform["x"] + platform["width"]
                    self.vel_x = -self.vel_x * 0.6

        # 詳細地面檢測
        if not ground_detected:
            for platform in platforms:
                # 檢查水平重疊
                if (
                    self.x < platform["x"] + platform["width"]
                    and self.x + self.width > platform["x"]
                ):
                    # 檢查垂直接觸
                    platform_top = platform["y"]
                    player_bottom = self.y + self.height
                    if abs(player_bottom - platform_top) <= 3 and self.vel_y >= -0.5:
                        ground_detected = True
                        self.y = platform_top - self.height
                        self.vel_y = 0
                        break

        self.on_ground = ground_detected

    def start_jump_charge(self):
        """開始跳躍蓄力"""
        self.jump_charging = True
        self.jump_power = MIN_JUMP_POWER

    def update_jump_charge(self):
        """更新跳躍蓄力"""
        if self.jump_charging:
            self.jump_power += JUMP_CHARGE_RATE
            if self.jump_power > MAX_JUMP_POWER:
                self.jump_power = MAX_JUMP_POWER

    def execute_jump(self, direction):
        """執行跳躍"""
        if self.jump_charging and self.on_ground:
            # 計算跳躍向量
            angle = 0
            if direction == "left":
                angle = 120  # 左上
                self.facing_right = False
            elif direction == "right":
                angle = 60  # 右上
                self.facing_right = True
            else:  # 直接向上
                angle = 90

            # 轉換為弧度
            angle_rad = math.radians(angle)

            # 應用跳躍力
            jump_force = self.jump_power * 1.2
            self.vel_x = math.cos(angle_rad) * jump_force
            self.vel_y = math.sin(angle_rad) * -jump_force

            # 重置跳躍狀態
            self.jump_charging = False
            self.jump_power = 0
            self.on_ground = False
        else:
            # 即使無法跳躍也要重置蓄力狀態
            if self.jump_charging:
                self.jump_charging = False
                self.jump_power = 0

    def draw(self, screen, camera_y):
        """繪製玩家"""
        # 計算玩家顏色
        player_color = PLAYER_COLOR
        if self.jump_charging:
            charge_ratio = (self.jump_power - MIN_JUMP_POWER) / (
                MAX_JUMP_POWER - MIN_JUMP_POWER
            )
            red_component = min(255, int(100 + charge_ratio * 155))
            player_color = (red_component, 100, 237)

        # 繪製玩家
        pygame.draw.rect(
            screen, player_color, (self.x, self.y - camera_y, self.width, self.height)
        )

        # 繪製面向方向指示
        eye_x = self.x + (20 if self.facing_right else 10)
        eye_y = self.y - camera_y + 10
        pygame.draw.circle(screen, WHITE, (eye_x, eye_y), 3)

        # 繪製蓄力指示器
        if self.jump_charging:
            charge_ratio = (self.jump_power - MIN_JUMP_POWER) / (
                MAX_JUMP_POWER - MIN_JUMP_POWER
            )
            bar_width = 40
            bar_height = 8
            bar_x = self.x - 5
            bar_y = self.y - camera_y - 15

            # 背景
            pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))

            # 蓄力條
            charge_width = int(bar_width * charge_ratio)
            charge_color = (
                RED if charge_ratio > 0.8 else YELLOW if charge_ratio > 0.5 else GREEN
            )
            pygame.draw.rect(
                screen, charge_color, (bar_x, bar_y, charge_width, bar_height)
            )
