# ============================================================================
# Python 闭包（Closure）与作用域
# 对应文章：2.6 闭包与作用域
# ============================================================================
#
# 【C# 程序员的 Python 修炼手册】
#
# 闭包 = 内部函数 + 它引用的外部变量（即使外部函数已经返回）
#
# | C# 概念                  | Python 等价           | 说明                       |
# |--------------------------|-----------------------|----------------------------|
# | Lambda 捕获变量          | 闭包                  | 都是捕获变量引用，不是值     |
# | local 变量               | LEGB 中的 L          | 函数内局部变量              |
# | 静态变量 (static local)  | 闭包 + nonlocal       | Python 用闭包模拟 static     |
# | 迭代器中的闭包陷阱       | 循环闭包陷阱          | 两者都捕获变量引用导致问题   |
# | Action<T> / Func<T>     | 返回内部函数的函数    | 函数是一等公民              |
#
# 关键区别：
# - C# lambda 捕获的变量在 C# 8+ 中有明确的 mutability 限制
# - Python 闭包捕获的是变量的引用，完全开放读写
# - C# 的闭包变量编译后生成编译器类（closure class），Python 在函数 __closure__ 中
# ============================================================================

from functools import wraps, partial


# ============================================================================
# 1. 基础闭包 —— 函数返回函数，内函数引用外部变量
# ============================================================================
#
# 闭包的三个条件：
#   1. 有嵌套函数（函数内部定义函数）
#   2. 内部函数引用了外部函数的变量
#   3. 外部函数返回内部函数

def make_multiplier(factor):
    """创建一个乘法器函数

    【C# 等价】
    Func<int, int> MakeMultiplier(int factor)
    {
        return x => x * factor;  // lambda 捕获 factor
    }

    关键：factor 被"记住"了，即使 make_multiplier() 已经执行完毕
    """
    def multiplier(x):
        return x * factor
    return multiplier


# --- 演示 ---
print("=" * 70)
print("  Python 闭包（Closure）与作用域演示")
print("  C# 程序员的 Python 修炼手册 —— 2.6")
print("=" * 70)

print("\n--- 1. 基础闭包 ---")
triple = make_multiplier(3)    # factor=3 被记住
double = make_multiplier(2)    # factor=2 被记住

print(f"  triple(5)  = {triple(5)}")     # 15
print(f"  double(5)  = {double(5)}")     # 10
print(f"  triple(10) = {triple(10)}")    # 30

# 查看闭包捕获的变量
print(f"\n  triple.__closure__ 中有 {len(triple.__closure__)} 个自由变量")
print(f"  被捕获的值: {triple.__closure__[0].cell_contents}")  # 3


# ============================================================================
# 2. nonlocal 关键字 —— 在闭包中修改外部变量
# ============================================================================
#
# 【C# 对比】
# C# 中 lambda 可以直接捕获并修改外部变量（变量提升为编译器生成的类字段）
# Python 中，如果要在内部函数修改外部变量，必须用 nonlocal 声明
#
# 为什么需要 nonlocal？
# Python 默认内部函数中的赋值会创建一个新的局部变量，
# 而不是修改外部变量。nonlocal 告诉 Python "这个变量是外层的"。
#
# 注意：不能用 nonlocal 修改全局变量，修改全局变量用 global

print("\n--- 2. nonlocal 关键字 ---")

def make_counter(start=0):
    """创建一个计数器（用 nonlocal 修改外部变量）

    【C# 等价】
    Func<int> MakeCounter()
    {
        int count = 0;
        return () => ++count;  // C# 的 lambda 可以直接修改捕获的变量
    }
    """
    count = start

    def counter():
        nonlocal count    # 关键！没有这行会报 UnboundLocalError
        count += 1
        return count

    return counter


counter = make_counter()
print(f"  counter() = {counter()}")   # 1
print(f"  counter() = {counter()}")   # 2
print(f"  counter() = {counter()}")   # 3

# 从不同起始值开始
counter_from_10 = make_counter(10)
print(f"  counter_from_10() = {counter_from_10()}")  # 11
print(f"  counter_from_10() = {counter_from_10()}")  # 12


# ============================================================================
# 3. 闭包陷阱（经典 Bug）—— 循环中的闭包
# ============================================================================
#
# 【C# 等价】
# C# 也有完全一样的陷阱！（C# 5.0 之前 foreach 的匿名方法中捕获循环变量）
#
# 陷阱原理：
#   Python 的闭包捕获的是"变量的引用"，不是"变量的值"
#   循环结束后，变量 i 的值是 4，所有 lambda 都引用同一个 i
#   所以调用时都会输出 4
#
# 这是 Python 和 C# 共有的坑，面试高频题！

print("\n--- 3. 闭包陷阱（经典 Bug）---")

# 陷阱重现
print("  陷阱重现:")
funcs = []
for i in range(5):
    funcs.append(lambda: i)  # 所有 lambda 捕获的是同一个 i

# 期望: 0, 1, 2, 3, 4
# 实际: 4, 4, 4, 4, 4
for f in funcs:
    print(f"    输出: {f()}")  # 全是 4！

# --- 解决方法 ---

# 解决方法1：用默认参数绑定当前值（Python 专属技巧）
print("\n  解决方法1: 默认参数（lambda i=i）")
funcs = []
for i in range(5):
    funcs.append(lambda i=i: i)  # i=i 在定义时求值，绑定当前 i 的值
for f in funcs:
    print(f"    输出: {f()}")  # 0, 1, 2, 3, 4

# 解决方法2：用 functools.partial（更 Pythonic）
print("\n  解决方法2: functools.partial")
funcs = [partial(print, f"    输出: {i}") for i in range(5)]
for f in funcs:
    f()  # 0, 1, 2, 3, 4

# 解决方法3：循环内创建新作用域（等价于 C# 的做法）
print("\n  解决方法3: 循环内创建新作用域")
funcs = []
for i in range(5):
    def make_func(val):
        return lambda: val    # 每次调用 make_func 创建新的局部变量 val
    funcs.append(make_func(i))
for f in funcs:
    print(f"    输出: {f()}")  # 0, 1, 2, 3, 4


# ============================================================================
# 4. LEGB 规则 —— Python 变量查找顺序
# ============================================================================
#
# Python 查找一个变量时，按以下顺序搜索：
#   L - Local      局部变量（函数内部）
#   E - Enclosing  外层函数变量（闭包中的自由变量）
#   G - Global     全局变量（模块级别）
#   B - Built-in   内置变量（print, len, range 等）
#
# 【C# 对比】
# C# 的变量作用域规则类似但更严格：
# - 内部变量可以遮蔽外部变量（类似 Python）
# - 但 C# 编译器会警告 CS0136（变量遮蔽）
# - Python 不会有警告，容易踩坑

print("\n--- 4. LEGB 规则 ---")

x = "global"            # G: Global

def outer():
    x = "enclosing"     # E: Enclosing

    def inner():
        x = "local"     # L: Local
        print(f"    inner  中 x = '{x}'")   # local

    inner()
    print(f"    outer  中 x = '{x}'")       # enclosing

outer()
print(f"    全局   中 x = '{x}'")            # global

# --- 无法访问更内层的变量 ---
print("\n  作用域隔离（无法反向访问）:")

def demo_scope():
    local_var = "只存在于 demo_scope 内部"
    print(f"    函数内可以访问: {local_var}")

demo_scope()
try:
    print(f"    函数外: {local_var}")
except NameError as e:
    print(f"    函数外访问失败: {e}")

# --- global vs nonlocal ---
print("\n  global vs nonlocal 对比:")
counter_g = 0

def increment_global():
    global counter_g     # 声明使用全局变量
    counter_g += 1
    print(f"    全局 counter_g = {counter_g}")

print(f"  调用前 counter_g = {counter_g}")
increment_global()
increment_global()
print(f"  调用后 counter_g = {counter_g}")


# ============================================================================
# 5. 闭包作为状态机
# ============================================================================
#
# 闭包最强大的用途之一：封装可变状态，同时隐藏实现细节
#
# 【C# 对比】
# C# 中通常用 class 来实现状态机，但 lambda + 闭包也可以做到：
#   Func<int> counter = (() => { int n = 0; return ++n; });
#   不过 C# 没有 nonlocal，无法直接累加，通常需要 ref 或类
#
# Python 闭包可以实现比 C# lambda 更丰富的状态机

print("\n--- 5. 闭包作为状态机 ---")

# --- 5.1 累加器 ---
print("  5.1 累加器（Accumulator）:")

def make_accumulator(initial=0):
    """创建一个累加器 —— 每次调用追加值"""
    total = initial
    def accumulate(value):
        nonlocal total
        total += value
        return total
    return accumulate

acc = make_accumulator()
print(f"    acc(10)  = {acc(10)}")    # 10
print(f"    acc(20)  = {acc(20)}")    # 30
print(f"    acc(5)   = {acc(5)}")     # 35

# --- 5.2 移动平均 ---
print("\n  5.2 移动平均（Moving Average）:")

def make_moving_average(window_size):
    """创建一个移动平均计算器"""
    values = []

    def average(new_value):
        values.append(new_value)
        # 只保留最近 window_size 个值
        if len(values) > window_size:
            values.pop(0)
        return sum(values) / len(values)

    return average

avg = make_moving_average(3)
print(f"    avg(10) = {avg(10):.2f}")    # 10.00
print(f"    avg(20) = {avg(20):.2f}")    # 15.00
print(f"    avg(30) = {avg(30):.2f}")    # 20.00
print(f"    avg(5)  = {avg(5):.2f}")     # 18.33（窗口: 20, 30, 5）

# --- 5.3 状态机（有限状态机） ---
print("\n  5.3 简易状态机:")

def make_traffic_light():
    """模拟交通灯状态机: green → yellow → red → green ..."""
    states = ["green", "yellow", "red"]
    index = 0

    def next_state():
        nonlocal index
        current = states[index]
        index = (index + 1) % len(states)
        return current

    return next_state

light = make_traffic_light()
for _ in range(6):
    state = light()
    emoji = {"green": "GREEN", "yellow": "YELLOW", "red": "RED"}[state]
    print(f"    当前状态: {emoji}")


# ============================================================================
# 6. 闭包的实用场景
# ============================================================================

print("\n--- 6. 闭包的实用场景 ---")

# --- 6.1 用闭包实现装饰器 ---
print("  6.1 用闭包实现日志装饰器:")

def log_decorator(prefix="[LOG]"):
    """带前缀的日志装饰器（闭包的经典应用）

    【C# 对比】
    等价于 ASP.NET Core 的 ILogger<T> + Action Filter
    或者 [Log("前缀")] 自定义 Attribute
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"    {prefix} 调用 {func.__name__}({args}, {kwargs})")
            result = func(*args, **kwargs)
            print(f"    {prefix} {func.__name__} 返回 {result}")
            return result
        return wrapper
    return decorator

@log_decorator("[SERVICE]")
def add(a, b):
    return a + b

@log_decorator("[DEBUG]")
def multiply(a, b):
    return a * b

add(3, 5)
multiply(4, 7)

# --- 6.2 用闭包封装私有状态（模拟私有字段） ---
print("\n  6.2 闭包封装私有状态（模拟 OOP 私有字段）:")

def make_bank_account(owner, initial_balance=0):
    """模拟银行账户 —— 余额是私有的，只能通过方法访问

    【C# 等价】
    class BankAccount
    {
        private decimal _balance;  // 私有字段
        public decimal Deposit(decimal amount) { ... }
        public decimal Withdraw(decimal amount) { ... }
    }

    Python 没有 private 关键字，闭包是实现真正私有的一种方式
    """
    balance = initial_balance   # 外部无法直接访问

    def deposit(amount):
        nonlocal balance
        if amount <= 0:
            raise ValueError("存款金额必须为正")
        balance += amount
        print(f"    存入 {amount}，余额: {balance}")
        return balance

    def withdraw(amount):
        nonlocal balance
        if amount > balance:
            raise ValueError(f"余额不足: {balance} < {amount}")
        balance -= amount
        print(f"    取出 {amount}，余额: {balance}")
        return balance

    def get_balance():
        return balance

    def get_info():
        return f"账户 {owner}，余额 {balance}"

    # 返回所有操作方法（类似暴露公共 API）
    deposit.__name__ = f"{owner}.deposit"
    withdraw.__name__ = f"{owner}.withdraw"
    return deposit, withdraw, get_balance, get_info

deposit, withdraw, get_balance, get_info = make_bank_account("Alice", 1000)
deposit(500)
withdraw(200)
print(f"    查询: {get_info()}")

# 试图直接访问 balance —— 不可能！
print(f"    balance 变量从外部不可访问（真正的私有）")

# --- 6.3 用闭包实现工厂函数 ---
print("\n  6.3 闭包实现验证器工厂:")

def create_validator(validator_type):
    """验证器工厂 —— 根据类型返回不同的验证函数

    【C# 等价】
    Func<string, bool> CreateValidator(ValidatorType type)
    {
        return type switch
        {
            ValidatorType.Email => value => Regex.IsMatch(value, @"..."),
            ValidatorType.Phone => value => Regex.IsMatch(value, @"..."),
            _ => _ => false
        };
    }
    """
    if validator_type == "email":
        def validate(value):
            return "@" in value and "." in value
        return validate
    elif validator_type == "phone":
        def validate(value):
            return value.isdigit() and len(value) == 11
        return validate
    elif validator_type == "age":
        def validate(value):
            return isinstance(value, int) and 0 <= value <= 150
        return validate
    else:
        raise ValueError(f"未知的验证类型: {validator_type}")

email_validator = create_validator("email")
phone_validator = create_validator("phone")
age_validator = create_validator("age")

print(f"    'user@test.com' 是有效邮箱? {email_validator('user@test.com')}")
print(f"    'invalid' 是有效邮箱?      {email_validator('invalid')}")
print(f"    '13800138000' 是有效手机?   {phone_validator('13800138000')}")
print(f"    '123' 是有效手机?          {phone_validator('123')}")
print(f"    25 是有效年龄?             {age_validator(25)}")
print(f"    200 是有效年龄?            {age_validator(200)}")


# ============================================================================
# 7. 闭包 vs 类 vs Lambda 的选择指南
# ============================================================================

print("\n--- 7. 闭包 vs 类 vs Lambda ---")
print("""
  +-----------+------------------------+------------------------------------+
  | 特性      | 闭包                   | 类                                |
  +-----------+------------------------+------------------------------------+
  | 状态      | 通过 nonlocal 修改      | 通过 self.attribute 修改            |
  | 隐私      | 真正私有（外部不可访问） | 约定私有（_前缀或__name mangling） |
  | 代码量    | 少                      | 多（需要 __init__ 等）             |
  | 可读性    | 简单场景好，复杂场景差   | 复杂场景好                         |
  | 可测试性  | 差（无法单独测试内部函数）| 好（方法可独立测试）               |
  | 继承      | 不支持                  | 支持                               |
  +-----------+------------------------+------------------------------------+

  选择指南：
  - 简单状态 + 无继承 → 闭包（更简洁）
  - 复杂状态 + 需要测试 → 类（更规范）
  - 一次性操作 → lambda（更方便）
""")

print("=" * 70)
print("  总结：")
print("  - 闭包 = 内部函数 + 外部变量引用")
print("  - nonlocal 是修改外层变量的必要声明")
print("  - 循环闭包陷阱：捕获的是变量引用，不是值")
print("  - LEGB 规则：Local → Enclosing → Global → Built-in")
print("  - 闭包适合：装饰器、状态机、工厂函数、私有状态封装")
print("  - Python 闭包比 C# lambda 更强大（有 nonlocal 支持）")
print("=" * 70)
