score = int(input("請輸入成績: "))  # 提示使用者輸入成績並轉為整數
if score >= 100:
    print("等第: S")  # 100分以上(含)為S
elif score <= 0:
    print("等第: noob")  # 0分以下(含)為noob
elif score >= 90:
    print("等第: A")  # 90分以上(含)為A
elif score >= 80:
    print("等第: B")  # 80分以上(含)為B
elif score >= 70:
    print("等第: C")  # 70分以上(含)為C
elif score >= 60:
    print("等第: D")  # 60分以上(含)為D
else:
    print("等第: F")  # 60分以下為F
