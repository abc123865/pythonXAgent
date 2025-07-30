# sort : 將list中的元素進行排序, 預設是從小到大排序(升序)
# (sort : sort the elements of the list in ascending order by default)
# 注意 : 這個方法會直接修改原始的list
# (Note : This method will modify the original list in place)
L = [1, 3, 2, 4, 5]
L.sort()
print(L)

# 從大到小(降序)
# (sort : sort the elements of the list in descending order)
L.sort(reverse=True)
print(L)

# 算術指定運算子 (Arithmetic Assignment Operators)
a = 1
a += 2  # 等同於 a = a + 2
print(a)
a -= 1  # 等同於 a = a - 1
print(a)
a *= 2  # 等同於 a = a * 2
print(a)
a /= 2  # 等同於 a = a / 2
print(a)
a //= 2  # 等同於 a = a // 2
print(a)
a %= 5  # 等同於 a = a % 5
print(a)
a **= 2  # 等同於 a = a ** 2
print(a)

# 優先順序 (Operator Precedence)
# 1. () 括號
# 2. ** 指數
# 3. * / 乘除
# 4. + - 加減
# 5. 比較運算子
# 6. not
# 7. and
# 8. or
# 9. 算術指定運算子

# while迴圈 (While Loop)
# while 會搭配一個條件式來使用 (while is used with a condition)
# 條件式為 True 時，會一直執行迴圈 (The loop will continue as long as the condition is True)
# 條件式為 False 時，會跳出迴圈 (The loop will exit when the condition is False)
# 每次迴圈結束時，會重新檢查條件式 (The condition is checked again at the end of each loop)
i = 0
while i < 5:  # 當 i 小於 5 時，繼續執行迴圈 (Continue the loop while i is less than 5)
    print(i)
    i += 1  # 每次迴圈結束時，i 會加 1 (At the end of each loop, i will be incremented by 1)

# break 會立即跳出迴圈 (break will immediately exit the loop)
# 先判斷 break 屬於哪個迴圈 (Determine which loop the break belongs to)
# 然後跳出該迴圈 (Then exit that loop)
i = 0
while i < 5:
    print(i)

    for j in range(5):
        print(j)

    if i == 3:
        break  # 跳出屬於while的迴圈 (Then exit that loop)
    i += 1

for i in range(5):
    print(i)
    if i == 3:
        break  # 跳出屬於for的迴圈 (Then exit that loop)
