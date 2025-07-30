import pygame
import random
import sys
import math

# 初始化 pygame
pygame.init()

# 遊戲設定 - 支持動態解析度
DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 400
SCREEN_WIDTH = DEFAULT_SCREEN_WIDTH
SCREEN_HEIGHT = DEFAULT_SCREEN_HEIGHT
GROUND_HEIGHT = int(SCREEN_HEIGHT * 0.875)  # 動態地面高度
FPS = 60

# 全螢幕設定
FULLSCREEN_MODE = False
WINDOW_MODE = pygame.RESIZABLE


# 顏色定義 - 參考 class3-3.py 的顏色管理方式
def define_color_palette():
    """
    定義遊戲中使用的顏色調色板

    Returns:
        dict: 包含所有顏色的字典
    """
    return {
        "WHITE": (255, 255, 255),
        "BLACK": (0, 0, 0),
        "GRAY": (128, 128, 128),
        "GREEN": (0, 255, 0),
        "RED": (255, 0, 0),
        "BLUE": (0, 0, 255),
        "YELLOW": (255, 255, 0),
        "PURPLE": (128, 0, 128),
        "ORANGE": (255, 165, 0),
        "PINK": (255, 192, 203),
        "LIGHT_BLUE": (173, 216, 230),
        "DARK_GREEN": (0, 100, 0),
        "DARK_GRAY": (64, 64, 64),
    }


# 全域顏色變數（向後兼容）
colors = define_color_palette()
WHITE = colors["WHITE"]
BLACK = colors["BLACK"]
GRAY = colors["GRAY"]
GREEN = colors["GREEN"]

# 為了向後兼容，創建一個全域變數
_global_colors = colors

# 遊戲狀態
GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAME_OVER = 2

# 難度設定
DIFFICULTY_EASY = 1
DIFFICULTY_MEDIUM = 2
DIFFICULTY_HARD = 3
DIFFICULTY_NIGHTMARE = 4


class MenuSystem:
    """主選單系統"""

    def __init__(self, colors, fonts):
        self.colors = colors
        self.fonts = fonts
        self.selected_difficulty = DIFFICULTY_EASY
        self.menu_options = [
            {
                "name": "簡單 (Easy)",
                "difficulty": DIFFICULTY_EASY,
                "description": "適合新手，慢節奏遊戲",
            },
            {
                "name": "中等 (Medium)",
                "difficulty": DIFFICULTY_MEDIUM,
                "description": "標準難度，平衡的挑戰",
            },
            {
                "name": "困難 (Hard)",
                "difficulty": DIFFICULTY_HARD,
                "description": "快節奏，需要技巧",
            },
            {
                "name": "噩夢 (Nightmare)",
                "difficulty": DIFFICULTY_NIGHTMARE,
                "description": "極速+隱形+爆炸+重力干擾",
            },
        ]
        self.selected_index = 0
        self.animation_timer = 0

    def handle_menu_input(self, event):
        """處理選單輸入"""
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
        """繪製主選單 - 支持動態螢幕大小"""
        # 背景
        screen.fill(self.colors["BLACK"])

        # 繪製背景星空效果
        star_count = max(
            50, SCREEN_WIDTH * SCREEN_HEIGHT // 10000
        )  # 根據螢幕大小調整星星數量
        for i in range(star_count):
            x = (i * 157) % SCREEN_WIDTH
            y = (i * 211) % SCREEN_HEIGHT
            brightness = int(100 + 50 * math.sin(self.animation_timer * 0.01 + i))
            color = (brightness, brightness, brightness)
            star_size = max(1, int(SCREEN_WIDTH / 800))  # 根據螢幕大小調整星星大小
            pygame.draw.circle(screen, color, (x, y), star_size)

        # 遊戲標題 - 動態位置
        title_text = "🦕 超級進階小恐龍遊戲 🦕"
        title_surface = self.fonts["large"].render(
            title_text, True, self.colors["YELLOW"]
        )
        title_y = int(SCREEN_HEIGHT * 0.08)  # 8% 的螢幕高度
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, title_y))
        screen.blit(title_surface, title_rect)

        # 副標題 - 動態位置
        subtitle_text = "選擇您的挑戰等級"
        subtitle_surface = self.fonts["medium"].render(
            subtitle_text, True, self.colors["WHITE"]
        )
        subtitle_y = int(SCREEN_HEIGHT * 0.12)  # 12% 的螢幕高度
        subtitle_rect = subtitle_surface.get_rect(
            center=(SCREEN_WIDTH // 2, subtitle_y)
        )
        screen.blit(subtitle_surface, subtitle_rect)

        # 繪製選單選項 - 動態位置和大小
        start_y = int(SCREEN_HEIGHT * 0.2)  # 20% 的螢幕高度開始
        option_spacing = int(SCREEN_HEIGHT * 0.08)  # 8% 螢幕高度的間距
        selection_width = min(400, int(SCREEN_WIDTH * 0.5))  # 選擇框寬度

        for i, option in enumerate(self.menu_options):
            y_pos = start_y + i * option_spacing

            # 選中效果
            if i == self.selected_index:
                # 發光邊框
                glow_intensity = int(50 + 30 * math.sin(self.animation_timer * 0.1))

                # 選中背景 - 動態大小
                selection_rect = pygame.Rect(
                    SCREEN_WIDTH // 2 - selection_width // 2,
                    y_pos - int(option_spacing * 0.3),
                    selection_width,
                    int(option_spacing * 0.6),
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

            option_rect = option_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            screen.blit(option_surface, option_rect)

            # 難度描述
            desc_color = (
                self.colors["YELLOW"]
                if i == self.selected_index
                else self.colors["DARK_GRAY"]
            )
            if "DARK_GRAY" not in self.colors:
                desc_color = (
                    (100, 100, 100)
                    if i != self.selected_index
                    else self.colors["YELLOW"]
                )

            desc_surface = self.fonts["small"].render(
                option["description"], True, desc_color
            )
            desc_y = y_pos + int(option_spacing * 0.25)
            desc_rect = desc_surface.get_rect(center=(SCREEN_WIDTH // 2, desc_y))
            screen.blit(desc_surface, desc_rect)

        # 控制說明 - 動態位置
        control_text = "↑↓ 選擇難度  |  空白鍵/Enter 開始遊戲  |  F11 全螢幕"
        control_surface = self.fonts["small"].render(
            control_text, True, self.colors["WHITE"]
        )
        control_y = int(SCREEN_HEIGHT * 0.9)  # 90% 螢幕高度
        control_rect = control_surface.get_rect(center=(SCREEN_WIDTH // 2, control_y))
        screen.blit(control_surface, control_rect)

        # 難度預覽 - 動態位置
        preview_texts = {
            DIFFICULTY_EASY: [
                "• 慢速障礙物",
                "• 簡單的跳躍和蹲下",
                "• 適合學習基本操作",
            ],
            DIFFICULTY_MEDIUM: ["• 中等速度", "• 基本障礙物組合", "• 需要一定反應能力"],
            DIFFICULTY_HARD: ["• 快速移動", "• 複雜障礙物", "• 需要高度集中"],
            DIFFICULTY_NIGHTMARE: [
                "• 超極速模式 + 重力異常",
                "• 隱形&爆炸&分裂障礙物",
                "• 能力冷卻時間大幅增加",
                "• 螢幕會隨機閃爍干擾",
            ],
        }

        selected_option = self.menu_options[self.selected_index]
        if selected_option["difficulty"] in preview_texts:
            preview_start_y = int(SCREEN_HEIGHT * 0.7)  # 70% 螢幕高度開始
            preview_line_spacing = int(SCREEN_HEIGHT * 0.025)  # 2.5% 螢幕高度間距

            for j, preview_text in enumerate(
                preview_texts[selected_option["difficulty"]]
            ):
                preview_surface = self.fonts["small"].render(
                    preview_text, True, self.colors["ORANGE"]
                )
                preview_y = preview_start_y + j * preview_line_spacing
                preview_rect = preview_surface.get_rect(
                    center=(SCREEN_WIDTH // 2, preview_y)
                )
                screen.blit(preview_surface, preview_rect)


class Dinosaur:
    def __init__(self, colors=None):
        if colors is None:
            colors = define_color_palette()
        self.colors = colors

        # 動態位置和大小
        scale_factor = min(
            SCREEN_WIDTH / DEFAULT_SCREEN_WIDTH, SCREEN_HEIGHT / DEFAULT_SCREEN_HEIGHT
        )
        self.x = int(80 * scale_factor)
        self.width = int(40 * scale_factor)
        self.height = int(40 * scale_factor)
        self.original_height = self.height
        self.y = GROUND_HEIGHT - self.height

        # 物理屬性
        self.jump_speed = 0
        self.gravity = 0.8 * scale_factor
        self.is_jumping = False
        self.is_ducking = False
        self.jump_strength = -15 * scale_factor

        # 新增能力
        self.dash_cooldown = 0
        self.dash_distance = 0
        self.is_dashing = False
        self.shield_time = 0
        self.has_shield = False
        self.double_jump_available = False
        self.animation_frame = 0

        # 噩夢/地獄模式專用屬性
        self.gravity_reversal_time = 0  # 重力反轉時間
        self.is_gravity_reversed = False  # 重力是否反轉
        self.control_inversion_time = 0  # 控制反轉時間
        self.is_control_inverted = False  # 控制是否反轉
        self.ability_malfunction_time = 0  # 能力故障時間
        self.nightmare_effects = {
            "screen_flicker": 0,
            "gravity_chaos": 0,
            "time_distortion": 1.0,
            "ability_curse": 0,
        }

    def jump(self):
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
        """衝刺功能"""
        # 檢查能力是否故障
        if self.ability_malfunction_time > 0:
            return

        if self.dash_cooldown <= 0 and not self.is_dashing:
            self.is_dashing = True
            self.dash_distance = 80
            # 噩夢/地獄模式冷卻時間更長
            base_cooldown = 180
            if hasattr(self, "nightmare_effects"):
                base_cooldown = int(
                    base_cooldown * (1 + self.nightmare_effects["time_distortion"])
                )
            self.dash_cooldown = base_cooldown

    def activate_shield(self):
        """啟動護盾"""
        # 檢查能力是否故障
        if self.ability_malfunction_time > 0:
            return

        if not self.has_shield:
            self.has_shield = True
            self.shield_time = 300  # 5秒護盾時間

    def duck(self):
        """蹲下功能"""
        if not self.is_jumping:
            self.is_ducking = True
            self.height = 20  # 降低高度
            self.y = GROUND_HEIGHT - 20  # 調整位置

    def stand_up(self):
        """站起來"""
        if not self.is_jumping:
            self.is_ducking = False
            self.height = self.original_height
            self.y = GROUND_HEIGHT - self.original_height

    def update(self):
        self.animation_frame += 1

        # 處理噩夢模式效果
        if hasattr(self, "nightmare_effects"):
            # 重力反轉效果
            if self.gravity_reversal_time > 0:
                self.gravity_reversal_time -= 1
                self.is_gravity_reversed = True
            else:
                self.is_gravity_reversed = False

            # 控制反轉效果
            if self.control_inversion_time > 0:
                self.control_inversion_time -= 1
                self.is_control_inverted = True
            else:
                self.is_control_inverted = False

            # 能力故障效果
            if self.ability_malfunction_time > 0:
                self.ability_malfunction_time -= 1

        # 衝刺邏輯
        if self.is_dashing and self.dash_distance > 0:
            move_amount = min(8, self.dash_distance)
            self.x += move_amount
            self.dash_distance -= move_amount
            if self.dash_distance <= 0:
                self.is_dashing = False
                self.x = max(80, self.x)  # 確保不會超出螢幕

        # 冷卻時間減少
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        # 護盾時間減少
        if self.shield_time > 0:
            self.shield_time -= 1
            if self.shield_time <= 0:
                self.has_shield = False

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
                if self.y >= GROUND_HEIGHT - self.height:
                    self.y = GROUND_HEIGHT - self.height
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

            # 畫小恐龍（簡單的矩形）
        dino_color = (
            self.colors["GREEN"] if not self.has_shield else self.colors["LIGHT_BLUE"]
        )
        pygame.draw.rect(screen, dino_color, (self.x, self.y, self.width, self.height))

        # 恐龍的眼睛
        eye_y = self.y + 10 if not self.is_ducking else self.y + 5
        pygame.draw.circle(screen, self.colors["BLACK"], (self.x + 10, eye_y), 3)

        # 如果在蹲下，改變形狀
        if self.is_ducking:
            # 畫蹲下的恐龍（更扁平）
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


class Obstacle:
    """基礎障礙物類"""

    def __init__(self, x=None, obstacle_type="normal", colors=None):
        if colors is None:
            colors = define_color_palette()
        self.colors = colors
        self.x = x if x is not None else SCREEN_WIDTH
        self.speed = 5
        self.obstacle_type = obstacle_type
        self.animation_counter = 0
        self.warning_time = 0
        self.is_warned = False
        self.health = 1  # 預設生命值
        self.setup_obstacle()

    def setup_obstacle(self):
        """根據障礙物類型設置屬性 - 支持動態縮放"""
        # 計算縮放因子
        scale_factor = min(
            SCREEN_WIDTH / DEFAULT_SCREEN_WIDTH, SCREEN_HEIGHT / DEFAULT_SCREEN_HEIGHT
        )

        if self.obstacle_type == "normal":
            # 普通仙人掌
            self.width = int(20 * scale_factor)
            self.height = int(30 * scale_factor)
            self.y = GROUND_HEIGHT - self.height
            self.color = BLACK
        elif self.obstacle_type == "tall":
            # 高仙人掌
            self.width = int(25 * scale_factor)
            self.height = int(50 * scale_factor)
            self.y = GROUND_HEIGHT - self.height
            self.color = BLACK
        elif self.obstacle_type == "wide":
            # 寬仙人掌
            self.width = int(35 * scale_factor)
            self.height = int(35 * scale_factor)
            self.y = GROUND_HEIGHT - self.height
            self.color = BLACK
        elif self.obstacle_type == "short":
            # 矮仙人掌（不需要跳躍）
            self.width = int(30 * scale_factor)
            self.height = int(15 * scale_factor)
            self.y = GROUND_HEIGHT - self.height
            self.color = self.colors["DARK_GREEN"]
        elif self.obstacle_type == "flying":
            # 飛行障礙物（鳥類）
            self.width = int(25 * scale_factor)
            self.height = int(15 * scale_factor)
            self.y = GROUND_HEIGHT - int(80 * scale_factor)
            self.color = self.colors["GRAY"]
        elif self.obstacle_type == "double":
            # 雙重障礙物（上下兩個）
            self.y = GROUND_HEIGHT - 30
            self.width = 20
            self.height = 30
            self.color = self.colors["PURPLE"]
            self.upper_y = GROUND_HEIGHT - 100
            self.upper_height = 25
        elif self.obstacle_type == "moving_up":
            # 上下移動的障礙物
            self.y = GROUND_HEIGHT - 40
            self.original_y = self.y
            self.width = 22
            self.height = 40
            self.color = self.colors["ORANGE"]
            self.move_range = 30
            self.move_speed = 2
        elif self.obstacle_type == "invisible":
            # 隱形障礙物（只在警告時可見）
            self.y = GROUND_HEIGHT - 35
            self.width = 25
            self.height = 35
            self.color = self.colors["RED"]
            self.warning_time = 90  # 1.5秒警告時間
        elif self.obstacle_type == "explosive":
            # 爆炸障礙物（碰撞後會擴散）
            self.y = GROUND_HEIGHT - 40
            self.width = 30
            self.height = 40
            self.color = self.colors["RED"]
            self.health = 1
            self.explosion_radius = 0
            self.is_exploding = False
        elif self.obstacle_type == "armored":
            # 裝甲障礙物（需要多次攻擊）
            self.y = GROUND_HEIGHT - 45
            self.width = 35
            self.height = 45
            self.color = self.colors["BLUE"]
            self.health = 3  # 需要3次攻擊
            self.original_color = self.colors["BLUE"]

    def update(self):
        self.animation_counter += 1
        self.x -= self.speed

        # 特殊障礙物的更新邏輯
        if self.obstacle_type == "moving_up":
            # 上下移動邏輯
            move_offset = math.sin(self.animation_counter * 0.1) * self.move_range
            self.y = self.original_y + move_offset
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
        elif self.obstacle_type == "armored":
            # 裝甲障礙物可能改變顏色
            pass

    def draw(self, screen):
        if self.obstacle_type == "flying":
            # 畫飛行障礙物（簡單的鳥形）
            pygame.draw.ellipse(
                screen, self.color, (self.x, self.y, self.width, self.height)
            )
            # 翅膀
            pygame.draw.ellipse(screen, self.color, (self.x - 5, self.y + 3, 15, 8))
            pygame.draw.ellipse(screen, self.color, (self.x + 15, self.y + 3, 15, 8))
        elif self.obstacle_type == "short":
            # 畫矮障礙物（石頭）
            pygame.draw.rect(
                screen, self.color, (self.x, self.y, self.width, self.height)
            )
            # 添加一些細節讓它看起來像石頭
            pygame.draw.circle(
                screen, self.colors["GREEN"], (self.x + 5, self.y + 5), 3
            )
            pygame.draw.circle(
                screen, self.colors["GREEN"], (self.x + 20, self.y + 8), 2
            )
        elif self.obstacle_type == "double":
            # 畫雙重障礙物
            pygame.draw.rect(
                screen, self.color, (self.x, self.y, self.width, self.height)
            )
            pygame.draw.rect(
                screen,
                self.color,
                (self.x, self.upper_y, self.width, self.upper_height),
            )
            # 連接線
            pygame.draw.line(
                screen,
                self.color,
                (self.x + self.width // 2, self.y),
                (self.x + self.width // 2, self.upper_y + self.upper_height),
                3,
            )
        elif self.obstacle_type == "moving_up":
            # 畫移動障礙物
            pygame.draw.rect(
                screen, self.color, (self.x, self.y, self.width, self.height)
            )
            # 添加移動指示器
            pygame.draw.polygon(
                screen,
                colors["YELLOW"],
                [
                    (self.x + self.width // 2, self.y - 10),
                    (self.x + self.width // 2 - 5, self.y - 5),
                    (self.x + self.width // 2 + 5, self.y - 5),
                ],
            )
        elif self.obstacle_type == "invisible":
            # 隱形障礙物只在警告時顯示
            if self.is_warned:
                # 閃爍效果
                alpha = 100 + int(50 * math.sin(self.animation_counter * 0.3))
                warning_surface = pygame.Surface((self.width + 10, self.height + 10))
                warning_surface.set_alpha(alpha)
                warning_surface.fill(colors["RED"])
                screen.blit(warning_surface, (self.x - 5, self.y - 5))
                # 警告標記
                pygame.draw.rect(
                    screen,
                    colors["YELLOW"],
                    (self.x, self.y, self.width, self.height),
                    3,
                )
        elif self.obstacle_type == "explosive":
            # 畫爆炸障礙物
            if self.is_exploding:
                # 爆炸效果
                for i in range(5):
                    radius = self.explosion_radius - i * 10
                    if radius > 0:
                        alpha = max(0, 255 - i * 50)
                        explosion_surface = pygame.Surface((radius * 2, radius * 2))
                        explosion_surface.set_alpha(alpha)
                        explosion_surface.fill(colors["ORANGE"])
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
                    colors["YELLOW"],
                    (self.x + self.width // 2, self.y + self.height // 2),
                    8,
                )
                pygame.draw.circle(
                    screen,
                    colors["RED"],
                    (self.x + self.width // 2, self.y + self.height // 2),
                    5,
                )
        elif self.obstacle_type == "armored":
            # 畫裝甲障礙物
            # 根據生命值改變顏色
            if self.health == 3:
                current_color = colors["BLUE"]
            elif self.health == 2:
                current_color = colors["PURPLE"]
            else:
                current_color = colors["RED"]

            pygame.draw.rect(
                screen, current_color, (self.x, self.y, self.width, self.height)
            )
            # 裝甲線條
            for i in range(3):
                y_offset = i * (self.height // 3)
                pygame.draw.line(
                    screen,
                    colors["WHITE"],
                    (self.x, self.y + y_offset),
                    (self.x + self.width, self.y + y_offset),
                    2,
                )
            # 生命值顯示
            for i in range(self.health):
                pygame.draw.circle(
                    screen, colors["WHITE"], (self.x + 5 + i * 8, self.y + 5), 3
                )
        else:
            # 畫普通障礙物（仙人掌）
            pygame.draw.rect(
                screen, self.color, (self.x, self.y, self.width, self.height)
            )
            if self.obstacle_type == "tall":
                # 高仙人掌添加分支
                pygame.draw.rect(screen, self.color, (self.x - 8, self.y + 15, 15, 8))
                pygame.draw.rect(screen, self.color, (self.x + 18, self.y + 20, 15, 8))
            elif self.obstacle_type == "wide":
                # 寬仙人掌添加更多分支
                pygame.draw.rect(screen, self.color, (self.x - 5, self.y + 10, 12, 6))
                pygame.draw.rect(screen, self.color, (self.x + 28, self.y + 15, 12, 6))
            # 畫分裂障礙物
            if not self.has_split:
                pygame.draw.rect(
                    screen, self.color, (self.x, self.y, self.width, self.height)
                )
                # 分裂標記
                pygame.draw.line(
                    screen,
                    colors["YELLOW"],
                    (self.x + self.width // 2, self.y),
                    (self.x + self.width // 2, self.y + self.height),
                    3,
                )
            else:
                # 繪製分裂體
                for child in self.split_children:
                    pygame.draw.rect(
                        screen,
                        child["color"],
                        (child["x"], child["y"], child["width"], child["height"]),
                    )

            # 畫重力炸彈
            color = colors["RED"] if self.is_active else colors["BLACK"]
            pygame.draw.circle(
                screen,
                color,
                (self.x + self.width // 2, self.y + self.height // 2),
                self.width // 2,
            )
            if self.is_active:
                # 重力場效果
                for i in range(3):
                    radius = self.gravity_radius - i * 20
                    pygame.draw.circle(
                        screen,
                        colors["PURPLE"],
                        (self.x + self.width // 2, self.y + self.height // 2),
                        radius,
                        2,
                    )

            # 畫時空扭曲障礙物
            # 扭曲效果
            for i in range(5):
                offset = int(self.warp_intensity * math.sin(i * 0.5))
                pygame.draw.rect(
                    screen, self.color, (self.x + offset, self.y + i * 9, self.width, 9)
                )
            # 時空漩渦
            pygame.draw.circle(
                screen,
                colors["LIGHT_BLUE"],
                (self.x + self.width // 2, self.y + self.height // 2),
                20 + abs(self.warp_intensity // 2),
                2,
            )

            # 畫地獄尖刺
            for i in range(self.spike_count):
                spike_x = self.x + i * self.spike_spacing
                # 尖刺三角形
                pygame.draw.polygon(
                    screen,
                    self.color,
                    [
                        (spike_x, self.y + self.height),
                        (spike_x + self.width // 2, self.y),
                        (spike_x + self.width, self.y + self.height),
                    ],
                )
                # 地獄火焰效果
                pygame.draw.circle(
                    screen, colors["ORANGE"], (spike_x + self.width // 2, self.y), 5
                )

            # 畫惡魔傳送門
            # 傳送門本體
            pygame.draw.ellipse(
                screen, colors["PURPLE"], (self.x, self.y, self.width, self.height)
            )
            pygame.draw.ellipse(
                screen,
                colors["BLACK"],
                (self.x + 5, self.y + 5, self.width - 10, self.height - 10),
            )
            # 傳送門能量
            energy_color = (
                128 + int(127 * math.sin(self.animation_counter * 0.2)),
                0,
                128,
            )
            pygame.draw.ellipse(
                screen,
                energy_color,
                (self.x + 8, self.y + 8, self.width - 16, self.height - 16),
            )

            # 繪製傳送門生成的惡魔
            for demon in self.portal_demons:
                pygame.draw.rect(
                    screen,
                    demon["color"],
                    (demon["x"], demon["y"], demon["width"], demon["height"]),
                )
                # 惡魔眼睛
                pygame.draw.circle(
                    screen, colors["YELLOW"], (demon["x"] + 3, demon["y"] + 3), 2
                )
                pygame.draw.circle(
                    screen, colors["YELLOW"], (demon["x"] + 9, demon["y"] + 3), 2
                )
            else:
                # 畫普通障礙物（仙人掌）
                pygame.draw.rect(
                    screen, self.color, (self.x, self.y, self.width, self.height)
                )
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
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def can_duck_under(self):
        """檢查是否可以蹲下通過"""
        return self.obstacle_type in ["flying"]

    def can_walk_through(self):
        """檢查是否可以直接走過"""
        return self.obstacle_type in ["short"]


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(0, 200)
        self.y = random.randint(50, 150)
        self.speed = 1

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        # 畫雲朵
        pygame.draw.ellipse(screen, GRAY, (self.x, self.y, 40, 20))
        pygame.draw.ellipse(screen, GRAY, (self.x + 10, self.y - 5, 30, 20))


class Game:
    def __init__(self):
        # 初始化螢幕設定
        self.fullscreen_mode = FULLSCREEN_MODE
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.ground_height = GROUND_HEIGHT

        # 設定顯示模式
        self.setup_display()
        pygame.display.set_caption("🦕 超級進階小恐龍遊戲 - 進階版本")
        self.clock = pygame.time.Clock()

        # 遊戲狀態
        self.game_state = GAME_STATE_MENU
        self.selected_difficulty = DIFFICULTY_EASY

        # 載入顏色調色板
        self.colors = define_color_palette()

        # 字體設定 - 參考 class3-3.py 的字體處理方式
        self.setup_fonts()

        # 主選單系統
        self.menu_system = MenuSystem(
            self.colors,
            {
                "large": self.font_large,
                "medium": self.font_medium,
                "small": self.font_small,
            },
        )

        # 遊戲物件 (初始化但不使用)
        self.dinosaur = None
        self.obstacles = []
        self.clouds = []
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.obstacle_timer = 0
        self.cloud_timer = 0
        self.game_speed = 5
        self.speed_increase_timer = 0

        # 新增遊戲機制
        self.difficulty_level = 1
        self.combo_count = 0
        self.max_combo = 0
        self.power_up_timer = 0
        self.screen_shake = 0
        self.warning_obstacles = []
        self.particle_effects = []

    def setup_display(self):
        """設定遊戲顯示模式"""
        if self.fullscreen_mode:
            # 全螢幕模式
            display_info = pygame.display.Info()
            self.screen_width = display_info.current_w
            self.screen_height = display_info.current_h
            self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height), pygame.FULLSCREEN
            )
            print(f"🖥️ 全螢幕模式: {self.screen_width}x{self.screen_height}")
        else:
            # 視窗模式
            self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height), WINDOW_MODE
            )
            print(f"🪟 視窗模式: {self.screen_width}x{self.screen_height}")

        # 更新地面高度
        self.ground_height = int(self.screen_height * 0.875)

        # 更新全域變數
        global SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT
        SCREEN_WIDTH = self.screen_width
        SCREEN_HEIGHT = self.screen_height
        GROUND_HEIGHT = self.ground_height

    def toggle_fullscreen(self):
        """切換全螢幕模式"""
        self.fullscreen_mode = not self.fullscreen_mode
        if self.fullscreen_mode:
            # 進入全螢幕
            display_info = pygame.display.Info()
            self.screen_width = display_info.current_w
            self.screen_height = display_info.current_h
            self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height), pygame.FULLSCREEN
            )
            print(f"🖥️ 切換到全螢幕模式: {self.screen_width}x{self.screen_height}")
        else:
            # 回到視窗模式
            self.screen_width = DEFAULT_SCREEN_WIDTH
            self.screen_height = DEFAULT_SCREEN_HEIGHT
            self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height), WINDOW_MODE
            )
            print(f"🪟 切換到視窗模式: {self.screen_width}x{self.screen_height}")

        # 更新相關設定
        self.ground_height = int(self.screen_height * 0.875)

        # 更新全域變數
        global SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT
        SCREEN_WIDTH = self.screen_width
        SCREEN_HEIGHT = self.screen_height
        GROUND_HEIGHT = self.ground_height

        # 重新設定恐龍位置
        if hasattr(self, "dinosaur") and self.dinosaur:
            self.dinosaur.y = self.ground_height - self.dinosaur.height

    def setup_fonts(self):
        """設定遊戲字體 - 參考 class3-3.py 的字體處理，支持動態大小"""
        # 根據螢幕大小調整字體大小
        scale_factor = min(
            self.screen_width / DEFAULT_SCREEN_WIDTH,
            self.screen_height / DEFAULT_SCREEN_HEIGHT,
        )
        large_size = int(36 * scale_factor)
        medium_size = int(24 * scale_factor)
        small_size = int(18 * scale_factor)

        # 嘗試載入微軟正黑體
        font_path = r"C:\Windows\Fonts\msjh.ttc"
        try:
            self.font_large = pygame.font.Font(font_path, large_size)
            self.font_medium = pygame.font.Font(font_path, medium_size)
            self.font_small = pygame.font.Font(font_path, small_size)
            print(f"✅ 成功載入微軟正黑體 (縮放: {scale_factor:.2f}x)")
        except FileNotFoundError:
            # 如果找不到微軟正黑體，使用系統預設字體
            print("⚠️ 找不到微軟正黑體，使用系統預設字體")
            self.font_large = pygame.font.Font(None, large_size)
            self.font_medium = pygame.font.Font(None, medium_size)
            self.font_small = pygame.font.Font(None, small_size)

    def start_game(self, difficulty):
        """根據選擇的難度開始遊戲"""
        self.selected_difficulty = difficulty
        self.difficulty_level = difficulty
        self.game_state = GAME_STATE_PLAYING

        # 重新初始化遊戲物件
        self.dinosaur = Dinosaur(colors=self.colors)
        self.obstacles = []
        self.clouds = []
        self.score = 0
        self.game_over = False
        self.obstacle_timer = 0
        self.cloud_timer = 0
        self.combo_count = 0
        self.screen_shake = 0

        # 根據難度設定遊戲參數
        difficulty_settings = (
            {
                DIFFICULTY_EASY: {
                    "game_speed": 3,
                    "obstacle_spawn_rate": 1.0,
                    "speed_increase_rate": 0.1,
                },
                DIFFICULTY_MEDIUM: {
                    "game_speed": 5,
                    "obstacle_spawn_rate": 1.2,
                    "speed_increase_rate": 0.15,
                },
                DIFFICULTY_HARD: {
                    "game_speed": 7,
                    "obstacle_spawn_rate": 1.5,
                    "speed_increase_rate": 0.2,
                },
                DIFFICULTY_NIGHTMARE: {
                    "game_speed": 12,
                    "obstacle_spawn_rate": 2.5,
                    "speed_increase_rate": 0.4,
                },
                "game_speed": 15,
                "obstacle_spawn_rate": 3.5,
                "speed_increase_rate": 0.6,
            },
        )

        settings = difficulty_settings[difficulty]
        self.game_speed = settings["game_speed"]
        self.obstacle_spawn_rate = settings["obstacle_spawn_rate"]
        self.speed_increase_rate = settings["speed_increase_rate"]

        print(f"🚀 遊戲開始！難度等級: {difficulty}")

    def return_to_menu(self):
        """返回主選單"""
        self.game_state = GAME_STATE_MENU
        self.menu_system.selected_index = 0

    def spawn_obstacle(self):
        if self.obstacle_timer <= 0:
            # 根據難度等級選擇障礙物類型
            if self.difficulty_level == DIFFICULTY_EASY:
                obstacle_types = ["normal", "tall", "wide", "short", "flying"]
            elif self.difficulty_level == DIFFICULTY_MEDIUM:
                obstacle_types = ["normal", "tall", "wide", "short", "flying", "double"]
            elif self.difficulty_level == DIFFICULTY_HARD:
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
            elif self.difficulty_level == DIFFICULTY_NIGHTMARE:
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
                    # 新增分裂障礙物
                ]
            else:  # 最高難度為噩夢
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

            obstacle_type = random.choice(obstacle_types)
            self.obstacles.append(
                Obstacle(obstacle_type=obstacle_type, colors=self.colors)
            )

            # 根據難度調整生成間隔 - 地獄模式更加瘋狂
            base_interval = max(15, int(120 / self.obstacle_spawn_rate))
            interval_variation = max(5, int(40 / self.obstacle_spawn_rate))
            if False:  # 地獄難度已移除
                base_interval = max(10, base_interval // 2)  # 地獄模式間隔減半

            self.obstacle_timer = random.randint(
                base_interval, base_interval + interval_variation
            )
        else:
            self.obstacle_timer -= 1

    def spawn_cloud(self):
        if self.cloud_timer <= 0:
            self.clouds.append(Cloud())
            self.cloud_timer = random.randint(180, 300)  # 3-5秒間隔
        else:
            self.cloud_timer -= 1

    def check_collision(self):
        dino_rect = self.dinosaur.get_collision_rect()

        for obstacle in self.obstacles[:]:
            obstacle_rect = obstacle.get_collision_rect()

            # 檢查是否有碰撞
            if dino_rect.colliderect(obstacle_rect):
                # 檢查特殊情況
                if obstacle.can_walk_through():
                    # 矮障礙物可以直接走過，不算碰撞，增加分數
                    self.combo_count += 1
                    self.score += 5
                    continue
                elif obstacle.can_duck_under() and self.dinosaur.is_ducking:
                    # 飛行障礙物在蹲下時可以避開
                    self.combo_count += 1
                    self.score += 10
                    continue
                elif self.dinosaur.has_shield:
                    # 護盾可以阻擋一次攻擊
                    self.dinosaur.has_shield = False
                    self.dinosaur.shield_time = 0
                    self.screen_shake = 10

                    # 爆炸障礙物觸發爆炸
                    if obstacle.obstacle_type == "explosive":
                        obstacle.is_exploding = True

                    # 移除障礙物並增加分數
                    if obstacle in self.obstacles:
                        self.obstacles.remove(obstacle)
                    self.score += 20
                    continue
                elif obstacle.obstacle_type == "invisible" and not obstacle.is_warned:
                    # 隱形障礙物在不警告時不會碰撞
                    continue
                else:
                    # 處理裝甲障礙物
                    if obstacle.obstacle_type == "armored":
                        obstacle.health -= 1
                        if obstacle.health > 0:
                            self.screen_shake = 5
                            continue

                    # 重置連擊
                    self.combo_count = 0
                    return True
        return False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # 全域快捷鍵 - 不分遊戲狀態
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    # F11 切換全螢幕
                    self.toggle_fullscreen()
                    # 重新設定字體
                    self.setup_fonts()
                    # 更新選單系統的字體
                    if hasattr(self, "menu_system"):
                        self.menu_system.fonts = {
                            "large": self.font_large,
                            "medium": self.font_medium,
                            "small": self.font_small,
                        }
                elif event.key == pygame.K_F4 and (
                    pygame.key.get_pressed()[pygame.K_LALT]
                    or pygame.key.get_pressed()[pygame.K_RALT]
                ):
                    # Alt+F4 退出遊戲
                    return False

            # 處理視窗大小改變
            if event.type == pygame.VIDEORESIZE and not self.fullscreen_mode:
                self.screen_width = event.w
                self.screen_height = event.h
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height), WINDOW_MODE
                )
                self.ground_height = int(self.screen_height * 0.875)

                # 更新全域變數
                global SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT
                SCREEN_WIDTH = self.screen_width
                SCREEN_HEIGHT = self.screen_height
                GROUND_HEIGHT = self.ground_height

                # 重新設定字體
                self.setup_fonts()
                # 更新選單系統的字體
                if hasattr(self, "menu_system"):
                    self.menu_system.fonts = {
                        "large": self.font_large,
                        "medium": self.font_medium,
                        "small": self.font_small,
                    }
                print(f"🔄 視窗大小調整: {self.screen_width}x{self.screen_height}")

            # 處理主選單事件
            if self.game_state == GAME_STATE_MENU:
                if self.menu_system.handle_menu_input(event):
                    # 開始遊戲
                    self.start_game(self.menu_system.selected_difficulty)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return False  # 退出遊戲

            # 處理遊戲中事件
            elif self.game_state == GAME_STATE_PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # 返回主選單
                        self.return_to_menu()
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        if not self.game_over:
                            # 檢查控制是否反轉
                            if (
                                hasattr(self.dinosaur, "is_control_inverted")
                                and self.dinosaur.is_control_inverted
                            ):
                                self.dinosaur.duck()  # 反轉：上鍵變蹲下
                            else:
                                self.dinosaur.jump()  # 正常：上鍵跳躍
                        else:
                            # 重新開始遊戲 (同樣難度)
                            self.start_game(self.selected_difficulty)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if not self.game_over:
                            # 檢查控制是否反轉
                            if (
                                hasattr(self.dinosaur, "is_control_inverted")
                                and self.dinosaur.is_control_inverted
                            ):
                                self.dinosaur.jump()  # 反轉：下鍵變跳躍
                            else:
                                self.dinosaur.duck()  # 正常：下鍵蹲下
                    elif event.key == pygame.K_x:
                        # 衝刺
                        if not self.game_over:
                            self.dinosaur.dash()
                    elif event.key == pygame.K_z:
                        # 啟動護盾
                        if not self.game_over:
                            self.dinosaur.activate_shield()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if not self.game_over:
                            # 檢查控制是否反轉 - 反轉時不需要站起來，因為下鍵變成跳躍
                            if not (
                                hasattr(self.dinosaur, "is_control_inverted")
                                and self.dinosaur.is_control_inverted
                            ):
                                self.dinosaur.stand_up()
        return True

    def restart_game(self):
        self.dinosaur = Dinosaur()
        self.obstacles = []
        self.clouds = []
        self.score = 0
        self.game_over = False
        self.obstacle_timer = 0
        self.cloud_timer = 0
        self.game_speed = 5
        self.speed_increase_timer = 0
        self.difficulty_level = 1
        self.combo_count = 0
        self.screen_shake = 0
        print("🔄 遊戲重新開始")

    def update(self):
        if self.game_state == GAME_STATE_MENU:
            # 更新主選單動畫
            self.menu_system.update()
        elif self.game_state == GAME_STATE_PLAYING:
            if not self.game_over:
                # 噩夢和地獄模式的特殊效果
                if self.difficulty_level >= DIFFICULTY_NIGHTMARE:
                    self.apply_nightmare_effects()

                self.dinosaur.update()

                # 增加遊戲速度 - 根據難度調整
                self.speed_increase_timer += 1
                speed_increase_interval = max(
                    120, 600 - self.difficulty_level * 80
                )  # 更激進的速度提升
                if self.speed_increase_timer >= speed_increase_interval:
                    self.game_speed += self.speed_increase_rate
                    self.speed_increase_timer = 0
                    print(f"🚀 遊戲速度提升！當前速度: {self.game_speed:.1f}")

                # 生成障礙物和雲朵
                self.spawn_obstacle()
                self.spawn_cloud()

                # 更新障礙物
                for obstacle in self.obstacles[:]:
                    obstacle.speed = self.game_speed
                    obstacle.update()
                    if obstacle.x + obstacle.width < 0:
                        self.obstacles.remove(obstacle)
                        # 根據難度給予不同分數
                        score_multiplier = {
                            DIFFICULTY_EASY: 1,
                            DIFFICULTY_MEDIUM: 1.5,
                            DIFFICULTY_HARD: 2,
                            DIFFICULTY_NIGHTMARE: 4,
                            DIFFICULTY_HELL: 6,
                        }
                        self.score += int(10 * score_multiplier[self.difficulty_level])

                # 更新雲朵
                for cloud in self.clouds[:]:
                    cloud.update()
                    if cloud.x + 40 < 0:
                        self.clouds.remove(cloud)

                # 檢查碰撞
                if self.check_collision():
                    self.game_over = True
                    if self.score > self.high_score:
                        self.high_score = self.score
                        print(f"🎉 新紀錄！分數: {self.high_score}")

            # 減少螢幕震動
            if self.screen_shake > 0:
                self.screen_shake -= 1

    def apply_nightmare_effects(self):
        """應用噩夢和地獄模式的特殊效果"""
        if not hasattr(self, "dinosaur") or not self.dinosaur:
            return

        # 螢幕閃爍效果（噩夢模式）
        if self.difficulty_level >= DIFFICULTY_NIGHTMARE:
            if random.randint(1, 300) == 1:  # 隨機閃爍
                self.screen_shake = random.randint(5, 15)

        # 重力異常（噩夢模式）
        if self.difficulty_level >= DIFFICULTY_NIGHTMARE:
            if random.randint(1, 600) == 1:  # 每10秒大約一次
                if hasattr(self.dinosaur, "gravity_reversal_time"):
                    self.dinosaur.gravity_reversal_time = random.randint(
                        180, 300
                    )  # 3-5秒
                    print("⚠️ 重力異常發生！")

        # 地獄模式專屬效果
        if False:  # 地獄難度已移除
            # 控制反轉
            if random.randint(1, 900) == 1:  # 更頻繁的混亂
                if hasattr(self.dinosaur, "control_inversion_time"):
                    self.dinosaur.control_inversion_time = random.randint(
                        120, 240
                    )  # 2-4秒
                    print("💀 控制反轉！上下顛倒！")

            # 能力隨機故障
            if random.randint(1, 1200) == 1:
                if hasattr(self.dinosaur, "ability_malfunction_time"):
                    self.dinosaur.ability_malfunction_time = random.randint(
                        180, 360
                    )  # 3-6秒
                    print("💀 能力故障！衝刺和護盾失效！")

            # 時間扭曲效果
            if random.randint(1, 800) == 1:
                if hasattr(self.dinosaur, "nightmare_effects"):
                    time_factor = random.choice([0.5, 1.5, 2.0])  # 時間變慢或變快
                    self.dinosaur.nightmare_effects["time_distortion"] = time_factor
                    print(f"💀 時空扭曲！時間流速: {time_factor}x")

            # 每隔一段時間恢復正常時間流速
            if random.randint(1, 600) == 1:
                if hasattr(self.dinosaur, "nightmare_effects"):
                    self.dinosaur.nightmare_effects["time_distortion"] = 1.0

    def draw_game_info(self):
        """
        繪製遊戲資訊文字 - 支持動態縮放
        """
        # 計算動態位置
        margin = int(self.screen_width * 0.0125)  # 1.25% 的螢幕寬度作為邊距
        line_height = int(self.screen_height * 0.04)  # 4% 的螢幕高度作為行高

        # 分數顯示
        score_text = f"分數: {self.score}"
        score_surface = self.font_medium.render(score_text, True, self.colors["BLACK"])
        self.screen.blit(score_surface, (margin, margin))

        # 最高分顯示
        if self.high_score > 0:
            high_score_text = f"最高分: {self.high_score}"
            high_score_surface = self.font_small.render(
                high_score_text, True, self.colors["PURPLE"]
            )
            self.screen.blit(high_score_surface, (margin, margin + line_height))

        # 遊戲速度顯示
        speed_text = f"速度: {self.game_speed:.1f}x"
        speed_surface = self.font_small.render(speed_text, True, self.colors["BLUE"])
        self.screen.blit(speed_surface, (margin, margin + line_height * 2))

        # 難度等級顯示
        difficulty_names = {
            DIFFICULTY_EASY: "簡單",
            DIFFICULTY_MEDIUM: "中等",
            DIFFICULTY_HARD: "困難",
            DIFFICULTY_NIGHTMARE: "噩夢",
        }
        difficulty_text = f"難度: {difficulty_names.get(self.difficulty_level, '未知')}"
        difficulty_color = (
            self.colors["RED"]
            if self.difficulty_level >= DIFFICULTY_HELL
            else self.colors["PURPLE"]
        )
        difficulty_surface = self.font_small.render(
            difficulty_text, True, difficulty_color
        )
        self.screen.blit(difficulty_surface, (margin, margin + line_height * 3))

        # 連擊數顯示
        current_line = 4
        if self.combo_count > 0:
            combo_text = f"連擊: {self.combo_count}"
            combo_surface = self.font_small.render(
                combo_text, True, self.colors["ORANGE"]
            )
            self.screen.blit(
                combo_surface, (margin, margin + line_height * current_line)
            )
            current_line += 1

        # 恐龍狀態顯示
        if self.dinosaur and self.dinosaur.has_shield:
            shield_text = f"護盾: {self.dinosaur.shield_time // 60 + 1}秒"
            shield_surface = self.font_small.render(
                shield_text, True, self.colors["LIGHT_BLUE"]
            )
            self.screen.blit(
                shield_surface, (margin, margin + line_height * current_line)
            )
            current_line += 1

        if self.dinosaur and self.dinosaur.dash_cooldown > 0:
            dash_text = f"衝刺冷卻: {self.dinosaur.dash_cooldown // 60 + 1}秒"
            dash_surface = self.font_small.render(
                dash_text, True, self.colors["YELLOW"]
            )
            self.screen.blit(
                dash_surface, (margin, margin + line_height * current_line)
            )
            current_line += 1

        # 噩夢/地獄模式效果顯示
        if self.dinosaur and self.difficulty_level >= DIFFICULTY_NIGHTMARE:
            if (
                hasattr(self.dinosaur, "is_gravity_reversed")
                and self.dinosaur.is_gravity_reversed
            ):
                gravity_text = "⚠️ 重力反轉中！"
                gravity_surface = self.font_small.render(
                    gravity_text, True, self.colors["RED"]
                )
                self.screen.blit(
                    gravity_surface, (margin, margin + line_height * current_line)
                )
                current_line += 1

            if (
                hasattr(self.dinosaur, "is_control_inverted")
                and self.dinosaur.is_control_inverted
            ):
                control_text = "💀 控制反轉中！"
                control_surface = self.font_small.render(
                    control_text, True, self.colors["RED"]
                )
                self.screen.blit(
                    control_surface, (margin, margin + line_height * current_line)
                )
                current_line += 1

            if (
                hasattr(self.dinosaur, "ability_malfunction_time")
                and self.dinosaur.ability_malfunction_time > 0
            ):
                malfunction_text = "💀 能力故障中！"
                malfunction_surface = self.font_small.render(
                    malfunction_text, True, self.colors["RED"]
                )
                self.screen.blit(
                    malfunction_surface, (margin, margin + line_height * current_line)
                )
                current_line += 1

    def draw_game_over_screen(self):
        """
        繪製遊戲結束畫面 - 參考 class3-3.py 的居中文字處理
        """
        # 半透明背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(self.colors["BLACK"])
        self.screen.blit(overlay, (0, 0))

        # 遊戲結束標題
        game_over_text = "遊戲結束！Game Over!"
        game_over_surface = self.font_large.render(
            game_over_text, True, self.colors["RED"]
        )
        game_over_rect = game_over_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)
        )
        self.screen.blit(game_over_surface, game_over_rect)

        # 分數顯示
        final_score_text = f"最終分數: {self.score}"
        final_score_surface = self.font_medium.render(
            final_score_text, True, self.colors["YELLOW"]
        )
        final_score_rect = final_score_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
        )
        self.screen.blit(final_score_surface, final_score_rect)

        # 最高分顯示
        if self.score == self.high_score and self.high_score > 0:
            new_record_text = "🎉 新紀錄！New Record!"
            new_record_surface = self.font_medium.render(
                new_record_text, True, self.colors["PINK"]
            )
            new_record_rect = new_record_surface.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)
            )
            self.screen.blit(new_record_surface, new_record_rect)

        # 重新開始提示
        restart_text = "空白鍵: 重新開始同難度  |  ESC: 返回主選單"
        restart_surface = self.font_medium.render(
            restart_text, True, self.colors["WHITE"]
        )
        restart_rect = restart_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
        )
        self.screen.blit(restart_surface, restart_rect)

    def draw_start_instructions(self):
        """
        繪製開始遊戲的操作說明 - 支持動態縮放
        """
        if not self.game_over and self.score == 0:
            # 計算動態位置
            center_x = SCREEN_WIDTH // 2
            instruction_y = int(SCREEN_HEIGHT * 0.15)  # 15% 螢幕高度
            line_spacing = int(SCREEN_HEIGHT * 0.04)  # 4% 螢幕高度間距

            # 主要操作說明
            instruction_text = (
                "↑/空白鍵:跳躍  ↓/S鍵:蹲下  X:衝刺  Z:護盾  F11:全螢幕  ESC:返回選單"
            )
            instruction_surface = self.font_medium.render(
                instruction_text, True, self.colors["GRAY"]
            )
            instruction_rect = instruction_surface.get_rect(
                center=(center_x, instruction_y)
            )
            self.screen.blit(instruction_surface, instruction_rect)

            # 障礙物說明 (根據難度顯示不同提示)
            if self.difficulty_level <= DIFFICULTY_MEDIUM:
                obstacles_text = "🌵 仙人掌需跳躍  🪨 石頭可走過  🐦 鳥類需蹲下"
            else:
                obstacles_text = "⚡ 高難度！注意隱形、爆炸、移動障礙物！"

            obstacles_surface = self.font_small.render(
                obstacles_text, True, self.colors["BLUE"]
            )
            obstacles_rect = obstacles_surface.get_rect(
                center=(center_x, instruction_y + line_spacing)
            )
            self.screen.blit(obstacles_surface, obstacles_rect)

            # 難度提示
            difficulty_names = {
                DIFFICULTY_EASY: "輕鬆享受遊戲樂趣！",
                DIFFICULTY_MEDIUM: "保持專注，挑戰自我！",
                DIFFICULTY_HARD: "高速挑戰，考驗反應！",
                DIFFICULTY_NIGHTMARE: "極限模式，生存挑戰！",
            }
            subtitle_text = (
                f"當前難度: {difficulty_names.get(self.difficulty_level, '未知難度')}"
            )
            subtitle_surface = self.font_small.render(
                subtitle_text, True, self.colors["GREEN"]
            )
            subtitle_rect = subtitle_surface.get_rect(
                center=(center_x, instruction_y + line_spacing * 2)
            )
            self.screen.blit(subtitle_surface, subtitle_rect)

    def draw(self):
        """
        主要繪製方法 - 根據遊戲狀態繪製不同內容
        """
        if self.game_state == GAME_STATE_MENU:
            # 繪製主選單
            self.menu_system.draw(self.screen)
        elif self.game_state == GAME_STATE_PLAYING:
            # 螢幕震動效果
            screen_offset_x = (
                random.randint(-self.screen_shake, self.screen_shake)
                if self.screen_shake > 0
                else 0
            )
            screen_offset_y = (
                random.randint(-self.screen_shake, self.screen_shake)
                if self.screen_shake > 0
                else 0
            )

            # 清空螢幕 - 根據難度調整背景色
            bg_colors = {
                DIFFICULTY_EASY: self.colors["WHITE"],
                DIFFICULTY_MEDIUM: (250, 250, 250),
                DIFFICULTY_HARD: (240, 240, 240),
                DIFFICULTY_NIGHTMARE: (200, 200, 200),
            }
            current_bg = bg_colors.get(self.difficulty_level, self.colors["WHITE"])

            # 地獄模式的動態背景效果
            if False:  # 地獄難度已移除
                # 地獄火焰效果
                flame_intensity = int(40 * math.sin(pygame.time.get_ticks() * 0.01))
                current_bg = (80 + flame_intensity, flame_intensity // 4, 0)

            self.screen.fill(current_bg)

            # 畫地面
            pygame.draw.line(
                self.screen,
                self.colors["BLACK"],
                (screen_offset_x, GROUND_HEIGHT + screen_offset_y),
                (SCREEN_WIDTH + screen_offset_x, GROUND_HEIGHT + screen_offset_y),
                2,
            )

            # 畫雲朵
            for cloud in self.clouds:
                cloud.draw(self.screen)

            # 畫恐龍
            if self.dinosaur:
                self.dinosaur.draw(self.screen)

            # 畫障礙物
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)

            # 顯示遊戲資訊
            self.draw_game_info()

            # 顯示控制說明 (只在遊戲開始時)
            if self.score == 0 and not self.game_over:
                self.draw_start_instructions()

            # 遊戲結束畫面
            if self.game_over:
                self.draw_game_over_screen()

        # 更新顯示
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    print("=" * 70)
    print("🦕 超級進階小恐龍遊戲啟動！💀 地獄版本 💀")
    print("=" * 70)
    print("🎮 全新特色：")
    print("   • 五種難度等級選擇 - 從簡單到地獄級")
    print("   • 主選單系統 - 精美的難度選擇介面")
    print("   • 動態速度調整 - 根據難度智能調節")
    print("   • 進階障礙物系統 - 隱形、爆炸、移動、分裂障礙物")
    print("   • 地獄級新障礙物 - 重力炸彈、時空扭曲、惡魔傳送門")
    print("   • 恐龍新能力 - 衝刺、護盾、二段跳")
    print("   • 連擊系統 - 獎勵技巧性操作")
    print("   • 螢幕震動特效 - 增強遊戲感受")
    print("   • 💀 噩夢效果 - 重力異常、控制反轉、能力故障")
    print("   • 🖥️ 全螢幕支持 - 自適應任何螢幕大小")
    print()
    print("🎯 難度等級：")
    print("   • 簡單 (Easy) - 適合新手，慢節奏遊戲")
    print("   • 中等 (Medium) - 標準難度，平衡的挑戰")
    print("   • 困難 (Hard) - 快節奏，需要高度技巧")
    print("   • 噩夢 (Nightmare) - 超極速+重力異常+螢幕閃爍")
    print("   • 💀 地獄 (HELL) - 控制反轉+時空扭曲+惡魔障礙物")
    print()
    print("🕹️ 操作說明：")
    print("   • ↑方向鍵/空白鍵：跳躍 (可二段跳)")
    print("   • ↓方向鍵/S鍵：蹲下")
    print("   • X鍵：衝刺 (有冷卻時間)")
    print("   • Z鍵：護盾 (短時間無敵)")
    print("   • ESC鍵：返回主選單")
    print("   • F11鍵：切換全螢幕模式")
    print("   • Alt+F4：退出遊戲")
    print("   • ⚠️ 地獄模式：控制可能隨時反轉！")
    print()
    print("🖥️ 顯示功能：")
    print("   • 支持全螢幕模式 (F11切換)")
    print("   • 支持視窗大小調整")
    print("   • 自動適應不同解析度")
    print("   • 動態UI縮放")
    print("   • 保持最佳遊戲比例")
    print()
    print("🌟 障礙物類型：")
    print("   • 基礎障礙物：仙人掌、石頭、飛鳥")
    print("   • 進階障礙物：雙重、上下移動、分裂")
    print("   • 💀 地獄障礙物：重力炸彈、時空扭曲、地獄尖刺、惡魔傳送門")
    print()
    print("🔥 噩夢/地獄模式特殊效果：")
    print("   • 重力異常：重力可能突然反轉")
    print("   • 控制反轉：上下鍵功能隨機顛倒")
    print("   • 能力故障：衝刺和護盾隨機失效")
    print("   • 時空扭曲：遊戲時間流速改變")
    print("   • 螢幕閃爍：視覺干擾效果")
    print()
    print("💡 生存技巧：")
    print("   • 合理使用衝刺和護盾能力")
    print("   • 觀察障礙物預警，提前做好準備")
    print("   • 💀 地獄模式：適應控制反轉，保持冷靜")
    print("   • 利用連擊系統獲得更高分數")
    print("   • 在重力異常時快速調整策略")
    print()
    print("🎯 準備好挑戰地獄級的極限了嗎？")
    print("💀 警告：地獄模式可能會讓您懷疑人生！")
    print("=" * 70)

    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"❌ 遊戲發生錯誤: {e}")
        print("請確保已安裝 pygame：pip install pygame")
        sys.exit(1)
