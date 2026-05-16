# ============================================================================
# Python 装饰器（Decorator）
# 对应文章：2.5 装饰器
# ============================================================================
#
# 【C# 程序员的 Python 修炼手册】
#
# 装饰器 = Python 版的 Attribute / 中间件 / AOP（面向切面编程）
#
# 核心思想：不修改原函数代码，给函数"套上"额外功能
#
# | C# 概念            | Python 等价             | 说明                      |
# |--------------------|-------------------------|---------------------------|
# | [Attribute]        | @decorator              | 元数据标注 / 函数包装      |
# | Action Filter      | @decorator（函数式）     | ASP.NET Core 请求拦截      |
# | 中间件 Middleware   | @decorator（栈式）       | 请求管道                   |
# | AOP 拦截器         | @decorator              | 方法前后的横切逻辑         |
# | partial class      | 类装饰器 class Decorator | 用类实现装饰器             |
#
# 关键区别：
# - C# Attribute 本质是元数据，需要反射/框架才能生效
# - Python 装饰器本质是函数包装，@ 语法糖在定义时就生效
# - Python 装饰器更灵活，但也更容易滥用
# ============================================================================

import time
import random
from functools import wraps


# ============================================================================
# 1. 最简单的装饰器 —— @timer（无括号版本）
# ============================================================================
#
# 【C# 对比】
# C# 中没有等价的无参数装饰器语法。
# C# 的 [MyAttribute] 相当于 Python 的 @my_decorator（不带括号）
#
# 什么时候用 @timer（不带括号）？
# 当装饰器只需要接收被装饰函数本身，不需要额外参数时

def timer(func):
    """
    计时装饰器：测量函数执行时间

    【为什么用 @wraps(func)？】
    没有 @wraps 时，装饰后的函数会"丢失"原函数的名字和文档：
      - __name__  变成 "wrapper" 而不是原函数名
      - __doc__   变成 wrapper 的文档而不是原函数的
      - __module__ 和其他元信息也会丢失

    这在调试和框架反射时会出大问题！
    假装你有一个被 @timer 装饰的函数叫 slow_query()，
    没有 @wraps 的话，错误日志会显示 "wrapper() failed"，
    你根本不知道是哪个函数出了问题。

    【C# 对比】
    C# 的 Attribute 不需要考虑这个问题，因为它不包装函数本身，
    只是给方法贴了个"标签"，方法还是原来的方法。
    但这也意味着 C# Attribute 无法像 Python 装饰器那样灵活地修改函数行为。
    """
    @wraps(func)  # 关键！保留原函数的 __name__, __doc__, __module__ 等
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"  [timer] {func.__name__} 执行完成，耗时: {elapsed:.4f}秒")
        return result
    return wrapper


# ============================================================================
# 2. 带参数的装饰器 —— @cache, @retry, @require_role
# ============================================================================
#
# 【C# 对比】
# 带参数的装饰器 ≈ C# Attribute 带构造函数参数
#   [Cache(DurationSeconds = 300)]
#   [Authorize(Roles = "Admin")]
#
# 但 Python 装饰器参数可以是任意表达式，比 C# Attribute 灵活得多
#
# 结构理解（三层嵌套）：
#   def decorator_with_args(arg):     # 第1层：接收装饰器参数
#       def decorator(func):          # 第2层：接收被装饰函数
#           @wraps(func)
#           def wrapper(*a, **kw):    # 第3层：实际执行的包装函数
#               ...
#           return wrapper
#       return decorator
#   return decorator

def cache(maxsize=128):
    """缓存装饰器：记忆函数结果，避免重复计算

    【C# 对比】
    等价于 [MemoryCache] 或 [Cached] 属性
    也等价于 System.Runtime.CompilerServices caching 特性
    """
    def decorator(func):
        cache_dict = {}  # 闭包捕获的缓存字典

        @wraps(func)
        def wrapper(*args):
            if args in cache_dict:
                print(f"  [cache] {func.__name__}{args} 命中缓存！")
                return cache_dict[args]
            result = func(*args)
            cache_dict[args] = result
            return result

        # 暴露缓存信息（方便调试）
        wrapper.cache_info = lambda: f"缓存大小: {len(cache_dict)}"
        wrapper.cache_clear = lambda: cache_dict.clear()
        return wrapper
    return decorator


def retry(max_attempts=3, delay=0.1):
    """重试装饰器：函数失败时自动重试

    【C# 对比】
    等价于 Polly 的 RetryPolicy
      Policy.Handle<Exception>()
            .Retry(3, (ex, i) => Console.WriteLine($"Retry {i}"))
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts:
                        print(f"  [retry] 第{attempt}次尝试失败: {e}，{delay}秒后重试...")
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator


def require_role(role):
    """权限检查装饰器：调用前检查用户角色

    【C# 对比】
    等价于 [Authorize(Roles = "Admin")]
    也等价于 ASP.NET Core 的 [Authorize] + Policy-based 鉴权
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.pop('user', None)
            if not user:
                raise PermissionError(f"[require_role] 缺少用户信息，需要 {role} 角色")
            if role not in user.get('roles', []):
                raise PermissionError(
                    f"[require_role] 用户 '{user.get('name')}' 无 {role} 角色，"
                    f"当前角色: {user.get('roles', [])}"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ============================================================================
# 3. 装饰器堆叠（Stacking Decorators）
# ============================================================================
#
# 【C# 对比】
# C# 也可以堆叠 Attribute：
#   [Log("入口")]
#   [Cache(DurationSeconds = 60)]
#   [Authorize(Roles = "Admin")]
#   public void MyMethod() { ... }
#
# 执行顺序（从下往上应用，从外往内执行）：
#   @A       →    @B(func)    →  A(B(func))
#   @B
#   def func        先包装 B，再包装 A
#
# 调用时：A.wrapper → B.wrapper → func

@timer                          # 最外层，最后包装，最先执行
def heavy_computation(n):
    """一个耗时的计算函数"""
    time.sleep(0.1)
    return sum(range(n))


# ============================================================================
# 4. 类装饰器 —— Python 版的 C# Attribute / IMethodInterceptor
# ============================================================================
#
# 【C# 对比】
# 这是最接近 C# Attribute 的实现方式！
# 在 C# 中我们写：
#   [Log("开始")]
#   [Cache(Duration = 60)]
#   public void MyMethod() { ... }
#
# Python 类装饰器 vs 函数装饰器：
# - 类装饰器：可以维护状态，更接近 C# 的 class-based Attribute
# - 函数装饰器：更简洁，大多数场景够用
#
# 真正的 C# Attribute 是元数据+反射，运行时需要框架（如 ASP.NET）读取
# Python 类装饰器在 @ 语法糖处理时就直接替换函数了

class CountCalls:
    """统计函数被调用次数的类装饰器

    【C# 对比】
    类似 C# 的 ICallCounter + Autofac 注入
    但 Python 的类装饰器更直接：直接包装函数并替换
    """
    def __init__(self, func):
        wraps(func)(self)           # 把原函数的元信息复制到实例上
        self.func = func
        self.call_count = 0

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        print(f"  [CountCalls] {self.func.__name__} 第{self.call_count}次调用")
        return self.func(*args, **kwargs)

    def get_stats(self):
        return f"{self.func.__name__} 已被调用 {self.call_count} 次"


# ============================================================================
# 5. 访问被包装的原始函数 —— func.__wrapped__
# ============================================================================
#
# 装饰器堆叠后，有时候我们需要绕过装饰器直接调用原函数
# Python 在 @wraps 中自动提供了 __wrapped__ 属性
#
# 【C# 对比】
# C# 没有直接等价物，但类似的设计模式：
# - Decorator Pattern 中保留原始对象的引用
# - DI 中注册原服务和装饰后的服务
# - Autofac 的 .AsSelf() / .As<T>() 注册

def debug(func):
    """调试装饰器：打印函数入参和返回值"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  [debug] 调用 {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"  [debug] 返回 {result}")
        return result
    return wrapper


# ============================================================================
# 6. 定义被装饰的函数
# ============================================================================

@timer
def slow_function():
    """模拟一个耗时操作"""
    time.sleep(0.5)
    return "完成"


@cache(maxsize=128)
def fibonacci(n):
    """斐波那契数列 —— 递归 + 缓存的经典组合"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@retry(max_attempts=3, delay=0.1)
def unreliable_function():
    """模拟一个不稳定的网络调用"""
    if random.random() < 0.7:  # 70% 概率失败
        raise ConnectionError("网络连接超时")
    return "调用成功"


@require_role("Admin")
def delete_user(user_id):
    """删除用户 —— 需要 Admin 角色"""
    print(f"  已删除用户 {user_id}")
    return True


# ---- 堆叠装饰器示例 ----
@debug                          # 先打印调用信息
@timer                          # 再统计耗时（最内层）
def compute_sum(n):
    """计算 1 到 n 的和"""
    return sum(range(1, n + 1))


# ---- 类装饰器示例 ----
@CountCalls
def greet(name):
    """打招呼"""
    print(f"  Hello, {name}!")
    return f"greeted {name}"


# ============================================================================
# 主程序：演示所有装饰器效果
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  Python 装饰器（Decorator）演示")
    print("  C# 程序员的 Python 修炼手册 —— 2.5")
    print("=" * 70)

    # --- 1. @timer 无括号装饰器 ---
    print("\n--- 1. @timer（无括号装饰器）---")
    print("  说明: @timer 不带括号，直接接收函数作为参数")
    print("  C# 等价: 没有直接等价物，C# Attribute 始终需要 [] 语法\n")
    result = slow_function()
    print(f"  返回值: {result}")

    # 演示 @wraps 的效果
    print(f"\n  slow_function.__name__ = '{slow_function.__name__}'")
    print(f"  (没有 @wraps 的话这里会显示 'wrapper')")

    # --- 2. @cache 缓存装饰器 ---
    print("\n--- 2. @cache（带参数的缓存装饰器）---")
    print("  说明: @cache(maxsize=128) 带参数，需要三层嵌套")
    print("  C# 等价: [MemoryCache] 或 Polly 缓存策略\n")
    print(f"  fibonacci(10) = {fibonacci(10)}")
    print(f"  fibonacci(20) = {fibonacci(20)}")
    print(f"  {fibonacci.cache_info()}")

    # --- 3. @retry 重试装饰器 ---
    print("\n--- 3. @retry（重试装饰器）---")
    print("  说明: 失败时自动重试，C# 等价: Polly RetryPolicy\n")
    try:
        result = unreliable_function()
        print(f"  最终结果: {result}")
    except Exception as e:
        print(f"  最终失败: {e}")

    # --- 4. @require_role 权限装饰器 ---
    print("\n--- 4. @require_role（权限检查装饰器）---")
    print("  说明: C# 等价: [Authorize(Roles = \"Admin\")]\n")

    # 正确权限
    admin_user = {"name": "张三", "roles": ["Admin", "Editor"]}
    print("  尝试用 Admin 用户删除...")
    delete_user(42, user=admin_user)

    # 错误权限
    viewer_user = {"name": "李四", "roles": ["Viewer"]}
    print("\n  尝试用 Viewer 用户删除...")
    try:
        delete_user(42, user=viewer_user)
    except PermissionError as e:
        print(f"  权限不足: {e}")

    # --- 5. 装饰器堆叠 ---
    print("\n--- 5. 装饰器堆叠（Stacking Decorators）---")
    print("  @debug + @timer 同时应用在一个函数上")
    print("  执行顺序: debug.wrapper → timer.wrapper → compute_sum\n")
    result = compute_sum(1000)
    print(f"  结果: {result}")

    # --- 6. 类装饰器（C# Attribute 等价物）---
    print("\n--- 6. 类装饰器 CountCalls（C# Attribute 等价物）---")
    print("  说明: 这是最接近 C# [Attribute] 的 Python 实现方式\n")
    greet("Alice")
    greet("Bob")
    greet("Charlie")
    print(f"  统计: {greet.get_stats()}")

    # --- 7. 访问被包装的原始函数 ---
    print("\n--- 7. 访问被包装的原始函数（__wrapped__）---")
    print("  说明: 有时需要绕过装饰器，直接调用原函数\n")

    # 通过 __wrapped__ 跳过 @timer 直接调用
    print("  通过 slow_function.__wrapped__() 调用（不经过 timer）:")
    # 直接调用原函数，不会打印计时信息
    raw_start = time.time()
    raw_result = slow_function.__wrapped__()
    raw_elapsed = time.time() - raw_start
    print(f"  原始函数返回: {raw_result}，手动计时: {raw_elapsed:.4f}秒")

    print("\n" + "=" * 70)
    print("  总结：")
    print("  - @wraps 是装饰器的必备操作，保留函数元信息")
    print("  - 带参数的装饰器需要三层嵌套")
    print("  - 装饰器堆叠从下往上包装，从外往内执行")
    print("  - 类装饰器最接近 C# Attribute 的理念")
    print("  - __wrapped__ 可以绕过装饰器访问原始函数")
    print("  - Python 装饰器比 C# Attribute 更灵活，但需要自律")
    print("=" * 70)
