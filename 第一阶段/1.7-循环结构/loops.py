# Python 循环结构示例
# 对应文章：1.7 循环结构

# ==================== for-in 循环 ====================
print("=== for-in 循环 ===")
# Python 只有一种 for 循环（for-in），不像 C# 有 for、foreach、do-while
for i in range(5):
    print(i, end=" ")  # 0 1 2 3 4
print()

# range() 的三种用法
print(f"range(5):       {list(range(5))}")        # [0, 1, 2, 3, 4]
print(f"range(2, 5):    {list(range(2, 5))}")     # [2, 3, 4]
print(f"range(0, 10, 2): {list(range(0, 10, 2))}")  # [0, 2, 4, 6, 8]

# ==================== 遍历列表 ====================
print("\n=== 遍历列表 ===")
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    print(num, end=" ")
print()

# 倒序遍历
print("倒序:", end=" ")
for num in reversed(numbers):
    print(num, end=" ")  # 5 4 3 2 1
print()

# ==================== 带索引的遍历 ====================
print("\n=== 带索引遍历 ===")
# Python 用 enumerate()，C# 的 foreach 自带 index
for i, num in enumerate(numbers):
    print(f"  [{i}] = {num}")
# 也可以指定起始索引
for i, num in enumerate(numbers, start=1):
    print(f"  第{i}个: {num}")

# ==================== zip() 并行遍历 ====================
print("\n=== zip() 并行遍历 ===")
names = ["Alice", "Bob", "Charlie"]
scores = [95, 87, 92]
for name, score in zip(names, scores):
    print(f"  {name}: {score}")
# C# 对比：C# 的 Zip() 方法或 LINQ 的 Zip()

# ==================== while 循环 ====================
print("\n=== while 循环 ===")
i = 0
while i < 5:
    print(i, end=" ")
    i += 1
print()

# Python 没有 do-while，但可以模拟
print("模拟 do-while:", end=" ")
i = 0
while True:
    print(i, end=" ")
    i += 1
    if i >= 5:
        break  # 先执行一次，再判断

# ==================== break 和 continue ====================
print("\n\n=== break 和 continue ===")
print("跳过 5，到 10 停止:", end=" ")
for k in range(20):
    if k == 5: continue  # 跳过 5
    if k == 10: break    # 遇到 10 停止
    print(k, end=" ")    # 0 1 2 3 4 6 7 8 9
print()

# ==================== for-else（Python 独有！） ====================
print("\n=== for-else ===")
# 规则：循环正常结束（没有 break）才执行 else
# 适合搜索场景：找到就 break，没找到就执行 else

# 场景1：找到了，else 不执行
search_list = [1, 3, 5, 7, 9, 11]
target = 7
for item in search_list:
    if item == target:
        print(f"找到了 {target}")
        break
else:
    print(f"没找到 {target}")
# 输出：找到了 7

# 场景2：没找到，else 执行
target = 6
for item in search_list:
    if item == target:
        print(f"找到了 {target}")
        break
else:
    print(f"没找到 {target}")
# 输出：没找到 6

# ==================== 遍历字典 ====================
print("\n=== 遍历字典 ===")
person = {"name": "Alice", "age": 25, "city": "Beijing"}
for key, value in person.items():
    print(f"  {key}: {value}")
