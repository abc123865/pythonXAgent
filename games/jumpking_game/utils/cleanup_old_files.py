#!/usr/bin/env python3
"""
Jump King 遊戲檔案清理腳本
將舊版本檔案移動到 backup 資料夾
"""
import os
import shutil
from pathlib import Path


def create_backup_and_clean():
    """創建備份並清理舊檔案"""
    base_dir = Path(__file__).parent.parent
    backup_dir = base_dir / "backup" / "jumpking_old"

    print("🧹 開始清理 Jump King 舊檔案...")
    print(f"📁 基礎目錄: {base_dir}")
    print(f"📁 備份目錄: {backup_dir}")

    # 創建備份目錄
    backup_dir.mkdir(parents=True, exist_ok=True)

    # 要移動的檔案和資料夾
    items_to_backup = [
        "jumpking",  # 舊的 jumpking 資料夾
        "jumpking_save.json",  # 根目錄的存檔檔案
        "__pycache__",  # 快取檔案
    ]

    moved_items = []

    for item_name in items_to_backup:
        item_path = base_dir / item_name
        if item_path.exists():
            backup_path = backup_dir / item_name

            try:
                if item_path.is_file():
                    # 移動檔案
                    shutil.move(str(item_path), str(backup_path))
                    moved_items.append(f"📄 {item_name}")
                elif item_path.is_dir():
                    # 移動資料夾
                    if backup_path.exists():
                        shutil.rmtree(backup_path)
                    shutil.move(str(item_path), str(backup_path))
                    moved_items.append(f"📁 {item_name}")

                print(f"✅ 已移動: {item_name} -> backup/jumpking_old/")

            except Exception as e:
                print(f"❌ 移動失敗 {item_name}: {e}")

    # 顯示結果
    if moved_items:
        print(f"\n🎉 成功清理 {len(moved_items)} 個項目:")
        for item in moved_items:
            print(f"   {item}")
    else:
        print("\n✨ 沒有找到需要清理的檔案")

    print(f"\n📍 清理完成！")
    print(f"📁 新版遊戲位置: {base_dir}/games/jumpking_game/")
    print(f"📁 舊版備份位置: {backup_dir}/")

    return len(moved_items)


if __name__ == "__main__":
    try:
        moved_count = create_backup_and_clean()
        print(f"\n🏁 程式結束，共處理 {moved_count} 個項目")
    except Exception as e:
        print(f"💥 程式執行錯誤: {e}")
        import traceback

        traceback.print_exc()
