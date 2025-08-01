#!/usr/bin/env python3
"""
Jump King 關卡管理器
處理所有關卡的創建和管理
"""
import sys
import os

# 添加 src 目錄到路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(current_dir), "src")
sys.path.insert(0, src_dir)

try:
    from game_config import TOTAL_LEVELS
except ImportError:
    TOTAL_LEVELS = 11  # 默認值


class LevelManager:
    def __init__(self):
        self.levels = self.create_all_levels()

    def create_all_levels(self):
        """創建所有關卡的平台和死亡區域"""
        levels = {}

        # 第1關 - 簡單練習
        levels[1] = {
            "name": "初學者之路",
            "platforms": [
                {"x": 0, "y": 550, "width": 800, "height": 50},  # 地面
                {"x": 200, "y": 450, "width": 150, "height": 20},
                {"x": 450, "y": 350, "width": 150, "height": 20},
                {"x": 200, "y": 250, "width": 150, "height": 20},
                {"x": 300, "y": 100, "width": 200, "height": 30},  # 目標
            ],
            "death_zones": [],
            "goal_y": 100,
            "start_pos": (100, 500),
            "target_deaths": 5,
        }

        # 第2關 - 加入陷阱
        levels[2] = {
            "name": "小心陷阱",
            "platforms": [
                {"x": 0, "y": 550, "width": 800, "height": 50},
                {"x": 150, "y": 450, "width": 100, "height": 20},
                {"x": 400, "y": 400, "width": 80, "height": 20},
                {"x": 100, "y": 300, "width": 80, "height": 20},
                {"x": 500, "y": 250, "width": 100, "height": 20},
                {"x": 200, "y": 150, "width": 80, "height": 20},
                {"x": 350, "y": 50, "width": 100, "height": 30},
            ],
            "death_zones": [
                {"x": 250, "y": 400, "width": 150, "height": 200},
            ],
            "goal_y": 50,
            "start_pos": (100, 500),
            "target_deaths": 8,
        }

        # 第3關 - 精確跳躍
        levels[3] = {
            "name": "精確控制",
            "platforms": [
                {"x": 0, "y": 550, "width": 100, "height": 50},
                {"x": 180, "y": 450, "width": 60, "height": 20},
                {"x": 320, "y": 380, "width": 50, "height": 20},
                {"x": 500, "y": 320, "width": 60, "height": 20},
                {"x": 650, "y": 250, "width": 50, "height": 20},
                {"x": 100, "y": 180, "width": 60, "height": 20},
                {"x": 300, "y": 100, "width": 80, "height": 30},
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 800, "height": 100},
            ],
            "goal_y": 100,
            "start_pos": (50, 500),
            "target_deaths": 12,
        }

        # 第4關 - 危險跳躍
        levels[4] = {
            "name": "危險跳躍",
            "platforms": [
                {"x": 0, "y": 550, "width": 100, "height": 50},
                {"x": 150, "y": 480, "width": 40, "height": 15},
                {"x": 250, "y": 420, "width": 35, "height": 15},
                {"x": 350, "y": 380, "width": 40, "height": 15},
                {"x": 500, "y": 320, "width": 35, "height": 15},
                {"x": 600, "y": 260, "width": 40, "height": 15},
                {"x": 450, "y": 200, "width": 35, "height": 15},
                {"x": 200, "y": 140, "width": 40, "height": 15},
                {"x": 350, "y": 80, "width": 100, "height": 30},
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 800, "height": 100},
                {"x": 100, "y": 450, "width": 50, "height": 150},
            ],
            "goal_y": 80,
            "start_pos": (50, 500),
            "target_deaths": 15,
        }

        # 第5關 - 中級試煉
        levels[5] = {
            "name": "中級試煉",
            "platforms": [
                {"x": 0, "y": 550, "width": 80, "height": 50},
                {"x": 120, "y": 490, "width": 30, "height": 15},
                {"x": 200, "y": 440, "width": 25, "height": 15},
                {"x": 300, "y": 400, "width": 30, "height": 15},
                {"x": 400, "y": 350, "width": 25, "height": 15},
                {"x": 520, "y": 300, "width": 30, "height": 15},
                {"x": 600, "y": 240, "width": 25, "height": 15},
                {"x": 500, "y": 180, "width": 30, "height": 15},
                {"x": 350, "y": 120, "width": 25, "height": 15},
                {"x": 200, "y": 60, "width": 30, "height": 15},
                {"x": 300, "y": 0, "width": 100, "height": 30},
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 800, "height": 100},
                {"x": 80, "y": 450, "width": 40, "height": 100},
                {"x": 450, "y": 250, "width": 50, "height": 100},
            ],
            "goal_y": 0,
            "start_pos": (40, 500),
            "target_deaths": 20,
        }

        # 第6關 - 進階挑戰
        levels[6] = {
            "name": "進階挑戰",
            "platforms": [
                {"x": 0, "y": 550, "width": 80, "height": 30},
                {"x": 120, "y": 500, "width": 60, "height": 20},
                {"x": 250, "y": 460, "width": 55, "height": 18},
                {"x": 150, "y": 400, "width": 55, "height": 18},
                {"x": 320, "y": 350, "width": 50, "height": 15},
                {"x": 480, "y": 300, "width": 50, "height": 15},
                {"x": 350, "y": 240, "width": 50, "height": 15},
                {"x": 520, "y": 180, "width": 45, "height": 15},
                {"x": 300, "y": 120, "width": 100, "height": 25},
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},
                {"x": 80, "y": 470, "width": 25, "height": 80},
                {"x": 200, "y": 420, "width": 25, "height": 80},
                {"x": 280, "y": 370, "width": 25, "height": 80},
                {"x": 420, "y": 260, "width": 25, "height": 80},
                {"x": 460, "y": 200, "width": 25, "height": 80},
            ],
            "goal_y": 120,
            "start_pos": (40, 520),
            "target_deaths": 35,
        }

        # 第7關 - 簡潔挑戰
        levels[7] = {
            "name": "簡潔挑戰",
            "platforms": [
                {"x": 0, "y": 550, "width": 80, "height": 20},
                {"x": 180, "y": 450, "width": 40, "height": 15},
                {"x": 320, "y": 350, "width": 35, "height": 15},
                {"x": 480, "y": 250, "width": 35, "height": 15},
                {"x": 620, "y": 150, "width": 35, "height": 15},
                {"x": 480, "y": 80, "width": 120, "height": 20},
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},
                {"x": 80, "y": 400, "width": 20, "height": 120},
                {"x": 600, "y": 200, "width": 20, "height": 120},
            ],
            "goal_y": 80,
            "start_pos": (40, 530),
            "target_deaths": 25,
        }

        # 第8關 - 高手挑戰
        levels[8] = {
            "name": "高手挑戰",
            "platforms": [
                {"x": 0, "y": 550, "width": 60, "height": 30},
                {"x": 113, "y": 510, "width": 30, "height": 10},
                {"x": 190, "y": 450, "width": 30, "height": 10},
                {"x": 335, "y": 410, "width": 30, "height": 10},
                {"x": 213, "y": 350, "width": 30, "height": 10},
                {"x": 336, "y": 310, "width": 30, "height": 10},
                {"x": 486, "y": 250, "width": 30, "height": 10},
                {"x": 364, "y": 210, "width": 30, "height": 10},
                {"x": 487, "y": 150, "width": 30, "height": 10},
                {"x": 600, "y": 90, "width": 30, "height": 10},
                {"x": 500, "y": 30, "width": 80, "height": 25},
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},
                {"x": 80, "y": 480, "width": 15, "height": 150},
                {"x": 270, "y": 380, "width": 15, "height": 150},
                {"x": 160, "y": 320, "width": 15, "height": 150},
                {"x": 410, "y": 220, "width": 15, "height": 150},
                {"x": 320, "y": 180, "width": 15, "height": 150},
                {"x": 550, "y": 120, "width": 15, "height": 150},
                {"x": 450, "y": 60, "width": 15, "height": 150},
            ],
            "goal_y": 30,
            "start_pos": (30, 520),
            "target_deaths": 60,
        }

        # 第9關 - 螺旋迷宮
        levels[9] = {
            "name": "螺旋迷宮",
            "platforms": [
                {"x": 0, "y": 550, "width": 50, "height": 25},
                {"x": 200, "y": 480, "width": 25, "height": 12},
                {"x": 380, "y": 420, "width": 25, "height": 12},
                {"x": 550, "y": 360, "width": 25, "height": 12},
                {"x": 700, "y": 300, "width": 25, "height": 12},
                {"x": 600, "y": 240, "width": 25, "height": 12},
                {"x": 450, "y": 180, "width": 22, "height": 10},
                {"x": 280, "y": 120, "width": 22, "height": 10},
                {"x": 120, "y": 60, "width": 22, "height": 10},
                {"x": 300, "y": 0, "width": 22, "height": 10},
                {"x": 500, "y": -60, "width": 20, "height": 8},
                {"x": 680, "y": -120, "width": 20, "height": 8},
                {"x": 520, "y": -180, "width": 20, "height": 8},
                {"x": 340, "y": -240, "width": 20, "height": 8},
                {"x": 450, "y": -300, "width": 60, "height": 20},
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},
                {"x": 100, "y": 450, "width": 15, "height": 200},
                {"x": 290, "y": 390, "width": 15, "height": 200},
                {"x": 465, "y": 330, "width": 15, "height": 200},
                {"x": 625, "y": 270, "width": 15, "height": 200},
                {"x": 525, "y": 210, "width": 15, "height": 200},
                {"x": 365, "y": 150, "width": 14, "height": 250},
                {"x": 200, "y": 90, "width": 14, "height": 250},
                {"x": 50, "y": 30, "width": 14, "height": 250},
                {"x": 220, "y": -30, "width": 14, "height": 250},
                {"x": 400, "y": -90, "width": 13, "height": 300},
                {"x": 600, "y": -150, "width": 13, "height": 300},
                {"x": 430, "y": -210, "width": 13, "height": 300},
                {"x": 260, "y": -270, "width": 13, "height": 300},
                {"x": 0, "y": -100, "width": 20, "height": 500},
                {"x": 780, "y": -100, "width": 20, "height": 500},
            ],
            "goal_y": -300,
            "start_pos": (25, 525),
            "target_deaths": 80,
        }

        # 第10關 - 終極挑戰
        levels[10] = {
            "name": "終極挑戰",
            "platforms": [
                {"x": 0, "y": 550, "width": 45, "height": 20},
                {"x": 220, "y": 480, "width": 18, "height": 8},
                {"x": 420, "y": 420, "width": 18, "height": 8},
                {"x": 600, "y": 360, "width": 18, "height": 8},
                {"x": 750, "y": 300, "width": 18, "height": 8},
                {"x": 600, "y": 240, "width": 18, "height": 8},
                {"x": 400, "y": 180, "width": 16, "height": 6},
                {"x": 200, "y": 120, "width": 16, "height": 6},
                {"x": 50, "y": 60, "width": 16, "height": 6},
                {"x": 300, "y": 0, "width": 16, "height": 6},
                {"x": 550, "y": -60, "width": 14, "height": 5},
                {"x": 750, "y": -120, "width": 14, "height": 5},
                {"x": 600, "y": -180, "width": 14, "height": 5},
                {"x": 400, "y": -240, "width": 14, "height": 5},
                {"x": 150, "y": -300, "width": 14, "height": 5},
                {"x": 450, "y": -360, "width": 12, "height": 4},
                {"x": 700, "y": -420, "width": 12, "height": 4},
                {"x": 500, "y": -480, "width": 12, "height": 4},
                {"x": 250, "y": -540, "width": 12, "height": 4},
                {"x": 400, "y": -600, "width": 60, "height": 20},
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},
                {"x": 110, "y": 450, "width": 12, "height": 200},
                {"x": 320, "y": 390, "width": 12, "height": 200},
                {"x": 510, "y": 330, "width": 12, "height": 200},
                {"x": 675, "y": 270, "width": 12, "height": 200},
                {"x": 525, "y": 210, "width": 12, "height": 200},
                {"x": 300, "y": 150, "width": 11, "height": 250},
                {"x": 125, "y": 90, "width": 11, "height": 250},
                {"x": 25, "y": 30, "width": 11, "height": 250},
                {"x": 175, "y": -30, "width": 11, "height": 250},
                {"x": 425, "y": -90, "width": 10, "height": 300},
                {"x": 675, "y": -150, "width": 10, "height": 300},
                {"x": 525, "y": -210, "width": 10, "height": 300},
                {"x": 275, "y": -270, "width": 10, "height": 300},
                {"x": 75, "y": -330, "width": 10, "height": 300},
                {"x": 325, "y": -390, "width": 9, "height": 350},
                {"x": 575, "y": -450, "width": 9, "height": 350},
                {"x": 375, "y": -510, "width": 9, "height": 350},
                {"x": 125, "y": -570, "width": 9, "height": 350},
                {"x": 0, "y": -300, "width": 15, "height": 800},
                {"x": 785, "y": -300, "width": 15, "height": 800},
                {"x": 0, "y": -650, "width": 1200, "height": 40},
            ],
            "goal_y": -600,
            "start_pos": (22, 530),
            "target_deaths": 120,
        }

        # 第11關 - 天堂之塔
        levels[11] = {
            "name": "天堂之塔",
            "platforms": [
                {"x": 0, "y": 550, "width": 40, "height": 15},
                {"x": 240, "y": 480, "width": 15, "height": 6},
                {"x": 480, "y": 420, "width": 15, "height": 6},
                {"x": 700, "y": 360, "width": 15, "height": 6},
                {"x": 550, "y": 300, "width": 15, "height": 6},
                {"x": 350, "y": 240, "width": 15, "height": 6},
                {"x": 150, "y": 180, "width": 15, "height": 6},
                {"x": 400, "y": 120, "width": 15, "height": 6},
                {"x": 650, "y": 60, "width": 15, "height": 6},
                {"x": 500, "y": 0, "width": 15, "height": 6},
                {"x": 250, "y": -60, "width": 12, "height": 5},
                {"x": 50, "y": -120, "width": 12, "height": 5},
                {"x": 350, "y": -180, "width": 12, "height": 5},
                {"x": 600, "y": -240, "width": 12, "height": 5},
                {"x": 400, "y": -300, "width": 12, "height": 5},
                {"x": 150, "y": -360, "width": 12, "height": 5},
                {"x": 450, "y": -420, "width": 10, "height": 4},
                {"x": 700, "y": -480, "width": 10, "height": 4},
                {"x": 500, "y": -540, "width": 10, "height": 4},
                {"x": 250, "y": -600, "width": 10, "height": 4},
                {"x": 550, "y": -660, "width": 10, "height": 4},
                {"x": 750, "y": -720, "width": 10, "height": 4},
                {"x": 550, "y": -780, "width": 8, "height": 3},
                {"x": 300, "y": -840, "width": 8, "height": 3},
                {"x": 100, "y": -900, "width": 8, "height": 3},
                {"x": 400, "y": -960, "width": 8, "height": 3},
                {"x": 650, "y": -1020, "width": 8, "height": 3},
                {"x": 450, "y": -1080, "width": 8, "height": 3},
                {"x": 200, "y": -1140, "width": 6, "height": 3},
                {"x": 500, "y": -1200, "width": 6, "height": 3},
                {"x": 350, "y": -1260, "width": 80, "height": 20},
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},
                {"x": 120, "y": 450, "width": 8, "height": 200},
                {"x": 360, "y": 390, "width": 8, "height": 200},
                {"x": 590, "y": 330, "width": 8, "height": 200},
                {"x": 450, "y": 270, "width": 8, "height": 200},
                {"x": 250, "y": 210, "width": 8, "height": 200},
                {"x": 50, "y": 150, "width": 8, "height": 200},
                {"x": 275, "y": 90, "width": 8, "height": 200},
                {"x": 525, "y": 30, "width": 8, "height": 200},
                {"x": 150, "y": -30, "width": 7, "height": 250},
                {"x": 25, "y": -90, "width": 7, "height": 250},
                {"x": 225, "y": -150, "width": 7, "height": 250},
                {"x": 475, "y": -210, "width": 7, "height": 250},
                {"x": 325, "y": -270, "width": 7, "height": 250},
                {"x": 75, "y": -330, "width": 7, "height": 250},
                {"x": 325, "y": -390, "width": 6, "height": 300},
                {"x": 575, "y": -450, "width": 6, "height": 300},
                {"x": 375, "y": -510, "width": 6, "height": 300},
                {"x": 125, "y": -570, "width": 6, "height": 300},
                {"x": 425, "y": -630, "width": 6, "height": 300},
                {"x": 625, "y": -690, "width": 6, "height": 300},
                {"x": 425, "y": -750, "width": 5, "height": 350},
                {"x": 200, "y": -810, "width": 5, "height": 350},
                {"x": 50, "y": -870, "width": 5, "height": 350},
                {"x": 275, "y": -930, "width": 5, "height": 350},
                {"x": 525, "y": -990, "width": 5, "height": 350},
                {"x": 375, "y": -1050, "width": 5, "height": 350},
                {"x": 100, "y": -1110, "width": 4, "height": 400},
                {"x": 350, "y": -1170, "width": 4, "height": 400},
                {"x": 250, "y": -1230, "width": 4, "height": 400},
                {"x": 0, "y": -600, "width": 15, "height": 800},
                {"x": 785, "y": -600, "width": 15, "height": 800},
                {"x": 0, "y": -1320, "width": 1200, "height": 50},
            ],
            "goal_y": -1260,
            "start_pos": (20, 535),
            "target_deaths": 200,
        }

        return levels

    def get_level(self, level_num):
        """獲取指定關卡"""
        return self.levels.get(level_num)
