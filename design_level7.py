#!/usr/bin/env python3
"""
設計一個可行的第七關
"""
import math

# 遊戲物理設定
MAX_JUMP_POWER = 20
MIN_JUMP_POWER = 5


def calculate_max_jump_distance():
    """計算最大跳躍距離"""
    # 45度角最大跳躍力的理論最大距離
    angle_rad = math.radians(45)
    jump_force = MAX_JUMP_POWER * 1.2

    vel_x = math.cos(angle_rad) * jump_force
    vel_y = math.sin(angle_rad) * -jump_force

    # 計算飛行時間（到達最高點再落回原高度）
    # 使用 y = v0*t + 0.5*a*t^2，當y=0時求t
    # 0 = vel_y*t + 0.5*0.5*t^2
    # 0 = vel_y + 0.25*t
    # t = -vel_y / 0.25 = -vel_y * 4
    flight_time = -vel_y * 2 / 0.5  # 總飛行時間

    max_distance = vel_x * flight_time
    return max_distance


def design_feasible_level7():
    """設計一個可行的第七關"""
    max_distance = calculate_max_jump_distance()
    print(f"最大跳躍距離: {max_distance:.1f}像素")

    # 設計原則：
    # 1. 每次跳躍距離不超過最大距離的80%
    # 2. 平台要有合理大小（至少30像素寬）
    # 3. 高度差要合理

    safe_distance = max_distance * 0.6  # 安全距離
    print(f"安全跳躍距離: {safe_distance:.1f}像素")

    platforms = [
        {"x": 0, "y": 550, "width": 100, "height": 50, "name": "起始平台"},
    ]

    # 從起始平台開始設計路線
    current_x = 50  # 起始平台中心
    current_y = 550
    platform_count = 1

    # 向上攀爬的路線
    target_y = -50  # 目標高度

    while current_y > target_y:
        # 計算下一個平台位置
        # 隨機選擇方向和距離（在安全範圍內）
        if platform_count % 4 == 1:  # 向右
            next_x = current_x + safe_distance * 0.8
            next_y = current_y - 35
        elif platform_count % 4 == 2:  # 向右上
            next_x = current_x + safe_distance * 0.6
            next_y = current_y - 40
        elif platform_count % 4 == 3:  # 向左上
            next_x = current_x - safe_distance * 0.6
            next_y = current_y - 40
        else:  # 向左
            next_x = current_x - safe_distance * 0.8
            next_y = current_y - 35

        # 確保在螢幕範圍內
        next_x = max(30, min(next_x, 770))

        platforms.append(
            {
                "x": int(next_x - 15),
                "y": int(next_y),
                "width": 30,
                "height": 15,
                "name": f"平台{platform_count}",
            }
        )

        current_x = next_x
        current_y = next_y
        platform_count += 1

        if platform_count > 15:  # 限制平台數量
            break

    # 最終目標平台
    platforms.append(
        {
            "x": int(current_x - 50),
            "y": int(current_y - 50),
            "width": 100,
            "height": 30,
            "name": "目標平台",
        }
    )

    return platforms


def generate_level_code(platforms):
    """生成關卡代碼"""
    print("\n生成的第七關代碼：")
    print("levels[7] = {")
    print('    "name": "專家考驗",')
    print('    "platforms": [')

    for platform in platforms:
        print(
            f'        {{"x": {platform["x"]}, "y": {platform["y"]}, "width": {platform["width"]}, "height": {platform["height"]}}},  # {platform["name"]}'
        )

    print("    ],")
    print('    "death_zones": [')
    print('        {"x": 0, "y": 600, "width": 1200, "height": 100},  # 底部死亡區域')
    print("    ],")
    goal_y = platforms[-1]["y"]
    print(f'    "goal_y": {goal_y},')
    print('    "start_pos": (50, 500),')
    print('    "target_deaths": 30,')
    print("}")


if __name__ == "__main__":
    platforms = design_feasible_level7()
    generate_level_code(platforms)
