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


# 音效設定
class SoundSystem:
    # 音效檔案路徑 (如果存在)
    SOUND_ENABLED = True
    SOUND_VOLUME = 0.5  # 音量 (0.0 到 1.0)

    # 按鍵音效頻率設定 (用於程序生成音效)
    KEY_PRESS_FREQUENCY = 800  # Hz
    KEY_PRESS_DURATION = 100  # 毫秒

    JUMP_FREQUENCY = 600
    JUMP_DURATION = 150

    DASH_FREQUENCY = 1000
    DASH_DURATION = 120

    SHIELD_FREQUENCY = 1200
    SHIELD_DURATION = 200

    MENU_MOVE_FREQUENCY = 700
    MENU_MOVE_DURATION = 80

    MENU_SELECT_FREQUENCY = 900
    MENU_SELECT_DURATION = 150


# 分數系統設定
class ScoreSystem:
    # 距離分數設定
    DISTANCE_SCORE_INTERVAL = 100  # 每走過100像素給分
    BASE_DISTANCE_SCORE = 1  # 基礎距離分數

    # 速度倍數設定
    SPEED_BONUS_THRESHOLD = 8.0  # 速度超過此值開始給額外分數
    SPEED_BONUS_MULTIPLIER = 0.2  # 每增加1速度單位，分數倍數增加0.2
    MAX_SPEED_MULTIPLIER = 5.0  # 最大速度倍數

    # 障礙物分數（根據難度調整）
    OBSTACLE_BASE_SCORE = 10
    COMBO_BONUS_MULTIPLIER = 1.5  # 連擊倍數

    # 難度分數倍數
    DIFFICULTY_MULTIPLIERS = {
        1: 1.0,  # 簡單
        2: 1.5,  # 中等
        3: 2.0,  # 困難
        4: 3.0,  # 噩夢
    }
