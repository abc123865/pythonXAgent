# 恐龍遊戲 AI 編程指南

## 架構概覽

這是一個模組化的 Pygame 恐龍跳躍遊戲，採用清晰的 MVC 分離設計：

- **`main.py`**: 僅作為入口點，所有遊戲邏輯都在 `src/` 模組中
  - **`game_engine.py`**: 核心協調器，管理遊戲狀態、事件處理、渲染循環、日夜模式、螢幕效果
- **`dinosaur.py`**: 玩家角色，包含物理系統、技能系統、噩夢模式效果
- **`obstacles.py`**: 障礙物系統，支援 10+ 種類型（隱形、爆炸、移動等）
- **`menu_system.py`**: 選單界面，處理難度選擇和 UI 交互
- **`sound_manager.py`**: 實時音效系統，支援 Popcat 風格音效合成
- **`config/game_config.py`**: 集中式配置，包含所有常數、顏色、難度設定、音效參數

## 關鍵設計模式

### 1. 響應式螢幕適應

所有尺寸使用 `scale_factor` 動態計算：

```python
scale_factor = min(screen_width / 800, screen_height / 400)
self.width = int(40 * scale_factor)
```

修改 UI 元素時，始終使用螢幕比例而非固定像素值。

### 2. 中文支持與字體處理

專門處理 Windows 中文環境，字體載入有容錯機制：

```python
# 優先載入微軟正黑體，失敗時使用系統預設
self.font_large = pygame.font.Font(FONT_PATH, large_size)
```

所有中文字串都應正確編碼，UI 文字使用繁體中文。

### 3. 實時音效合成系統

`sound_manager.py` 使用 numpy 實現真正的 Popcat 音效合成，並支援背景音樂：

```python
def generate_popcat_sound(self, base_frequency, duration):
    # 快速攻擊階段 + 噪音模擬 "p" 音
    # 指數衰減階段 + 諧波豐富化
    # 生成立體聲 16-bit 音頻數據

def setup_background_music(self):
    # YouTube 音頻下載與播放
    # 自動備用音樂生成
    # 背景音樂循環播放
```

特點：

- 所有按鍵都有對應的音效頻率和時長
- 支援複合音效（如衝刺的三連音、死亡的五段下降音）
- 容錯機制：numpy 失敗時回退到簡化版，再失敗時使用系統音效
- 異步播放避免阻塞遊戲循環
- **YouTube 背景音樂**：自動下載指定 URL 的音頻作為背景音樂
- **智慧備用系統**：無法下載時自動生成和諧的合成背景音樂
- **音樂控制**：F2 鍵切換背景音樂開關，支援音量調節

### 4. 日夜循環與視覺適應

每 2000 分自動切換日夜模式，包含平滑的淡入淡出動畫：

```python
def update_day_night_transition(self):
    # 檢測週期變化並啟動轉換動畫
    # 使用 transition_progress (0-1) 控制轉換進度
    # 平滑的顏色插值實現淡入淡出效果

def lerp_color(self, color1, color2, t):
    # 線性插值混合兩個顏色
    # 用於背景、文字、UI元素的平滑轉換
```

特點：

- 平滑的背景顏色轉換，避免突兀的切換
- 文字顏色自動適應，確保在任何轉換階段都可見
- 轉換過程中的視覺提示（"🌙→ 轉入夜晚"）
- 不同難度有不同的日夜色調變化

### 5. 難度系統驅動

遊戲邏輯高度依賴 `DIFFICULTY_SETTINGS` 配置：

- 速度倍率、障礙物生成率、特效強度都由難度控制
- 新增功能時考慮不同難度的適配
- 噩夢模式 (`Difficulty.NIGHTMARE`) 有特殊的視覺和物理效果

### 6. 事件驅動的狀態管理

遊戲使用 `GameState` 枚舉管理狀態轉換：

- `MENU` → `PLAYING` → `GAME_OVER` → `MENU`
- 每個狀態有獨立的事件處理邏輯
- 全域快捷鍵（F11、Alt+F4）在所有狀態下生效

### 7. 距離計分系統

`ScoreSystem` 類處理基於距離的計分：

```python
# 每移動一定距離獲得分數，速度越快分數越高
distance_score = (distance_interval // DISTANCE_SCORE_INTERVAL) * base_score
speed_bonus = int(current_speed * speed_multiplier)
```

## 技術特殊性

### 音效合成架構

專業級 Popcat 音效生成，結合多層容錯機制和背景音樂系統：

1. **主要生成器**：numpy 版本

   - 雙階段波形設計（攻擊 + 衰減）
   - 諧波疊加讓聲音更豐富
   - 噪音注入模擬爆破音"p"

2. **簡化備案**：純數學版本

   - 不依賴 numpy，使用 Python array
   - 保持基本的波形包絡

3. **系統備案**：Windows API 音效

   - 完全失敗時的最後手段

4. **背景音樂系統**：
   - **YouTube 下載**：使用 yt-dlp 自動下載指定 URL 的音頻
   - **備用生成**：無法下載時自動生成和諧的合成背景音樂
   - **循環播放**：支援無限循環和音量控制
   - **動態控制**：F2 鍵實時切換開關

所有音效都異步播放，支援複合序列（如死亡時的五段下降音）。

### 物理系統

- 支援重力反轉（噩夢模式）：`is_gravity_reversed`
- 控制反轉機制：跳躍和蹲下鍵位互換
- 二段跳系統：空中可執行第二次跳躍

### 動態視覺效果

**日夜循環系統**：

- 每 2000 分進行一次日夜顛倒
- 平滑的淡入淡出轉換動畫（`transition_progress`）
- 線性插值顏色混合（`lerp_color`）
- 文字和 UI 元素的動態顏色適應
- 轉換過程中的視覺回饋提示

**噩夢模式特效**：

- 5 秒間隔的螢幕閃爍：`screen_flicker_timer`
- 隨機強度的白色覆蓋效果
- 重力反轉和控制反轉

### 障礙物擴展

在 `obstacles.py` 中新增障礙物類型，需要實作：

- `setup_obstacle()`: 設定尺寸、顏色、位置
- `can_walk_through()` / `can_duck_under()`: 定義互動規則
- `update()`: 特殊行為邏輯（移動、隱形、爆炸等）

### 螢幕震動和視覺效果

使用 `screen_shake` 變數實作螢幕震動：

```python
screen_offset_x = random.randint(-self.screen_shake, self.screen_shake)
```

所有繪製都考慮偏移量，創造動態視覺回饋。

### 計分系統架構

`ScoreSystem` 類統一處理各種計分邏輯：

```python
class ScoreSystem:
    def update_distance_score(self, speed):
        # 基於移動距離的主要計分
        # 速度越快獲得越多分數

    def add_obstacle_score(self, obstacle_type):
        # 不同障礙物有不同分數獎勵
```

## 開發工作流程

### 執行和測試

```bash
# 在專案根目錄執行
python main.py

# 確保已安裝依賴
pip install pygame
```

### 偵錯策略

- 遊戲引擎會輸出詳細的狀態變化 log
- 使用 F11 測試全螢幕適應性
- 不同難度測試各種功能組合

### 配置修改

所有遊戲參數集中在 `config/game_config.py`：

- 修改顏色：編輯 `get_color_palette()`
- 調整難度：修改 `DIFFICULTY_SETTINGS`
- 物理常數：更新 `Physics` 類

## 程式碼約定

- 使用繁體中文註釋和變數名稱
- 類別方法包含完整的 docstring
- 所有魔術數字都定義為常數
- 錯誤處理要考慮 Windows 環境特殊性（字體路徑、編碼等）
- 新功能必須支援動態螢幕縮放

## 新功能開發指南

### 音效系統擴展

新增音效時，在 `sound_manager.py` 中：

1. 在 `SoundSystem` 類新增頻率和時長常數
2. 實作對應的播放方法
3. 考慮複合音效（如連續播放多個頻率）
4. 所有音效都使用異步播放

### 視覺效果開發

新增視覺效果時注意：

1. 使用 `scale_factor` 確保螢幕適應性
2. 考慮日夜模式的顏色適配
3. 噩夢模式的特殊處理
4. 效果應該支援開關控制

### 遊戲機制擴展

新增遊戲機制時：

1. 在 `game_config.py` 中定義相關常數
2. 考慮不同難度的適配
3. 確保與現有系統的兼容性
4. 添加適當的音效回饋

這個專案的獨特之處在於完整的中文本地化、複雜的難度漸進系統，以及對 Windows 環境的特殊優化。最新的音效合成系統和視覺效果系統讓遊戲體驗更加豐富和專業。
