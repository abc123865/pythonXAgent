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
                
                # 初始化背景音樂
                self.setup_background_music()
                
            except pygame.error as e:
                print(f"⚠️ 音效系統初始化失敗: {e}")
                self.enabled = False
        else:
            print("🔇 Popcat 音效系統已停用")

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

    def play_duck_sound(self):
        """播放蹲下音效 - 中頻的 popcat"""
        self.play_popcat_async(1200, 120)

    def play_dash(self):
        """播放衝刺音效 - 快速三連 Popcat"""
        frequencies = [1400, 1500, 1600]
        for i, freq in enumerate(frequencies):

            def play_delayed(frequency, delay):
                def delayed_play():
                    time.sleep(delay)
                    self.play_popcat_async(frequency, 60)

                threading.Thread(target=delayed_play, daemon=True).start()

            play_delayed(freq, i * 0.03)

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
            
            self.background_music_file = os.path.join(music_dir, "background_music.mp3")
            
            # 檢查是否已有音樂文件
            if not os.path.exists(self.background_music_file):
                print("🎵 正在下載背景音樂...")
                self.download_background_music()
            
            # 載入背景音樂
            if os.path.exists(self.background_music_file):
                pygame.mixer.music.load(self.background_music_file)
                pygame.mixer.music.set_volume(self.background_music_volume)
                print("🎵 背景音樂載入成功")
            else:
                print("⚠️ 背景音樂文件不存在")
                
        except Exception as e:
            print(f"⚠️ 背景音樂設置失敗: {e}")
            self.background_music_enabled = False

    def download_background_music(self):
        """下載背景音樂"""
        try:
            # 嘗試使用 yt-dlp 下載音樂
            command = [
                "yt-dlp",
                "--extract-audio",
                "--audio-format", "mp3",
                "--audio-quality", "192K",
                "-o", self.background_music_file.replace(".mp3", ".%(ext)s"),
                self.background_music_url
            ]
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✅ 背景音樂下載成功")
            else:
                print(f"⚠️ yt-dlp 下載失敗: {result.stderr}")
                # 創建一個備用的靜音文件
                self.create_fallback_music()
                
        except subprocess.TimeoutExpired:
            print("⚠️ 下載超時，使用備用音樂")
            self.create_fallback_music()
        except FileNotFoundError:
            print("⚠️ 找不到 yt-dlp，請安裝: pip install yt-dlp")
            self.create_fallback_music()
        except Exception as e:
            print(f"⚠️ 下載背景音樂時發生錯誤: {e}")
            self.create_fallback_music()

    def create_fallback_music(self):
        """創建備用音樂（簡單的循環音效）"""
        try:
            # 生成一個簡單的背景音調
            import numpy as np
            
            sample_rate = 22050
            duration = 30  # 30秒循環
            frames = sample_rate * duration
            
            # 生成和諧的背景音
            t = np.linspace(0, duration, frames)
            
            # 使用多個諧波創建舒緩的背景音
            wave = (
                0.1 * np.sin(2 * np.pi * 220 * t) +  # A3
                0.08 * np.sin(2 * np.pi * 330 * t) +  # E4
                0.06 * np.sin(2 * np.pi * 440 * t) +  # A4
                0.04 * np.sin(2 * np.pi * 660 * t)    # E5
            )
            
            # 添加淡入淡出
            fade_samples = sample_rate // 2  # 0.5秒淡入淡出
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            
            wave[:fade_samples] *= fade_in
            wave[-fade_samples:] *= fade_out
            
            # 轉換為 16-bit 立體聲
            wave = (wave * 32767 * 0.3).astype(np.int16)
            stereo_wave = np.column_stack((wave, wave))
            
            # 保存為臨時音頻文件
            import tempfile
            import wave as wave_module
            
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                with wave_module.open(temp_file.name, 'wb') as wav_file:
                    wav_file.setnchannels(2)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(sample_rate)
                    wav_file.writeframes(stereo_wave.tobytes())
                
                # 複製到最終位置
                import shutil
                fallback_file = self.background_music_file.replace(".mp3", "_fallback.wav")
                shutil.copy2(temp_file.name, fallback_file)
                self.background_music_file = fallback_file
                
                print("🎵 已創建備用背景音樂")
                
        except Exception as e:
            print(f"⚠️ 創建備用音樂失敗: {e}")
            self.background_music_enabled = False

    def start_background_music(self):
        """開始播放背景音樂"""
        if not self.background_music_enabled or not self.enabled:
            return
            
        try:
            if self.background_music_file and os.path.exists(self.background_music_file):
                pygame.mixer.music.play(-1)  # -1 表示無限循環
                self.is_music_playing = True
                print("🎵 背景音樂開始播放")
            else:
                print("⚠️ 背景音樂文件不存在")
        except Exception as e:
            print(f"⚠️ 播放背景音樂失敗: {e}")

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
        if self.is_music_playing:
            self.stop_background_music()
        else:
            self.start_background_music()

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
