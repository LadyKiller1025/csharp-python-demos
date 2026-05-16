// =============================================================================
// C# 多线程示例 — C# 老兵的 Python 修炼手册 5.2
// 对应文章：5.2 多线程与GIL
// 关键概念：Task, Thread, ThreadPool, async, Parallel,
//           无 GIL 的真正并行
// =============================================================================
// 【C# vs Python 对比 — 最大的差异之一】
//
// C# 没有 GIL（全局解释器锁），线程可以真正并行执行 CPU 密集型任务
// Python 有 GIL，同一时刻只有一个线程执行 Python 字节码
//
// 这意味着 C# 在多线程方面天然强于 Python：
// - C# Task.Run 即可利用多核
// - Python 需要 multiprocessing 才能绕过 GIL
// =============================================================================

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace ThreadDemo
{
    public static class ThreadExamples
    {
        private static int _counter = 0;
        private static readonly object _lockObj = new object();

        // =========================================================================
        // 1. C# 没有 GIL —— 线程可以真正并行
        // =========================================================================
        // 【Python 对比】
        // Python 的 threading 受 GIL 限制，CPU 密集型任务无法加速
        // C# 的线程由 CLR 管理，每个线程可以独立执行 JIT 编译的机器码

        /// <summary>
        /// 无锁原子操作
        /// 【Python 对比】需要 threading.Lock() 手动加锁
        /// C# 的 Interlocked 类提供原子操作，不需要锁
        /// </summary>
        public static void IncrementWithInterlocked()
        {
            for (int i = 0; i < 1_000_000; i++)
            {
                Interlocked.Increment(ref _counter);
            }
        }

        /// <summary>
        /// 使用 lock 语句
        /// 【Python 对比】with threading.Lock(): counter += 1
        /// </summary>
        public static void IncrementWithLock()
        {
            for (int i = 0; i < 1_000_000; i++)
            {
                lock (_lockObj)
                {
                    _counter++;
                }
            }
        }

        /// <summary>
        /// 演示线程安全的并发递增
        /// </summary>
        public static void DemoThreadingBasics()
        {
            Console.WriteLine("\n=== 1. 线程安全的并发操作 ===");

            _counter = 0;
            var t1 = new Thread(IncrementWithInterlocked);
            var t2 = new Thread(IncrementWithInterlocked);

            var sw = Stopwatch.StartNew();
            t1.Start();
            t2.Start();
            t1.Join();
            t2.Join();
            sw.Stop();

            Console.WriteLine($"  两个线程各递增 1,000,000 次");
            Console.WriteLine($"  结果: {Interlocked(ref _counter):N0} (期望: 2,000,000)");
            Console.WriteLine($"  耗时: {sw.ElapsedMilliseconds}ms");
        }

        private static int Interlocked(ref int target) => target;

        // =========================================================================
        // 2. C# 没有 GIL —— CPU 密集型任务可以真正加速
        // =========================================================================
        // 【Python 对比】
        // Python 的 threading 对 CPU 密集型无效（GIL 限制）
        // C# 的 Task.Run / Parallel.For 可以真正利用多核

        /// <summary>
        /// CPU 密集型计算
        /// </summary>
        public static double CpuBoundWork(int n)
        {
            double total = 0;
            for (int i = 0; i < n; i++)
            {
                total += Math.Sqrt(i);
            }
            return total;
        }

        /// <summary>
        /// 演示 CPU 密集型任务的真正并行
        /// 【Python 对比】需要用 multiprocessing 才能达到类似效果
        /// </summary>
        public static void DemoNoGilParallel()
        {
            Console.WriteLine("\n=== 2. 没有 GIL — CPU 密集型真正并行 ===");

            int n = 2_000_000;

            // 单线程串行
            var sw = Stopwatch.StartNew();
            double r1 = CpuBoundWork(n);
            double r2 = CpuBoundWork(n);
            long singleTime = sw.ElapsedMilliseconds;
            Console.WriteLine($"  单线程串行: {singleTime}ms (结果: {r1 + r2:N0})");

            // 多线程并行（C# 真正利用多核！）
            sw.Restart();
            double[] results = new double[2];
            Parallel.For(0, 2, i =>
            {
                results[i] = CpuBoundWork(n);
            });
            long parallelTime = sw.ElapsedMilliseconds;
            Console.WriteLine($"  Parallel.For: {parallelTime}ms (结果: {results.Sum():N0})");
            Console.WriteLine($"  加速比: {(double)singleTime / parallelTime:F2}x");
            Console.WriteLine($"  【Python 对比】Python threading 无法做到这一点（GIL 限制）");
        }

        // =========================================================================
        // 3. Task —— C# 最常用的并发方式
        // =========================================================================
        // 【Python 对比】
        // C#: Task.Run(() => DoWork())
        // Python: threading.Thread(target=func).start() 或 asyncio.create_task(coro)

        /// <summary>
        /// 演示 Task 的使用
        /// </summary>
        public static async Task DemoTaskAsync()
        {
            Console.WriteLine("\n=== 3. Task 并发 ===");

            // 创建多个并行任务
            var tasks = Enumerable.Range(1, 5)
                .Select(i => Task.Run(() =>
                {
                    Thread.Sleep(200);  // 模拟工作
                    return $"任务{i}完成 (线程ID: {Thread.CurrentThread.ManagedThreadId})";
                }))
                .ToList();

            string[] results = await Task.WhenAll(tasks);
            foreach (string result in results)
            {
                Console.WriteLine($"  {result}");
            }

            Console.WriteLine($"  主线程 ID: {Thread.CurrentThread.ManagedThreadId}");
            Console.WriteLine($"  【Python 对比】asyncio.gather() 实现类似功能");
        }

        // =========================================================================
        // 4. ThreadPool —— 线程池管理
        // =========================================================================
        // 【Python 对比】concurrent.futures.ThreadPoolExecutor
        // C# 的 ThreadPool 由 CLR 自动管理

        /// <summary>
        /// 演示 ThreadPool 和 Parallel
        /// </summary>
        public static void DemoThreadPool()
        {
            Console.WriteLine("\n=== 4. ThreadPool 与 Parallel ===");

            // ThreadPool.QueueUserWorkItem —— 底层的线程池任务
            // 【Python 对比】executor.submit(func, args)
            var resetEvent = new ManualResetEventSlim(false);

            ThreadPool.QueueUserWorkItem(_ =>
            {
                Console.WriteLine($"  ThreadPool 工作项 (线程ID: {Thread.CurrentThread.ManagedThreadId})");
                resetEvent.Set();
            });

            resetEvent.Wait();

            // Parallel.For —— 数据并行
            // 【Python 对比】multiprocessing.Pool.map() 或 concurrent.futures
            Console.WriteLine("  Parallel.For 结果:");
            long sum = 0;
            Parallel.For(0, 100, i =>
            {
                Interlocked.Add(ref sum, i);
            });
            Console.WriteLine($"    0到99的和 = {sum}");
        }

        // =========================================================================
        // 5. 异步 I/O —— 对比 Python asyncio
        // =========================================================================
        // 【Python 对比】
        // Python: async def fetch(url): ... await asyncio.sleep(1)
        // C#:     async Task<string> FetchAsync(url) { await Task.Delay(1000); }
        //
        // 两者原理相同：不阻塞线程，让出 CPU 给其他任务

        /// <summary>
        /// 模拟异步 I/O 操作
        /// </summary>
        public static async Task<string> FetchDataAsync(string url, int delayMs)
        {
            Console.WriteLine($"  [开始] {url}");
            await Task.Delay(delayMs);  // 不阻塞线程
            Console.WriteLine($"  [完成] {url}");
            return $"来自 {url} 的数据";
        }

        /// <summary>
        /// 演示异步 I/O 并发
        /// </summary>
        public static async Task DemoAsyncIoAsync()
        {
            Console.WriteLine("\n=== 5. 异步 I/O（对比 Python asyncio）===");

            var sw = Stopwatch.StartNew();

            // 并发执行多个异步请求
            // 【Python 对比】await asyncio.gather(fetch(u) for u in urls)
            var tasks = new[]
            {
                FetchDataAsync("api/users", 1000),
                FetchDataAsync("api/orders", 1500),
                FetchDataAsync("api/products", 800)
            };

            string[] results = await Task.WhenAll(tasks);

            sw.Stop();
            Console.WriteLine($"  获取 {results.Length} 个结果, 耗时: {sw.ElapsedMilliseconds}ms");
            Console.WriteLine($"  【Python 对比】asyncio.gather() 实现相同效果");
        }

        // =========================================================================
        // 6. CancellationToken —— 对比 Python 的取消机制
        // =========================================================================
        // 【Python 对比】
        // Python: asyncio 通过 CancelledError 取消协程
        // C#: CancellationToken 协作式取消，更优雅

        /// <summary>
        /// 可取消的异步任务
        /// </summary>
        public static async Task CancellableWorkAsync(CancellationToken token)
        {
            for (int i = 0; i < 10; i++)
            {
                token.ThrowIfCancellationRequested();
                Console.WriteLine($"  工作步骤 {i + 1}/10");
                await Task.Delay(200, token);
            }
        }

        /// <summary>
        /// 演示取消操作
        /// </summary>
        public static async Task DemoCancellationAsync()
        {
            Console.WriteLine("\n=== 6. CancellationToken（协作式取消）===");

            using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(1));

            try
            {
                await CancellableWorkAsync(cts.Token);
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("  [已取消] 任务在1秒后被取消");
            }

            Console.WriteLine("  【Python 对比】asyncio 的 CancelledError 机制类似");
        }
    }

    // =========================================================================
    // 主程序入口
    // =========================================================================
    class Program
    {
        /// <summary>
        /// 程序入口
        /// 【Python 对比】if __name__ == "__main__": main()
        /// </summary>
        static async Task Main(string[] args)
        {
            Console.WriteLine("============================================================");
            Console.WriteLine("  C# 老兵的 Python 修炼手册 — 5.2 多线程与 GIL");
            Console.WriteLine("============================================================");
            Console.WriteLine($"  C# CLR 没有 GIL，线程可以真正并行");
            Console.WriteLine($"  Python CPython 有 GIL，CPU 密集型需用 multiprocessing");

            ThreadExamples.DemoThreadingBasics();
            ThreadExamples.DemoNoGilParallel();
            await ThreadExamples.DemoTaskAsync();
            ThreadExamples.DemoThreadPool();
            await ThreadExamples.DemoAsyncIoAsync();
            await ThreadExamples.DemoCancellationAsync();

            Console.WriteLine("\n============================================================");
            Console.WriteLine("  核心结论：");
            Console.WriteLine("  1. C# 没有 GIL，Task.Run / Parallel.For 天然支持并行");
            Console.WriteLine("  2. Python 有 GIL，CPU 密集型必须用 multiprocessing");
            Console.WriteLine("  3. I/O 密集型两者都可用异步模型处理");
            Console.WriteLine("  4. C# 的 CancellationToken 比 Python 的取消机制更优雅");
            Console.WriteLine("============================================================");
        }
    }
}
