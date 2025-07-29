# 字典 (Dictionary)
# dict是透過key-value對來儲存資料的資料結構, Key是唯一的, Value可以是任何資料型別
# ( A dict is a collection of key-value pairs, where each key is unique and maps to a value. )
# dict是無序的 所以無法用index來存取資料
# ( A dict is unordered, so you cannot access its elements by index. )
# dict的key必須是不可變的資料型態 例如 : int, float, string
# ( The keys in a dict must be of an immutable data type. )
# dict的value可以是任何資料型態
# ( The values in a dict can be of any data type. )
# dict的value-key是透過冒號來連接
# ( The key-value pairs in a dict are connected by colons. )
# dict的value-key是透過逗號來分隔
# ( The key-value pairs in a dict are separated by commas. )
d = {"a": 1, "b": 2, "c": 3}  # 建立一個字典 (Create a dictionary)

# 取得dict的key ( Get the keys of a dict )
print(d.keys())  # dict_keys(['a', 'b', 'c'])    #印出所有的key( Print all keys )
for key in d.keys():  # 迴圈印出所有的key ( Loop through all keys )
    print(key)  # 印出每個key ( Print each key )

# 取得dict的value ( Get the values of a dict )
print(d.values())  # dict_values([1, 2, 3])    #印出所有的value( Print all values )
for value in d.values():  # 迴圈印出所有的value ( Loop through all values )
    print(value)  # 印出每個value ( Print each value )

# 取得dict的key-value對 ( Get the key-value pairs of a dict )
print(
    d.items()
)  # dict_items([('a', 1), ('b', 2), ('c', 3)])    #印出所有的key-value對( Print all key-value pairs )
for (
    key,
    value,
) in d.items():  # 迴圈印出所有的key-value對 ( Loop through all key-value pairs )
    print(key, value)  # 印出每個key-value對 ( Print each key-value pair )

# 新增或更新dict的key-value對 ( Add or update key-value pairs in a dict )
d["d"] = 4  # 新增key-value對 ( Add a new key-value pair )
print(
    d
)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}  # 印出更新後的dict ( Print the updated dict )
d["a"] = 10  # 更新key-value對 ( Update an existing key-value pair )
print(
    d
)  # {'a': 10, 'b': 2, 'c': 3, 'd': 4}  # 印出更新後的dict ( Print the updated dict )

# 刪除dict的key-value對, pop()方法 ( Delete key-value pairs from a dict using the pop() method )
# 如果資料存在, 就刪除並回傳value( If the key exists, it deletes and returns the value)
print(d.pop("b"))  # 2  # 刪除key為'b'的key-value對並回傳value
# ( Delete the key-value pair with key 'b' and return its value )
# 如果不存在, 就回傳預設值 (if not, it returns a default value )
print(d.pop("e", "Not Found"))  # Not Found  # 刪除key為'e'的key-value對並回傳預設值
# ( Delete the key-value pair with key 'e' and return the default value )
# 如果資料不存在也沒有預設值, 就會報錯(KeyError)

# 檢查dict是否存在某個key ( Check if a key exists in the dict )
# in不能檢查dict的value ( in cannot check the values of a dict )
# 跟list一樣, 可以用in來檢查key是否存在 ( Similar to a list, you can use 'in' to check if a key exists )
print("a" in d)  # True  # 檢查key 'a'是否存在 ( Check if key 'a' exists )
print("b" in d)  # False  # 檢查key 'b'是否存在 ( Check if key 'b' exists )

# 比較複雜的dict ( Comparing complex dicts )
d = {"a": [1, 2, 3], "b": {"c": 3, "d": 4}}
# value也可以是list或dict ( The value can also be a list or a dict )
print(d["a"])  # [1, 2, 3] #取得key "a"的value ( Get the value of key "a" )
print(
    d["a"][0]
)  # 1 #取得key "a"的第一個元素 ( Get the first element of the value of key "a" )
print(d["b"])  # {'c': 3, 'd': 4} #取得key "b"的value ( Get the value of key "b" )
print(
    d["b"]["c"]
)  # 3 #取得key "b"的key "c"的value ( Get the value of key "c" in the value of key "b" )

# 成績登記系統 ( Grade statistics ), key是學生名字, value是成績
grade = {
    "小明": {"國文": [90, 80, 70], "數學": [90, 85, 80], "英文": [95, 90, 85]},
    "小華": {"國文": [80, 85, 75], "數學": [85, 80, 75], "英文": [90, 85, 80]},
    "小美": {"國文": [75, 80, 70], "數學": [80, 75, 70], "英文": [85, 80, 75]},
}

# 取得小明的數學成績
print(grade["小明"]["數學"])
# [90, 85, 80]  # 取得小明的數學成績 ( Get the math grades of 小明 )
# 取得小美的第一次英文成績
print(grade["小美"]["英文"][0])
# 85  # 取得小美的第一次英文成績 ( Get the first English grade of 小美 )
# 取得小華的第二次國文成績
print(grade["小華"]["國文"][1])
# 85  # 取得小華的第二次國文成績 ( Get the second Chinese grade of 小華 )

# 印出所有學生的國文段考成績平均值 ( Print the average Chinese grades of all students )
for name, scores in grade.items():
    # 逐一取得每位同學的科目成績
    # 取得國文成績
    chinese_scores = scores["國文"]  # 取得國文成績
    avg = sum(chinese_scores) / len(chinese_scores) if chinese_scores else 0
    print(f"{name}的國文成績平均值: {avg}")  # 印出平均成績
