#!/usr/bin/env python3
"""
簡單的跳躍力量循環邏輯測試
不需要圖形界面，直接測試邏輯
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 模擬跳躍常數
MAX_JUMP_POWER = 20
MIN_JUMP_POWER = 5
JUMP_CHARGE_RATE = 0.5


class MockPlayer:
    """模擬玩家類別用於測試"""

    def __init__(self):
        self.jump_charging = False
        self.jump_power = 0
        self.jump_power_paused = False
        self.jump_power_pause_timer = 0
        self.jump_power_pause_duration = 30

    def start_jump_charge(self):
        """開始跳躍充能"""
        self.jump_charging = True
        self.jump_power = MIN_JUMP_POWER
        self.jump_power_paused = False
        self.jump_power_pause_timer = 0

    def update_jump_charge(self):
        """更新跳躍充能（與遊戲中的邏輯相同）"""
        if self.jump_charging:
            if self.jump_power_paused:
                # 處於暫停狀態，計時器遞減
                self.jump_power_pause_timer -= 1
                if self.jump_power_pause_timer <= 0:
                    # 暫停結束，重新開始充能
                    self.jump_power_paused = False
                    self.jump_power = MIN_JUMP_POWER
            else:
                # 正常充能狀態
                self.jump_power += JUMP_CHARGE_RATE
                if self.jump_power >= MAX_JUMP_POWER:
                    # 達到最大值，進入暫停狀態
                    self.jump_power = MAX_JUMP_POWER
                    self.jump_power_paused = True
                    self.jump_power_pause_timer = self.jump_power_pause_duration


def test_jump_cycle_logic():
    """測試跳躍循環邏輯"""
    print("=== 跳躍力量循環邏輯測試 ===")

    player = MockPlayer()
    player.start_jump_charge()

    print(f"初始狀態: 力量={player.jump_power}, 暫停={player.jump_power_paused}")

    frame_count = 0
    cycle_count = 0

    # 模擬 200 幀 (約 3.3 秒)
    for frame in range(200):
        old_paused = player.jump_power_paused
        old_power = player.jump_power

        player.update_jump_charge()
        frame_count += 1

        # 檢測狀態變化
        if not old_paused and player.jump_power_paused:
            print(f"幀 {frame}: 達到最大值 ({player.jump_power})，進入暫停狀態")
            cycle_count += 1
        elif old_paused and not player.jump_power_paused:
            print(
                f"幀 {frame}: 暫停結束，重新開始充能 (力量重置為 {player.jump_power})"
            )

        # 每 10 幀報告一次狀態
        if frame % 10 == 0:
            status = "暫停中" if player.jump_power_paused else "充能中"
            if player.jump_power_paused:
                print(
                    f"幀 {frame}: {status} - 剩餘暫停時間: {player.jump_power_pause_timer}"
                )
            else:
                print(f"幀 {frame}: {status} - 當前力量: {player.jump_power:.1f}")

    print(f"\n✅ 測試完成!")
    print(f"總幀數: {frame_count}")
    print(f"完成循環次數: {cycle_count}")
    print(f"最終狀態: 力量={player.jump_power:.1f}, 暫停={player.jump_power_paused}")

    if cycle_count >= 2:
        print("🎉 循環系統運作正常！")
    else:
        print("⚠️  循環次數不足，可能需要調整參數")


if __name__ == "__main__":
    test_jump_cycle_logic()
