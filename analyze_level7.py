#!/usr/bin/env python3
"""
分析第七關跳躍路線的可行性
"""
import math

# 遊戲物理設定
MAX_JUMP_POWER = 20
MIN_JUMP_POWER = 5
GRAVITY = 0.5
MAX_FALL_SPEED = 15

# 玩家設定
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 40

# 第7關平台配置
platforms = [
    {"x": 0, "y": 550, "width": 80, "height": 50, "name": "起始平台"},
    {"x": 100, "y": 520, "width": 20, "height": 10, "name": "平台1"},
    {"x": 140, "y": 490, "width": 20, "height": 10, "name": "平台2"},
    {"x": 180, "y": 460, "width": 20, "height": 10, "name": "平台3"},
    {"x": 220, "y": 430, "width": 20, "height": 10, "name": "平台4"},
    {"x": 260, "y": 400, "width": 20, "height": 10, "name": "平台5"},
    {"x": 300, "y": 370, "width": 20, "height": 10, "name": "平台6"},
    {"x": 340, "y": 340, "width": 20, "height": 10, "name": "平台7"},
    {"x": 380, "y": 310, "width": 20, "height": 10, "name": "平台8"},
    {"x": 420, "y": 280, "width": 20, "height": 10, "name": "平台9"},
    {"x": 460, "y": 250, "width": 20, "height": 10, "name": "平台10"},
    {"x": 500, "y": 220, "width": 20, "height": 10, "name": "平台11"},
    {"x": 540, "y": 190, "width": 20, "height": 10, "name": "平台12"},
    {"x": 580, "y": 160, "width": 20, "height": 10, "name": "平台13"},
    {"x": 540, "y": 130, "width": 20, "height": 10, "name": "平台14"},
    {"x": 500, "y": 100, "width": 20, "height": 10, "name": "平台15"},
    {"x": 460, "y": 70, "width": 20, "height": 10, "name": "平台16"},
    {"x": 420, "y": 40, "width": 20, "height": 10, "name": "平台17"},
    {"x": 380, "y": 10, "width": 20, "height": 10, "name": "平台18"},
    {"x": 350, "y": -30, "width": 100, "height": 30, "name": "目標平台"},
]

start_pos = (20, 500)


def calculate_jump_trajectory(start_x, start_y, angle_degrees, power):
    """計算跳躍軌跡"""
    angle_rad = math.radians(angle_degrees)
    jump_force = power * 1.2  # 遊戲中的跳躍力增強

    vel_x = math.cos(angle_rad) * jump_force
    vel_y = math.sin(angle_rad) * -jump_force  # 負值表示向上

    # 模擬軌跡
    x, y = start_x, start_y
    time_step = 0.1
    max_time = 100  # 最大模擬時間

    trajectory = [(x, y)]

    for t in range(max_time):
        # 更新速度（重力影響）
        vel_y += GRAVITY * time_step
        if vel_y > MAX_FALL_SPEED:
            vel_y = MAX_FALL_SPEED

        # 更新位置
        x += vel_x * time_step
        y += vel_y * time_step

        trajectory.append((x, y))

        # 如果開始往下墜落且已經低於起始點很多，停止模擬
        if vel_y > 0 and y > start_y + 200:
            break

    return trajectory


def can_reach_platform(from_platform, to_platform, player_start_x):
    """檢查是否能從一個平台跳到另一個平台"""
    # 計算起跳點（平台中心）
    start_x = from_platform["x"] + from_platform["width"] // 2
    start_y = from_platform["y"]

    # 如果有指定起始x位置，使用它
    if player_start_x is not None:
        start_x = player_start_x

    # 計算目標平台範圍
    target_left = to_platform["x"]
    target_right = to_platform["x"] + to_platform["width"]
    target_top = to_platform["y"]

    print(f"\n檢查跳躍: {from_platform['name']} -> {to_platform['name']}")
    print(f"起跳點: ({start_x}, {start_y})")
    print(f"目標平台: x={target_left}-{target_right}, y={target_top}")

    # 計算距離和高度差
    horizontal_distance = (target_left + target_right) / 2 - start_x
    vertical_distance = start_y - target_top

    print(f"水平距離: {horizontal_distance:.1f}, 垂直距離: {vertical_distance:.1f}")

    # 嘗試不同的跳躍角度和力度
    best_result = None
    angles_to_try = (
        [45, 60, 75, 90, 105, 120, 135]
        if horizontal_distance > 0
        else [45, 60, 75, 90, 105, 120, 135]
    )

    for angle in angles_to_try:
        for power in [
            MIN_JUMP_POWER,
            (MIN_JUMP_POWER + MAX_JUMP_POWER) / 2,
            MAX_JUMP_POWER,
        ]:
            trajectory = calculate_jump_trajectory(start_x, start_y, angle, power)

            # 檢查軌跡是否穿過目標平台
            for x, y in trajectory:
                if (
                    target_left <= x <= target_right and abs(y - target_top) <= 10
                ):  # 允許10像素誤差

                    if best_result is None or abs(y - target_top) < abs(
                        best_result[1] - target_top
                    ):
                        best_result = (x, y, angle, power)
                        print(
                            f"  可能方案: 角度{angle}°, 力度{power:.1f} -> 到達({x:.1f}, {y:.1f})"
                        )

    return best_result is not None, best_result


def analyze_level():
    """分析整個關卡的可行性"""
    print("第七關跳躍路線分析")
    print("=" * 50)

    current_platform = platforms[0]  # 起始平台
    player_x = start_pos[0]

    impossible_jumps = []

    for i in range(1, len(platforms)):
        next_platform = platforms[i]
        can_reach, best_solution = can_reach_platform(
            current_platform, next_platform, player_x if i == 1 else None
        )

        if not can_reach:
            impossible_jumps.append((current_platform["name"], next_platform["name"]))
            print(f"❌ 無法從 {current_platform['name']} 跳到 {next_platform['name']}")
        else:
            print(f"✅ 可以從 {current_platform['name']} 跳到 {next_platform['name']}")
            if best_solution:
                x, y, angle, power = best_solution
                print(f"   最佳方案: 角度{angle}°, 力度{power:.1f}")

        current_platform = next_platform
        player_x = None  # 後續使用平台中心

    print(f"\n總結:")
    print(f"總平台數: {len(platforms)}")
    print(f"不可能的跳躍: {len(impossible_jumps)}")

    if impossible_jumps:
        print("❌ 關卡設計有問題，以下跳躍不可能完成:")
        for from_plat, to_plat in impossible_jumps:
            print(f"  - {from_plat} -> {to_plat}")
        return False
    else:
        print("✅ 關卡設計可行，所有跳躍都是可能的")
        return True


if __name__ == "__main__":
    is_possible = analyze_level()

    if not is_possible:
        print("\n建議修改:")
        print("1. 增加平台尺寸")
        print("2. 減少平台間距離")
        print("3. 調整平台高度差")
        print("4. 添加中間平台")
