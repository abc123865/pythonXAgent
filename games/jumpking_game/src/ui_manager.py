#!/usr/bin/env python3
"""
Jump King UI管理器
處理所有使用者介面的繪製和互動
"""
import pygame
import os
from game_config import *


class UIManager:
    def __init__(self):
        self.load_fonts()

    def load_fonts(self):
        """載入字體"""
        font_loaded = False
        for font_path in FONT_PATHS:
            try:
                self.font_large = pygame.font.Font(font_path, FONT_LARGE_SIZE)
                self.font_medium = pygame.font.Font(font_path, FONT_MEDIUM_SIZE)
                self.font_small = pygame.font.Font(font_path, FONT_SMALL_SIZE)
                font_loaded = True
                print(f"成功載入字體: {font_path}")
                break
            except:
                continue

        if not font_loaded:
            # 使用系統預設字體
            self.font_large = pygame.font.Font(None, FONT_LARGE_SIZE)
            self.font_medium = pygame.font.Font(None, FONT_MEDIUM_SIZE)
            self.font_small = pygame.font.Font(None, FONT_SMALL_SIZE)
            print("使用系統預設字體")

    def draw_menu(self, screen, menu_selection, unlocked_levels):
        """繪製主選單"""
        screen.fill(DARK_BLUE)

        # 標題
        title = self.font_large.render("Jump King - 十一關挑戰", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title, title_rect)

        # 副標題
        subtitle = self.font_medium.render("考驗你的耐心與技巧", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(subtitle, subtitle_rect)

        # 選單選項
        menu_options = ["開始遊戲", "繼續遊戲", "退出遊戲"]
        for i, option in enumerate(menu_options):
            color = YELLOW if i == menu_selection else WHITE
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 50))
            screen.blit(text, text_rect)

        # 進度資訊
        progress_text = f"已解鎖關卡: {unlocked_levels}/{TOTAL_LEVELS}"
        progress = self.font_small.render(progress_text, True, GREEN)
        progress_rect = progress.get_rect(center=(SCREEN_WIDTH // 2, 500))
        screen.blit(progress, progress_rect)

        # 操作說明
        controls = ["↑↓ 選擇", "Enter 確認", "ESC 退出", "F11 切換全屏"]
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, GRAY)
            screen.blit(text, (50, 500 + i * 25))

    def draw_level_select(
        self,
        screen,
        level_select_selection,
        unlocked_levels,
        level_stats,
        level_manager,
    ):
        """繪製關卡選擇畫面"""
        screen.fill(DARK_BLUE)

        # 標題
        title = self.font_large.render("選擇關卡", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        # 關卡選項
        start_x = 50
        start_y = 180
        cols = 6
        rows = 2

        for level in range(1, TOTAL_LEVELS + 1):
            row = (level - 1) // cols
            col = (level - 1) % cols
            x = start_x + col * 120
            y = start_y + row * 120

            # 判斷關卡狀態
            if level > unlocked_levels:
                color = GRAY
                text_color = BLACK
                status = "鎖定"
            elif level == 11:
                if str(level) in level_stats and level_stats[str(level)]["completed"]:
                    color = PURPLE
                    text_color = WHITE
                    deaths = level_stats[str(level)]["best_deaths"]
                    status = f"征服\n{deaths}死"
                else:
                    color = (128, 0, 128)
                    text_color = WHITE
                    deaths = level_stats.get(str(level), {}).get("deaths", 0)
                    status = f"挑戰\n{deaths}死"
            elif str(level) in level_stats and level_stats[str(level)]["completed"]:
                color = GREEN
                text_color = WHITE
                deaths = level_stats[str(level)]["best_deaths"]
                status = f"完成\n{deaths}死"
            else:
                color = ORANGE
                text_color = WHITE
                deaths = level_stats.get(str(level), {}).get("deaths", 0)
                status = f"進行中\n{deaths}死"

            # 選中的關卡
            if level == level_select_selection:
                pygame.draw.rect(screen, YELLOW, (x - 5, y - 5, 110, 90), 3)

            # 關卡方塊
            pygame.draw.rect(screen, color, (x, y, 100, 80))

            # 關卡編號
            level_text = self.font_medium.render(f"第{level}關", True, text_color)
            level_rect = level_text.get_rect(center=(x + 50, y + 20))
            screen.blit(level_text, level_rect)

            # 關卡名稱
            level_data = level_manager.get_level(level)
            if level_data:
                name_text = self.font_small.render(level_data["name"], True, text_color)
                name_rect = name_text.get_rect(center=(x + 50, y + 40))
                screen.blit(name_text, name_rect)

            # 狀態
            for i, line in enumerate(status.split("\n")):
                status_text = self.font_small.render(line, True, text_color)
                status_rect = status_text.get_rect(center=(x + 50, y + 55 + i * 12))
                screen.blit(status_text, status_rect)

        # 關卡詳情
        if 1 <= level_select_selection <= TOTAL_LEVELS:
            level_data = level_manager.get_level(level_select_selection)
            if level_data:
                detail_y = 450

                # 關卡名稱
                name = self.font_medium.render(
                    f"第{level_select_selection}關: {level_data['name']}", True, YELLOW
                )
                name_rect = name.get_rect(center=(SCREEN_WIDTH // 2, detail_y))
                screen.blit(name, name_rect)

                # 目標死亡次數
                target_text = f"挑戰目標: {level_data['target_deaths']}次死亡內完成"
                if level_select_selection == 11:
                    target_text = f"超級挑戰: {level_data['target_deaths']}次死亡內完成"
                target = self.font_small.render(target_text, True, WHITE)
                target_rect = target.get_rect(center=(SCREEN_WIDTH // 2, detail_y + 30))
                screen.blit(target, target_rect)

                # 第11關特殊警告
                if level_select_selection == 11:
                    warning_text = "⚠️ 注意：此關卡包含隨機掉落陷阱！"
                    warning = self.font_small.render(warning_text, True, RED)
                    warning_rect = warning.get_rect(
                        center=(SCREEN_WIDTH // 2, detail_y + 55)
                    )
                    screen.blit(warning, warning_rect)

        # 操作說明
        controls = ["← → 選擇關卡", "Enter 開始", "ESC 返回", "F11 切換全屏"]
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, GRAY)
            screen.blit(text, (50, 550 + i * 20))

    def draw_playing_ui(self, screen, current_level, level_data, player):
        """繪製遊戲中的UI"""
        # 關卡資訊
        level_text = f"第{current_level}關: {level_data['name']}"
        text = self.font_medium.render(level_text, True, YELLOW)
        screen.blit(text, (10, 10))

        # 死亡次數
        deaths_text = f"死亡次數: {player.death_count}"
        text = self.font_small.render(deaths_text, True, WHITE)
        screen.blit(text, (10, 45))

        # 目標
        target_text = f"目標: {level_data['target_deaths']}次內完成"
        color = GREEN if player.death_count <= level_data["target_deaths"] else RED
        text = self.font_small.render(target_text, True, color)
        screen.blit(text, (10, 70))

        # 高度
        height = max(0, int((level_data["start_pos"][1] - player.y) / 10))
        height_text = f"高度: {height}m"
        text = self.font_small.render(height_text, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - 150, 10))

        # 控制說明
        controls = [
            "按住 SPACE 蓄力",
            "蓄力時按 ← → 選方向",
            "放開 SPACE 跳躍",
            "R 重置位置",
            "ESC 返回選單",
            "F11 切換全屏",
            "撞牆會反彈！",
        ]

        # 第11關特殊說明
        if current_level == 11:
            controls.extend(["⚠️ 小心！某些區域", "高速墜落會觸發", "掉落陷阱！"])

        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, WHITE)
            screen.blit(text, (10, SCREEN_HEIGHT - 140 + i * 20))

        # 玩家狀態
        status_text = f"在地面: {'是' if player.on_ground else '否'}"
        color = GREEN if player.on_ground else RED
        text = self.font_small.render(status_text, True, color)
        screen.blit(text, (SCREEN_WIDTH - 150, 35))

        # 蓄力狀態
        if player.jump_charging:
            charge_text = f"蓄力: {player.jump_power:.1f}"
            text = self.font_small.render(charge_text, True, YELLOW)
            screen.blit(text, (SCREEN_WIDTH - 150, 60))

    def draw_victory(self, screen, current_level, level_data, player):
        """繪製勝利畫面"""
        screen.fill(DARK_BLUE)

        # 勝利訊息
        title = self.font_large.render("恭喜過關！", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(title, title_rect)

        # 統計資料
        if level_data:
            deaths = player.death_count
            target = level_data["target_deaths"]

            stats_text = f"第{current_level}關: {level_data['name']}"
            text = self.font_medium.render(stats_text, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 280))
            screen.blit(text, text_rect)

            deaths_text = f"死亡次數: {deaths}"
            color = GREEN if deaths <= target else RED
            text = self.font_medium.render(deaths_text, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 320))
            screen.blit(text, text_rect)

            target_text = f"目標: {target}次"
            text = self.font_medium.render(target_text, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 360))
            screen.blit(text, text_rect)

            if deaths <= target:
                perfect_text = "挑戰成功！"
                text = self.font_medium.render(perfect_text, True, GREEN)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 400))
                screen.blit(text, text_rect)

        # 操作說明
        if current_level < TOTAL_LEVELS:
            continue_text = "Enter 繼續下一關"
        else:
            continue_text = "你已完成所有關卡！"

        text = self.font_small.render(continue_text, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 480))
        screen.blit(text, text_rect)

        back_text = "ESC 返回主選單"
        text = self.font_small.render(back_text, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 510))
        screen.blit(text, text_rect)

        # F11全屏快捷鍵說明
        fullscreen_text = "F11 切換全屏"
        text = self.font_small.render(fullscreen_text, True, GRAY)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 540))
        screen.blit(text, text_rect)
