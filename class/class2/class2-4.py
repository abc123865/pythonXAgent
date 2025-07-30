import random

# 設定初始範圍和目標數字
min_range = 0
max_range = 100
target = random.randint(min_range, max_range)

print(f"請輸入{min_range}~{max_range}的整數:", end="")
guess = int(input())

while guess != target:
    if guess < min_range or guess > max_range:
        print("你超出範圍了!")
        print(f"請輸入{min_range}~{max_range}的整數:", end="")
        guess = int(input())
        continue

    if guess > target:
        print("再小一點")
        max_range = guess  # 更新上限
    else:
        print("再大一點")
        min_range = guess  # 更新下限

    print(f"請輸入{min_range}~{max_range}的整數:", end="")
    guess = int(input())

print("恭喜猜中!")
print("Congratulations, you guessed it!")
