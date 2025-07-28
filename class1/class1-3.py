# 比較運算子, 只能同樣類型作比較 (Comparison operators)
print(1 == 1)  # 等於運算, 印出True
# Equality operation, prints True
print(1 != 2)  # 不等於運算, 印出True
# Inequality operation, prints True
print(1 < 2)  # 小於運算, 印出True
# Less than operation, prints True
print(1 > 2)  # 大於運算, 印出False
# Greater than operation, prints False
print(1 <= 1)  # 小於等於運算, 印出True
# Less than or equal to operation, prints True
print(1 >= 2)  # 大於等於運算, 印出False
# Greater than or equal to operation, prints False

# 邏輯運算子 (Logical operators)
# and 運算子, 兩邊都為True才為True, 只要有一個為False就為False
# and operator, both sides must be True for the result to be True, if either side is False, the result is False
print(True and True)  # 印出True
print(True and False)  # 印出False
print(False and True)  # 印出False
print(False and False)  # 印出False

# or 運算子, 只要有一邊為True就為True, 兩邊都為False才為False
# or operator, if either side is True, the result is True, only if both sides are False is the result False
print(True or True)  # 印出True
print(True or False)  # 印出True
print(False or True)  # 印出True
print(False or False)  # 印出False

# not 運算子, 將True變為False, False變為True
# not operator, converts True to False and False to True
print(not True)  # 印出False
print(not False)  # 印出True

# 優先順序 (Order of operations)
# 1. () 括號 (Parentheses)
# 2. ** 指數運算 (Exponentiation)
# 3. *, /, //, % 乘除運算 (Multiplication, Division, Floor Division, and Modulus)
# 4. +, - 加減運算 (Addition and Subtraction)
# 5. ==, !=, <, >, <=, >= 比較運算 (Comparison)
# 6. not (not operator)
# 7. and (and operator)
# 8. or (or operator)

# 密碼門檢查 (Password strength check)
password = input(
    "請輸入密碼: "
)  # 提示使用者輸入密碼 (Prompt the user to enter a password)
if password == "0604":
    print("歡迎習包子")  # 密碼正確,歡迎習包子 (Correct password, welcome Xi Jinping)
elif password == "0911":
    print("歡迎飛機們")  # 密碼正確,歡迎川普 (Correct password, welcome Donald Trump)
elif password == "0921":
    print(
        "歡迎地震來"
    )  # 密碼正確,歡迎小熊維尼 (Correct password, welcome Winnie the Pooh)
else:
    print("密碼錯誤")  # 密碼錯誤 (Incorrect password)
# 連續使用if跟elif的差別在於:
# if是獨立判斷, 而elif是依賴於前面的條件
# The difference between using if and elif is that:
# if is an independent condition, while elif depends on the previous condition
