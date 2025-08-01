"""
Getting Over It - 測試腳本
用於測試遊戲的各種功能
"""

import pygame
import sys
import os

# 添加當前目錄到路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 導入遊戲模組
from goi import Game, Vector2, Physics, Player, Hammer, Terrain


def test_vector2():
    """測試 Vector2 類別"""
    print("測試 Vector2 類別...")

    v1 = Vector2(3, 4)
    v2 = Vector2(1, 2)

    # 測試基本運算
    assert (v1 + v2).x == 4 and (v1 + v2).y == 6
    assert (v1 - v2).x == 2 and (v1 - v2).y == 2
    assert (v1 * 2).x == 6 and (v1 * 2).y == 8
    assert (v1 / 2).x == 1.5 and (v1 / 2).y == 2.0

    # 測試長度
    assert v1.magnitude() == 5.0

    # 測試正規化
    normalized = v1.normalized()
    assert abs(normalized.magnitude() - 1.0) < 0.001

    print("✓ Vector2 測試通過")


def test_physics():
    """測試物理系統"""
    print("測試物理系統...")

    velocity = Vector2(1, 0)

    # 測試重力
    new_velocity = Physics.apply_gravity(velocity)
    assert new_velocity.x == 1
    assert new_velocity.y == 0.8  # 更新為新的重力值

    # 測試空氣阻力
    air_velocity = Physics.apply_air_resistance(velocity)
    assert air_velocity.x == 0.995  # 更新為新的空氣阻力值
    assert air_velocity.y == 0

    print("✓ 物理系統測試通過")


def test_terrain():
    """測試地形系統"""
    print("測試地形系統...")

    terrain = Terrain()

    # 確保有平台和障礙物
    assert len(terrain.platforms) > 0
    assert len(terrain.obstacles) > 0

    # 測試碰撞檢測
    test_rect = pygame.Rect(0, 750, 10, 10)  # 地面位置
    collisions = terrain.check_collision(test_rect)
    assert len(collisions) > 0

    print("✓ 地形系統測試通過")


def test_player():
    """測試玩家系統"""
    print("測試玩家系統...")

    player = Player(100, 100)

    # 測試初始位置
    assert player.position.x == 100
    assert player.position.y == 100

    # 測試錘子
    assert player.hammer is not None
    assert player.hammer.length == 100  # 更新為新的錘子長度

    print("✓ 玩家系統測試通過")


def run_visual_test():
    """運行視覺測試"""
    print("開始視覺測試...")

    pygame.init()

    try:
        game = Game()
        print("✓ 遊戲初始化成功")

        # 運行幾幀來測試
        for _ in range(10):
            game.handle_events()
            game.update()
            game.draw()
            game.clock.tick(60)

        print("✓ 遊戲主循環測試通過")

    except Exception as e:
        print(f"✗ 視覺測試失敗: {e}")
        return False
    finally:
        pygame.quit()

    return True


def main():
    """主測試函數"""
    print("=== Getting Over It 遊戲測試 ===\n")

    try:
        # 單元測試
        test_vector2()
        test_physics()
        test_terrain()
        test_player()

        # 視覺測試
        if run_visual_test():
            print("\n=== 所有測試通過！ ===")
            print("遊戲可以正常運行。")
        else:
            print("\n=== 視覺測試失敗 ===")
            print("請檢查遊戲配置。")

    except Exception as e:
        print(f"\n=== 測試失敗 ===")
        print(f"錯誤: {e}")
        return False

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
