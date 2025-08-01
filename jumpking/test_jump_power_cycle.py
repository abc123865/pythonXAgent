#!/usr/bin/env python3
"""
測試跳躍力量循環系統
測試彈跳耐久達到最滿後的暫停和重新開始功能
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from jumpking import Game, PLAYING, MAX_JUMP_POWER
import pygame


def test_jump_power_cycle():
    """測試跳躍力量循環系統"""
    print("=== 跳躍力量循環系統測試 ===")

    # 初始化遊戲
    game = Game()

    # 開始第一關
    game.start_level(1)

    if game.state != PLAYING or not game.player:
        print("❌ 無法開始遊戲測試")
        return

    player = game.player

    print("\n🎮 控制說明：")
    print("SPACE - 開始/停止跳躍充能")
    print("觀察充能條的變化：")
    print("  - 正常充能：紅色條逐漸增長")
    print("  - 達到最大值：進入暫停狀態")
    print("  - 暫停期間：黃色/橙色閃爍")
    print("  - 暫停結束：重新開始充能")
    print("ESC - 退出測試")
    print("\n🔄 開始測試...")

    clock = pygame.time.Clock()
    running = True

    # 測試狀態
    test_phase = "waiting"  # waiting, charging, observing
    test_start_time = 0

    while running:
        # 處理事件
        game.handle_events()

        # 檢查遊戲是否被關閉
        if not game.running:
            running = False
            continue

        # 額外的測試控制
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            running = False

        # 自動測試充能循環
        if test_phase == "waiting":
            print("🚀 開始自動充能測試...")
            player.start_jump_charge()
            test_phase = "charging"
            test_start_time = pygame.time.get_ticks()

        elif test_phase == "charging":
            # 檢查是否達到暫停狀態
            if player.jump_power_paused:
                print(
                    f"⏸️  達到最大值，進入暫停狀態 (暫停時間: {player.jump_power_pause_timer} 幀)"
                )
                test_phase = "paused"

        elif test_phase == "paused":
            # 檢查是否暫停結束
            if not player.jump_power_paused:
                print("🔄 暫停結束，重新開始充能")
                test_phase = "recharging"

        elif test_phase == "recharging":
            # 觀察第二次循環
            if player.jump_power_paused:
                print("✅ 第二次循環成功，系統運作正常！")
                test_phase = "completed"

        elif test_phase == "completed":
            # 測試完成，繼續運行讓用戶觀察
            pass

        # 更新遊戲
        game.update()

        # 繪製遊戲
        game.draw()

        # 顯示測試資訊
        if game.player:
            status_text = (
                f"充能狀態: {'暫停' if player.jump_power_paused else '充能中'}"
            )
            if player.jump_power_paused:
                status_text += f" (剩餘: {player.jump_power_pause_timer} 幀)"
            else:
                status_text += f" (力量: {player.jump_power:.1f}/{MAX_JUMP_POWER})"

            pygame.display.set_caption(f"Jump King - 跳躍力量循環測試 - {status_text}")

        clock.tick(60)

    game.quit()
    print("✅ 測試完成")


if __name__ == "__main__":
    test_jump_power_cycle()
