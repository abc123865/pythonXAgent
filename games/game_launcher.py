#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 Python 遊戲合集啟動器
============================

這是一個集合了多個遊戲的啟動器，包含：
- 🦕 超級進階小恐龍遊戲
- 🏔️ JumpKing 跳躍之王
- 🧱 敲磚塊遊戲

作者: pythonXAgent
版本: 2.0
日期: 2025-07-30
"""

import os
import sys
import subprocess

def show_banner():
    """顯示遊戲合集橫幅"""
    print("=" * 80)
    print(" 🎮 Python 遊戲合集 v2.0 - 重構版本")
    print("=" * 80)
    print()
    print("📁 重新組織的遊戲結構：")
    print("   ✅ 模組化設計")
    print("   ✅ 清晰的檔案結構")
    print("   ✅ 易於維護和擴展")
    print("   ✅ 完整的文檔說明")
    print()

def show_game_menu():
    """顯示遊戲選單"""
    print("🎯 可用遊戲：")
    print()
    print("1. 🦕 超級進階小恐龍遊戲")
    print("   - 四種難度等級（簡單到噩夢）")
    print("   - 恐龍特殊技能（衝刺、護盾、二段跳）")
    print("   - 多樣化障礙物系統")
    print("   - 噩夢模式特效（重力反轉、控制反轉）")
    print("   - 全螢幕支持和動態解析度")
    print()
    print("2. 🏔️ JumpKing 跳躍之王")
    print("   - 精確的跳躍控制")
    print("   - 挑戰性的平台設計")
    print("   - 物理模擬系統")
    print()
    print("3. 🧱 敲磚塊遊戲")
    print("   - 經典的磚塊消除")
    print("   - 多種磚塊類型")
    print("   - 彈球物理效果")
    print()
    print("0. 🚪 退出")
    print()

def run_game(game_path, game_name):
    """
    執行指定的遊戲
    
    Args:
        game_path (str): 遊戲檔案路徑
        game_name (str): 遊戲名稱
    """
    if not os.path.exists(game_path):
        print(f"❌ 找不到遊戲檔案: {game_path}")
        return False
    
    print(f"🚀 啟動 {game_name}...")
    print(f"📁 執行: {game_path}")
    print()
    
    try:
        # 改變工作目錄到遊戲目錄
        game_dir = os.path.dirname(game_path)
        original_dir = os.getcwd()
        os.chdir(game_dir)
        
        # 執行遊戲
        result = subprocess.run([sys.executable, os.path.basename(game_path)], 
                              capture_output=False)
        
        # 恢復原始工作目錄
        os.chdir(original_dir)
        
        if result.returncode == 0:
            print(f"✅ {game_name} 正常結束")
        else:
            print(f"⚠️ {game_name} 異常結束 (返回碼: {result.returncode})")
            
    except Exception as e:
        print(f"❌ 執行 {game_name} 時發生錯誤: {e}")
        return False
    
    return True

def main():
    """主程式"""
    show_banner()
    
    # 獲取當前腳本所在目錄
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 定義遊戲路徑
    games = {
        "1": {
            "name": "🦕 超級進階小恐龍遊戲",
            "path": os.path.join(current_dir, "dinosaur", "main.py")
        },
        "2": {
            "name": "🏔️ JumpKing 跳躍之王",
            "path": os.path.join(current_dir, "jumpking", "main.py")
        },
        "3": {
            "name": "🧱 敲磚塊遊戲",
            "path": os.path.join(current_dir, "brick_breaker", "main.py")
        }
    }
    
    while True:
        show_game_menu()
        
        try:
            choice = input("請選擇遊戲 (0-3): ").strip()
            
            if choice == "0":
                print("👋 感謝使用 Python 遊戲合集！")
                break
            elif choice in games:
                game_info = games[choice]
                print(f"\n選擇了: {game_info['name']}")
                
                # 檢查遊戲檔案是否存在
                if not os.path.exists(game_info['path']):
                    print(f"❌ 遊戲檔案不存在: {game_info['path']}")
                    print("請確保遊戲檔案已正確安裝")
                    input("\n按 Enter 繼續...")
                    continue
                
                # 確認執行
                confirm = input(f"確定要啟動 {game_info['name']} 嗎？(y/n): ").strip().lower()
                if confirm in ['y', 'yes', '是', '']:
                    run_game(game_info['path'], game_info['name'])
                    input("\n按 Enter 返回主選單...")
                
            else:
                print("❌ 無效的選擇，請輸入 0-3")
                input("按 Enter 繼續...")
            
            print("\n" + "=" * 80 + "\n")
                
        except KeyboardInterrupt:
            print("\n\n👋 使用者中斷，退出程式")
            break
        except Exception as e:
            print(f"❌ 發生錯誤: {e}")
            input("按 Enter 繼續...")

if __name__ == "__main__":
    main()
