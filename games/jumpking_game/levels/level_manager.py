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

        # 第1關 - 初學者之路（多路線入門）
        levels[1] = {
            "name": "初學者之路",
            "platforms": [
                {"x": 0, "y": 550, "width": 150, "height": 50},  # 起始平台
                # 第一層 - 兩條路線選擇
                {"x": 220, "y": 450, "width": 80, "height": 20},  # 左路
                {"x": 380, "y": 450, "width": 80, "height": 20},  # 右路
                # 第二層 - 路線延續
                {"x": 150, "y": 350, "width": 70, "height": 20},  # 左路延續
                {"x": 450, "y": 350, "width": 70, "height": 20},  # 右路延續
                {"x": 300, "y": 380, "width": 60, "height": 20},  # 中間連接
                # 第三層 - 匯合
                {"x": 200, "y": 250, "width": 80, "height": 20},  # 左匯合
                {"x": 350, "y": 250, "width": 80, "height": 20},  # 右匯合
                # 目標平台
                {"x": 250, "y": 100, "width": 200, "height": 30},  # 大目標平台
            ],
            "death_zones": [],
            "goal_y": 100,
            "start_pos": (75, 500),
            "target_deaths": 5,
        }

        # 第2關 - 分流冒險
        levels[2] = {
            "name": "分流冒險",
            "platforms": [
                {"x": 0, "y": 550, "width": 120, "height": 50},  # 起始平台
                # 第一層 - 三條路線分叉
                {"x": 180, "y": 450, "width": 60, "height": 20},  # 左路
                {"x": 320, "y": 470, "width": 60, "height": 20},  # 中路（稍低）
                {"x": 460, "y": 450, "width": 60, "height": 20},  # 右路
                # 第二層 - 路線發展
                {"x": 120, "y": 380, "width": 50, "height": 20},  # 左路延續
                {"x": 280, "y": 400, "width": 50, "height": 20},  # 中路延續
                {"x": 440, "y": 380, "width": 50, "height": 20},  # 右路延續
                # 第三層 - 挑戰區域
                {"x": 200, "y": 320, "width": 45, "height": 20},  # 左側匯合
                {"x": 350, "y": 330, "width": 50, "height": 20},  # 中央平台
                {"x": 500, "y": 320, "width": 45, "height": 20},  # 右側匯合
                # 第四層 - 預備跳躍
                {"x": 150, "y": 250, "width": 60, "height": 20},  # 左準備
                {"x": 400, "y": 250, "width": 60, "height": 20},  # 右準備
                # 目標區域
                {"x": 270, "y": 150, "width": 120, "height": 30},  # 大目標平台
            ],
            "death_zones": [
                {"x": 250, "y": 400, "width": 30, "height": 100},  # 中央小陷阱
                {"x": 340, "y": 280, "width": 20, "height": 80},  # 匯合點陷阱
            ],
            "goal_y": 150,
            "start_pos": (60, 500),
            "target_deaths": 8,
        }

        # 第3關 - 三叉路口
        levels[3] = {
            "name": "三叉路口",
            "platforms": [
                {"x": 0, "y": 550, "width": 100, "height": 50},  # 起始平台
                # 第一層 - 三條明顯路線
                {"x": 150, "y": 470, "width": 50, "height": 20},  # 左路
                {"x": 280, "y": 480, "width": 50, "height": 20},  # 中路（稍低）
                {"x": 410, "y": 470, "width": 50, "height": 20},  # 右路
                # 第二層 - 左路發展
                {"x": 80, "y": 400, "width": 45, "height": 20},  # 左路深入
                {"x": 200, "y": 420, "width": 40, "height": 20},  # 左路連接
                # 第二層 - 中路發展
                {"x": 320, "y": 410, "width": 45, "height": 20},  # 中路延續
                {"x": 250, "y": 350, "width": 40, "height": 20},  # 中路回轉
                # 第二層 - 右路發展
                {"x": 480, "y": 400, "width": 45, "height": 20},  # 右路深入
                {"x": 550, "y": 340, "width": 40, "height": 20},  # 右路延續
                # 第三層 - 路線交叉
                {"x": 120, "y": 320, "width": 50, "height": 20},  # 左交叉點
                {"x": 350, "y": 330, "width": 50, "height": 20},  # 中心交叉
                {"x": 480, "y": 320, "width": 50, "height": 20},  # 右交叉點
                # 第四層 - 匯合準備
                {"x": 180, "y": 250, "width": 45, "height": 20},  # 左匯合
                {"x": 380, "y": 260, "width": 45, "height": 20},  # 右匯合
                {"x": 280, "y": 200, "width": 60, "height": 20},  # 中央匯合
                # 目標平台
                {"x": 250, "y": 120, "width": 100, "height": 30},  # 目標
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 800, "height": 100},  # 底部
                {"x": 240, "y": 380, "width": 20, "height": 60},  # 中路陷阱
                {"x": 430, "y": 360, "width": 20, "height": 60},  # 右路陷阱
            ],
            "goal_y": 120,
            "start_pos": (50, 500),
            "target_deaths": 12,
        }

        # 第4關 - 四路挑戰
        levels[4] = {
            "name": "四路挑戰",
            "platforms": [
                {"x": 0, "y": 550, "width": 100, "height": 50},  # 起始平台
                # 第一層 - 四條路線選擇
                {"x": 140, "y": 480, "width": 40, "height": 15},  # 左路
                {"x": 220, "y": 490, "width": 40, "height": 15},  # 左中路
                {"x": 300, "y": 490, "width": 40, "height": 15},  # 右中路
                {"x": 380, "y": 480, "width": 40, "height": 15},  # 右路
                # 第二層 - 路線發展
                {"x": 80, "y": 420, "width": 35, "height": 15},  # 左路深入
                {"x": 180, "y": 430, "width": 35, "height": 15},  # 左中延續
                {"x": 280, "y": 430, "width": 35, "height": 15},  # 右中延續
                {"x": 430, "y": 420, "width": 35, "height": 15},  # 右路深入
                # 第三層 - 交叉連接
                {"x": 120, "y": 360, "width": 40, "height": 15},  # 左交叉
                {"x": 240, "y": 370, "width": 40, "height": 15},  # 中左交叉
                {"x": 320, "y": 370, "width": 40, "height": 15},  # 中右交叉
                {"x": 440, "y": 360, "width": 40, "height": 15},  # 右交叉
                # 第四層 - 路線匯合
                {"x": 160, "y": 300, "width": 45, "height": 15},  # 左側匯合
                {"x": 280, "y": 310, "width": 50, "height": 15},  # 中央匯合
                {"x": 400, "y": 300, "width": 45, "height": 15},  # 右側匯合
                # 第五層 - 接近目標
                {"x": 200, "y": 240, "width": 40, "height": 15},  # 左準備
                {"x": 340, "y": 250, "width": 40, "height": 15},  # 右準備
                # 第六層 - 最終跳躍
                {"x": 250, "y": 180, "width": 50, "height": 15},  # 最終準備
                # 目標平台
                {"x": 300, "y": 100, "width": 120, "height": 30},  # 大目標
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 800, "height": 100},  # 底部
                {"x": 200, "y": 450, "width": 20, "height": 80},  # 第一層陷阱
                {"x": 360, "y": 390, "width": 20, "height": 70},  # 第三層陷阱
                {"x": 270, "y": 320, "width": 15, "height": 60},  # 匯合陷阱
            ],
            "goal_y": 100,
            "start_pos": (50, 500),
            "target_deaths": 15,
        }

        # 第5關 - 環形迴路
        levels[5] = {
            "name": "環形迴路",
            "platforms": [
                {"x": 0, "y": 550, "width": 80, "height": 50},  # 起始平台
                # 第一層 - 雙路分叉
                {"x": 120, "y": 480, "width": 40, "height": 15},  # 左路入口
                {"x": 240, "y": 480, "width": 40, "height": 15},  # 右路入口
                # 第二層 - 左環形路線
                {"x": 60, "y": 420, "width": 35, "height": 15},  # 左環左側
                {"x": 150, "y": 400, "width": 35, "height": 15},  # 左環頂部
                {"x": 180, "y": 340, "width": 35, "height": 15},  # 左環右側
                {"x": 120, "y": 280, "width": 35, "height": 15},  # 左環底部
                # 第二層 - 右環形路線
                {"x": 300, "y": 420, "width": 35, "height": 15},  # 右環左側
                {"x": 380, "y": 400, "width": 35, "height": 15},  # 右環頂部
                {"x": 420, "y": 340, "width": 35, "height": 15},  # 右環右側
                {"x": 360, "y": 280, "width": 35, "height": 15},  # 右環底部
                # 第三層 - 中央連接區
                {"x": 200, "y": 360, "width": 40, "height": 15},  # 中央橋樑
                {"x": 240, "y": 300, "width": 40, "height": 15},  # 中央平台
                # 第四層 - 向上路線
                {"x": 160, "y": 220, "width": 40, "height": 15},  # 左上路
                {"x": 300, "y": 220, "width": 40, "height": 15},  # 右上路
                {"x": 230, "y": 160, "width": 50, "height": 15},  # 匯合平台
                # 第五層 - 最終階段
                {"x": 180, "y": 100, "width": 40, "height": 15},  # 左最終
                {"x": 280, "y": 100, "width": 40, "height": 15},  # 右最終
                # 目標平台
                {"x": 200, "y": 40, "width": 100, "height": 30},  # 目標
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 800, "height": 100},  # 底部
                {"x": 80, "y": 450, "width": 15, "height": 100},  # 左環陷阱
                {"x": 200, "y": 320, "width": 15, "height": 80},  # 中央陷阱
                {"x": 340, "y": 450, "width": 15, "height": 100},  # 右環陷阱
                {"x": 220, "y": 130, "width": 15, "height": 60},  # 最終陷阱
            ],
            "goal_y": 40,
            "start_pos": (40, 500),
            "target_deaths": 20,
        }

        # 第6關 - 網格迷宮
        levels[6] = {
            "name": "網格迷宮",
            "platforms": [
                {"x": 0, "y": 550, "width": 80, "height": 30},  # 起始平台
                # 第一層 - 三路分叉
                {"x": 120, "y": 480, "width": 50, "height": 20},  # 左路
                {"x": 250, "y": 490, "width": 50, "height": 20},  # 中路
                {"x": 380, "y": 480, "width": 50, "height": 20},  # 右路
                # 第二層 - 網格擴展
                {"x": 80, "y": 420, "width": 45, "height": 18},  # 左外
                {"x": 180, "y": 430, "width": 45, "height": 18},  # 左內
                {"x": 280, "y": 430, "width": 45, "height": 18},  # 中央
                {"x": 380, "y": 430, "width": 45, "height": 18},  # 右內
                {"x": 480, "y": 420, "width": 45, "height": 18},  # 右外
                # 第三層 - 交錯連接
                {"x": 120, "y": 370, "width": 40, "height": 15},  # 左連接
                {"x": 220, "y": 380, "width": 40, "height": 15},  # 左中連接
                {"x": 320, "y": 380, "width": 40, "height": 15},  # 右中連接
                {"x": 420, "y": 370, "width": 40, "height": 15},  # 右連接
                # 第四層 - 中間匯合
                {"x": 160, "y": 320, "width": 50, "height": 15},  # 左匯合
                {"x": 300, "y": 330, "width": 60, "height": 15},  # 中央大平台
                {"x": 440, "y": 320, "width": 50, "height": 15},  # 右匯合
                # 第五層 - 最終路線選擇
                {"x": 100, "y": 260, "width": 45, "height": 15},  # 左最終路
                {"x": 200, "y": 270, "width": 45, "height": 15},  # 左中最終
                {"x": 350, "y": 270, "width": 45, "height": 15},  # 右中最終
                {"x": 450, "y": 260, "width": 45, "height": 15},  # 右最終路
                # 第六層 - 預備跳躍
                {"x": 180, "y": 200, "width": 50, "height": 15},  # 左預備
                {"x": 320, "y": 210, "width": 50, "height": 15},  # 右預備
                # 目標區域
                {"x": 250, "y": 140, "width": 100, "height": 25},  # 大目標平台
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},  # 底部死亡區域
                {"x": 150, "y": 450, "width": 20, "height": 80},  # 左路陷阱
                {"x": 350, "y": 450, "width": 20, "height": 80},  # 右路陷阱
                {"x": 260, "y": 350, "width": 20, "height": 80},  # 中央陷阱
                {"x": 270, "y": 230, "width": 15, "height": 60},  # 最終陷阱
            ],
            "goal_y": 140,
            "start_pos": (40, 520),
            "target_deaths": 30,
        }

        # 第7關 - 平衡之道
        levels[7] = {
            "name": "平衡之道",
            "platforms": [
                {"x": 0, "y": 550, "width": 100, "height": 30},  # 起始平台（較大）
                {"x": 180, "y": 470, "width": 50, "height": 18},  # 第一跳：向右
                {"x": 350, "y": 400, "width": 45, "height": 15},  # 第二跳：向右上
                {"x": 200, "y": 330, "width": 45, "height": 15},  # 第三跳：向左上
                {"x": 80, "y": 260, "width": 45, "height": 15},  # 第四跳：向左
                {"x": 280, "y": 190, "width": 50, "height": 15},  # 第五跳：向右上
                {"x": 480, "y": 140, "width": 45, "height": 15},  # 第六跳：向右
                {"x": 300, "y": 80, "width": 45, "height": 15},  # 第七跳：向左上
                {"x": 400, "y": 20, "width": 100, "height": 25},  # 目標平台（較大）
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},  # 底部死亡區域
                {"x": 125, "y": 440, "width": 25, "height": 60},  # 第一跳後的陷阱
                {"x": 320, "y": 370, "width": 25, "height": 60},  # 第二跳後的陷阱
                {"x": 170, "y": 300, "width": 25, "height": 60},  # 第三跳後的陷阱
                {"x": 250, "y": 160, "width": 25, "height": 60},  # 第五跳後的陷阱
                {"x": 450, "y": 110, "width": 25, "height": 60},  # 第六跳後的陷阱
            ],
            "goal_y": 20,
            "start_pos": (50, 520),  # 起始平台中心
            "target_deaths": 18,  # 調整為更合理的死亡次數
        }

        # 第8關 - 多路探索
        levels[8] = {
            "name": "多路探索",
            "platforms": [
                # 起始區域
                {"x": 0, "y": 550, "width": 120, "height": 30},  # 起始平台（大）
                # 第一層 - 三條路線分叉
                {"x": 200, "y": 480, "width": 50, "height": 15},  # 左路
                {"x": 350, "y": 490, "width": 50, "height": 15},  # 中路
                {"x": 500, "y": 480, "width": 50, "height": 15},  # 右路
                # 第二層 - 左路線延續
                {"x": 80, "y": 420, "width": 45, "height": 15},  # 左路
                {"x": 280, "y": 430, "width": 45, "height": 15},  # 左路延續
                # 第二層 - 中路線延續
                {"x": 420, "y": 430, "width": 45, "height": 15},  # 中路
                {"x": 270, "y": 380, "width": 45, "height": 15},  # 中路回轉
                # 第二層 - 右路線延續
                {"x": 600, "y": 420, "width": 45, "height": 15},  # 右路
                {"x": 450, "y": 380, "width": 45, "height": 15},  # 右路回轉
                # 第三層 - 路線開始匯合
                {"x": 150, "y": 360, "width": 50, "height": 15},  # 左中匯合點
                {"x": 350, "y": 330, "width": 50, "height": 15},  # 中心平台
                {"x": 550, "y": 360, "width": 50, "height": 15},  # 右中匯合點
                # 第四層 - 更多選擇
                {"x": 100, "y": 300, "width": 40, "height": 15},  # 左側選擇
                {"x": 250, "y": 280, "width": 60, "height": 15},  # 中央大平台
                {"x": 450, "y": 300, "width": 40, "height": 15},  # 右側選擇
                {"x": 600, "y": 280, "width": 40, "height": 15},  # 遠右選擇
                # 第五層 - 接近匯合
                {"x": 180, "y": 230, "width": 50, "height": 15},  # 左側
                {"x": 380, "y": 240, "width": 50, "height": 15},  # 中央
                {"x": 520, "y": 230, "width": 50, "height": 15},  # 右側
                # 第六層 - 最終匯合前
                {"x": 120, "y": 180, "width": 45, "height": 15},  # 左
                {"x": 300, "y": 190, "width": 60, "height": 15},  # 中央大平台
                {"x": 480, "y": 180, "width": 45, "height": 15},  # 右
                # 第七層 - 接近終點
                {"x": 200, "y": 130, "width": 50, "height": 15},  # 左路終點接近
                {"x": 400, "y": 140, "width": 50, "height": 15},  # 右路終點接近
                # 第八層 - 最終跳躍準備
                {"x": 300, "y": 80, "width": 70, "height": 15},  # 最終準備平台
                # 目標平台
                {"x": 350, "y": 20, "width": 150, "height": 30},  # 大目標平台
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},  # 底部死亡區域
                # 減少死亡陷阱，讓關卡更友善
                {"x": 120, "y": 450, "width": 20, "height": 80},  # 第一層小陷阱
                {"x": 470, "y": 450, "width": 20, "height": 80},  # 第一層小陷阱
                {"x": 320, "y": 350, "width": 20, "height": 60},  # 中層小陷阱
                {"x": 250, "y": 200, "width": 20, "height": 60},  # 上層小陷阱
                {"x": 450, "y": 200, "width": 20, "height": 60},  # 上層小陷阱
            ],
            "goal_y": 20,
            "start_pos": (60, 520),  # 起始平台中心
            "target_deaths": 25,  # 減少目標死亡數，因為更注重探索而非難度
        }

        # 第9關 - 雙螺旋塔
        levels[9] = {
            "name": "雙螺旋塔",
            "platforms": [
                {"x": 0, "y": 550, "width": 80, "height": 25},  # 起始平台
                # 第一層 - 雙路分叉
                {"x": 150, "y": 480, "width": 40, "height": 15},  # 左螺旋入口
                {"x": 350, "y": 480, "width": 40, "height": 15},  # 右螺旋入口
                # 第二層 - 左螺旋路線
                {"x": 80, "y": 420, "width": 35, "height": 12},  # 左螺旋第1段
                {"x": 200, "y": 390, "width": 35, "height": 12},  # 左螺旋第2段
                {"x": 120, "y": 330, "width": 35, "height": 12},  # 左螺旋第3段
                {"x": 180, "y": 270, "width": 35, "height": 12},  # 左螺旋第4段
                # 第二層 - 右螺旋路線
                {"x": 420, "y": 420, "width": 35, "height": 12},  # 右螺旋第1段
                {"x": 300, "y": 390, "width": 35, "height": 12},  # 右螺旋第2段
                {"x": 380, "y": 330, "width": 35, "height": 12},  # 右螺旋第3段
                {"x": 320, "y": 270, "width": 35, "height": 12},  # 右螺旋第4段
                # 第三層 - 螺旋交匯
                {"x": 140, "y": 210, "width": 40, "height": 12},  # 左螺旋上升
                {"x": 360, "y": 210, "width": 40, "height": 12},  # 右螺旋上升
                {"x": 250, "y": 180, "width": 50, "height": 15},  # 中央交匯平台
                # 第四層 - 向上路線
                {"x": 100, "y": 150, "width": 35, "height": 12},  # 左上路
                {"x": 200, "y": 120, "width": 35, "height": 12},  # 中左上路
                {"x": 300, "y": 120, "width": 35, "height": 12},  # 中右上路
                {"x": 400, "y": 150, "width": 35, "height": 12},  # 右上路
                # 第五層 - 最終螺旋
                {"x": 150, "y": 90, "width": 30, "height": 10},  # 左最終螺旋
                {"x": 320, "y": 90, "width": 30, "height": 10},  # 右最終螺旋
                {"x": 220, "y": 60, "width": 35, "height": 10},  # 頂部連接
                # 第六層 - 深入地下
                {"x": 180, "y": 0, "width": 30, "height": 10},  # 地下入口左
                {"x": 290, "y": 0, "width": 30, "height": 10},  # 地下入口右
                {"x": 120, "y": -60, "width": 30, "height": 10},  # 地下左路
                {"x": 350, "y": -60, "width": 30, "height": 10},  # 地下右路
                {"x": 240, "y": -120, "width": 40, "height": 10},  # 地下匯合
                # 目標平台
                {"x": 200, "y": -180, "width": 100, "height": 20},  # 地下目標
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 1200, "height": 100},  # 底部死亡區域
                {"x": 100, "y": 450, "width": 15, "height": 150},  # 左入口陷阱
                {"x": 385, "y": 450, "width": 15, "height": 150},  # 右入口陷阱
                {"x": 240, "y": 340, "width": 15, "height": 100},  # 中央陷阱
                {"x": 170, "y": 30, "width": 15, "height": 80},  # 地下入口陷阱
                {"x": 315, "y": 30, "width": 15, "height": 80},  # 地下入口陷阱
                {"x": 0, "y": -200, "width": 20, "height": 300},  # 左邊界
                {"x": 480, "y": -200, "width": 20, "height": 300},  # 右邊界
            ],
            "goal_y": -180,
            "start_pos": (40, 525),
            "target_deaths": 50,  # 降低難度
        }

        # 第10關 - 多元終極
        levels[10] = {
            "name": "多元終極",
            "platforms": [
                {"x": 0, "y": 550, "width": 80, "height": 20},  # 起始平台
                # 第一層 - 三路終極分叉
                {"x": 150, "y": 480, "width": 40, "height": 15},  # 左路
                {"x": 280, "y": 490, "width": 40, "height": 15},  # 中路
                {"x": 410, "y": 480, "width": 40, "height": 15},  # 右路
                # 第二層 - 路線深入
                {"x": 100, "y": 420, "width": 35, "height": 12},  # 左路深入
                {"x": 200, "y": 430, "width": 35, "height": 12},  # 左中連接
                {"x": 300, "y": 430, "width": 35, "height": 12},  # 右中連接
                {"x": 450, "y": 420, "width": 35, "height": 12},  # 右路深入
                # 第三層 - 挑戰區域
                {"x": 80, "y": 360, "width": 30, "height": 10},  # 左挑戰
                {"x": 180, "y": 370, "width": 30, "height": 10},  # 左中挑戰
                {"x": 280, "y": 380, "width": 40, "height": 10},  # 中央平台
                {"x": 370, "y": 370, "width": 30, "height": 10},  # 右中挑戰
                {"x": 470, "y": 360, "width": 30, "height": 10},  # 右挑戰
                # 第四層 - 地下進入
                {"x": 120, "y": 300, "width": 35, "height": 10},  # 左地下入口
                {"x": 250, "y": 310, "width": 50, "height": 10},  # 中央地下入口
                {"x": 400, "y": 300, "width": 35, "height": 10},  # 右地下入口
                # 第五層 - 地下路線
                {"x": 80, "y": 240, "width": 30, "height": 8},  # 左地下
                {"x": 200, "y": 250, "width": 30, "height": 8},  # 左中地下
                {"x": 320, "y": 250, "width": 30, "height": 8},  # 右中地下
                {"x": 440, "y": 240, "width": 30, "height": 8},  # 右地下
                # 第六層 - 深入地下
                {"x": 140, "y": 180, "width": 30, "height": 8},  # 左深地下
                {"x": 260, "y": 190, "width": 40, "height": 8},  # 中深地下
                {"x": 380, "y": 180, "width": 30, "height": 8},  # 右深地下
                # 第七層 - 最深層
                {"x": 100, "y": 120, "width": 25, "height": 6},  # 左最深
                {"x": 200, "y": 130, "width": 25, "height": 6},  # 左中最深
                {"x": 300, "y": 130, "width": 25, "height": 6},  # 右中最深
                {"x": 400, "y": 120, "width": 25, "height": 6},  # 右最深
                # 第八層 - 地底匯合
                {"x": 180, "y": 60, "width": 35, "height": 8},  # 左匯合
                {"x": 320, "y": 60, "width": 35, "height": 8},  # 右匯合
                # 第九層 - 最終挑戰
                {"x": 220, "y": 0, "width": 40, "height": 8},  # 最終平台
                {"x": 160, "y": -60, "width": 30, "height": 6},  # 左最終
                {"x": 290, "y": -60, "width": 30, "height": 6},  # 右最終
                # 目標平台
                {"x": 200, "y": -120, "width": 80, "height": 20},  # 終極目標
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 800, "height": 100},  # 底部死亡區域
                {"x": 220, "y": 450, "width": 15, "height": 80},  # 第一層陷阱
                {"x": 340, "y": 340, "width": 15, "height": 100},  # 第三層陷阱
                {"x": 160, "y": 270, "width": 12, "height": 80},  # 地下陷阱
                {"x": 360, "y": 270, "width": 12, "height": 80},  # 地下陷阱
                {"x": 240, "y": 150, "width": 10, "height": 80},  # 深層陷阱
                {"x": 250, "y": 30, "width": 10, "height": 60},  # 最終陷阱
                {"x": 0, "y": -150, "width": 15, "height": 300},  # 左邊界
                {"x": 485, "y": -150, "width": 15, "height": 300},  # 右邊界
            ],
            "goal_y": -120,
            "start_pos": (40, 530),
            "target_deaths": 60,  # 降低難度
        }

        # 第11關 - 天堂三路
        levels[11] = {
            "name": "天堂三路",
            "platforms": [
                {"x": 0, "y": 550, "width": 60, "height": 20},  # 起始平台
                # 第一層 - 三路通天
                {"x": 120, "y": 480, "width": 30, "height": 12},  # 左天路
                {"x": 220, "y": 490, "width": 30, "height": 12},  # 中天路
                {"x": 320, "y": 480, "width": 30, "height": 12},  # 右天路
                # 第二層 - 路線發展
                {"x": 80, "y": 420, "width": 25, "height": 10},  # 左路發展
                {"x": 160, "y": 430, "width": 25, "height": 10},  # 左中連接
                {"x": 240, "y": 430, "width": 25, "height": 10},  # 中央發展
                {"x": 300, "y": 430, "width": 25, "height": 10},  # 右中連接
                {"x": 380, "y": 420, "width": 25, "height": 10},  # 右路發展
                # 第三層 - 向上攀登
                {"x": 100, "y": 360, "width": 20, "height": 8},  # 左攀登
                {"x": 180, "y": 370, "width": 20, "height": 8},  # 左中攀登
                {"x": 260, "y": 380, "width": 30, "height": 8},  # 中央攀登（較大）
                {"x": 320, "y": 370, "width": 20, "height": 8},  # 右中攀登
                {"x": 400, "y": 360, "width": 20, "height": 8},  # 右攀登
                # 第四層 - 天空區域
                {"x": 120, "y": 300, "width": 20, "height": 8},  # 左天空
                {"x": 200, "y": 310, "width": 20, "height": 8},  # 左中天空
                {"x": 280, "y": 320, "width": 25, "height": 8},  # 中央天空
                {"x": 340, "y": 310, "width": 20, "height": 8},  # 右中天空
                {"x": 420, "y": 300, "width": 20, "height": 8},  # 右天空
                # 第五層 - 雲層穿越
                {"x": 80, "y": 240, "width": 18, "height": 6},  # 左雲層
                {"x": 160, "y": 250, "width": 18, "height": 6},  # 左中雲層
                {"x": 240, "y": 260, "width": 20, "height": 6},  # 中央雲層
                {"x": 320, "y": 250, "width": 18, "height": 6},  # 右中雲層
                {"x": 400, "y": 240, "width": 18, "height": 6},  # 右雲層
                # 第六層 - 高空區域
                {"x": 120, "y": 180, "width": 15, "height": 6},  # 左高空
                {"x": 200, "y": 190, "width": 15, "height": 6},  # 左中高空
                {"x": 280, "y": 200, "width": 20, "height": 6},  # 中央高空
                {"x": 340, "y": 190, "width": 15, "height": 6},  # 右中高空
                {"x": 420, "y": 180, "width": 15, "height": 6},  # 右高空
                # 第七層 - 接近天頂
                {"x": 160, "y": 120, "width": 15, "height": 6},  # 左天頂接近
                {"x": 240, "y": 130, "width": 15, "height": 6},  # 中左天頂
                {"x": 300, "y": 140, "width": 18, "height": 6},  # 中央天頂
                {"x": 360, "y": 130, "width": 15, "height": 6},  # 中右天頂
                {"x": 440, "y": 120, "width": 15, "height": 6},  # 右天頂接近
                # 第八層 - 天頂前的最後挑戰
                {"x": 180, "y": 60, "width": 12, "height": 5},  # 左最終
                {"x": 260, "y": 70, "width": 12, "height": 5},  # 中左最終
                {"x": 320, "y": 80, "width": 15, "height": 5},  # 中央最終
                {"x": 380, "y": 70, "width": 12, "height": 5},  # 中右最終
                {"x": 460, "y": 60, "width": 12, "height": 5},  # 右最終
                # 第九層 - 天堂之門
                {"x": 220, "y": 0, "width": 15, "height": 5},  # 左天堂門
                {"x": 300, "y": 10, "width": 20, "height": 5},  # 中央天堂門
                {"x": 380, "y": 0, "width": 15, "height": 5},  # 右天堂門
                # 最終目標 - 天堂
                {"x": 250, "y": -60, "width": 100, "height": 20},  # 天堂平台
            ],
            "death_zones": [
                {"x": 0, "y": 600, "width": 800, "height": 100},  # 底部死亡區域
                {"x": 200, "y": 450, "width": 10, "height": 80},  # 第一層陷阱
                {"x": 140, "y": 390, "width": 8, "height": 70},  # 第二層陷阱
                {"x": 340, "y": 390, "width": 8, "height": 70},  # 第二層陷阱
                {"x": 220, "y": 330, "width": 8, "height": 60},  # 第四層陷阱
                {"x": 360, "y": 330, "width": 8, "height": 60},  # 第四層陷阱
                {"x": 180, "y": 270, "width": 6, "height": 50},  # 第五層陷阱
                {"x": 280, "y": 270, "width": 6, "height": 50},  # 第五層陷阱
                {"x": 380, "y": 270, "width": 6, "height": 50},  # 第五層陷阱
                {"x": 240, "y": 210, "width": 6, "height": 40},  # 第六層陷阱
                {"x": 320, "y": 210, "width": 6, "height": 40},  # 第六層陷阱
                {"x": 280, "y": 150, "width": 5, "height": 30},  # 第七層陷阱
                {"x": 340, "y": 90, "width": 5, "height": 30},  # 第八層陷阱
                {"x": 270, "y": 30, "width": 5, "height": 30},  # 天堂門陷阱
                {"x": 0, "y": -80, "width": 15, "height": 200},  # 左邊界
                {"x": 485, "y": -80, "width": 15, "height": 200},  # 右邊界
            ],
            "goal_y": -60,
            "start_pos": (30, 530),
            "target_deaths": 100,  # 降低難度但保持挑戰性
        }

        return levels

    def get_level(self, level_num):
        """獲取指定關卡"""
        return self.levels.get(level_num)
