import pygame
import sys
import random

# 初始化 pygame
pygame.init()

# 遊戲設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 顏色定義
COLORS = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "PINK": (255, 182, 193),
    "PURPLE": (147, 112, 219),
    "BLUE": (135, 206, 250),
    "GREEN": (144, 238, 144),
    "YELLOW": (255, 255, 0),
    "ORANGE": (255, 165, 0),
    "RED": (255, 99, 71),
    "GRAY": (128, 128, 128),
    "DARK_BLUE": (0, 0, 139),
}


class Brick:
    """
    磚塊物件基礎類
    定義磚塊的位置、大小和顏色
    """

    def __init__(self, x, y, width=60, height=20, color=COLORS["PINK"]):
        """
        初始化磚塊

        Args:
            x (int): 磚塊的 x 座標位置
            y (int): 磚塊的 y 座標位置
            width (int): 磚塊的寬度，預設 60
            height (int): 磚塊的高度，預設 20
            color (tuple): 磚塊的顏色，預設粉色
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.destroyed = False
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        """
        繪製磚塊到螢幕上

        Args:
            screen: pygame 螢幕物件
        """
        if not self.destroyed:
            # 繪製磚塊主體
            pygame.draw.rect(screen, self.color, self.rect)
            # 繪製磚塊邊框，增加立體感
            pygame.draw.rect(screen, COLORS["WHITE"], self.rect, 2)

    def get_rect(self):
        """
        獲取磚塊的碰撞矩形

        Returns:
            pygame.Rect: 磚塊的碰撞矩形
        """
        return self.rect

    def destroy(self):
        """
        銷毀磚塊
        """
        self.destroyed = True

    def is_destroyed(self):
        """
        檢查磚塊是否已被銷毀

        Returns:
            bool: 如果磚塊已被銷毀返回 True
        """
        return self.destroyed


class Paddle(Brick):
    """
    球拍物件，繼承 Brick 物件的屬性
    用於控制球的移動和反彈
    """

    def __init__(self, x, y, width=100, height=15):
        """
        初始化球拍，繼承磚塊的基本屬性

        Args:
            x (int): 球拍的 x 座標位置
            y (int): 球拍的 y 座標位置
            width (int): 球拍的寬度，預設 100
            height (int): 球拍的高度，預設 15
        """
        # 繼承 Brick 的屬性
        super().__init__(x, y, width, height, COLORS["PURPLE"])
        self.speed = 8  # 球拍移動速度
        self.max_x = SCREEN_WIDTH - width  # 球拍最大 x 位置

    def move_left(self):
        """
        向左移動球拍
        """
        if self.x > 0:
            self.x -= self.speed
            self.rect.x = self.x

    def move_right(self):
        """
        向右移動球拍
        """
        if self.x < self.max_x:
            self.x += self.speed
            self.rect.x = self.x

    def update_position(self, mouse_x=None):
        """
        根據滑鼠位置更新球拍位置

        Args:
            mouse_x (int): 滑鼠的 x 座標，如果為 None 則不更新
        """
        if mouse_x is not None:
            # 讓球拍跟隨滑鼠，但保持在螢幕範圍內
            self.x = max(0, min(mouse_x - self.width // 2, self.max_x))
            self.rect.x = self.x

    def draw(self, screen):
        """
        繪製球拍，添加特殊的視覺效果

        Args:
            screen: pygame 螢幕物件
        """
        # 繪製球拍主體
        pygame.draw.rect(screen, self.color, self.rect)
        # 繪製球拍邊框
        pygame.draw.rect(screen, COLORS["WHITE"], self.rect, 2)
        # 添加漸層效果，讓球拍更有質感
        for i in range(3):
            inner_rect = pygame.Rect(
                self.rect.x + i,
                self.rect.y + i,
                self.rect.width - 2 * i,
                self.rect.height - 2 * i,
            )
            color_intensity = 255 - i * 30
            gradient_color = (
                color_intensity // 3,
                color_intensity // 3,
                color_intensity,
            )
            pygame.draw.rect(screen, gradient_color, inner_rect, 1)


class Ball:
    """
    球物件，用於彈跳和碰撞檢測
    """

    def __init__(self, x, y, radius=10):
        """
        初始化球

        Args:
            x (int): 球的初始 x 位置
            y (int): 球的初始 y 位置
            radius (int): 球的半徑
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = 0  # 初始靜止
        self.speed_y = 0  # 初始靜止
        self.color = COLORS["YELLOW"]
        self.trail = []  # 球的軌跡效果
        self.launched = False  # 球是否已發射

    def update(self, paddle=None):
        """
        更新球的位置

        Args:
            paddle: 球拍物件，當球未發射時需要跟隨球拍
        """
        if not self.launched:
            # 球未發射時，跟隨球拍移動
            if paddle:
                self.x = paddle.x + paddle.width // 2
                self.y = paddle.y - self.radius
            return

        self.x += self.speed_x
        self.y += self.speed_y

        # 記錄軌跡
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:  # 保持軌跡長度
            self.trail.pop(0)

        # 邊界碰撞檢測
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.speed_x = -self.speed_x
        if self.y <= self.radius:
            self.speed_y = -self.speed_y

    def draw(self, screen):
        """
        繪製球和軌跡效果

        Args:
            screen: pygame 螢幕物件
        """
        # 只有發射後才繪製軌跡效果
        if self.launched:
            for i, (trail_x, trail_y) in enumerate(self.trail):
                alpha = (i + 1) / len(self.trail)
                trail_radius = int(self.radius * alpha * 0.7)
                if trail_radius > 0:
                    pygame.draw.circle(
                        screen,
                        (
                            int(self.color[0] * alpha),
                            int(self.color[1] * alpha),
                            int(self.color[2] * alpha),
                        ),
                        (int(trail_x), int(trail_y)),
                        trail_radius,
                    )

        # 繪製球本體
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # 添加高光效果
        highlight_offset = self.radius // 3
        pygame.draw.circle(
            screen,
            COLORS["WHITE"],
            (int(self.x - highlight_offset), int(self.y - highlight_offset)),
            self.radius // 3,
        )

        # 如果球未發射，添加等待發射的視覺提示
        if not self.launched:
            # 繪製一個閃爍的圓圈提示
            import time

            if int(time.time() * 3) % 2:  # 每0.33秒閃爍一次
                pygame.draw.circle(
                    screen,
                    COLORS["WHITE"],
                    (int(self.x), int(self.y)),
                    self.radius + 5,
                    2,
                )

    def get_rect(self):
        """
        獲取球的碰撞矩形

        Returns:
            pygame.Rect: 球的碰撞矩形
        """
        return pygame.Rect(
            self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2
        )

    def bounce_off_paddle(self, paddle):
        """
        從球拍反彈，根據碰撞位置調整角度

        Args:
            paddle: 球拍物件
        """
        # 計算球與球拍碰撞的相對位置
        paddle_center = paddle.x + paddle.width // 2
        hit_pos = (self.x - paddle_center) / (paddle.width // 2)

        # 根據碰撞位置調整反彈角度
        self.speed_x = hit_pos * 7  # 最大速度為 7
        self.speed_y = -abs(self.speed_y)  # 確保向上反彈

    def launch(self):
        """
        發射球
        """
        if not self.launched:
            self.launched = True
            self.speed_x = random.choice([-4, -3, -2, 2, 3, 4])  # 隨機水平速度
            self.speed_y = -6  # 向上發射
            self.trail = []  # 清空軌跡

    def reset_position(self, x, y):
        """
        重置球的位置

        Args:
            x (int): 新的 x 位置
            y (int): 新的 y 位置
        """
        self.x = x
        self.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.launched = False  # 重置為未發射狀態
        self.trail = []


class BrickBreakerGame:
    """
    敲磚塊遊戲主類
    """

    def __init__(self):
        """
        初始化遊戲
        """
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 敲磚塊遊戲 🎮")
        self.clock = pygame.time.Clock()

        # 初始化遊戲物件
        self.paddle = Paddle(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50)
        # 球初始位置在球拍上方
        ball_x = self.paddle.x + self.paddle.width // 2
        ball_y = self.paddle.y - 10  # 球的半徑
        self.ball = Ball(ball_x, ball_y)
        self.bricks = []

        # 遊戲狀態
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.game_won = False

        # 設定中文字體 - 使用微軟正黑體絕對路徑
        self.setup_fonts()

        # 創建磚塊
        self.create_bricks()

    def setup_fonts(self):
        """
        設定中文字體，使用微軟正黑體
        """
        font_path = r"C:\Windows\Fonts\msjh.ttc"
        try:
            self.font_large = pygame.font.Font(font_path, 48)
            self.font_medium = pygame.font.Font(font_path, 32)
            self.font_small = pygame.font.Font(font_path, 24)
            print("✅ 成功載入微軟正黑體")
        except (FileNotFoundError, OSError):
            # 如果找不到微軟正黑體，嘗試其他中文字體
            alternative_fonts = [
                r"C:\Windows\Fonts\msyh.ttc",  # 微軟雅黑
                r"C:\Windows\Fonts\simhei.ttf",  # 黑體
                r"C:\Windows\Fonts\simsun.ttc",  # 新細明體
            ]

            font_loaded = False
            for font_path in alternative_fonts:
                try:
                    self.font_large = pygame.font.Font(font_path, 48)
                    self.font_medium = pygame.font.Font(font_path, 32)
                    self.font_small = pygame.font.Font(font_path, 24)
                    print(f"✅ 成功載入字體: {font_path}")
                    font_loaded = True
                    break
                except (FileNotFoundError, OSError):
                    continue

            if not font_loaded:
                # 使用系統預設字體
                print("⚠️ 找不到中文字體，使用系統預設字體")
                self.font_large = pygame.font.Font(None, 48)
                self.font_medium = pygame.font.Font(None, 32)
                self.font_small = pygame.font.Font(None, 24)

    def create_bricks(self):
        """
        創建磚塊陣列
        """
        self.bricks = []
        colors = [
            COLORS["PINK"],
            COLORS["PURPLE"],
            COLORS["BLUE"],
            COLORS["GREEN"],
            COLORS["YELLOW"],
            COLORS["ORANGE"],
        ]

        rows = 6
        cols = 12
        brick_width = 60
        brick_height = 20
        padding = 5
        start_x = (SCREEN_WIDTH - (cols * (brick_width + padding) - padding)) // 2
        start_y = 80

        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (brick_width + padding)
                y = start_y + row * (brick_height + padding)
                color = colors[row % len(colors)]
                brick = Brick(x, y, brick_width, brick_height, color)
                self.bricks.append(brick)

    def handle_events(self):
        """
        處理遊戲事件

        Returns:
            bool: 如果遊戲應該繼續運行返回 True
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and (self.game_over or self.game_won):
                    self.restart_game()
                elif event.key == pygame.K_LEFT:
                    self.paddle.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.paddle.move_right()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 滑鼠左鍵
                    if (
                        not self.ball.launched
                        and not self.game_over
                        and not self.game_won
                    ):
                        self.ball.launch()
            elif event.type == pygame.MOUSEMOTION:
                # 滑鼠控制球拍
                mouse_x, _ = pygame.mouse.get_pos()
                self.paddle.update_position(mouse_x)

        # 鍵盤連續按鍵檢測
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.move_left()
        if keys[pygame.K_RIGHT]:
            self.paddle.move_right()

        return True

    def update(self):
        """
        更新遊戲狀態
        """
        if self.game_over or self.game_won:
            return

        # 更新球的位置，如果球未發射則跟隨球拍
        self.ball.update(self.paddle)

        # 只有球發射後才檢查碰撞和掉落
        if self.ball.launched:
            # 檢查球是否掉出螢幕底部
            if self.ball.y > SCREEN_HEIGHT:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                else:
                    # 重置球的位置到球拍上
                    ball_x = self.paddle.x + self.paddle.width // 2
                    ball_y = self.paddle.y - self.ball.radius
                    self.ball.reset_position(ball_x, ball_y)

            # 檢查球與球拍的碰撞
            if self.ball.get_rect().colliderect(self.paddle.get_rect()):
                if self.ball.speed_y > 0:  # 只有向下移動時才反彈
                    self.ball.bounce_off_paddle(self.paddle)

            # 檢查球與磚塊的碰撞
            ball_rect = self.ball.get_rect()
            for brick in self.bricks[:]:
                if not brick.is_destroyed() and ball_rect.colliderect(brick.get_rect()):
                    brick.destroy()
                    self.score += 10

                    # 簡單的反彈邏輯
                    self.ball.speed_y = -self.ball.speed_y

                    # 如果所有磚塊都被銷毀，遊戲獲勝
                    if all(brick.is_destroyed() for brick in self.bricks):
                        self.game_won = True
                    break

    def draw(self):
        """
        繪製遊戲畫面
        """
        # 繪製背景漸層
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(20 + (50 - 20) * color_ratio)
            g = int(25 + (60 - 25) * color_ratio)
            b = int(50 + (100 - 50) * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # 繪製磚塊
        for brick in self.bricks:
            brick.draw(self.screen)

        # 繪製球拍和球
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)

        # 繪製 UI
        self.draw_ui()

        # 繪製遊戲結束或獲勝畫面
        if self.game_over:
            self.draw_game_over()
        elif self.game_won:
            self.draw_game_won()

        pygame.display.flip()

    def draw_ui(self):
        """
        繪製使用者介面
        """
        # 分數
        score_text = f"分數: {self.score}"
        score_surface = self.font_medium.render(score_text, True, COLORS["WHITE"])
        self.screen.blit(score_surface, (20, 20))

        # 生命數
        lives_text = f"生命: {self.lives}"
        lives_surface = self.font_medium.render(lives_text, True, COLORS["WHITE"])
        self.screen.blit(lives_surface, (20, 50))

        # 剩餘磚塊數
        remaining_bricks = sum(1 for brick in self.bricks if not brick.is_destroyed())
        bricks_text = f"剩餘磚塊: {remaining_bricks}"
        bricks_surface = self.font_small.render(bricks_text, True, COLORS["WHITE"])
        self.screen.blit(bricks_surface, (SCREEN_WIDTH - 150, 20))

        # 操作說明
        if not self.ball.launched and not self.game_over and not self.game_won:
            launch_text = "按滑鼠左鍵發射球！"
            launch_surface = self.font_medium.render(
                launch_text, True, COLORS["YELLOW"]
            )
            launch_rect = launch_surface.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
            )
            self.screen.blit(launch_surface, launch_rect)

        if self.score == 0 and self.lives == 3:
            control_text = "← → 方向鍵或滑鼠控制球拍"
            control_surface = self.font_small.render(
                control_text, True, COLORS["WHITE"]
            )
            control_rect = control_surface.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)
            )
            self.screen.blit(control_surface, control_rect)

    def draw_game_over(self):
        """
        繪製遊戲結束畫面
        """
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(COLORS["BLACK"])
        self.screen.blit(overlay, (0, 0))

        game_over_text = "遊戲結束！"
        game_over_surface = self.font_large.render(game_over_text, True, COLORS["RED"])
        game_over_rect = game_over_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        )
        self.screen.blit(game_over_surface, game_over_rect)

        final_score_text = f"最終分數: {self.score}"
        final_score_surface = self.font_medium.render(
            final_score_text, True, COLORS["YELLOW"]
        )
        final_score_rect = final_score_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )
        self.screen.blit(final_score_surface, final_score_rect)

        restart_text = "按空白鍵重新開始"
        restart_surface = self.font_medium.render(restart_text, True, COLORS["WHITE"])
        restart_rect = restart_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        )
        self.screen.blit(restart_surface, restart_rect)

    def draw_game_won(self):
        """
        繪製遊戲獲勝畫面
        """
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(COLORS["BLACK"])
        self.screen.blit(overlay, (0, 0))

        won_text = "🎉 恭喜獲勝！🎉"
        won_surface = self.font_large.render(won_text, True, COLORS["PINK"])
        won_rect = won_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        )
        self.screen.blit(won_surface, won_rect)

        final_score_text = f"最終分數: {self.score}"
        final_score_surface = self.font_medium.render(
            final_score_text, True, COLORS["YELLOW"]
        )
        final_score_rect = final_score_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )
        self.screen.blit(final_score_surface, final_score_rect)

        restart_text = "按空白鍵重新開始"
        restart_surface = self.font_medium.render(restart_text, True, COLORS["WHITE"])
        restart_rect = restart_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        )
        self.screen.blit(restart_surface, restart_rect)

    def restart_game(self):
        """
        重新開始遊戲
        """
        self.paddle = Paddle(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50)
        # 球重新開始時也要在球拍上
        ball_x = self.paddle.x + self.paddle.width // 2
        ball_y = self.paddle.y - 10
        self.ball = Ball(ball_x, ball_y)
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.game_won = False
        self.create_bricks()

    def run(self):
        """
        運行遊戲主迴圈
        """
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
    print("🎮 敲磚塊遊戲啟動！🎮")
    print("=" * 60)
    print("🎯 遊戲目標：")
    print("   • 用球拍控制球反彈，擊破所有磚塊！")
    print("   • 精美的配色設計，帶來優質的遊戲體驗！")
    print()
    print("🕹️ 操作說明：")
    print("   • ← → 方向鍵：移動球拍")
    print("   • 滑鼠移動：也可以控制球拍位置")
    print("   • 滑鼠左鍵：發射球")
    print("   • 空白鍵：遊戲結束後重新開始")
    print()
    print("🏗️ 技術實現：")
    print("   • Brick 類：定義磚塊的位置、大小和顏色")
    print("   • Paddle 類：繼承 Brick 的屬性，增加移動功能")
    print("   • Ball 類：處理球的物理運動和碰撞")
    print("   • 精美的軌跡效果和視覺回饋")
    print()
    print("💡 遊戲特色：")
    print("   • 物件導向設計，符合開發計畫")
    print("   • 精美色彩搭配，充滿質感")
    print("   • 流暢的物理效果和碰撞檢測")
    print("   • 多種控制方式，提升遊戲體驗")
    print("   • 支援中文字體顯示")
    print()
    print("🚀 準備開始遊戲了嗎？Let's go！")
    print("=" * 60)

    try:
        game = BrickBreakerGame()
        game.run()
    except Exception as e:
        print(f"❌ 遊戲發生錯誤: {e}")
        print("請確保已安裝 pygame：pip install pygame")
        sys.exit(1)
