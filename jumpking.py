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

# 物理設定
GRAVITY = 0.5
MAX_FALL_SPEED = 15
JUMP_CHARGE_RATE = 0.3
MAX_JUMP_POWER = 20
MIN_JUMP_POWER = 5


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

    def update(self, platforms):
        # 處理重力
        if not self.on_ground:
            self.vel_y += GRAVITY
            if self.vel_y > MAX_FALL_SPEED:
                self.vel_y = MAX_FALL_SPEED

        # 更新位置
        self.x += self.vel_x
        self.y += self.vel_y

        # 檢查平台碰撞
        self.check_platform_collision(platforms)

        # 減少水平速度（摩擦力）
        if self.on_ground:
            self.vel_x *= 0.8
        else:
            self.vel_x *= 0.95

    def check_platform_collision(self, platforms):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.on_ground = False

        for platform in platforms:
            platform_rect = pygame.Rect(
                platform["x"], platform["y"], platform["width"], platform["height"]
            )

            if player_rect.colliderect(platform_rect):
                # 從上方落下 (改善碰撞檢測)
                if self.vel_y > 0 and self.y + self.height - 10 <= platform["y"]:
                    self.y = platform["y"] - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    print(f"Landed on platform at y={platform['y']}")
                # 從下方撞擊
                elif (
                    self.vel_y < 0 and self.y >= platform["y"] + platform["height"] - 10
                ):
                    self.y = platform["y"] + platform["height"]
                    self.vel_y = 0
                # 從左側撞擊
                elif self.vel_x > 0 and self.x + self.width - 10 <= platform["x"]:
                    self.x = platform["x"] - self.width
                    self.vel_x = 0
                # 從右側撞擊
                elif (
                    self.vel_x < 0 and self.x >= platform["x"] + platform["width"] - 10
                ):
                    self.x = platform["x"] + platform["width"]
                    self.vel_x = 0

    def start_jump_charge(self):
        if self.on_ground:
            self.jump_charging = True
            self.jump_power = MIN_JUMP_POWER
            print(f"Started charging jump. On ground: {self.on_ground}")

    def update_jump_charge(self):
        if self.jump_charging and self.on_ground:
            self.jump_power += JUMP_CHARGE_RATE
            if self.jump_power > MAX_JUMP_POWER:
                self.jump_power = MAX_JUMP_POWER

    def execute_jump(self, direction):
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

            # 除錯訊息
            print(
                f"Jump executed! Direction: {direction}, Power: {jump_force}, Angle: {angle}"
            )
            print(f"Velocity set to: x={self.vel_x:.2f}, y={self.vel_y:.2f}")

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


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jump King Clone")
        self.clock = pygame.time.Clock()
        self.running = True

        # 初始化玩家 (確保在地面上)
        self.player = Player(100, 510)  # 調整Y座標確保在起始平台上

        # 相機
        self.camera_y = 0

        # 創建平台
        self.platforms = self.create_platforms()

        # 遊戲狀態
        self.highest_y = self.player.y
        self.save_file = "jumpking_save.json"
        self.load_game()

    def create_platforms(self):
        platforms = []

        # 起始平台
        platforms.append({"x": 0, "y": 550, "width": 800, "height": 50})

        # 第一層
        platforms.append({"x": 150, "y": 450, "width": 100, "height": 20})
        platforms.append({"x": 350, "y": 400, "width": 80, "height": 20})
        platforms.append({"x": 550, "y": 450, "width": 120, "height": 20})

        # 第二層
        platforms.append({"x": 50, "y": 350, "width": 90, "height": 20})
        platforms.append({"x": 250, "y": 300, "width": 100, "height": 20})
        platforms.append({"x": 450, "y": 320, "width": 80, "height": 20})
        platforms.append({"x": 650, "y": 350, "width": 100, "height": 20})

        # 第三層
        platforms.append({"x": 100, "y": 200, "width": 70, "height": 20})
        platforms.append({"x": 300, "y": 150, "width": 90, "height": 20})
        platforms.append({"x": 500, "y": 180, "width": 100, "height": 20})

        # 第四層 - 更有挑戰性
        platforms.append({"x": 80, "y": 50, "width": 60, "height": 20})
        platforms.append({"x": 220, "y": 0, "width": 80, "height": 20})
        platforms.append({"x": 400, "y": 30, "width": 70, "height": 20})
        platforms.append({"x": 550, "y": -10, "width": 90, "height": 20})

        # 最終目標平台
        platforms.append({"x": 350, "y": -100, "width": 100, "height": 30})

        return platforms

    def update_camera(self):
        # 相機跟隨玩家，但有平滑效果
        target_y = self.player.y - SCREEN_HEIGHT // 2
        self.camera_y += (target_y - self.camera_y) * 0.1

    def save_game(self):
        save_data = {
            "player_x": self.player.x,
            "player_y": self.player.y,
            "highest_y": self.highest_y,
        }
        try:
            with open(self.save_file, "w") as f:
                json.dump(save_data, f)
        except:
            pass

    def load_game(self):
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, "r") as f:
                    save_data = json.load(f)
                    self.player.x = save_data.get("player_x", 100)
                    self.player.y = save_data.get("player_y", 510)  # 調整預設位置
                    self.highest_y = save_data.get("highest_y", self.player.y)
        except:
            pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_game()
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.start_jump_charge()
                elif event.key == pygame.K_r:
                    # 重置遊戲
                    self.player.x = 100
                    self.player.y = 510  # 調整重置位置
                    self.player.vel_x = 0
                    self.player.vel_y = 0
                    self.save_game()
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

    def update(self):
        # 更新跳躍蓄力
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.player.update_jump_charge()

        # 更新玩家
        self.player.update(self.platforms)

        # 更新相機
        self.update_camera()

        # 更新最高記錄
        if self.player.y < self.highest_y:
            self.highest_y = self.player.y
            self.save_game()

        # 檢查是否到達目標
        if self.player.y <= -80:  # 到達最高平台
            self.show_victory_message()

    def show_victory_message(self):
        font = pygame.font.Font(None, 72)
        text = font.render("You Win!", True, YELLOW)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)

    def draw(self):
        # 清除螢幕
        self.screen.fill(DARK_BLUE)

        # 繪製平台
        for platform in self.platforms:
            color = BROWN
            if platform["y"] <= -80:  # 目標平台
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

        # 繪製玩家
        self.player.draw(self.screen, self.camera_y)

        # 繪製UI
        self.draw_ui()

        # 更新顯示
        pygame.display.flip()

    def draw_ui(self):
        font = pygame.font.Font(None, 36)

        # 顯示控制說明
        instructions = [
            "Hold SPACE to charge jump",
            "Release SPACE to jump",
            "LEFT/RIGHT arrows for direction",
            "R to reset position",
        ]

        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, WHITE)
            self.screen.blit(text, (10, 10 + i * 25))

        # 顯示高度
        height_text = f"Height: {max(0, int((550 - self.player.y) / 10))}m"
        text = font.render(height_text, True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH - 200, 10))

        # 顯示最高記錄
        best_height = f"Best: {max(0, int((550 - self.highest_y) / 10))}m"
        text = font.render(best_height, True, YELLOW)
        self.screen.blit(text, (SCREEN_WIDTH - 200, 40))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
