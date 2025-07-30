import pygame
import random
import sys

# 初始化 pygame
pygame.init()

# 遊戲設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 350
FPS = 60


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
    }


# 全域顏色變數（向後兼容）
colors = define_color_palette()
WHITE = colors["WHITE"]
BLACK = colors["BLACK"]
GRAY = colors["GRAY"]
GREEN = colors["GREEN"]


class Dinosaur:
    def __init__(self):
        self.x = 80
        self.y = GROUND_HEIGHT - 40
        self.width = 40
        self.height = 40
        self.original_height = 40
        self.jump_speed = 0
        self.gravity = 0.8
        self.is_jumping = False
        self.is_ducking = False
        self.jump_strength = -15

    def jump(self):
        if not self.is_jumping and not self.is_ducking:
            self.jump_speed = self.jump_strength
            self.is_jumping = True

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
        if self.is_jumping:
            self.y += self.jump_speed
            self.jump_speed += self.gravity

            # 檢查是否著地
            if self.y >= GROUND_HEIGHT - self.height:
                self.y = GROUND_HEIGHT - self.height
                self.is_jumping = False
                self.jump_speed = 0

    def draw(self, screen):
        # 畫小恐龍（簡單的矩形）
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
        # 恐龍的眼睛
        eye_y = self.y + 10 if not self.is_ducking else self.y + 5
        pygame.draw.circle(screen, BLACK, (self.x + 10, eye_y), 3)

        # 如果在蹲下，改變形狀
        if self.is_ducking:
            # 畫蹲下的恐龍（更扁平）
            pygame.draw.rect(
                screen, colors["DARK_GREEN"], (self.x, self.y, self.width, 5)
            )

    def get_collision_rect(self):
        """獲取碰撞檢測矩形"""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Obstacle:
    """基礎障礙物類"""

    def __init__(self, obstacle_type="normal"):
        self.x = SCREEN_WIDTH
        self.speed = 5
        self.obstacle_type = obstacle_type
        self.setup_obstacle()

    def setup_obstacle(self):
        """根據障礙物類型設置屬性"""
        if self.obstacle_type == "normal":
            # 普通仙人掌
            self.y = GROUND_HEIGHT - 30
            self.width = 20
            self.height = 30
            self.color = BLACK
        elif self.obstacle_type == "tall":
            # 高仙人掌
            self.y = GROUND_HEIGHT - 50
            self.width = 25
            self.height = 50
            self.color = BLACK
        elif self.obstacle_type == "wide":
            # 寬仙人掌
            self.y = GROUND_HEIGHT - 35
            self.width = 35
            self.height = 35
            self.color = BLACK
        elif self.obstacle_type == "short":
            # 矮仙人掌（不需要跳躍）
            self.y = GROUND_HEIGHT - 15
            self.width = 30
            self.height = 15
            self.color = colors["DARK_GREEN"]
        elif self.obstacle_type == "flying":
            # 飛行障礙物（鳥類）
            self.y = GROUND_HEIGHT - 80
            self.width = 25
            self.height = 15
            self.color = colors["GRAY"]

    def update(self):
        self.x -= self.speed

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
            pygame.draw.circle(screen, colors["GREEN"], (self.x + 5, self.y + 5), 3)
            pygame.draw.circle(screen, colors["GREEN"], (self.x + 20, self.y + 8), 2)
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
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("小恐龍遊戲")
        self.clock = pygame.time.Clock()
        self.dinosaur = Dinosaur()
        self.obstacles = []
        self.clouds = []
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.obstacle_timer = 0
        self.cloud_timer = 0
        self.game_speed = 5
        self.speed_increase_timer = 0

        # 載入顏色調色板
        self.colors = define_color_palette()

        # 字體設定 - 參考 class3-3.py 的字體處理方式
        self.setup_fonts()

    def setup_fonts(self):
        """設定遊戲字體 - 參考 class3-3.py 的字體處理"""
        # 嘗試載入微軟正黑體
        font_path = r"C:\Windows\Fonts\msjh.ttc"
        try:
            self.font_large = pygame.font.Font(font_path, 36)
            self.font_medium = pygame.font.Font(font_path, 24)
            self.font_small = pygame.font.Font(font_path, 18)
            print("✅ 成功載入微軟正黑體")
        except FileNotFoundError:
            # 如果找不到微軟正黑體，使用系統預設字體
            print("⚠️ 找不到微軟正黑體，使用系統預設字體")
            self.font_large = pygame.font.Font(None, 36)
            self.font_medium = pygame.font.Font(None, 24)
            self.font_small = pygame.font.Font(None, 18)

    def spawn_obstacle(self):
        if self.obstacle_timer <= 0:
            # 隨機選擇障礙物類型
            obstacle_types = ["normal", "tall", "wide", "short", "flying"]
            obstacle_type = random.choice(obstacle_types)
            self.obstacles.append(Obstacle(obstacle_type))
            self.obstacle_timer = random.randint(60, 120)  # 1-2秒間隔
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

        for obstacle in self.obstacles:
            obstacle_rect = obstacle.get_collision_rect()

            # 檢查是否有碰撞
            if dino_rect.colliderect(obstacle_rect):
                # 檢查特殊情況
                if obstacle.can_walk_through():
                    # 矮障礙物可以直接走過，不算碰撞
                    continue
                elif obstacle.can_duck_under() and self.dinosaur.is_ducking:
                    # 飛行障礙物在蹲下時可以避開
                    continue
                else:
                    return True
        return False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if not self.game_over:
                        self.dinosaur.jump()
                    else:
                        # 重新開始遊戲
                        self.restart_game()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if not self.game_over:
                        self.dinosaur.duck()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if not self.game_over:
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
        print("🔄 遊戲重新開始")

    def update(self):
        if not self.game_over:
            self.dinosaur.update()

            # 增加遊戲速度 - 每5秒增加一次難度
            self.speed_increase_timer += 1
            if self.speed_increase_timer >= 300:  # 5秒 = 60fps * 5
                self.game_speed += 0.2
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
                    self.score += 10

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

    def draw_game_info(self):
        """
        繪製遊戲資訊文字 - 參考 class3-3.py 的文字顯示方式
        """
        # 分數顯示
        score_text = f"分數: {self.score}"
        score_surface = self.font_medium.render(score_text, True, self.colors["BLACK"])
        self.screen.blit(score_surface, (10, 10))

        # 最高分顯示
        if self.high_score > 0:
            high_score_text = f"最高分: {self.high_score}"
            high_score_surface = self.font_small.render(
                high_score_text, True, self.colors["PURPLE"]
            )
            self.screen.blit(high_score_surface, (10, 40))

        # 遊戲速度顯示
        speed_text = f"速度: {self.game_speed:.1f}x"
        speed_surface = self.font_small.render(speed_text, True, self.colors["BLUE"])
        self.screen.blit(speed_surface, (10, 65))

        # 恐龍座標顯示（調試用）
        dino_pos_text = f"恐龍位置: ({self.dinosaur.x}, {int(self.dinosaur.y)})"
        dino_pos_surface = self.font_small.render(
            dino_pos_text, True, self.colors["DARK_GREEN"]
        )
        self.screen.blit(dino_pos_surface, (10, 90))

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
        restart_text = "按空白鍵重新開始 (Press SPACE to restart)"
        restart_surface = self.font_medium.render(
            restart_text, True, self.colors["WHITE"]
        )
        restart_rect = restart_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
        )
        self.screen.blit(restart_surface, restart_rect)

    def draw_start_instructions(self):
        """
        繪製開始遊戲的操作說明
        """
        if not self.game_over and self.score == 0:
            # 主要操作說明
            instruction_text = "↑/空白鍵:跳躍  ↓/S鍵:蹲下"
            instruction_surface = self.font_medium.render(
                instruction_text, True, self.colors["GRAY"]
            )
            instruction_rect = instruction_surface.get_rect(
                center=(SCREEN_WIDTH // 2, 90)
            )
            self.screen.blit(instruction_surface, instruction_rect)

            # 障礙物說明
            obstacles_text = "🌵 高低仙人掌需跳躍  🪨 石頭可走過  🐦 鳥類需蹲下"
            obstacles_surface = self.font_small.render(
                obstacles_text, True, self.colors["BLUE"]
            )
            obstacles_rect = obstacles_surface.get_rect(center=(SCREEN_WIDTH // 2, 115))
            self.screen.blit(obstacles_surface, obstacles_rect)

            # 副標題
            subtitle_text = "運用不同策略避開障礙物，獲得高分！"
            subtitle_surface = self.font_small.render(
                subtitle_text, True, self.colors["GREEN"]
            )
            subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 140))
            self.screen.blit(subtitle_surface, subtitle_rect)

    def draw(self):
        """
        主要繪製方法 - 參考 class3-3.py 的清晰結構
        """
        # 清空螢幕 - 使用白色背景
        self.screen.fill(self.colors["WHITE"])

        # 畫地面
        pygame.draw.line(
            self.screen,
            self.colors["BLACK"],
            (0, GROUND_HEIGHT),
            (SCREEN_WIDTH, GROUND_HEIGHT),
            2,
        )

        # 畫雲朵
        for cloud in self.clouds:
            cloud.draw(self.screen)

        # 畫恐龍
        self.dinosaur.draw(self.screen)

        # 畫障礙物
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # 顯示遊戲資訊
        self.draw_game_info()

        # 顯示開始說明
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
    print("=" * 60)
    print("🦕 進階小恐龍遊戲啟動！")
    print("=" * 60)
    print("🎮 遊戲特色：")
    print("   • 動態速度調整 - 遊戲會越來越快！")
    print("   • 精美的中文字體顯示")
    print("   • 最高分記錄系統")
    print("   • 多種類型的障礙物挑戰")
    print("   • 跳躍和蹲下雙重操作策略")
    print()
    print("🕹️ 操作說明：")
    print("   • ↑方向鍵 或 空白鍵：讓恐龍跳躍")
    print("   • ↓方向鍵 或 S鍵：讓恐龍蹲下")
    print()
    print("🌵 障礙物類型：")
    print("   • 普通仙人掌 (黑色) - 需要跳躍避開")
    print("   • 高仙人掌 (黑色+分支) - 需要跳躍避開")
    print("   • 寬仙人掌 (黑色+多分支) - 需要跳躍避開")
    print("   • 矮石頭 (綠色) - 可以直接走過，不會碰撞")
    print("   • 飛行鳥類 (灰色) - 需要蹲下避開")
    print()
    print("💡 策略提示：")
    print("   • 觀察障礙物類型，選擇正確的應對方式")
    print("   • 矮石頭安全無害，飛行鳥類必須蹲下")
    print("   • 獲得高分，挑戰自己的極限！")
    print()
    print("🎯 準備好接受挑戰了嗎？開始遊戲吧！")
    print("=" * 60)

    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"❌ 遊戲發生錯誤: {e}")
        print("請確保已安裝 pygame：pip install pygame")
        sys.exit(1)
