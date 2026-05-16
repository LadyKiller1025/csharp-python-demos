# ============================================================
# Python 函数定义示例 —— C# 老兵的 Python 修炼手册 第二阶段 2.1
# ============================================================
# C# 程序员注意：Python 没有 "方法" 这个概念，只有函数。
# 类里面的函数叫"方法"，模块顶层的叫"函数"，就这么简单。
# 不需要 public/private/protected，不需要 static（类方法除外），
# 甚至不需要声明返回类型——Python 说：信我就对了！


# ============================================================
# 1. 基础语法：def 就完事了
# ============================================================
# C# 等价：public string Greet(string name) { ... }
# Python 不需要访问修饰符、返回类型、参数类型——一个 def 走天下

def greet(name):
    return f"Hello, {name}!"

print("=== 1. 基础语法 ===")
print(greet("Python"))


# ============================================================
# 2. 无返回值（隐式返回 None）
# ============================================================
# C# 等价：public void SayHello() { ... }
# Python 没有 void 关键字，不写 return 就返回 None
# 就像 C# 的 async void 一样让人不安（开玩笑）

def say_hello():
    print("Hello!")

print("\n=== 2. 无返回值 ===")
say_hello()
# 验证一下：不写 return 到底返回啥
result = say_hello()
print(f"say_hello() 的返回值: {result}")  # None
print(f"类型: {type(result)}")  # <class 'NoneType'>


# ============================================================
# 3. 多参数与类型提示（Type Hints）
# ============================================================
# C# 等价：public static int Add(int a, int b) { ... }
# 类型提示是可选的（Python 3.5+），解释器会忽略它们
# 但对 IDE 补全和静态检查（mypy）很有用
# 相当于 C# 的 nullable annotation，是"建议"而非"约束"

def add(a: int, b: int) -> int:
    return a + b

print("\n=== 3. 多参数与类型提示 ===")
print(f"add(3, 5) = {add(3, 5)}")
# Python 不关心你传什么类型，类型提示只是"君子协定"
print(f"add('Hello', ' World') = {add('Hello', ' World')}")  # 照样跑
print("Python: '类型提示？我看看就好，不检查的。'")  # 运行时不验证！


# ============================================================
# 4. 默认参数
# ============================================================
# C# 等价：public string Greet2(string name, string greeting = "Hello")
# 规则一样：有默认值的参数放后面
# [WARN] 经典坑：默认参数是可变对象时，会被所有调用共享！

def greet2(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print("\n=== 4. 默认参数 ===")
print(greet2("World"))
print(greet2("World", "你好"))

# [WARN] 经典陷阱：可变默认参数（mutable default argument）
def buggy_append(item, lst=[]):
    lst.append(item)
    return lst

print(f"第一次调用: {buggy_append(1)}")  # [1]
print(f"第二次调用: {buggy_append(2)}")  # [1, 2] —— 意不意外？
print("[WARN] 默认列表被共享了！C# 至少不会给你这个'惊喜'")

# 正确写法：用 None 作为哨兵值
def safe_append(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(f"修正后第一次: {safe_append(1)}")  # [1]
print(f"修正后第二次: {safe_append(2)}")  # [2] —— 这才对！


# ============================================================
# 5. *args —— 可变位置参数
# ============================================================
# C# 等价：public static int Sum(params int[] numbers) { ... }
# *args 接收任意数量的位置参数，打包成 tuple
# C# 的 params 只能放在最后一个参数，Python 也是

def sum_numbers(*args):
    print(f"  args 的类型: {type(args)}")  # <class 'tuple'>
    print(f"  args 的值: {args}")
    return sum(args)

print("\n=== 5. *args 可变参数 ===")
print(f"sum_numbers(1, 2, 3) = {sum_numbers(1, 2, 3)}")
print(f"sum_numbers(10, 20) = {sum_numbers(10, 20)}")


# ============================================================
# 6. **kwargs —— 可变关键字参数
# ============================================================
# C# 没有直接等价物，最接近的是 Dictionary<string, object>
# 或者用命名参数 + 可选参数模拟
# **kwargs 接收任意数量的关键字参数，打包成 dict

def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

print("\n=== 6. **kwargs 可变关键字参数 ===")
print_info(name="张三", age=25, language="Python")


# ============================================================
# 7. 混合使用：*args, **kwargs, 默认参数
# ============================================================
# 参数顺序规则（C# 也类似）：
#   普通参数 > 默认参数 > *args > keyword-only > **kwargs

def flexible(a, b, *args, **kwargs):
    print(f"  a={a}, b={b}")
    print(f"  args={args}")
    print(f"  kwargs={kwargs}")

print("\n=== 7. 混合参数 ===")
flexible(1, 2, 3, 4, 5, key1="x", key2="y")


# ============================================================
# 8. 仅限位置参数（Python 3.8+）
# ============================================================
# C# 没有等价物！这是 Python 独有的。
# 参数名前加 / 表示这个参数只能按位置传递
# 用途：允许参数名和内置函数/父类参数名不同，避免冲突

def pos_only(arg, /, multiplier=1):
    # arg 只能位置传递，不能写 pos_only(arg=xxx)
    return arg * multiplier

print("\n=== 8. 仅限位置参数 (Python 3.8+) ===")
print(f"pos_only(5, 2) = {pos_only(5, 2)}")       # 10
# 下面这行会报错：pos_only(arg=5)
print("C# 没有这个概念，这是 Python 独创！")


# ============================================================
# 9. 仅限关键字参数
# ============================================================
# C# 没有等价物（命名参数是调用方选择的，不是定义方强制的）
# * 号后面的参数必须用关键字传递

def kwd_func(arg1, *, verbose=False, indent=2):
    if verbose:
        print(f"  {' ' * indent}处理中...")
    return f"result={arg1}"

print("\n=== 9. 仅限关键字参数 ===")
print(kwd_func(42))
print(kwd_func(42, verbose=True))


# ============================================================
# 10. 函数作为参数（高阶函数）
# ============================================================
# C# 等价：使用 Func<T, TResult> 或 Action<T> 委托
# Python 函数是一等公民（first-class citizen），
# 可以像变量一样传来传去，不需要定义委托类型

def apply(func, value):
    return func(value)

print("\n=== 10. 高阶函数 ===")
# 传入普通函数
print(f"apply(str, 42) = {apply(str, 42)}")
# 传入 lambda
print(f"apply(lambda x: x**2, 5) = {apply(lambda x: x**2, 5)}")
# 传入内置函数
print(f"apply(len, 'hello') = {apply(len, 'hello')}")


# ============================================================
# 11. 多个返回值（元组解包）
# ============================================================
# C# 等价：返回 (int, int) 命名元组
# Python 天然支持多返回值，实际是返回一个 tuple
# 然后用解包语法一次接收——比 C# 的 ValueTuple 更自然

def divide(a, b):
    return a // b, a % b  # 返回元组 (quotient, remainder)

print("\n=== 11. 多个返回值 ===")
quotient, remainder = divide(10, 3)
print(f"10 // 3 = {quotient}, 10 % 3 = {remainder}")


# ============================================================
# 12. 嵌套函数与闭包
# ============================================================
# C# 等价：本地函数（C# 7.0+）或 Lambda 闭包
# Python 支持函数嵌套，内部函数可以捕获外部变量（闭包）

def make_counter(start=0):
    """创建一个计数器——经典的闭包用法"""
    count = start

    def counter():
        nonlocal count  # 类似 C# 的闭包捕获外部变量
        count += 1
        return count

    return counter

print("\n=== 12. 嵌套函数与闭包 ===")
my_counter = make_counter(10)
print(f"计数器: {my_counter()}")  # 11
print(f"计数器: {my_counter()}")  # 12
print(f"计数器: {my_counter()}")  # 13
print("（C# 本地函数不能这样玩，因为它不支持 nonlocal）")


# ============================================================
# 13. 装饰器预告（简单展示）
# ============================================================
# C# 没有等价物，最接近的是 [Attribute] + AOP 框架
# 装饰器本质上是"函数包装函数"，后面章节会详细讲

import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"  [TIMER] {func.__name__} 耗时 {end - start:.6f}s")
        return result
    return wrapper

print("\n=== 13. 装饰器预告 ===")

@timer  # 这个语法糖后面会详细讲
def slow_add(a, b):
    time.sleep(0.01)
    return a + b

print(f"slow_add(1, 2) = {slow_add(1, 2)}")


# ============================================================
# 14. 类型提示完整示例
# ============================================================
# C# 程序员会觉得这才是"正常"的写法
# 但记住：Python 的类型提示是可选的，运行时完全忽略

from typing import List, Dict, Optional, Tuple, Callable

def process_data(
    items: List[int],
    config: Dict[str, str],
    callback: Optional[Callable[[int], str]] = None
) -> Tuple[List[str], int]:
    """类型提示完整示例"""
    results = []
    for item in items:
        if callback:
            results.append(callback(item))
        else:
            results.append(str(item))
    return results, len(items)

print("\n=== 14. 类型提示完整示例 ===")
nums = [1, 2, 3, 4, 5]
cfg = {"format": "json"}
result_list, count = process_data(nums, cfg, lambda x: f"item_{x}")
print(f"结果: {result_list}")
print(f"数量: {count}")
print("C# 程序员：'这下舒服多了，有类型提示就是亲切！'")


# ============================================================
# 15. 函数注解（Function Annotations）
# ============================================================
# Python 3.0 引入，给函数参数和返回值附加元数据
# 运行时可以通过 __annotations__ 访问
# 类型提示的底层机制

def annotated_func(x: int, y: str = "hello") -> bool:
    """演示函数注解"""
    return len(y) > x

print("\n=== 15. 函数注解 ===")
print(f"注解内容: {annotated_func.__annotations__}")
print(f"返回值: {annotated_func(3, 'world')}")


# ============================================================
# 总结对比
# ============================================================
print("\n" + "=" * 50)
print("[TABLE] C# vs Python 函数定义 速查表")
print("=" * 50)
print("""
┌─────────────────────┬──────────────────────────────┐
│       C#            │          Python              │
├─────────────────────┼──────────────────────────────┤
│ void Method()       │ def func():                  │
│ int Add(int a, int b)│ def add(a: int, b: int) -> int│
│ params int[] nums   │ *args                       │
│ Dictionary<...>     │ **kwargs                    │
│ 默认参数在最后       │ 同上                        │
│ Func<T,R> 委托      │ 直接传函数名/lambda          │
│ ValueTuple 多返回值  │ 直接 return a, b            │
│ 本地函数             │ 嵌套函数 + nonlocal          │
│ [Attribute] 装饰     │ @decorator 语法糖           │
│ 必须声明类型         │ 类型提示可选                 │
└─────────────────────┴──────────────────────────────┘
""")
