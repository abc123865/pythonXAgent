#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
遊戲配置文件
包含遊戲的所有常數和設定
"""

import pygame

# 螢幕設定
DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 400
GROUND_HEIGHT_RATIO = 0.875  # 地面高度佔螢幕高度的比例
FPS = 60

# 全螢幕設定
FULLSCREEN_MODE = False
WINDOW_MODE = pygame.RESIZABLE


# 遊戲狀態常數
class GameState:
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2


# 難度等級常數
class Difficulty:
    EASY = 1
    MEDIUM = 2
    HARD = 3
    NIGHTMARE = 4


# 顏色調色板
def get_color_palette():
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


# 難度設定
DIFFICULTY_SETTINGS = {
    Difficulty.EASY: {
        "name": "簡單 (Easy)",
        "description": "適合新手，慢節奏遊戲",
        "game_speed": 4,
        "obstacle_spawn_rate": 0.9,
        "speed_increase_rate": 0.08,
    },
    Difficulty.MEDIUM: {
        "name": "中等 (Medium)",
        "description": "標準難度，平衡的挑戰",
        "game_speed": 7,
        "obstacle_spawn_rate": 1.1,
        "speed_increase_rate": 0.12,
    },
    Difficulty.HARD: {
        "name": "困難 (Hard)",
        "description": "快節奏，需要技巧",
        "game_speed": 10,
        "obstacle_spawn_rate": 1.3,
        "speed_increase_rate": 0.15,
    },
    Difficulty.NIGHTMARE: {
        "name": "噩夢 (Nightmare)",
        "description": "極速挑戰，僅靠反應力",
        "game_speed": 24,
        "obstacle_spawn_rate": 1.6,
        "speed_increase_rate": 0.3,
    },
}


# 物理常數
class Physics:
    GRAVITY = 1.2  # 增加重力，從0.8增加到1.2，讓跳躍更快落下
    JUMP_STRENGTH = -13  # 稍微減少跳躍力度，從-15調整到-13
    MAX_FALL_SPEED = 25  # 增加最大下降速度，讓下降更快


# 字體設定
FONT_PATH = r"C:\Windows\Fonts\msjh.ttc"  # 微軟正黑體路徑
