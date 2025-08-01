import pygame
import math
import json
import os

# 初始化 Pygame
pygame.init()
pygame.mixer.init()

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
TOTAL_LEVELS = 12


class Player:
    def __init__(self, x, y, game=None):
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
        self.game = game  # 對遊戲實例的引用，用於播放音效

        # 跳躍力量循環系統
        self.jump_power_paused = False  # 是否處於暫停狀態
        self.jump_power_pause_timer = 0  # 暫停計時器
        self.jump_power_pause_duration = 30  # 暫停幀數（約0.5秒，假設60FPS）

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

        # 重置跳躍力量循環系統
        self.jump_power_paused = False
        self.jump_power_pause_timer = 0

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

        # 特殊處理第12關的無限生成機制
        if level_num == 12:
            # 當玩家達到很高的高度時，動態生成新的平台
            current_height = -self.y  # 轉換為正數高度
            if current_height > 2000:  # 超過2000像素高度
                # 觸發無限模式
                return "infinite_mode"

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
        # 重置暫停狀態
        self.jump_power_paused = False
        self.jump_power_pause_timer = 0

    def update_jump_charge(self):
        # 只要在蓄力就持續處理力量變化
        if self.jump_charging:
            if self.jump_power_paused:
                # 處於暫停狀態，計時器遞減
                self.jump_power_pause_timer -= 1
                if self.jump_power_pause_timer <= 0:
                    # 暫停結束，重新開始充能
                    self.jump_power_paused = False
                    self.jump_power = MIN_JUMP_POWER
            else:
                # 正常充能狀態
                self.jump_power += JUMP_CHARGE_RATE
                if self.jump_power >= MAX_JUMP_POWER:
                    # 達到最大值，進入暫停狀態
                    self.jump_power = MAX_JUMP_POWER
                    self.jump_power_paused = True
                    self.jump_power_pause_timer = self.jump_power_pause_duration

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

            # 播放跳躍音效
            if self.game:
                self.game.play_jump_sound()

            # 重置跳躍狀態
            self.jump_charging = False
            self.jump_power = 0
            self.on_ground = False
            # 重置暫停狀態
            self.jump_power_paused = False
            self.jump_power_pause_timer = 0
        else:
            # 即使無法跳躍也要重置蓄力狀態
            if self.jump_charging:
                self.jump_charging = False
                self.jump_power = 0
                # 重置暫停狀態
                self.jump_power_paused = False
                self.jump_power_pause_timer = 0

    def draw(self, screen, camera_y):
        # 繪製玩家
        player_color = BLUE
        if self.jump_charging:
            if self.jump_power_paused:
                # 暫停狀態：閃爍效果
                flash_intensity = int(self.jump_power_pause_timer / 3) % 2
                if flash_intensity:
                    player_color = (255, 100, 100)  # 紅色閃爍
                else:
                    player_color = (255, 200, 100)  # 橙色閃爍
            else:
                # 正常蓄力時顯示不同顏色
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
            bar_width = 40
            bar_height = 8
            bar_x = self.x - 5
            bar_y = self.y - camera_y - 15

            # 背景
            pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))

            if self.jump_power_paused:
                # 暫停狀態：顯示滿條並閃爍
                flash_intensity = int(self.jump_power_pause_timer / 3) % 2
                bar_color = (
                    (255, 255, 0) if flash_intensity else (255, 100, 0)
                )  # 黃色/橙色閃爍
                pygame.draw.rect(
                    screen, bar_color, (bar_x, bar_y, bar_width, bar_height)
                )
            else:
                # 正常蓄力狀態
                charge_ratio = (self.jump_power - MIN_JUMP_POWER) / (
                    MAX_JUMP_POWER - MIN_JUMP_POWER
                )
                pygame.draw.rect(
                    screen, RED, (bar_x, bar_y, bar_width * charge_ratio, bar_height)
                )


class LevelManager:
    def __init__(self):
        self.levels = self.create_all_levels()

    def generate_infinite_platforms_segment(self, base_y, segment_num):
        """為無限關卡生成一個階段的平台"""
        import random

        random.seed(segment_num)  # 使用段數作為種子，確保結果可重現

        platforms = []
        platform_spacing = 200  # 每個段落的高度間隔

        # 根據段數調整難度
        difficulty = min(segment_num, 10)  # 最大難度為10
        platform_size = max(8, 20 - difficulty)  # 平台大小隨難度減小
        platform_height = max(3, 8 - difficulty // 2)  # 平台高度隨難度減小

        # 每個段落生成6-8個平台
        num_platforms = random.randint(6, 8)

        for i in range(num_platforms):
            # 計算平台位置
            x = random.randint(50, 750)
            y = base_y + i * (platform_spacing // num_platforms)

            # 添加一些隨機偏移讓路線更有趣
            x_offset = random.randint(-50, 50)
            y_offset = random.randint(-20, 20)

            x = max(50, min(750, x + x_offset))
            y = y + y_offset

            platforms.append(
                {"x": x, "y": y, "width": platform_size, "height": platform_height}
            )

        return platforms

    def generate_infinite_death_zones_segment(self, base_y, segment_num):
        """為無限關卡生成一個階段的死亡區域"""
        import random

        random.seed(segment_num + 1000)  # 不同的種子避免和平台重疊

        death_zones = []

        # 根據段數調整陷阱密度
        difficulty = min(segment_num, 10)
        num_traps = difficulty + 2  # 陷阱數量隨難度增加

        for i in range(num_traps):
            # 隨機放置陷阱
            x = random.randint(100, 700)
            y = base_y + random.randint(-100, 100)
            width = random.randint(5, 15)
            height = random.randint(50, 150)

            death_zones.append({"x": x, "y": y, "width": width, "height": height})

        return death_zones

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

        # 第6關 - 進階挑戰（重新設計，更流暢的路徑）
        levels[6] = {
            "name": "進階挑戰",
            "platforms": [
                {"x": 0, "y": 550, "width": 80, "height": 30},  # 起始平台（更大）
                {"x": 120, "y": 500, "width": 60, "height": 20},  # 簡單開始跳躍
                {"x": 250, "y": 460, "width": 55, "height": 18},  # 中程跳躍
                {"x": 150, "y": 400, "width": 55, "height": 18},  # 回跳（技巧性）
                {"x": 320, "y": 350, "width": 50, "height": 15},  # 前進跳躍
                {"x": 480, "y": 300, "width": 50, "height": 15},  # 長距離跳躍
                {"x": 350, "y": 240, "width": 50, "height": 15},  # 精準回跳
                {"x": 520, "y": 180, "width": 45, "height": 15},  # 挑戰跳躍
                {
                    "x": 300,
                    "y": 120,
                    "width": 100,
                    "height": 25,
                },  # 目標平台（更大更容易落地）
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},  # 底部深淵
                # 重新設計的陷阱，更合理的位置
                {"x": 80, "y": 470, "width": 25, "height": 80},  # 第一個陷阱
                {"x": 200, "y": 420, "width": 25, "height": 80},  # 第二個陷阱
                {"x": 280, "y": 370, "width": 25, "height": 80},  # 第三個陷阱
                {"x": 420, "y": 260, "width": 25, "height": 80},  # 第四個陷阱
                {"x": 460, "y": 200, "width": 25, "height": 80},  # 第五個陷阱
            ],
            "goal_y": 120,
            "start_pos": (40, 520),
            "target_deaths": 35,  # 稍微降低死亡目標，提高可玩性
        }

        # 第7關 - 簡單練習（簡化版本）
        levels[7] = {
            "name": "簡單練習",
            "platforms": [
                {"x": 50, "y": 550, "width": 120, "height": 25},  # 起始平台（加大）
                # 簡化路線：只保留關鍵平台
                {"x": 250, "y": 480, "width": 90, "height": 20},  # 第一跳（大平台）
                {"x": 450, "y": 420, "width": 85, "height": 20},  # 第二跳
                {"x": 200, "y": 360, "width": 85, "height": 20},  # 回跳
                {"x": 400, "y": 300, "width": 80, "height": 20},  # 前進
                {"x": 150, "y": 240, "width": 80, "height": 20},  # 左側
                {"x": 350, "y": 180, "width": 80, "height": 20},  # 中央
                {"x": 500, "y": 120, "width": 75, "height": 20},  # 右側
                # 勝利平台：超大平台
                {"x": 250, "y": 60, "width": 200, "height": 30},  # 勝利平台（超大）
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},  # 底部深淵
                # 只保留3個簡單陷阱
                {"x": 380, "y": 350, "width": 8, "height": 100},  # 中間陷阱1
                {"x": 280, "y": 250, "width": 8, "height": 100},  # 中間陷阱2
                {"x": 450, "y": 150, "width": 8, "height": 100},  # 上層陷阱
                # 邊界保護
                {"x": 0, "y": -50, "width": 8, "height": 400},  # 左邊界
                {"x": 792, "y": -50, "width": 8, "height": 400},  # 右邊界
            ],
            "goal_y": 60,
            "start_pos": (100, 530),  # 起始位置調整
            "target_deaths": 8,  # 大幅降低死亡目標
        }

        # 第8關 - 輕鬆練習（超簡化版本）
        levels[8] = {
            "name": "輕鬆練習",
            "platforms": [
                {"x": 0, "y": 550, "width": 120, "height": 30},  # 起始平台（超大）
                {"x": 200, "y": 480, "width": 100, "height": 25},  # 第一跳（超大）
                {"x": 400, "y": 420, "width": 90, "height": 25},  # 第二跳（大平台）
                {"x": 250, "y": 360, "width": 90, "height": 25},  # 回跳（大平台）
                {"x": 450, "y": 300, "width": 85, "height": 25},  # 前進
                {"x": 200, "y": 240, "width": 85, "height": 25},  # 左側
                {"x": 400, "y": 180, "width": 80, "height": 25},  # 右側
                # 勝利平台：超級大平台
                {"x": 250, "y": 120, "width": 200, "height": 35},  # 勝利平台（超大）
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},  # 底部深淵
                # 只保留2個很小的陷阱
                {"x": 350, "y": 350, "width": 6, "height": 80},  # 小陷阱1
                {"x": 320, "y": 220, "width": 6, "height": 80},  # 小陷阱2
                # 邊界保護
                {"x": 0, "y": -50, "width": 8, "height": 300},  # 左邊界
                {"x": 792, "y": -50, "width": 8, "height": 300},  # 右邊界
            ],
            "goal_y": 120,
            "start_pos": (50, 520),
            "target_deaths": 5,  # 超低死亡目標
        }

        # 第9關 - 螺旋迷宮（物理驗證挑戰版本）
        levels[9] = {
            "name": "螺旋迷宮",
            "platforms": [
                # 起始平台
                {"x": 0, "y": 550, "width": 50, "height": 25},
                # 第一層螺旋 - 外圈（安全距離）
                {"x": 200, "y": 480, "width": 25, "height": 12},  # 跳躍距離: 208px
                {"x": 380, "y": 420, "width": 25, "height": 12},  # 跳躍距離: 188px
                {"x": 550, "y": 360, "width": 25, "height": 12},  # 跳躍距離: 178px
                {"x": 700, "y": 300, "width": 25, "height": 12},  # 跳躍距離: 158px
                {"x": 600, "y": 240, "width": 25, "height": 12},  # 回跳距離: 112px
                # 第二層螺旋 - 中圈（增加挑戰）
                {"x": 450, "y": 180, "width": 22, "height": 10},  # 跳躍距離: 158px
                {"x": 280, "y": 120, "width": 22, "height": 10},  # 跳躍距離: 178px
                {"x": 120, "y": 60, "width": 22, "height": 10},  # 跳躍距離: 168px
                {"x": 300, "y": 0, "width": 22, "height": 10},  # 跳躍距離: 188px
                # 第三層螺旋 - 內圈（最終挑戰）
                {"x": 500, "y": -60, "width": 20, "height": 8},  # 跳躍距離: 208px
                {"x": 680, "y": -120, "width": 20, "height": 8},  # 跳躍距離: 188px
                {"x": 520, "y": -180, "width": 20, "height": 8},  # 跳躍距離: 168px
                {"x": 340, "y": -240, "width": 20, "height": 8},  # 跳躍距離: 188px
                # 最終目標
                {"x": 450, "y": -300, "width": 60, "height": 20},  # 跳躍距離: 128px
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},
                # 第一層螺旋陷阱
                {"x": 100, "y": 450, "width": 15, "height": 200},  # 外圈陷阱1
                {"x": 290, "y": 390, "width": 15, "height": 200},  # 外圈陷阱2
                {"x": 465, "y": 330, "width": 15, "height": 200},  # 外圈陷阱3
                {"x": 625, "y": 270, "width": 15, "height": 200},  # 邊界陷阱
                {"x": 525, "y": 210, "width": 15, "height": 200},  # 回程陷阱
                # 第二層螺旋陷阱
                {"x": 365, "y": 150, "width": 14, "height": 250},  # 中圈陷阱1
                {"x": 200, "y": 90, "width": 14, "height": 250},  # 中圈陷阱2
                {"x": 50, "y": 30, "width": 14, "height": 250},  # 中圈陷阱3
                {"x": 220, "y": -30, "width": 14, "height": 250},  # 穿越陷阱
                # 第三層螺旋陷阱
                {"x": 400, "y": -90, "width": 13, "height": 300},  # 內圈陷阱1
                {"x": 600, "y": -150, "width": 13, "height": 300},  # 內圈陷阱2
                {"x": 430, "y": -210, "width": 13, "height": 300},  # 內圈陷阱3
                {"x": 260, "y": -270, "width": 13, "height": 300},  # 最終陷阱
                # 邊界死亡牆
                {"x": 0, "y": -100, "width": 20, "height": 500},  # 左邊界
                {"x": 780, "y": -100, "width": 20, "height": 500},  # 右邊界
            ],
            "goal_y": -300,
            "start_pos": (25, 525),
            "target_deaths": 80,  # 有挑戰性但合理
        }

        # 第10關 - 終極挑戰（物理驗證困難版本）
        levels[10] = {
            "name": "終極挑戰",
            "platforms": [
                # 起始平台
                {"x": 0, "y": 550, "width": 45, "height": 20},
                # 第一階段 - 精密跳躍挑戰
                {"x": 220, "y": 480, "width": 18, "height": 8},  # 跳躍距離: 228px
                {"x": 420, "y": 420, "width": 18, "height": 8},  # 跳躍距離: 208px
                {"x": 600, "y": 360, "width": 18, "height": 8},  # 跳躍距離: 188px
                {"x": 750, "y": 300, "width": 18, "height": 8},  # 跳躍距離: 158px
                {"x": 600, "y": 240, "width": 18, "height": 8},  # 回跳距離: 158px
                # 第二階段 - 高空精密操作
                {"x": 400, "y": 180, "width": 16, "height": 6},  # 跳躍距離: 208px
                {"x": 200, "y": 120, "width": 16, "height": 6},  # 跳躍距離: 208px
                {"x": 50, "y": 60, "width": 16, "height": 6},  # 跳躍距離: 158px
                {"x": 300, "y": 0, "width": 16, "height": 6},  # 跳躍距離: 258px
                # 第三階段 - 超高空極限
                {"x": 550, "y": -60, "width": 14, "height": 5},  # 跳躍距離: 258px
                {"x": 750, "y": -120, "width": 14, "height": 5},  # 跳躍距離: 208px
                {"x": 600, "y": -180, "width": 14, "height": 5},  # 跳躍距離: 158px
                {"x": 400, "y": -240, "width": 14, "height": 5},  # 跳躍距離: 208px
                {"x": 150, "y": -300, "width": 14, "height": 5},  # 跳躍距離: 258px
                # 第四階段 - 終極精準
                {"x": 450, "y": -360, "width": 12, "height": 4},  # 跳躍距離: 308px
                {"x": 700, "y": -420, "width": 12, "height": 4},  # 跳躍距離: 258px
                {"x": 500, "y": -480, "width": 12, "height": 4},  # 跳躍距離: 208px
                {"x": 250, "y": -540, "width": 12, "height": 4},  # 跳躍距離: 258px
                # 最終目標平台
                {"x": 400, "y": -600, "width": 60, "height": 20},  # 跳躍距離: 178px
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},
                # 第一階段陷阱
                {"x": 110, "y": 450, "width": 12, "height": 200},  # 陷阱1
                {"x": 320, "y": 390, "width": 12, "height": 200},  # 陷阱2
                {"x": 510, "y": 330, "width": 12, "height": 200},  # 陷阱3
                {"x": 675, "y": 270, "width": 12, "height": 200},  # 邊界陷阱
                {"x": 525, "y": 210, "width": 12, "height": 200},  # 回程陷阱
                # 第二階段陷阱
                {"x": 300, "y": 150, "width": 11, "height": 250},  # 高空陷阱1
                {"x": 125, "y": 90, "width": 11, "height": 250},  # 高空陷阱2
                {"x": 25, "y": 30, "width": 11, "height": 250},  # 邊界陷阱
                {"x": 175, "y": -30, "width": 11, "height": 250},  # 穿越陷阱
                # 第三階段陷阱
                {"x": 425, "y": -90, "width": 10, "height": 300},  # 超高空陷阱1
                {"x": 675, "y": -150, "width": 10, "height": 300},  # 超高空陷阱2
                {"x": 525, "y": -210, "width": 10, "height": 300},  # 超高空陷阱3
                {"x": 275, "y": -270, "width": 10, "height": 300},  # 超高空陷阱4
                {"x": 75, "y": -330, "width": 10, "height": 300},  # 邊界超高空陷阱
                # 第四階段陷阱
                {"x": 325, "y": -390, "width": 9, "height": 350},  # 終極陷阱1
                {"x": 575, "y": -450, "width": 9, "height": 350},  # 終極陷阱2
                {"x": 375, "y": -510, "width": 9, "height": 350},  # 終極陷阱3
                {"x": 125, "y": -570, "width": 9, "height": 350},  # 最終陷阱
                # 邊界死亡牆
                {"x": 0, "y": -300, "width": 15, "height": 800},  # 左邊界
                {"x": 785, "y": -300, "width": 15, "height": 800},  # 右邊界
                # 天花板
                {"x": 0, "y": -650, "width": 1200, "height": 40},  # 天花板死亡區
            ],
            "goal_y": -600,
            "start_pos": (22, 530),
            "target_deaths": 120,  # 很有挑戰性但可達成
        }

        # 第11關 - 天堂之塔（物理驗證終極挑戰，無岩漿）
        levels[11] = {
            "name": "天堂之塔",
            "platforms": [
                # 起始平台
                {"x": 0, "y": 550, "width": 40, "height": 15},
                # 第一階段 - 基礎攀爬（高度：550 → 200）
                {"x": 240, "y": 480, "width": 15, "height": 6},  # 跳躍距離: 248px
                {"x": 480, "y": 420, "width": 15, "height": 6},  # 跳躍距離: 248px
                {"x": 700, "y": 360, "width": 15, "height": 6},  # 跳躍距離: 228px
                {"x": 550, "y": 300, "width": 15, "height": 6},  # 回跳距離: 158px
                {"x": 350, "y": 240, "width": 15, "height": 6},  # 跳躍距離: 208px
                {"x": 150, "y": 180, "width": 15, "height": 6},  # 跳躍距離: 208px
                {"x": 400, "y": 120, "width": 15, "height": 6},  # 跳躍距離: 258px
                {"x": 650, "y": 60, "width": 15, "height": 6},  # 跳躍距離: 258px
                {"x": 500, "y": 0, "width": 15, "height": 6},  # 跳躍距離: 158px
                # 第二階段 - 雲端區域（高度：0 → -350）
                {"x": 250, "y": -60, "width": 12, "height": 5},  # 跳躍距離: 258px
                {"x": 50, "y": -120, "width": 12, "height": 5},  # 跳躍距離: 208px
                {"x": 350, "y": -180, "width": 12, "height": 5},  # 跳躍距離: 308px
                {"x": 600, "y": -240, "width": 12, "height": 5},  # 跳躍距離: 258px
                {"x": 400, "y": -300, "width": 12, "height": 5},  # 跳躍距離: 208px
                {"x": 150, "y": -360, "width": 12, "height": 5},  # 跳躍距離: 258px
                # 第三階段 - 天空殿堂（高度：-360 → -710）
                {"x": 450, "y": -420, "width": 10, "height": 4},  # 跳躍距離: 308px
                {"x": 700, "y": -480, "width": 10, "height": 4},  # 跳躍距離: 258px
                {"x": 500, "y": -540, "width": 10, "height": 4},  # 跳躍距離: 208px
                {"x": 250, "y": -600, "width": 10, "height": 4},  # 跳躍距離: 258px
                {"x": 550, "y": -660, "width": 10, "height": 4},  # 跳躍距離: 308px
                {"x": 750, "y": -720, "width": 10, "height": 4},  # 跳躍距離: 208px
                # 第四階段 - 星辰領域（高度：-720 → -1070）
                {"x": 550, "y": -780, "width": 8, "height": 3},  # 跳躍距離: 208px
                {"x": 300, "y": -840, "width": 8, "height": 3},  # 跳躍距離: 258px
                {"x": 100, "y": -900, "width": 8, "height": 3},  # 跳躍距離: 208px
                {"x": 400, "y": -960, "width": 8, "height": 3},  # 跳躍距離: 308px
                {"x": 650, "y": -1020, "width": 8, "height": 3},  # 跳躍距離: 258px
                {"x": 450, "y": -1080, "width": 8, "height": 3},  # 跳躍距離: 208px
                # 第五階段 - 天堂之門（高度：-1080 → -1200）
                {"x": 200, "y": -1140, "width": 6, "height": 3},  # 跳躍距離: 258px
                {"x": 500, "y": -1200, "width": 6, "height": 3},  # 跳躍距離: 308px
                # 最終目標 - 天堂頂峰
                {"x": 350, "y": -1260, "width": 80, "height": 20},  # 跳躍距離: 178px
            ],
            "death_zones": [
                # 普通地板死亡區域（不是岩漿）
                {"x": 0, "y": 600, "width": 1200, "height": 100},  # 底部深淵
                # 第一階段陷阱 - 雲霧陷阱
                {"x": 120, "y": 450, "width": 8, "height": 200},  # 雲霧陷阱1
                {"x": 360, "y": 390, "width": 8, "height": 200},  # 雲霧陷阱2
                {"x": 590, "y": 330, "width": 8, "height": 200},  # 雲霧陷阱3
                {"x": 450, "y": 270, "width": 8, "height": 200},  # 回程雲霧陷阱
                {"x": 250, "y": 210, "width": 8, "height": 200},  # 雲霧陷阱4
                {"x": 50, "y": 150, "width": 8, "height": 200},  # 邊界雲霧陷阱
                {"x": 275, "y": 90, "width": 8, "height": 200},  # 雲霧陷阱5
                {"x": 525, "y": 30, "width": 8, "height": 200},  # 雲霧陷阱6
                # 第二階段陷阱 - 風暴陷阱
                {"x": 150, "y": -30, "width": 7, "height": 250},  # 風暴陷阱1
                {"x": 25, "y": -90, "width": 7, "height": 250},  # 邊界風暴陷阱
                {"x": 225, "y": -150, "width": 7, "height": 250},  # 風暴陷阱2
                {"x": 475, "y": -210, "width": 7, "height": 250},  # 風暴陷阱3
                {"x": 325, "y": -270, "width": 7, "height": 250},  # 風暴陷阱4
                {"x": 75, "y": -330, "width": 7, "height": 250},  # 風暴陷阱5
                # 第三階段陷阱 - 雷電陷阱
                {"x": 325, "y": -390, "width": 6, "height": 300},  # 雷電陷阱1
                {"x": 575, "y": -450, "width": 6, "height": 300},  # 雷電陷阱2
                {"x": 375, "y": -510, "width": 6, "height": 300},  # 雷電陷阱3
                {"x": 125, "y": -570, "width": 6, "height": 300},  # 雷電陷阱4
                {"x": 425, "y": -630, "width": 6, "height": 300},  # 雷電陷阱5
                {"x": 625, "y": -690, "width": 6, "height": 300},  # 雷電陷阱6
                # 第四階段陷阱 - 虛空陷阱
                {"x": 425, "y": -750, "width": 5, "height": 350},  # 虛空陷阱1
                {"x": 200, "y": -810, "width": 5, "height": 350},  # 虛空陷阱2
                {"x": 50, "y": -870, "width": 5, "height": 350},  # 虛空陷阱3
                {"x": 275, "y": -930, "width": 5, "height": 350},  # 虛空陷阱4
                {"x": 525, "y": -990, "width": 5, "height": 350},  # 虛空陷阱5
                {"x": 375, "y": -1050, "width": 5, "height": 350},  # 虛空陷阱6
                # 第五階段陷阱 - 天堂審判陷阱
                {"x": 100, "y": -1110, "width": 4, "height": 400},  # 審判陷阱1
                {"x": 350, "y": -1170, "width": 4, "height": 400},  # 審判陷阱2
                {"x": 250, "y": -1230, "width": 4, "height": 400},  # 最終審判陷阱
                # 邊界死亡牆 - 高塔邊界
                {"x": 0, "y": -600, "width": 15, "height": 800},  # 左邊界虛空牆
                {"x": 785, "y": -600, "width": 15, "height": 800},  # 右邊界虛空牆
                # 天空屏障
                {"x": 0, "y": -1320, "width": 1200, "height": 50},  # 天空屏障
            ],
            "goal_y": -1260,  # 極高的目標高度，相當於21層樓
            "start_pos": (20, 535),
            "target_deaths": 200,  # 超級高死亡目標，真正的終極挑戰
        }

        # 第12關 - 無限之塔（真正的無限高度挑戰）
        levels[12] = {
            "name": "無限之塔",
            "platforms": [
                # 起始平台
                {"x": 0, "y": 550, "width": 60, "height": 20},
                # 第一段階梯 - 每隔200高度生成一組平台
                *self.generate_infinite_platforms_segment(-200, 1),
                *self.generate_infinite_platforms_segment(-400, 2),
                *self.generate_infinite_platforms_segment(-600, 3),
                *self.generate_infinite_platforms_segment(-800, 4),
                *self.generate_infinite_platforms_segment(-1000, 5),
                *self.generate_infinite_platforms_segment(-1200, 6),
                *self.generate_infinite_platforms_segment(-1400, 7),
                *self.generate_infinite_platforms_segment(-1600, 8),
                *self.generate_infinite_platforms_segment(-1800, 9),
                *self.generate_infinite_platforms_segment(-2000, 10),
                # 理論上可以繼續無限延伸...
                # 終極目標平台（如果真的有人能到達）
                {"x": 350, "y": -2200, "width": 150, "height": 40},  # 神級目標
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},  # 底部深淵
                # 為每個階段生成相應的陷阱
                *self.generate_infinite_death_zones_segment(-200, 1),
                *self.generate_infinite_death_zones_segment(-400, 2),
                *self.generate_infinite_death_zones_segment(-600, 3),
                *self.generate_infinite_death_zones_segment(-800, 4),
                *self.generate_infinite_death_zones_segment(-1000, 5),
                *self.generate_infinite_death_zones_segment(-1200, 6),
                *self.generate_infinite_death_zones_segment(-1400, 7),
                *self.generate_infinite_death_zones_segment(-1600, 8),
                *self.generate_infinite_death_zones_segment(-1800, 9),
                *self.generate_infinite_death_zones_segment(-2000, 10),
                # 邊界死亡牆
                {"x": 0, "y": -1500, "width": 15, "height": 2000},  # 左邊界
                {"x": 785, "y": -1500, "width": 15, "height": 2000},  # 右邊界
            ],
            "goal_y": -2200,  # 超高目標，但理論上可以更高
            "start_pos": (30, 530),
            "target_deaths": 500,  # 史詩級死亡目標
            "infinite": True,  # 標記為無限關卡
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

        # 情緒價值系統
        self.encouragement_messages = []
        self.encouragement_timer = 0
        self.congratulation_messages = []
        self.congratulation_timer = 0
        self.mega_celebration = False
        self.mega_celebration_timer = 0

        # 載入字體
        self.load_fonts()

        # 音效系統
        self.sound_enabled = True
        self.sound_volume = 0.7
        self.load_sounds()

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

    def load_sounds(self):
        """載入音效"""
        try:
            # 載入跳躍音效
            sound_path = os.path.join(os.path.dirname(__file__), "sound", "jump.mp3")
            if os.path.exists(sound_path):
                self.jump_sound = pygame.mixer.Sound(sound_path)
                self.jump_sound.set_volume(self.sound_volume)
                print(f"成功載入跳躍音效: {sound_path}")
            else:
                print(f"找不到音效文件: {sound_path}")
                self.jump_sound = None

            # 載入通關音效
            victory_sound_path = os.path.join(
                os.path.dirname(__file__), "sound", "golfclap.mp3"
            )
            if os.path.exists(victory_sound_path):
                self.victory_sound = pygame.mixer.Sound(victory_sound_path)
                self.victory_sound.set_volume(self.sound_volume)
                print(f"成功載入通關音效: {victory_sound_path}")
            else:
                print(f"找不到音效文件: {victory_sound_path}")
                self.victory_sound = None

            # 載入失敗音效
            gameover_sound_paths = [
                os.path.join(os.path.dirname(__file__), "sound", "gameover.mp3"),
                os.path.join(os.path.dirname(__file__), "sound", "gameover.wav"),
            ]

            self.gameover_sound = None
            for path in gameover_sound_paths:
                if os.path.exists(path):
                    self.gameover_sound = pygame.mixer.Sound(path)
                    self.gameover_sound.set_volume(self.sound_volume)
                    print(f"成功載入失敗音效: {path}")
                    break

            if not self.gameover_sound:
                print("找不到失敗音效文件 (gameover.mp3 或 gameover.wav)")
                self.gameover_sound = None

            # 載入 Yee 失敗音效
            yee_sound_path = os.path.join(os.path.dirname(__file__), "sound", "yee.mp3")
            if os.path.exists(yee_sound_path):
                self.yee_sound = pygame.mixer.Sound(yee_sound_path)
                self.yee_sound.set_volume(self.sound_volume)
                print(f"成功載入 Yee 失敗音效: {yee_sound_path}")
            else:
                print(f"找不到音效文件: {yee_sound_path}")
                self.yee_sound = None

            # 載入背景音樂
            self.load_background_music()

        except Exception as e:
            print(f"載入音效失敗: {e}")
            self.jump_sound = None
            self.victory_sound = None
            self.gameover_sound = None
            self.yee_sound = None

    def load_background_music(self):
        """載入背景音樂"""
        try:
            # 支援多種音樂格式
            music_paths = [
                os.path.join(os.path.dirname(__file__), "sound", "background.mp3"),
                os.path.join(os.path.dirname(__file__), "sound", "background.wav"),
                os.path.join(os.path.dirname(__file__), "sound", "background.ogg"),
                os.path.join(os.path.dirname(__file__), "sound", "bgm.mp3"),
                os.path.join(os.path.dirname(__file__), "sound", "bgm.wav"),
                os.path.join(os.path.dirname(__file__), "sound", "music.mp3"),
            ]

            self.background_music_loaded = False
            for music_path in music_paths:
                if os.path.exists(music_path):
                    try:
                        pygame.mixer.music.load(music_path)
                        self.background_music_loaded = True
                        self.background_music_path = music_path
                        print(f"成功載入背景音樂: {music_path}")
                        break
                    except Exception as e:
                        print(f"載入背景音樂失敗 {music_path}: {e}")
                        continue

            if not self.background_music_loaded:
                print(
                    "找不到背景音樂文件 (支援格式: background.mp3/wav/ogg, bgm.mp3/wav, music.mp3)"
                )

        except Exception as e:
            print(f"背景音樂系統初始化失敗: {e}")
            self.background_music_loaded = False

    def play_jump_sound(self):
        """播放跳躍音效"""
        if self.sound_enabled and self.jump_sound:
            try:
                self.jump_sound.play()
            except Exception as e:
                print(f"播放音效失敗: {e}")

    def play_victory_sound(self):
        """播放通關音效"""
        if self.sound_enabled and self.victory_sound:
            try:
                self.victory_sound.play()
            except Exception as e:
                print(f"播放通關音效失敗: {e}")

    def play_gameover_sound(self):
        """播放失敗音效"""
        if self.sound_enabled:
            # 播放一般失敗音效
            if self.gameover_sound:
                try:
                    self.gameover_sound.play()
                    print("🔊 播放失敗音效")
                except Exception as e:
                    print(f"播放失敗音效失敗: {e}")

            # 使用 pygame 線程來延遲播放 Yee 音效
            if self.yee_sound:
                try:
                    # 設定定時器，0.5秒後觸發 Yee 音效
                    pygame.time.set_timer(pygame.USEREVENT + 1, 500)  # 500ms 後播放
                    print("⏰ 已設定 Yee 音效延遲播放 (0.5秒)")
                except Exception as e:
                    print(f"設定 Yee 音效定時器失敗: {e}")

    def play_yee_sound(self):
        """播放 Yee 音效"""
        if self.sound_enabled and self.yee_sound:
            try:
                self.yee_sound.play()
                print("🎵 播放 Yee 音效")
            except Exception as e:
                print(f"播放 Yee 音效失敗: {e}")

    def start_background_music(self):
        """開始播放背景音樂"""
        if self.sound_enabled and self.background_music_loaded:
            try:
                pygame.mixer.music.play(-1)  # -1 表示無限循環
                pygame.mixer.music.set_volume(
                    self.sound_volume * 0.6
                )  # 背景音樂音量稍低
                print("🎵 開始播放背景音樂")
            except Exception as e:
                print(f"播放背景音樂失敗: {e}")

    def stop_background_music(self):
        """停止背景音樂"""
        try:
            pygame.mixer.music.stop()
            print("⏹️  停止背景音樂")
        except Exception as e:
            print(f"停止背景音樂失敗: {e}")

    def pause_background_music(self):
        """暫停背景音樂"""
        try:
            pygame.mixer.music.pause()
            print("⏸️  暫停背景音樂")
        except Exception as e:
            print(f"暫停背景音樂失敗: {e}")

    def resume_background_music(self):
        """恢復背景音樂"""
        try:
            pygame.mixer.music.unpause()
            print("▶️  恢復背景音樂")
        except Exception as e:
            print(f"恢復背景音樂失敗: {e}")

    def set_background_music_volume(self, volume):
        """設置背景音樂音量"""
        try:
            pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
        except Exception as e:
            print(f"設置背景音樂音量失敗: {e}")

    def toggle_sound(self):
        """切換音效開關"""
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            print("音效已開啟")
            # 如果在遊戲中且有背景音樂，重新開始播放
            if (
                hasattr(self, "state")
                and self.state == 2
                and self.background_music_loaded
            ):  # 2 = PLAYING
                self.start_background_music()
        else:
            print("音效已關閉")
            # 停止背景音樂
            self.stop_background_music()

    def set_sound_volume(self, volume):
        """設置音效音量（0.0-1.0）"""
        self.sound_volume = max(0.0, min(1.0, volume))
        if self.jump_sound:
            self.jump_sound.set_volume(self.sound_volume)
        if self.victory_sound:
            self.victory_sound.set_volume(self.sound_volume)
        if self.gameover_sound:
            self.gameover_sound.set_volume(self.sound_volume)
        if self.yee_sound:
            self.yee_sound.set_volume(self.sound_volume)
        # 更新背景音樂音量
        if self.background_music_loaded:
            self.set_background_music_volume(self.sound_volume * 0.6)
        print(f"音效音量設置為: {self.sound_volume:.1f}")

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
        self.player = Player(start_x, start_y, self)  # 傳遞遊戲實例

        # 確保玩家正確地站在起始平台上
        self.player.on_ground = True
        self.player.vel_x = 0
        self.player.vel_y = 0

        self.camera_y = 0
        self.state = PLAYING

        # 開始播放背景音樂
        self.start_background_music()

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

        # 播放通關音效
        self.play_victory_sound()

        # 解鎖下一關
        if self.current_level < TOTAL_LEVELS:
            self.unlocked_levels = max(self.unlocked_levels, self.current_level + 1)

        # 觸發情緒價值系統
        self.trigger_level_completion_celebration()

        self.save_progress()
        self.state = VICTORY

    def game_over(self):
        """遊戲失敗"""
        print(f"遊戲失敗！第{self.current_level}關超過目標死亡次數")
        self.state = GAME_OVER
        self.stop_background_music()  # 停止背景音樂
        self.play_gameover_sound()

    def restart_current_level(self):
        """重新開始當前關卡"""
        if hasattr(self, "current_level"):
            # 重新開始當前關卡，重置死亡次數
            self.start_level(self.current_level)
            # 重置死亡次數統計（給玩家新的機會）
            if self.player:
                self.player.death_count = 0
            print(f"重新開始第{self.current_level}關")
        else:
            # 如果沒有當前關卡，返回關卡選擇
            self.state = LEVEL_SELECT

    def trigger_level_completion_celebration(self):
        """觸發關卡完成慶祝"""
        level_data = self.level_manager.get_level(self.current_level)
        deaths = self.player.death_count
        target = level_data["target_deaths"]

        # 普通完成關卡的情緒價值
        if deaths <= target:
            # 在目標內完成
            self.congratulation_messages = [
                "🎉 太棒了！你在目標內完成了！",
                "💪 你的技巧正在進步！",
                "⭐ 完美的控制力！",
                "🔥 繼續保持這個節奏！",
            ]
        else:
            # 超過目標但仍完成
            self.congratulation_messages = [
                "🎊 恭喜完成關卡！",
                "💯 永不放棄的精神！",
                "🌟 堅持就是勝利！",
                "👏 你做到了！",
            ]

        # 特殊關卡的額外慶祝
        if self.current_level == 11:
            # 第11關天堂之塔
            self.congratulation_messages.extend(
                ["👑 天堂之塔征服者！", "🚀 你已超越了極限！", "🏆 真正的跳躍大師！"]
            )
        elif self.current_level == 12:
            # 第12關無限之塔 - 超大情緒價值
            self.mega_celebration = True
            self.mega_celebration_timer = 600  # 10秒的超級慶祝
            self.congratulation_messages = [
                "🎆🎆🎆 史詩級成就解鎖！🎆🎆🎆",
                "👑👑👑 無限之塔征服者！👑👑👑",
                "🏆🏆🏆 跳躍之神誕生！🏆🏆🏆",
                "🌟🌟🌟 傳說級玩家！🌟🌟🌟",
                "🚀🚀🚀 你打破了物理定律！🚀🚀🚀",
                "💎💎💎 絕對的完美！💎💎💎",
                "🔥🔥🔥 燃燒吧！跳躍魂！🔥🔥🔥",
            ]

        # 所有關卡完成的終極慶祝
        if self.current_level == TOTAL_LEVELS:
            self.mega_celebration = True
            self.mega_celebration_timer = 900  # 15秒的終極慶祝
            self.congratulation_messages.extend(
                [
                    "🎖️🎖️🎖️ 全關卡制霸！🎖️🎖️🎖️",
                    "👑 你就是跳躍之王！👑",
                    "🌈 傳奇之路完成！🌈",
                    "💫 你創造了奇蹟！💫",
                ]
            )

        self.congratulation_timer = 300  # 5秒顯示

    def add_encouragement_message(self):
        """添加鼓勵訊息（死亡時）"""
        encouragement_pool = [
            "💪 不要放棄！你可以的！",
            "🌟 每次失敗都是學習！",
            "🔥 堅持下去，勝利在前方！",
            "⚡ 再試一次，你會更強！",
            "💯 失敗是成功之母！",
            "🚀 向著目標前進！",
            "⭐ 相信自己的能力！",
            "🎯 專注，你能做到的！",
            "💎 每一次跳躍都在進步！",
            "🏆 冠軍從不輕易放棄！",
        ]

        import random

        message = random.choice(encouragement_pool)
        self.encouragement_messages.append(message)
        self.encouragement_timer = 180  # 3秒顯示

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
            elif event.type == pygame.USEREVENT + 1:
                # 定時器事件：播放 Yee 音效
                self.play_yee_sound()
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # 停止定時器
            elif event.type == pygame.KEYDOWN:
                # 全域按鍵處理
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                elif event.key == pygame.K_m:
                    # M 鍵切換音效
                    self.toggle_sound()
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    # 減號鍵降低音量
                    self.set_sound_volume(self.sound_volume - 0.1)
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                    # 等號/加號鍵提高音量
                    self.set_sound_volume(self.sound_volume + 0.1)
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
                    elif self.state == VICTORY:
                        if event.key == pygame.K_RETURN:
                            self.state = LEVEL_SELECT
                        elif event.key == pygame.K_ESCAPE:
                            self.state = MENU
                    elif self.state == GAME_OVER:
                        if event.key == pygame.K_RETURN:
                            # 重新開始當前關卡
                            self.restart_current_level()
                        elif event.key == pygame.K_ESCAPE:
                            self.state = MENU
                        elif event.key == pygame.K_SPACE:
                            # 重新開始當前關卡
                            self.restart_current_level()
            else:
                if self.state == MENU:
                    self.handle_menu_events(event)
                elif self.state == LEVEL_SELECT:
                    self.handle_level_select_events(event)
                elif self.state == PLAYING:
                    self.handle_playing_events(event)
                elif self.state == VICTORY:
                    pass  # VICTORY 狀態的其他事件類型不需要處理
                elif self.state == GAME_OVER:
                    pass  # GAME_OVER 狀態的其他事件類型不需要處理

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
            # 添加鼓勵訊息
            self.add_encouragement_message()
            self.save_progress()

            # 檢查是否超過目標死亡次數
            if self.player.death_count > level_data["target_deaths"]:
                self.game_over()
                return

        elif result == "fall_trap":
            # 掉落陷阱的特殊處理 - 不重置但記錄
            self.level_stats[str(self.current_level)][
                "deaths"
            ] = self.player.death_count
            # 添加鼓勵訊息
            self.add_encouragement_message()
            self.save_progress()

            # 檢查是否超過目標死亡次數
            if self.player.death_count > level_data["target_deaths"]:
                self.game_over()
                return

        elif result == "infinite_mode":
            # 第12關無限模式觸發
            self.handle_infinite_mode()

        # 更新相機
        self.update_camera()

        # 檢查是否完成關卡（必須踩在目標平台上）
        if self.check_goal_completion(level_data):
            self.complete_level()

    def handle_infinite_mode(self):
        """處理第12關的無限模式"""
        if self.current_level != 12:
            return

        current_height = -self.player.y
        # 每達到新的500像素高度里程碑，添加鼓勵訊息
        milestone = int(current_height // 500) * 500

        if milestone > 2000 and milestone % 500 == 0:
            infinite_messages = [
                f"🚀 突破{milestone}米高度！",
                "🌟 你正在創造奇蹟！",
                "💫 繼續攀登，勇士！",
                "⚡ 無限的力量！",
                "🔥 燃燒吧！跳躍魂！",
            ]
            import random

            message = random.choice(infinite_messages)
            self.encouragement_messages.append(message)
            self.encouragement_timer = 240  # 4秒顯示

    def update_camera(self):
        """更新相機位置"""
        if self.player:
            target_y = self.player.y - SCREEN_HEIGHT // 2
            self.camera_y += (target_y - self.camera_y) * 0.1

    def update(self):
        """更新遊戲邏輯"""
        if self.state == PLAYING:
            self.update_playing()

        # 更新情緒價值系統計時器
        if self.encouragement_timer > 0:
            self.encouragement_timer -= 1
            if self.encouragement_timer <= 0:
                self.encouragement_messages.clear()

        if self.congratulation_timer > 0:
            self.congratulation_timer -= 1
            if self.congratulation_timer <= 0:
                self.congratulation_messages.clear()

        if self.mega_celebration_timer > 0:
            self.mega_celebration_timer -= 1
            if self.mega_celebration_timer <= 0:
                self.mega_celebration = False

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
        controls = ["↑↓ 選擇", "Enter 確認", "M 切換音效", "ESC 退出", "F11 切換全屏"]
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
        cols = 6  # 改為6列以容納12關
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
            elif level == 12:
                # 第12關無限之塔特殊顯示
                if (
                    str(level) in self.level_stats
                    and self.level_stats[str(level)]["completed"]
                ):
                    color = (255, 215, 0)  # 完成的第12關用金色
                    text_color = BLACK
                    deaths = self.level_stats[str(level)]["best_deaths"]
                    status = f"神級\n{deaths}死"
                else:
                    color = (184, 134, 11)  # 未完成的第12關用深金色
                    text_color = WHITE
                    deaths = self.level_stats.get(str(level), {}).get("deaths", 0)
                    status = f"無限\n{deaths}死"
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

                # 第12關特殊說明
                if self.level_select_selection == 12:
                    warning_text = "🚀 無限之塔：挑戰你的極限！"
                    warning = self.font_small.render(warning_text, True, (255, 215, 0))
                    warning_x, warning_y = self.scale_pos(
                        SCREEN_WIDTH // 2, detail_y + 55
                    )
                    warning_rect = warning.get_rect(center=(warning_x, warning_y))
                    self.screen.blit(warning, warning_rect)

                    warning_text2 = "理論上可以無限攀爬..."
                    warning2 = self.font_small.render(warning_text2, True, PURPLE)
                    warning2_x, warning2_y = self.scale_pos(
                        SCREEN_WIDTH // 2, detail_y + 75
                    )
                    warning2_rect = warning2.get_rect(center=(warning2_x, warning2_y))
                    self.screen.blit(warning2, warning2_rect)

        # 操作說明
        controls = [
            "← → 選擇關卡",
            "Enter 開始",
            "M 切換音效",
            "ESC 返回",
            "F11 切換全屏",
        ]
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

        # 繪製情緒價值訊息
        self.draw_emotional_messages(screen)

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
            "M 切換音效",
            "+ - 調整音量",
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

        # 音效狀態
        sound_status = "開啟" if self.sound_enabled else "關閉"
        sound_text = f"音效: {sound_status} ({int(self.sound_volume * 100)}%)"
        text = self.font_small.render(sound_text, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - 150, 85))

    def draw_emotional_messages(self, screen):
        """繪製情緒價值訊息"""
        import math

        # 繪製鼓勵訊息（死亡時）
        if self.encouragement_messages and self.encouragement_timer > 0:
            y_offset = 250
            for i, message in enumerate(
                self.encouragement_messages[-3:]
            ):  # 最多顯示3條
                # 淡入淡出效果
                alpha = min(255, int(255 * (self.encouragement_timer / 60)))

                # 創建半透明背景
                message_surface = pygame.Surface((len(message) * 12, 30))
                message_surface.set_alpha(alpha // 2)
                message_surface.fill((0, 0, 0))
                screen.blit(
                    message_surface,
                    (SCREEN_WIDTH // 2 - len(message) * 6, y_offset + i * 35),
                )

                # 繪製文字
                text = self.font_medium.render(message, True, (255, 255, 0, alpha))
                text_rect = text.get_rect(
                    center=(SCREEN_WIDTH // 2, y_offset + i * 35 + 15)
                )
                screen.blit(text, text_rect)

        # 繪製完成關卡慶祝訊息
        if self.congratulation_messages and self.congratulation_timer > 0:
            y_offset = 200
            for i, message in enumerate(self.congratulation_messages):
                # 彩虹效果
                time_factor = (300 - self.congratulation_timer) / 300.0
                hue = (time_factor * 360 + i * 60) % 360
                import colorsys

                rgb = colorsys.hsv_to_rgb(hue / 360.0, 1.0, 1.0)
                color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

                # 跳動效果
                bounce = abs(math.sin(time_factor * 10 + i)) * 10

                # 創建半透明背景
                bg_width = len(message) * 12
                message_surface = pygame.Surface((bg_width, 35))
                message_surface.set_alpha(150)
                message_surface.fill((0, 0, 0))
                screen.blit(
                    message_surface,
                    (SCREEN_WIDTH // 2 - bg_width // 2, y_offset + i * 40 - bounce),
                )

                # 繪製慶祝文字
                text = self.font_medium.render(message, True, color)
                text_rect = text.get_rect(
                    center=(SCREEN_WIDTH // 2, y_offset + i * 40 + 15 - bounce)
                )
                screen.blit(text, text_rect)

        # 超級慶祝效果（完成最終關卡）
        if self.mega_celebration and self.mega_celebration_timer > 0:
            # 全螢幕閃爍效果
            flash_alpha = int(50 * abs(math.sin(self.mega_celebration_timer * 0.2)))
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash_surface.set_alpha(flash_alpha)

            # 彩虹閃爍
            time_factor = self.mega_celebration_timer / 100.0
            hue = (time_factor * 720) % 360
            import colorsys

            rgb = colorsys.hsv_to_rgb(hue / 360.0, 0.5, 1.0)
            flash_color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
            flash_surface.fill(flash_color)
            screen.blit(flash_surface, (0, 0))

            # 大字慶祝文字
            if self.mega_celebration_timer > 450:  # 前7.5秒
                mega_text = "🎆 傳奇誕生！🎆"
                text = self.font_large.render(mega_text, True, (255, 255, 255))
                text_rect = text.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                )

                # 文字發光效果
                for offset in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                    glow_text = self.font_large.render(mega_text, True, flash_color)
                    glow_rect = text_rect.copy()
                    glow_rect.x += offset[0]
                    glow_rect.y += offset[1]
                    screen.blit(glow_text, glow_rect)

                screen.blit(text, text_rect)

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
        # 特殊背景效果
        if self.current_level == 12 or self.current_level == TOTAL_LEVELS:
            # 為最終關卡添加特殊背景
            import math
            import time

            for i in range(0, SCREEN_WIDTH, 20):
                for j in range(0, SCREEN_HEIGHT, 20):
                    hue = (i + j + time.time() * 100) % 360
                    import colorsys

                    rgb = colorsys.hsv_to_rgb(hue / 360.0, 0.3, 0.6)
                    color = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
                    pygame.draw.rect(screen, color, (i, j, 20, 20))
        else:
            screen.fill(DARK_BLUE)

        # 勝利訊息
        if self.current_level == 12:
            title = self.font_large.render("🏆 無限征服者！🏆", True, (255, 215, 0))
        elif self.current_level == TOTAL_LEVELS:
            title = self.font_large.render("👑 跳躍之神！👑", True, (255, 215, 0))
        else:
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
                if self.current_level == 12:
                    perfect_text = "🌟 史詩級成就達成！🌟"
                    text = self.font_medium.render(perfect_text, True, (255, 215, 0))
                else:
                    perfect_text = "挑戰成功！"
                    text = self.font_medium.render(perfect_text, True, GREEN)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 400))
                screen.blit(text, text_rect)

        # 特殊成就顯示
        if self.current_level == 12:
            achievement_texts = [
                "✨ 你征服了無限！",
                "🚀 突破了所有極限！",
                "💎 創造了不可能的奇蹟！",
            ]
            for i, achievement in enumerate(achievement_texts):
                text = self.font_small.render(achievement, True, (255, 215, 0))
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 440 + i * 25))
                screen.blit(text, text_rect)

        # 操作說明
        if self.current_level < TOTAL_LEVELS:
            continue_text = "Enter 繼續下一關"
        else:
            continue_text = "你已完成所有關卡！"

        text = self.font_small.render(continue_text, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 520))
        screen.blit(text, text_rect)

        back_text = "ESC 返回主選單"
        text = self.font_small.render(back_text, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 550))
        screen.blit(text, text_rect)

        # F11全屏快捷鍵說明
        fullscreen_text = "F11 切換全屏"
        text = self.font_small.render(fullscreen_text, True, GRAY)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 580))
        screen.blit(text, text_rect)

    def draw_game_over(self):
        """繪製失敗畫面"""
        if self.fullscreen:
            # 全屏模式下，先繪製到虛擬畫布
            virtual_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.draw_game_over_content(virtual_screen)
            self.scale_and_blit_virtual_screen(virtual_screen)
        else:
            # 視窗模式直接繪製
            self.draw_game_over_content(self.screen)

    def draw_game_over_content(self, screen):
        """繪製失敗畫面內容"""
        # 深紅色背景
        screen.fill((80, 20, 20))

        # 失敗標題
        title = self.font_large.render("挑戰失敗！", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(title, title_rect)

        # 關卡資訊
        level_data = self.level_manager.get_level(self.current_level)
        if level_data and self.player:
            deaths = self.player.death_count
            target = level_data["target_deaths"]

            # 關卡名稱
            level_text = f"第{self.current_level}關: {level_data['name']}"
            text = self.font_medium.render(level_text, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 280))
            screen.blit(text, text_rect)

            # 死亡次數
            deaths_text = f"你的死亡次數: {deaths}"
            text = self.font_medium.render(deaths_text, True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 320))
            screen.blit(text, text_rect)

            # 目標次數
            target_text = f"目標死亡次數: {target}"
            text = self.font_medium.render(target_text, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 360))
            screen.blit(text, text_rect)

            # 超過提示
            over_text = f"超過目標 {deaths - target} 次"
            text = self.font_medium.render(over_text, True, YELLOW)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 400))
            screen.blit(text, text_rect)

        # 鼓勵文字
        encouragement = "不要放棄！再試一次！"
        text = self.font_medium.render(encouragement, True, GREEN)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 460))
        screen.blit(text, text_rect)

        # 操作說明
        restart_text = "Enter/Space 重新開始關卡"
        text = self.font_small.render(restart_text, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 520))
        screen.blit(text, text_rect)

        menu_text = "ESC 返回主選單"
        text = self.font_small.render(menu_text, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 550))
        screen.blit(text, text_rect)

        # F11全屏快捷鍵說明
        fullscreen_text = "F11 切換全屏"
        text = self.font_small.render(fullscreen_text, True, GRAY)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 580))
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
        elif self.state == GAME_OVER:
            self.draw_game_over()

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
