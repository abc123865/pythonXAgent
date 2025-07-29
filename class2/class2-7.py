# try except    # 例外處理結構 (Exception Handling Structure)
# 錯誤處理 (Error Handling)
try:  # 嘗試執行可能出錯的程式碼 (Code to try)
    n = int(
        input("請輸入一個整數: ")
    )  # ← 讀取使用者輸入並轉換為整數 (Read user input and convert to integer)
except:  # 捕捉到錯誤時執行的程式碼 (Code to execute when an error is caught)
    print("輸入錯誤，請輸入一個整數")  # ← 輸出錯誤訊息 (Output error message)
    # 提醒使用者必須輸入一個整數 (Remind user to input an integer)


# 函數定義 (Function Definition)
# 新增一個函數要用 def 開頭, 後面接著函數名稱, 再加上小括號, 最後加上冒號
# (To define a function, start with def, followed by the function name, parentheses, and a colon)
def hello():  # 定義一個不帶整數的函數 (Define a function without parameters)
    print("Hello, World!")  # 輸出Hello, World! (Output Hello, World!)


for i in range(5):  # 使用for迴圈重複執行5次 (Use for loop to repeat 5 times)
    hello()  # 呼叫函數 (Call the function)


# 有傳入參數的函數 (Function with Parameters)
# 這個函數有一個參數 name , 當呼叫這個函數時, 可以傳入一筆資料給 name
# (This function has a parameter name, which can receive data when called)
def hello(name):  # 定義帶有參數的函數(Define a function with parameters)
    print(f"Hello, {name}!")  # 輸出Hello, [name]! (Output Hello, [name]!)


hello("Alice")  # 傳入Alice作為參數 (Call the function with a parameter)
hello("Bob")  # 傳入Bob作為參數 (Call the function with another parameter)
hello("Charlie")  # 傳入Charlie作為參數 (Call the function with a third parameter)


# 有回傳值的函數 (Function with Return Value)
# 這個函數會回傳一個值, 當呼叫這個函數時, 可以把回傳的值存起來
# (This function returns a value, which can be stored when called)
# 在指令當中只要執行return, 就會回傳這個值, 並結束函數
# (In the command, just execute return to return this value and end the function)
def add(a, b):  # 可以允許多個傳入參數 (This function can accept multiple parameters)
    return a + b  # 回傳兩數相加的結果 (Return the result of adding two numbers)


print(add(1, 2))  # 呼叫函數並輸出1+2的結果 (Call the function and print the result)
print(add("Hello, ", "World!"))  # 呼叫函數並輸出字串連接的結果
# (Call the function and print the result of string concatenation)
sum = add(3, 4)  # 呼叫函數並將結果存入變數sum
# (Call the function and store the result in variable sum)
print(sum)  # 輸出sum的值 (Print the value of sum)


# 有多個回傳值的函數 (Function with Multiple Return Values)
# 這個函數會回傳兩個值, 當呼叫這個函數時, 可以把回傳的值存起來
# (This function returns two values, which can be stored when called)
def add_sub(
    a, b
):  # 定義同時回傳兩個值的函數 (Define a function that returns two values)
    return (
        a + b,
        a - b,
    )  # 回傳兩數相加和相減的結果 (Return the result of adding and subtracting two numbers)


# 預設參數 ( Default Parameters)
# 可以在函數的參數中設定預設值, 當呼叫這個函數時, 如果沒有提供對應的參數,當呼叫這個函數時
# (If no corresponding parameter is provided when calling this function)
# 多個參數時, 有預設值的參數要放在沒有預設值的參數後面
# (When there are multiple parameters, parameters with default values must be placed after those without default values)
def hello(name, message="Hello!"):
    # message 參數有預設值 (The message parameter has a default value)
    print(f"{message}, {name}!")  # 輸出自訂訊息 (Output custom message)


hello("Alice")  # 呼叫函數, 使用預設訊息 (Call the function with default message)
hello("Bob", "Hi")  # 呼叫函數, 使用自訂訊息 (Call the function with custom message)


# 建議傳入函數型態 (Recommended to pass function types)
# 可以在函數的參數中設定型態, 當呼叫這個函數時, 可以提醒使用者要傳入的參數型態
# (You can set the type in the function parameters to remind users of the expected parameter types when calling this function)
# 變數: 型態 = 預設值 (Variable: Type = Default Value)
# 型態 , 代表回傳值的型態( type, indicates the return value type)
def add(a: int, b: int = 0) -> int:
    # 限定參數與回傳值的型態 (Restrict the types of parameters and return values)
    return a + b  # 回傳加法結果 (Return the result of addition)


print(add(1, 2))  # 呼叫函數並輸出1+2的結果 (Call the function and print the result)
print(
    add("Hello, ", "World!")
)  # 呼叫函數並輸出字串連接的結果 (Call the function and print the result of string concatenation)
# 這行不會報錯 但會輸出字串相加的結果
# (This line will not raise an error, but will output the result of string concatenation)

# def 區域變數與全域變數 (Function Local and Global Variables)
length = 5  # 定義全域變數 (Define a global variable)


def calculate_square_area():  # 計算正方形面積的函數 (Function to calculate square area)
    area = length**2
    # length 是全域變數 (length is a global variable), area 是區域變數 (area is a local variable)
    # length = length + 1  # 這行會出錯
    # 因為在函數內部length是區域變數, 不能直接修改全域變數
    # (This line will raise an error)
    print("正方形的面積是:", area)  # 輸出正方形的面積 (Output the area of the square)


calculate_square_area()  # 呼叫函數 (Call the function)
# print("長度是:", area) # 這行會出錯, 因為area是區域變數
# (This line will raise an error, because area is a local variable)

length = 5  # 全域變數


def calculate_square_area():
    area = length**2
    # length 是全域變數 (length is a global variable), area 是區域變數 (area is a local variable)
    print("正方形的面積是:", area)  # 輸出正方形的面積 (Output the area of the square)


length = 10  # 全域變數 (Modify the global variable)
calculate_square_area()  # 面積是100
# 因為要等到函數被呼叫時才會執行, 所以area的值是在函數被呼叫時才會計算
# (Because the execution occurs only when the function is called, the value of area is calculated at that time)

length = 5  # 全域變數 (Global variable)
area = 100  # 全域變數 (Global variable)


def calculate_square_area():
    area = length**2  # 計算正方形的面積 (Calculate the area of the square)
    # length是全域變數, area是區域變數 (length is a global variable, area is a local variable)
    print("正方形的面積是:", area)  # 輸出正方形的面積 (Output the area of the square)


length = 10  # 全域變數 (Global variable, modify the global variable)
calculate_square_area()  # 面積是100 (area is 100)
# 因為要等到函數被呼叫時才會執行, 所以area的值是在函數被呼叫時才會計算
# (Because the execution occurs only when the function is called, the value of area is calculated at that time)

length = 5  # 全域變數 (Global variable)
area = 100  # 全域變數 (Global variable)


def calculate_square_area():
    area = length**2  # 計算正方形的面積 (Calculate the area of the square)
    # length是全域變數, area是區域變數 (length is a global variable, area is a local variable)


calculate_square_area()  # 呼叫函數 (Call the function)
print("正方形的面積是:", area)  # 輸出正方形的面積 (Output the area of the square)
# 這時候指令內部的area是區域變數, 不會影響全域變數
# (At this point, the area inside the command is a local variable and does not affect the global variable)


calculate_square_area()  # 呼叫函數 (Call the function)
print("正方形的面積是:", area)  # 輸出正方形的面積 (Output the area of the square)
# 因為area是區域變數, 所以不會影響全域變數
# (Because area is a local variable, it does not affect the global variable)

length = 5  # 全域變數 (Global variable)
area = 100  # 全域變數 (Global variable)


def calculate_square_area() -> int:  # 回傳面積的函數 (Function to return the area)
    area = length**2
    # length是全域變數, area是區域變數 (length is a global variable, area is a local variable)
    return area  # 回傳面積


area = calculate_square_area()
# 呼叫函數並將結果存入area (Call the function and store the result in area)
print("正方形的面積是:", area)  # 輸出正方形的面積 (Output the area of the square)

length = 5  # 全域變數 (Global variable)
area = 100  # 全域變數 (Global variable)


def calculate_square_area():  # 修改面積的函數 (Function to return the area)
    global area  # 使用global關鍵字來修改全域變數 (Use the global keyword to modify the global variable)
    area = length**2  # 計算正方形的面積 (Calculate the area of the square)
    # length是全域變數, area是區域變數 (length is a global variable, area is a local variable)


calculate_square_area()  # 呼叫函數 (Call the function)
print("正方形的面積是:", area)  # 輸出正方形的面積 (Output the area of the square)


def hello(name: str):
    # 函數傳入參數都是區域變數 (Function parameters are local variables)
    """
    指令說明區(Documentation Area)\n
    這個函數會輸出一個問候訊息\n
    (This function will output a greeting message)\n
    參數: (Parameters:)\n
    name: str - 姓名 (name)\n

    回傳: None (Returns: None)\n
    Returns: None\n

    範例:\n
    hello("Alice") #Hello, Alice! \n(Example: hello("Alice") # Hello, Alice!)\n
    Example: hello("Alice") # Hello, Alice!\n
    """
    print(f"Hello, {name}!")  # 輸出問候訊息 (Output greeting message)
