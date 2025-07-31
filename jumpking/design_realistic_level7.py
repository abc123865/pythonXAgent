#!/usr/bin/env python3
"""
重新分析跳躍物理並設計可行的第七關
"""
import math

# 遊戲物理設定
MAX_JUMP_POWER = 20
MIN_JUMP_POWER = 5
GRAVITY = 0.5
MAX_FALL_SPEED = 15


def detailed_jump_analysis():
    """詳細分析跳躍距離"""
    print("詳細跳躍分析：")
    print("=" * 30)

    # 測試不同角度和力度的跳躍
    angles = [30, 45, 60, 75, 90]
    powers = [MIN_JUMP_POWER, (MIN_JUMP_POWER + MAX_JUMP_POWER) / 2, MAX_JUMP_POWER]

    max_horizontal = 0
    best_config = None

    for angle in angles:
        for power in powers:
            angle_rad = math.radians(angle)
            jump_force = power * 1.2

            vel_x = math.cos(angle_rad) * jump_force
            vel_y = math.sin(angle_rad) * -jump_force

            # 模擬跳躍軌跡
            x, y = 0, 0
            time_step = 0.1
            max_height = 0

            trajectory = []
            for t in range(200):  # 最多20秒
                y += vel_y * time_step
                x += vel_x * time_step
                vel_y += GRAVITY * time_step

                if vel_y > MAX_FALL_SPEED:
                    vel_y = MAX_FALL_SPEED

                max_height = min(max_height, y)  # y是向上為負
                trajectory.append((x, y))

                # 如果回到起始高度或更低，停止
                if y >= 0 and t > 10:
                    break

            final_x = x
            print(
                f"角度{angle}°, 力度{power:.1f}: 水平距離{final_x:.1f}, 最大高度{-max_height:.1f}"
            )

            if final_x > max_horizontal:
                max_horizontal = final_x
                best_config = (angle, power, final_x, -max_height)

    print(f"\n最佳配置: 角度{best_config[0]}°, 力度{best_config[1]:.1f}")
    print(f"最大水平距離: {best_config[2]:.1f}像素")
    print(f"最大高度: {best_config[3]:.1f}像素")

    return best_config[2]


def design_realistic_level7():
    """設計真實可行的第七關"""
    max_distance = detailed_jump_analysis()

    # 使用60%的最大距離作為安全距離
    safe_horizontal = max_distance * 0.6
    safe_vertical_up = 50  # 向上跳躍的安全高度
    safe_vertical_down = 30  # 向下跳躍時的高度差

    print(f"\n設計參數:")
    print(f"安全水平距離: {safe_horizontal:.1f}像素")
    print(f"安全向上高度: {safe_vertical_up}像素")
    print(f"安全向下高度: {safe_vertical_down}像素")

    platforms = [
        {"x": 0, "y": 550, "width": 120, "height": 50},  # 起始平台（更大）
    ]

    # 設計一條Z字形的攀登路線
    current_x = 60  # 起始平台中心
    current_y = 550

    # 第一跳：向右
    next_x = current_x + safe_horizontal * 0.7
    next_y = current_y - safe_vertical_up * 0.8
    platforms.append(
        {"x": int(next_x - 20), "y": int(next_y), "width": 40, "height": 15}
    )
    current_x, current_y = next_x, next_y

    # 第二跳：向右上
    next_x = current_x + safe_horizontal * 0.5
    next_y = current_y - safe_vertical_up * 0.6
    platforms.append(
        {"x": int(next_x - 20), "y": int(next_y), "width": 40, "height": 15}
    )
    current_x, current_y = next_x, next_y

    # 第三跳：向左上
    next_x = current_x - safe_horizontal * 0.6
    next_y = current_y - safe_vertical_up * 0.7
    platforms.append(
        {"x": int(next_x - 20), "y": int(next_y), "width": 40, "height": 15}
    )
    current_x, current_y = next_x, next_y

    # 第四跳：向左
    next_x = current_x - safe_horizontal * 0.5
    next_y = current_y - safe_vertical_up * 0.5
    platforms.append(
        {"x": int(next_x - 20), "y": int(next_y), "width": 40, "height": 15}
    )
    current_x, current_y = next_x, next_y

    # 第五跳：向右上
    next_x = current_x + safe_horizontal * 0.8
    next_y = current_y - safe_vertical_up * 0.9
    platforms.append(
        {"x": int(next_x - 20), "y": int(next_y), "width": 40, "height": 15}
    )
    current_x, current_y = next_x, next_y

    # 第六跳：向右
    next_x = current_x + safe_horizontal * 0.6
    next_y = current_y - safe_vertical_up * 0.6
    platforms.append(
        {"x": int(next_x - 20), "y": int(next_y), "width": 40, "height": 15}
    )
    current_x, current_y = next_x, next_y

    # 第七跳：向左上
    next_x = current_x - safe_horizontal * 0.7
    next_y = current_y - safe_vertical_up * 0.8
    platforms.append(
        {"x": int(next_x - 20), "y": int(next_y), "width": 40, "height": 15}
    )
    current_x, current_y = next_x, next_y

    # 最終跳躍到目標平台
    next_x = current_x + safe_horizontal * 0.4
    next_y = current_y - safe_vertical_up * 1.2
    platforms.append(
        {"x": int(next_x - 60), "y": int(next_y), "width": 120, "height": 30}
    )

    return platforms


def generate_verified_level():
    """生成並驗證關卡"""
    platforms = design_realistic_level7()

    print("\n生成的第七關:")
    print("levels[7] = {")
    print('    "name": "專家考驗",')
    print('    "platforms": [')

    for i, platform in enumerate(platforms):
        if i == 0:
            comment = "# 起始平台"
        elif i == len(platforms) - 1:
            comment = "# 目標平台"
        else:
            comment = f"# 平台{i}"
        print(
            f'        {{"x": {platform["x"]}, "y": {platform["y"]}, "width": {platform["width"]}, "height": {platform["height"]}}},  {comment}'
        )

    print("    ],")
    print('    "death_zones": [')
    print('        {"x": 0, "y": 600, "width": 1200, "height": 100},  # 底部死亡區域')
    print("    ],")
    goal_y = platforms[-1]["y"]
    print(f'    "goal_y": {goal_y},')
    print('    "start_pos": (60, 500),  # 起始平台中心')
    print('    "target_deaths": 25,')
    print("}")

    return platforms


if __name__ == "__main__":
    platforms = generate_verified_level()
