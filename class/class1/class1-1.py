# 請將以下所有的程式註解都翻譯成中英版本

# 這是在終端機印出hello的訊息
print("hello")
"""
這是多行註解
This is a multi-line comment
可以在裡面寫很多想要記錄下來的事情
You can write many things you want to document here
這些註解不會被程式執行
These comments will not be executed by the program
"""

# 這是單行註解
# This is a single-line comment
# 單行註解通常用來解釋程式碼的某一行或某一段
# Single-line comments are usually used to explain a specific line or section of code

# 單行註解可以用 ctrl + / 來快速添加或移除
# Single-line comments can be quickly added or removed using ctrl + /

# 基本型態 (Basic data types)
print(1)  # int這是整數
# int, this is an integer
print(1.0)  # float這是浮點數
# float, this is a floating-point number
print(1.234)  # float這是浮點數
# float, this is a floating-point number
print(apple)  # str 這是字串
# str, this is a string
print(True)  # bool 這是布林值
# bool, this is a boolean value
print(False)  # bool 這是布林值
# bool, this is a boolean value

# 變數 (Variables)
a = 10  # 新增一個儲存空間並取名為a, "="的功能是將右邊的值10賦值給左邊的a
# Create a new storage space named 'a', the '=' operator assigns the value 10 on the right to 'a' on the left
print(a)  # 在終端機顯示a所存的值
# Display the value stored in 'a' in the terminal
a = "apple"  # 將字串"apple"賦值給變數a
# Assign the string "apple" to the variable 'a'
print(a)  # 在終端機顯示a所存的字串
# Display the string stored in 'a' in the terminal

# 運算子 (Operators)
print(1 + 2)  # 加法運算, 印出3
# Addition operation, prints 3
print(5 - 3)  # 減法運算, 印出2
# Subtraction operation, prints 2
print(2 * 3)  # 乘法運算, 印出6
# Multiplication operation, prints 6
print(6 / 2)  # 除法運算, 印出3.0
# Division operation, prints 3.0
print(5 % 2)  # 取餘數運算, 印出1
# Modulus operation, prints 1
print(2**3)  # 指數運算, 印出8
# Exponentiation operation, prints 8
print(5 // 2)  # 取商運算, 印出2
# Floor division operation, prints 2

# 優先順序 (Order of operations)
# 1. () (Parentheses)
# 2. ** (Exponentiation)
# 3. *, /, //, % (Multiplication, Division, Floor Division, and Modulus)
# 4. +, - (Addition and Subtraction)

# 字串運算 (String operations)
print("hello" + " world")  # 字串連接, 印出"hello world"
# String concatenation, prints "hello world"
print("hello" * 3)  # 字串乘法, 印出"hellohellohello"
# String multiplication, prints "hellohellohello"
print("hello" + str(123))  # 將整數轉為字串後連接, 印出"hello123"
# Convert integer to string and concatenate, prints "hello123"
print("hello" * 3)  # 字串重複, 印出"hellohellohello"
# String repetition, prints "hellohellohello"

# 字串格式化 (String formatting)
name = "Alice"  # 定義一個字串變數name
age = 30  # 定義一個整數變數age
# ex 如果直接放進去會錯誤,因為age是整數, 不能與字串相加
# For example, if we directly concatenate, it will cause an error because 'age' is an integer and cannot be added to a string
print("My name is " + name + " and I am " + age + "years old.")  # 這樣會錯誤
# This will cause an error
# 將變數轉為字串後連接, 印出"My name is Alice and I am 30 years old."
# Concatenate variables after converting them to strings, prints "My name is Alice and I am 30 years old."
print(f"My name is {name} and I am {age} years old.")
# My name is Alice and I am 30 years old.
# 使用f-string格式化字串, 印出"My name is Alice and I am 30 years old."
# Using f-string to format the string, prints "My name is Alice and I am 30 years old."

# len() 函數用來取得字串、串列等物件的長度
# The len() function is used to get the length of a string, list, or other objects
print(len("apple"))  # 印出字串長度, 這裡是5
# Print the length of the string, which is 5 here
print(len(","))  # 印出字串長度, 這裡是1
# Print the length of the string, which is 1 here
# type() 函數用來取得物件的類型
# The type() function is used to get the type of an object
print(type(1))  # 印出整數的類型, 這裡是<class 'int'>
# Print the type of the integer, which is <class 'int'>
print(type(1.0))  # 印出浮點數的類型, 這裡是<class 'float'>
# Print the type of the floating-point number, which is <class 'float'>
print(type("apple"))  # 印出字串的類型, 這裡是<class 'str'>
# Print the type of the string, which is <class 'str'>
print(type(True))  # 印出布林值的類型, 這裡是<class 'bool'>
# Print the type of the boolean value, which is <class 'bool'>

# 型態轉換 (Type conversion)
print(int("123"))  # 將字串轉為整數, 印出123
# Convert string to integer, prints 123
print(float("123.45"))  # 將字串轉為浮點數, 印出123.45
# Convert string to floating-point number, prints 123.45
print(str(123))  # 將整數轉為字串, 印出"123"
# Convert integer to string, prints "123"
print(str(123.45))  # 將浮點數轉為字串, 印出"123.45"
# Convert floating-point number to string, prints "123.45"
print(bool(1))  # 將整數轉為布林值, 印出True
# Convert integer to boolean, prints True
print(bool(0))  # 將整數轉為布林值, 印出False
# Convert integer to boolean, prints False

print("輸入開始")  # 開始輸入 (Start input)
# input() 函數用來取得使用者輸入
# The input() function is used to get user input
a = input("請輸入數字: ")  # 提示使用者輸入內容 (Prompt the user to enter something)
print(int(a) + 10)  # 顯示使用者輸入的內容 (Display the content entered by the user)
print(type(a))  # 證明透過input()取得的內容是字串
# Prove that the content obtained through input() is a string
