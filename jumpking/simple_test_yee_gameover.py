#!/usr/bin/env python3
"""
簡單測試失敗音效播放
測試失敗時同時播放失敗音效和 Yee 音效
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from jumpking import Game
import pygame
import time


def simple_test_gameover_sounds():
    """簡單測試失敗音效播放"""
    print("=== 簡單失敗音效測試 ===")

    # 初始化遊戲
    game = Game()

    print("🔊 音效載入狀態:")
    print(f"失敗音效: {'✅' if game.gameover_sound else '❌'}")
    print(f"Yee 音效: {'✅' if game.yee_sound else '❌'}")

    if game.gameover_sound and game.yee_sound:
        print("\n🎵 播放失敗音效序列...")

        # 直接呼叫失敗音效方法
        game.play_gameover_sound()
        print("✅ 失敗音效已觸發")
        print("   → 應該聽到失敗音效，然後 0.5 秒後聽到 Yee 音效")

        # 等待音效播放完成
        print("\n⏰ 等待音效播放...")
        for i in range(3):
            print(f"   {3-i} 秒...")
            time.sleep(1)

        print("\n🎵 測試單獨播放 Yee 音效...")
        game.play_yee_sound()
        print("✅ Yee 音效已播放")

        time.sleep(2)

    else:
        print("❌ 部分音效未載入，無法進行測試")

    game.quit()
    print("\n✅ 測試完成")


if __name__ == "__main__":
    simple_test_gameover_sounds()
