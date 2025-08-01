#!/usr/bin/env python3
"""
測試 yee.mp3 音效
確保從 .mepj 專案提取的音訊可以正常播放
"""

import pygame
import os
import sys


def test_yee_sound():
    """測試 yee.mp3 音效"""
    pygame.init()
    pygame.mixer.init()

    # 創建測試視窗
    screen = pygame.display.set_mode((500, 400))
    pygame.display.set_caption("Yee 音效測試")

    # 載入 yee 音效
    sound_path = os.path.join("sound", "yee.mp3")

    if not os.path.exists(sound_path):
        print(f"❌ 找不到音效檔案: {sound_path}")
        return False

    try:
        yee_sound = pygame.mixer.Sound(sound_path)
        print(f"✅ 成功載入 yee 音效: {sound_path}")

        # 檢查音效屬性
        file_size = os.path.getsize(sound_path)
        print(f"📏 檔案大小: {file_size} bytes")

    except Exception as e:
        print(f"❌ 載入音效失敗: {e}")
        return False

    print("\n🎮 控制說明:")
    print("Y - 播放 Yee 音效")
    print("+ - 增加音量")
    print("- - 減少音量")
    print("Q - 退出測試")
    print("\n🎵 開始測試...")

    volume = 0.7
    yee_sound.set_volume(volume)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    print(f"🔊 播放 Yee 音效 (音量: {volume:.1f})")
                    yee_sound.play()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    volume = min(1.0, volume + 0.1)
                    yee_sound.set_volume(volume)
                    print(f"🔊 音量增加到: {volume:.1f}")
                elif event.key == pygame.K_MINUS:
                    volume = max(0.0, volume - 0.1)
                    yee_sound.set_volume(volume)
                    print(f"🔉 音量減少到: {volume:.1f}")
                elif event.key == pygame.K_q:
                    running = False

        # 簡單的視覺反饋
        screen.fill((50, 50, 100))

        # 顯示說明文字（簡單版本）
        font = pygame.font.Font(None, 36)
        text = font.render("Press Y to play Yee sound", True, (255, 255, 255))
        screen.blit(text, (50, 180))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return True


if __name__ == "__main__":
    print("=== Yee 音效測試 ===")
    success = test_yee_sound()
    if success:
        print("✅ 測試完成")
    else:
        print("❌ 測試失敗")
        sys.exit(1)
