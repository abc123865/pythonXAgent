#!/usr/bin/env python3
"""
分析所有關卡的可行性
"""
import math

# 遊戲物理設定
MAX_JUMP_POWER = 20
MIN_JUMP_POWER = 5
GRAVITY = 0.5
MAX_FALL_SPEED = 15

def calculate_jump_trajectory(start_x, start_y, angle_degrees, power):
    """計算跳躍軌跡"""
    angle_rad = math.radians(angle_degrees)
    jump_force = power * 1.2
    
    vel_x = math.cos(angle_rad) * jump_force
    vel_y = math.sin(angle_rad) * -jump_force
    
    x, y = start_x, start_y
    time_step = 0.1
    max_time = 100
    
    for t in range(max_time):
        vel_y += GRAVITY * time_step
        if vel_y > MAX_FALL_SPEED:
            vel_y = MAX_FALL_SPEED
        
        x += vel_x * time_step
        y += vel_y * time_step
        
        if vel_y > 0 and y > start_y + 200:
            break
    
    return x, y

def can_reach_platform_simple(from_platform, to_platform):
    """簡化版本的平台可達性檢查"""
    start_x = from_platform["x"] + from_platform["width"] // 2
    start_y = from_platform["y"]
    
    target_left = to_platform["x"]
    target_right = to_platform["x"] + to_platform["width"]
    target_top = to_platform["y"]
    
    # 計算距離
    horizontal_distance = (target_left + target_right) / 2 - start_x
    vertical_distance = start_y - target_top
    
    # 嘗試幾個常用角度
    angles_to_try = [30, 45, 60, 75, 90, 105, 120, 135]
    powers_to_try = [MIN_JUMP_POWER, (MIN_JUMP_POWER + MAX_JUMP_POWER) / 2, MAX_JUMP_POWER]
    
    for angle in angles_to_try:
        for power in powers_to_try:
            final_x, final_y = calculate_jump_trajectory(start_x, start_y, angle, power)
            
            # 檢查是否能到達目標平台範圍
            if (target_left <= final_x <= target_right and 
                abs(final_y - target_top) <= 15):
                return True, horizontal_distance, vertical_distance
    
    return False, horizontal_distance, vertical_distance

def analyze_all_levels():
    """分析所有關卡的可行性"""
    
    # 這裡只分析第8-11關，因為第7關已經修正了
    level_configs = {
        8: {
            "platforms": [
                {"x": 0, "y": 550, "width": 40, "height": 50},
                {"x": 60, "y": 530, "width": 10, "height": 5},
                {"x": 90, "y": 510, "width": 10, "height": 5},
                {"x": 120, "y": 490, "width": 10, "height": 5},
                {"x": 150, "y": 470, "width": 10, "height": 5},
                {"x": 180, "y": 450, "width": 10, "height": 5},
            ],
            "start_pos": (20, 500)
        },
        9: {
            "platforms": [
                {"x": 0, "y": 550, "width": 30, "height": 50},
                {"x": 50, "y": 540, "width": 8, "height": 3},
                {"x": 70, "y": 530, "width": 8, "height": 3},
                {"x": 90, "y": 520, "width": 8, "height": 3},
            ],
            "start_pos": (15, 500)
        },
        10: {
            "platforms": [
                {"x": 0, "y": 550, "width": 25, "height": 50},
                {"x": 35, "y": 545, "width": 5, "height": 2},
                {"x": 50, "y": 540, "width": 5, "height": 2},
            ],
            "start_pos": (12, 500)
        }
    }
    
    print("分析關卡可行性:")
    print("=" * 50)
    
    problematic_levels = []
    
    for level_num, config in level_configs.items():
        print(f"\n第{level_num}關分析:")
        platforms = config["platforms"]
        start_pos = config["start_pos"]
        
        # 檢查起始跳躍
        start_platform = platforms[0]
        if len(platforms) > 1:
            first_target = platforms[1]
            
            # 調整起始位置檢查
            temp_start_platform = {
                "x": start_pos[0] - 15,
                "y": start_pos[1] + 40,  # 玩家底部位置
                "width": 30,
                "height": 10
            }
            
            can_reach, h_dist, v_dist = can_reach_platform_simple(temp_start_platform, first_target)
            
            print(f"  起始跳躍: ({start_pos[0]}, {start_pos[1]}) -> 平台1")
            print(f"  距離: 水平{h_dist:.1f}, 垂直{v_dist:.1f}")
            print(f"  可達性: {'✅' if can_reach else '❌'}")
            
            if not can_reach:
                problematic_levels.append(level_num)
                print(f"  ⚠️ 第{level_num}關起始跳躍不可行!")
        
        # 檢查相鄰平台間的跳躍
        for i in range(len(platforms) - 1):
            from_plat = platforms[i]
            to_plat = platforms[i + 1]
            
            can_reach, h_dist, v_dist = can_reach_platform_simple(from_plat, to_plat)
            
            if not can_reach:
                print(f"  ❌ 平台{i} -> 平台{i+1}: 不可達 (距離: {h_dist:.1f}, {v_dist:.1f})")
                if level_num not in problematic_levels:
                    problematic_levels.append(level_num)
            else:
                print(f"  ✅ 平台{i} -> 平台{i+1}: 可達")
    
    print(f"\n總結:")
    if problematic_levels:
        print(f"❌ 有問題的關卡: {problematic_levels}")
        print("這些關卡需要重新設計!")
        return problematic_levels
    else:
        print("✅ 所有分析的關卡都是可行的")
        return []

if __name__ == "__main__":
    problematic = analyze_all_levels()
    
    if problematic:
        print(f"\n需要修正的關卡: {problematic}")
        print("建議:")
        print("1. 增加平台尺寸")
        print("2. 減少平台間距離") 
        print("3. 調整平台高度差")
        print("4. 重新設計跳躍路線")
