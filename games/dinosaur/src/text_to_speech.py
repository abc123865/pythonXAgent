#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文字轉語音模組 - 非同步版本
使用 Windows SAPI 或 pyttsx3 將文字轉換為語音
支援 async/await 非同步操作
"""

import asyncio
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import queue


class AsyncTextToSpeech:
    """非同步文字轉語音類別"""

    def __init__(self):
        """初始化語音合成系統"""
        self.is_available = False
        self.engine = None
        self.speaking = False
        self.speech_queue = queue.Queue()
        self.executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="TTS")
        self._stop_event = threading.Event()

        # 啟動背景語音處理線程
        self._worker_thread = threading.Thread(
            target=self._process_speech_queue, daemon=True, name="TTS-Worker"
        )
        self._worker_thread.start()

        # 嘗試初始化語音引擎
        self._init_engine()

    def _init_engine(self):
        """初始化語音引擎"""
        # 方法1: 嘗試使用 pyttsx3
        try:
            import pyttsx3

            self.engine = pyttsx3.init()

            # 設定語音參數
            voices = self.engine.getProperty("voices")
            # 嘗試找到中文語音
            for voice in voices:
                if (
                    "chinese" in voice.name.lower()
                    or "taiwan" in voice.name.lower()
                    or "zh" in voice.id.lower()
                ):
                    self.engine.setProperty("voice", voice.id)
                    break

            # 設定語音速度和音量
            self.engine.setProperty("rate", 200)  # 語音速度
            self.engine.setProperty("volume", 0.8)  # 音量

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
                if (
                    "chinese" in voice.GetDescription().lower()
                    or "taiwan" in voice.GetDescription().lower()
                ):
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

        if os.name == "nt":  # Windows
            self.engine = "system"
            self.is_available = True
            print("✅ 使用系統語音備案")
        else:
            print("❌ 無可用的語音合成引擎")

    async def speak_async(self, text, priority="normal"):
        """
        非同步朗讀文字

        Args:
            text (str): 要朗讀的文字
            priority (str): 優先級 ("high", "normal", "low")

        Returns:
            Future: 可等待的 Future 物件
        """
        if not self.is_available:
            return

        # 創建語音任務
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        # 將任務放入佇列
        speech_task = {"text": text, "priority": priority, "future": future}

        # 根據優先級決定放入位置
        if priority == "high":
            # 高優先級任務放在隊列前面
            temp_queue = queue.Queue()
            temp_queue.put(speech_task)
            while not self.speech_queue.empty():
                temp_queue.put(self.speech_queue.get())
            self.speech_queue = temp_queue
        else:
            self.speech_queue.put(speech_task)

        return future

    def speak(self, text, blocking=False, priority="normal"):
        """
        朗讀文字 (向後兼容方法)

        Args:
            text (str): 要朗讀的文字
            blocking (bool): 是否阻塞執行 (已棄用，建議使用 async 版本)
            priority (str): 優先級 ("high", "normal", "low")
        """
        if not self.is_available or self.speaking:
            return

        if blocking:
            # 同步執行（不建議使用）
            self._speak_text(text)
        else:
            # 使用 asyncio 非同步執行
            try:
                loop = asyncio.get_event_loop()
                loop.create_task(self.speak_async(text, priority))
            except RuntimeError:
                # 如果沒有事件循環，回退到線程模式
                thread = threading.Thread(
                    target=self._speak_text, args=(text,), daemon=True
                )
                thread.start()

    def _process_speech_queue(self):
        """背景處理語音佇列"""
        while not self._stop_event.is_set():
            try:
                # 等待語音任務
                speech_task = self.speech_queue.get(timeout=1.0)

                # 執行語音合成
                try:
                    self._speak_text(speech_task["text"])

                    # 標記任務完成
                    if not speech_task["future"].done():
                        speech_task["future"].set_result(True)

                except Exception as e:
                    # 標記任務失敗
                    if not speech_task["future"].done():
                        speech_task["future"].set_exception(e)

                # 標記佇列任務完成
                self.speech_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                print(f"⚠️ 語音佇列處理錯誤: {e}")

    def _speak_text(self, text):
        """實際執行語音合成"""
        try:
            self.speaking = True

            if hasattr(self.engine, "say"):  # pyttsx3
                self.engine.say(text)
                self.engine.runAndWait()

            elif hasattr(self.engine, "Speak"):  # Windows SAPI
                self.engine.Speak(text)

            elif self.engine == "system":  # 系統命令備案
                import os
                import tempfile
                import subprocess

                # 使用臨時檔案避免轉義問題
                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".txt", delete=False, encoding="utf-8"
                ) as f:
                    f.write(text)
                    temp_file = f.name

                # 使用 subprocess 避免阻塞，並且不等待完成
                try:
                    cmd = [
                        "powershell",
                        "-Command",
                        f"Add-Type -AssemblyName System.Speech; "
                        f"$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                        f"$text = Get-Content -Path '{temp_file}' -Encoding UTF8 -Raw; "
                        f"$synth.Speak($text);",
                    ]
                    # 使用 Popen 非阻塞執行
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        creationflags=(
                            subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
                        ),
                    )
                    # 不等待進程完成，讓它在背景運行

                except Exception as e:
                    print(f"⚠️ PowerShell 語音執行失敗: {e}")

                # 延遲清理臨時檔案
                def cleanup_temp_file():
                    import time

                    time.sleep(5)  # 等待5秒後清理
                    try:
                        os.unlink(temp_file)
                    except:
                        pass

                # 在背景線程中清理
                cleanup_thread = threading.Thread(target=cleanup_temp_file, daemon=True)
                cleanup_thread.start()

        except Exception as e:
            print(f"⚠️ 語音合成失敗: {e}")
        finally:
            self.speaking = False

    def stop(self):
        """停止語音播放"""
        try:
            # 清空佇列
            while not self.speech_queue.empty():
                try:
                    task = self.speech_queue.get_nowait()
                    if not task["future"].done():
                        task["future"].cancel()
                except queue.Empty:
                    break

            # 停止語音引擎
            if hasattr(self.engine, "stop"):  # pyttsx3
                self.engine.stop()
            elif hasattr(self.engine, "Pause"):  # Windows SAPI
                self.engine.Pause()
        except:
            pass
        self.speaking = False

    def shutdown(self):
        """關閉語音系統"""
        self._stop_event.set()
        self.stop()
        self.executor.shutdown(wait=True)

    def is_speaking(self):
        """檢查是否正在朗讀"""
        return self.speaking or not self.speech_queue.empty()


# 向後兼容的別名
TextToSpeech = AsyncTextToSpeech
