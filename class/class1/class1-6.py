x = int(input("請輸入1~9的整數："))
if 1 <= x <= 9:
    for i in range(1, x + 1):
        print(str(i) * i)
else:
    print("輸入錯誤")
