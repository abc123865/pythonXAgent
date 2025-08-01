#!/usr/bin/env python3
"""
測試失敗音效系統
用途：當超過目標死亡次數時播放失敗音效

使用方法：
1. 執行此檔案
2. 按下 G 鍵播放失敗音效
3. 按下 Q 鍵退出測試

注意：請確保 sound/gameover.mp3 檔案存在
"""

import pygame
import os
import sys


def test_gameover_sound():
    """測試失敗音效系統"""
    pygame.init()  # 完整初始化
    pygame.mixer.init()

    # 創建一個小窗口用於事件處理
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("失敗音效測試")

    # 檢查失敗音效（支援 MP3 和 WAV）
    sound_paths = [
        os.path.join(os.path.dirname(__file__), "sound", "gameover.mp3"),
        os.path.join(os.path.dirname(__file__), "sound", "gameover.wav"),
    ]

    gameover_sound = None
    for sound_path in sound_paths:
        print(f"檢查音效檔案：{sound_path}")
        if os.path.exists(sound_path):
            try:
                gameover_sound = pygame.mixer.Sound(sound_path)
                print(f"✅ 成功載入失敗音效：{sound_path}")
                break
            except Exception as e:
                print(f"❌ 載入失敗音效失敗：{e}")
                continue

    if not gameover_sound:
        print("❌ 錯誤：找不到 sound/gameover.mp3 或 sound/gameover.wav 檔案")
        print("請確保音效檔案存在於 sound 目錄中")
        print("或執行 python generate_test_gameover.py 生成測試音效")
        return False

    print("\n控制說明：")
    print("G - 播放失敗音效")
    print("Q - 退出測試")
    print("\n開始測試...")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    print("🔊 播放失敗音效...")
                    gameover_sound.play()
                elif event.key == pygame.K_q:
                    print("退出測試")
                    running = False

        clock.tick(60)

    pygame.quit()
    return True


if __name__ == "__main__":
    print("=== Jump King 失敗音效測試 ===")
    success = test_gameover_sound()
    if success:
        print("測試完成")
    else:
        print("測試失敗")
        sys.exit(1)
