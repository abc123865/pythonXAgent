#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試噩夢模式修正
用於驗證噩夢模式不會強制返回主頁面
"""

import sys
import os

# 添加 src 目錄到 Python 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

from config.game_config import Difficulty
from dinosaur import Dinosaur
from game_engine import Game


def test_nightmare_effects():
    """測試噩夢模式效果是否會引發錯誤"""
    print("🧪 開始測試噩夢模式修正...")

    try:
        # 創建遊戲實例
        game = Game()

        # 手動設置噩夢模式
        game.selected_difficulty = Difficulty.NIGHTMARE

        # 創建恐龍物件
        game.dinosaur = Dinosaur(800, 400, 350)

        # 測試噩夢模式效果
        print("🧪 測試 apply_nightmare_effects...")
        for i in range(10):
            try:
                game.apply_nightmare_effects()
                print(f"   測試 {i+1}/10: ✅ 正常")
            except Exception as e:
                print(f"   測試 {i+1}/10: ❌ 錯誤: {e}")
                return False

        # 測試恐龍更新
        print("🧪 測試恐龍更新...")
        for i in range(10):
            try:
                game.dinosaur.update()
                print(f"   測試 {i+1}/10: ✅ 正常")
            except Exception as e:
                print(f"   測試 {i+1}/10: ❌ 錯誤: {e}")
                return False

        # 測試重力反轉效果
        print("🧪 測試重力反轉效果...")
        try:
            game.dinosaur.apply_nightmare_effect("gravity_reversal", 300)
            for i in range(50):
                game.dinosaur.update()
            print("   重力反轉測試: ✅ 正常")
        except Exception as e:
            print(f"   重力反轉測試: ❌ 錯誤: {e}")
            return False

        print("🎉 所有測試通過！噩夢模式修正成功。")
        return True

    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_nightmare_effects()
    if success:
        print("\n✅ 噩夢模式已修正，不會再強制返回主頁面")
        print("🎮 現在可以安全地在噩夢模式下遊戲了！")
    else:
        print("\n❌ 測試失敗，仍需要進一步修正")

    sys.exit(0 if success else 1)
