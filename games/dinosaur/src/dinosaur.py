#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恐龍角色類別
處理恐龍的移動、技能和狀態
"""

import pygame
import math
import random
from config.game_config import Physics, get_color_palette


class Dinosaur:
    """恐龍玩家角色"""

    def __init__(self, screen_width, screen_height, ground_height):
        """
        初始化恐龍

        Args:
            screen_width (int): 螢幕寬度
            screen_height (int): 螢幕高度
            ground_height (int): 地面高度
        """
        self.colors = get_color_palette()

        # 螢幕尺寸
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ground_height = ground_height

        # 動態位置和大小
        scale_factor = min(screen_width / 800, screen_height / 400)
        self.x = int(80 * scale_factor)
        self.width = int(40 * scale_factor)
        self.height = int(40 * scale_factor)
        self.original_height = self.height
        self.y = ground_height - self.height

        # 物理屬性
        self.jump_speed = 0
        self.gravity = Physics.GRAVITY * scale_factor
        self.is_jumping = False
        self.is_ducking = False
        self.jump_strength = Physics.JUMP_STRENGTH * scale_factor

        # 特殊技能
        self.dash_cooldown = 0
        self.dash_distance = 0
        self.is_dashing = False
        self.shield_time = 0
        self.has_shield = False
        self.double_jump_available = False
        self.animation_frame = 0

        # 噩夢模式效果
        self.gravity_reversal_time = 0
        self.is_gravity_reversed = False
        self.control_inversion_time = 0
        self.is_control_inverted = False
        self.ability_malfunction_time = 0
        self.nightmare_effects = {
            "screen_flicker": 0,
            "gravity_chaos": 0,
            "time_distortion": 1.0,
            "ability_curse": 0,
        }

    def jump(self):
        """執行跳躍動作"""
        # 檢查能力是否故障
        if self.ability_malfunction_time > 0:
            return

        if not self.is_jumping and not self.is_ducking:
            # 根據重力狀態調整跳躍
            jump_strength = self.jump_strength
            if self.is_gravity_reversed:
                jump_strength = -jump_strength

            self.jump_speed = jump_strength
            self.is_jumping = True
            self.double_jump_available = True
        elif self.is_jumping and self.double_jump_available:
            # 二段跳
            jump_strength = self.jump_strength * 0.8
            if self.is_gravity_reversed:
                jump_strength = -jump_strength
            self.jump_speed = jump_strength
            self.double_jump_available = False

    def dash(self):
        """執行衝刺技能"""
        # 檢查能力是否故障
        if self.ability_malfunction_time > 0:
            return

        if self.dash_cooldown <= 0 and not self.is_dashing:
            self.is_dashing = True
            self.dash_distance = 80
            # 噩夢模式冷卻時間更長
            base_cooldown = 180
            if hasattr(self, "nightmare_effects"):
                base_cooldown = int(
                    base_cooldown * (1 + self.nightmare_effects["time_distortion"])
                )
            self.dash_cooldown = base_cooldown

    def activate_shield(self):
        """啟動護盾技能"""
        # 檢查能力是否故障
        if self.ability_malfunction_time > 0:
            return

        if not self.has_shield:
            self.has_shield = True
            self.shield_time = 300  # 5秒護盾時間

    def duck(self):
        """蹲下動作"""
        if not self.is_jumping:
            self.is_ducking = True
            self.height = int(self.original_height * 0.5)
            self.y = self.ground_height - self.height
        elif self.is_jumping:
            # 在跳躍時按蹲下可以快速下降
            if not self.is_gravity_reversed:
                # 正常重力時向下快速下降
                self.jump_speed = max(self.jump_speed, 8)
            else:
                # 重力反轉時向上快速移動
                self.jump_speed = min(self.jump_speed, -8)

    def stand_up(self):
        """站起來動作"""
        if not self.is_jumping:
            self.is_ducking = False
            self.height = self.original_height
            self.y = self.ground_height - self.original_height

    def update(self):
        """更新恐龍狀態"""
        self.animation_frame += 1

        # 處理噩夢模式效果
        self._update_nightmare_effects()

        # 處理衝刺邏輯
        self._update_dash()

        # 更新冷卻時間
        self._update_cooldowns()

        # 處理跳躍物理
        self._update_physics()

    def _update_nightmare_effects(self):
        """更新噩夢模式效果"""
        if not hasattr(self, "nightmare_effects"):
            return

        # 重力反轉效果
        previous_gravity_state = self.is_gravity_reversed
        if self.gravity_reversal_time > 0:
            self.gravity_reversal_time -= 1
            if not self.is_gravity_reversed:
                # 第一次進入重力反轉狀態
                self.is_gravity_reversed = True
                # 自動讓恐龍開始"跳躍"以適應重力變化
                if not self.is_jumping:
                    self.is_jumping = True
                    self.jump_speed = -3  # 向天花板移動
            else:
                self.is_gravity_reversed = True
        else:
            if self.is_gravity_reversed:
                # 重力反轉結束，恢復正常
                self.is_gravity_reversed = False
                # 如果恐龍在空中，讓其自然下落
                if self.y < self.ground_height - self.height:
                    self.is_jumping = True
                    self.jump_speed = 2

        # 控制反轉效果
        if self.control_inversion_time > 0:
            self.control_inversion_time -= 1
            self.is_control_inverted = True
        else:
            self.is_control_inverted = False

        # 能力故障效果
        if self.ability_malfunction_time > 0:
            self.ability_malfunction_time -= 1

    def _update_dash(self):
        """更新衝刺狀態"""
        if self.is_dashing and self.dash_distance > 0:
            move_amount = min(8, self.dash_distance)
            self.x += move_amount
            self.dash_distance -= move_amount
            if self.dash_distance <= 0:
                self.is_dashing = False
                self.x = max(80, self.x)  # 確保不會超出螢幕

    def _update_cooldowns(self):
        """更新技能冷卻時間"""
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        if self.shield_time > 0:
            self.shield_time -= 1
            if self.shield_time <= 0:
                self.has_shield = False

    def _update_physics(self):
        """更新物理狀態"""
        if self.is_jumping:
            # 根據重力狀態調整物理
            gravity = self.gravity
            if self.is_gravity_reversed:
                gravity = -gravity

            self.y += self.jump_speed
            self.jump_speed += gravity

            # 檢查是否著地（根據重力方向）
            if not self.is_gravity_reversed:
                # 正常重力
                if self.y >= self.ground_height - self.height:
                    self.y = self.ground_height - self.height
                    self.is_jumping = False
                    self.jump_speed = 0
                    self.double_jump_available = False
            else:
                # 反轉重力 - 撞到天花板
                if self.y <= 50:
                    self.y = 50
                    self.is_jumping = False
                    self.jump_speed = 0
                    self.double_jump_available = False

    def draw(self, screen):
        """繪製恐龍"""
        # 護盾效果
        if self.has_shield:
            shield_radius = 35 + int(5 * math.sin(self.animation_frame * 0.3))
            pygame.draw.circle(
                screen,
                self.colors["LIGHT_BLUE"],
                (self.x + self.width // 2, self.y + self.height // 2),
                shield_radius,
                3,
            )

        # 衝刺效果
        if self.is_dashing:
            # 殘影效果
            for i in range(3):
                alpha = 100 - i * 30
                dash_surface = pygame.Surface((self.width, self.height))
                dash_surface.set_alpha(alpha)
                dash_surface.fill(self.colors["YELLOW"])
                screen.blit(dash_surface, (self.x - i * 10, self.y))

        # 恐龍本體
        dino_color = (
            self.colors["GREEN"] if not self.has_shield else self.colors["LIGHT_BLUE"]
        )
        pygame.draw.rect(screen, dino_color, (self.x, self.y, self.width, self.height))

        # 恐龍的眼睛
        eye_y = self.y + 10 if not self.is_ducking else self.y + 5
        pygame.draw.circle(screen, self.colors["BLACK"], (self.x + 10, eye_y), 3)

        # 蹲下時的特殊形狀
        if self.is_ducking:
            pygame.draw.rect(
                screen, self.colors["DARK_GREEN"], (self.x, self.y, self.width, 5)
            )

        # 二段跳指示器
        if self.double_jump_available:
            pygame.draw.circle(
                screen, self.colors["YELLOW"], (self.x + self.width + 5, self.y + 5), 4
            )

    def get_collision_rect(self):
        """獲取碰撞檢測矩形"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def apply_nightmare_effect(self, effect_type, duration=180):
        """
        應用噩夢模式效果

        Args:
            effect_type (str): 效果類型 ('gravity_reversal', 'control_inversion', 'ability_malfunction')
            duration (int): 效果持續時間（幀數）
        """
        if effect_type == "gravity_reversal":
            self.gravity_reversal_time = duration
        elif effect_type == "control_inversion":
            self.control_inversion_time = duration
        elif effect_type == "ability_malfunction":
            self.ability_malfunction_time = duration
