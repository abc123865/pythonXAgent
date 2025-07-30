# 恐龍遊戲 AI 編程指南

## 架構概覽

這是一個模組化的 Pygame 恐龍跳躍遊戲，採用清晰的 MVC 分離設計：

- **`main.py`**: 僅作為入口點，所有遊戲邏輯都在 `src/` 模組中
- **`game_engine.py`**: 核心協調器，管理遊戲狀態、事件處理、渲染循環
- **`dinosaur.py`**: 玩家角色，包含物理系統、技能系統、噩夢模式效果
- **`obstacles.py`**: 障礙物系統，支援 10+ 種類型（隱形、爆炸、移動等）
- **`menu_system.py`**: 選單界面，處理難度選擇和 UI 交互
- **`config/game_config.py`**: 集中式配置，包含所有常數、顏色、難度設定

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

### 3. 難度系統驅動

遊戲邏輯高度依賴 `DIFFICULTY_SETTINGS` 配置：

- 速度倍率、障礙物生成率、特效強度都由難度控制
- 新增功能時考慮不同難度的適配
- 噩夢模式 (`Difficulty.NIGHTMARE`) 有特殊的視覺和物理效果

### 4. 事件驅動的狀態管理

遊戲使用 `GameState` 枚舉管理狀態轉換：

- `MENU` → `PLAYING` → `GAME_OVER` → `MENU`
- 每個狀態有獨立的事件處理邏輯
- 全域快捷鍵（F11、Alt+F4）在所有狀態下生效

## 技術特殊性

### 物理系統

- 支援重力反轉（噩夢模式）：`is_gravity_reversed`
- 控制反轉機制：跳躍和蹲下鍵位互換
- 二段跳系統：空中可執行第二次跳躍

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

這個專案的獨特之處在於完整的中文本地化、複雜的難度漸進系統，以及對 Windows 環境的特殊優化。
