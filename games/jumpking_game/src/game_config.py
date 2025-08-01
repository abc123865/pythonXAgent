#!/usr/bin/env python3
"""
Jump King 遊戲設定檔案
包含所有遊戲相關的常數和配置
"""

# 視窗設定
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
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

# 檔案路徑
SAVE_FILE = "jumpking_save.json"

# 字體路徑
FONT_PATHS = [
    "C:\\Windows\\Fonts\\msjh.ttc",  # 微軟正黑體
    "C:\\Windows\\Fonts\\msyh.ttc",  # 微軟雅黑
    "C:\\Windows\\Fonts\\simsun.ttc",  # 新細明體
    "C:\\Windows\\Fonts\\kaiu.ttf",  # 標楷體
]

# 玩家設定
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 40
PLAYER_COLOR = BLUE

# UI設定
FONT_LARGE_SIZE = 48
FONT_MEDIUM_SIZE = 36
FONT_SMALL_SIZE = 24
