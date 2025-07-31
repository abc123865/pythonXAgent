#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡化版語音合成 - 生成 WAV 檔案並播放
避免 PowerShell 轉義問題
"""

import os
import pygame

def create_speech_audio():
    """創建遊戲介紹的語音檔案"""
    
    # 如果已經有語音檔案，直接返回
    audio_file = "assets/speech/game_intro.wav"
    if os.path.exists(audio_file):
        return audio_file
    
    # 創建目錄
    os.makedirs("assets/speech", exist_ok=True)
    
    # 嘗試使用 Windows SAPI 生成 WAV 檔案
    try:
        import win32com.client
        
        # 初始化語音引擎
        voice = win32com.client.Dispatch("SAPI.SpVoice")
        file_stream = win32com.client.Dispatch("SAPI.SpFileStream")
        
        # 設定輸出檔案
        file_stream.Open(audio_file, 3)
        voice.AudioOutputStream = file_stream
        
        # 語音內容
        text = """歡迎來到超級進階小恐龍遊戲！
        這是一個功能豐富的跳躍遊戲，包含四種難度等級。
        遊戲特色包括動態螢幕適應、進階障礙物系統、恐龍特殊技能等。
        操作很簡單：使用方向鍵或空白鍵跳躍，Z鍵啟動護盾。
        準備好挑戰了嗎？讓我們開始遊戲吧！"""
        
        # 生成語音
        voice.Speak(text)
        file_stream.Close()
        
        print(f"✅ 語音檔案已生成: {audio_file}")
        return audio_file
        
    except ImportError:
        print("⚠️ 無法使用 Windows SAPI 生成語音檔案")
        return None
    except Exception as e:
        print(f"⚠️ 生成語音檔案失敗: {e}")
        return None

def play_speech_audio():
    """播放遊戲介紹語音"""
    
    # 嘗試生成語音檔案
    audio_file = create_speech_audio()
    
    if not audio_file or not os.path.exists(audio_file):
        print("🔇 無法播放語音介紹")
        return
    
    try:
        # 使用 pygame 播放音效
        pygame.mixer.init()
        sound = pygame.mixer.Sound(audio_file)
        sound.play()
        print(f"🔊 正在播放語音介紹: {audio_file}")
        
    except Exception as e:
        print(f"⚠️ 播放語音失敗: {e}")

if __name__ == "__main__":
    play_speech_audio()
