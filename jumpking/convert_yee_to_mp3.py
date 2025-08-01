#!/usr/bin/env python3
"""
音頻格式轉換工具
將 yee.mepj 轉換為 MP3 格式

支援的轉換方法：
1. 使用 pydub 進行轉換
2. 使用 ffmpeg 進行轉換
3. 檔案重命名（如果是標準音頻格式）
"""

import os
import shutil
import subprocess
import sys


def check_ffmpeg():
    """檢查 ffmpeg 是否可用"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_pydub():
    """檢查 pydub 是否可用"""
    try:
        import pydub

        return True
    except ImportError:
        return False


def convert_with_pydub(input_path, output_path):
    """使用 pydub 轉換音頻"""
    try:
        from pydub import AudioSegment

        # 嘗試載入音頻文件
        # .mepj 可能是重命名的音頻文件
        audio = AudioSegment.from_file(input_path)

        # 導出為 MP3
        audio.export(output_path, format="mp3")
        return True
    except Exception as e:
        print(f"pydub 轉換失敗: {e}")
        return False


def convert_with_ffmpeg(input_path, output_path):
    """使用 ffmpeg 轉換音頻"""
    try:
        cmd = ["ffmpeg", "-i", input_path, "-codec:a", "mp3", "-y", output_path]
        result = subprocess.run(cmd, capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg 轉換失敗: {e}")
        return False


def try_rename_copy(input_path, output_path):
    """嘗試簡單複製並重命名（如果是標準音頻格式）"""
    try:
        shutil.copy2(input_path, output_path)
        print(f"檔案已複製並重命名為: {output_path}")
        return True
    except Exception as e:
        print(f"檔案複製失敗: {e}")
        return False


def convert_yee_to_mp3():
    """將 yee.mepj 轉換為 MP3"""
    input_path = os.path.join(os.path.dirname(__file__), "sound", "yee.mepj")
    output_path = os.path.join(os.path.dirname(__file__), "sound", "yee.mp3")

    if not os.path.exists(input_path):
        print(f"❌ 找不到輸入檔案: {input_path}")
        return False

    print(f"📁 輸入檔案: {input_path}")
    print(f"📁 輸出檔案: {output_path}")

    # 檢查檔案大小
    file_size = os.path.getsize(input_path)
    print(f"📏 檔案大小: {file_size} bytes")

    # 嘗試不同的轉換方法
    methods = []

    if check_pydub():
        methods.append(("pydub", convert_with_pydub))
        print("✅ pydub 可用")
    else:
        print("⚠️  pydub 不可用")

    if check_ffmpeg():
        methods.append(("ffmpeg", convert_with_ffmpeg))
        print("✅ ffmpeg 可用")
    else:
        print("⚠️  ffmpeg 不可用")

    methods.append(("重命名複製", try_rename_copy))

    print(f"\n🔄 開始轉換，共有 {len(methods)} 種方法可嘗試...")

    for method_name, method_func in methods:
        print(f"\n🚀 嘗試使用 {method_name} 轉換...")

        if method_func(input_path, output_path):
            print(f"✅ 使用 {method_name} 轉換成功！")

            # 檢查輸出檔案
            if os.path.exists(output_path):
                output_size = os.path.getsize(output_path)
                print(f"📏 輸出檔案大小: {output_size} bytes")

                # 測試是否可以用 pygame 載入
                try:
                    import pygame

                    pygame.mixer.init()
                    test_sound = pygame.mixer.Sound(output_path)
                    print("🎵 檔案可以正常載入到 pygame")
                    pygame.quit()
                except Exception as e:
                    print(f"⚠️  pygame 載入測試失敗: {e}")

                return True
            else:
                print(f"❌ 輸出檔案不存在: {output_path}")
        else:
            print(f"❌ {method_name} 轉換失敗")

    print("\n❌ 所有轉換方法都失敗了")
    return False


def install_dependencies():
    """安裝轉換所需的依賴"""
    print("=== 安裝音頻轉換依賴 ===")

    # 安裝 pydub
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pydub"])
        print("✅ pydub 安裝成功")
    except subprocess.CalledProcessError:
        print("❌ pydub 安裝失敗")

    print("\n📋 ffmpeg 安裝說明:")
    print("1. 訪問 https://ffmpeg.org/download.html")
    print("2. 下載 Windows 版本")
    print("3. 解壓並將 ffmpeg.exe 添加到 PATH")
    print("4. 或使用 chocolatey: choco install ffmpeg")


if __name__ == "__main__":
    print("=== yee.mepj 轉 MP3 轉換工具 ===")

    if len(sys.argv) > 1 and sys.argv[1] == "--install-deps":
        install_dependencies()
    else:
        success = convert_yee_to_mp3()
        if success:
            print("\n🎉 轉換完成！")
            print("現在可以在遊戲中使用 yee.mp3 音效了")
        else:
            print("\n💡 如果轉換失敗，請嘗試:")
            print("python convert_yee_to_mp3.py --install-deps")
            print("然後重新運行轉換")
