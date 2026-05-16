# ============================================================
# Python 列表推导式 vs C# LINQ
# 对应文章：2.3 列表推导式 vs LINQ
# ============================================================
# 一句话总结：Python 的列表推导式 ≈ C# 的 LINQ
# 但 Python 版更简洁，C# 版更类型安全。
# 你 LINQ 用得溜，Python 列表推导式就无师自通！
# ============================================================

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# ============================================================
# 1. 基础：筛选 + 转换
# ============================================================
# C# 对应：numbers.Where(x => x % 2 == 0)
evens = [x for x in numbers if x % 2 == 0]
print(f"筛选偶数: {evens}")

# C# 对应：numbers.Select(x => x * 2)
doubled = [x * 2 for x in numbers]
print(f"全部翻倍: {doubled}")

# C# 对应：numbers.Where(x => x > 3).Select(x => x * 2)
# 即 filter + transform 一步到位
filtered_transformed = [x * 2 for x in numbers if x > 3]
print(f"筛选 > 3 再翻倍: {filtered_transformed}")

# ============================================================
# 2. if-else 表达式在推导式中
# ============================================================
# C# 对应：numbers.Select(x => x > 3 ? x * 2 : x)
# 注意：C# 用三元运算符 ? :，Python 用 if-else（顺序不同！）
# Python 语法：[值1 if 条件 else 值2 for x in 数据]
#              ^^^^^^^^^^^^^^^^^^^^^^^^^^ 先写表达式，再写 for
result_if_else = [x * 2 if x > 3 else x for x in numbers]
print(f"if-else 推导式: {result_if_else}")

# 另一个例子：奇偶标记
# C# 对应：numbers.Select(x => x % 2 == 0 ? "偶" : "奇")
labels = ["偶" if x % 2 == 0 else "奇" for x in numbers]
print(f"奇偶标记: {labels}")

# ============================================================
# 3. 排序
# ============================================================
# C# 对应：numbers.OrderByDescending(x => x)
# Python 的 sorted() 返回新列表，推导式本身不排序
sorted_list = sorted(numbers, reverse=True)
print(f"降序排序: {sorted_list}")

# 按自定义规则排序
# C# 对应：numbers.OrderBy(x => x % 10).ThenByDescending(x => x)
sorted_custom = sorted(numbers, key=lambda x: x % 10)
print(f"按个位数排序: {sorted_custom}")

# ============================================================
# 4. 聚合操作
# ============================================================
# C# 对应：numbers.Sum() / numbers.Average()
total = sum(numbers)
avg = sum(numbers) / len(numbers)
min_val = min(numbers)
max_val = max(numbers)
print(f"求和: {total}, 平均值: {avg}, 最小: {min_val}, 最大: {max_val}")

# C# 对应：numbers.Aggregate((acc, x) => acc * x)
from functools import reduce
product = reduce(lambda acc, x: acc * x, numbers)
print(f"累乘: {product}")

# ============================================================
# 5. 链式操作（推导式的精髓）
# ============================================================
# C# 对应：
#   numbers.Where(x => x > 3)
#          .Select(x => x * 2)
#          .OrderBy(x => x)
#          .ToList()
# Python 的推导式从右往左读，LINQ 从上往下读——方向不同，效果相同！
result = sorted([x * 2 for x in numbers if x > 3])
print(f"链式操作（筛选 > 3 → 翻倍 → 排序）: {result}")

# ============================================================
# 6. 字典推导式
# ============================================================
# C# 对应：numbers.ToDictionary(x => x, x => x * x)
# 或者 Enumerable.Range(1,10).ToDictionary(x => x, x => x * x)
square_dict = {x: x ** 2 for x in numbers}
print(f"字典推导: {square_dict}")

# 带条件的字典推导
even_dict = {x: x ** 2 for x in numbers if x % 2 == 0}
print(f"偶数的平方字典: {even_dict}")

# 键值互换
# C# 对应：dict.ToDictionary(kvp => kvp.Value, kvp => kvp.Key)
inverted = {v: k for k, v in square_dict.items()}
print(f"键值互换: {inverted}")

# ============================================================
# 7. 集合推导式
# ============================================================
# C# 对应：numbers.Select(x => x % 3).Distinct().ToList()
# 集合自动去重，跟 C# 的 Distinct() 一个意思
remainders = {x % 3 for x in numbers}
print(f"除以3的余数集合（自动去重）: {remainders}")

square_set = {x ** 2 for x in numbers}
print(f"平方集合: {square_set}")

# ============================================================
# 8. 笛卡尔积
# ============================================================
# C# 对应：
#   colors.SelectMany(c => sizes, (c, s) => (c, s))
# C# 的 SelectMany 就是 Python 推导式里嵌套两个 for 的效果
colors = ["红", "蓝", "绿"]
sizes = ["S", "M", "L"]
combinations = [(c, s) for c in colors for s in sizes]
print(f"笛卡尔积: {combinations}")
print(f"组合数: {len(combinations)} (3 颜色 × 3 尺码)")

# ============================================================
# 9. 嵌套列表推导（矩阵操作）
# ============================================================
# C# 对应：matrix.SelectMany(row => row)
# SelectMany 就是"展平"（flatten），Python 需要手动写嵌套 for
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [x for row in matrix for x in row]
print(f"矩阵展平: {flattened}")

# 嵌套推导的进阶用法：提取每行最大值
# C# 对应：matrix.Select(row => row.Max())
row_maxes = [max(row) for row in matrix]
print(f"每行最大值: {row_maxes}")

# 提取对角线元素
diagonal = [matrix[i][i] for i in range(len(matrix))]
print(f"对角线元素: {diagonal}")

# ============================================================
# 10. 生成器表达式（省内存的推导式）
# ============================================================
# C# 对应：IEnumerable<int> 的延迟求值（Deferred Execution）
# 列表推导式 [] 会立即求值，生成器表达式 () 是惰性的
# C# 的 IEnumerable 默认就是惰性的，Python 需要用 () 来切换
squares_gen = (x ** 2 for x in numbers)  # 注意：圆括号！
print(f"生成器类型: {type(squares_gen)}")
print(f"生成器转列表: {list(squares_gen)}")

# 生成器用于大数据集——不会撑爆内存
big_sum = sum(x ** 2 for x in range(1_000_000))
print(f"百万个数的平方和: {big_sum}")

# ============================================================
# 11. 海象运算符（Walrus Operator）:=（Python 3.8+）
# ============================================================
# C# 没有直接对应，最接近的是：
#   var list = Enumerable.Range(0, 10)
#       .Select(x => new { x, y = x * x })
#       .Where(obj => obj.y > 10)
#       .Select(obj => obj.y);
#
# 海象运算符能在推导式中同时赋值和使用变量，省去重复计算！
# 语法：[表达式 for x in 数据 if (y := f(x)) > 阈值]
#       ^^^^^^^^^^^^^^ 在条件里赋值给 y，同时判断条件

# 没有海象运算符（x**2 被计算了两次：条件里算一次，表达式里又算一次）
squares_without = [x ** 2 for x in range(10) if x ** 2 > 10]
print(f"没有海象运算符: {squares_without}")

# 使用海象运算符（x**2 只计算一次，同时赋值给 y 用于条件判断）
# 关键：海象运算符要写在 if 条件里，这样赋值和判断一步完成
# 语法：[表达式 for x in 数据 if (y := f(x)) > 阈值]
squares_with = [y for x in range(10) if (y := x ** 2) > 10]
print(f"使用海象运算符: {squares_with}")

# 更实用的例子：匹配并处理字符串
import re
texts = ["hello 42", "world", "python 3.14", "no numbers here"]
# 提取数字（海象运算符避免重复调用 re.search）
found = [match.group() for t in texts if (match := re.search(r'\d+', t))]
print(f"海象运算符提取数字: {found}")

# ============================================================
# 12. 用 None 过滤（常见的 Python 惯用法）
# ============================================================
# C# 对应：list.Where(x => x != null)
# Python 的 None 就是 C# 的 null
data = [1, None, 3, None, 5, None, 7]
cleaned = [x for x in data if x is not None]
print(f"过滤 None: {cleaned}")

# ============================================================
# 总结对比表：
# ============================================================
# | 操作         | Python 推导式              | C# LINQ               |
# |-------------|---------------------------|------------------------|
# | 筛选         | [x for x in L if cond]   | L.Where(x => cond)    |
# | 转换         | [f(x) for x in L]        | L.Select(x => f(x))   |
# | 筛选+转换    | [f(x) for x in L if c]   | L.Where(...).Select() |
# | if-else     | [a if c else b for x in L]| L.Select(x=>c?a:b)    |
# | 排序         | sorted(L, key=...)        | L.OrderBy(...)         |
# | 聚合         | sum(L) / min(L) / max(L) | L.Sum() / L.Min()     |
# | 展平         | [x for row in L for x in row] | L.SelectMany(...) |
# | 字典         | {k:v for ...}             | L.ToDictionary(...)    |
# | 延迟求值     | (x for x in L)           | L (IEnumerable 默认)   |
# | 海象运算符   | [y:=f(x) for x in L]     | 无直接对应             |
# ============================================================

print("\n=== 列表推导式 vs LINQ 演示完成！===")
print("记住：Python 追求简洁，C# 追求类型安全。")
print("两种风格各有千秋，关键是选对场景！")
