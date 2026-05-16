# Python 字典与集合示例
# 对应文章：1.9 字典与集合

# ==================== 字典创建 ====================
print("=== 字典创建 ===")
dict1 = {}                                      # 空字典
dict2 = dict()                                  # 空字典
dict3 = {"Alice": 25, "Bob": 30, "Charlie": 35} # 字面量

# 从键值对列表创建
dict4 = dict([("Alice", 25), ("Bob", 30)])

# 字典推导式
dict5 = {k: v for k, v in [("Alice", 25), ("Bob", 30)]}

# 从两个列表创建（zip + dict）
keys = ["Alice", "Bob"]
values = [25, 30]
dict6 = dict(zip(keys, values))

print(f"dict3 = {dict3}")
print(f"dict6 = {dict6}")

# ==================== 添加/修改/访问 ====================
print("\n=== 添加/修改/访问 ===")
scores = {"Alice": 95, "Bob": 87}

# 添加或修改（同一个语法！）
scores["Charlie"] = 92       # 添加
scores["Alice"] = 98         # 修改
print(f"修改后: {scores}")

# 访问
age = scores["Alice"]         # 直接访问（键不存在抛 KeyError）
val = scores.get("David", 0)  # 安全访问（不存在返回默认值 0）
val2 = scores.get("David")    # 不存在返回 None
print(f"Alice: {age}, David: {val}")

# ==================== 删除 ====================
print("\n=== 删除 ===")
scores = {"Alice": 95, "Bob": 87, "Charlie": 92}
del scores["Alice"]           # 删除指定键（键不存在抛 KeyError）
print(f"del: {scores}")

val = scores.pop("Bob")      # 删除并返回值
print(f"pop('Bob'): {val}, 剩余: {scores}")

val = scores.pop("David", 0)  # 安全删除（不存在返回默认值）
print(f"pop('David'): {val}")

# ==================== 判断和遍历 ====================
print("\n=== 判断和遍历 ===")
scores = {"Alice": 95, "Bob": 87, "Charlie": 92}
print(f"'Alice' in scores: {'Alice' in scores}")  # True（判断键！）
print(f"keys:    {list(scores.keys())}")
print(f"values:  {list(scores.values())}")
print(f"items:   {list(scores.items())}")

for key, value in scores.items():
    print(f"  {key}: {value}")

# ==================== 字典推导式 ====================
print("\n=== 字典推导式 ===")
# 过滤
passed = {k: v for k, v in scores.items() if v >= 90}
print(f"及格(>=90): {passed}")

# 反转键值
reversed_dict = {v: k for k, v in scores.items()}
print(f"反转: {reversed_dict}")

# ==================== 字典合并（Python 3.9+）====================
print("\n=== 字典合并 ===")
dict_a = {"x": 1, "y": 2}
dict_b = {"y": 3, "z": 4}
merged = dict_a | dict_b       # Python 3.9+ 合并运算符（后者覆盖前者）
print(f"dict_a | dict_b = {merged}")  # {'x': 1, 'y': 3, 'z': 4}

# 更新方式（Python 3.5+）
merged2 = {**dict_a, **dict_b}  # 解包合并
print(f"{{**a, **b}}   = {merged2}")

# ==================== 默认值处理 ====================
print("\n=== 默认值处理（5种方式）===")
from collections import defaultdict, Counter

# 方式1：get
val = scores.get("David", 0)

# 方式2：in 判断
if "David" not in scores:
    scores["David"] = 0

# 方式3：setdefault（键不存在时设置默认值）
scores.setdefault("Eve", 0)
print(f"setdefault: {scores}")

# 方式4：defaultdict（自动创建默认值）
word_count = defaultdict(int)   # 默认值为 0
for word in ["hello", "world", "hello", "python", "hello"]:
    word_count[word] += 1
print(f"defaultdict: {dict(word_count)}")

# 方式5：Counter（计数器）
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counter = Counter(words)
print(f"Counter: {counter}")
print(f"最常见的2个: {counter.most_common(2)}")

# ==================== 集合 ====================
print("\n=== 集合 ===")
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}
print(f"set1 = {set1}")
print(f"set2 = {set2}")

# 集合运算（用运算符！比 C# 的方法调用简洁）
print(f"并集:   {set1 | set2}")        # {1,2,3,4,5,6,7,8}
print(f"交集:   {set1 & set2}")        # {4,5}
print(f"差集:   {set1 - set2}")        # {1,2,3}
print(f"对称差: {set1 ^ set2}")        # {1,2,3,6,7,8}

# 判断
print(f"3 in set1:       {3 in set1}")       # True
print(f"set1 <= set2:    {set1 <= set2}")    # False（子集）
s = {4,5}
print(f"{{4,5}} <= set1:    {s <= set1}    # {{4,5}}.issubset(set1)")

# 去重（集合最常用的场景！）
lst = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique = list(set(lst))
print(f"去重: {lst} -> {unique}")

# 保持顺序的去重（Python 3.7+）
unique_ordered = list(dict.fromkeys(lst))
print(f"保序去重: {unique_ordered}")
