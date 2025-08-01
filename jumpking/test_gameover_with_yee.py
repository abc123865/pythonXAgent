#!/usr/bin/env python3
"""
測試失敗時的 Yee 音效播放
確保在遊戲失敗時同時播放失敗音效和 Yee 音效
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from jumpking import Game, GAME_OVER
import pygame


def test_gameover_with_yee():
    """測試包含 Yee 音效的遊戲失敗機制"""
    print("=== 失敗音效 + Yee 音效測試 ===")

    # 初始化遊戲
    game = Game()

    # 檢查音效是否載入成功
    print("\n🔊 音效載入狀態:")
    print(f"跳躍音效: {'✅' if game.jump_sound else '❌'}")
    print(f"通關音效: {'✅' if game.victory_sound else '❌'}")
    print(f"失敗音效: {'✅' if game.gameover_sound else '❌'}")
    print(f"Yee 音效: {'✅' if game.yee_sound else '❌'}")

    if not game.yee_sound:
        print("\n⚠️  Yee 音效未載入，請確保 sound/yee.mp3 檔案存在")

    # 模擬開始遊戲
    game.start_level(1)

    print("\n🎮 控制說明：")
    print("G - 觸發遊戲失敗 (播放失敗音效 + Yee 音效)")
    print("Y - 單獨播放 Yee 音效")
    print("R - 重新開始 (從失敗狀態)")
    print("M - 切換音效開關")
    print("+/- - 調整音量")
    print("ESC - 退出測試")
    print("\n🎵 開始測試...")

    clock = pygame.time.Clock()
    running = True

    while running:
        # 讓遊戲處理所有事件（包括定時器事件）
        game.handle_events()

        # 檢查遊戲是否被關閉
        if not game.running:
            running = False

        # 額外的測試控制
        keys = pygame.key.get_pressed()
        if keys[pygame.K_g]:
            print("🔥 觸發遊戲失敗...")
            game.game_over()
            print("   → 應該播放失敗音效，然後 0.5 秒後播放 Yee 音效")
            pygame.time.wait(100)  # 防止重複觸發
        elif keys[pygame.K_y]:
            print("🎵 播放 Yee 音效...")
            game.play_yee_sound()
            pygame.time.wait(100)  # 防止重複觸發

        # 更新遊戲狀態
        game.update()

        # 繪製遊戲
        game.draw()

        # 顯示當前狀態
        if game.state == GAME_OVER:
            pygame.display.set_caption("Jump King - 遊戲失敗狀態")
        else:
            pygame.display.set_caption("Jump King - 測試模式")

        clock.tick(60)

    game.quit()
    print("✅ 測試完成")


if __name__ == "__main__":
    test_gameover_with_yee()
