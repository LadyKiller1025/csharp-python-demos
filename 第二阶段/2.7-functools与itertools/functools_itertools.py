# Python functools 与 itertools 示例
# 对应文章：2.7 functools与itertools
#
# C# 老兵的 Python 修炼手册：
# functools 是 Python 的"函数工具箱"，相当于 C# 的扩展方法 + 特性；
# itertools 是 Python 的"迭代器军火库"，相当于 C# 的 LINQ + 一些黑科技。

from functools import (
    reduce, lru_cache, partial, singledispatch, cache
)
from itertools import (
    count, cycle, repeat, chain, islice,
    compress, filterfalse, starmap, groupby, product,
    takewhile, dropwhile, zip_longest,
    permutations, combinations
)
from operator import mul, itemgetter

# ================================================================
#                       functools 示例
# ================================================================

print("=" * 60)
print("               functools 模块 —— 函数的瑞士军刀")
print("=" * 60)

# 1. reduce —— 累积计算（C# 中用 LINQ 的 Aggregate）
# C# 对应: numbers.Aggregate((acc, x) => acc + x)
numbers = [1, 2, 3, 4, 5]
total = reduce(lambda acc, x: acc + x, numbers)
product_result = reduce(mul, numbers)
print(f"\n--- 1. reduce（累积计算）---")
print(f"  求和: {total}")        # 15
print(f"  求积: {product_result}")  # 120

# 2. lru_cache —— LRU 缓存（C# 需手动用 Dictionary 实现）
# C# 对应: 手动维护 Dictionary<int, long> 做缓存，或用 [Memoize] 特性（.NET 8+）
@lru_cache(maxsize=128)
def fibonacci(n):
    """经典的斐波那契 —— 有缓存后从 O(2^n) 变成 O(n)"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(f"\n--- 2. lru_cache（LRU 缓存）---")
print(f"  fib(30) = {fibonacci(30)}")
print(f"  缓存命中: {fibonacci.cache_info()}")

# 3. cache —— Python 3.9+ 的无限缓存（比 lru_cache 更简洁）
# C# 对应: 没有内置的无限缓存，需要自己封装
#           [Memoize] 特性（.NET 8+）是类似的思路，但没有大小限制管理
# cache = lru_cache(maxsize=None)  # 本质上就是这样！

@cache
def factorial(n):
    """用 @cache 装饰的阶乘 —— 比 @lru_cache 写起来更爽"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(f"\n--- 3. cache（无限缓存，Python 3.9+）---")
print(f"  10! = {factorial(10)}")
print(f"  20! = {factorial(20)}")
print(f"  特点: 不需要指定 maxsize，永远不会淘汰缓存")
print(f"  对比 @lru_cache: cache = lru_cache(maxsize=None)，但写起来更短更爽")
print(f"  C# 对比: .NET 8 的 [Memoize] 特性有点类似，但目前还不支持异步")

# 4. partial —— 偏函数（固定部分参数）
# C# 对应: Func<T> 闭包，或者带默认参数的方法
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)
print(f"\n--- 4. partial（偏函数）---")
print(f"  平方: {square(5)}")   # 25
print(f"  立方: {cube(5)}")     # 125

# 5. singledispatch —— 单分派泛型函数（C# 有真正的泛型！）
# C# 对应: 方法重载 / 模式匹配（switch + when）
@singledispatch
def to_string(value):
    return str(value)

@to_string.register(int)
def _(value):
    return f"整数: {value}"

@to_string.register(list)
def _(value):
    return f"列表(长度{len(value)}): {value}"

@to_string.register(dict)
def _(value):
    return f"字典({len(value)}个键): {list(value.keys())}"

print(f"\n--- 5. singledispatch（单分派泛型）---")
print(f"  {to_string(42)}")           # 整数: 42
print(f"  {to_string([1, 2, 3])}")   # 列表(长度3): [1, 2, 3]
print(f"  {to_string({'a': 1})}")    # 字典(1个键): ['a']
print(f"  C# 对比: 直接用方法重载就行，C# 的类型系统更强")

# ================================================================
#                       itertools 示例
# ================================================================

print("\n" + "=" * 60)
print("               itertools 模块 —— 迭代器的军火库")
print("=" * 60)

# 6. chain —— 串联多个可迭代对象（C# 用 Concat）
# C# 对应: list1.Concat(list2).Concat(list3)
list1 = [1, 2, 3]
list2 = ["a", "b", "c"]
list3 = [100, 200]
combined = list(chain(list1, list2, list3))
print(f"\n--- 6. chain（串联）---")
print(f"  结果: {combined}")

# 7. islice —— 切片迭代器（C# 用 Take/Skip）
# C# 对应: Enumerable.Range(1, 5)
first_five = list(islice(count(1), 5))
print(f"\n--- 7. islice（切片）---")
print(f"  前5个自然数: {first_five}")

# 8. compress —— 按掩码过滤（C# 用 Where + 索引）
# C# 对应: data.Where((item, index) => mask[index])
data = ["A", "B", "C", "D", "E"]
mask = [1, 0, 1, 0, 1]
filtered = list(compress(data, mask))
print(f"\n--- 8. compress（掩码过滤）---")
print(f"  结果: {filtered}")  # ['A', 'C', 'E']

# 9. groupby —— 分组（C# 有 GroupBy，但需要预排序！）
# C# 对应: data.GroupBy(x => x.Item1)，但 C# 的 GroupBy 不要求预排序
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4), ("A", 5)]
data.sort(key=itemgetter(0))
print(f"\n--- 9. groupby（分组）---")
for key, group in groupby(data, key=itemgetter(0)):
    print(f"  组 {key}: {list(group)}")
print(f"  注意: Python 的 groupby 要求数据先排序！C# 的 GroupBy 不需要")

# 10. product —— 笛卡尔积（C# 用 SelectMany）
# C# 对应: suits.SelectMany(s => ranks, (s, r) => (s, r))
suits = ["S", "H"]
ranks = ["A", "K", "Q"]
cards = [(s, r) for s, r in product(suits, ranks)]
print(f"\n--- 10. product（笛卡尔积）---")
print(f"  扑克牌: {cards}")

# 11. starmap —— 星号映射（C# 用 Select）
# C# 对应: pairs.Select(p => p.Item1 * p.Item2)
pairs = [(2, 3), (4, 5), (6, 7)]
results = list(starmap(mul, pairs))
print(f"\n--- 11. starmap（星号映射）---")
print(f"  结果: {results}")  # [6, 20, 42]

# 12. takewhile / dropwhile —— 条件截断（C# 用 TakeWhile / SkipWhile）
# C# 对应: numbers.TakeWhile(n => n < 4)
#           numbers.SkipWhile(n => n % 2 == 0)
# 这两个是 Python 迭代器的"杀手级"功能，用起来特别优雅！
numbers_tw = [1, 3, 5, 2, 4, 6, 8]
taken = list(takewhile(lambda x: x < 5, numbers_tw))
dropped = list(dropwhile(lambda x: x < 5, numbers_tw))
print(f"\n--- 12. takewhile / dropwhile（条件截断）---")
print(f"  原始数据: {numbers_tw}")
print(f"  takewhile(x < 5): {taken}")   # [1, 3] —— 遇到 5 就停
print(f"  dropwhile(x < 5): {dropped}") # [5, 2, 4, 6, 8] —— 跳过小于5的，之后全保留
print(f"  C# 对比: TakeWhile / SkipWhile，几乎一模一样")

# 13. zip_longest —— 不等长拉链（C# 用 Zip + 第三个参数）
# C# 对应: list1.Zip(list2, (a, b) => (a, b)) 但 C# 的 Zip 默认以短的为准
#           要实现 zip_longest 效果需要用更多代码
names = ["Alice", "Bob", "Charlie", "Diana"]
scores = [95, 87, 91]
# 普通 zip 会丢掉 Diana
normal_zip = list(zip(names, scores))
# zip_longest 用 None 填充
full_zip = list(zip_longest(names, scores, fillvalue="(缺考)"))
print(f"\n--- 13. zip_longest（不等长拉链）---")
print(f"  普通 zip:  {normal_zip}")
print(f"  zip_longest: {full_zip}")
print(f"  C# 对比: C# 的 Zip 默认以短的为准，要填充需要额外处理")

# 14. permutations / combinations —— 排列组合（C# 需要手写或用第三方库）
# C# 没有内置的排列组合函数，通常需要自己写递归或用 NuGet 包
# 这是 Python 的 itertools 最让人羡慕的功能之一！
print(f"\n--- 14. permutations / combinations（排列组合）---")
items = ["A", "B", "C"]

# 排列：考虑顺序，从3个中取2个
perms = list(permutations(items, 2))
print(f"  permutations(ABC, 2) = {perms}")
print(f"  共 {len(perms)} 种排列（顺序不同算不同）")

# 组合：不考虑顺序，从3个中取2个
combos = list(combinations(items, 2))
print(f"  combinations(ABC, 2) = {combos}")
print(f"  共 {len(combos)} 种组合（顺序相同算同一种）")

# 全排列
full_perms = list(permutations(items))
print(f"  全排列: {full_perms}")
print(f"  共 {len(full_perms)} = 3! 种")
print(f"  C# 对比: C# 没有内置排列组合，需要自己写递归或用 MoreLINQ 等库")

print("\n" + "=" * 60)
print("  总结: functools 是函数的增强工具箱，itertools 是迭代器的军火库")
print("  C# 开发者的感受: LINQ 已经很强了，但 itertools 的排列组合真的很香！")
print("=" * 60)
