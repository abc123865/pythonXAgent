#!/usr/bin/env python3
"""
重新設計第8-11關
"""
import math

# 遊戲物理設定
MAX_JUMP_POWER = 20
MIN_JUMP_POWER = 5

def calculate_safe_distance():
    """計算安全跳躍距離"""
    # 使用30度角最大力度作為參考
    angle_rad = math.radians(30)
    jump_force = MAX_JUMP_POWER * 1.2
    
    vel_x = math.cos(angle_rad) * jump_force
    vel_y = math.sin(angle_rad) * -jump_force
    
    # 計算最大距離（簡化）
    flight_time = -vel_y * 2 / 0.5
    max_distance = vel_x * flight_time
    
    return max_distance * 0.5  # 使用50%作為安全距離

def design_level_8():
    """設計第8關 - 大師級"""
    safe_dist = calculate_safe_distance()
    
    platforms = [
        {"x": 0, "y": 550, "width": 100, "height": 50},  # 起始平台
    ]
    
    # Z字形路線，難度適中
    current_x, current_y = 50, 550
    
    # 第一段：右上
    for i in range(3):
        current_x += safe_dist * 0.4
        current_y -= 35
        platforms.append({
            "x": int(current_x - 15),
            "y": int(current_y),
            "width": 30,
            "height": 12
        })
    
    # 第二段：左上
    for i in range(3):
        current_x -= safe_dist * 0.4
        current_y -= 35
        platforms.append({
            "x": int(current_x - 15),
            "y": int(current_y),
            "width": 30,
            "height": 12
        })
    
    # 第三段：右上到目標
    for i in range(2):
        current_x += safe_dist * 0.5
        current_y -= 40
        platforms.append({
            "x": int(current_x - 15),
            "y": int(current_y),
            "width": 30,
            "height": 12
        })
    
    # 目標平台
    platforms.append({
        "x": int(current_x - 50),
        "y": int(current_y - 50),
        "width": 100,
        "height": 30
    })
    
    return platforms

def design_level_9():
    """設計第9關 - 傳說級"""
    safe_dist = calculate_safe_distance()
    
    platforms = [
        {"x": 0, "y": 550, "width": 80, "height": 50},  # 起始平台
    ]
    
    # 更具挑戰性但仍可行的路線
    current_x, current_y = 40, 550
    
    # 螺旋上升路線
    angles = [0, 60, 120, 180, 240, 300, 0, 60, 120, 180]  # 度數
    for i, angle in enumerate(angles):
        # 計算螺旋位置
        radius = 100
        offset_x = radius * math.cos(math.radians(angle))
        offset_y = -50 * (i + 1)  # 每次上升50像素
        
        next_x = 300 + offset_x  # 螺旋中心在x=300
        next_y = 550 + offset_y
        
        platforms.append({
            "x": int(next_x - 12),
            "y": int(next_y),
            "width": 24,
            "height": 10
        })
    
    # 目標平台
    platforms.append({
        "x": 250,
        "y": int(next_y - 60),
        "width": 100,
        "height": 30
    })
    
    return platforms

def design_level_10():
    """設計第10關 - 絕望深淵（極高難度但仍可行）"""
    safe_dist = calculate_safe_distance()
    
    platforms = [
        {"x": 0, "y": 550, "width": 60, "height": 50},  # 起始平台
    ]
    
    # 極具挑戰性的路線
    current_x, current_y = 30, 550
    
    # 第一段：精確跳躍序列
    jump_sequence = [
        (safe_dist * 0.3, -30),   # 短距離右上
        (safe_dist * 0.2, -25),   # 更短距離右上
        (-safe_dist * 0.4, -30),  # 左上
        (-safe_dist * 0.2, -25),  # 短左上
        (safe_dist * 0.5, -35),   # 長右上
        (safe_dist * 0.1, -20),   # 極短右上
        (-safe_dist * 0.3, -30),  # 左上
        (safe_dist * 0.4, -40),   # 右上
        (-safe_dist * 0.2, -25),  # 左上
        (safe_dist * 0.6, -45),   # 長右上
        (-safe_dist * 0.5, -35),  # 長左上
        (safe_dist * 0.3, -30),   # 右上
    ]
    
    for dx, dy in jump_sequence:
        current_x += dx
        current_y += dy
        
        # 確保在螢幕範圍內
        current_x = max(20, min(current_x, 780))
        
        platforms.append({
            "x": int(current_x - 10),
            "y": int(current_y),
            "width": 20,
            "height": 8
        })
    
    # 最終目標平台
    platforms.append({
        "x": int(current_x - 60),
        "y": int(current_y - 80),
        "width": 120,
        "height": 30
    })
    
    return platforms

def design_level_11():
    """設計第11關 - 絕望之塔（超級挑戰）"""
    safe_dist = calculate_safe_distance()
    
    platforms = [
        {"x": 0, "y": 550, "width": 100, "height": 50},  # 起始平台
    ]
    
    # 超長的攀登路線
    current_x, current_y = 50, 550
    
    # 多段式攀登
    for section in range(5):  # 5個段落
        for step in range(4):  # 每段4步
            if step % 2 == 0:
                dx = safe_dist * 0.6
                dy = -45
            else:
                dx = -safe_dist * 0.4
                dy = -35
            
            current_x += dx
            current_y += dy
            
            # 確保在螢幕範圍內
            current_x = max(30, min(current_x, 770))
            
            # 平台大小隨高度減小
            width = max(15, 35 - section * 3)
            height = max(8, 15 - section * 1)
            
            platforms.append({
                "x": int(current_x - width//2),
                "y": int(current_y),
                "width": width,
                "height": height
            })
    
    # 最終勝利平台
    platforms.append({
        "x": int(current_x - 80),
        "y": int(current_y - 100),
        "width": 160,
        "height": 40
    })
    
    return platforms

def generate_all_levels():
    """生成所有重新設計的關卡"""
    levels = {
        8: design_level_8(),
        9: design_level_9(), 
        10: design_level_10(),
        11: design_level_11()
    }
    
    level_names = {
        8: "大師挑戰",
        9: "傳說試煉", 
        10: "絕望深淵",
        11: "絕望之塔"
    }
    
    target_deaths = {
        8: 35,
        9: 50,
        10: 80,
        11: 120
    }
    
    for level_num, platforms in levels.items():
        print(f"\n        # 第{level_num}關 - {level_names[level_num]}（重新設計）")
        print(f"        levels[{level_num}] = {{")
        print(f'            "name": "{level_names[level_num]}",')
        print(f'            "platforms": [')
        
        for i, platform in enumerate(platforms):
            if i == 0:
                comment = "# 起始平台"
            elif i == len(platforms) - 1:
                comment = "# 目標平台"
            else:
                comment = f"# 平台{i}"
            print(f'                {{"x": {platform["x"]}, "y": {platform["y"]}, "width": {platform["width"]}, "height": {platform["height"]}}},  {comment}')
        
        print(f'            ],')
        print(f'            "death_zones": [')
        print(f'                {{"x": 0, "y": 600, "width": 1200, "height": 100}},  # 底部死亡區域')
        
        # 第11關添加特殊陷阱
        if level_num == 11:
            print(f'                # 掉落陷阱區域')
            for i in range(0, 800, 200):
                y_pos = 500 - i // 4
                print(f'                {{"x": {i}, "y": {y_pos}, "width": 50, "height": 20}},')
        
        print(f'            ],')
        goal_y = platforms[-1]["y"]
        print(f'            "goal_y": {goal_y},')
        
        # 起始位置
        if level_num == 8:
            start_pos = "(50, 500)"
        elif level_num == 9:
            start_pos = "(40, 500)"
        elif level_num == 10:
            start_pos = "(30, 500)"
        else:  # level 11
            start_pos = "(50, 500)"
            
        print(f'            "start_pos": {start_pos},')
        print(f'            "target_deaths": {target_deaths[level_num]},')
        print(f'        }}')

if __name__ == "__main__":
    print("重新設計的關卡配置:")
    print("=" * 50)
    generate_all_levels()
