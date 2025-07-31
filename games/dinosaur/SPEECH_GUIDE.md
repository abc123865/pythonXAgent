# 🎤 語音功能安裝指南

## 快速啟用語音播報

### 方法一：安裝 pyttsx3（推薦）
```bash
pip install pyttsx3
```

### 方法二：安裝 Windows Speech API 支援
```bash
pip install pywin32
```

### 方法三：系統內建語音（已自動啟用）
- Windows 10/11 會自動使用 PowerShell 語音合成
- 無需額外安裝，但可能有轉義問題

## 語音功能說明

遊戲啟動時會自動播放遊戲介紹語音，包括：
- 遊戲特色說明
- 操作指南
- 難度介紹
- 歡迎訊息

## 疑難排解

### 如果語音播放失敗：
1. 確認系統音量已開啟
2. 檢查 Windows 語音設定
3. 安裝推薦的 pyttsx3 套件

### 語音相關檔案：
- `src/text_to_speech.py` - 完整語音模組
- `src/simple_speech.py` - 簡化語音模組
- `assets/speech/` - 語音檔案存放目錄（自動建立）

## 自訂語音內容

您可以修改 `main.py` 中的 `speak_intro()` 函數來自訂語音內容。
