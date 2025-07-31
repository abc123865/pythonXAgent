import pygame
import math
import json
import os

# 初始化 Pygame
pygame.init()

# 遊戲設定
SCREEN_WIDTH = 1200  # 增加視窗寬度
SCREEN_HEIGHT = 900  # 增加視窗高度
FPS = 60

# 顏色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)
GRAY = (128, 128, 128)
DARK_BLUE = (25, 25, 112)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)

# 物理設定
GRAVITY = 0.5
MAX_FALL_SPEED = 15
JUMP_CHARGE_RATE = 0.3
MAX_JUMP_POWER = 20
MIN_JUMP_POWER = 5

# 遊戲狀態
MENU = 0
PLAYING = 1
LEVEL_SELECT = 2
GAME_OVER = 3
VICTORY = 4

# 關卡設定
TOTAL_LEVELS = 11


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = True  # 初始化時假設在地面上
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
        self.on_ground = True  # 確保重置後在地面上
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
        self.on_ground = True  # 確保設置後在地面上

    def update(self, platforms, death_zones=None, level_num=None):
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
        if level_num == 11 and self.y > 400:  # 當玩家在較高位置時
            # 如果玩家墜落速度很快且在特定區域，有機率觸發直接掉落
            if self.vel_y > 10:  # 高速墜落時
                import random

                # 在特定x座標範圍內，有15%機率直接掉到底部
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

        # 左邊界（考慮牆壁寬度）
        if self.x <= wall_width:
            self.x = wall_width
            if self.vel_x < 0:  # 只有當玩家向左移動時才反彈
                self.vel_x = -self.vel_x * 0.7  # 反彈，保持較多速度

        # 右邊界（考慮牆壁寬度）
        if self.x + self.width >= SCREEN_WIDTH - wall_width:
            self.x = SCREEN_WIDTH - wall_width - self.width
            if self.vel_x > 0:  # 只有當玩家向右移動時才反彈
                self.vel_x = -self.vel_x * 0.7  # 反彈，保持較多速度

    def check_platform_collision(self, platforms):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        was_on_ground = self.on_ground
        ground_detected = False  # 先用標記而不是直接設置

        for platform in platforms:
            platform_rect = pygame.Rect(
                platform["x"], platform["y"], platform["width"], platform["height"]
            )

            if player_rect.colliderect(platform_rect):
                # 改善碰撞檢測 - 更精確的判斷
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
                    # 從左側撞擊平台 - 反彈
                    self.x = platform["x"] - self.width
                    self.vel_x = -self.vel_x * 0.6  # 反彈，保持更多速度
                elif min_overlap == overlap_right and self.vel_x <= 0:
                    # 從右側撞擊平台 - 反彈
                    self.x = platform["x"] + platform["width"]
                    self.vel_x = -self.vel_x * 0.6  # 反彈，保持更多速度

        # 詳細地面檢測 - 檢查玩家底部是否接觸任何平台
        if not ground_detected:
            for platform in platforms:
                # 檢查水平重疊
                if (
                    self.x < platform["x"] + platform["width"]
                    and self.x + self.width > platform["x"]
                ):
                    # 檢查垂直接觸（允許小誤差）
                    platform_top = platform["y"]
                    player_bottom = self.y + self.height
                    if abs(player_bottom - platform_top) <= 3 and self.vel_y >= -0.5:
                        ground_detected = True
                        self.y = platform_top - self.height
                        self.vel_y = 0
                        break

        # 只有確認不在地面時才設置為 False
        self.on_ground = ground_detected

    def start_jump_charge(self):
        # 移除 on_ground 檢查，允許任何時候開始蓄力（但執行時仍需檢查）
        self.jump_charging = True
        self.jump_power = MIN_JUMP_POWER

    def update_jump_charge(self):
        # 只要在蓄力就持續增加力量
        if self.jump_charging:
            self.jump_power += JUMP_CHARGE_RATE
            if self.jump_power > MAX_JUMP_POWER:
                self.jump_power = MAX_JUMP_POWER

    def execute_jump(self, direction):
        # 只有在地面上且蓄力時才能跳躍
        if self.jump_charging and self.on_ground:
            # 計算跳躍向量
            angle = 0
            if direction == "left":
                angle = 120  # 左上 (調整角度)
                self.facing_right = False
            elif direction == "right":
                angle = 60  # 右上 (調整角度)
                self.facing_right = True
            else:  # 直接向上
                angle = 90

            # 轉換為弧度
            angle_rad = math.radians(angle)

            # 應用跳躍力 (增強跳躍力)
            jump_force = self.jump_power * 1.2  # 增加跳躍力
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
        # 繪製玩家
        player_color = BLUE
        if self.jump_charging:
            # 蓄力時顯示不同顏色
            charge_ratio = (self.jump_power - MIN_JUMP_POWER) / (
                MAX_JUMP_POWER - MIN_JUMP_POWER
            )
            red_component = min(255, int(100 + charge_ratio * 155))
            player_color = (red_component, 100, 237)

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
            pygame.draw.rect(
                screen, RED, (bar_x, bar_y, bar_width * charge_ratio, bar_height)
            )


class LevelManager:
    def __init__(self):
        self.levels = self.create_all_levels()

    def create_all_levels(self):
        """創建所有關卡的平台和死亡區域"""
        levels = {}

        # 第1關 - 簡單練習
        levels[1] = {
            "name": "初學者之路",
            "platforms": [
                {"x": 0, "y": 550, "width": 800, "height": 50},  # 地面
                {"x": 200, "y": 450, "width": 150, "height": 20},
                {"x": 450, "y": 350, "width": 150, "height": 20},
                {"x": 200, "y": 250, "width": 150, "height": 20},
                {"x": 300, "y": 100, "width": 200, "height": 30},  # 目標
            ],
            "death_zones": [],
            "goal_y": 100,
            "start_pos": (100, 500),
            "target_deaths": 5,  # 期望死亡次數
        }

        # 第2關 - 加入陷阱
        levels[2] = {
            "name": "小心陷阱",
            "platforms": [
                {"x": 0, "y": 550, "width": 800, "height": 50},
                {"x": 150, "y": 450, "width": 100, "height": 20},
                {"x": 400, "y": 400, "width": 80, "height": 20},
                {"x": 100, "y": 300, "width": 80, "height": 20},
                {"x": 500, "y": 250, "width": 100, "height": 20},
                {"x": 200, "y": 150, "width": 80, "height": 20},
                {"x": 350, "y": 50, "width": 100, "height": 30},
            ],
            "death_zones": [
                {"x": 250, "y": 400, "width": 150, "height": 200},  # 陷阱區域
            ],
            "goal_y": 50,
            "start_pos": (100, 500),
            "target_deaths": 8,
        }

        # 第3關 - 精確跳躍
        levels[3] = {
            "name": "精確控制",
            "platforms": [
                {"x": 0, "y": 550, "width": 100, "height": 50},
                {"x": 180, "y": 450, "width": 60, "height": 20},
                {"x": 320, "y": 380, "width": 50, "height": 20},
                {"x": 500, "y": 320, "width": 60, "height": 20},
                {"x": 650, "y": 250, "width": 50, "height": 20},
                {"x": 100, "y": 180, "width": 60, "height": 20},
                {"x": 300, "y": 100, "width": 80, "height": 30},
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 800, "height": 100},  # 底部死亡
            ],
            "goal_y": 100,
            "start_pos": (50, 500),
            "target_deaths": 12,
        }

        # 第4關 - 移動平台(靜態，但位置更難)
        levels[4] = {
            "name": "危險跳躍",
            "platforms": [
                {"x": 0, "y": 550, "width": 100, "height": 50},
                {"x": 150, "y": 480, "width": 40, "height": 15},
                {"x": 250, "y": 420, "width": 35, "height": 15},
                {"x": 350, "y": 380, "width": 40, "height": 15},
                {"x": 500, "y": 320, "width": 35, "height": 15},
                {"x": 600, "y": 260, "width": 40, "height": 15},
                {"x": 450, "y": 200, "width": 35, "height": 15},
                {"x": 200, "y": 140, "width": 40, "height": 15},
                {"x": 350, "y": 80, "width": 100, "height": 30},
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 800, "height": 100},
                {"x": 100, "y": 450, "width": 50, "height": 150},  # 額外陷阱
            ],
            "goal_y": 80,
            "start_pos": (50, 500),
            "target_deaths": 15,
        }

        # 第5關 - 中級挑戰
        levels[5] = {
            "name": "中級試煉",
            "platforms": [
                {"x": 0, "y": 550, "width": 80, "height": 50},
                {"x": 120, "y": 490, "width": 30, "height": 15},
                {"x": 200, "y": 440, "width": 25, "height": 15},
                {"x": 300, "y": 400, "width": 30, "height": 15},
                {"x": 400, "y": 350, "width": 25, "height": 15},
                {"x": 520, "y": 300, "width": 30, "height": 15},
                {"x": 600, "y": 240, "width": 25, "height": 15},
                {"x": 500, "y": 180, "width": 30, "height": 15},
                {"x": 350, "y": 120, "width": 25, "height": 15},
                {"x": 200, "y": 60, "width": 30, "height": 15},
                {"x": 300, "y": 0, "width": 100, "height": 30},
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 800, "height": 100},
                {"x": 80, "y": 450, "width": 40, "height": 100},
                {"x": 450, "y": 250, "width": 50, "height": 100},
            ],
            "goal_y": 0,
            "start_pos": (40, 500),
            "target_deaths": 20,
        }

        # 第6關 - 高級挑戰（稍微降低難度）
        levels[6] = {
            "name": "高手之路",
            "platforms": [
                {"x": 0, "y": 550, "width": 80, "height": 50},  # 增加起始平台大小
                {"x": 120, "y": 500, "width": 30, "height": 15},  # 增加平台大小
                {"x": 200, "y": 460, "width": 30, "height": 15},
                {"x": 280, "y": 420, "width": 30, "height": 15},
                {"x": 360, "y": 380, "width": 30, "height": 15},
                {"x": 440, "y": 340, "width": 30, "height": 15},
                {"x": 520, "y": 300, "width": 30, "height": 15},
                {"x": 600, "y": 260, "width": 30, "height": 15},
                {"x": 680, "y": 220, "width": 30, "height": 15},
                {"x": 600, "y": 180, "width": 30, "height": 15},
                {"x": 520, "y": 140, "width": 30, "height": 15},
                {"x": 440, "y": 100, "width": 30, "height": 15},
                {"x": 360, "y": 60, "width": 30, "height": 15},
                {"x": 280, "y": 20, "width": 30, "height": 15},
                {"x": 350, "y": -40, "width": 100, "height": 30},
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 800, "height": 100},
                {"x": 80, "y": 400, "width": 40, "height": 200},  # 減少死亡區域
                {"x": 320, "y": 300, "width": 40, "height": 200},
                {"x": 560, "y": 200, "width": 40, "height": 200},
            ],
            "goal_y": -40,
            "start_pos": (40, 500),
            "target_deaths": 25,  # 稍微降低目標
        }

        # 第7關 - 專家級（經過物理驗證的可行設計）
        levels[7] = {
            "name": "專家考驗",
            "platforms": [
                {"x": 0, "y": 550, "width": 120, "height": 50},  # 起始平台
                {"x": 214, "y": 510, "width": 40, "height": 15},  # 平台1
                {"x": 339, "y": 480, "width": 40, "height": 15},  # 平台2
                {"x": 189, "y": 445, "width": 40, "height": 15},  # 平台3
                {"x": 64, "y": 420, "width": 40, "height": 15},  # 平台4
                {"x": 264, "y": 375, "width": 40, "height": 15},  # 平台5
                {"x": 414, "y": 345, "width": 40, "height": 15},  # 平台6
                {"x": 239, "y": 305, "width": 40, "height": 15},  # 平台7
                {"x": 299, "y": 245, "width": 120, "height": 30},  # 目標平台
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},  # 底部死亡區域
            ],
            "goal_y": 245,
            "start_pos": (60, 500),  # 起始平台中心
            "target_deaths": 25,
        }

        # 第8關 - 大師挑戰（重新設計）
        levels[8] = {
            "name": "大師挑戰",
            "platforms": [
                {"x": 0, "y": 550, "width": 100, "height": 50},  # 起始平台
                {"x": 234, "y": 515, "width": 30, "height": 12},  # 平台1
                {"x": 434, "y": 480, "width": 30, "height": 12},  # 平台2
                {"x": 633, "y": 445, "width": 30, "height": 12},  # 平台3
                {"x": 434, "y": 410, "width": 30, "height": 12},  # 平台4
                {"x": 234, "y": 375, "width": 30, "height": 12},  # 平台5
                {"x": 34, "y": 340, "width": 30, "height": 12},  # 平台6
                {"x": 284, "y": 300, "width": 30, "height": 12},  # 平台7
                {"x": 533, "y": 260, "width": 30, "height": 12},  # 平台8
                {"x": 498, "y": 210, "width": 100, "height": 30},  # 目標平台
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},  # 底部死亡區域
            ],
            "goal_y": 210,
            "start_pos": (50, 500),
            "target_deaths": 35,
        }

        # 第9關 - 傳說級（物理驗證版本）
        levels[9] = {
            "name": "螺旋之謎",
            "platforms": [
                # 起始平台（確保安全起跳）
                {"x": 0, "y": 550, "width": 80, "height": 30},
                # 螺旋路徑 - 每個跳躍距離都在物理極限內（<250px）
                {"x": 200, "y": 480, "width": 60, "height": 20},  # 跳躍距離: 200px
                {"x": 400, "y": 420, "width": 50, "height": 20},  # 跳躍距離: 200px
                {"x": 550, "y": 350, "width": 50, "height": 20},  # 跳躍距離: 150px
                {"x": 650, "y": 280, "width": 50, "height": 20},  # 跳躍距離: 100px
                {"x": 700, "y": 200, "width": 50, "height": 20},  # 跳躍距離: 80px
                # 回轉路徑
                {"x": 500, "y": 130, "width": 50, "height": 20},  # 跳躍距離: 200px
                {"x": 300, "y": 80, "width": 50, "height": 20},  # 跳躍距離: 200px
                {"x": 100, "y": 40, "width": 50, "height": 20},  # 跳躍距離: 200px
                # 最終挑戰
                {"x": 250, "y": -20, "width": 50, "height": 20},  # 跳躍距離: 150px
                {
                    "x": 450,
                    "y": -80,
                    "width": 60,
                    "height": 30,
                },  # 跳躍距離: 200px (目標平台)
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},  # 底部死亡區域
            ],
            "goal_y": -80,
            "start_pos": (40, 520),
            "target_deaths": 60,
        }

        # 第10關 - 終極挑戰（物理驗證版本）
        levels[10] = {
            "name": "絕望深淵",
            "platforms": [
                # 起始平台
                {"x": 0, "y": 550, "width": 60, "height": 30},
                # 精密跳躍路徑 - 每個跳躍距離都經過計算驗證
                {"x": 180, "y": 480, "width": 40, "height": 15},  # 跳躍距離: 180px
                {"x": 350, "y": 420, "width": 40, "height": 15},  # 跳躍距離: 170px
                {"x": 500, "y": 350, "width": 40, "height": 15},  # 跳躍距離: 150px
                {"x": 620, "y": 280, "width": 40, "height": 15},  # 跳躍距離: 120px
                {"x": 700, "y": 210, "width": 40, "height": 15},  # 跳躍距離: 80px
                {"x": 580, "y": 140, "width": 40, "height": 15},  # 跳躍距離: 120px
                {"x": 420, "y": 80, "width": 40, "height": 15},  # 跳躍距離: 160px
                {"x": 240, "y": 20, "width": 40, "height": 15},  # 跳躍距離: 180px
                {"x": 80, "y": -40, "width": 40, "height": 15},  # 跳躍距離: 160px
                {"x": 260, "y": -100, "width": 40, "height": 15},  # 跳躍距離: 180px
                {"x": 440, "y": -160, "width": 40, "height": 15},  # 跳躍距離: 180px
                {"x": 600, "y": -220, "width": 40, "height": 15},  # 跳躍距離: 160px
                # 最終目標平台
                {
                    "x": 300,
                    "y": -280,
                    "width": 80,
                    "height": 30,
                },  # 跳躍距離: 300px (挑戰性但可達成)
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},  # 底部死亡區域
            ],
            "goal_y": -280,
            "start_pos": (30, 520),
            "target_deaths": 80,
        }

        # 第11關 - 無限爬升挑戰（物理驗證版本）
        levels[11] = {
            "name": "絕望之塔",
            "platforms": [
                # 起始平台
                {"x": 0, "y": 550, "width": 80, "height": 30},
                # 第一階段 - 基礎攀登
                {"x": 200, "y": 480, "width": 50, "height": 20},  # 跳躍距離: 200px
                {"x": 400, "y": 420, "width": 50, "height": 20},  # 跳躍距離: 200px
                {"x": 600, "y": 360, "width": 50, "height": 20},  # 跳躍距離: 200px
                {
                    "x": 450,
                    "y": 300,
                    "width": 50,
                    "height": 20,
                },  # 跳躍距離: 150px (回跳)
                {"x": 250, "y": 240, "width": 50, "height": 20},  # 跳躍距離: 200px
                # 第二階段 - 精密跳躍
                {"x": 450, "y": 180, "width": 45, "height": 15},  # 跳躍距離: 200px
                {"x": 650, "y": 120, "width": 45, "height": 15},  # 跳躍距離: 200px
                {"x": 500, "y": 60, "width": 45, "height": 15},  # 跳躍距離: 150px
                {"x": 300, "y": 0, "width": 45, "height": 15},  # 跳躍距離: 200px
                {"x": 500, "y": -60, "width": 45, "height": 15},  # 跳躍距離: 200px
                # 第三階段 - 高難度區域
                {"x": 700, "y": -120, "width": 40, "height": 15},  # 跳躍距離: 200px
                {"x": 550, "y": -180, "width": 40, "height": 15},  # 跳躍距離: 150px
                {"x": 350, "y": -240, "width": 40, "height": 15},  # 跳躍距離: 200px
                {"x": 550, "y": -300, "width": 40, "height": 15},  # 跳躍距離: 200px
                {"x": 750, "y": -360, "width": 40, "height": 15},  # 跳躍距離: 200px
                # 第四階段 - 終極挑戰
                {"x": 600, "y": -420, "width": 35, "height": 15},  # 跳躍距離: 150px
                {"x": 400, "y": -480, "width": 35, "height": 15},  # 跳躍距離: 200px
                {"x": 600, "y": -540, "width": 35, "height": 15},  # 跳躍距離: 200px
                {"x": 450, "y": -600, "width": 35, "height": 15},  # 跳躍距離: 150px
                {"x": 650, "y": -660, "width": 35, "height": 15},  # 跳躍距離: 200px
                # 最終平台
                {
                    "x": 350,
                    "y": -720,
                    "width": 100,
                    "height": 30,
                },  # 跳躍距離: 300px (終極挑戰)
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},  # 底部死亡區域
                # 特殊掉落機制死亡區域 (模擬第11關的掉落特性)
                {"x": 0, "y": -800, "width": 1200, "height": 50},  # 高處掉落緩衝區
            ],
            "goal_y": -720,
            "start_pos": (40, 520),
            "target_deaths": 120,
        }

        return levels

    def get_level(self, level_num):
        """獲取指定關卡"""
        return self.levels.get(level_num)


class Game:
    def __init__(self):
        # 全屏設定
        self.fullscreen = False
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.ui_scale_x = 1.0
        self.ui_scale_y = 1.0
        self.ui_scale = 1.0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jump King - 十關挑戰")
        self.clock = pygame.time.Clock()
        self.running = True

        # 遊戲狀態
        self.state = MENU
        self.current_level = 1

        # 載入進度
        self.save_file = "jumpking_save.json"
        self.unlocked_levels = 1
        self.level_stats = {}  # 每關的統計資料
        self.load_progress()

        # 初始化組件
        self.level_manager = LevelManager()
        self.player = None
        self.camera_y = 0

        # 字體 - 使用微軟正黑體支援中文
        font_paths = [
            "C:\\Windows\\Fonts\\msjh.ttc",  # 微軟正黑體
            "C:\\Windows\\Fonts\\msyh.ttc",  # 微軟雅黑
            "C:\\Windows\\Fonts\\simsun.ttc",  # 新細明體
            "C:\\Windows\\Fonts\\kaiu.ttf",  # 標楷體
        ]

        # 選單選項
        self.menu_selection = 0
        self.level_select_selection = 1

        # 載入字體
        self.load_fonts()

    def load_fonts(self):
        """載入字體"""
        font_paths = [
            "C:\\Windows\\Fonts\\msjh.ttc",  # 微軟正黑體
            "C:\\Windows\\Fonts\\msyh.ttc",  # 微軟雅黑
            "C:\\Windows\\Fonts\\simsun.ttc",  # 新細明體
            "C:\\Windows\\Fonts\\kaiu.ttf",  # 標楷體
        ]

        # 根據縮放調整字體大小，但確保在全屏模式下字體不會太小
        if self.fullscreen:
            # 全屏模式下使用基礎字體大小，因為會通過虛擬畫布縮放
            large_size = 48
            medium_size = 36
            small_size = 24
        else:
            # 視窗模式使用原始大小
            large_size = 48
            medium_size = 36
            small_size = 24

        font_loaded = False
        for font_path in font_paths:
            try:
                self.font_large = pygame.font.Font(font_path, large_size)
                self.font_medium = pygame.font.Font(font_path, medium_size)
                self.font_small = pygame.font.Font(font_path, small_size)
                font_loaded = True
                print(f"成功載入字體: {font_path}")
                break
            except:
                continue

        if not font_loaded:
            # 如果所有字體都載入失敗，使用系統預設字體
            self.font_large = pygame.font.Font(None, large_size)
            self.font_medium = pygame.font.Font(None, medium_size)
            self.font_small = pygame.font.Font(None, small_size)
            print("使用系統預設字體")

    def load_progress(self):
        """載入遊戲進度"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.unlocked_levels = data.get("unlocked_levels", 1)
                    self.level_stats = data.get("level_stats", {})
        except:
            self.unlocked_levels = 1
            self.level_stats = {}

    def save_progress(self):
        """儲存遊戲進度"""
        try:
            data = {
                "unlocked_levels": self.unlocked_levels,
                "level_stats": self.level_stats,
            }
            with open(self.save_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except:
            pass

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
            self.ui_scale = min(self.ui_scale_x, self.ui_scale_y)  # 保持比例
        else:
            self.screen_width = SCREEN_WIDTH
            self.screen_height = SCREEN_HEIGHT
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.ui_scale_x = 1.0
            self.ui_scale_y = 1.0
            self.ui_scale = 1.0

        # 重新載入字體以適應新的縮放比例
        self.load_fonts()
        pygame.display.set_caption("Jump King - 十關挑戰")

    def scale_pos(self, x, y):
        """根據UI縮放調整位置"""
        if self.fullscreen:
            # 居中顯示，保持比例
            offset_x = (self.screen_width - SCREEN_WIDTH * self.ui_scale) // 2
            offset_y = (self.screen_height - SCREEN_HEIGHT * self.ui_scale) // 2
            return int(x * self.ui_scale + offset_x), int(y * self.ui_scale + offset_y)
        return x, y

    def scale_size(self, width, height=None):
        """根據UI縮放調整大小"""
        if height is None:
            height = width
        if self.fullscreen:
            return int(width * self.ui_scale), int(height * self.ui_scale)
        return width, height

    def get_scaled_font(self, base_size):
        """獲取縮放後的字體大小"""
        if self.fullscreen:
            return max(int(base_size * self.ui_scale), 12)  # 最小字體大小12
        return base_size

    def start_level(self, level_num):
        """開始指定關卡"""
        level_data = self.level_manager.get_level(level_num)
        if not level_data:
            return

        self.current_level = level_num
        start_x, start_y = level_data["start_pos"]
        self.player = Player(start_x, start_y)

        # 確保玩家正確地站在起始平台上
        self.player.on_ground = True
        self.player.vel_x = 0
        self.player.vel_y = 0

        self.camera_y = 0
        self.state = PLAYING

        # 初始化關卡統計
        if str(level_num) not in self.level_stats:
            self.level_stats[str(level_num)] = {
                "deaths": 0,
                "completed": False,
                "best_deaths": None,
            }

    def complete_level(self):
        """完成關卡"""
        level_key = str(self.current_level)
        if level_key in self.level_stats:
            self.level_stats[level_key]["completed"] = True
            deaths = self.player.death_count

            # 更新最佳記錄
            if (
                self.level_stats[level_key]["best_deaths"] is None
                or deaths < self.level_stats[level_key]["best_deaths"]
            ):
                self.level_stats[level_key]["best_deaths"] = deaths

        # 解鎖下一關
        if self.current_level < TOTAL_LEVELS:
            self.unlocked_levels = max(self.unlocked_levels, self.current_level + 1)

        self.save_progress()
        self.state = VICTORY

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
                    # 找到最高未完成關卡
                    level_to_start = 1
                    for i in range(1, self.unlocked_levels + 1):
                        if (
                            str(i) not in self.level_stats
                            or not self.level_stats[str(i)]["completed"]
                        ):
                            level_to_start = i
                            break
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
                if self.level_select_selection < self.unlocked_levels:
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
                self.save_progress()
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
                elif self.state in [VICTORY, GAME_OVER]:
                    pass  # 其他事件類型不需要處理

    def check_goal_completion(self, level_data):
        """檢查玩家是否踩在目標平台上"""
        if not self.player or not self.player.on_ground:
            return False

        # 找到目標平台（黃色平台）
        goal_platforms = []
        for platform in level_data["platforms"]:
            if platform["y"] <= level_data["goal_y"]:
                goal_platforms.append(platform)

        # 檢查玩家是否踩在任何目標平台上
        player_rect = pygame.Rect(
            self.player.x, self.player.y, self.player.width, self.player.height
        )

        for platform in goal_platforms:
            platform_rect = pygame.Rect(
                platform["x"], platform["y"], platform["width"], platform["height"]
            )

            # 檢查玩家底部是否接觸平台頂部
            if (
                self.player.x < platform["x"] + platform["width"]
                and self.player.x + self.player.width > platform["x"]
                and abs((self.player.y + self.player.height) - platform["y"]) <= 3
                and self.player.on_ground
            ):
                return True

        return False

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
            self.level_stats[str(self.current_level)][
                "deaths"
            ] = self.player.death_count
            self.save_progress()
        elif result == "fall_trap":
            # 掉落陷阱的特殊處理 - 不重置但記錄
            self.level_stats[str(self.current_level)][
                "deaths"
            ] = self.player.death_count
            self.save_progress()

        # 更新相機
        self.update_camera()

        # 檢查是否完成關卡（必須踩在目標平台上）
        if self.check_goal_completion(level_data):
            self.complete_level()

    def update_camera(self):
        """更新相機位置"""
        if self.player:
            target_y = self.player.y - SCREEN_HEIGHT // 2
            self.camera_y += (target_y - self.camera_y) * 0.1

    def update(self):
        """更新遊戲邏輯"""
        if self.state == PLAYING:
            self.update_playing()

    def draw_menu(self):
        """繪製主選單"""
        if self.fullscreen:
            # 全屏模式下，先繪製到虛擬畫布
            virtual_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.draw_menu_content(virtual_screen)
            self.scale_and_blit_virtual_screen(virtual_screen)
        else:
            # 視窗模式直接繪製
            self.draw_menu_content(self.screen)

    def draw_menu_content(self, screen):
        """繪製主選單內容"""
        screen.fill(DARK_BLUE)

        # 標題
        title = self.font_large.render("Jump King - 十關挑戰", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title, title_rect)

        # 副標題
        subtitle = self.font_medium.render("考驗你的耐心與技巧", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(subtitle, subtitle_rect)

        # 選單選項
        menu_options = ["開始遊戲", "繼續遊戲", "退出遊戲"]
        for i, option in enumerate(menu_options):
            color = YELLOW if i == self.menu_selection else WHITE
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 50))
            screen.blit(text, text_rect)

        # 進度資訊
        progress_text = f"已解鎖關卡: {self.unlocked_levels}/{TOTAL_LEVELS}"
        progress = self.font_small.render(progress_text, True, GREEN)
        progress_rect = progress.get_rect(center=(SCREEN_WIDTH // 2, 500))
        screen.blit(progress, progress_rect)

        # 操作說明
        controls = ["↑↓ 選擇", "Enter 確認", "ESC 退出", "F11 切換全屏"]
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, GRAY)
            screen.blit(text, (50, 500 + i * 25))

    def draw_level_select(self):
        """繪製關卡選擇畫面"""
        if self.fullscreen:
            # 全屏模式下，先繪製到虛擬畫布
            virtual_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.draw_level_select_content(virtual_screen)
            self.scale_and_blit_virtual_screen(virtual_screen)
        else:
            # 視窗模式直接繪製
            self.draw_level_select_content(self.screen)

    def draw_level_select_content(self, screen):
        """繪製關卡選擇畫面內容"""
        screen.fill(DARK_BLUE)

        # 標題
        title = self.font_large.render("選擇關卡", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        # 關卡選項
        start_x = 50
        start_y = 180
        cols = 6  # 改為6列以容納11關
        rows = 2

        for level in range(1, TOTAL_LEVELS + 1):
            row = (level - 1) // cols
            col = (level - 1) % cols
            x = start_x + col * 120  # 稍微減小間距
            y = start_y + row * 120

            # 使用縮放位置
            scaled_x, scaled_y = self.scale_pos(x, y)
            rect_width, rect_height = self.scale_size(100, 80)
            border_width, border_height = self.scale_size(110, 90)

            # 判斷關卡狀態
            if level > self.unlocked_levels:
                # 未解鎖
                color = GRAY
                text_color = BLACK
                status = "鎖定"
            elif level == 11:
                # 第11關特殊顯示
                if (
                    str(level) in self.level_stats
                    and self.level_stats[str(level)]["completed"]
                ):
                    color = PURPLE  # 完成的第11關用紫色
                    text_color = WHITE
                    deaths = self.level_stats[str(level)]["best_deaths"]
                    status = f"征服\n{deaths}死"
                else:
                    color = (128, 0, 128)  # 未完成的第11關用深紫色
                    text_color = WHITE
                    deaths = self.level_stats.get(str(level), {}).get("deaths", 0)
                    status = f"挑戰\n{deaths}死"
            elif (
                str(level) in self.level_stats
                and self.level_stats[str(level)]["completed"]
            ):
                # 已完成
                color = GREEN
                text_color = WHITE
                deaths = self.level_stats[str(level)]["best_deaths"]
                status = f"完成\n{deaths}死"
            else:
                # 可玩但未完成
                color = ORANGE
                text_color = WHITE
                deaths = self.level_stats.get(str(level), {}).get("deaths", 0)
                status = f"進行中\n{deaths}死"

            # 選中的關卡
            if level == self.level_select_selection:
                border_x = scaled_x - int(5 * self.ui_scale)
                border_y = scaled_y - int(5 * self.ui_scale)
                border_thickness = max(1, int(3 * self.ui_scale))
                pygame.draw.rect(
                    self.screen,
                    YELLOW,
                    (border_x, border_y, border_width, border_height),
                    border_thickness,
                )

            # 關卡方塊
            pygame.draw.rect(
                self.screen, color, (scaled_x, scaled_y, rect_width, rect_height)
            )

            # 關卡編號
            level_text = self.font_medium.render(f"第{level}關", True, text_color)
            level_text_x, level_text_y = self.scale_pos(x + 50, y + 20)
            level_rect = level_text.get_rect(center=(level_text_x, level_text_y))
            self.screen.blit(level_text, level_rect)

            # 關卡名稱
            level_data = self.level_manager.get_level(level)
            if level_data:
                name_text = self.font_small.render(level_data["name"], True, text_color)
                name_text_x, name_text_y = self.scale_pos(x + 50, y + 40)
                name_rect = name_text.get_rect(center=(name_text_x, name_text_y))
                self.screen.blit(name_text, name_rect)

            # 狀態
            for i, line in enumerate(status.split("\n")):
                status_text = self.font_small.render(line, True, text_color)
                status_text_x, status_text_y = self.scale_pos(x + 50, y + 55 + i * 12)
                status_rect = status_text.get_rect(
                    center=(status_text_x, status_text_y)
                )
                self.screen.blit(status_text, status_rect)

        # 關卡詳情
        if 1 <= self.level_select_selection <= TOTAL_LEVELS:
            level_data = self.level_manager.get_level(self.level_select_selection)
            if level_data:
                detail_y = 450

                # 關卡名稱
                name = self.font_medium.render(
                    f"第{self.level_select_selection}關: {level_data['name']}",
                    True,
                    YELLOW,
                )
                name_x, name_y = self.scale_pos(SCREEN_WIDTH // 2, detail_y)
                name_rect = name.get_rect(center=(name_x, name_y))
                self.screen.blit(name, name_rect)

                # 目標死亡次數
                target_text = f"挑戰目標: {level_data['target_deaths']}次死亡內完成"
                if self.level_select_selection == 11:
                    target_text = f"超級挑戰: {level_data['target_deaths']}次死亡內完成"
                target = self.font_small.render(target_text, True, WHITE)
                target_x, target_y = self.scale_pos(SCREEN_WIDTH // 2, detail_y + 30)
                target_rect = target.get_rect(center=(target_x, target_y))
                self.screen.blit(target, target_rect)

                # 第11關特殊警告
                if self.level_select_selection == 11:
                    warning_text = "⚠️ 注意：此關卡包含隨機掉落陷阱！"
                    warning = self.font_small.render(warning_text, True, RED)
                    warning_x, warning_y = self.scale_pos(
                        SCREEN_WIDTH // 2, detail_y + 55
                    )
                    warning_rect = warning.get_rect(center=(warning_x, warning_y))
                    self.screen.blit(warning, warning_rect)

        # 操作說明
        controls = ["← → 選擇關卡", "Enter 開始", "ESC 返回", "F11 切換全屏"]
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, GRAY)
            control_x, control_y = self.scale_pos(50, 550 + i * 20)
            self.screen.blit(text, (control_x, control_y))

    def draw_playing(self):
        """繪製遊戲畫面"""
        if self.fullscreen:
            # 全屏模式下，先繪製到虛擬畫布
            virtual_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.draw_playing_content(virtual_screen)

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
        else:
            # 視窗模式直接繪製
            self.draw_playing_content(self.screen)

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

    def draw_playing_content(self, screen):
        """繪製遊戲畫面內容"""
        screen.fill(DARK_BLUE)

        if not self.player:
            return

        # 獲取當前關卡資料
        level_data = self.level_manager.get_level(self.current_level)
        if not level_data:
            return

        # 繪製屏幕邊界牆壁
        wall_width = 10
        # 左邊界牆壁
        pygame.draw.rect(screen, GRAY, (0, 0, wall_width, SCREEN_HEIGHT))
        # 右邊界牆壁
        pygame.draw.rect(
            screen, GRAY, (SCREEN_WIDTH - wall_width, 0, wall_width, SCREEN_HEIGHT)
        )

        # 繪製平台
        for platform in level_data["platforms"]:
            color = BROWN
            if platform["y"] <= level_data["goal_y"]:  # 目標平台
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

        # 繪製死亡區域
        for zone in level_data["death_zones"]:
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

        # 第11關特殊視覺效果 - 繪製掉落陷阱警告區域
        if self.current_level == 11:
            danger_zones = [
                (90, 160, 480, 20),  # x_min, x_max, y, height
                (240, 310, 380, 20),
                (490, 560, 280, 20),
                (740, 810, 200, 20),
            ]

            import time

            # 讓警告區域閃爍
            alpha = int(128 + 127 * abs((time.time() * 3) % 2 - 1))
            warning_color = (*ORANGE, alpha)

            for min_x, max_x, y, height in danger_zones:
                # 創建一個有透明度的表面
                warning_surface = pygame.Surface((max_x - min_x, height))
                warning_surface.set_alpha(alpha)
                warning_surface.fill(ORANGE)
                screen.blit(warning_surface, (min_x, y - self.camera_y))

        # 繪製玩家
        self.draw_player_content(screen, self.camera_y)

        # 繪製UI
        self.draw_playing_ui_content(screen, level_data)

    def draw_player_content(self, screen, camera_y):
        """繪製玩家（不縮放版本，用於虛擬畫布）"""
        if not self.player:
            return

        # 繪製玩家
        player_color = BLUE
        if self.player.jump_charging:
            # 蓄力時顯示不同顏色
            charge_ratio = (self.player.jump_power - MIN_JUMP_POWER) / (
                MAX_JUMP_POWER - MIN_JUMP_POWER
            )
            red_component = min(255, int(100 + charge_ratio * 155))
            player_color = (red_component, 100, 237)

        pygame.draw.rect(
            screen,
            player_color,
            (
                self.player.x,
                self.player.y - camera_y,
                self.player.width,
                self.player.height,
            ),
        )

        # 繪製面向方向指示
        eye_offset_x = 20 if self.player.facing_right else 10
        eye_x = self.player.x + eye_offset_x
        eye_y = self.player.y - camera_y + 10
        pygame.draw.circle(screen, WHITE, (eye_x, eye_y), 3)

        # 繪製蓄力指示器
        if self.player.jump_charging:
            charge_ratio = (self.player.jump_power - MIN_JUMP_POWER) / (
                MAX_JUMP_POWER - MIN_JUMP_POWER
            )
            bar_width = 40
            bar_height = 8
            bar_x = self.player.x - 5
            bar_y = self.player.y - camera_y - 15

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

    def draw_player(self, camera_y):
        """繪製玩家（適應縮放）"""
        if not self.player:
            return

        # 繪製玩家
        player_color = BLUE
        if self.player.jump_charging:
            # 蓄力時顯示不同顏色
            charge_ratio = (self.player.jump_power - MIN_JUMP_POWER) / (
                MAX_JUMP_POWER - MIN_JUMP_POWER
            )
            red_component = min(255, int(100 + charge_ratio * 155))
            player_color = (red_component, 100, 237)

        # 計算玩家位置和大小
        player_x, player_y = self.scale_pos(self.player.x, self.player.y - camera_y)
        player_width, player_height = self.scale_size(
            self.player.width, self.player.height
        )

        pygame.draw.rect(
            self.screen, player_color, (player_x, player_y, player_width, player_height)
        )

        # 繪製面向方向指示
        eye_offset_x = 20 if self.player.facing_right else 10
        eye_x, eye_y = self.scale_pos(
            self.player.x + eye_offset_x, self.player.y - camera_y + 10
        )
        eye_radius = max(1, int(3 * self.ui_scale))
        pygame.draw.circle(self.screen, WHITE, (eye_x, eye_y), eye_radius)

        # 繪製蓄力指示器
        if self.player.jump_charging:
            charge_ratio = (self.player.jump_power - MIN_JUMP_POWER) / (
                MAX_JUMP_POWER - MIN_JUMP_POWER
            )
            bar_width, bar_height = self.scale_size(40, 8)
            bar_x, bar_y = self.scale_pos(
                self.player.x - 5, self.player.y - camera_y - 15
            )

            # 背景
            pygame.draw.rect(self.screen, GRAY, (bar_x, bar_y, bar_width, bar_height))

            # 蓄力條
            charge_width = int(bar_width * charge_ratio)
            charge_color = (
                RED if charge_ratio > 0.8 else YELLOW if charge_ratio > 0.5 else GREEN
            )
            pygame.draw.rect(
                self.screen, charge_color, (bar_x, bar_y, charge_width, bar_height)
            )

    def draw_playing_ui(self, level_data):
        """繪製遊戲中的UI"""
        # 關卡資訊
        level_text = f"第{self.current_level}關: {level_data['name']}"
        text = self.font_medium.render(level_text, True, YELLOW)
        ui_x, ui_y = self.scale_pos(10, 10)
        self.screen.blit(text, (ui_x, ui_y))

        # 死亡次數
        deaths_text = f"死亡次數: {self.player.death_count}"
        text = self.font_small.render(deaths_text, True, WHITE)
        deaths_x, deaths_y = self.scale_pos(10, 45)
        self.screen.blit(text, (deaths_x, deaths_y))

        # 目標
        target_text = f"目標: {level_data['target_deaths']}次內完成"
        color = GREEN if self.player.death_count <= level_data["target_deaths"] else RED
        text = self.font_small.render(target_text, True, color)
        target_x, target_y = self.scale_pos(10, 70)
        self.screen.blit(text, (target_x, target_y))

        # 高度
        height = max(0, int((level_data["start_pos"][1] - self.player.y) / 10))
        height_text = f"高度: {height}m"
        text = self.font_small.render(height_text, True, WHITE)
        height_x, height_y = self.scale_pos(SCREEN_WIDTH - 150, 10)
        self.screen.blit(text, (height_x, height_y))

        # 控制說明
        controls = [
            "按住 SPACE 蓄力",
            "蓄力時按 ← → 選方向",
            "放開 SPACE 跳躍",
            "R 重置位置",
            "ESC 返回選單",
            "F11 切換全屏",
            "撞牆會反彈！",
        ]

        # 第11關特殊說明
        if self.current_level == 11:
            controls.append("⚠️ 小心！某些區域")
            controls.append("高速墜落會觸發")
            controls.append("掉落陷阱！")

        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, WHITE)
            control_x, control_y = self.scale_pos(10, SCREEN_HEIGHT - 140 + i * 20)
            self.screen.blit(text, (control_x, control_y))

        # 玩家狀態
        status_text = f"在地面: {'是' if self.player.on_ground else '否'}"
        color = GREEN if self.player.on_ground else RED
        text = self.font_small.render(status_text, True, color)
        status_x, status_y = self.scale_pos(SCREEN_WIDTH - 150, 35)
        self.screen.blit(text, (status_x, status_y))

        # 蓄力狀態
        if self.player.jump_charging:
            charge_text = f"蓄力: {self.player.jump_power:.1f}"
            text = self.font_small.render(charge_text, True, YELLOW)
            charge_x, charge_y = self.scale_pos(SCREEN_WIDTH - 150, 60)
            self.screen.blit(text, (charge_x, charge_y))

    def draw_playing_ui_content(self, screen, level_data):
        """繪製遊戲中的UI（不縮放版本，用於虛擬畫布）"""
        # 關卡資訊
        level_text = f"第{self.current_level}關: {level_data['name']}"
        text = self.font_medium.render(level_text, True, YELLOW)
        screen.blit(text, (10, 10))

        # 死亡次數
        deaths_text = f"死亡次數: {self.player.death_count}"
        text = self.font_small.render(deaths_text, True, WHITE)
        screen.blit(text, (10, 45))

        # 目標
        target_text = f"目標: {level_data['target_deaths']}次內完成"
        color = GREEN if self.player.death_count <= level_data["target_deaths"] else RED
        text = self.font_small.render(target_text, True, color)
        screen.blit(text, (10, 70))

        # 高度
        height = max(0, int((level_data["start_pos"][1] - self.player.y) / 10))
        height_text = f"高度: {height}m"
        text = self.font_small.render(height_text, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - 150, 10))

        # 控制說明
        controls = [
            "按住 SPACE 蓄力",
            "蓄力時按 ← → 選方向",
            "放開 SPACE 跳躍",
            "R 重置位置",
            "ESC 返回選單",
            "F11 切換全屏",
            "撞牆會反彈！",
        ]

        # 第11關特殊說明
        if self.current_level == 11:
            controls.append("⚠️ 小心！某些區域")
            controls.append("高速墜落會觸發")
            controls.append("掉落陷阱！")

        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, WHITE)
            screen.blit(text, (10, SCREEN_HEIGHT - 140 + i * 20))

        # 玩家狀態
        status_text = f"在地面: {'是' if self.player.on_ground else '否'}"
        color = GREEN if self.player.on_ground else RED
        text = self.font_small.render(status_text, True, color)
        screen.blit(text, (SCREEN_WIDTH - 150, 35))

        # 蓄力狀態
        if self.player.jump_charging:
            charge_text = f"蓄力: {self.player.jump_power:.1f}"
            text = self.font_small.render(charge_text, True, YELLOW)
            screen.blit(text, (SCREEN_WIDTH - 150, 60))

    def draw_victory(self):
        """繪製勝利畫面"""
        if self.fullscreen:
            # 全屏模式下，先繪製到虛擬畫布
            virtual_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.draw_victory_content(virtual_screen)
            self.scale_and_blit_virtual_screen(virtual_screen)
        else:
            # 視窗模式直接繪製
            self.draw_victory_content(self.screen)

    def draw_victory_content(self, screen):
        """繪製勝利畫面內容"""
        screen.fill(DARK_BLUE)

        # 勝利訊息
        title = self.font_large.render("恭喜過關！", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(title, title_rect)

        # 統計資料
        level_data = self.level_manager.get_level(self.current_level)
        if level_data:
            deaths = self.player.death_count
            target = level_data["target_deaths"]

            stats_text = f"第{self.current_level}關: {level_data['name']}"
            text = self.font_medium.render(stats_text, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 280))
            screen.blit(text, text_rect)

            deaths_text = f"死亡次數: {deaths}"
            color = GREEN if deaths <= target else RED
            text = self.font_medium.render(deaths_text, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 320))
            screen.blit(text, text_rect)

            target_text = f"目標: {target}次"
            text = self.font_medium.render(target_text, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 360))
            screen.blit(text, text_rect)

            if deaths <= target:
                perfect_text = "挑戰成功！"
                text = self.font_medium.render(perfect_text, True, GREEN)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 400))
                screen.blit(text, text_rect)

        # 操作說明
        if self.current_level < TOTAL_LEVELS:
            continue_text = "Enter 繼續下一關"
        else:
            continue_text = "你已完成所有關卡！"

        text = self.font_small.render(continue_text, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 480))
        screen.blit(text, text_rect)

        back_text = "ESC 返回主選單"
        text = self.font_small.render(back_text, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 510))
        screen.blit(text, text_rect)

        # F11全屏快捷鍵說明
        fullscreen_text = "F11 切換全屏"
        text = self.font_small.render(fullscreen_text, True, GRAY)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 540))
        screen.blit(text, text_rect)

    def draw(self):
        """繪製畫面"""
        if self.state == MENU:
            self.draw_menu()
        elif self.state == LEVEL_SELECT:
            self.draw_level_select()
        elif self.state == PLAYING:
            self.draw_playing()
        elif self.state == VICTORY:
            self.draw_victory()

        pygame.display.flip()

    def run(self):
        """主遊戲循環"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
