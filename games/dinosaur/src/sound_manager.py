#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音效管理系統
處理遊戲中的所有音效播放
"""

import pygame
import threading
import time
import sys
from config.game_config import SoundSystem


class SoundManager:
    """音效管理器"""

    def __init__(self):
        """初始化音效系統"""
        self.enabled = SoundSystem.SOUND_ENABLED
        self.volume = SoundSystem.SOUND_VOLUME

        if self.enabled:
            try:
                # 初始化音效系統
                pygame.mixer.pre_init(
                    frequency=22050, size=-16, channels=2, buffer=1024
                )
                pygame.mixer.init()
                print("🔊 音效系統初始化成功")
            except pygame.error as e:
                print(f"⚠️ 音效系統初始化失敗: {e}")
                self.enabled = False
        else:
            print("🔇 音效系統已停用")

    def generate_simple_beep(self, frequency, duration):
        """
        生成簡單的嗶嗶聲（使用系統音效或簡單波形）

        Args:
            frequency (int): 頻率 (Hz)
            duration (int): 持續時間 (毫秒)
        """
        if not self.enabled:
            return

        # 使用異步線程播放音效，避免阻塞遊戲
        threading.Thread(
            target=self._play_system_beep, args=(frequency, duration), daemon=True
        ).start()

    def _play_system_beep(self, frequency, duration):
        """播放系統提示音"""
        try:
            # 在 Windows 系統上使用 winsound（如果可用）
            if sys.platform == "win32":
                try:
                    import winsound

                    # 使用系統預設提示音
                    winsound.MessageBeep(winsound.MB_OK)
                    return
                except ImportError:
                    pass

            # 如果 winsound 不可用，使用系統提示音的替代方案
            print("\a", end="", flush=True)  # ASCII 提示音

        except Exception as e:
            # 靜默處理錯誤，避免影響遊戲體驗
            pass

    def play_key_press(self):
        """播放一般按鍵音效"""
        self.generate_simple_beep(
            SoundSystem.KEY_PRESS_FREQUENCY, SoundSystem.KEY_PRESS_DURATION
        )

    def play_jump(self):
        """播放跳躍音效"""
        self.generate_simple_beep(SoundSystem.JUMP_FREQUENCY, SoundSystem.JUMP_DURATION)

    def play_dash(self):
        """播放衝刺音效"""
        self.generate_simple_beep(SoundSystem.DASH_FREQUENCY, SoundSystem.DASH_DURATION)

    def play_shield(self):
        """播放護盾音效"""
        self.generate_simple_beep(
            SoundSystem.SHIELD_FREQUENCY, SoundSystem.SHIELD_DURATION
        )

    def play_menu_move(self):
        """播放選單移動音效"""
        self.generate_simple_beep(
            SoundSystem.MENU_MOVE_FREQUENCY, SoundSystem.MENU_MOVE_DURATION
        )

    def play_menu_select(self):
        """播放選單選擇音效"""
        self.generate_simple_beep(
            SoundSystem.MENU_SELECT_FREQUENCY, SoundSystem.MENU_SELECT_DURATION
        )

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

    def cleanup(self):
        """清理音效系統"""
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
