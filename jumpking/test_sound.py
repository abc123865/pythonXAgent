#!/usr/bin/env python3
"""
音效測試腳本
測試jump.mp3音效是否能正常播放
"""

import pygame
import os
import time


def test_sound():
    print("初始化pygame...")
    pygame.init()
    pygame.mixer.init()

    # 載入音效
    sound_path = os.path.join(os.path.dirname(__file__), "sound", "jump.mp3")
    print(f"嘗試載入音效: {sound_path}")

    if not os.path.exists(sound_path):
        print(f"錯誤: 找不到音效文件 {sound_path}")
        return False

    try:
        jump_sound = pygame.mixer.Sound(sound_path)
        print("音效載入成功！")

        # 設置音量
        jump_sound.set_volume(0.7)
        print("音量設置為70%")

        # 播放音效
        print("播放跳躍音效...")
        jump_sound.play()

        # 等待音效播放完成
        time.sleep(2)

        print("音效測試完成！")
        return True

    except Exception as e:
        print(f"音效載入或播放失敗: {e}")
        return False

    finally:
        pygame.quit()


if __name__ == "__main__":
    print("=== Jump King 音效測試 ===")
    success = test_sound()
    if success:
        print("✅ 音效系統工作正常！")
    else:
        print("❌ 音效系統有問題，請檢查音效文件。")
