print([])  # 這是一個空list
# Output: This is an empty list
print([1, 2, 3])  # 這是一個包含三個整數的list
# Output: This is a list containing three integers
print([1, 2, 3, a, b, c])  # 這是一個包含三個整數和三個變數, 六個元素的list
# Output: This is a list containing three integers and three variables, for a total of six elements
print([1, 2, 3, ["a", "b", "c"]])  # 這是一個包含三個整數和一個list, 四個元素的list
# Output: This is a list containing three integers and one list, for a total of four elements
print(
    [1, True, "a", 1.23]
)  # 這是一個包含一個整數、一個布林值、一個字串和一個浮點數的四個元素的list
# Output: This is a list containing one integer, one boolean, one string, and one float, for a total of four elements

# list 讀取元素時, 元素的index從0開始
# Example 5: Accessing elements in a list using indices
# 這是CRUD的R (This is the R in CRUD)
L = [1, 2, 3, "a", "b", "c"]
print(L[0])  # 輸出第一個元素 1
# Output: 1
print(L[1])  # 輸出第二個元素 2
# Output: 2
print(L[2])  # 輸出第三個元素 3
# Output: 3
print(L[3])  # 輸出第四個元素 "a"
# Output: a

# 切片
L = [1, 2, 3, "a", "b", "c"]
print(L[::2])
# 就是取index 0到最後, 每次取2個元素, 所以是[1, 3, "b"]
# (This is taking every second element starting from index 0, so it results in [1, 3, "b"])
print(L[1:4])
# 就是取index 1到3, 所以是[2, 3, "a"]
# (This is taking elements from index 1 to 3, resulting in [2, 3, "a"])
print(L[1:4:2])
# 就是取index 1到4, 不包含4, 每次取2個元素, 所以是[2, "a"]
# (This is taking elements from index 1 to 4, every second element, resulting in [2, "a"])
# 跟Range一樣, 切片的結尾不包含最後一個元素
# Just like with Range, the end index in slicing does not include the last element.

# list 取長度, 也就是list中有幾個元素, 不是index的最大值
# Example 6: Getting the length of a list
L = [1, 2, 3, "a", "b", "c"]
print(len(L))  # 輸出 6, 因為有六個元素
# Output: 6, because there are six elements in the list
# list 走訪元素
# Example 7: Iterating through a list
# 可以透過取得index來找到list中的資料
# You can find data in a list by accessing its index
L = [1, 2, 3, "a", "b", "c"]

for i in range(0, len(L)):
    print(L[i])  # 透過index取得資料
    # Output: 1, 2, 3, a, b, c

# 也可以直接把list當作一個範圍來取得資料
# You can also treat the list as a range to access data

for i in L:
    print(i)  # 直接使用list取得資料
    # Output: 1, 2, 3, a, b, c

# 這兩種方式都可以, 但是看使用的情景是否會需要index來決定要用哪一種方式
# Both methods can be used, but the choice depends on whether you need the index in your context

# list 修改元素
# Example 8: Modifying elements in a list
# 可以透過index來修改list中的元素
# You can modify elements in a list using their index
L = [1, 2, 3, "a", "b", "c"]
L[0] = 2  # 修改第一個元素為2
print(L)  # 輸出 [2, 2, 3, "a", "b", "c"]
# Output: [2, 2, 3, "a", "b", "c"]

# call by value (傳值呼叫)
a = 1
b = a  # b現在是1
b = 2  # 修改b, 但不影響a
print(a, b)  # 輸出 1 2
# Output: 1 2

# call by reference (傳址呼叫)
a = [1, 2, 3]  # a是一個list
b = a  # b現在指向同一個list
b[0] = 2  # 修改b的第一個元素, 也會影響到a
print(a, b)  # 輸出 [2, 2, 3] [2, 2, 3]
# Output: [2, 2, 3] [2, 2, 3]

a = [1, 2, 3]  # a是一個list
b = a.copy()  # b現在是a的副本, 不再指向同一個list
# (Copying a list creates a new list that is independent of the original
b[0] = 2  # 修改b的第一個元素, 不會影響到a
print(a, b)  # 輸出 [1, 2, 3] [2, 2, 3]
# Output: [1, 2, 3] [2, 2, 3]

# list的append(append to list)
L = [1, 2, 3]  # 初始化一個list
L.append(4)  # 在list的最後面添加一個元素4
print(L)  # 輸出 [1, 2, 3, 4]
# Output: [1, 2, 3, 4]

# list的移除方式有兩種(Two ways to remove elements from a list)
# 第一種是使用remove方法, 使用remove, 可以移除由左至右第一個指定的元素(很重要)
L = [1, 2, 3, 4]
L.remove(2)  # 移除元素2
# 代表移除由左至右第一個出現的2, 也就是index 1的元素
# (This means removing the first occurrence of 2 from left to right, which is the
# 如果想要移除所有的2, 可以使用迴圈

for i in L:
    if i == 2:
        L.remove(i)
print(L)  # 輸出 [1, 3, 4]
# Output: [1, 3, 4]

# 第二種是使用del關鍵字, 使用del, 可以移除指定index的元素
L = [1, 2, 3, 4, 1]
L.pop(0)  # 移除index 0的元素
# 代表pop方法會移除並返回指定index的元素, 如果不指定index, 預設是移除最後一個元素
print(L)  # 輸出 [2, 3, 4, 1]
# Output: [2, 3, 4, 1]
