# ============================================================
# Python 生成器 vs C# 迭代器（IEnumerable + yield）
# 对应文章：2.4 生成器与迭代器
# ============================================================
# 一句话总结：Python 的生成器 ≈ C# 的 yield return
# 但 Python 更简洁——一个 yield 就搞定，C# 需要实现接口。
# 生成器的本质：用的时候才算，算完就扔，省内存！
# ============================================================

from itertools import islice

# ============================================================
# 1. 最简单的生成器函数
# ============================================================
# C# 对应：
#   IEnumerable<int> GetNumbers(int count) {
#       for (int i = 0; i < count; i++) yield return i;
#   }
#
# Python 的 yield ≈ C# 的 yield return
# 区别：Python 只需要一个 yield，C# 需要返回 IEnumerable<T>
def get_numbers(count):
    for i in range(count):
        yield i  # 暂停，返回值，下次从这里继续

print("=== 1. 基础生成器 ===")
for num in get_numbers(5):
    print(f"  {num}", end="")
print()  # 输出: 0 1 2 3 4

# ============================================================
# 2. __iter__ / __next__ 协议（生成器的底层原理）
# ============================================================
# Python 的生成器自动实现了两个魔术方法：
#   __iter__()  → 返回自身（所以生成器可以直接用于 for 循环）
#   __next__()  → 返回下一个值，没有更多值时抛出 StopIteration
#
# C# 对应：IEnumerator<T> 的 MoveNext() + Current
#   MoveNext() → 返回 bool（相当于 Python 的不抛 StopIteration）
#   Current     → 获取当前值
#
# 本质上是同一个设计模式，只是 Python 更隐式（自动实现），
# C# 更显式（需要手动实现接口）。

print("\n=== 2. __iter__ / __next__ 协议 ===")
# 手动调用 next() 就是在调用 __next__()
gen = get_numbers(3)
print(f"  next(gen) = {next(gen)}")   # 0
print(f"  next(gen) = {next(gen)}")   # 1
print(f"  next(gen) = {next(gen)}")   # 2
try:
    next(gen)  # 没有更多值了！
except StopIteration:
    print("  next(gen) → StopIteration!（C# 里 MoveNext() 返回 false）")

# ============================================================
# 3. 斐波那契生成器（经典面试题）
# ============================================================
# C# 对应：
#   IEnumerable<int> Fibonacci(int count) {
#       int a = 0, b = 1;
#       for (int i = 0; i < count; i++) {
#           yield return a;
#           (a, b) = (b, a + b);
#       }
#   }
def fibonacci(count):
    a, b = 0, 1
    for _ in range(count):
        yield a
        a, b = b, a + b  # Python 的元组解包，C# 写法：(a, b) = (b, a + b)

print("\n=== 3. 斐波那契生成器 ===")
print(f"  前 10 个斐波那契数: {list(fibonacci(10))}")

# ============================================================
# 4. return 提前结束（≈ C# 的 yield break）
# ============================================================
# C# 对应：yield break（提前终止迭代）
# Python 的 return 在生成器里 = 立即抛出 StopIteration
def get_positive_numbers(numbers):
    for num in numbers:
        if num <= 0:
            return  # 提前结束迭代（≈ C# 的 yield break）
        yield num

print("\n=== 4. return 提前结束（yield break）===")
data = [3, 1, 4, -1, 5, -2, 9]
result = list(get_positive_numbers(data))
print(f"  输入: {data}")
print(f"  输出（遇到负数就停）: {result}")

# ============================================================
# 5. yield from（委托子生成器）
# ============================================================
# C# 对应：yield return 遍历子集合
#   foreach (var item in First()) yield return item;
#   foreach (var item in Second()) yield return item;
#
# Python 3.3+ 的 yield from 一行搞定！
def concat(first, second):
    yield from first   # 委托给第一个生成器
    yield from second  # 再委托给第二个

print("\n=== 5. yield from（委托子生成器）===")
result = list(concat([1, 2, 3], ["a", "b", "c"]))
print(f"  concat([1,2,3], ['a','b','c']) = {result}")

# ============================================================
# 6. 无限生成器 + islice（按需取值）
# ============================================================
# C# 对应：Take(n) 取前 n 个
#   InfiniteFibonacci().Take(10)
# Python 用 itertools.islice 实现同样的效果
def infinite_fibonacci():
    a, b = 0, 1
    while True:  # 无限循环！但不会撑爆内存
        yield a
        a, b = b, a + b

print("\n=== 6. 无限生成器 + islice ===")
fib = list(islice(infinite_fibonacci(), 10))
print(f"  前 10 个斐波那契数: {fib}")

# 取 10 到 15 的斐波那契数（跳过前 10 个）
fib_slice = list(islice(infinite_fibonacci(), 10, 15))
print(f"  第 10~15 个斐波那契数: {fib_slice}")

# ============================================================
# 7. 生成器管道（数据流处理）
# ============================================================
# C# 对应：LINQ 的链式调用
#   ReadData()
#       .Where(x => x > 0)
#       .Select(x => x * 2)
#       .Take(5)
#
# Python 的生成器管道：多个生成器串联，数据像流水线一样流过
# 每个生成器只处理自己那一步，内存占用极低！

def read_data():
    """模拟从文件/数据库读取数据"""
    for i in range(20):
        yield i

def filter_positive(data):
    """只保留正数"""
    for x in data:
        if x > 0:
            yield x

def double_values(data):
    """每个值翻倍"""
    for x in data:
        yield x * 2

def take_n(data, n):
    """只取前 n 个"""
    count = 0
    for x in data:
        if count >= n:
            return
        yield x
        count += 1

print("\n=== 7. 生成器管道 ===")
# 数据流：读取 → 过滤正数 → 翻倍 → 取前 5 个
pipeline = take_n(double_values(filter_positive(read_data())), 5)
print(f"  管道结果: {list(pipeline)}")

# 用生成器表达式更优雅的写法（一行搞定管道）
pipeline_v2 = list(islice(
    (x * 2 for x in read_data() if x > 0),
    5
))
print(f"  推导式管道: {pipeline_v2}")

# ============================================================
# 8. send() 方法——给生成器发消息
# ============================================================
# C# 没有直接对应！这是 Python 生成器的独家绝活。
# send() 可以向生成器内部发送值，改变生成器的行为。
# 常用于协程（coroutine）模式。
def accumulator():
    """累加器：接收外部传入的值并累加"""
    total = 0
    while True:
        value = yield total  # yield 既输出 total，又接收 send() 的值
        if value is None:
            break
        total += value

print("\n=== 8. send() 方法 ===")
acc = accumulator()
next(acc)              # 启动生成器（必须先调用 next 或 send(None)）
print(f"  send(10) → 累计: {acc.send(10)}")   # 10
print(f"  send(20) → 累计: {acc.send(20)}")   # 30
print(f"  send(30) → 累计: {acc.send(30)}")   # 60
print("  （C# 没有 send()，但可以用 Rx.NET 实现类似效果）")

# ============================================================
# 9. 生成器只能遍历一次！
# ============================================================
# C# 的 IEnumerable<T> 也是一样的——每次 foreach 都重新执行
# 但 IEnumerable 可以反复调用（每次调用GetEnumerator()），
# Python 的生成器用完就没了，不能重来。
def numbers():
    yield 1
    yield 2
    yield 3

print("\n=== 9. 生成器只能遍历一次 ===")
gen = numbers()
print(f"  第一次 list(gen): {list(gen)}")   # [1, 2, 3]
print(f"  第二次 list(gen): {list(gen)}")   # []  空了！
print("  （用完就没了！C# 的 IEnumerable 也需要重新调用方法才能再次遍历）")

# 如果需要多次遍历，转换为列表
gen2 = numbers()
data_list = list(gen2)  # 转为列表，可以多次使用
print(f"  转列表后: {data_list}, 再次: {data_list}")

# ============================================================
# 10. 生成器表达式（一行搞定）
# ============================================================
# C# 对应：Enumerable.Range(1, 5).Select(x => x * x)
# Python 的生成器表达式用圆括号 ()，列表推导式用方括号 []
print("\n=== 10. 生成器表达式 ===")
squares_gen = (x ** 2 for x in range(1, 6))  # 圆括号 = 生成器
print(f"  类型: {type(squares_gen)}")
print(f"  转列表: {list(squares_gen)}")

# 用于求和——不需要中间列表，直接流式计算
big_sum = sum(x ** 2 for x in range(1_000_000))
print(f"  百万个数的平方和: {big_sum}")

# ============================================================
# 11. 生成器 vs 列表：内存对比
# ============================================================
print("\n=== 11. 生成器 vs 列表：内存对比 ===")
import sys

# 列表：所有数据同时存在于内存中
list_comp = [x ** 2 for x in range(1000)]
print(f"  列表占用内存: {sys.getsizeof(list_comp)} 字节")

# 生成器：只保存当前状态，内存几乎不变
gen_comp = (x ** 2 for x in range(1000))
print(f"  生成器占用内存: {sys.getsizeof(gen_comp)} 字节")
print("  （生成器的内存占用是固定的，跟数据量无关！）")

# ============================================================
# 总结对比表：
# ============================================================
# | 操作              | Python                  | C#                      |
# |------------------|-------------------------|--------------------------|
# | 生成/迭代         | yield                   | yield return             |
# | 委托子生成器       | yield from              | foreach + yield return   |
# | 提前结束           | return                  | yield break              |
# | 按需取前 n 个      | islice(gen, n)          | .Take(n)                 |
# | 发送值给生成器      | gen.send(value)         | 无直接对应               |
# | 无限序列           | while True: yield       | while (true) yield return|
# | 惰性求值           | 生成器自动惰性           | IEnumerable 默认惰性      |
# | 多次遍历           | 不能（需转列表）          | 可以（重新GetEnumerator） |
# ============================================================

print("\n=== 生成器 vs 迭代器 演示完成！===")
print("记住：生成器是 Python 最优雅的特性之一。")
print("C# 的 yield return 虽然啰嗦一点，但思路完全一样！")
