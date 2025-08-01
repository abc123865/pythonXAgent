#!/usr/bin/env python3
"""
Jump King 存檔管理器
處理遊戲進度的儲存和載入
"""
import json
import os
import sys

# 添加 src 目錄到路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(current_dir), "src")
sys.path.insert(0, src_dir)

try:
    from game_config import SAVE_FILE, TOTAL_LEVELS
except ImportError:
    SAVE_FILE = "jumpking_save.json"
    TOTAL_LEVELS = 11


class SaveManager:
    def __init__(self):
        self.save_file = os.path.join(os.path.dirname(__file__), SAVE_FILE)
        self.unlocked_levels = 1
        self.level_stats = {}
        self.load_progress()

    def load_progress(self):
        """載入遊戲進度"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.unlocked_levels = data.get("unlocked_levels", 1)
                    self.level_stats = data.get("level_stats", {})
                    print(f"成功載入存檔: {self.save_file}")
            else:
                print("沒有找到存檔檔案，使用預設設定")
        except Exception as e:
            print(f"載入存檔失敗: {e}")
            self.unlocked_levels = 1
            self.level_stats = {}

    def save_progress(self):
        """儲存遊戲進度"""
        try:
            data = {
                "unlocked_levels": self.unlocked_levels,
                "level_stats": self.level_stats,
            }
            with open(self.save_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"成功儲存進度: {self.save_file}")
        except Exception as e:
            print(f"儲存進度失敗: {e}")

    def update_level_stats(self, level_num, deaths, completed=False):
        """更新關卡統計"""
        level_key = str(level_num)

        if level_key not in self.level_stats:
            self.level_stats[level_key] = {
                "deaths": 0,
                "completed": False,
                "best_deaths": None,
            }

        self.level_stats[level_key]["deaths"] = deaths

        if completed:
            self.level_stats[level_key]["completed"] = True
            # 更新最佳記錄
            if (
                self.level_stats[level_key]["best_deaths"] is None
                or deaths < self.level_stats[level_key]["best_deaths"]
            ):
                self.level_stats[level_key]["best_deaths"] = deaths

    def unlock_next_level(self, current_level):
        """解鎖下一關"""
        if current_level < TOTAL_LEVELS:
            self.unlocked_levels = max(self.unlocked_levels, current_level + 1)

    def get_next_unfinished_level(self):
        """獲取下一個未完成的關卡"""
        for i in range(1, self.unlocked_levels + 1):
            if (
                str(i) not in self.level_stats
                or not self.level_stats[str(i)]["completed"]
            ):
                return i
        return 1

    def reset_progress(self):
        """重置所有進度"""
        self.unlocked_levels = 1
        self.level_stats = {}
        self.save_progress()

    def get_completion_percentage(self):
        """獲取完成百分比"""
        completed_levels = sum(
            1
            for level_key in self.level_stats
            if self.level_stats[level_key]["completed"]
        )
        return (completed_levels / TOTAL_LEVELS) * 100

    def get_total_deaths(self):
        """獲取總死亡次數"""
        return sum(stats.get("deaths", 0) for stats in self.level_stats.values())
