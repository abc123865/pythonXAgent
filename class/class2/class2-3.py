# import random # 匯入 random 模組 (Import the random module)
import random as r

# random.randrange() 設定抽籤範圍的方式跟range()一樣( random.randrange() sets the range for the lottery in the same way as range()
print(r.randrange(10))  # 產生 0 到 9 的隨機整數 (Generate a random integer from 0 to 9)
print(
    r.randrange(1, 10)
)  # 產生 1 到 9 的隨機整數 (Generate a random integer from 1 to 9)
print(
    r.randrange(1, 10, 2)
)  # 產生 1 到 9 的隨機奇數 (Generate a random odd integer from 1 to 9)

# random.randint() 產生指定範圍內的隨機整數 (Generate a random integer within a specified range)
# 結束的數字是包含在內的 (The ending number is included)
print(
    r.randint(1, 10)
)  # 產生 1 到 10 的隨機整數 (Generate a random integer from 1 to 10)
