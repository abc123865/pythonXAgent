#!/usr/bin/env python3
"""
通關音效測試腳本
測試golfclap.mp3音效是否能正常播放
"""

import pygame
import os
import time


def test_victory_sound():
    print("初始化pygame...")
    pygame.init()
    pygame.mixer.init()

    # 載入通關音效
    sound_path = os.path.join(os.path.dirname(__file__), "sound", "golfclap.mp3")
    print(f"嘗試載入通關音效: {sound_path}")

    if not os.path.exists(sound_path):
        print(f"錯誤: 找不到音效文件 {sound_path}")
        return False

    try:
        victory_sound = pygame.mixer.Sound(sound_path)
        print("通關音效載入成功！")

        # 設置音量
        victory_sound.set_volume(0.7)
        print("音量設置為70%")

        # 播放音效
        print("播放通關音效...")
        victory_sound.play()

        # 等待音效播放完成（通關音效通常比較長）
        time.sleep(5)

        print("通關音效測試完成！")
        return True

    except Exception as e:
        print(f"音效載入或播放失敗: {e}")
        return False

    finally:
        pygame.quit()


def test_both_sounds():
    """測試兩種音效"""
    print("=== 測試跳躍音效 ===")
    pygame.init()
    pygame.mixer.init()

    try:
        # 測試跳躍音效
        jump_path = os.path.join(os.path.dirname(__file__), "sound", "jump.mp3")
        jump_sound = pygame.mixer.Sound(jump_path)
        jump_sound.set_volume(0.7)
        print("播放跳躍音效...")
        jump_sound.play()
        time.sleep(2)

        # 測試通關音效
        print("\n=== 測試通關音效 ===")
        victory_path = os.path.join(os.path.dirname(__file__), "sound", "golfclap.mp3")
        victory_sound = pygame.mixer.Sound(victory_path)
        victory_sound.set_volume(0.7)
        print("播放通關音效...")
        victory_sound.play()
        time.sleep(5)

        print("\n✅ 所有音效測試完成！")
        return True

    except Exception as e:
        print(f"音效測試失敗: {e}")
        return False

    finally:
        pygame.quit()


if __name__ == "__main__":
    print("=== Jump King 通關音效測試 ===")
    success = test_victory_sound()
    if success:
        print("✅ 通關音效系統工作正常！")
        print("\n現在測試所有音效...")
        test_both_sounds()
    else:
        print("❌ 通關音效系統有問題，請檢查音效文件。")
