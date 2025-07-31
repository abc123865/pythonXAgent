"""
🦕 超級進階小恐龍遊戲 - 主程式入口
==============================

這是一個功能豐富的小恐龍跳躍遊戲，包含：
- 四種難度等級
- 多種障礙物類型
- 恐龍特殊技能
- 動態螢幕適應
- 噩夢模式特效

作者: pythonXAgent
版本: 2.0
日期: 2025-07-30
"""

import sys
import os

# 添加 src 目錄到 Python 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

from game_engine import Game


def main():
    """主程式入口"""
    print("=" * 70)
    print("🦕 超級進階小恐龍遊戲啟動！v2.0 重構版本")
    print("=" * 70)
    print("🎮 全新特色：")
    print("   • 四種難度等級選擇 - 從簡單到噩夢級")
    print("   • 主選單系統 - 精美的難度選擇介面")
    print("   • 動態速度調整 - 根據難度智能調節")
    print("   • 進階障礙物系統 - 隱形、爆炸、移動障礙物")
    print("   • 恐龍新能力 - 衝刺、護盾、二段跳")
    print("   • 連擊系統 - 獎勵技巧性操作")
    print("   • 螢幕震動特效 - 增強遊戲感受")
    print("   • ⚡ 噩夢效果 - 重力異常、控制反轉")
    print("   • 🌙 日夜反轉 - 2000分時進入夜晚模式")
    print("   • 🖥️ 全螢幕支持 - 自適應任何螢幕大小")
    print("   • 🔊 Popcat 音效系統 - 每個按鍵都有清脆的 pop 音效")
    print()
    print("🎯 難度等級：")
    print("   • 簡單 (Easy) - 適合新手，慢節奏遊戲")
    print("   • 中等 (Medium) - 標準難度，平衡的挑戰")
    print("   • 困難 (Hard) - 快節奏，需要高度技巧")
    print("   • 噩夢 (Nightmare) - 超極速+重力異常+螢幕閃爍")
    print()
    print("🕹️ 操作說明：")
    print("   • ↑方向鍵/空白鍵：跳躍 (可二段跳)")
    print("   • ↓方向鍵/S鍵：蹲下")
    print("   • X鍵：衝刺 (有冷卻時間)")
    print("   • Z鍵：護盾 (短時間無敵)")
    print("   • ESC鍵：返回主選單")
    print("   • F1鍵：切換音效開關")
    print("   • F11鍵：切換全螢幕模式")
    print("   • Alt+F4：退出遊戲")
    print()
    print("🎯 準備好挑戰噩夢級的極限了嗎？")
    print("=" * 70)

    try:
        game = Game()
        game.run()
    except ImportError as e:
        print(f"❌ 模組載入錯誤: {e}")
        print("請確保所有遊戲檔案都在正確位置")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 遊戲發生錯誤: {e}")
        print("請確保已安裝 pygame：pip install pygame")
        sys.exit(1)


if __name__ == "__main__":
    main()
