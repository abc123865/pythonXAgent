# 購物小幫手 Shopping Assistant
# 使用 list 來儲存購物清單
shopping_list = []

print("🛒 歡迎使用購物小幫手！")
print("🛒 Welcome to Shopping Assistant!")

# 使用 while 迴圈來持續顯示選單
while True:
    # 顯示目前的購物清單
    print("\n📋 目前購物清單 Current Shopping List:")
    if len(shopping_list) == 0:
        print("   清單是空的 The list is empty")
    else:
        i = 0
        while i < len(shopping_list):
            print("   " + str(i + 1) + ". " + shopping_list[i])
            i += 1

    # 顯示選單
    print("\n📋 你可以做這些事 You can do these things:")
    print("1️⃣ 新增東西 Add items")
    print("2️⃣ 修改東西 Modify items")
    print("3️⃣ 刪除東西 Delete items")
    print("4️⃣ 離開程式 Exit the program")

    # 取得使用者選擇
    choice = input("\n請選擇 (1-4): ")

    # 選項 1: 新增東西
    if choice == "1":
        item = input("➕ 請輸入要新增的物品: ")
        shopping_list.append(item)  # 使用 append 加到清單最後
        print("✅ 已新增: " + item)

    # 選項 2: 修改東西
    elif choice == "2":
        if len(shopping_list) == 0:
            print("❌ 清單是空的，無法修改")
        else:
            index = int(
                input("✏️ 請輸入要修改的編號 (1-" + str(len(shopping_list)) + "): ")
            )
            if index >= 1 and index <= len(shopping_list):
                old_item = shopping_list[index - 1]
                new_item = input("請輸入新的物品名稱: ")
                shopping_list[index - 1] = new_item  # 直接修改 list 元素
                print("✅ 已將 '" + old_item + "' 修改為 '" + new_item + "'")
            else:
                print("❌ 編號超出範圍")

    # 選項 3: 刪除東西
    elif choice == "3":
        if len(shopping_list) == 0:
            print("❌ 清單是空的，無法刪除")
        else:
            print("選擇刪除方式:")
            print("1. 用名稱刪除")
            print("2. 用位置刪除")
            delete_choice = input("請選擇 (1-2): ")

            if delete_choice == "1":
                # 用名稱刪除 (remove)
                item_name = input("❌ 請輸入要刪除的物品名稱: ")
                if item_name in shopping_list:
                    shopping_list.remove(item_name)  # 使用 remove 方法
                    print("✅ 已刪除: " + item_name)
                else:
                    print("❌ 找不到該物品")

            elif delete_choice == "2":
                # 用位置刪除 (pop)
                index = int(
                    input("🗑️ 請輸入要刪除的位置 (1-" + str(len(shopping_list)) + "): ")
                )
                if index >= 1 and index <= len(shopping_list):
                    removed_item = shopping_list.pop(index - 1)  # 使用 pop 方法
                    print("✅ 已刪除位置 " + str(index) + " 的物品: " + removed_item)
                else:
                    print("❌ 位置超出範圍")
            else:
                print("❌ 無效的選擇")

    # 選項 4: 離開程式
    elif choice == "4":
        print("👋 謝謝使用購物小幫手，再見！")
        print("👋 Thank you for using Shopping Assistant, goodbye!")
        break  # 跳出 while 迴圈

    # 無效選擇
    else:
        print("❌ 無效的選擇，請重新輸入")
