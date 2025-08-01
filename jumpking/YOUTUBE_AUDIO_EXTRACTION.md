# YouTube 音頻提取指南

## 目標

從 YouTube 影片 https://www.youtube.com/watch?v=nJkhLNadub8 提取 18-37 秒音頻片段作為遊戲失敗音效。

## 方法一：使用 yt-dlp 和 ffmpeg

### 安裝工具

```bash
# 安裝 yt-dlp
pip install yt-dlp

# 安裝 ffmpeg（需要從官網下載）
# https://ffmpeg.org/download.html
```

### 提取音頻

```bash
# 1. 下載完整音頻
yt-dlp -x --audio-format mp3 "https://www.youtube.com/watch?v=nJkhLNadub8"

# 2. 剪輯指定時間段（18-37秒）
ffmpeg -i "下載的音頻文件名.mp3" -ss 00:00:18 -t 00:00:19 -c copy "sound/gameover.mp3"
```

## 方法二：使用線上工具

### 推薦網站

1. **Y2Mate**: https://y2mate.com/
2. **OnlineVideoConverter**: https://www.onlinevideoconverter.com/
3. **ClipConverter**: https://www.clipconverter.cc/

### 步驟

1. 複製 YouTube 網址：https://www.youtube.com/watch?v=nJkhLNadub8
2. 在線上工具中貼上網址
3. 選擇 MP3 格式
4. 下載音頻文件
5. 使用音頻編輯軟體（如 Audacity）剪輯 18-37 秒片段

## 方法三：使用 Audacity

### 下載和剪輯

1. 下載 Audacity：https://www.audacityteam.org/
2. 使用線上工具下載完整 MP3
3. 在 Audacity 中開啟音頻文件
4. 選擇 18-37 秒時間範圍
5. 匯出選取部分為 MP3 格式
6. 儲存為 `sound/gameover.mp3`

## 檔案放置位置

```
jumpking/
├── sound/
│   ├── jump.mp3          (跳躍音效)
│   ├── golfclap.mp3      (通關音效)
│   └── gameover.mp3      (失敗音效) ← 新增這個檔案
├── jumpking.py
└── ...
```

## 測試音效

完成音頻提取後，執行以下命令測試：

```bash
python test_gameover_sound.py
```

## 注意事項

1. 確保音頻文件格式為 MP3
2. 檔案名稱必須是 `gameover.mp3`
3. 音頻長度建議控制在 10-20 秒內
4. 音量適中，避免過大或過小

## 版權提醒

- 僅供個人學習和測試使用
- 請遵守 YouTube 服務條款和版權法律
- 商業使用請獲得相應授權
