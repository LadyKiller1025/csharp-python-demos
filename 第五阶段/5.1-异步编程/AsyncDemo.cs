// =============================================================================
// C# 异步编程示例 — C# 老兵的 Python 修炼手册 5.1
// 对应文章：5.1 async异步编程
// 关键概念：async/await, Task.WhenAll, Task.Run,
//           IAsyncEnumerable<T>, IAsyncDisposable
// =============================================================================
// 【C# vs Python 对比】
// C# 的 async/await 由编译器生成状态机（IAsyncStateMachine）
// Python 的 async/await 基于事件循环（event loop），协程是核心
// C#: Task.WhenAll() ≈ Python: asyncio.gather()
// C#: IAsyncEnumerable<T> ≈ Python: async generator (async def + yield)
// =============================================================================

using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;

namespace AsyncDemo
{
    public static class AsyncExamples
    {
        private static readonly HttpClient _client = new HttpClient();

        // =========================================================================
        // 1. 基础异步方法 —— 对比 Python 的 async def
        // =========================================================================
        // Python:
        //   async def fetch_data(url: str, delay: float = 1.0) -> str:
        //       await asyncio.sleep(delay)
        //       return f"data from {url}"
        //
        // C#: async 关键字 + Task<T> 返回类型，编译器自动生成状态机

        /// <summary>
        /// 模拟异步 HTTP 请求
        /// 【Python 对比】async def fetch_data(url, delay=1.0) -> str
        /// </summary>
        public static async Task<string> FetchDataAsync(string url, int delayMs = 1000)
        {
            Console.WriteLine($"  [开始] 请求 {url}");
            await Task.Delay(delayMs);  // 不阻塞线程，仅让出控制权
            Console.WriteLine($"  [完成] 请求 {url}");
            return $"来自 {url} 的数据";
        }

        // =========================================================================
        // 2. Task.WhenAll —— 并发执行多个异步任务
        // =========================================================================
        // 【Python 对比】
        // Python: results = await asyncio.gather(coro1(), coro2(), coro3())
        // C#:     var results = await Task.WhenAll(task1, task2, task3);
        //
        // 关键区别:
        // - C# Task 创建后立即在线程池上开始执行（热启动）
        // - Python 协程需要 await 或 create_task 才会被调度（冷启动）

        /// <summary>
        /// 演示 Task.WhenAll 并发执行
        /// </summary>
        public static async Task DemoWhenAllAsync()
        {
            Console.WriteLine("\n=== 2. Task.WhenAll 并发执行 ===");
            var sw = System.Diagnostics.Stopwatch.StartNew();

            // 创建三个异步任务
            var task1 = FetchDataAsync("api/users", 1000);
            var task2 = FetchDataAsync("api/orders", 1500);
            var task3 = FetchDataAsync("api/products", 800);

            // WhenAll 等待所有任务完成
            string[] results = await Task.WhenAll(task1, task2, task3);

            sw.Stop();
            Console.WriteLine($"  所有结果: [{string.Join(", ", results)}]");
            Console.WriteLine($"  总耗时: {sw.ElapsedMilliseconds}ms (并发执行)");
        }

        // =========================================================================
        // 3. Task.Run + 精细控制 —— 对比 Python 的 create_task
        // =========================================================================
        // 【Python 对比】
        // Python:
        //   task = asyncio.create_task(fetch_data("url"))
        //   # 做其他事...
        //   result = await task
        //
        // C#:
        //   var task = FetchDataAsync("url");
        //   // 做其他事（task 已经在后台运行）
        //   string result = await task;
        //
        // 两者相似：创建后立即开始执行，之后再 await 获取结果

        /// <summary>
        /// 演示任务的精细控制
        /// </summary>
        public static async Task DemoCreateTaskAsync()
        {
            Console.WriteLine("\n=== 3. Task 精细控制 ===");

            // Task 在创建时就开始执行（与 Python create_task 类似）
            Task<string> task1 = FetchDataAsync("后台任务A", 1000);
            Task<string> task2 = FetchDataAsync("后台任务B", 500);

            Console.WriteLine("  [主线程] task 已创建，正在做其他工作...");
            await Task.Delay(100);  // 模拟主线程的其他工作

            // 等待并获取结果
            string result1 = await task1;
            string result2 = await task2;
            Console.WriteLine($"  结果1: {result1}");
            Console.WriteLine($"  结果2: {result2}");
        }

        // =========================================================================
        // 4. 异步迭代器 IAsyncEnumerable<T> —— 对比 Python async generator
        // =========================================================================
        // 【Python 对比】
        // Python:
        //   async def async_range(start, stop, delay=0.1):
        //       for i in range(start, stop):
        //           await asyncio.sleep(delay)
        //           yield i
        //
        //   async for num in async_range(1, 6):
        //       print(num)
        //
        // C# 8+: 使用 IAsyncEnumerable<T> + await foreach

        /// <summary>
        /// 异步生成器：逐个产出数据
        /// 【Python 对比】async def async_range(start, stop, delay): ... yield i
        /// </summary>
        public static async IAsyncEnumerable<int> GenerateNumbersAsync(
            int start, int stop, int delayMs = 100)
        {
            for (int i = start; i < stop; i++)
            {
                await Task.Delay(delayMs);  // 模拟异步操作
                yield return i;  // 产出一个值
            }
        }

        /// <summary>
        /// 演示异步迭代器
        /// </summary>
        public static async Task DemoAsyncEnumerableAsync()
        {
            Console.WriteLine("\n=== 4. IAsyncEnumerable<T> (对比 Python async generator) ===");

            // await foreach 逐个消费异步流
            // 【Python 对比】async for num in async_range(1, 6): ...
            Console.WriteLine("  使用 await foreach 逐个获取:");
            await foreach (int num in GenerateNumbersAsync(1, 6, 50))
            {
                Console.WriteLine($"    收到: {num}");
            }
        }

        // =========================================================================
        // 5. 异步上下文管理器 IAsyncDisposable —— 对比 Python async with
        // =========================================================================
        // 【Python 对比】
        // Python:
        //   async with AsyncDatabase("conn_str") as db:
        //       results = await db.query("SELECT ...")
        //
        // C# 8+:
        //   await using var db = new AsyncDatabase("conn_str");
        //   var results = await db.QueryAsync("SELECT ...");

        /// <summary>
        /// 异步资源管理——实现 IAsyncDisposable
        /// 【Python 对比】实现 __aenter__ 和 __aexit__ 方法
        /// </summary>
        public class AsyncDatabase : IAsyncDisposable
        {
            private readonly string _connectionString;
            private bool _connected;

            public AsyncDatabase(string connectionString)
            {
                _connectionString = connectionString;
            }

            /// <summary>
            /// 异步初始化
            /// 【Python 对比】__aenter__ 方法
            /// </summary>
            public async Task<AsyncDatabase> ConnectAsync()
            {
                Console.WriteLine($"  [AsyncDB] 正在连接: {_connectionString}");
                await Task.Delay(100);  // 模拟连接耗时
                _connected = true;
                Console.WriteLine("  [AsyncDB] 连接成功");
                return this;
            }

            public async Task<List<string>> QueryAsync(string sql)
            {
                if (!_connected) throw new InvalidOperationException("未连接数据库");
                await Task.Delay(50);
                return new List<string> { "Alice", "Bob" };
            }

            /// <summary>
            /// 异步释放资源
            /// 【Python 对比】__aexit__ 方法
            /// </summary>
            public async ValueTask DisposeAsync()
            {
                Console.WriteLine("  [AsyncDB] 正在断开连接...");
                await Task.Delay(50);
                _connected = false;
                Console.WriteLine("  [AsyncDB] 已断开");
            }
        }

        /// <summary>
        /// 演示异步上下文管理器
        /// </summary>
        public static async Task DemoAsyncDisposableAsync()
        {
            Console.WriteLine("\n=== 5. IAsyncDisposable (对比 Python async with) ===");

            // C# 8+ using 声明 + await using
            // 【Python 对比】async with AsyncDatabase(...) as db:
            var db = new AsyncDatabase("Server=localhost;Database=test");
            await using (db.ConfigureAwait(false))
            {
                await db.ConnectAsync();
                var results = await db.QueryAsync("SELECT * FROM users");
                Console.WriteLine($"  查询结果: [{string.Join(", ", results)}]");
            }
            // 离开 await using 块，自动调用 DisposeAsync()
        }

        // =========================================================================
        // 6. 异步错误处理与取消
        // =========================================================================

        /// <summary>
        /// 演示异步超时处理
        /// 【Python 对比】asyncio.wait_for(coro, timeout=1.0)
        /// </summary>
        public static async Task DemoErrorHandlingAsync()
        {
            Console.WriteLine("\n=== 6. 异步错误处理 ===");

            // 超时处理
            // 【Python 对比】asyncio.wait_for(coro, timeout=1.0)
            using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(1));
            try
            {
                string result = await FetchDataAsync("慢接口", 5000)
                    .WaitAsync(cts.Token);  // .NET 8+
                Console.WriteLine($"  结果: {result}");
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("  [超时] 请求超过1秒，已取消");
            }

            // Task.WhenAll + 逐个处理异常
            // 【Python 对比】asyncio.gather(..., return_exceptions=True)
            var tasks = new[]
            {
                FetchDataAsync("成功接口", 100),
                Task.FromException<string>(new InvalidOperationException("模拟错误"))
            };

            var results = await Task.WhenAll(tasks);
            for (int i = 0; i < results.Length; i++)
            {
                try
                {
                    Console.WriteLine($"  任务{i} 成功: {results[i]}");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"  任务{i} 失败: {ex.Message}");
                }
            }
        }

        // =========================================================================
        // 7. 实际 HttpClient 用法
        // =========================================================================

        /// <summary>
        /// 演示 HttpClient 的异步用法
        /// 【Python 对比】
        /// async with aiohttp.ClientSession() as session:
        ///     async with session.get(url) as response:
        ///         return await response.text()
        /// </summary>
        public static async Task DemoHttpClientAsync()
        {
            Console.WriteLine("\n=== 7. HttpClient 用法 (对比 aiohttp) ===");

            try
            {
                // C# 的 HttpClient 是内置的，Python 需要第三方库 aiohttp
                string data = await _client.GetStringAsync("https://httpbin.org/get")
                    .WaitAsync(CancellationToken.None);
                Console.WriteLine($"  获取到 {data.Length} 字符");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  请求失败 (网络不可用时正常): {ex.GetType().Name}");
            }
        }
    }

    // =========================================================================
    // 主程序入口
    // =========================================================================
    class Program
    {
        /// <summary>
        /// 程序入口
        /// 【Python 对比】asyncio.run(main())
        /// </summary>
        static async Task Main(string[] args)
        {
            Console.WriteLine("============================================================");
            Console.WriteLine("  C# 老兵的 Python 修炼手册 — 5.1 异步编程");
            Console.WriteLine("============================================================");

            await AsyncExamples.DemoWhenAllAsync();
            await AsyncExamples.DemoCreateTaskAsync();
            await AsyncExamples.DemoAsyncEnumerableAsync();
            await AsyncExamples.DemoAsyncDisposableAsync();
            await AsyncExamples.DemoErrorHandlingAsync();
            await AsyncExamples.DemoHttpClientAsync();

            Console.WriteLine("\n============================================================");
            Console.WriteLine("  所有异步演示完成！");
            Console.WriteLine("  关键区别: C# Task 是热启动(hot)，Python 协程是冷启动(cold)");
            Console.WriteLine("============================================================");
        }
    }
}
