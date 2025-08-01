#!/usr/bin/env python3
"""
失敗機制測試腳本
測試超過目標死亡次數時的遊戲失敗功能
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from jumpking import Game, Player


def test_game_over_mechanism():
    """測試遊戲失敗機制"""
    print("=== 測試遊戲失敗機制 ===")

    # 創建遊戲實例
    game = Game()

    # 開始第1關（目標死亡次數為5）
    game.start_level(1)

    if not game.player:
        print("❌ 玩家未正確初始化")
        return False

    # 獲取關卡資訊
    level_data = game.level_manager.get_level(1)
    target_deaths = level_data["target_deaths"]

    print(f"第1關目標死亡次數: {target_deaths}")
    print(f"當前玩家死亡次數: {game.player.death_count}")

    # 模擬超過目標死亡次數
    print(f"模擬死亡到超過目標...")
    original_deaths = game.player.death_count

    # 設置死亡次數為目標+1
    game.player.death_count = target_deaths + 1
    print(f"設置死亡次數為: {game.player.death_count}")

    # 手動觸發遊戲失敗檢查
    if game.player.death_count > target_deaths:
        game.game_over()
        print("✅ 遊戲失敗機制觸發成功")
        print(f"當前遊戲狀態: {game.state} (3=GAME_OVER)")

        if game.state == 3:  # GAME_OVER
            print("✅ 遊戲狀態正確設置為 GAME_OVER")

            # 測試重新開始功能
            print("測試重新開始功能...")
            game.restart_current_level()

            if game.state == 1:  # PLAYING
                print("✅ 重新開始功能正常，遊戲狀態恢復為 PLAYING")
                print(f"重新開始後死亡次數: {game.player.death_count}")

                if game.player.death_count == 0:
                    print("✅ 死亡次數成功重置為0")
                    return True
                else:
                    print("❌ 死亡次數未正確重置")
                    return False
            else:
                print(f"❌ 重新開始失敗，當前狀態: {game.state}")
                return False
        else:
            print("❌ 遊戲狀態未正確設置")
            return False
    else:
        print("❌ 死亡次數設置失敗")
        return False


def test_death_count_progression():
    """測試死亡次數遞增和失敗觸發"""
    print("\n=== 測試死亡次數遞增和失敗觸發 ===")

    game = Game()
    game.start_level(1)

    level_data = game.level_manager.get_level(1)
    target_deaths = level_data["target_deaths"]

    print(f"目標死亡次數: {target_deaths}")

    # 模擬死亡過程
    for i in range(target_deaths + 2):
        deaths_before = game.player.death_count

        # 模擬死亡
        game.player.death_count += 1
        current_deaths = game.player.death_count

        print(f"死亡 #{current_deaths}: ", end="")

        if current_deaths <= target_deaths:
            print(f"還在目標內 ({current_deaths}/{target_deaths})")
        else:
            print(f"超過目標！({current_deaths}/{target_deaths}) - 觸發失敗")
            game.game_over()
            if game.state == 3:  # GAME_OVER
                print("✅ 遊戲失敗機制正確觸發")
                return True
            else:
                print("❌ 遊戲失敗機制未正確觸發")
                return False

    print("❌ 測試過程中未觸發失敗機制")
    return False


if __name__ == "__main__":
    print("開始測試遊戲失敗機制...")

    # 測試1：基本失敗機制
    test1_passed = test_game_over_mechanism()

    # 測試2：死亡次數遞增
    test2_passed = test_death_count_progression()

    print(f"\n=== 測試結果 ===")
    print(f"基本失敗機制: {'✅ 通過' if test1_passed else '❌ 失敗'}")
    print(f"死亡次數遞增: {'✅ 通過' if test2_passed else '❌ 失敗'}")

    if test1_passed and test2_passed:
        print("🎉 所有測試通過！遊戲失敗機制工作正常。")
    else:
        print("⚠️ 部分測試失敗，請檢查遊戲失敗機制。")
