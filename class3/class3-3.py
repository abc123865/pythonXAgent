import pygame
import sys
import math

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


def get_color_sequence():
    """
    取得顏色變換序列

    Returns:
        list: 顏色名稱列表
    """
    return ["RED", "GREEN", "BLUE", "YELLOW", "PURPLE", "ORANGE", "PINK"]


# ==========================================
# 繪圖函數
# ==========================================


def draw_red_square(
    display_surface, colors, square_x, square_y, current_color="RED", square_size=80
):
    """
    在顯示表面上繪製指定顏色的正方形

    Args:
        display_surface (pygame.Surface): 要繪製的表面
        colors (dict): 顏色調色板
        square_x (int): 方塊的 x 座標
        square_y (int): 方塊的 y 座標
        current_color (str): 當前顏色名稱
        square_size (int): 方塊的邊長
    """
    # 繪製正方形 - 使用當前顏色
    pygame.draw.rect(
        display_surface,
        colors[current_color],
        (square_x, square_y, square_size, square_size),
    )


def draw_coordinate_text(
    display_surface,
    colors,
    square_x,
    square_y,
    font,
    total_distance,
    current_color,
    square_size=80,
):
    """
    在左上角顯示方塊中心座標和移動資訊

    Args:
        display_surface (pygame.Surface): 要繪製的表面
        colors (dict): 顏色調色板
        square_x (int): 方塊的 x 座標
        square_y (int): 方塊的 y 座標
        font (pygame.font.Font): 字體物件
        total_distance (float): 累計移動距離
        current_color (str): 當前顏色名稱
        square_size (int): 方塊的邊長
    """
    # 計算方塊中心座標
    center_x = square_x + square_size // 2
    center_y = square_y + square_size // 2

    # 建立座標文字
    coordinate_text = f"方塊中心座標: ({center_x}, {center_y})"
    distance_text = f"累計移動距離: {total_distance:.1f}"
    color_text = f"當前顏色: {current_color}"

    # 渲染文字表面
    coord_surface = font.render(coordinate_text, True, colors["BLACK"])
    distance_surface = font.render(distance_text, True, colors["BLACK"])
    color_surface = font.render(color_text, True, colors[current_color])

    # 在左上角顯示文字
    display_surface.blit(coord_surface, (10, 10))
    display_surface.blit(distance_surface, (10, 40))
    display_surface.blit(color_surface, (10, 70))


# ==========================================
# 鍵盤處理函數
# ==========================================


def handle_keyboard_input(keys_pressed, square_x, square_y, move_speed=5):
    """
    處理鍵盤輸入並更新方塊位置

    Args:
        keys_pressed: pygame 鍵盤狀態
        square_x (int): 當前方塊 x 座標
        square_y (int): 當前方塊 y 座標
        move_speed (int): 移動速度

    Returns:
        tuple: 新的 (x, y) 座標和本次移動距離
    """
    new_x, new_y = square_x, square_y
    move_distance = 0

    # WASD 鍵控制
    if keys_pressed[pygame.K_w]:  # W 鍵 - 向上移動
        new_y -= move_speed
        move_distance = move_speed
    if keys_pressed[pygame.K_s]:  # S 鍵 - 向下移動
        new_y += move_speed
        move_distance = move_speed
    if keys_pressed[pygame.K_a]:  # A 鍵 - 向左移動
        new_x -= move_speed
        move_distance = move_speed
    if keys_pressed[pygame.K_d]:  # D 鍵 - 向右移動
        new_x += move_speed
        move_distance = move_speed

    # 如果同時按下多個鍵，計算對角線移動距離
    if move_distance > 0:
        dx = new_x - square_x
        dy = new_y - square_y
        actual_distance = math.sqrt(dx * dx + dy * dy)
        move_distance = actual_distance

    return new_x, new_y, move_distance


def keep_square_in_bounds(
    square_x, square_y, window_width, window_height, square_size=80
):
    """
    確保方塊保持在視窗範圍內

    Args:
        square_x (int): 方塊 x 座標
        square_y (int): 方塊 y 座標
        window_width (int): 視窗寬度
        window_height (int): 視窗高度
        square_size (int): 方塊邊長

    Returns:
        tuple: 修正後的 (x, y) 座標
    """
    # 限制 x 座標範圍
    square_x = max(0, min(square_x, window_width - square_size))
    # 限制 y 座標範圍
    square_y = max(0, min(square_y, window_height - square_size))

    return square_x, square_y


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


def update_color_system(total_distance, color_index, color_sequence):
    """
    更新顏色系統，當累計距離達到50時切換顏色

    Args:
        total_distance (float): 累計移動距離
        color_index (int): 當前顏色索引
        color_sequence (list): 顏色序列

    Returns:
        tuple: (新的累計距離, 新的顏色索引, 當前顏色名稱)
    """
    if total_distance >= 50:
        # 重置累計距離
        total_distance = 0
        # 切換到下一個顏色
        color_index = (color_index + 1) % len(color_sequence)

    current_color = color_sequence[color_index]
    return total_distance, color_index, current_color


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
    WINDOW_TITLE = "WASD 控制彩色正方形 - aespa Style! 💫"
    TARGET_FPS = 60
    MOVE_SPEED = 5
    SQUARE_SIZE = 80

    # 創建顯示視窗和時鐘物件
    display_surface = create_display_surface(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game_clock = pygame.time.Clock()

    # 初始化字體 - 使用微軟正黑體
    font_path = r"C:\Windows\Fonts\msjh.ttc"
    try:
        font = pygame.font.Font(font_path, 24)
    except FileNotFoundError:
        # 如果找不到微軟正黑體，使用系統預設字體
        print("警告：找不到微軟正黑體，使用系統預設字體")
        font = pygame.font.Font(None, 24)

    # 載入顏色調色板和顏色序列
    colors = define_color_palette()
    color_sequence = get_color_sequence()

    # 方塊初始位置和顏色系統初始化
    square_x = 50
    square_y = 50
    total_distance = 0.0
    color_index = 0
    current_color = color_sequence[color_index]

    # 主遊戲迴圈
    running = True
    while running:
        # 控制幀率
        game_clock.tick(TARGET_FPS)

        # 處理事件
        running = not handle_events()

        # 獲取鍵盤狀態
        keys_pressed = pygame.key.get_pressed()

        # 處理鍵盤輸入並更新方塊位置
        new_x, new_y, move_distance = handle_keyboard_input(
            keys_pressed, square_x, square_y, MOVE_SPEED
        )

        # 確保方塊保持在視窗範圍內
        new_x, new_y = keep_square_in_bounds(
            new_x, new_y, WINDOW_WIDTH, WINDOW_HEIGHT, SQUARE_SIZE
        )

        # 更新累計距離（只有在實際移動時才累加）
        if new_x != square_x or new_y != square_y:
            total_distance += move_distance

        # 更新方塊位置
        square_x, square_y = new_x, new_y

        # 更新顏色系統
        total_distance, color_index, current_color = update_color_system(
            total_distance, color_index, color_sequence
        )

        # 清除螢幕 - 填充白色背景
        display_surface.fill(colors["WHITE"])

        # 繪製當前顏色的正方形
        draw_red_square(
            display_surface, colors, square_x, square_y, current_color, SQUARE_SIZE
        )

        # 顯示方塊資訊
        draw_coordinate_text(
            display_surface,
            colors,
            square_x,
            square_y,
            font,
            total_distance,
            current_color,
            SQUARE_SIZE,
        )

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
