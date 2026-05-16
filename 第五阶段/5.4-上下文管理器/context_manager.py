# =============================================================================
# Python 上下文管理器示例 — C# 老兵的 Python 修炼手册 5.4
# 对应文章：5.4 上下文管理器
# 关键概念：__enter__/__exit__, @contextlib.contextmanager,
#           ExitStack, async context manager
# =============================================================================
# 【C# vs Python 对比】
# C#: using (var resource = new Disposable()) { ... }
# Python: with ContextManager() as resource: ...
#
# 两者核心思想相同：确保资源的获取和释放配对执行
# C#: IDisposable.Dispose() ≈ Python: __exit__()
# C#: IAsyncDisposable.DisposeAsync() ≈ Python: __aexit__()
# =============================================================================

import time
from contextlib import contextmanager, ExitStack
from typing import IO


# =============================================================================
# 1. 类实现上下文管理器 —— __enter__ 和 __exit__
# =============================================================================
# 【C# 对比】
# C#:
#   public class Timer : IDisposable
#   {
#       private Stopwatch _sw = new Stopwatch();
#       public Timer() { _sw.Start(); }      // 对应 __enter__
#       public void Dispose() { _sw.Stop(); } // 对应 __exit__
#   }
#   using (var t = new Timer()) { ... }
#
# Python:
#   class Timer:
#       def __enter__(self): self.start = time.time(); return self
#       def __exit__(self, exc_type, exc_val, exc_tb): ...
#   with Timer() as t: ...


class Timer:
    """计时器上下文管理器 —— 对比 C# 的 IDisposable + using
    
    __enter__  → 进入 with 块时调用（对应 C# 构造函数/using 开始）
    __exit__   → 离开 with 块时调用（对应 C# Dispose）
    """
    def __enter__(self):
        """进入上下文——分配资源
        
        【C# 对比】对应 IDisposable 对象的创建和 using 语句的开始
        """
        self.start = time.perf_counter()
        self._entered = True
        return self  # 返回值绑定到 'as' 变量

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文——释放资源
        
        参数:
            exc_type: 异常类型（没有异常时为 None）
            exc_val: 异常值
            exc_tb: 异常追踪
        返回:
            True  = 吞掉异常（不向上传播）
            False = 继续传播异常
        
        【C# 对比】对应 Dispose() 方法，但 C# 的 Dispose 无法访问异常信息
        """
        elapsed = time.perf_counter() - self.start
        if exc_type is not None:
            print(f"  [Timer] 异常发生: {exc_type.__name__}: {exc_val}")
        print(f"  [Timer] 耗时: {elapsed:.4f}s")
        return False  # 不吞异常（与 C# Dispose 一样）


class FileManager:
    """文件管理器——演示资源获取和释放"""
    
    def __init__(self, filename: str, mode: str = "r"):
        self.filename = filename
        self.mode = mode
        self._file = None
    
    def __enter__(self):
        """打开文件"""
        # 【C# 对比】对应 using (var file = File.Open(...))
        self._file = open(self.filename, self.mode, encoding="utf-8")
        print(f"  [FileManager] 已打开: {self.filename}")
        return self._file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """关闭文件"""
        if self._file and not self._file.closed:
            self._file.close()
            print(f"  [FileManager] 已关闭: {self.filename}")
        # 返回 False，让异常继续传播
        return False


def demo_class_based():
    """演示类实现的上下文管理器"""
    print("\n=== 1. 类实现上下文管理器 (__enter__ / __exit__) ===")

    # 基本用法
    with Timer() as t:
        time.sleep(0.1)
        print(f"  Timer 对象: {t}")

    # 异常处理
    print("\n  异常场景:")
    try:
        with Timer():
            raise ValueError("模拟错误")
    except ValueError:
        print("  [主程序] 异常已捕获")

    # 文件管理器
    print("\n  文件操作:")
    # 创建临时文件供演示
    import tempfile
    import os
    tmp_file = os.path.join(tempfile.gettempdir(), "demo.txt")
    with open(tmp_file, "w") as f:
        f.write("Hello, Context Manager!")

    with FileManager(tmp_file, "r") as f:
        content = f.read()
        print(f"  读取内容: {content}")

    os.remove(tmp_file)


# =============================================================================
# 2. @contextmanager 装饰器 —— 更简洁的方式
# =============================================================================
# 【C# 对比】
# C# 没有直接对应的语法糖，需要实现完整的 IDisposable
# Python 的 @contextmanager 用生成器简化了上下文管理器的编写
#
# yield 之前的代码 = __enter__
# yield 的值     = as 绑定的变量
# yield 之后的代码 = __exit__
# 异常在 yield 处抛出


@contextmanager
def timer_decorator(label: str = "操作"):
    """用装饰器实现的计时器——对比 C# using 语句的简化版"""
    start = time.perf_counter()
    try:
        yield start  # yield 的值绑定到 as 变量
        # yield 之后是"正常退出"路径
    except Exception as e:
        # 捕获异常，做清理
        print(f"  [timer_decorator] 异常: {e}")
        raise  # 重新抛出，让调用者处理
    finally:
        # 无论如何都会执行
        elapsed = time.perf_counter() - start
        print(f"  [{label}] 耗时: {elapsed:.4f}s")


@contextmanager
def database_connection(connection_string: str):
    """模拟数据库连接——对比 C# using (var conn = new DbConnection(...))
    
    @contextmanager 的优势：
    1. 不需要定义 __enter__ 和 __exit__ 两个方法
    2. 用 try/finally 自然表达资源获取和释放
    3. yield 的值直接绑定到 as 变量
    """
    # __enter__ 部分: 获取资源
    print(f"  [DB] 连接到: {connection_string}")
    connection = {"connected": True, "string": connection_string}

    try:
        yield connection  # 返回连接对象
    except Exception as e:
        print(f"  [DB] 异常: {e}")
        raise
    finally:
        # __exit__ 部分: 释放资源
        connection["connected"] = False
        print(f"  [DB] 断开连接")


def demo_decorator_based():
    """演示 @contextmanager 装饰器"""
    print("\n=== 2. @contextmanager 装饰器 ===")

    # 基本用法
    with timer_decorator("sleep 操作"):
        time.sleep(0.1)

    # 获取 yield 的值
    with timer_decorator("计算操作") as start:
        result = sum(range(1_000_000))
        print(f"  计算结果: {result}")

    # 数据库连接
    print()
    with database_connection("Server=localhost;Database=test") as conn:
        print(f"  连接状态: {conn}")
        # 执行查询...
    print(f"  释放后: {conn}")

    print("  【C# 对比】C# 需要写完整的 class + IDisposable 接口")


# =============================================================================
# 3. ExitStack —— 动态管理多个上下文
# =============================================================================
# 【C# 对比】
# C# 没有直接对应——需要嵌套多个 using 或用 try-finally
# Python ExitStack 可以在运行时动态决定打开哪些资源
#
# 这是 Python 独有的强大功能，在处理不确定数量的资源时非常有用


def demo_exit_stack():
    """演示 ExitStack"""
    print("\n=== 3. ExitStack（动态管理多个上下文） ===")

    import tempfile
    import os

    # 创建临时文件列表
    tmp_files = []
    for i in range(3):
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, prefix=f"demo{i}_"
        )
        f.write(f"内容 {i}")
        f.close()
        tmp_files.append(f.name)

    # ExitStack 动态管理多个上下文
    # 【C# 对比】C# 没有直接对应，需要嵌套 using
    # C#:
    # using (var f1 = File.Open(...))
    # using (var f2 = File.Open(...))
    # using (var f3 = File.Open(...))
    # { ... }  // 嵌套深度 = 文件数量
    #
    # Python ExitStack 可以在循环中动态添加
    with ExitStack() as stack:
        files = []
        for path in tmp_files:
            f = stack.enter_context(open(path, "r"))
            files.append(f)

        # 所有文件都已打开
        for f in files:
            print(f"  {f.name}: {f.read().strip()}")

    # 所有文件都已自动关闭
    print("  所有文件已自动关闭")

    # 清理
    for path in tmp_files:
        os.remove(path)

    print("  【C# 对比】C# 嵌套 using 语句，无法动态管理")


# =============================================================================
# 4. 异步上下文管理器 —— 对比 C# IAsyncDisposable
# =============================================================================
# 【C# 对比】
# C# 8+:
#   public class AsyncResource : IAsyncDisposable
#   {
#       public async ValueTask DisposeAsync() { ... }
#   }
#   await using var resource = new AsyncResource();
#
# Python:
#   async with AsyncResource() as res:
#       await res.do_something()
#
# 两者都需要实现异步的资源获取和释放

import asyncio


class AsyncDatabase:
    """异步数据库连接——对比 C# IAsyncDisposable"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connected = False
    
    async def __aenter__(self):
        """异步进入上下文
        【C# 对比】对应构造函数或 InitializeAsync()
        """
        print(f"  [AsyncDB] 异步连接: {self.connection_string}")
        await asyncio.sleep(0.05)  # 模拟异步连接
        self.connected = True
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步退出上下文
        【C# 对比】对应 DisposeAsync()
        """
        print("  [AsyncDB] 异步断开连接")
        await asyncio.sleep(0.02)  # 模拟异步断开
        self.connected = False
        return False  # 不吞异常
    
    async def query(self, sql: str) -> list:
        """异步查询"""
        await asyncio.sleep(0.02)
        return [{"id": 1, "result": "ok"}]


@contextmanager
def async_cm_decorator():
    """用 @contextmanager 不支持异步——这是它的限制
    
    【C# 对比】C# 的 using 语句天然支持同步和异步
    Python 需要分别实现 __enter__/__exit__ 和 __aenter__/__aexit__
    """
    print("  [Sync CM] 同步上下文管理器")
    yield
    print("  [Sync CM] 清理完成")


async def demo_async_context_manager():
    """演示异步上下文管理器"""
    print("\n=== 4. 异步上下文管理器 (对比 C# IAsyncDisposable) ===")

    # 类实现的异步上下文管理器
    # 【C# 对比】await using var db = new AsyncDatabase("...");
    async with AsyncDatabase("Server=localhost;Database=test") as db:
        results = await db.query("SELECT * FROM users")
        print(f"  查询结果: {results}")
        print(f"  连接状态: {db.connected}")

    # 也可以组合使用
    print("\n  组合同步和异步上下文:")
    async with AsyncDatabase("另一个连接") as db:
        with Timer() as t:
            results = await db.query("SELECT 1")
            print(f"  结果: {results}")

    print("  【C# 对比】await using 是 C# 8+ 的内置语法")


# =============================================================================
# 5. 实际案例：事务管理器
# =============================================================================

@contextmanager
def transaction(connection_string: str):
    """模拟数据库事务——对比 C# 的 TransactionScope
    
    特性：
    - 正常结束时自动提交
    - 异常时自动回滚
    """
    print(f"  [Transaction] 开始事务 ({connection_string})")
    connection = {"connected": True, "in_transaction": True}

    try:
        yield connection
        # 正常结束——提交
        connection["in_transaction"] = False
        print("  [Transaction] 事务已提交")
    except Exception as e:
        # 异常——回滚
        connection["in_transaction"] = False
        print(f"  [Transaction] 事务已回滚 (原因: {e})")
        raise
    finally:
        connection["connected"] = False
        print("  [Transaction] 连接已关闭")


def demo_practical_examples():
    """实际案例演示"""
    print("\n=== 5. 实际案例：事务管理器 ===")

    # 正常事务
    print("  正常事务:")
    with transaction("Server=localhost") as conn:
        print(f"  执行: INSERT INTO users ...")
        print(f"  连接状态: {conn}")

    print()

    # 异常事务
    print("  异常事务:")
    try:
        with transaction("Server=localhost") as conn:
            print(f"  执行: INSERT INTO users ...")
            raise ValueError("模拟 SQL 错误")
    except ValueError as e:
        print(f"  [主程序] 捕获异常: {e}")

    print("  【C# 对比】C# TransactionScope 实现类似功能")


# =============================================================================
# 6. 上下文管理器的嵌套与组合
# =============================================================================

def demo_nesting():
    """演示上下文管理器的嵌套"""
    print("\n=== 6. 上下文管理器嵌套 ===")

    # Python 支持一行嵌套多个上下文
    # 【C# 对比】C# 需要嵌套多层 using
    # C#:
    # using (var a = new A())
    # using (var b = new B())
    # using (var c = new C())
    # { ... }
    #
    # Python:
    # with A() as a, B() as b, C() as c: ...
    # 或 Python 3.10+:
    # with (A() as a, B() as b, C() as c): ...

    import tempfile
    import os

    f1_path = os.path.join(tempfile.gettempdir(), "nest1.txt")
    f2_path = os.path.join(tempfile.gettempdir(), "nest2.txt")

    # 同时管理文件和计时器
    # Python 3.10+ 语法:
    with Timer() as t, open(f1_path, "w") as f1, open(f2_path, "w") as f2:
        f1.write("Hello from file 1")
        f2.write("Hello from file 2")
        print(f"  两个文件已写入")

    # 读取验证
    with open(f1_path) as f1, open(f2_path) as f2:
        print(f"  文件1: {f1.read()}")
        print(f"  文件2: {f2.read()}")

    os.remove(f1_path)
    os.remove(f2_path)

    print("  【C# 对比】C# 需要嵌套 using，Python 可以一行搞定")


# =============================================================================
# 主程序入口
# =============================================================================

def main():
    """运行所有演示"""
    print("=" * 60)
    print("  C# 老兵的 Python 修炼手册 — 5.4 上下文管理器")
    print("=" * 60)

    demo_class_based()
    demo_decorator_based()
    demo_exit_stack()
    asyncio.run(demo_async_context_manager())
    demo_practical_examples()
    demo_nesting()

    print("\n" + "=" * 60)
    print("  核心总结：")
    print("  1. Python with ≈ C# using，都是 RAII 模式")
    print("  2. __enter__/__exit__ ≈ IDisposable.Dispose")
    print("  3. @contextmanager 让编写更简洁（C# 没有等价物）")
    print("  4. ExitStack 支持动态资源管理（C# 没有等价物）")
    print("  5. async with ≈ await using (C# 8+)")
    print("  6. Python 支持一行嵌套多个上下文")
    print("=" * 60)


if __name__ == "__main__":
    main()
