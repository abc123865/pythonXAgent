#!/usr/bin/env python3
"""
從 .mepj 專案檔案提取音訊片段
根據專案設定提取指定的音訊片段並轉換為 MP3
"""

import json
import os
import subprocess
import shutil


def extract_audio_from_mepj():
    """從 .mepj 專案檔案提取音訊"""

    # 讀取解壓後的配置
    config_path = os.path.join("sound", "yee_extracted", "config.json")

    if not os.path.exists(config_path):
        print("❌ 找不到配置檔案")
        return False

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # 解析專案設定
    try:
        clips = config["data"]["content"]["timeline"]["clips"]
        if not clips:
            print("❌ 專案中沒有音訊片段")
            return False

        clip = clips[0]["clip"]
        timing = clips[0]["timing"]

        # 獲取原始檔案路徑
        source_path = clip["file"]["path"]
        print(f"📁 原始檔案: {source_path}")

        # 獲取時間資訊（以毫秒為單位）
        source_position = timing["sourcePosition"]  # 開始位置
        duration = timing["duration"]  # 持續時間
        sample_rate = clip["file"]["audioTracks"][0]["Audio"]["sampleRate"]

        # 轉換時間（從樣本數轉為秒）
        start_seconds = source_position / sample_rate
        duration_seconds = duration / sample_rate

        print(f"⏰ 開始時間: {start_seconds:.2f} 秒")
        print(f"⏰ 持續時間: {duration_seconds:.2f} 秒")
        print(f"🔊 採樣率: {sample_rate} Hz")

        # 檢查原始檔案是否存在
        if not os.path.exists(source_path):
            print(f"❌ 原始檔案不存在: {source_path}")

            # 檢查是否在當前目錄有同名檔案
            filename = os.path.basename(source_path)
            local_path = os.path.join("sound", filename)

            if os.path.exists(local_path):
                source_path = local_path
                print(f"✅ 找到本地檔案: {source_path}")
            else:
                print(f"💡 請將檔案 '{filename}' 放到 sound 目錄中")
                return False

        # 輸出檔案路徑
        output_path = os.path.join("sound", "yee.mp3")

        # 使用 ffmpeg 提取音訊片段
        if extract_with_ffmpeg(
            source_path, output_path, start_seconds, duration_seconds
        ):
            return True

        # 如果 ffmpeg 失敗，嘗試簡單複製（如果時間範圍是完整檔案）
        if start_seconds < 1 and duration_seconds > 250:  # 接近完整檔案
            print("🔄 嘗試複製完整檔案...")
            try:
                shutil.copy2(source_path, output_path)
                print("✅ 檔案複製成功")
                return True
            except Exception as e:
                print(f"❌ 檔案複製失敗: {e}")

        return False

    except Exception as e:
        print(f"❌ 解析專案配置失敗: {e}")
        return False


def extract_with_ffmpeg(source_path, output_path, start_seconds, duration_seconds):
    """使用 ffmpeg 提取音訊片段"""
    try:
        cmd = [
            "ffmpeg",
            "-i",
            source_path,
            "-ss",
            str(start_seconds),
            "-t",
            str(duration_seconds),
            "-acodec",
            "mp3",
            "-y",
            output_path,
        ]

        print(f"🚀 執行 ffmpeg 命令...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ ffmpeg 提取成功")
            return True
        else:
            print(f"❌ ffmpeg 提取失敗: {result.stderr}")
            return False

    except FileNotFoundError:
        print("❌ 找不到 ffmpeg，請安裝 ffmpeg")
        return False
    except Exception as e:
        print(f"❌ ffmpeg 執行失敗: {e}")
        return False


def test_extracted_audio():
    """測試提取的音訊是否可用"""
    output_path = os.path.join("sound", "yee.mp3")

    if not os.path.exists(output_path):
        print("❌ 提取的音訊檔案不存在")
        return False

    # 檢查檔案大小
    file_size = os.path.getsize(output_path)
    print(f"📏 音訊檔案大小: {file_size} bytes")

    # 測試 pygame 載入
    try:
        import pygame

        pygame.mixer.init()
        test_sound = pygame.mixer.Sound(output_path)
        print("🎵 音訊檔案可以正常載入到 pygame")
        pygame.quit()
        return True
    except Exception as e:
        print(f"⚠️  pygame 載入測試失敗: {e}")
        return False


if __name__ == "__main__":
    print("=== 從 .mepj 專案提取音訊 ===")

    if extract_audio_from_mepj():
        print("\n🎉 音訊提取成功！")
        if test_extracted_audio():
            print("✅ 音訊檔案可以正常使用")
        else:
            print("⚠️  音訊檔案可能有問題")
    else:
        print("\n❌ 音訊提取失敗")
        print("\n💡 可能的解決方案:")
        print("1. 確保原始音訊檔案存在")
        print("2. 安裝 ffmpeg")
        print("3. 檢查檔案權限")
