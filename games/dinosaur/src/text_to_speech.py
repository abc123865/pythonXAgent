#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文字轉語音模組
使用 Windows SAPI 或 pyttsx3 將文字轉換為語音
"""

import threading
import time

class TextToSpeech:
    """文字轉語音類別"""
    
    def __init__(self):
        """初始化語音合成系統"""
        self.is_available = False
        self.engine = None
        self.speaking = False
        
        # 嘗試初始化語音引擎
        self._init_engine()
    
    def _init_engine(self):
        """初始化語音引擎"""
        # 方法1: 嘗試使用 pyttsx3
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            
            # 設定語音參數
            voices = self.engine.getProperty('voices')
            # 嘗試找到中文語音
            for voice in voices:
                if 'chinese' in voice.name.lower() or 'taiwan' in voice.name.lower() or 'zh' in voice.id.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            
            # 設定語音速度和音量
            self.engine.setProperty('rate', 200)  # 語音速度
            self.engine.setProperty('volume', 0.8)  # 音量
            
            self.is_available = True
            print("✅ pyttsx3 語音引擎初始化成功")
            return
            
        except ImportError:
            print("⚠️ pyttsx3 未安裝，嘗試備用方案")
        except Exception as e:
            print(f"⚠️ pyttsx3 初始化失敗: {e}")
        
        # 方法2: 嘗試使用 Windows SAPI
        try:
            import win32com.client
            self.engine = win32com.client.Dispatch("SAPI.SpVoice")
            
            # 嘗試設定中文語音
            voices = self.engine.GetVoices()
            for i in range(voices.Count):
                voice = voices.Item(i)
                if 'chinese' in voice.GetDescription().lower() or 'taiwan' in voice.GetDescription().lower():
                    self.engine.Voice = voice
                    break
            
            self.is_available = True
            print("✅ Windows SAPI 語音引擎初始化成功")
            return
            
        except ImportError:
            print("⚠️ pywin32 未安裝，無法使用 Windows SAPI")
        except Exception as e:
            print(f"⚠️ Windows SAPI 初始化失敗: {e}")
        
        # 方法3: 最後備案 - 使用系統命令
        import os
        if os.name == 'nt':  # Windows
            self.engine = 'system'
            self.is_available = True
            print("✅ 使用系統語音備案")
        else:
            print("❌ 無可用的語音合成引擎")
    
    def speak(self, text, blocking=False):
        """
        朗讀文字
        
        Args:
            text (str): 要朗讀的文字
            blocking (bool): 是否阻塞執行
        """
        if not self.is_available or self.speaking:
            return
        
        if blocking:
            self._speak_text(text)
        else:
            # 非阻塞模式，在新線程中執行
            thread = threading.Thread(target=self._speak_text, args=(text,), daemon=True)
            thread.start()
    
    def _speak_text(self, text):
        """實際執行語音合成"""
        try:
            self.speaking = True
            
            if hasattr(self.engine, 'say'):  # pyttsx3
                self.engine.say(text)
                self.engine.runAndWait()
                
            elif hasattr(self.engine, 'Speak'):  # Windows SAPI
                self.engine.Speak(text)
                
            elif self.engine == 'system':  # 系統命令備案
                import os
                import tempfile
                
                # 使用臨時檔案避免轉義問題
                with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                    f.write(text)
                    temp_file = f.name
                
                # 使用 PowerShell 讀取檔案並朗讀
                cmd = f'powershell -Command "Add-Type -AssemblyName System.Speech; $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $text = Get-Content -Path \'{temp_file}\' -Encoding UTF8 -Raw; $synth.Speak($text);"'
                os.system(cmd)
                
                # 清理臨時檔案
                try:
                    os.unlink(temp_file)
                except:
                    pass
            
        except Exception as e:
            print(f"⚠️ 語音合成失敗: {e}")
        finally:
            self.speaking = False
    
    def stop(self):
        """停止語音播放"""
        try:
            if hasattr(self.engine, 'stop'):  # pyttsx3
                self.engine.stop()
            elif hasattr(self.engine, 'Pause'):  # Windows SAPI
                self.engine.Pause()
        except:
            pass
        self.speaking = False
    
    def is_speaking(self):
        """檢查是否正在朗讀"""
        return self.speaking


def speak_game_intro():
    """朗讀遊戲介紹"""
    tts = TextToSpeech()
    
    if not tts.is_available:
        print("❌ 語音功能不可用")
        return
    
    intro_text = """
    歡迎來到超級進階小恐龍遊戲！
    
    這是一個功能豐富的跳躍遊戲，包含四種難度等級：
    簡單模式適合新手，中等模式提供平衡挑戰，
    困難模式需要高度技巧，噩夢模式則是極限挑戰。
    
    遊戲特色包括：
    動態螢幕適應、進階障礙物系統、恐龍特殊技能、
    日夜反轉效果、以及專業的音效系統。
    
    操作很簡單：
    使用方向鍵或空白鍵跳躍，Z鍵啟動護盾，
    F11切換全螢幕，ESC返回選單。
    
    準備好挑戰了嗎？讓我們開始遊戲吧！
    """
    
    print("🔊 開始朗讀遊戲介紹...")
    tts.speak(intro_text.strip())


if __name__ == "__main__":
    # 測試語音功能
    speak_game_intro()
