# =============================================================================
# Python 异步编程示例 — C# 老兵的 Python 修炼手册 5.1
# 对应文章：5.1 async异步编程
# 关键概念：async/await, asyncio.gather, asyncio.create_task,
#           async context manager, async generator
# =============================================================================
# 【C# vs Python 对比】
# C# 的 async/await 由编译器生成状态机，Task 表示异步操作
# Python 的 async/await 基于事件循环（event loop），协程（coroutine）是核心
# C#: Task.WhenAll() ≈ Python: asyncio.gather()
# C#: async IAsyncEnumerable<T> ≈ Python: async generator (async def + yield)
# =============================================================================

import asyncio
import time

# =============================================================================
# 1. 基础异步函数 —— 对比 C# 的 async Task 方法
# =============================================================================
# C#: public static async Task<string> GetDataAsync(string url)
# Python: async def get_data(url: str) -> str

async def fetch_data(url: str, delay: float = 1.0) -> str:
    """模拟一个异步 HTTP 请求（用 asyncio.sleep 代替真实网络请求）
    
    【C# 对比】
    C#: await Task.Delay(1000);
    Python: await asyncio.sleep(1.0)
    
    两者都是让出控制权，不阻塞事件循环
    """
    print(f"  [开始] 请求 {url}")
    await asyncio.sleep(delay)  # 模拟网络 I/O，不阻塞线程
    print(f"  [完成] 请求 {url}")
    return f"来自 {url} 的数据"


# =============================================================================
# 2. asyncio.gather() —— 并发执行多个协程
# =============================================================================
# 【C# 对比】
# C#: await Task.WhenAll(task1, task2, task3);
# Python: await asyncio.gather(coroutine1(), coroutine2(), coroutine3())
#
# 关键区别：
# - C# 的 Task 是对象，可以提前创建并传递
# - Python 的协程必须在事件循环运行时创建，不能提前"启动"

async def demo_gather():
    """演示 asyncio.gather 并发执行"""
    print("\n=== 2. asyncio.gather 并发执行 ===")
    start = time.perf_counter()

    # gather 会并发运行所有协程，等全部完成
    # 【C# 对比】类似 Task.WhenAll
    results = await asyncio.gather(
        fetch_data("api/users", delay=1.0),
        fetch_data("api/orders", delay=1.5),
        fetch_data("api/products", delay=0.8),
    )

    elapsed = time.perf_counter() - start
    print(f"  所有结果: {results}")
    print(f"  总耗时: {elapsed:.2f}s (并发执行，最慢的那个决定总耗时)")


# =============================================================================
# 3. asyncio.create_task() —— 更精细的并发控制
# =============================================================================
# 【C# 对比】
# C#: var task = Task.Run(() => DoWork());
#      // task 已经在后台运行
#      await task;  // 等待结果
#
# Python: task = asyncio.create_task(coro())
#         // 注意：协程此刻才被调度到事件循环
#         result = await task

async def demo_create_task():
    """演示 create_task 与 gather 的区别"""
    print("\n=== 3. asyncio.create_task 精细控制 ===")

    # 创建 task 对象——此时协程被安排执行，但尚未 await
    task1 = asyncio.create_task(fetch_data("后台任务A", delay=1.0))
    task2 = asyncio.create_task(fetch_data("后台任务B", delay=0.5))

    # 在等待期间可以做其他事
    print("  [主线程] task 已创建，正在做其他工作...")
    await asyncio.sleep(0.1)

    # 然后再 await 获取结果
    result1 = await task1
    result2 = await task2
    print(f"  结果1: {result1}")
    print(f"  结果2: {result2}")


# =============================================================================
# 4. 异步生成器 —— 对比 C# 的 IAsyncEnumerable<T>
# =============================================================================
# 【C# 对比】
# C# 8+:
#   public static async IAsyncEnumerable<int> GenerateAsync()
#   {
#       for (int i = 0; i < 10; i++)
#       {
#           await Task.Delay(100);
#           yield return i;
#       }
#   }
#   await foreach (var item in GenerateAsync()) { ... }
#
# Python:
#   async def generate():
#       for i in range(10):
#           await asyncio.sleep(0.1)
#           yield i
#   async for item in generate(): ...

async def async_range(start: int, stop: int, delay: float = 0.1):
    """异步生成器：逐个产出数据，每次间隔 delay 秒
    
    注意 Python 用 'async def' + 'yield' 定义异步生成器
    """
    for i in range(start, stop):
        await asyncio.sleep(delay)
        yield i  # yield 使函数变成生成器；async def 使其异步


async def demo_async_generator():
    """演示异步生成器的使用"""
    print("\n=== 4. 异步生成器 (对比 C# IAsyncEnumerable<T>) ===")

    # async for 逐个消费异步生成器
    # 【C# 对比】await foreach (var item in asyncRange) { ... }
    print("  使用 async for 逐个获取:")
    async for num in async_range(1, 6, delay=0.05):
        print(f"    收到: {num}")

    # 异步生成器推导式（类似列表推导式）
    results = [num async for num in async_range(1, 6, delay=0.02)]
    print(f"  异步推导式结果: {results}")


# =============================================================================
# 5. 异步上下文管理器 —— 对比 C# 的 IAsyncDisposable
# =============================================================================
# 【C# 对比】
# C# 8+:
#   await using var resource = new AsyncResource();
#   // 使用资源
#   // 离开作用域自动调用 DisposeAsync()
#
#   public class AsyncResource : IAsyncDisposable
#   {
#       public async ValueTask DisposeAsync() { ... }
#   }
#
# Python:
#   async with AsyncResource() as res:
#       # 使用资源
#   # 自动调用 __aexit__

class AsyncDatabase:
    """模拟异步数据库连接（对比 C# 的 IAsyncDisposable）"""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connected = False

    async def __aenter__(self):
        """异步进入上下文——对应 C# 构造函数或 InitializeAsync"""
        print(f"  [AsyncDB] 正在连接: {self.connection_string}")
        await asyncio.sleep(0.1)  # 模拟连接耗时
        self.connected = True
        print("  [AsyncDB] 连接成功")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步退出上下文——对应 C# 的 DisposeAsync"""
        print("  [AsyncDB] 正在断开连接...")
        await asyncio.sleep(0.05)
        self.connected = False
        print("  [AsyncDB] 已断开")
        return False  # 返回 False 表示不吞掉异常（True 会吞掉）

    async def query(self, sql: str) -> list:
        """模拟异步查询"""
        await asyncio.sleep(0.05)
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]


async def demo_async_context_manager():
    """演示异步上下文管理器"""
    print("\n=== 5. 异步上下文管理器 (对比 C# IAsyncDisposable) ===")

    # 【C# 对比】await using var db = new AsyncDatabase("...");
    async with AsyncDatabase("Server=localhost;Database=test") as db:
        results = await db.query("SELECT * FROM users")
        print(f"  查询结果: {results}")
    # 离开 async with 块，自动调用 __aexit__


# =============================================================================
# 6. 异步错误处理与超时
# =============================================================================

async def demo_error_handling():
    """演示异步中的错误处理"""
    print("\n=== 6. 异步错误处理 ===")

    # asyncio.wait_for —— 设置超时
    # 【C# 对比】var cts = new CancellationTokenSource(TimeSpan.FromSeconds(2));
    #             await task.WaitAsync(cts.Token);
    try:
        result = await asyncio.wait_for(
            fetch_data("慢接口", delay=5.0),
            timeout=1.0  # 1秒超时
        )
    except asyncio.TimeoutError:
        print("  [超时] 请求超过1秒，已取消")

    # asyncio.gather 的 return_exceptions 参数
    # 【C# 对比】类似 Task.WhenAll + try-catch each
    results = await asyncio.gather(
        fetch_data("成功接口", delay=0.1),
        failing_task(),
        return_exceptions=True,  # 异常作为结果返回，不中断其他任务
    )
    for i, r in enumerate(results):
        if isinstance(r, Exception):
            print(f"  任务{i} 失败: {r}")
        else:
            print(f"  任务{i} 成功: {r}")


async def failing_task():
    """一个必定失败的异步任务"""
    await asyncio.sleep(0.1)
    raise ValueError("模拟异步错误")


# =============================================================================
# 7. 模拟 aiohttp 用法（演示模式，不依赖外部库）
# =============================================================================

class MockResponse:
    """模拟 aiohttp 的响应对象"""
    def __init__(self, text: str, status: int = 200):
        self._text = text
        self.status = status

    async def text(self) -> str:
        return self._text

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass  # 不需要关闭


class MockSession:
    """模拟 aiohttp.ClientSession"""
    def get(self, url: str) -> MockResponse:
        # 注意: aiohttp 的 session.get() 返回一个 async context manager
        # 这里简化为直接返回 MockResponse（已经实现了 __aenter__/__aexit__）
        return MockResponse(f"数据来自 {url}")

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        print("  [Session] 已关闭")


async def demo_aiohttp_pattern():
    """演示 aiohttp 的使用模式（用 mock 模拟，无需安装 aiohttp）
    
    【C# 对比】
    C#: using var client = new HttpClient();
        var response = await client.GetStringAsync(url);
    Python: async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.text()
    """
    print("\n=== 7. aiohttp 使用模式 (Mock) ===")

    async with MockSession() as session:
        async with session.get("https://api.example.com/data") as response:
            data = await response.text()
            print(f"  状态码: {response.status}")
            print(f"  响应: {data}")


# =============================================================================
# 主程序入口
# =============================================================================

async def main():
    """运行所有异步演示
    
    【C# 对比】
    C#: static async Task Main() { await DemoAllAsync(); }
    Python: asyncio.run(main())
    """
    print("=" * 60)
    print("  C# 老兵的 Python 修炼手册 — 5.1 异步编程")
    print("=" * 60)

    await demo_gather()
    await demo_create_task()
    await demo_async_generator()
    await demo_async_context_manager()
    await demo_error_handling()
    await demo_aiohttp_pattern()

    print("\n" + "=" * 60)
    print("  所有异步演示完成！")
    print("  关键区别: C# Task 是热启动(hot)，Python 协程是冷启动(cold)")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
