#!/usr/bin/env python3
"""
完整測試遊戲失敗機制
包含音效播放和畫面顯示
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from jumpking import Game, GAME_OVER
import pygame


def test_complete_gameover():
    """測試完整的遊戲失敗機制"""
    print("=== 完整遊戲失敗機制測試 ===")

    # 初始化遊戲
    game = Game()

    # 模擬開始遊戲
    game.start_level(1)

    print("遊戲已開始，模擬失敗情況...")
    print("控制說明：")
    print("SPACE - 觸發遊戲失敗")
    print("R - 重新開始")
    print("ESC - 退出測試")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    print("觸發遊戲失敗...")
                    game.game_over()
                elif event.key == pygame.K_r and game.state == GAME_OVER:
                    print("重新開始遊戲...")
                    game.restart_current_level()

            # 傳遞事件給遊戲處理
            game.handle_event(event)

        # 更新遊戲狀態
        game.update()

        # 繪製遊戲
        game.draw()

        # 顯示當前狀態
        if game.state == GAME_OVER:
            # 在控制台顯示狀態
            pass

        clock.tick(60)

    game.quit()
    print("測試完成")


if __name__ == "__main__":
    test_complete_gameover()
