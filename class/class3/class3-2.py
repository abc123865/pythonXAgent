import pygame
import sys

# ==========================================
# 初始化函數
# ==========================================


def initialize_pygame():
    """初始化 pygame 系統"""
    pygame.init()


# ==========================================
# 視窗創建函數
# ==========================================


def create_display_surface(window_width, window_height, window_title):
    """
    創建顯示視窗

    Args:
        window_width (int): 視窗寬度
        window_height (int): 視窗高度
        window_title (str): 視窗標題

    Returns:
        pygame.Surface: 遊戲視窗表面
    """
    display_surface = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption(window_title)
    return display_surface


# ==========================================
# 顏色定義函數
# ==========================================


def define_color_palette():
    """
    定義遊戲中使用的顏色調色板

    Returns:
        dict: 包含所有顏色的字典
    """
    return {
        "WHITE": (255, 255, 255),
        "BLACK": (0, 0, 0),
        "RED": (255, 0, 0),
        "GREEN": (0, 255, 0),
        "BLUE": (0, 0, 255),
        "YELLOW": (255, 255, 0),
        "PURPLE": (128, 0, 128),
        "ORANGE": (255, 165, 0),
        "PINK": (255, 192, 203),
        "GRAY": (128, 128, 128),
    }


# ==========================================
# 繪圖函數
# ==========================================


def draw_geometric_shapes(display_surface, colors):
    """
    在顯示表面上繪製各種幾何圖形

    Args:
        display_surface (pygame.Surface): 要繪製的表面
        colors (dict): 顏色調色板
    """
    # 繪製矩形 - 紅色實心矩形
    pygame.draw.rect(display_surface, colors["RED"], (50, 50, 100, 80))

    # 繪製圓形 - 藍色實心圓
    pygame.draw.circle(display_surface, colors["BLUE"], (250, 100), 50)

    # 繪製橢圓 - 綠色實心橢圓
    pygame.draw.ellipse(display_surface, colors["GREEN"], (350, 50, 120, 80))

    # 繪製直線 - 黑色粗線
    pygame.draw.line(display_surface, colors["BLACK"], (50, 200), (200, 250), 5)

    # 繪製多邊形 - 紫色三角形
    triangle_points = [(300, 200), (350, 300), (250, 300)]
    pygame.draw.polygon(display_surface, colors["PURPLE"], triangle_points)

    # 繪製弧線 - 橙色半圓弧
    pygame.draw.arc(display_surface, colors["ORANGE"], (450, 200, 100, 100), 0, 3.14, 3)

    # 繪製連續線段 - 粉色抗鋸齒線
    line_points = [(100, 350), (120, 350), (140, 350), (160, 350)]
    pygame.draw.aalines(display_surface, colors["PINK"], False, line_points, 2)


# ==========================================
# 事件處理函數
# ==========================================


def handle_events():
    """
    處理 pygame 事件

    Returns:
        bool: 如果應該退出程式則返回 True，否則返回 False
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False


# ==========================================
# 主程式函數
# ==========================================


def main():
    """主程式入口點"""
    # 初始化 pygame 系統
    initialize_pygame()

    # 遊戲視窗配置常數
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 400
    WINDOW_TITLE = "Pygame Window"
    TARGET_FPS = 60

    # 創建顯示視窗和時鐘物件
    display_surface = create_display_surface(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game_clock = pygame.time.Clock()

    # 載入顏色調色板
    colors = define_color_palette()

    # 主遊戲迴圈
    running = True
    while running:
        # 控制幀率
        game_clock.tick(TARGET_FPS)

        # 處理事件
        running = not handle_events()

        # 清除螢幕 - 填充白色背景
        display_surface.fill(colors["WHITE"])

        # 繪製所有幾何圖形
        draw_geometric_shapes(display_surface, colors)

        # 更新顯示
        pygame.display.flip()

    # 清理並退出
    pygame.quit()
    sys.exit()


# ==========================================
# 程式入口點
# ==========================================


if __name__ == "__main__":
    main()
