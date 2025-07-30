# open() 開啟模式
# 'r' 讀取模式, 檔案必須存在
# 'w' 寫入模式, 檔案不存在則會建立新檔案
# 'a' 附加模式, 檔案不存在則會建立新檔案
# 'r+' 讀取與寫入模式, 檔案必須存在
# 'w+' 讀取與寫入模式, 檔案不存在則會建立新檔案
# 'a+' 讀取與附加模式, 檔案不存在則會建立新檔案

f = open("class1/class1-1", "r", encoding="utf-8")  # 開啟檔案
content = f.read()  # 讀取檔案內容
print(content)  # 印出內容
f.close()  # 關閉檔案
###########################################
with open("class1/class1-2", "w", encoding="utf-8") as f:  # 使用with語句開啟檔案
    content = f.read()  # 讀取檔案內容
    print(content)  # 印出內容
# 不用寫 f.close()，with語句會自動關閉檔案
