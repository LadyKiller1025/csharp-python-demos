# ============================================================
# Python Lambda 表达式示例 —— C# 老兵的 Python 修炼手册 第二阶段 2.2
# ============================================================
# C# 程序员注意：Python 的 lambda 比 C# 的简单得多（也弱得多）
# Python lambda 只能是一个表达式，不能写多行语句
# C# 的 lambda 可以有代码块、async、throw……是亲生的
# Python 的 lambda 是"匿名函数的快捷方式"，仅此而已


# ============================================================
# 1. 基础语法：lambda 参数 : 表达式
# ============================================================
# C# 等价：Func<int, int> square = x => x * x;
# Python 写法：lambda x: x * x
# 区别：Python 用冒号，C# 用箭头 =>
#        Python 只能写一个表达式，C# 可以写代码块 { }

print("=== 1. 基础语法 ===")
square = lambda x: x * x
add = lambda a, b: a + b
print(f"square(5) = {square(5)}")        # 25
print(f"add(3, 4) = {add(3, 4)}")        # 7

# Python lambda 可以直接调用（IIFE 风格）
# C# 做不到：(x => x + 1)(5) 编译不通过
print(f"(lambda x: x + 1)(10) = {(lambda x: x + 1)(10)}")  # 11
print("Python lambda 可以立即调用，C# 不行（除非先赋值给变量）")


# ============================================================
# 2. map() 和 filter() 中的 lambda
# ============================================================
# C# 等价：numbers.Select(x => x * 2).ToList()  /  numbers.Where(x => x % 2 == 0)
# Python 的 map/filter 返回迭代器，需要用 list() 转换
# C# 的 LINQ 方法返回 IQueryable 或 IEnumerable，调用 ToList() 才执行

print("\n=== 2. map 和 filter ===")
numbers = [1, 2, 3, 4, 5]

doubled = list(map(lambda x: x * 2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"原始列表: {numbers}")
print(f"map(x*2): {doubled}")           # [2, 4, 6, 8, 10]
print(f"filter(偶数): {evens}")          # [2, 4]

# map 可以接受多个可迭代对象
a = [1, 2, 3]
b = [10, 20, 30]
sums = list(map(lambda x, y: x + y, a, b))
print(f"多列表 map: {sums}")            # [11, 22, 33]


# ============================================================
# 3. 排序中的 lambda
# ============================================================
# C# 等价：users.Sort((a, b) => a.Age.CompareTo(b.Age));
# Python 的 sort() 接受 key 参数（一个函数）
# C# 的 Sort() 接受 Comparer 或 lambda 返回 int
# Python 更简洁：指定排序键就行，不用写比较逻辑

print("\n=== 3. 排序中的 lambda ===")
users = [
    {"name": "张三", "age": 25},
    {"name": "李四", "age": 30},
    {"name": "王五", "age": 22},
    {"name": "赵六", "age": 35},
]

# 按名字排序
by_name = sorted(users, key=lambda u: u["name"])
print("按名字排序:")
for u in by_name:
    print(f"  {u['name']} ({u['age']}岁)")

# 按年龄降序排序
by_age_desc = sorted(users, key=lambda u: u["age"], reverse=True)
print("按年龄降序:")
for u in by_age_desc:
    print(f"  {u['name']} ({u['age']}岁)")

# 用 itemgetter 替代 lambda（性能更好）
from operator import itemgetter
by_name_fast = sorted(users, key=itemgetter("name"))
print(f"\n用 itemgetter 排序（更快，相当于 C# 的属性访问）")


# ============================================================
# 4. 闭包：Lambda 捕获外部变量
# ============================================================
# C# 等价：Func<int, int> multiplier = x => x * factor;
# Python 和 C# 都支持闭包——Lambda 可以"记住"定义时的变量
# C# 注意：循环中的闭包陷阱在两个语言中都存在！

print("\n=== 4. 闭包 ===")

def multiplier(factor):
    """返回一个乘法器——经典的闭包用法"""
    return lambda x: x * factor

triple = multiplier(3)
double = multiplier(2)
print(f"triple(5) = {triple(5)}")     # 15
print(f"double(5) = {double(5)}")      # 10

# 闭包捕获的是变量引用，不是值
def make_accumulator():
    total = 0
    def accumulator(x):
        nonlocal total
        total += x
        return total
    return accumulator

acc = make_accumulator()
print(f"acc(1) = {acc(1)}")     # 1
print(f"acc(2) = {acc(2)}")     # 3
print(f"acc(3) = {acc(3)}")     # 6
print("每次调用都记住了上一次的 total——这就是闭包的魔力")


# ============================================================
# 5. Lambda 作为参数
# ============================================================
# C# 等价：Apply(x => x * 2, 5)
# Python 函数是一等公民，Lambda 可以作为参数传递
# C# 需要通过 Func<T, TResult> 委托传递

print("\n=== 5. Lambda 作为参数 ===")

def apply(func, value):
    """接受一个函数和一个值，对值应用函数"""
    return func(value)

# 传入 lambda
result1 = apply(lambda x: x * 2, 5)
result2 = apply(lambda x: x ** 2, 5)
result3 = apply(lambda x: f"[{x}]", "hello")
print(f"apply(x*2, 5) = {result1}")      # 10
print(f"apply(x**2, 5) = {result2}")     # 25
print(f"apply([x], hello) = {result3}")   # [hello]

# 实际应用：数据转换
users_sorted = sorted(
    [{"name": "张三", "age": 25}, {"name": "李四", "age": 30}],
    key=lambda u: u["age"]
)
print(f"排序结果: {[u['name'] for u in users_sorted]}")


# ============================================================
# 6. 条件表达式（三元运算符）
# ============================================================
# C# 等价：condition ? trueValue : falseValue
# Python 写法：trueValue if condition else falseValue
# 注意顺序不同！C# 是 condition?true:false，Python 是 true if condition else false

print("\n=== 6. 条件表达式（三元运算符）")
# 基础三元
age = 20
status = "成年" if age >= 18 else "未成年"
print(f"年龄 {age}: {status}")

# Lambda 中使用三元
classify = lambda x: "正数" if x > 0 else ("零" if x == 0 else "负数")
print(f"classify(5) = {classify(5)}")
print(f"classify(-3) = {classify(-3)}")
print(f"classify(0) = {classify(0)}")

# C# 等价：Func<int, string> classify = x => x > 0 ? "正数" : (x == 0 ? "零" : "负数");
# Python 的 if-else 在 lambda 中是表达式（有返回值）
# 但 Python 的 if 语句在 lambda 中不能用（因为它是语句不是表达式）
# 例如：lambda x: print(x) if x > 0 else None  # print 返回 None，不是 True/False 的分支

# [WARN] 注意：Python 的条件表达式和 if 语句是不同的东西
# 条件表达式：a if condition else b  （表达式，有返回值）
# if 语句：if condition: ...         （语句，没有返回值，不能用在 lambda 里）


# ============================================================
# 7. 最佳实践：列表推导式 vs Lambda 链
# ============================================================
# 当 lambda + map/filter 变复杂时，列表推导式通常更清晰
# C# 同学：这就像是 LINQ 查询语法 vs 方法语法的选择

print("\n=== 7. 最佳实践：列表推导式 vs Lambda ===")
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# [X] 不好：嵌套的 lambda + map + filter（可读性差）
bad_result = list(map(lambda x: x * 2, filter(lambda x: x > 3, numbers)))
print(f"嵌套 map/filter: {bad_result}")

# [OK] 好：列表推导式（Pythonic！）
good_result = [x * 2 for x in numbers if x > 3]
print(f"列表推导式:      {good_result}")

# [OK] 也好：链式方法调用（类 LINQ 风格）
also_good = [x * 2 for x in numbers if x > 3]  # 列表推导式
# 或者用 sorted + key 这种场景，lambda 就很合适
sorted_nums = sorted(numbers, key=lambda x: -x)  # 降序
print(f"降序排序: {sorted_nums}")

# 总结：什么时候用什么？
print("""
使用指南：
  [OK] 用 lambda：sorted(key=...), 作为回调, 简单的一行转换
  [OK] 用列表推导式：复杂的过滤+转换, 需要可读性
  [X] 避免：嵌套的 map(lambda, filter(lambda, ...))
  类似 C# 中 LINQ 方法链 vs 查询语法的选择
""")


# ============================================================
# 8. 高级用法：reduce 和 functools
# ============================================================
# C# 等价：numbers.Aggregate(0, (acc, x) => acc + x)
# Python 的 reduce 需要导入 functools
# C# 的 Aggregate 方法内置在 LINQ 中

print("=== 8. reduce（函数式编程）===")
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# 累加
total = reduce(lambda acc, x: acc + x, numbers)
print(f"reduce(累加): {total}")  # 15

# 累乘
product = reduce(lambda acc, x: acc * x, numbers)
print(f"reduce(累乘): {product}")  # 120

# 但其实不用这么复杂——Python 内置了 sum() 和 math.prod()
import math
print(f"sum() 更简单: {sum(numbers)}")
print(f"math.prod() 更简单: {math.prod(numbers)}")
print("记住：能用内置函数就别用 reduce——Python 的哲学是简洁至上")


# ============================================================
# 9. 用 sorted + lambda 处理复杂排序
# ============================================================
# 实战场景：多键排序、自定义排序逻辑

print("=== 9. 实战：复杂排序 ===")
students = [
    {"name": "张三", "math": 90, "english": 85},
    {"name": "李四", "math": 85, "english": 92},
    {"name": "王五", "math": 90, "english": 78},
    {"name": "赵六", "math": 75, "english": 85},
]

# 按数学成绩降序，英语成绩升序（C# 的 ThenBy 等价）
sorted_students = sorted(
    students,
    key=lambda s: (-s["math"], s["english"])  # 负号实现降序
)
print("按数学降序、英语升序:")
for s in sorted_students:
    print(f"  {s['name']}: 数学={s['math']}, 英语={s['english']}")


# ============================================================
# 10. Lambda 陷阱与注意事项
# ============================================================
print("\n=== 10. Lambda 陷阱 ===")
print("""
[WARN] Python Lambda 注意事项：
  1. 只能写一个表达式，不能有赋值、循环等语句
  2. 调试困难——lambda 没有名字（除非赋值给变量）
  3. 不能加文档字符串（docstring）
  4. 复杂逻辑请用 def 定义正式函数
  5. Python 的 lambda 比 C# 的弱很多——别指望它做太多事
""")


# ============================================================
# 总结对比
# ============================================================
print("=" * 50)
print("[TABLE] C# vs Python Lambda 速查表")
print("=" * 50)
print("""
┌───────────────────────────┬──────────────────────────────┐
│          C#               │          Python              │
├───────────────────────────┼──────────────────────────────┤
│ x => x * x               │ lambda x: x * x             │
│ (x, y) => x + y          │ lambda x, y: x + y          │
│ x => { ... }             │ [X] 不支持代码块             │
│ Func<int, int>            │ 直接赋值给变量              │
│ .Select(x => ...)        │ map(lambda x: ..., list)    │
│ .Where(x => ...)         │ filter(lambda x: ..., list) │
│ .OrderBy(x => ...)       │ sorted(key=lambda x: ...)   │
│ .Aggregate(...)          │ functools.reduce(...)       │
│ condition ? a : b        │ a if condition else b       │
│ 支持 async/await          │ [X] 不支持                    │
└───────────────────────────┴──────────────────────────────┘
""")
