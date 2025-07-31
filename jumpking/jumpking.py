import pygame
import math
import json
import os

# 初始化 Pygame
pygame.init()

# 遊戲設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
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
TOTAL_LEVELS = 10


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
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

    def update(self, platforms, death_zones=None):
        # 處理重力
        if not self.on_ground:
            self.vel_y += GRAVITY
            if self.vel_y > MAX_FALL_SPEED:
                self.vel_y = MAX_FALL_SPEED

        # 更新位置
        self.x += self.vel_x
        self.y += self.vel_y

        # 檢查死亡區域
        if death_zones:
            for zone in death_zones:
                if (self.x < zone["x"] + zone["width"] and 
                    self.x + self.width > zone["x"] and
                    self.y < zone["y"] + zone["height"] and 
                    self.y + self.height > zone["y"]):
                    return "death"

        # 檢查平台碰撞
        self.check_platform_collision(platforms)

        # 減少水平速度（摩擦力）
        if self.on_ground:
            self.vel_x *= 0.8
        else:
            self.vel_x *= 0.95

        return None

    def check_platform_collision(self, platforms):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        was_on_ground = self.on_ground
        self.on_ground = False

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
                    self.on_ground = True
                elif min_overlap == overlap_bottom and self.vel_y <= 0:
                    # 從下方撞擊
                    self.y = platform["y"] + platform["height"]
                    self.vel_y = 0
                elif min_overlap == overlap_left and self.vel_x >= 0:
                    # 從左側撞擊
                    self.x = platform["x"] - self.width
                    self.vel_x = 0
                elif min_overlap == overlap_right and self.vel_x <= 0:
                    # 從右側撞擊
                    self.x = platform["x"] + platform["width"]
                    self.vel_x = 0

        # 簡化地面檢測 - 如果玩家底部接觸任何平台就算在地面上
        if not self.on_ground:
            # 檢查玩家底部是否接觸平台
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
                        self.on_ground = True
                        self.y = platform_top - self.height
                        self.vel_y = 0
                        break

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
            "target_deaths": 5  # 期望死亡次數
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
            "target_deaths": 8
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
            "target_deaths": 12
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
            "target_deaths": 15
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
            "target_deaths": 20
        }
        
        # 第6關 - 高級挑戰
        levels[6] = {
            "name": "高手之路",
            "platforms": [
                {"x": 0, "y": 550, "width": 60, "height": 50},
                {"x": 100, "y": 500, "width": 20, "height": 10},
                {"x": 180, "y": 460, "width": 20, "height": 10},
                {"x": 260, "y": 420, "width": 20, "height": 10},
                {"x": 340, "y": 380, "width": 20, "height": 10},
                {"x": 420, "y": 340, "width": 20, "height": 10},
                {"x": 500, "y": 300, "width": 20, "height": 10},
                {"x": 580, "y": 260, "width": 20, "height": 10},
                {"x": 660, "y": 220, "width": 20, "height": 10},
                {"x": 580, "y": 180, "width": 20, "height": 10},
                {"x": 500, "y": 140, "width": 20, "height": 10},
                {"x": 420, "y": 100, "width": 20, "height": 10},
                {"x": 340, "y": 60, "width": 20, "height": 10},
                {"x": 260, "y": 20, "width": 20, "height": 10},
                {"x": 350, "y": -40, "width": 100, "height": 30},
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 800, "height": 100},
                {"x": 60, "y": 400, "width": 40, "height": 200},
                {"x": 300, "y": 300, "width": 40, "height": 200},
                {"x": 540, "y": 200, "width": 40, "height": 200},
            ],
            "goal_y": -40,
            "start_pos": (30, 500),
            "target_deaths": 30
        }
        
        # 第7關 - 專家級
        levels[7] = {
            "name": "專家考驗",
            "platforms": [
                {"x": 0, "y": 550, "width": 50, "height": 50},
                {"x": 80, "y": 520, "width": 15, "height": 8},
                {"x": 130, "y": 490, "width": 15, "height": 8},
                {"x": 180, "y": 460, "width": 15, "height": 8},
                {"x": 230, "y": 430, "width": 15, "height": 8},
                {"x": 280, "y": 400, "width": 15, "height": 8},
                {"x": 330, "y": 370, "width": 15, "height": 8},
                {"x": 380, "y": 340, "width": 15, "height": 8},
                {"x": 430, "y": 310, "width": 15, "height": 8},
                {"x": 480, "y": 280, "width": 15, "height": 8},
                {"x": 530, "y": 250, "width": 15, "height": 8},
                {"x": 580, "y": 220, "width": 15, "height": 8},
                {"x": 630, "y": 190, "width": 15, "height": 8},
                {"x": 680, "y": 160, "width": 15, "height": 8},
                {"x": 630, "y": 130, "width": 15, "height": 8},
                {"x": 580, "y": 100, "width": 15, "height": 8},
                {"x": 530, "y": 70, "width": 15, "height": 8},
                {"x": 480, "y": 40, "width": 15, "height": 8},
                {"x": 430, "y": 10, "width": 15, "height": 8},
                {"x": 350, "y": -30, "width": 100, "height": 30},
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 800, "height": 100},
                {"x": 50, "y": 450, "width": 30, "height": 150},
                {"x": 200, "y": 350, "width": 30, "height": 150},
                {"x": 350, "y": 250, "width": 30, "height": 150},
                {"x": 500, "y": 150, "width": 30, "height": 150},
                {"x": 650, "y": 100, "width": 30, "height": 150},
            ],
            "goal_y": -30,
            "start_pos": (25, 500),
            "target_deaths": 50
        }
        
        # 第8關 - 大師級
        levels[8] = {
            "name": "大師挑戰",
            "platforms": [
                {"x": 0, "y": 550, "width": 40, "height": 50},
                {"x": 60, "y": 530, "width": 10, "height": 5},
                {"x": 90, "y": 510, "width": 10, "height": 5},
                {"x": 120, "y": 490, "width": 10, "height": 5},
                {"x": 150, "y": 470, "width": 10, "height": 5},
                {"x": 180, "y": 450, "width": 10, "height": 5},
                {"x": 210, "y": 430, "width": 10, "height": 5},
                {"x": 240, "y": 410, "width": 10, "height": 5},
                {"x": 270, "y": 390, "width": 10, "height": 5},
                {"x": 300, "y": 370, "width": 10, "height": 5},
                {"x": 330, "y": 350, "width": 10, "height": 5},
                {"x": 360, "y": 330, "width": 10, "height": 5},
                {"x": 390, "y": 310, "width": 10, "height": 5},
                {"x": 420, "y": 290, "width": 10, "height": 5},
                {"x": 450, "y": 270, "width": 10, "height": 5},
                {"x": 480, "y": 250, "width": 10, "height": 5},
                {"x": 510, "y": 230, "width": 10, "height": 5},
                {"x": 540, "y": 210, "width": 10, "height": 5},
                {"x": 570, "y": 190, "width": 10, "height": 5},
                {"x": 600, "y": 170, "width": 10, "height": 5},
                {"x": 630, "y": 150, "width": 10, "height": 5},
                {"x": 660, "y": 130, "width": 10, "height": 5},
                {"x": 690, "y": 110, "width": 10, "height": 5},
                {"x": 720, "y": 90, "width": 10, "height": 5},
                {"x": 690, "y": 70, "width": 10, "height": 5},
                {"x": 660, "y": 50, "width": 10, "height": 5},
                {"x": 630, "y": 30, "width": 10, "height": 5},
                {"x": 600, "y": 10, "width": 10, "height": 5},
                {"x": 570, "y": -10, "width": 10, "height": 5},
                {"x": 540, "y": -30, "width": 10, "height": 5},
                {"x": 510, "y": -50, "width": 10, "height": 5},
                {"x": 480, "y": -70, "width": 10, "height": 5},
                {"x": 450, "y": -90, "width": 10, "height": 5},
                {"x": 350, "y": -120, "width": 100, "height": 30},
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 800, "height": 100},
                {"x": 40, "y": 450, "width": 20, "height": 150},
                {"x": 130, "y": 400, "width": 20, "height": 150},
                {"x": 220, "y": 350, "width": 20, "height": 150},
                {"x": 310, "y": 300, "width": 20, "height": 150},
                {"x": 400, "y": 250, "width": 20, "height": 150},
                {"x": 490, "y": 200, "width": 20, "height": 150},
                {"x": 580, "y": 150, "width": 20, "height": 150},
                {"x": 670, "y": 100, "width": 20, "height": 150},
                {"x": 760, "y": 50, "width": 40, "height": 150},
            ],
            "goal_y": -120,
            "start_pos": (20, 500),
            "target_deaths": 70
        }
        
        # 第9關 - 傳說級
        levels[9] = {
            "name": "傳說試煉",
            "platforms": [
                {"x": 0, "y": 550, "width": 30, "height": 50},
                {"x": 50, "y": 540, "width": 8, "height": 3},
                {"x": 70, "y": 530, "width": 8, "height": 3},
                {"x": 90, "y": 520, "width": 8, "height": 3},
                {"x": 110, "y": 510, "width": 8, "height": 3},
                {"x": 130, "y": 500, "width": 8, "height": 3},
                {"x": 150, "y": 490, "width": 8, "height": 3},
                {"x": 170, "y": 480, "width": 8, "height": 3},
                {"x": 190, "y": 470, "width": 8, "height": 3},
                {"x": 210, "y": 460, "width": 8, "height": 3},
                {"x": 230, "y": 450, "width": 8, "height": 3},
                {"x": 250, "y": 440, "width": 8, "height": 3},
                {"x": 270, "y": 430, "width": 8, "height": 3},
                {"x": 290, "y": 420, "width": 8, "height": 3},
                {"x": 310, "y": 410, "width": 8, "height": 3},
                {"x": 330, "y": 400, "width": 8, "height": 3},
                {"x": 350, "y": 390, "width": 8, "height": 3},
                {"x": 370, "y": 380, "width": 8, "height": 3},
                {"x": 390, "y": 370, "width": 8, "height": 3},
                {"x": 410, "y": 360, "width": 8, "height": 3},
                {"x": 430, "y": 350, "width": 8, "height": 3},
                {"x": 450, "y": 340, "width": 8, "height": 3},
                {"x": 470, "y": 330, "width": 8, "height": 3},
                {"x": 490, "y": 320, "width": 8, "height": 3},
                {"x": 510, "y": 310, "width": 8, "height": 3},
                {"x": 530, "y": 300, "width": 8, "height": 3},
                {"x": 550, "y": 290, "width": 8, "height": 3},
                {"x": 570, "y": 280, "width": 8, "height": 3},
                {"x": 590, "y": 270, "width": 8, "height": 3},
                {"x": 610, "y": 260, "width": 8, "height": 3},
                {"x": 630, "y": 250, "width": 8, "height": 3},
                {"x": 650, "y": 240, "width": 8, "height": 3},
                {"x": 670, "y": 230, "width": 8, "height": 3},
                {"x": 690, "y": 220, "width": 8, "height": 3},
                {"x": 710, "y": 210, "width": 8, "height": 3},
                {"x": 730, "y": 200, "width": 8, "height": 3},
                {"x": 750, "y": 190, "width": 8, "height": 3},
                {"x": 770, "y": 180, "width": 8, "height": 3},
                {"x": 750, "y": 170, "width": 8, "height": 3},
                {"x": 730, "y": 160, "width": 8, "height": 3},
                {"x": 710, "y": 150, "width": 8, "height": 3},
                {"x": 690, "y": 140, "width": 8, "height": 3},
                {"x": 670, "y": 130, "width": 8, "height": 3},
                {"x": 650, "y": 120, "width": 8, "height": 3},
                {"x": 630, "y": 110, "width": 8, "height": 3},
                {"x": 610, "y": 100, "width": 8, "height": 3},
                {"x": 590, "y": 90, "width": 8, "height": 3},
                {"x": 570, "y": 80, "width": 8, "height": 3},
                {"x": 550, "y": 70, "width": 8, "height": 3},
                {"x": 530, "y": 60, "width": 8, "height": 3},
                {"x": 510, "y": 50, "width": 8, "height": 3},
                {"x": 490, "y": 40, "width": 8, "height": 3},
                {"x": 470, "y": 30, "width": 8, "height": 3},
                {"x": 450, "y": 20, "width": 8, "height": 3},
                {"x": 430, "y": 10, "width": 8, "height": 3},
                {"x": 410, "y": 0, "width": 8, "height": 3},
                {"x": 390, "y": -10, "width": 8, "height": 3},
                {"x": 370, "y": -20, "width": 8, "height": 3},
                {"x": 350, "y": -30, "width": 8, "height": 3},
                {"x": 330, "y": -40, "width": 8, "height": 3},
                {"x": 310, "y": -50, "width": 8, "height": 3},
                {"x": 290, "y": -60, "width": 8, "height": 3},
                {"x": 270, "y": -70, "width": 8, "height": 3},
                {"x": 250, "y": -80, "width": 8, "height": 3},
                {"x": 230, "y": -90, "width": 8, "height": 3},
                {"x": 210, "y": -100, "width": 8, "height": 3},
                {"x": 190, "y": -110, "width": 8, "height": 3},
                {"x": 170, "y": -120, "width": 8, "height": 3},
                {"x": 150, "y": -130, "width": 8, "height": 3},
                {"x": 130, "y": -140, "width": 8, "height": 3},
                {"x": 110, "y": -150, "width": 8, "height": 3},
                {"x": 350, "y": -180, "width": 100, "height": 30},
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 800, "height": 100},
                # 大量的死亡陷阱
                {"x": 30, "y": 500, "width": 20, "height": 100},
                {"x": 80, "y": 480, "width": 20, "height": 100},
                {"x": 130, "y": 460, "width": 20, "height": 100},
                {"x": 180, "y": 440, "width": 20, "height": 100},
                {"x": 230, "y": 420, "width": 20, "height": 100},
                {"x": 280, "y": 400, "width": 20, "height": 100},
                {"x": 330, "y": 380, "width": 20, "height": 100},
                {"x": 380, "y": 360, "width": 20, "height": 100},
                {"x": 430, "y": 340, "width": 20, "height": 100},
                {"x": 480, "y": 320, "width": 20, "height": 100},
                {"x": 530, "y": 300, "width": 20, "height": 100},
                {"x": 580, "y": 280, "width": 20, "height": 100},
                {"x": 630, "y": 260, "width": 20, "height": 100},
                {"x": 680, "y": 240, "width": 20, "height": 100},
                {"x": 730, "y": 220, "width": 20, "height": 100},
                {"x": 780, "y": 200, "width": 20, "height": 100},
            ],
            "goal_y": -180,
            "start_pos": (15, 500),
            "target_deaths": 90
        }
        
        # 第10關 - 終極挑戰（需要死100次的超難關卡）
        levels[10] = {
            "name": "絕望深淵",
            "platforms": [
                {"x": 0, "y": 550, "width": 25, "height": 50},
                # 極窄平台組成的地獄之路
                {"x": 35, "y": 545, "width": 5, "height": 2},
                {"x": 50, "y": 540, "width": 5, "height": 2},
                {"x": 65, "y": 535, "width": 5, "height": 2},
                {"x": 80, "y": 530, "width": 5, "height": 2},
                {"x": 95, "y": 525, "width": 5, "height": 2},
                {"x": 110, "y": 520, "width": 5, "height": 2},
                {"x": 125, "y": 515, "width": 5, "height": 2},
                {"x": 140, "y": 510, "width": 5, "height": 2},
                {"x": 155, "y": 505, "width": 5, "height": 2},
                {"x": 170, "y": 500, "width": 5, "height": 2},
                {"x": 185, "y": 495, "width": 5, "height": 2},
                {"x": 200, "y": 490, "width": 5, "height": 2},
                {"x": 215, "y": 485, "width": 5, "height": 2},
                {"x": 230, "y": 480, "width": 5, "height": 2},
                {"x": 245, "y": 475, "width": 5, "height": 2},
                {"x": 260, "y": 470, "width": 5, "height": 2},
                {"x": 275, "y": 465, "width": 5, "height": 2},
                {"x": 290, "y": 460, "width": 5, "height": 2},
                {"x": 305, "y": 455, "width": 5, "height": 2},
                {"x": 320, "y": 450, "width": 5, "height": 2},
                {"x": 335, "y": 445, "width": 5, "height": 2},
                {"x": 350, "y": 440, "width": 5, "height": 2},
                {"x": 365, "y": 435, "width": 5, "height": 2},
                {"x": 380, "y": 430, "width": 5, "height": 2},
                {"x": 395, "y": 425, "width": 5, "height": 2},
                {"x": 410, "y": 420, "width": 5, "height": 2},
                {"x": 425, "y": 415, "width": 5, "height": 2},
                {"x": 440, "y": 410, "width": 5, "height": 2},
                {"x": 455, "y": 405, "width": 5, "height": 2},
                {"x": 470, "y": 400, "width": 5, "height": 2},
                {"x": 485, "y": 395, "width": 5, "height": 2},
                {"x": 500, "y": 390, "width": 5, "height": 2},
                {"x": 515, "y": 385, "width": 5, "height": 2},
                {"x": 530, "y": 380, "width": 5, "height": 2},
                {"x": 545, "y": 375, "width": 5, "height": 2},
                {"x": 560, "y": 370, "width": 5, "height": 2},
                {"x": 575, "y": 365, "width": 5, "height": 2},
                {"x": 590, "y": 360, "width": 5, "height": 2},
                {"x": 605, "y": 355, "width": 5, "height": 2},
                {"x": 620, "y": 350, "width": 5, "height": 2},
                {"x": 635, "y": 345, "width": 5, "height": 2},
                {"x": 650, "y": 340, "width": 5, "height": 2},
                {"x": 665, "y": 335, "width": 5, "height": 2},
                {"x": 680, "y": 330, "width": 5, "height": 2},
                {"x": 695, "y": 325, "width": 5, "height": 2},
                {"x": 710, "y": 320, "width": 5, "height": 2},
                {"x": 725, "y": 315, "width": 5, "height": 2},
                {"x": 740, "y": 310, "width": 5, "height": 2},
                {"x": 755, "y": 305, "width": 5, "height": 2},
                {"x": 770, "y": 300, "width": 5, "height": 2},
                
                # 更多極窄平台繼續向上...
                {"x": 785, "y": 295, "width": 5, "height": 2},
                {"x": 770, "y": 290, "width": 5, "height": 2},
                {"x": 755, "y": 285, "width": 5, "height": 2},
                {"x": 740, "y": 280, "width": 5, "height": 2},
                {"x": 725, "y": 275, "width": 5, "height": 2},
                {"x": 710, "y": 270, "width": 5, "height": 2},
                {"x": 695, "y": 265, "width": 5, "height": 2},
                {"x": 680, "y": 260, "width": 5, "height": 2},
                {"x": 665, "y": 255, "width": 5, "height": 2},
                {"x": 650, "y": 250, "width": 5, "height": 2},
                {"x": 635, "y": 245, "width": 5, "height": 2},
                {"x": 620, "y": 240, "width": 5, "height": 2},
                {"x": 605, "y": 235, "width": 5, "height": 2},
                {"x": 590, "y": 230, "width": 5, "height": 2},
                {"x": 575, "y": 225, "width": 5, "height": 2},
                {"x": 560, "y": 220, "width": 5, "height": 2},
                {"x": 545, "y": 215, "width": 5, "height": 2},
                {"x": 530, "y": 210, "width": 5, "height": 2},
                {"x": 515, "y": 205, "width": 5, "height": 2},
                {"x": 500, "y": 200, "width": 5, "height": 2},
                {"x": 485, "y": 195, "width": 5, "height": 2},
                {"x": 470, "y": 190, "width": 5, "height": 2},
                {"x": 455, "y": 185, "width": 5, "height": 2},
                {"x": 440, "y": 180, "width": 5, "height": 2},
                {"x": 425, "y": 175, "width": 5, "height": 2},
                {"x": 410, "y": 170, "width": 5, "height": 2},
                {"x": 395, "y": 165, "width": 5, "height": 2},
                {"x": 380, "y": 160, "width": 5, "height": 2},
                {"x": 365, "y": 155, "width": 5, "height": 2},
                {"x": 350, "y": 150, "width": 5, "height": 2},
                {"x": 335, "y": 145, "width": 5, "height": 2},
                {"x": 320, "y": 140, "width": 5, "height": 2},
                {"x": 305, "y": 135, "width": 5, "height": 2},
                {"x": 290, "y": 130, "width": 5, "height": 2},
                {"x": 275, "y": 125, "width": 5, "height": 2},
                {"x": 260, "y": 120, "width": 5, "height": 2},
                {"x": 245, "y": 115, "width": 5, "height": 2},
                {"x": 230, "y": 110, "width": 5, "height": 2},
                {"x": 215, "y": 105, "width": 5, "height": 2},
                {"x": 200, "y": 100, "width": 5, "height": 2},
                {"x": 185, "y": 95, "width": 5, "height": 2},
                {"x": 170, "y": 90, "width": 5, "height": 2},
                {"x": 155, "y": 85, "width": 5, "height": 2},
                {"x": 140, "y": 80, "width": 5, "height": 2},
                {"x": 125, "y": 75, "width": 5, "height": 2},
                {"x": 110, "y": 70, "width": 5, "height": 2},
                {"x": 95, "y": 65, "width": 5, "height": 2},
                {"x": 80, "y": 60, "width": 5, "height": 2},
                {"x": 65, "y": 55, "width": 5, "height": 2},
                {"x": 50, "y": 50, "width": 5, "height": 2},
                {"x": 35, "y": 45, "width": 5, "height": 2},
                {"x": 20, "y": 40, "width": 5, "height": 2},
                {"x": 5, "y": 35, "width": 5, "height": 2},
                {"x": 20, "y": 30, "width": 5, "height": 2},
                {"x": 35, "y": 25, "width": 5, "height": 2},
                {"x": 50, "y": 20, "width": 5, "height": 2},
                {"x": 65, "y": 15, "width": 5, "height": 2},
                {"x": 80, "y": 10, "width": 5, "height": 2},
                {"x": 95, "y": 5, "width": 5, "height": 2},
                {"x": 110, "y": 0, "width": 5, "height": 2},
                {"x": 125, "y": -5, "width": 5, "height": 2},
                {"x": 140, "y": -10, "width": 5, "height": 2},
                {"x": 155, "y": -15, "width": 5, "height": 2},
                {"x": 170, "y": -20, "width": 5, "height": 2},
                {"x": 185, "y": -25, "width": 5, "height": 2},
                {"x": 200, "y": -30, "width": 5, "height": 2},
                {"x": 215, "y": -35, "width": 5, "height": 2},
                {"x": 230, "y": -40, "width": 5, "height": 2},
                {"x": 245, "y": -45, "width": 5, "height": 2},
                {"x": 260, "y": -50, "width": 5, "height": 2},
                {"x": 275, "y": -55, "width": 5, "height": 2},
                {"x": 290, "y": -60, "width": 5, "height": 2},
                {"x": 305, "y": -65, "width": 5, "height": 2},
                {"x": 320, "y": -70, "width": 5, "height": 2},
                {"x": 335, "y": -75, "width": 5, "height": 2},
                {"x": 350, "y": -80, "width": 5, "height": 2},
                {"x": 365, "y": -85, "width": 5, "height": 2},
                {"x": 380, "y": -90, "width": 5, "height": 2},
                {"x": 395, "y": -95, "width": 5, "height": 2},
                {"x": 410, "y": -100, "width": 5, "height": 2},
                {"x": 425, "y": -105, "width": 5, "height": 2},
                {"x": 440, "y": -110, "width": 5, "height": 2},
                {"x": 455, "y": -115, "width": 5, "height": 2},
                {"x": 470, "y": -120, "width": 5, "height": 2},
                {"x": 485, "y": -125, "width": 5, "height": 2},
                {"x": 500, "y": -130, "width": 5, "height": 2},
                {"x": 515, "y": -135, "width": 5, "height": 2},
                {"x": 530, "y": -140, "width": 5, "height": 2},
                {"x": 545, "y": -145, "width": 5, "height": 2},
                {"x": 560, "y": -150, "width": 5, "height": 2},
                {"x": 575, "y": -155, "width": 5, "height": 2},
                {"x": 590, "y": -160, "width": 5, "height": 2},
                {"x": 605, "y": -165, "width": 5, "height": 2},
                {"x": 620, "y": -170, "width": 5, "height": 2},
                {"x": 635, "y": -175, "width": 5, "height": 2},
                {"x": 650, "y": -180, "width": 5, "height": 2},
                {"x": 665, "y": -185, "width": 5, "height": 2},
                {"x": 680, "y": -190, "width": 5, "height": 2},
                {"x": 695, "y": -195, "width": 5, "height": 2},
                {"x": 710, "y": -200, "width": 5, "height": 2},
                {"x": 725, "y": -205, "width": 5, "height": 2},
                {"x": 740, "y": -210, "width": 5, "height": 2},
                {"x": 755, "y": -215, "width": 5, "height": 2},
                {"x": 770, "y": -220, "width": 5, "height": 2},
                
                # 最終目標平台
                {"x": 350, "y": -250, "width": 100, "height": 30},
            ],
            "death_zones": [
                # 幾乎每個平台之間都有死亡陷阱
                {"x": 0, "y": 600, "width": 800, "height": 100},
                {"x": 25, "y": 500, "width": 10, "height": 50},
                {"x": 40, "y": 495, "width": 10, "height": 50},
                {"x": 55, "y": 490, "width": 10, "height": 50},
                {"x": 70, "y": 485, "width": 10, "height": 50},
                {"x": 85, "y": 480, "width": 10, "height": 50},
                {"x": 100, "y": 475, "width": 10, "height": 50},
                {"x": 115, "y": 470, "width": 10, "height": 50},
                {"x": 130, "y": 465, "width": 10, "height": 50},
                {"x": 145, "y": 460, "width": 10, "height": 50},
                {"x": 160, "y": 455, "width": 10, "height": 50},
                {"x": 175, "y": 450, "width": 10, "height": 50},
                {"x": 190, "y": 445, "width": 10, "height": 50},
                {"x": 205, "y": 440, "width": 10, "height": 50},
                {"x": 220, "y": 435, "width": 10, "height": 50},
                {"x": 235, "y": 430, "width": 10, "height": 50},
                {"x": 250, "y": 425, "width": 10, "height": 50},
                {"x": 265, "y": 420, "width": 10, "height": 50},
                {"x": 280, "y": 415, "width": 10, "height": 50},
                {"x": 295, "y": 410, "width": 10, "height": 50},
                {"x": 310, "y": 405, "width": 10, "height": 50},
                {"x": 325, "y": 400, "width": 10, "height": 50},
                {"x": 340, "y": 395, "width": 10, "height": 50},
                {"x": 355, "y": 390, "width": 10, "height": 50},
                {"x": 370, "y": 385, "width": 10, "height": 50},
                {"x": 385, "y": 380, "width": 10, "height": 50},
                {"x": 400, "y": 375, "width": 10, "height": 50},
                {"x": 415, "y": 370, "width": 10, "height": 50},
                {"x": 430, "y": 365, "width": 10, "height": 50},
                {"x": 445, "y": 360, "width": 10, "height": 50},
                {"x": 460, "y": 355, "width": 10, "height": 50},
                {"x": 475, "y": 350, "width": 10, "height": 50},
                {"x": 490, "y": 345, "width": 10, "height": 50},
                {"x": 505, "y": 340, "width": 10, "height": 50},
                {"x": 520, "y": 335, "width": 10, "height": 50},
                {"x": 535, "y": 330, "width": 10, "height": 50},
                {"x": 550, "y": 325, "width": 10, "height": 50},
                {"x": 565, "y": 320, "width": 10, "height": 50},
                {"x": 580, "y": 315, "width": 10, "height": 50},
                {"x": 595, "y": 310, "width": 10, "height": 50},
                {"x": 610, "y": 305, "width": 10, "height": 50},
                {"x": 625, "y": 300, "width": 10, "height": 50},
                {"x": 640, "y": 295, "width": 10, "height": 50},
                {"x": 655, "y": 290, "width": 10, "height": 50},
                {"x": 670, "y": 285, "width": 10, "height": 50},
                {"x": 685, "y": 280, "width": 10, "height": 50},
                {"x": 700, "y": 275, "width": 10, "height": 50},
                {"x": 715, "y": 270, "width": 10, "height": 50},
                {"x": 730, "y": 265, "width": 10, "height": 50},
                {"x": 745, "y": 260, "width": 10, "height": 50},
                {"x": 760, "y": 255, "width": 10, "height": 50},
                {"x": 775, "y": 250, "width": 10, "height": 50},
                {"x": 790, "y": 245, "width": 10, "height": 50},
            ],
            "goal_y": -250,
            "start_pos": (12, 500),
            "target_deaths": 100
        }
        
        return levels
    
    def get_level(self, level_num):
        """獲取指定關卡"""
        return self.levels.get(level_num)
class Game:
    def __init__(self):
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
        font_path = "C:\\Windows\\Fonts\\msjh.ttc"  # 微軟正黑體
        try:
            self.font_large = pygame.font.Font(font_path, 48)
            self.font_medium = pygame.font.Font(font_path, 36)
            self.font_small = pygame.font.Font(font_path, 24)
        except:
            # 如果載入失敗，使用系統預設字體
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)
        
        # 選單選項
        self.menu_selection = 0
        self.level_select_selection = 1
        
    def load_progress(self):
        """載入遊戲進度"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, "r", encoding='utf-8') as f:
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
                "level_stats": self.level_stats
            }
            with open(self.save_file, "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def start_level(self, level_num):
        """開始指定關卡"""
        level_data = self.level_manager.get_level(level_num)
        if not level_data:
            return
        
        self.current_level = level_num
        start_x, start_y = level_data["start_pos"]
        self.player = Player(start_x, start_y)
        self.camera_y = 0
        self.state = PLAYING
        
        # 初始化關卡統計
        if str(level_num) not in self.level_stats:
            self.level_stats[str(level_num)] = {
                "deaths": 0,
                "completed": False,
                "best_deaths": None
            }
    
    def complete_level(self):
        """完成關卡"""
        level_key = str(self.current_level)
        if level_key in self.level_stats:
            self.level_stats[level_key]["completed"] = True
            deaths = self.player.death_count
            
            # 更新最佳記錄
            if (self.level_stats[level_key]["best_deaths"] is None or 
                deaths < self.level_stats[level_key]["best_deaths"]):
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
                        if (str(i) not in self.level_stats or 
                            not self.level_stats[str(i)]["completed"]):
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
            else:
                if self.state == MENU:
                    self.handle_menu_events(event)
                elif self.state == LEVEL_SELECT:
                    self.handle_level_select_events(event)
                elif self.state == PLAYING:
                    self.handle_playing_events(event)
                elif self.state in [VICTORY, GAME_OVER]:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.state = LEVEL_SELECT
                        elif event.key == pygame.K_ESCAPE:
                            self.state = MENU
    
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
        result = self.player.update(level_data["platforms"], level_data["death_zones"])
        
        # 檢查死亡
        if result == "death":
            self.player.reset_position()
            self.level_stats[str(self.current_level)]["deaths"] = self.player.death_count
            self.save_progress()
        
        # 更新相機
        self.update_camera()
        
        # 檢查是否到達目標
        if self.player.y <= level_data["goal_y"]:
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
        self.screen.fill(DARK_BLUE)
        
        # 標題
        title = self.font_large.render("Jump King - 十關挑戰", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # 副標題
        subtitle = self.font_medium.render("考驗你的耐心與技巧", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(subtitle, subtitle_rect)
        
        # 選單選項
        menu_options = ["開始遊戲", "繼續遊戲", "退出遊戲"]
        for i, option in enumerate(menu_options):
            color = YELLOW if i == self.menu_selection else WHITE
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 50))
            self.screen.blit(text, text_rect)
        
        # 進度資訊
        progress_text = f"已解鎖關卡: {self.unlocked_levels}/{TOTAL_LEVELS}"
        progress = self.font_small.render(progress_text, True, GREEN)
        progress_rect = progress.get_rect(center=(SCREEN_WIDTH // 2, 500))
        self.screen.blit(progress, progress_rect)
        
        # 操作說明
        controls = [
            "↑↓ 選擇",
            "Enter 確認",
            "ESC 退出"
        ]
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, GRAY)
            self.screen.blit(text, (50, 500 + i * 25))
    
    def draw_level_select(self):
        """繪製關卡選擇畫面"""
        self.screen.fill(DARK_BLUE)
        
        # 標題
        title = self.font_large.render("選擇關卡", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # 關卡選項
        start_x = 50
        start_y = 200
        cols = 5
        rows = 2
        
        for level in range(1, TOTAL_LEVELS + 1):
            row = (level - 1) // cols
            col = (level - 1) % cols
            x = start_x + col * 140
            y = start_y + row * 120
            
            # 判斷關卡狀態
            if level > self.unlocked_levels:
                # 未解鎖
                color = GRAY
                text_color = BLACK
                status = "鎖定"
            elif str(level) in self.level_stats and self.level_stats[str(level)]["completed"]:
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
                pygame.draw.rect(self.screen, YELLOW, (x-5, y-5, 110, 90), 3)
            
            # 關卡方塊
            pygame.draw.rect(self.screen, color, (x, y, 100, 80))
            
            # 關卡編號
            level_text = self.font_medium.render(f"第{level}關", True, text_color)
            level_rect = level_text.get_rect(center=(x + 50, y + 20))
            self.screen.blit(level_text, level_rect)
            
            # 關卡名稱
            level_data = self.level_manager.get_level(level)
            if level_data:
                name_text = self.font_small.render(level_data["name"], True, text_color)
                name_rect = name_text.get_rect(center=(x + 50, y + 40))
                self.screen.blit(name_text, name_rect)
            
            # 狀態
            for i, line in enumerate(status.split('\n')):
                status_text = self.font_small.render(line, True, text_color)
                status_rect = status_text.get_rect(center=(x + 50, y + 55 + i * 12))
                self.screen.blit(status_text, status_rect)
        
        # 關卡詳情
        if 1 <= self.level_select_selection <= TOTAL_LEVELS:
            level_data = self.level_manager.get_level(self.level_select_selection)
            if level_data:
                detail_y = 450
                
                # 關卡名稱
                name = self.font_medium.render(f"第{self.level_select_selection}關: {level_data['name']}", True, YELLOW)
                name_rect = name.get_rect(center=(SCREEN_WIDTH // 2, detail_y))
                self.screen.blit(name, name_rect)
                
                # 目標死亡次數
                target = self.font_small.render(f"挑戰目標: {level_data['target_deaths']}次死亡內完成", True, WHITE)
                target_rect = target.get_rect(center=(SCREEN_WIDTH // 2, detail_y + 30))
                self.screen.blit(target, target_rect)
        
        # 操作說明
        controls = [
            "← → 選擇關卡",
            "Enter 開始",
            "ESC 返回"
        ]
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, GRAY)
            self.screen.blit(text, (50, 550 + i * 20))
    
    def draw_playing(self):
        """繪製遊戲畫面"""
        self.screen.fill(DARK_BLUE)
        
        if not self.player:
            return
        
        # 獲取當前關卡資料
        level_data = self.level_manager.get_level(self.current_level)
        if not level_data:
            return
        
        # 繪製平台
        for platform in level_data["platforms"]:
            color = BROWN
            if platform["y"] <= level_data["goal_y"]:  # 目標平台
                color = YELLOW
            pygame.draw.rect(
                self.screen,
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
                self.screen,
                RED,
                (
                    zone["x"],
                    zone["y"] - self.camera_y,
                    zone["width"],
                    zone["height"],
                ),
            )
        
        # 繪製玩家
        self.player.draw(self.screen, self.camera_y)
        
        # 繪製UI
        self.draw_playing_ui(level_data)
    
    def draw_playing_ui(self, level_data):
        """繪製遊戲中的UI"""
        # 關卡資訊
        level_text = f"第{self.current_level}關: {level_data['name']}"
        text = self.font_medium.render(level_text, True, YELLOW)
        self.screen.blit(text, (10, 10))
        
        # 死亡次數
        deaths_text = f"死亡次數: {self.player.death_count}"
        text = self.font_small.render(deaths_text, True, WHITE)
        self.screen.blit(text, (10, 45))
        
        # 目標
        target_text = f"目標: {level_data['target_deaths']}次內完成"
        color = GREEN if self.player.death_count <= level_data['target_deaths'] else RED
        text = self.font_small.render(target_text, True, color)
        self.screen.blit(text, (10, 70))
        
        # 高度
        height = max(0, int((level_data["start_pos"][1] - self.player.y) / 10))
        height_text = f"高度: {height}m"
        text = self.font_small.render(height_text, True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH - 150, 10))
        
        # 控制說明
        controls = [
            "按住 SPACE 蓄力",
            "蓄力時按 ← → 選方向",
            "放開 SPACE 跳躍",
            "R 重置位置",
            "ESC 返回選單"
        ]
        
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, WHITE)
            self.screen.blit(text, (10, SCREEN_HEIGHT - 140 + i * 20))
        
        # 玩家狀態
        status_text = f"在地面: {'是' if self.player.on_ground else '否'}"
        color = GREEN if self.player.on_ground else RED
        text = self.font_small.render(status_text, True, color)
        self.screen.blit(text, (SCREEN_WIDTH - 150, 35))
        
        # 蓄力狀態
        if self.player.jump_charging:
            charge_text = f"蓄力: {self.player.jump_power:.1f}"
            text = self.font_small.render(charge_text, True, YELLOW)
            self.screen.blit(text, (SCREEN_WIDTH - 150, 60))
    
    def draw_victory(self):
        """繪製勝利畫面"""
        self.screen.fill(DARK_BLUE)
        
        # 勝利訊息
        title = self.font_large.render("恭喜過關！", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)
        
        # 統計資料
        level_data = self.level_manager.get_level(self.current_level)
        if level_data:
            deaths = self.player.death_count
            target = level_data['target_deaths']
            
            stats_text = f"第{self.current_level}關: {level_data['name']}"
            text = self.font_medium.render(stats_text, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 280))
            self.screen.blit(text, text_rect)
            
            deaths_text = f"死亡次數: {deaths}"
            color = GREEN if deaths <= target else RED
            text = self.font_medium.render(deaths_text, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 320))
            self.screen.blit(text, text_rect)
            
            target_text = f"目標: {target}次"
            text = self.font_medium.render(target_text, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 360))
            self.screen.blit(text, text_rect)
            
            if deaths <= target:
                perfect_text = "挑戰成功！"
                text = self.font_medium.render(perfect_text, True, GREEN)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 400))
                self.screen.blit(text, text_rect)
        
        # 操作說明
        if self.current_level < TOTAL_LEVELS:
            continue_text = "Enter 繼續下一關"
        else:
            continue_text = "你已完成所有關卡！"
        
        text = self.font_small.render(continue_text, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 480))
        self.screen.blit(text, text_rect)
        
        back_text = "ESC 返回主選單"
        text = self.font_small.render(back_text, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 510))
        self.screen.blit(text, text_rect)
    
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
