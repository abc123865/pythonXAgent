# 水果店價格查詢系統 (Fruit Shop Price Inquiry System)
# 使用Dictionary來儲存水果名稱和價格 (Use Dictionary to store fruit names and prices)

# 初始化水果價格字典 (Initialize fruit price dictionary)
fruits = {"蘋果": 25, "香蕉": 20, "橘子": 30}  # ← Dictionary建立: 使用{}建立字典


def add_fruit(fruits):
    print("==========================")
    fruit_name = input("請輸入要新增的水果名稱: ")
    print(f"(Please enter the name of the fruit to add: {fruit_name})")
    if fruit_name in fruits:
        print(f"{fruit_name}已存在，請使用修改功能")
        print(f"({fruit_name} already exists, please use modify function)")
    else:
        price = int(input(f"請輸入{fruit_name}的價格: "))
        print(f"(Please enter the price of {fruit_name}: {price})")
        fruits[fruit_name] = price
        print(f"{fruit_name}已新增，價格 {price}元")
        print(f"({fruit_name} has been added, price {price}元)")
    print("==========================")


def modify_fruit(fruits):
    print("==========================")
    print("可修改的水果:", list(fruits.keys()))
    fruit_name = input("請輸入要修改的水果名稱: ")
    print(f"(Please enter the name of the fruit to modify: {fruit_name})")
    if fruit_name in fruits:
        print(f"目前{fruit_name}的價格: {fruits[fruit_name]}元")
        new_price = int(input(f"請輸入{fruit_name}的新價格: "))
        print(f"(Please enter the new price for {fruit_name}: {new_price})")
        fruits[fruit_name] = new_price
        print(f"{fruit_name}價格已修改為 {new_price}元")
        print(f"({fruit_name} price has been changed to {new_price}元)")
    else:
        print(f"{fruit_name}不存在")
        print(f"({fruit_name} does not exist)")
    print("==========================")


def delete_fruit(fruits):
    print("==========================")
    print("可刪除的水果:", list(fruits.keys()))
    fruit_name = input("請輸入要刪除的水果名稱: ")
    print(f"(Please enter the name of the fruit to delete: {fruit_name})")
    if fruit_name in fruits:
        deleted_price = fruits.pop(fruit_name)
        print(f"{fruit_name}已刪除，原價格為 {deleted_price}元")
        print(f"({fruit_name} has been deleted, original price was {deleted_price}元)")
    else:
        print(f"{fruit_name}不存在")
        print(f"({fruit_name} does not exist)")
    print("==========================")


def search_fruit(fruits):
    print("==========================")
    fruit_name = input("請輸入要查詢的水果名稱: ")
    if fruit_name in fruits:
        print(f"{fruit_name}的價格: {fruits[fruit_name]}元")
    else:
        print(f"{fruit_name}不存在於系統中")
    print("==========================")


def show_statistics(fruits):
    print("==========================")
    if fruits:
        prices = list(fruits.values())
        print(f"水果種類數量: {len(fruits)}")
        print(f"最高價格: {max(prices)}元")
        print(f"最低價格: {min(prices)}元")
        print(f"平均價格: {sum(prices) / len(prices):.1f}元")
        print(f"總價值: {sum(prices)}元")
    else:
        print("目前沒有水果資料")
    print("==========================")


print("=== 水果店價格查詢系統 ===")

while True:
    # 顯示目前所有水果價格 (Display current fruit prices)
    print("\n目前水果價格：")
    print("(Current fruit prices:)")

    # 使用字典的各種方法來顯示資料
    print("所有水果名稱:", list(fruits.keys()))  # ← Dictionary方法: keys()取得所有key
    print("所有價格:", list(fruits.values()))  # ← Dictionary方法: values()取得所有value
    print("水果總數:", len(fruits))  # ← Dictionary方法: len()取得字典大小

    # 使用items()來取得key-value對 (Use items() to get key-value pairs)
    for fruit, price in fruits.items():  # ← Dictionary方法: items()取得key-value對
        print(f"{fruit}: {price}元")
    print()

    # 顯示選單 (Show menu)
    print("1. 新增水果價格 (Add fruit price)")
    print("2. 修改水果價格 (Modify fruit price)")
    print("3. 刪除水果 (Delete fruit)")
    print("4. 查詢特定水果 (Search specific fruit)")
    print("5. 顯示價格統計 (Show price statistics)")
    print("6. 離開系統 (Exit system)")

    choice = input("請選擇功能 (1-6): ")

    if choice == "1":
        add_fruit(fruits)
    elif choice == "2":
        modify_fruit(fruits)
    elif choice == "3":
        delete_fruit(fruits)
    elif choice == "4":
        search_fruit(fruits)
    elif choice == "5":
        show_statistics(fruits)
    elif choice == "6":
        print("感謝使用水果店價格查詢系統！")
        print("(Thank you for using the Fruit Shop Price Inquiry System!)")
        break
    elif choice == "6":
        print("感謝使用水果店價格查詢系統！")
        print("(Thank you for using the Fruit Shop Price Inquiry System!)")
        break  # 跳出迴圈，結束程式
    else:
        print("請輸入有效的選項 (1-6)")
        print("(Please enter a valid option (1-6))")
        print(f"最低價格: {min(price)}元")
        print(f"平均價格: {sum(price) / len(price):.1f}元")
        print(f"總價值: {sum(price)}元")
