#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音效管理系統
處理遊戲中的所有音效播放 - 真正的 Popcat 音效 + 背景音樂
"""

import pygame
import threading
import time
import sys
import math
import array
import os
import subprocess
from config.game_config import SoundSystem


class SoundManager:
    """音效管理器"""

    def __init__(self):
        """初始化音效系統"""
        self.enabled = SoundSystem.SOUND_ENABLED
        self.volume = SoundSystem.SOUND_VOLUME

        # 背景音樂相關
        self.background_music_enabled = True
        self.background_music_volume = 0.3
        self.background_music_url = "https://www.youtube.com/watch?v=kK81m-A3qpU"
        self.background_music_file = None
        self.is_music_playing = False

        if self.enabled:
            try:
                # 初始化音效系統
                pygame.mixer.pre_init(
                    frequency=22050, size=-16, channels=2, buffer=1024
                )
                pygame.mixer.init()
                print("🔊 真正的 Popcat 音效系統初始化成功")

                # 檢查 FFmpeg 可用性
                self.check_ffmpeg_availability()

                # 初始化背景音樂
                self.setup_background_music()

            except pygame.error as e:
                print(f"⚠️ 音效系統初始化失敗: {e}")
                self.enabled = False
        else:
            print("🔇 Popcat 音效系統已停用")

    def check_ffmpeg_availability(self):
        """檢查 FFmpeg 可用性"""
        try:
            # 先嘗試系統 PATH 中的 ffmpeg
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            print("✅ 檢測到 FFmpeg，支援音頻格式轉換")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # 嘗試手動安裝的 FFmpeg 路徑
            try:
                subprocess.run(
                    [
                        "C:\\ffmpeg\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe",
                        "-version",
                    ],
                    capture_output=True,
                    check=True,
                )
                print("✅ 檢測到 FFmpeg（手動安裝），支援音頻格式轉換")
                return True
            except:
                print("⚠️ 未檢測到 FFmpeg")
                print("💡 提示：FFmpeg 可提供更好的音樂格式支援")
                return False

    def generate_popcat_sound(self, base_frequency, duration):
        """
        生成真正的 Popcat 音效 - 使用 numpy 優化版本

        Args:
            base_frequency (int): 基礎頻率 (Hz)
            duration (int): 持續時間 (毫秒)

        Returns:
            pygame.Sound: 生成的 popcat 音效物件
        """
        if not self.enabled:
            return None

        try:
            import numpy as np

            sample_rate = 22050
            frames = int(duration * sample_rate / 1000)

            # 生成時間數組
            t = np.linspace(0, duration / 1000, frames)

            # Popcat 特徵波形
            # 1. 快速攻擊階段 (前 5ms)
            attack_duration = 0.005
            attack_mask = t < attack_duration

            # 2. 衰減階段
            decay_mask = t >= attack_duration

            # 初始化波形
            wave = np.zeros(frames)

            # 攻擊階段：快速上升 + 噪音
            if np.any(attack_mask):
                attack_t = t[attack_mask]
                attack_envelope = attack_t / attack_duration

                # 基礎正弦波
                base_wave = np.sin(2 * np.pi * base_frequency * attack_t)

                # 添加噪音模擬 "p" 音
                noise = 0.3 * (np.random.random(len(attack_t)) * 2 - 1)

                wave[attack_mask] = attack_envelope * (0.7 * base_wave + 0.3 * noise)

            # 衰減階段：指數衰減
            if np.any(decay_mask):
                decay_t = t[decay_mask] - attack_duration
                decay_envelope = np.exp(-decay_t * 6)  # 快速衰減

                # 添加諧波讓聲音更豐富
                fundamental = np.sin(2 * np.pi * base_frequency * t[decay_mask])
                harmonic2 = 0.2 * np.sin(2 * np.pi * base_frequency * 2 * t[decay_mask])
                harmonic3 = 0.1 * np.sin(2 * np.pi * base_frequency * 3 * t[decay_mask])

                wave[decay_mask] = decay_envelope * (
                    fundamental + harmonic2 + harmonic3
                )

            # 正規化並轉換為 16-bit 整數
            wave = wave * 32767 * self.volume
            wave = np.clip(wave, -32767, 32767).astype(np.int16)

            # 創建立體聲數組
            stereo_wave = np.column_stack((wave, wave))

            # 創建 pygame Sound 物件
            sound = pygame.sndarray.make_sound(stereo_wave)
            return sound

        except ImportError:
            print("⚠️ numpy 未可用，使用簡化版音效生成")
            return self._generate_simple_tone_fallback(base_frequency, duration)
        except Exception as e:
            print(f"⚠️ 優化 Popcat 音效生成失敗: {e}")
            return self._generate_simple_tone_fallback(base_frequency, duration)

    def _generate_simple_tone_fallback(self, frequency, duration):
        """簡化版音效生成（不依賴 numpy）"""
        try:
            sample_rate = 22050
            frames = int(duration * sample_rate / 1000)

            # 創建波形數據
            wave_data = []
            for i in range(frames):
                t = i / sample_rate

                # 簡單的衰減包絡
                if t < 0.01:  # 攻擊階段
                    envelope = t / 0.01
                    noise = (hash(i) % 100 - 50) / 200.0  # 輕微噪音
                    wave = envelope * (math.sin(2 * math.pi * frequency * t) + noise)
                else:  # 衰減階段
                    decay_time = t - 0.01
                    envelope = math.exp(-decay_time * 4)
                    wave = envelope * math.sin(2 * math.pi * frequency * t)

                # 轉換為 16-bit
                sample = int(wave * 32767 * self.volume)
                sample = max(-32767, min(32767, sample))

                # 立體聲
                wave_data.extend([sample, sample])

            # 使用 array 創建音頻數據
            import array

            sound_array = array.array("h", wave_data)
            sound = pygame.sndarray.make_sound(sound_array)
            return sound

        except Exception as e:
            print(f"⚠️ 簡化音效生成失敗: {e}")
            # 最終回退到系統音效
            self._play_system_beep_fallback(frequency, duration)
            return None

    def _play_system_beep_fallback(self, frequency, duration):
        """系統音效回退方案"""
        try:
            if sys.platform == "win32":
                import winsound

                winsound.MessageBeep(winsound.MB_OK)
            else:
                print("\a", end="", flush=True)
        except:
            pass

    def play_popcat_async(self, frequency, duration):
        """異步播放 popcat 音效"""
        if not self.enabled:
            return

        def play_sound():
            sound = self.generate_popcat_sound(frequency, duration)
            if sound and hasattr(sound, "play"):
                sound.play()

        threading.Thread(target=play_sound, daemon=True).start()

    # === 遊戲引擎所需的音效方法 ===

    def play_key_press(self):
        """播放一般按鍵音效 - Popcat 風格"""
        self.play_popcat_async(1300, 80)

    def play_jump(self):
        """播放跳躍音效 - 高頻短促的 popcat"""
        self.play_popcat_async(1500, 100)

    def play_shield(self):
        """播放護盾音效 - 低到高的 Popcat"""
        self.play_popcat_async(1000, 150)

    def play_menu_move(self):
        """播放選單移動音效 - 輕快 Popcat"""
        self.play_popcat_async(1250, 70)

    def play_menu_select(self):
        """播放選單選擇音效 - 確認 Popcat"""
        # 播放上升音調的確認音效
        self.play_popcat_async(1300, 100)

        def delayed_sound():
            time.sleep(0.08)
            self.play_popcat_async(1600, 100)

        threading.Thread(target=delayed_sound, daemon=True).start()

    def play_pause_sound(self):
        """播放暫停音效 - 低頻較長的 popcat"""
        self.play_popcat_async(1100, 150)

    def play_game_over_sound(self):
        """播放遊戲結束音效 - 下降頻率的連續 popcat"""
        frequencies = [1400, 1200, 1000, 800]  # 下降音階
        for i, freq in enumerate(frequencies):

            def play_delayed(frequency, delay):
                def delayed_play():
                    time.sleep(delay)
                    self.play_popcat_async(frequency, 120)

                threading.Thread(target=delayed_play, daemon=True).start()

            play_delayed(freq, i * 0.1)  # 每 100ms 播放一個音

    def play_death_sound(self):
        """播放死亡音效 - ooooof 音效"""
        # 創建長而低沉的 "ooooof" 音效
        # 使用下降的頻率模擬失望的聲音
        frequencies = [800, 700, 600, 500, 400]  # 下降音階
        durations = [200, 250, 300, 350, 400]  # 逐漸變長

        for i, (freq, dur) in enumerate(zip(frequencies, durations)):

            def play_delayed(frequency, duration, delay):
                def delayed_play():
                    time.sleep(delay)
                    self.play_popcat_async(frequency, duration)

                threading.Thread(target=delayed_play, daemon=True).start()

            play_delayed(freq, dur, i * 0.15)  # 每 150ms 播放一個音

    def play_lightning_sound(self):
        """播放閃電音效 - 急促的高頻爆裂聲"""
        # 模擬閃電的多層音效
        # 第一層：急促的高頻爆裂音
        frequencies = [2000, 2400, 1800, 2200, 1600]  # 高頻率範圍
        durations = [30, 25, 35, 20, 40]  # 短促時長

        for i, (freq, dur) in enumerate(zip(frequencies, durations)):

            def play_delayed(frequency, duration, delay):
                def delayed_play():
                    time.sleep(delay)
                    self.play_popcat_async(frequency, duration)

                threading.Thread(target=delayed_play, daemon=True).start()

            play_delayed(freq, dur, i * 0.02)  # 每 20ms 播放一個音

    def play_meteor_warning_sound(self):
        """播放隕石警告音效 - 急促的上升警告音"""
        frequencies = [1000, 1200, 1400, 1600]  # 上升音階
        for i, freq in enumerate(frequencies):

            def play_delayed(frequency, delay):
                def delayed_play():
                    time.sleep(delay)
                    self.play_popcat_async(frequency, 60)  # 短促警告音

                threading.Thread(target=delayed_play, daemon=True).start()

            play_delayed(freq, i * 0.05)  # 快速連續播放

    def play_meteor_impact_sound(self):
        """播放隕石撞擊音效 - 低沉的轟鳴聲"""
        # 模擬撞擊的多層音效
        # 第一層：低頻撞擊音
        self.play_popcat_async(400, 300)

        # 第二層：中頻振動音（延遲播放）
        def delayed_mid_freq():
            time.sleep(0.1)
            self.play_popcat_async(600, 200)

        threading.Thread(target=delayed_mid_freq, daemon=True).start()

        # 第三層：高頻余響（再延遲播放）
        def delayed_high_freq():
            time.sleep(0.2)
            self.play_popcat_async(1000, 150)

        threading.Thread(target=delayed_high_freq, daemon=True).start()

    def play_game_start_sound(self):
        """播放遊戲開始音效 - 激勵的上升音階"""
        # 三連音上升音階，營造開始的興奮感
        # 第一個音：低音開始
        self.play_popcat_async(523, 200)  # C5

        # 第二個音：中音（延遲播放）
        def delayed_mid_note():
            time.sleep(0.25)
            self.play_popcat_async(659, 200)  # E5

        threading.Thread(target=delayed_mid_note, daemon=True).start()

        # 第三個音：高音結尾（再延遲播放）
        def delayed_high_note():
            time.sleep(0.5)
            self.play_popcat_async(784, 300)  # G5，稍長一點作為結尾

        threading.Thread(target=delayed_high_note, daemon=True).start()

    def set_volume(self, volume):
        """
        設定音量

        Args:
            volume (float): 音量 (0.0 到 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))

    def toggle_sound(self):
        """切換音效開關"""
        self.enabled = not self.enabled
        status = "開啟" if self.enabled else "關閉"
        print(f"🔊 音效系統已{status}")

    def setup_background_music(self):
        """設置背景音樂"""
        if not self.background_music_enabled:
            return

        try:
            # 創建音樂目錄
            music_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "music")
            os.makedirs(music_dir, exist_ok=True)

            self.background_music_file = os.path.join(music_dir, "background_music.wav")

            # 檢查是否已有音樂文件
            if not os.path.exists(self.background_music_file):
                print("🎵 正在下載背景音樂...")
                self.download_background_music()

            # 嘗試載入背景音樂，按優先順序
            music_files_to_try = [
                os.path.join(
                    music_dir, "background_music_converted.wav"
                ),  # 首選：YouTube 轉換的高品質音樂
                os.path.join(
                    music_dir, "background_music_fallback.wav"
                ),  # 備用：合成音樂
            ]

            music_loaded = False
            for music_file in music_files_to_try:
                if os.path.exists(music_file):
                    try:
                        pygame.mixer.music.load(music_file)
                        pygame.mixer.music.set_volume(self.background_music_volume)
                        self.background_music_file = music_file
                        music_loaded = True
                        print(f"🎵 背景音樂載入成功: {os.path.basename(music_file)}")

                        # 自動開始播放背景音樂
                        pygame.mixer.music.play(-1)  # -1 表示無限循環
                        self.is_music_playing = True
                        print("🎵 背景音樂自動開始播放")

                        break
                    except pygame.error as e:
                        print(f"⚠️ 無法載入 {os.path.basename(music_file)}: {e}")
                        continue

            if not music_loaded:
                print("⚠️ 無法載入任何音樂文件，創建備用音樂")
                self.create_fallback_music()

                # 重新嘗試載入剛創建的備用音樂
                fallback_file = os.path.join(music_dir, "background_music_fallback.wav")
                if os.path.exists(fallback_file):
                    try:
                        pygame.mixer.music.load(fallback_file)
                        pygame.mixer.music.set_volume(self.background_music_volume)
                        self.background_music_file = fallback_file
                        music_loaded = True
                        print("🎵 備用背景音樂載入成功")

                        # 自動開始播放背景音樂
                        pygame.mixer.music.play(-1)  # -1 表示無限循環
                        self.is_music_playing = True
                        print("🎵 背景音樂自動開始播放")

                    except pygame.error as e:
                        print(f"⚠️ 連備用音樂也無法載入: {e}")
                        self.background_music_enabled = False

            if not music_loaded:
                print("⚠️ 所有音樂載入失敗，停用背景音樂")
                self.background_music_enabled = False

        except Exception as e:
            print(f"⚠️ 背景音樂設置失敗: {e}")
            self.background_music_enabled = False

    def download_background_music(self):
        """下載背景音樂"""
        try:
            # 嘗試使用 yt-dlp Python 模組下載音樂
            import yt_dlp

            music_dir = os.path.dirname(self.background_music_file)

            print("🎵 正在使用 yt-dlp 下載背景音樂...")

            # 方法1: 嘗試直接下載最佳音頻格式（不轉換）
            try:
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": os.path.join(music_dir, "background_music.%(ext)s"),
                    "noplaylist": True,
                    "quiet": True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # 先獲取視頻資訊
                    info = ydl.extract_info(self.background_music_url, download=False)

                    # 下載音頻
                    ydl.download([self.background_music_url])

                    # 尋找下載的文件
                    possible_extensions = ["webm", "m4a", "mp4", "opus", "mp3", "wav"]
                    downloaded_file = None

                    for ext in possible_extensions:
                        candidate = os.path.join(music_dir, f"background_music.{ext}")
                        if os.path.exists(candidate):
                            downloaded_file = candidate
                            break

                    if downloaded_file:
                        print(
                            f"✅ 背景音樂下載成功: {os.path.basename(downloaded_file)}"
                        )

                        # 如果下載的是 WebM 格式，嘗試轉換為 WAV
                        if downloaded_file.endswith(".webm"):
                            wav_file = os.path.join(music_dir, "background_music.wav")
                            if self.convert_audio_to_wav(downloaded_file, wav_file):
                                self.background_music_file = wav_file
                                return

                        # 根據文件擴展名設定音樂文件路徑
                        self.background_music_file = downloaded_file
                        return

            except Exception as direct_error:
                print(f"⚠️ 直接下載失敗: {direct_error}")

            # 方法2: 如果有 FFmpeg，嘗試轉換為 MP3
            try:
                # 檢查是否有 FFmpeg
                import subprocess

                subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)

                print("🎵 檢測到 FFmpeg，嘗試轉換為 MP3...")
                mp3_file = os.path.join(music_dir, "background_music.mp3")
                ydl_opts = {
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                    "outtmpl": mp3_file.replace(".mp3", ".%(ext)s"),
                    "noplaylist": True,
                    "quiet": True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([self.background_music_url])

                    if os.path.exists(mp3_file):
                        self.background_music_file = mp3_file
                        print("✅ 背景音樂下載並轉換成功 (MP3)")
                        return

            except (subprocess.CalledProcessError, FileNotFoundError):
                print("⚠️ 未找到 FFmpeg，無法轉換音頻格式")
            except Exception as ffmpeg_error:
                print(f"⚠️ FFmpeg 轉換失敗: {ffmpeg_error}")

            print("⚠️ 所有下載方法都失敗，使用備用音樂")
            self.create_fallback_music()

        except ImportError:
            print("⚠️ 找不到 yt-dlp 模組，請安裝: pip install yt-dlp")
            self.create_fallback_music()
        except Exception as e:
            print(f"⚠️ 下載背景音樂時發生錯誤: {e}")
            print("🎵 使用備用音樂...")
            self.create_fallback_music()

    def convert_audio_to_wav(self, input_file, output_file):
        """使用 FFmpeg 將音頻文件轉換為 WAV 格式"""
        try:
            print(
                f"🎵 正在轉換音頻格式: {os.path.basename(input_file)} -> {os.path.basename(output_file)}"
            )

            # FFmpeg 轉換命令（優先使用手動安裝的路徑）
            ffmpeg_paths = [
                "ffmpeg",  # 系統 PATH
                "C:\\ffmpeg\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe",  # 手動安裝
            ]

            for ffmpeg_cmd in ffmpeg_paths:
                try:
                    # 測試 FFmpeg 是否可用
                    subprocess.run(
                        [ffmpeg_cmd, "-version"], capture_output=True, check=True
                    )

                    # 執行轉換
                    cmd = [
                        ffmpeg_cmd,
                        "-i",
                        input_file,
                        "-ar",
                        "22050",
                        "-ac",
                        "2",
                        "-acodec",
                        "pcm_s16le",
                        "-y",
                        output_file,
                    ]

                    result = subprocess.run(cmd, capture_output=True, text=True)

                    if result.returncode == 0 and os.path.exists(output_file):
                        print(
                            f"✅ FFmpeg 音頻轉換成功: {os.path.basename(output_file)}"
                        )
                        return True

                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue

            print("⚠️ FFmpeg 不可用，無法轉換音頻格式")
            return False

        except Exception as e:
            print(f"⚠️ 音頻轉換失敗: {e}")
            return False

    def create_fallback_music(self):
        """創建備用音樂（豐富的遊戲背景音樂）"""
        try:
            print("🎵 正在創建備用背景音樂...")

            # 生成一個豐富的遊戲背景音樂
            import numpy as np

            sample_rate = 22050
            duration = 24  # 24秒循環，較長的循環避免重複感
            frames = sample_rate * duration

            # 生成時間數組
            t = np.linspace(0, duration, frames)

            # 創建動態的遊戲背景音樂
            # 主旋律：使用 C 大調五聲音階，營造愉快的遊戲氛圍

            # 基礎頻率（更高頻率，更清晰）
            bass_freq = 130.81  # C3
            mid_freq = 261.63  # C4
            high_freq = 523.25  # C5

            # 創建分段式音樂結構
            segment_length = duration / 4  # 4個段落

            wave = np.zeros(frames)

            for i in range(4):
                start_idx = int(i * segment_length * sample_rate)
                end_idx = int((i + 1) * segment_length * sample_rate)
                segment_t = t[start_idx:end_idx]

                if i == 0:  # 第一段：溫和的和弦
                    wave[start_idx:end_idx] = (
                        0.15 * np.sin(2 * np.pi * mid_freq * segment_t)  # C4 主音
                        + 0.12
                        * np.sin(2 * np.pi * (mid_freq * 5 / 4) * segment_t)  # E4 三度
                        + 0.10
                        * np.sin(2 * np.pi * (mid_freq * 3 / 2) * segment_t)  # G4 五度
                        + 0.08 * np.sin(2 * np.pi * bass_freq * segment_t)  # C3 低音
                    )
                elif i == 1:  # 第二段：加入節奏感
                    # 主旋律 + 輕微的節拍
                    rhythm = np.sin(2 * np.pi * 2 * segment_t)  # 2Hz 節拍
                    envelope = 0.5 + 0.3 * rhythm
                    wave[start_idx:end_idx] = envelope * (
                        0.18 * np.sin(2 * np.pi * (mid_freq * 6 / 5) * segment_t)  # D4
                        + 0.15
                        * np.sin(2 * np.pi * (mid_freq * 5 / 4) * segment_t)  # E4
                        + 0.12 * np.sin(2 * np.pi * mid_freq * segment_t)  # C4
                        + 0.08 * np.sin(2 * np.pi * bass_freq * segment_t)  # C3
                    )
                elif i == 2:  # 第三段：高潮部分
                    wave[start_idx:end_idx] = (
                        0.20 * np.sin(2 * np.pi * high_freq * segment_t)  # C5 高音
                        + 0.15
                        * np.sin(2 * np.pi * (mid_freq * 3 / 2) * segment_t)  # G4
                        + 0.12 * np.sin(2 * np.pi * mid_freq * segment_t)  # C4
                        + 0.08 * np.sin(2 * np.pi * bass_freq * segment_t)  # C3
                        + 0.05
                        * np.sin(2 * np.pi * (high_freq * 3 / 2) * segment_t)  # G5 泛音
                    )
                else:  # 第四段：收尾，回到溫和
                    fade_out_local = np.linspace(1, 0.3, len(segment_t))
                    wave[start_idx:end_idx] = fade_out_local * (
                        0.15 * np.sin(2 * np.pi * mid_freq * segment_t)  # C4
                        + 0.12
                        * np.sin(2 * np.pi * (mid_freq * 5 / 4) * segment_t)  # E4
                        + 0.10
                        * np.sin(2 * np.pi * (mid_freq * 3 / 2) * segment_t)  # G4
                        + 0.08 * np.sin(2 * np.pi * bass_freq * segment_t)  # C3
                    )

            # 整體淡入淡出
            fade_samples = sample_rate // 2  # 0.5秒淡入淡出
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)

            wave[:fade_samples] *= fade_in
            wave[-fade_samples:] *= fade_out

            # 添加輕微的回響效果
            delay_samples = int(0.1 * sample_rate)  # 100ms 延遲
            echo_wave = np.zeros_like(wave)
            echo_wave[delay_samples:] = wave[:-delay_samples] * 0.3
            wave = wave + echo_wave

            # 轉換為 16-bit 立體聲（增加音量）
            wave = (wave * 32767 * 0.7).astype(np.int16)  # 提高到 0.7 音量
            stereo_wave = np.column_stack((wave, wave))

            # 確定音樂目錄和文件路徑
            music_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "music")
            os.makedirs(music_dir, exist_ok=True)
            fallback_file = os.path.join(music_dir, "background_music_fallback.wav")

            # 保存為 WAV 文件
            import wave as wave_module

            with wave_module.open(fallback_file, "wb") as wav_file:
                wav_file.setnchannels(2)  # 立體聲
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(stereo_wave.tobytes())

            # 更新音樂文件路徑
            self.background_music_file = fallback_file
            print(f"✅ 豐富的備用背景音樂創建成功: {fallback_file}")
            return True

        except ImportError:
            print("⚠️ numpy 不可用，創建簡化版備用音樂")
            return self.create_simple_fallback_music()
        except Exception as e:
            print(f"⚠️ 創建備用音樂失敗: {e}")
            return self.create_simple_fallback_music()

    def create_simple_fallback_music(self):
        """創建簡化版備用音樂（不依賴 numpy，但依然動聽）"""
        try:
            import math
            import wave as wave_module

            print("🎵 正在創建簡化版備用音樂...")

            sample_rate = 22050
            duration = 16  # 16秒循環
            frames = sample_rate * duration

            # 定義更豐富的和弦進行
            # C - Am - F - G 經典進行
            chord_progression = [
                # C major (C-E-G)
                [(261.63, 0.25), (329.63, 0.20), (392.00, 0.15)],
                # A minor (A-C-E)
                [(220.00, 0.25), (261.63, 0.20), (329.63, 0.15)],
                # F major (F-A-C)
                [(174.61, 0.25), (220.00, 0.20), (261.63, 0.15)],
                # G major (G-B-D)
                [(196.00, 0.25), (246.94, 0.20), (293.66, 0.15)],
            ]

            # 生成音樂
            wave_data = []
            chord_duration = duration / len(chord_progression)

            for i in range(frames):
                t = i / sample_rate

                # 確定當前應該播放哪個和弦
                chord_index = int(t / chord_duration) % len(chord_progression)
                current_chord = chord_progression[chord_index]

                # 計算當前和弦內的時間
                chord_time = t % chord_duration

                # 生成和弦音
                sample = 0
                for freq, amplitude in current_chord:
                    # 基本音符
                    sample += amplitude * math.sin(2 * math.pi * freq * t)
                    # 添加泛音讓聲音更豐富
                    sample += amplitude * 0.1 * math.sin(2 * math.pi * freq * 2 * t)

                # 添加輕微的琶音效果
                arpeggio_speed = 8  # 琶音速度
                arpeggio_note = int((chord_time * arpeggio_speed) % len(current_chord))
                arpeggio_freq, arpeggio_amp = current_chord[arpeggio_note]
                sample += (
                    arpeggio_amp * 0.3 * math.sin(2 * math.pi * arpeggio_freq * 2 * t)
                )

                # 添加節拍感
                beat_freq = 0.5  # 每2秒一拍
                beat_envelope = 0.8 + 0.2 * math.sin(2 * math.pi * beat_freq * t)
                sample *= beat_envelope

                # 整體淡入淡出
                if i < sample_rate:  # 第一秒淡入
                    sample *= i / sample_rate
                elif i > frames - sample_rate:  # 最後一秒淡出
                    sample *= (frames - i) / sample_rate

                # 轉換為 16-bit 整數（提高音量）
                sample_int = int(sample * 32767 * 0.6)  # 提高到 0.6 音量
                sample_int = max(-32767, min(32767, sample_int))

                # 立體聲（左右聲道相同）
                wave_data.extend([sample_int, sample_int])

            # 確定音樂目錄和文件路徑
            music_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "music")
            os.makedirs(music_dir, exist_ok=True)
            fallback_file = os.path.join(music_dir, "background_music_fallback.wav")

            # 保存為 WAV 文件
            with wave_module.open(fallback_file, "wb") as wav_file:
                wav_file.setnchannels(2)  # 立體聲
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)

                # 轉換為 bytes
                import array

                sound_array = array.array("h", wave_data)
                wav_file.writeframes(sound_array.tobytes())

            # 更新音樂文件路徑
            self.background_music_file = fallback_file
            print(f"✅ 簡化版動聽背景音樂創建成功: {fallback_file}")
            return True

        except Exception as e:
            print(f"⚠️ 創建簡化版備用音樂失敗: {e}")
            self.background_music_enabled = False
            return False

    def start_background_music(self):
        """開始播放背景音樂"""
        if not self.background_music_enabled or not self.enabled:
            return

        try:
            if self.background_music_file and os.path.exists(
                self.background_music_file
            ):
                pygame.mixer.music.load(self.background_music_file)
                volume = max(0.6, self.background_music_volume)  # 至少 0.6 音量
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)  # -1 表示無限循環
                self.is_music_playing = True
                print(
                    f"✅ 背景音樂開始播放: {os.path.basename(self.background_music_file)}"
                )
            else:
                print("🔄 嘗試重新設置背景音樂...")
                self.setup_background_music()

        except Exception as e:
            print(f"❌ 播放背景音樂失敗: {e}")
            self.background_music_enabled = False

    def stop_background_music(self):
        """停止背景音樂"""
        try:
            pygame.mixer.music.stop()
            self.is_music_playing = False
            print("🎵 背景音樂已停止")
        except Exception as e:
            print(f"⚠️ 停止背景音樂失敗: {e}")

    def toggle_background_music(self):
        """切換背景音樂開關"""
        self.background_music_enabled = not self.background_music_enabled

        if self.background_music_enabled:
            print("🎵 背景音樂已開啟")
            self.start_background_music()
        else:
            print("🔇 背景音樂已關閉")
            self.stop_background_music()

    def set_music_volume(self, volume):
        """設置背景音樂音量"""
        self.background_music_volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.background_music_volume)
        except Exception as e:
            print(f"⚠️ 設置音樂音量失敗: {e}")

    def cleanup(self):
        """清理音效系統"""
        # 停止背景音樂
        if self.is_music_playing:
            self.stop_background_music()

        if self.enabled:
            try:
                pygame.mixer.quit()
                print("🔊 音效系統已清理")
            except:
                pass


# 全域音效管理器實例
sound_manager = None


def get_sound_manager():
    """取得音效管理器實例"""
    global sound_manager
    if sound_manager is None:
        sound_manager = SoundManager()
    return sound_manager
