#!/usr/bin/env python3
"""
生成簡單的失敗音效用於測試
在取得真正的 YouTube 音頻之前的臨時解決方案
"""

import pygame
import numpy as np
import os


def generate_test_gameover_sound():
    """生成簡單的失敗音效"""
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

    # 音頻參數
    duration = 3.0  # 3秒
    sample_rate = 22050

    # 生成時間軸
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # 創建失敗音效（低音下降音調）
    # 從 200Hz 下降到 50Hz
    frequency_start = 200
    frequency_end = 50
    frequency = frequency_start * (frequency_end / frequency_start) ** (t / duration)

    # 生成正弦波
    wave = np.sin(2 * np.pi * frequency * t)

    # 添加音量包絡（漸弱效果）
    envelope = np.exp(-t * 2)  # 指數衰減
    wave *= envelope

    # 標準化並轉換為16位音頻
    wave = np.int16(wave * 32767 * 0.3)  # 30% 音量

    # 創建立體聲
    stereo_wave = np.column_stack((wave, wave))

    # 確保數組是連續的
    stereo_wave = np.ascontiguousarray(stereo_wave, dtype=np.int16)

    # 創建 pygame Sound 對象
    sound = pygame.sndarray.make_sound(stereo_wave)

    # 保存到文件
    sound_path = os.path.join(os.path.dirname(__file__), "sound", "gameover.mp3")

    # 將音頻數據寫入 WAV 文件（pygame 無法直接保存 MP3）
    wav_path = sound_path.replace(".mp3", ".wav")
    pygame.mixer.music.stop()

    # 使用 pygame 保存
    try:
        # 創建臨時音頻
        pygame.mixer.music.load = None

        # 直接使用文件操作
        import wave

        with wave.open(wav_path, "w") as wav_file:
            wav_file.setnchannels(2)  # 立體聲
            wav_file.setsampwidth(2)  # 16位
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(stereo_wave.tobytes())

        print(f"✅ 成功生成測試失敗音效：{wav_path}")
        print("注意：這是臨時測試音效，建議使用真正的 YouTube 音頻")
        return True

    except Exception as e:
        print(f"❌ 生成音效失敗：{e}")
        return False


if __name__ == "__main__":
    print("=== 生成測試失敗音效 ===")

    # 檢查 numpy 是否可用
    try:
        import numpy as np
    except ImportError:
        print("❌ 需要安裝 numpy：pip install numpy")
        exit(1)

    success = generate_test_gameover_sound()
    if success:
        print("\n現在可以執行 test_gameover_sound.py 測試音效系統")
    else:
        print("\n生成失敗，請檢查錯誤訊息")
