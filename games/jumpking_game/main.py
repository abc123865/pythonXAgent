#!/usr/bin/env python3
"""
Jump King 遊戲主程式
重新建構版本 - 模組化設計
"""
import pygame
import sys
import os

# 添加 src 目錄到路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
levels_dir = os.path.join(current_dir, "levels")
data_dir = os.path.join(current_dir, "data")
sys.path.insert(0, src_dir)
sys.path.insert(0, levels_dir)
sys.path.insert(0, data_dir)

from src.game_engine import Game


def main():
    """主程式入口點"""
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"遊戲發生錯誤: {e}")
        import traceback

        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
