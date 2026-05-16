# Python 列表操作示例
# 对应文章：1.8 列表与数组

# ==================== 列表创建 ====================
print("=== 列表创建 ===")
lst1 = [1, 2, 3]
lst2 = list([1, 2, 3])
lst3 = list()  # 空列表
lst4 = []      # 空列表（更常用）

# 初始化
lst5 = [0] * 5       # [0, 0, 0, 0, 0]
lst6 = [None] * 3    # [None, None, None]
print(f"lst1 = {lst1}")
print(f"lst5 = {lst5}")

# ==================== 添加元素 ====================
print("\n=== 添加元素 ===")
lst = [1, 2, 3]
lst.append(6)          # 添加到末尾: [1, 2, 3, 6]
lst.insert(0, 0)       # 插入到指定位置: [0, 1, 2, 3, 6]
lst.extend([7, 8])     # 添加多个: [0, 1, 2, 3, 6, 7, 8]
print(f"操作后: {lst}")

# ==================== 删除元素 ====================
print("\n=== 删除元素 ===")
lst = [1, 2, 3, 2, 4]
lst.remove(2)          # 删除第一个匹配项: [1, 3, 2, 4]
print(f"remove(2): {lst}")

val = lst.pop()        # 删除并返回最后一个
print(f"pop(): {val}, 剩余: {lst}")

val = lst.pop(0)       # 删除并返回指定索引
print(f"pop(0): {val}, 剩余: {lst}")

del lst[0]             # 删除指定索引
print(f"del[0]:  剩余: {lst}")

# lst.clear()           # 清空列表

# ==================== 查找 ====================
print("\n=== 查找 ===")
lst = [10, 20, 30, 40, 50]
index = lst.index(30)   # 查找索引: 2
exists = 30 in lst      # 是否包含: True（运算符，不是方法！）
print(f"index(30) = {index}")
print(f"30 in lst = {exists}")

# ==================== 排序和反转 ====================
print("\n=== 排序和反转 ===")
lst = [3, 1, 4, 1, 5, 9, 2, 6]
sorted_lst = sorted(lst)  # 排序（返回新列表，不修改原列表）
print(f"原列表:    {lst}")
print(f"sorted():  {sorted_lst}")

lst.sort()              # 排序（原地修改）
print(f"sort()后:  {lst}")

lst.reverse()           # 反转（原地修改）
print(f"reverse(): {lst}")

# 按自定义规则排序
words = ["banana", "apple", "cherry"]
by_length = sorted(words, key=len)
print(f"按长度排序: {by_length}")

# ==================== 切片 ====================
print("\n=== 切片 ===")
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(f"原列表:  {lst}")
print(f"[1:4]:   {lst[1:4]}")      # [1, 2, 3]
print(f"[:5]:    {lst[:5]}")        # [0, 1, 2, 3, 4]
print(f"[::2]:   {lst[::2]}")       # [0, 2, 4, 6, 8]（每隔一个）
print(f"[::-1]:  {lst[::-1]}")      # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]（反转）

# ==================== 列表推导式 ====================
print("\n=== 列表推导式 ===")
numbers = [1, 2, 3, 4, 5]
squares = [x * x for x in numbers]                          # [1, 4, 9, 16, 25]
even = [x for x in numbers if x % 2 == 0]                  # [2, 4]
matrix = [[i * j for j in range(1, 4)] for i in range(1, 4)]  # 嵌套推导式
print(f"平方:  {squares}")
print(f"偶数:  {even}")
print(f"矩阵:  {matrix}")

# ==================== 内置函数 ====================
print("\n=== 内置聚合函数 ===")
numbers = [1, 2, 3, 4, 5]
print(f"sum:     {sum(numbers)}")      # 15
print(f"avg:     {sum(numbers) / len(numbers)}")  # 3.0
print(f"max:     {max(numbers)}")      # 5
print(f"min:     {min(numbers)}")      # 1
print(f"len:     {len(numbers)}")      # 5

# ==================== 浅拷贝 vs 深拷贝 ====================
print("\n=== 浅拷贝 vs 深拷贝 ===")
import copy

original = [[1, 2], [3, 4]]

# 浅拷贝：只复制一层
shallow = original.copy()  # 或 list(original) 或 original[:]
shallow[0][0] = 999
print(f"浅拷贝修改后 original: {original}")  # [[999, 2], [3, 4]]（被影响了！）

# 深拷贝：递归复制所有层
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0][0] = 999
print(f"深拷贝修改后 original: {original}")  # [[1, 2], [3, 4]]（不受影响！）

# ==================== 列表当栈使用 ====================
print("\n=== 列表当栈 ===")
stack = []
stack.append(1)    # push
stack.append(2)
stack.append(3)
print(f"入栈: {stack}")
val = stack.pop()  # pop（LIFO）
print(f"出栈: {val}, 栈: {stack}")

# 注意：列表当队列效率低！pop(0) 是 O(n)，用 collections.deque
from collections import deque
queue = deque([1, 2, 3])
queue.append(4)     # 入队
val = queue.popleft()  # 出队（O(1)）
print(f"队列出队: {val}, 队列: {queue}")
