# 背景音樂設置指南

## 系統說明

遊戲現在支援背景音樂功能！當玩家開始遊戲時會自動播放背景音樂，當玩家失敗時會停止播放。

## 支援的音樂格式

遊戲支援以下音樂格式：

- **MP3** (推薦)
- **WAV**
- **OGG**

## 音樂檔案命名規則

將音樂檔案放在 `sound/` 資料夾中，使用以下任一檔名：

- `background.mp3` / `background.wav` / `background.ogg`
- `bgm.mp3` / `bgm.wav`
- `music.mp3`

## 從 YouTube 下載音樂的方法

### 方法一：使用 yt-dlp（推薦）

1. **安裝 yt-dlp**：

   ```powershell
   pip install yt-dlp
   ```

2. **下載音樂**：

   ```powershell
   # 下載為 MP3 格式
   yt-dlp -x --audio-format mp3 "你的YouTube網址"

   # 例如：
   yt-dlp -x --audio-format mp3 "https://www.youtube.com/watch?v=你的影片ID"
   ```

3. **重命名檔案**：
   將下載的檔案重命名為 `background.mp3` 並放入 `sound/` 資料夾

### 方法二：使用線上轉換工具

1. 訪問線上 YouTube 轉 MP3 網站（如 y2mate.com, savefrom.net 等）
2. 貼上 YouTube 網址
3. 選擇 MP3 格式下載
4. 將檔案重命名為 `background.mp3` 並放入 `sound/` 資料夾

### 方法三：使用 FFmpeg（進階用戶）

如果你已經有影片檔案，可以使用 FFmpeg 轉換：

```powershell
ffmpeg -i input_video.mp4 -q:a 0 -map a background.mp3
```

## 音樂控制功能

遊戲提供以下背景音樂控制功能：

- **自動播放**：開始遊戲時自動播放
- **失敗停止**：玩家失敗時自動停止
- **音量控制**：可以通過遊戲設定調整音量
- **開關控制**：可以完全關閉背景音樂

## 注意事項

1. **檔案大小**：建議音樂檔案不要超過 50MB，以確保遊戲載入速度
2. **音量平衡**：建議使用適中音量的音樂，避免干擾遊戲音效
3. **版權問題**：請確保使用的音樂符合版權規定
4. **格式相容性**：如果 MP3 格式有問題，可以嘗試 WAV 格式

## 故障排除

### 音樂無法播放

1. 確認檔案格式是否支援（MP3/WAV/OGG）
2. 確認檔案名稱是否正確
3. 確認檔案是否放在 `sound/` 資料夾中
4. 檢查檔案是否損壞

### 音樂音量問題

1. 在遊戲中調整音量設定
2. 使用音訊編輯軟體調整檔案音量
3. 確認系統音量設定

## 範例設置步驟

1. **下載音樂**：

   ```powershell
   yt-dlp -x --audio-format mp3 "https://www.youtube.com/watch?v=你的影片ID"
   ```

2. **移動檔案**：

   ```powershell
   # 重命名並移動到正確位置
   move "下載的檔案名.mp3" "sound/background.mp3"
   ```

3. **測試遊戲**：
   執行遊戲並開始新關卡，應該會聽到背景音樂播放

## 技術細節

遊戲使用 `pygame.mixer.music` 模組來處理背景音樂：

- 支援循環播放
- 與遊戲狀態整合
- 獨立於音效系統的音量控制
- 格式自動檢測和載入

現在你可以享受有背景音樂的 Jump King 遊戲體驗了！
