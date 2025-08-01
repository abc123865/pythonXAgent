import pygame
import math
import random
import json
from typing import List, Tuple, Optional

# 初始化 Pygame
pygame.init()

# 常數定義
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# 顏色定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


class Vector2:
    """2D 向量類別"""

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float):
        return Vector2(self.x / scalar, self.y / scalar)

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def normalized(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)
        return Vector2(self.x / mag, self.y / mag)

    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y

    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)


class Physics:
    """物理系統"""

    GRAVITY = Vector2(0, 0.6)  # 減少重力，讓攀爬更容易
    AIR_RESISTANCE = 0.998  # 減少空氣阻力，保持動量
    FRICTION = 0.9  # 稍微減少摩擦力

    @staticmethod
    def apply_gravity(velocity: Vector2) -> Vector2:
        return velocity + Physics.GRAVITY

    @staticmethod
    def apply_air_resistance(velocity: Vector2) -> Vector2:
        return velocity * Physics.AIR_RESISTANCE

    @staticmethod
    def apply_friction(velocity: Vector2) -> Vector2:
        return velocity * Physics.FRICTION


class Terrain:
    """地形類別"""

    def __init__(self):
        self.platforms = []
        self.obstacles = []
        self.generate_terrain()

    def generate_terrain(self):
        """生成地形 - 重新設計更長更適合錘子攀爬的地形"""
        # 地面平台 - 擴展寬度
        self.platforms.append(pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH * 3, 50))

        # 第一段：起始練習區域
        self.platforms.append(pygame.Rect(200, SCREEN_HEIGHT - 120, 150, 20))
        self.platforms.append(pygame.Rect(450, SCREEN_HEIGHT - 180, 120, 20))
        self.platforms.append(pygame.Rect(650, SCREEN_HEIGHT - 120, 100, 20))
        self.platforms.append(pygame.Rect(850, SCREEN_HEIGHT - 200, 130, 20))

        # 第二段：初級攀爬 - 較大的平台
        self.platforms.append(pygame.Rect(300, SCREEN_HEIGHT - 280, 200, 25))
        self.platforms.append(pygame.Rect(600, SCREEN_HEIGHT - 380, 180, 25))
        self.platforms.append(pygame.Rect(150, SCREEN_HEIGHT - 480, 200, 25))
        self.platforms.append(pygame.Rect(800, SCREEN_HEIGHT - 450, 150, 25))
        self.platforms.append(pygame.Rect(1100, SCREEN_HEIGHT - 350, 160, 25))

        # 第三段：中級攀爬 - 中等平台
        self.platforms.append(pygame.Rect(450, SCREEN_HEIGHT - 580, 150, 20))
        self.platforms.append(pygame.Rect(200, SCREEN_HEIGHT - 680, 120, 20))
        self.platforms.append(pygame.Rect(700, SCREEN_HEIGHT - 650, 150, 20))
        self.platforms.append(pygame.Rect(950, SCREEN_HEIGHT - 580, 130, 20))
        self.platforms.append(pygame.Rect(50, SCREEN_HEIGHT - 780, 140, 20))
        self.platforms.append(pygame.Rect(1200, SCREEN_HEIGHT - 750, 120, 20))

        # 第四段：高級攀爬 - 小平台
        self.platforms.append(pygame.Rect(100, SCREEN_HEIGHT - 880, 80, 15))
        self.platforms.append(pygame.Rect(400, SCREEN_HEIGHT - 980, 100, 15))
        self.platforms.append(pygame.Rect(650, SCREEN_HEIGHT - 1080, 80, 15))
        self.platforms.append(pygame.Rect(900, SCREEN_HEIGHT - 950, 90, 15))
        self.platforms.append(pygame.Rect(300, SCREEN_HEIGHT - 1180, 110, 15))
        self.platforms.append(pygame.Rect(1000, SCREEN_HEIGHT - 1100, 85, 15))

        # 第五段：專家級攀爬 - 更多挑戰
        self.platforms.append(pygame.Rect(150, SCREEN_HEIGHT - 1280, 70, 15))
        self.platforms.append(pygame.Rect(550, SCREEN_HEIGHT - 1380, 90, 15))
        self.platforms.append(pygame.Rect(850, SCREEN_HEIGHT - 1450, 75, 15))
        self.platforms.append(pygame.Rect(200, SCREEN_HEIGHT - 1550, 100, 15))
        self.platforms.append(pygame.Rect(700, SCREEN_HEIGHT - 1650, 80, 15))

        # 第六段：終極挑戰
        self.platforms.append(pygame.Rect(400, SCREEN_HEIGHT - 1750, 60, 15))
        self.platforms.append(pygame.Rect(100, SCREEN_HEIGHT - 1850, 80, 15))
        self.platforms.append(pygame.Rect(600, SCREEN_HEIGHT - 1950, 70, 15))

        # 最終平台
        self.platforms.append(
            pygame.Rect(300, SCREEN_HEIGHT - 2050, 150, 25)
        )  # 終點平台

        # 攀爬輔助障礙物（岩壁等） - 增加更多
        # 第一區域的岩壁
        self.obstacles.append(pygame.Rect(580, SCREEN_HEIGHT - 250, 30, 150))
        self.obstacles.append(pygame.Rect(120, SCREEN_HEIGHT - 550, 25, 200))
        self.obstacles.append(pygame.Rect(750, SCREEN_HEIGHT - 450, 35, 180))
        self.obstacles.append(pygame.Rect(1050, SCREEN_HEIGHT - 400, 30, 200))

        # 第二區域的岩壁
        self.obstacles.append(pygame.Rect(350, SCREEN_HEIGHT - 850, 40, 250))
        self.obstacles.append(pygame.Rect(800, SCREEN_HEIGHT - 750, 35, 200))
        self.obstacles.append(pygame.Rect(150, SCREEN_HEIGHT - 950, 30, 180))
        self.obstacles.append(pygame.Rect(1150, SCREEN_HEIGHT - 900, 45, 300))

        # 第三區域的岩壁
        self.obstacles.append(pygame.Rect(250, SCREEN_HEIGHT - 1350, 50, 400))
        self.obstacles.append(pygame.Rect(650, SCREEN_HEIGHT - 1200, 40, 350))
        self.obstacles.append(pygame.Rect(950, SCREEN_HEIGHT - 1300, 35, 280))

        # 第四區域的岩壁
        self.obstacles.append(pygame.Rect(150, SCREEN_HEIGHT - 1650, 45, 350))
        self.obstacles.append(pygame.Rect(750, SCREEN_HEIGHT - 1800, 40, 400))
        self.obstacles.append(pygame.Rect(450, SCREEN_HEIGHT - 1900, 50, 300))

        # 一些小的攀爬點
        self.obstacles.append(pygame.Rect(500, SCREEN_HEIGHT - 350, 15, 80))
        self.obstacles.append(pygame.Rect(250, SCREEN_HEIGHT - 750, 20, 100))
        self.obstacles.append(pygame.Rect(1000, SCREEN_HEIGHT - 650, 18, 90))
        self.obstacles.append(pygame.Rect(450, SCREEN_HEIGHT - 1250, 22, 120))
        self.obstacles.append(pygame.Rect(800, SCREEN_HEIGHT - 1550, 20, 110))
        self.obstacles.append(pygame.Rect(350, SCREEN_HEIGHT - 1750, 25, 100))

    def draw(self, screen: pygame.Surface):
        """繪製地形"""
        # 繪製平台
        for platform in self.platforms:
            pygame.draw.rect(screen, BROWN, platform)
            pygame.draw.rect(screen, DARK_GRAY, platform, 2)

        # 繪製障礙物
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, GRAY, obstacle)
            pygame.draw.rect(screen, BLACK, obstacle, 2)

    def check_collision(self, rect: pygame.Rect) -> List[pygame.Rect]:
        """檢查碰撞"""
        collisions = []
        for platform in self.platforms + self.obstacles:
            if rect.colliderect(platform):
                collisions.append(platform)
        return collisions


class Hammer:
    """錘子類別 - 實現真正的Getting Over It擺動機制"""

    def __init__(self, player_pos: Vector2):
        self.length = 120  # 固定長度
        self.angle = 0
        self.player_pos = player_pos
        self.tip_pos = Vector2()
        self.target_pos = Vector2()  # 滑鼠目標位置
        self.is_hooked = False  # 是否掛住了
        self.hook_point = Vector2()  # 掛住的點
        self.hook_surface = None  # 掛住的表面
        self.swing_force_multiplier = 1.0  # 擺動力量倍數
        self.update_tip_position()

    def update_tip_position(self):
        """更新錘子尖端位置"""
        self.tip_pos.x = self.player_pos.x + math.cos(self.angle) * self.length
        self.tip_pos.y = self.player_pos.y + math.sin(self.angle) * self.length

    def check_hammer_collision(
        self, terrain: Terrain, target_tip: Vector2
    ) -> Tuple[bool, Vector2]:
        """檢查錘子本身是否會碰撞（只檢查錘子頭部，不檢查繩子路徑）"""
        # 只檢查錘子頭部是否碰撞
        tip_rect = pygame.Rect(target_tip.x - 8, target_tip.y - 8, 16, 16)
        collisions = terrain.check_collision(tip_rect)

        if collisions:
            # 錘子頭部碰撞，找一個安全的位置
            # 嘗試在碰撞表面的邊緣找到安全位置
            for collision in collisions:
                # 計算從玩家到目標的方向
                direction_x = target_tip.x - self.player_pos.x
                direction_y = target_tip.y - self.player_pos.y
                direction_length = math.sqrt(
                    direction_x * direction_x + direction_y * direction_y
                )

                if direction_length > 0:
                    # 正規化方向向量
                    dir_x = direction_x / direction_length
                    dir_y = direction_y / direction_length

                    # 嘗試在碰撞物體的各個邊緣找安全位置
                    safe_positions = [
                        Vector2(collision.left - 12, target_tip.y),  # 左邊
                        Vector2(collision.right + 12, target_tip.y),  # 右邊
                        Vector2(target_tip.x, collision.top - 12),  # 上邊
                        Vector2(target_tip.x, collision.bottom + 12),  # 下邊
                    ]

                    # 選擇最接近目標位置的安全位置
                    best_pos = safe_positions[0]
                    best_distance = float("inf")

                    for pos in safe_positions:
                        distance = math.sqrt(
                            (pos.x - target_tip.x) ** 2 + (pos.y - target_tip.y) ** 2
                        )
                        # 檢查這個位置是否安全
                        check_rect = pygame.Rect(pos.x - 8, pos.y - 8, 16, 16)
                        if (
                            not terrain.check_collision(check_rect)
                            and distance < best_distance
                        ):
                            best_pos = pos
                            best_distance = distance

                    return True, best_pos

        return False, target_tip

    def update(self, mouse_pos: Tuple[int, int], player_pos: Vector2, terrain: Terrain):
        """更新錘子狀態"""
        self.player_pos = player_pos
        self.target_pos.x = mouse_pos[0]
        self.target_pos.y = mouse_pos[1]

        # 計算滑鼠到玩家的角度
        dx = mouse_pos[0] - player_pos.x
        dy = mouse_pos[1] - player_pos.y
        target_angle = math.atan2(dy, dx)

        # 計算目標錘子尖端位置
        target_tip_x = player_pos.x + math.cos(target_angle) * self.length
        target_tip_y = player_pos.y + math.sin(target_angle) * self.length
        target_tip = Vector2(target_tip_x, target_tip_y)

        # 只檢查錘子本身是否碰撞（繩子可以穿牆）
        has_collision, safe_tip_pos = self.check_hammer_collision(terrain, target_tip)

        if has_collision:
            # 錘子頭部碰撞，使用安全位置
            self.tip_pos = safe_tip_pos
            # 重新計算角度和長度（繩子可以穿牆，所以保持連接）
            dx = safe_tip_pos.x - player_pos.x
            dy = safe_tip_pos.y - player_pos.y
            self.angle = math.atan2(dy, dx)
            # 長度根據實際距離調整
            actual_distance = math.sqrt(dx * dx + dy * dy)
            if actual_distance > 0:
                self.length = actual_distance
        else:
            # 沒有碰撞，正常更新
            self.angle = target_angle
            self.length = 120  # 恢復正常長度
            self.update_tip_position()

    def apply_swing_force(
        self, terrain: Terrain, is_pressing: bool, mouse_direction: Vector2
    ) -> Tuple[Vector2, bool]:
        """應用擺動力學 - 繩子可以穿牆的Getting Over It機制，回傳力和是否戳地"""
        force = Vector2()
        is_pogo_jump = False  # 是否進行戳地跳躍

        # 檢查錘子是否掛住了某個表面
        tip_rect = pygame.Rect(self.tip_pos.x - 8, self.tip_pos.y - 8, 16, 16)
        collisions = terrain.check_collision(tip_rect)

        if collisions and is_pressing:
            self.is_hooked = True
            self.hook_point = Vector2(self.tip_pos.x, self.tip_pos.y)
            self.hook_surface = collisions[0]

            # 計算從掛點到玩家的向量（繩子可以穿牆，直線距離）
            hook_to_player = Vector2(
                self.player_pos.x - self.hook_point.x,
                self.player_pos.y - self.hook_point.y,
            )

            # 計算當前擺動半徑（繩子的直線長度）
            current_radius = hook_to_player.magnitude()

            if current_radius > 0:
                # 計算玩家相對於掛點的角度
                current_angle = math.atan2(hook_to_player.y, hook_to_player.x)

                # 計算滑鼠方向相對於掛點的目標角度
                mouse_to_hook = Vector2(
                    mouse_direction.x - self.hook_point.x,
                    mouse_direction.y - self.hook_point.y,
                )

                if mouse_to_hook.magnitude() > 0:
                    target_angle = math.atan2(mouse_to_hook.y, mouse_to_hook.x)

                    # 計算角度差
                    angle_diff = target_angle - current_angle

                    # 正規化角度差到 -π 到 π
                    while angle_diff > math.pi:
                        angle_diff -= 2 * math.pi
                    while angle_diff < -math.pi:
                        angle_diff += 2 * math.pi

                    # 增強切線方向的力（因為繩子可以穿牆，擺動更自由）
                    tangent_force = angle_diff * 1.2  # 大幅增加力量

                    # 切線方向
                    tangent_x = -math.sin(current_angle)
                    tangent_y = math.cos(current_angle)

                    force.x = tangent_x * tangent_force
                    force.y = tangent_y * tangent_force

                    # 繩子穿牆特性：更強的向上甩力
                    if hook_to_player.y > 0:  # 玩家在掛點下方
                        # 增強向上的甩力
                        upward_boost = abs(tangent_force) * 1.5
                        if angle_diff < 0:  # 向左甩
                            force.y -= upward_boost
                        elif angle_diff > 0:  # 向右甩
                            force.y -= upward_boost

                    # 繩子拉力效果（更強，因為不受牆壁阻擋）
                    radial_force = -0.4  # 大幅增強向掛點方向的力
                    radial_x = hook_to_player.x / current_radius
                    radial_y = hook_to_player.y / current_radius

                    force.x += radial_x * radial_force
                    force.y += radial_y * radial_force

                    # 額外的穿牆優勢：如果玩家和掛點之間有牆，增加力量
                    # 檢查是否有牆壁阻擋
                    steps = 10
                    wall_blocked = False
                    for i in range(1, steps):
                        ratio = i / steps
                        check_x = (
                            self.player_pos.x
                            + (self.hook_point.x - self.player_pos.x) * ratio
                        )
                        check_y = (
                            self.player_pos.y
                            + (self.hook_point.y - self.player_pos.y) * ratio
                        )
                        check_rect = pygame.Rect(check_x - 5, check_y - 5, 10, 10)
                        if terrain.check_collision(check_rect):
                            wall_blocked = True
                            break

                    # 如果繩子穿過牆壁，給予額外力量獎勵
                    if wall_blocked:
                        force.x *= 1.3
                        force.y *= 1.3

        else:
            self.is_hooked = False
            self.hook_surface = None

            # 錘子沒有掛住時的邏輯
            if is_pressing:
                # 計算滑鼠相對於玩家的方向
                dx = mouse_direction.x - self.player_pos.x
                dy = mouse_direction.y - self.player_pos.y
                distance = math.sqrt(dx * dx + dy * dy)

                if distance > 0:
                    # 檢查是否向下戳地（向下戳地跳躍技巧）
                    # 如果滑鼠在玩家下方且錘子碰到了地面/平台
                    if dy > 30 and collisions:  # 滑鼠在玩家下方30像素以上
                        # 向下戳地跳躍！
                        is_pogo_jump = True  # 標記戳地跳躍
                        pogo_force = 2.5  # 戳地跳躍力量
                        
                        # 計算戳地的反作用力
                        # 主要向上，稍微向滑鼠相反方向
                        force.y = -pogo_force  # 強力向上推
                        force.x = -(dx / distance) * (pogo_force * 0.3)  # 反向水平力
                        
                        # 額外的向上推力，模擬戳地反彈
                        if abs(dx) < 50:  # 如果滑鼠幾乎在玩家正下方
                            force.y = -pogo_force * 1.2  # 更強的垂直推力
                    
                    else:
                        # 普通的空中移動力
                        force.x = (dx / distance) * 0.3
                        force.y = (dy / distance) * 0.3

        return force, is_pogo_jump

    def draw(self, screen: pygame.Surface):
        """繪製錘子和繩子"""
        # 繩子（總是從玩家直接連到錘子，可以穿牆）
        if self.is_hooked:
            rope_color = RED  # 掛住時變紅色
            rope_thickness = 4
        else:
            rope_color = (139, 69, 19)  # 棕色
            rope_thickness = 3

        # 繪製繩子 - 直線連接，可以穿牆
        pygame.draw.line(
            screen,
            rope_color,
            (int(self.player_pos.x), int(self.player_pos.y)),
            (int(self.tip_pos.x), int(self.tip_pos.y)),
            rope_thickness,
        )

        # 錘子頭（實體，不能穿牆）
        head_size = 12
        pygame.draw.circle(
            screen, GRAY, (int(self.tip_pos.x), int(self.tip_pos.y)), head_size
        )
        pygame.draw.circle(
            screen, BLACK, (int(self.tip_pos.x), int(self.tip_pos.y)), head_size, 2
        )

        # 如果錘子掛住了，顯示特效
        if self.is_hooked:
            pygame.draw.circle(
                screen,
                YELLOW,
                (int(self.tip_pos.x), int(self.tip_pos.y)),
                head_size + 5,
                3,
            )
            # 繪製掛點指示器
            pygame.draw.circle(
                screen,
                YELLOW,
                (int(self.hook_point.x), int(self.hook_point.y)),
                8,
                2,
            )


class Player:
    """玩家類別"""

    def __init__(self, x: float, y: float):
        self.position = Vector2(x, y)
        self.velocity = Vector2()
        self.size = 30
        self.rect = pygame.Rect(
            x - self.size // 2, y - self.size // 2, self.size, self.size
        )
        self.hammer = Hammer(self.position)
        self.on_ground = False
        self.highest_y = y  # 記錄最高位置
        self.is_pogo_jumping = False  # 是否正在戳地跳躍

    def update(self, mouse_pos: Tuple[int, int], mouse_pressed: bool, terrain: Terrain):
        """更新玩家狀態"""
        # 更新錘子
        self.hammer.update(mouse_pos, self.position, terrain)

        # 處理錘子擺動力學
        mouse_world_pos = Vector2(mouse_pos[0], mouse_pos[1])
        swing_force, is_pogo_jump = self.hammer.apply_swing_force(
            terrain, mouse_pressed, mouse_world_pos
        )

        # 保存戳地跳躍狀態供外部使用
        self.is_pogo_jumping = is_pogo_jump and mouse_pressed

        if mouse_pressed:
            self.velocity = self.velocity + swing_force

        # 應用物理
        self.velocity = Physics.apply_gravity(self.velocity)
        self.velocity = Physics.apply_air_resistance(self.velocity)

        # 如果在地面上應用摩擦力
        if self.on_ground:
            self.velocity = Physics.apply_friction(self.velocity)

        # 更新位置
        self.position = self.position + self.velocity

        # 更新碰撞盒
        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

        # 碰撞檢測
        self.handle_collisions(terrain)

        # 記錄最高位置
        if self.position.y < self.highest_y:
            self.highest_y = self.position.y

        # 邊界檢查
        if self.position.x < -50:  # 允許一些邊界外的移動
            self.position.x = -50
            self.velocity.x = max(0, self.velocity.x)  # 只阻止繼續向左
        elif self.position.x > SCREEN_WIDTH + 50:
            self.position.x = SCREEN_WIDTH + 50
            self.velocity.x = min(0, self.velocity.x)  # 只阻止繼續向右

        # 如果掉到底部太遠，重置位置
        if self.position.y > SCREEN_HEIGHT + 300:
            self.reset_position()

    def handle_collisions(self, terrain: Terrain):
        """處理碰撞"""
        self.on_ground = False
        collisions = terrain.check_collision(self.rect)

        for collision in collisions:
            # 從上方碰撞（著陸）
            if self.velocity.y > 0 and self.rect.bottom <= collision.top + 10:
                self.position.y = collision.top - self.size // 2
                self.velocity.y = 0
                self.on_ground = True

            # 從下方碰撞（撞頭）
            elif self.velocity.y < 0 and self.rect.top >= collision.bottom - 10:
                self.position.y = collision.bottom + self.size // 2
                self.velocity.y = 0

            # 從左側碰撞
            elif self.velocity.x > 0 and self.rect.right <= collision.left + 10:
                self.position.x = collision.left - self.size // 2
                self.velocity.x = 0

            # 從右側碰撞
            elif self.velocity.x < 0 and self.rect.left >= collision.right - 10:
                self.position.x = collision.right + self.size // 2
                self.velocity.x = 0

        # 更新碰撞盒位置
        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

    def reset_position(self):
        """重置玩家位置"""
        self.position = Vector2(100, SCREEN_HEIGHT - 100)
        self.velocity = Vector2()
        self.hammer.is_hooked = False

    def draw(self, screen: pygame.Surface):
        """繪製玩家"""
        # 繪製罐子（玩家身體）
        pot_rect = pygame.Rect(
            self.position.x - self.size // 2,
            self.position.y - self.size // 2,
            self.size,
            self.size,
        )
        pygame.draw.ellipse(screen, ORANGE, pot_rect)
        pygame.draw.ellipse(screen, BLACK, pot_rect, 3)

        # 繪製人頭
        head_radius = 8
        head_y = self.position.y - self.size // 2 - 5
        pygame.draw.circle(
            screen, (255, 220, 177), (int(self.position.x), int(head_y)), head_radius
        )
        pygame.draw.circle(
            screen, BLACK, (int(self.position.x), int(head_y)), head_radius, 2
        )

        # 繪製眼睛
        pygame.draw.circle(
            screen, BLACK, (int(self.position.x - 3), int(head_y - 2)), 2
        )
        pygame.draw.circle(
            screen, BLACK, (int(self.position.x + 3), int(head_y - 2)), 2
        )

        # 繪製錘子
        self.hammer.draw(screen)


class Camera:
    """攝影機類別"""

    def __init__(self):
        self.offset = Vector2()
        self.target_offset = Vector2()
        self.smooth_factor = 0.1

    def update(self, target_pos: Vector2):
        """更新攝影機位置"""
        # 計算目標偏移
        self.target_offset.x = SCREEN_WIDTH // 2 - target_pos.x
        self.target_offset.y = SCREEN_HEIGHT // 2 - target_pos.y

        # 平滑移動
        self.offset.x += (self.target_offset.x - self.offset.x) * self.smooth_factor
        self.offset.y += (self.target_offset.y - self.offset.y) * self.smooth_factor

    def apply(self, pos: Vector2) -> Vector2:
        """應用攝影機偏移"""
        return Vector2(pos.x + self.offset.x, pos.y + self.offset.y)


class Game:
    """主遊戲類別"""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Getting Over It - Python Edition")
        self.clock = pygame.time.Clock()
        self.running = True

        # 遊戲物件
        self.player = Player(100, SCREEN_HEIGHT - 100)
        self.terrain = Terrain()
        self.camera = Camera()

        # 遊戲狀態
        self.start_time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 72)

        # 遊戲狀態標記
        self.game_completed = False
        self.completion_time = 0
        self.best_time = self.load_best_time()

        # 粒子效果
        self.particles = []

        # 音效（如果需要可以添加）
        self.sounds = {}

    def load_best_time(self):
        """載入最佳時間記錄"""
        try:
            with open("best_time.txt", "r") as f:
                return int(f.read().strip())
        except FileNotFoundError:
            return None

    def save_best_time(self, time):
        """保存最佳時間記錄"""
        with open("best_time.txt", "w") as f:
            f.write(str(time))

    def add_particle(self, x, y, color):
        """添加粒子效果"""
        for _ in range(5):
            particle = {
                "x": x + random.randint(-10, 10),
                "y": y + random.randint(-10, 10),
                "vx": random.randint(-3, 3),
                "vy": random.randint(-5, -1),
                "life": 30,
                "color": color,
            }
            self.particles.append(particle)

    def update_particles(self):
        """更新粒子效果"""
        for particle in self.particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["vy"] += 0.1  # 重力
            particle["life"] -= 1

            if particle["life"] <= 0:
                self.particles.remove(particle)

    def check_completion(self):
        """檢查是否完成遊戲"""
        if not self.game_completed and self.player.position.y <= SCREEN_HEIGHT - 2050:
            self.game_completed = True
            self.completion_time = (pygame.time.get_ticks() - self.start_time) // 1000

            # 檢查是否創造新記錄
            if self.best_time is None or self.completion_time < self.best_time:
                self.best_time = self.completion_time
                self.save_best_time(self.best_time)

            # 添加慶祝粒子效果
            for _ in range(20):
                self.add_particle(
                    self.player.position.x, self.player.position.y, YELLOW
                )

    def handle_events(self):
        """處理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.player.reset_position()
                    self.game_completed = False
                    self.start_time = pygame.time.get_ticks()
                    self.particles.clear()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and self.game_completed:
                    # 重新開始遊戲
                    self.player.reset_position()
                    self.game_completed = False
                    self.start_time = pygame.time.get_ticks()
                    self.particles.clear()

    def update(self):
        """更新遊戲狀態"""
        if not self.game_completed:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]

            # 將滑鼠位置轉換為世界坐標
            world_mouse_x = mouse_pos[0] - self.camera.offset.x
            world_mouse_y = mouse_pos[1] - self.camera.offset.y

            # 更新玩家
            self.player.update(
                (world_mouse_x, world_mouse_y), mouse_pressed, self.terrain
            )

            # 檢查完成條件
            self.check_completion()

        # 更新攝影機
        self.camera.update(self.player.position)

        # 更新粒子效果
        self.update_particles()

        # 添加錘子掛住粒子效果
        if self.player.hammer.is_hooked and random.randint(0, 15) == 0:
            self.add_particle(
                self.player.hammer.tip_pos.x,
                self.player.hammer.tip_pos.y,
                (255, 200, 0),
            )

    def draw(self):
        """繪製遊戲"""
        self.screen.fill((135, 206, 235))  # 天空藍

        # 繪製地形（應用攝影機偏移）
        for platform in self.terrain.platforms:
            camera_rect = pygame.Rect(
                platform.x + self.camera.offset.x,
                platform.y + self.camera.offset.y,
                platform.width,
                platform.height,
            )
            pygame.draw.rect(self.screen, BROWN, camera_rect)
            pygame.draw.rect(self.screen, DARK_GRAY, camera_rect, 2)

        for obstacle in self.terrain.obstacles:
            camera_rect = pygame.Rect(
                obstacle.x + self.camera.offset.x,
                obstacle.y + self.camera.offset.y,
                obstacle.width,
                obstacle.height,
            )
            pygame.draw.rect(self.screen, GRAY, camera_rect)
            pygame.draw.rect(self.screen, BLACK, camera_rect, 2)

        # 繪製終點標記
        finish_line = pygame.Rect(
            300 + self.camera.offset.x,
            SCREEN_HEIGHT - 2080 + self.camera.offset.y,
            150,
            30,
        )
        pygame.draw.rect(self.screen, YELLOW, finish_line)
        pygame.draw.rect(self.screen, BLACK, finish_line, 3)

        # 創建臨時玩家物件用於繪製（應用攝影機偏移）
        draw_player = Player(
            self.player.position.x + self.camera.offset.x,
            self.player.position.y + self.camera.offset.y,
        )
        draw_player.hammer.player_pos = Vector2(
            self.player.hammer.player_pos.x + self.camera.offset.x,
            self.player.hammer.player_pos.y + self.camera.offset.y,
        )
        draw_player.hammer.tip_pos = Vector2(
            self.player.hammer.tip_pos.x + self.camera.offset.x,
            self.player.hammer.tip_pos.y + self.camera.offset.y,
        )
        draw_player.hammer.is_hooked = self.player.hammer.is_hooked
        if self.player.hammer.is_hooked:
            draw_player.hammer.hook_point = Vector2(
                self.player.hammer.hook_point.x + self.camera.offset.x,
                self.player.hammer.hook_point.y + self.camera.offset.y,
            )
        draw_player.hammer.length = self.player.hammer.length
        draw_player.draw(self.screen)

        # 繪製粒子效果
        for particle in self.particles:
            if particle["life"] > 0:
                alpha = particle["life"] / 30.0 * 255
                color = (*particle["color"][:3], int(alpha))
                pygame.draw.circle(
                    self.screen,
                    particle["color"],
                    (
                        int(particle["x"] + self.camera.offset.x),
                        int(particle["y"] + self.camera.offset.y),
                    ),
                    3,
                )

        # 繪製 UI
        self.draw_ui()

        # 繪製完成畫面
        if self.game_completed:
            self.draw_completion_screen()

        pygame.display.flip()

    def draw_ui(self):
        """繪製使用者界面"""
        # 遊戲時間
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        time_text = self.font.render(f"時間: {elapsed_time}秒", True, WHITE)
        self.screen.blit(time_text, (10, 10))

        # 高度指示
        height = max(0, int((SCREEN_HEIGHT - self.player.highest_y) / 10))
        height_text = self.font.render(f"最高高度: {height}m", True, WHITE)
        self.screen.blit(height_text, (10, 50))

        # 最佳時間記錄
        if self.best_time:
            best_text = self.small_font.render(
                f"最佳時間: {self.best_time}秒", True, YELLOW
            )
            self.screen.blit(best_text, (10, 90))

        # 進度指示 - 調整為新的關卡高度
        progress = min(100, int(height / 200 * 100))  # 新關卡高度約2000像素
        progress_text = self.small_font.render(f"進度: {progress}%", True, GREEN)
        self.screen.blit(progress_text, (10, 115))

        # 控制說明
        instructions = [
            "滑鼠控制錘子方向",
            "按住左鍵掛住並擺動",
            "繩子可以穿牆，槌子不行",
            "左右移動滑鼠來甩自己",
            "將滑鼠移到腳下戳地跳躍",
            "利用擺動力向上攀爬",
            "R鍵重置位置",
            "ESC鍵退出遊戲",
        ]

        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            self.screen.blit(text, (10, SCREEN_HEIGHT - 140 + i * 18))

        # 速度指示
        speed = self.player.velocity.magnitude()
        speed_text = self.small_font.render(f"速度: {speed:.1f}", True, WHITE)
        self.screen.blit(speed_text, (SCREEN_WIDTH - 150, 10))

        # 錘子狀態
        hammer_status = "掛住擺動" if self.player.hammer.is_hooked else "空中"
        hammer_text = self.small_font.render(f"錘子: {hammer_status}", True, WHITE)
        self.screen.blit(hammer_text, (SCREEN_WIDTH - 150, 35))

        # 繩子長度指示
        rope_length = int(self.player.hammer.length)
        length_text = self.small_font.render(f"繩子長度: {rope_length}", True, WHITE)
        self.screen.blit(length_text, (SCREEN_WIDTH - 150, 60))

        # 擺動狀態和穿牆提示
        if self.player.hammer.is_hooked:
            swing_text = self.small_font.render("正在擺動!", True, YELLOW)
            self.screen.blit(swing_text, (SCREEN_WIDTH - 150, 85))

            # 檢查繩子是否穿牆
            steps = 10
            wall_blocked = False
            for i in range(1, steps):
                ratio = i / steps
                check_x = (
                    self.player.position.x
                    + (self.player.hammer.hook_point.x - self.player.position.x) * ratio
                )
                check_y = (
                    self.player.position.y
                    + (self.player.hammer.hook_point.y - self.player.position.y) * ratio
                )
                check_rect = pygame.Rect(check_x - 5, check_y - 5, 10, 10)
                if self.terrain.check_collision(check_rect):
                    wall_blocked = True
                    break

            if wall_blocked:
                wall_text = self.small_font.render("繩子穿牆!", True, GREEN)
                self.screen.blit(wall_text, (SCREEN_WIDTH - 150, 110))
        else:
            # 檢查是否可以戳地跳躍
            mouse_pos = pygame.mouse.get_pos()
            world_mouse_x = mouse_pos[0] - self.camera.offset.x
            world_mouse_y = mouse_pos[1] - self.camera.offset.y
            
            # 檢查滑鼠是否在玩家下方
            dy = world_mouse_y - self.player.position.y
            if dy > 30:  # 滑鼠在玩家下方30像素以上
                # 檢查錘子下方是否有地面可以戳
                tip_rect = pygame.Rect(self.player.hammer.tip_pos.x - 8, self.player.hammer.tip_pos.y - 8, 16, 16)
                collisions = self.terrain.check_collision(tip_rect)
                if collisions:
                    pogo_text = self.small_font.render("可戳地跳躍!", True, (0, 255, 255))
                    self.screen.blit(pogo_text, (SCREEN_WIDTH - 150, 85))

    def draw_completion_screen(self):
        """繪製完成畫面"""
        # 半透明背景
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # 完成訊息
        congrats_text = self.big_font.render("恭喜完成！", True, YELLOW)
        congrats_rect = congrats_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        )
        self.screen.blit(congrats_text, congrats_rect)

        # 完成時間
        time_text = self.font.render(f"完成時間: {self.completion_time}秒", True, WHITE)
        time_rect = time_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        )
        self.screen.blit(time_text, time_rect)

        # 最佳時間
        if self.completion_time == self.best_time:
            new_record_text = self.font.render("新記錄！", True, GREEN)
            new_record_rect = new_record_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
            )
            self.screen.blit(new_record_text, new_record_rect)
        else:
            best_text = self.font.render(f"最佳時間: {self.best_time}秒", True, YELLOW)
            best_rect = best_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
            )
            self.screen.blit(best_text, best_rect)

        # 重新開始提示
        restart_text = self.font.render("按 SPACE 重新開始", True, WHITE)
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        )
        self.screen.blit(restart_text, restart_rect)

    def run(self):
        """運行遊戲主循環"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()


def main():
    """主函數"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
