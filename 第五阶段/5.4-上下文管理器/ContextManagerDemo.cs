// =============================================================================
// C# 上下文管理器示例 — C# 老兵的 Python 修炼手册 5.4
// 对应文章：5.4 上下文管理器
// 关键概念：IDisposable, using, IAsyncDisposable, await using
// =============================================================================
// 【C# vs Python 对比】
// C#: using (var resource = new Disposable()) { ... }
// Python: with ContextManager() as resource: ...
//
// C# 的 using 语句是 .NET 资源管理的核心机制
// Python 的 with 语句功能等价，但实现更灵活
// =============================================================================

using System;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;

namespace ContextManagerDemo
{
    // =========================================================================
    // 1. IDisposable 基础 —— 对比 Python __enter__/__exit__
    // =========================================================================
    // 【Python 对比】
    // Python:
    //   class Timer:
    //       def __enter__(self): self.start = time.time(); return self
    //       def __exit__(self, exc_type, exc_val, exc_tb): ...
    //
    // C#:
    //   public class Timer : IDisposable
    //   {
    //       public Timer() { ... }        // 对应 __enter__
    //       public void Dispose() { ... } // 对应 __exit__
    //   }

    /// <summary>
    /// 计时器——演示 IDisposable 模式
    /// </summary>
    public class Timer : IDisposable
    {
        private readonly Stopwatch _sw = new Stopwatch();
        private readonly string _label;

        public Timer(string label = "操作")
        {
            _label = label;
            _sw.Start();
            // 对应 Python 的 __enter__ 中的初始化代码
        }

        /// <summary>
        /// 释放资源
        /// 【Python 对比】__exit__(self, exc_type, exc_val, exc_tb)
        /// 注意: C# Dispose 无法访问异常信息，Python __exit__ 可以
        /// </summary>
        public void Dispose()
        {
            _sw.Stop();
            Console.WriteLine($"  [{_label}] 耗时: {_sw.ElapsedMilliseconds}ms");
            // 对应 Python 的 __exit__ 中的清理代码
        }
    }

    // =========================================================================
    // 2. using 语句 —— 对比 Python with 语句
    // =========================================================================
    // 【Python 对比】
    // with Timer() as t: ...
    //
    // C# 有两种形式:
    // using (var t = new Timer()) { ... }    // 传统语法
    // using var t = new Timer(); ...          // C# 8+ 声明语法

    /// <summary>
    /// 演示 using 语句的各种形式
    /// </summary>
    public static class UsingExamples
    {
        public static void DemoUsing()
        {
            Console.WriteLine("\n=== 1. using 语句（对比 Python with） ===");

            // 传统 using 语句
            // 【Python 对比】with Timer() as t: ...
            Console.WriteLine("  传统 using:");
            using (var timer = new Timer("传统 using"))
            {
                System.Threading.Thread.Sleep(50);
            }  // 自动调用 Dispose()

            // C# 8+ using 声明 —— 更像 Python 的 with
            // 【Python 对比】Python 的 with 本身就是这种"声明式"
            Console.WriteLine("  C# 8+ using 声明:");
            using var timer2 = new Timer("using 声明");
            System.Threading.Thread.Sleep(50);
            // 离开作用域时自动调用 Dispose()

            // 多个 using 嵌套
            // 【Python 对比】with A() as a, B() as b: ...  (Python 更简洁)
            Console.WriteLine("  嵌套 using:");
            using (var t1 = new Timer("外层"))
            using (var t2 = new Timer("内层"))
            {
                System.Threading.Thread.Sleep(50);
            }

            Console.WriteLine("  【Python 对比】Python 可以一行: with A(), B(), C(): ...");
        }
    }

    // =========================================================================
    // 3. 文件操作——最常见的 IDisposable 场景
    // =========================================================================
    // 【Python 对比】
    // Python: with open("file.txt", "r") as f: content = f.read()
    // C#:     using (var reader = new StreamReader("file.txt")) { ... }
    //
    // 注意: Python 的 open() 是内置函数，C# 需要创建 StreamReader 对象

    /// <summary>
    /// 演示文件操作的 using 模式
    /// </summary>
    public static class FileExamples
    {
        public static void DemoFileOperations()
        {
            Console.WriteLine("\n=== 2. 文件操作（对比 Python with open） ===");

            string tempFile = Path.GetTempFileName();

            try
            {
                // 写入文件
                // 【Python 对比】with open(path, "w") as f: f.write("...")
                using (var writer = new StreamWriter(tempFile))
                {
                    writer.WriteLine("Hello from C#!");
                    writer.WriteLine("Context Manager Demo");
                }  // writer 自动关闭

                // 读取文件
                // 【Python 对比】with open(path, "r") as f: content = f.read()
                using var reader = new StreamReader(tempFile);
                string content = reader.ReadToEnd();
                Console.WriteLine($"  文件内容: {content.Trim()}");
            }
            finally
            {
                File.Delete(tempFile);
            }

            Console.WriteLine("  【Python 对比】Python: with open(path) as f: ...");
        }
    }

    // =========================================================================
    // 4. 数据库连接——模拟实际场景
    // =========================================================================
    // 【Python 对比】
    // Python:
    //   with database_connection("conn_str") as conn:
    //       conn.execute("SELECT ...")
    //
    // C#:
    //   using var conn = new SqlConnection(connStr);
    //   conn.Open();
    //   ...

    /// <summary>
    /// 模拟数据库连接
    /// </summary>
    public class DatabaseConnection : IDisposable
    {
        private bool _disposed = false;
        private readonly string _connectionString;

        public DatabaseConnection(string connectionString)
        {
            _connectionString = connectionString;
            Console.WriteLine($"  [DB] 连接到: {connectionString}");
        }

        public void Execute(string sql)
        {
            if (_disposed)
                throw new ObjectDisposedException(nameof(DatabaseConnection));
            Console.WriteLine($"  [DB] 执行: {sql}");
        }

        /// <summary>
        /// 释放数据库连接
        /// 【Python 对比】__exit__ 方法
        /// </summary>
        public void Dispose()
        {
            if (!_disposed)
            {
                Console.WriteLine("  [DB] 关闭数据库连接");
                _disposed = true;
            }
        }
    }

    /// <summary>
    /// 演示数据库连接的 using 模式
    /// </summary>
    public static class DatabaseExamples
    {
        public static void DemoDatabase()
        {
            Console.WriteLine("\n=== 3. 数据库连接（对比 Python with db_conn） ===");

            // 单个连接
            // 【Python 对比】with database_connection("...") as conn:
            using var conn = new DatabaseConnection("Server=localhost;Database=test");
            conn.Execute("SELECT * FROM users");
            conn.Execute("INSERT INTO logs ...");
            // 离开作用域时自动 Dispose

            Console.WriteLine("  【Python 对比】Python 的 @contextmanager 简化了编写");
        }
    }

    // =========================================================================
    // 5. IAsyncDisposable —— 对比 Python async with
    // =========================================================================
    // 【Python 对比】
    // Python:
    //   async with AsyncResource() as res:
    //       await res.do_something()
    //
    // C# 8+:
    //   await using var resource = new AsyncResource();
    //   await resource.DoSomethingAsync();

    /// <summary>
    /// 异步资源——实现 IAsyncDisposable
    /// 【Python 对比】实现 __aenter__ 和 __aexit__
    /// </summary>
    public class AsyncResource : IAsyncDisposable
    {
        private bool _disposed = false;

        public AsyncResource()
        {
            Console.WriteLine("  [Async] 资源已创建");
        }

        public async ValueTask DisposeAsync()
        {
            if (!_disposed)
            {
                Console.WriteLine("  [Async] 异步释放资源...");
                await Task.Delay(50);  // 模拟异步清理
                _disposed = true;
                Console.WriteLine("  [Async] 资源已释放");
            }
        }
    }

    /// <summary>
    /// 演示 IAsyncDisposable
    /// </summary>
    public static class AsyncDisposableExamples
    {
        /// <summary>
        /// 异步上下文管理器示例
        /// 【Python 对比】async with AsyncResource() as res:
        /// </summary>
        public static async Task DemoAsyncDisposableAsync()
        {
            Console.WriteLine("\n=== 4. IAsyncDisposable（对比 Python async with） ===");

            // C# 8+ await using
            // 【Python 对比】async with AsyncResource() as res:
            await using (var resource = new AsyncResource())
            {
                Console.WriteLine("  [Async] 使用资源");
                await Task.Delay(50);
            }  // 自动调用 DisposeAsync()

            // C# 8+ await using 声明
            await using var resource2 = new AsyncResource();
            Console.WriteLine("  [Async] 使用资源2");

            Console.WriteLine("  【Python 对比】Python 需要 __aenter__ 和 __aexit__");
        }
    }

    // =========================================================================
    // 6. 自定义资源管理器——实际项目中的模式
    // =========================================================================

    /// <summary>
    /// 事务管理器——对比 Python 的 @contextmanager transaction
    /// </summary>
    public class Transaction : IDisposable
    {
        private bool _committed = false;
        private bool _disposed = false;
        private readonly string _connectionString;

        public Transaction(string connectionString)
        {
            _connectionString = connectionString;
            Console.WriteLine($"  [Transaction] 开始事务 ({connectionString})");
        }

        public void Commit()
        {
            _committed = true;
            Console.WriteLine("  [Transaction] 事务已提交");
        }

        public void Rollback()
        {
            _committed = false;
            Console.WriteLine("  [Transaction] 事务已回滚");
        }

        /// <summary>
        /// Dispose 时如果未提交则自动回滚
        /// 【Python 对比】__exit__ 中的 try/finally 逻辑
        /// </summary>
        public void Dispose()
        {
            if (!_disposed)
            {
                if (!_committed)
                {
                    Rollback();
                }
                Console.WriteLine("  [Transaction] 连接已关闭");
                _disposed = true;
            }
        }
    }

    /// <summary>
    /// 演示事务管理器
    /// </summary>
    public static class TransactionExamples
    {
        public static void DemoTransaction()
        {
            Console.WriteLine("\n=== 5. 事务管理器（对比 Python @contextmanager） ===");

            // 正常提交
            Console.WriteLine("  正常事务:");
            using (var tx = new Transaction("Server=localhost"))
            {
                Console.WriteLine("  执行: INSERT INTO users ...");
                tx.Commit();  // 手动提交
            }

            Console.WriteLine();

            // 异常回滚
            Console.WriteLine("  异常事务:");
            try
            {
                using var tx = new Transaction("Server=localhost");
                Console.WriteLine("  执行: INSERT INTO users ...");
                throw new InvalidOperationException("模拟 SQL 错误");
            }
            catch (InvalidOperationException ex)
            {
                Console.WriteLine($"  [主程序] 捕获异常: {ex.Message}");
            }
            // Dispose 时自动回滚（因为没有 Commit）

            Console.WriteLine("  【Python 对比】Python @contextmanager 的 yield 实现更简洁");
        }
    }

    // =========================================================================
    // 7. 嵌套 using——对比 Python 一行多上下文
    // =========================================================================

    public static class NestingExamples
    {
        public static void DemoNesting()
        {
            Console.WriteLine("\n=== 6. 嵌套 using ===");

            // C# 嵌套 using——每个资源一层
            // 【Python 对比】Python 可以一行: with A(), B(), C(): ...
            Console.WriteLine("  嵌套 using:");
            using (var t1 = new Timer("外层"))
            {
                using (var t2 = new Timer("中层"))
                {
                    using (var t3 = new Timer("内层"))
                    {
                        System.Threading.Thread.Sleep(30);
                    }
                }
            }

            // C# 8+ 简化嵌套
            Console.WriteLine("  C# 8+ 简化:");
            using var t4 = new Timer("using 声明1");
            using var t5 = new Timer("using 声明2");
            System.Threading.Thread.Sleep(30);

            Console.WriteLine("  【Python 对比】Python: with A() as a, B() as b: ...");
        }
    }

    // =========================================================================
    // 主程序入口
    // =========================================================================
    class Program
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine("============================================================");
            Console.WriteLine("  C# 老兵的 Python 修炼手册 — 5.4 上下文管理器");
            Console.WriteLine("============================================================");

            UsingExamples.DemoUsing();
            FileExamples.DemoFileOperations();
            DatabaseExamples.DemoDatabase();
            await AsyncDisposableExamples.DemoAsyncDisposableAsync();
            TransactionExamples.DemoTransaction();
            NestingExamples.DemoNesting();

            Console.WriteLine("\n============================================================");
            Console.WriteLine("  核心总结：");
            Console.WriteLine("  1. C# using ≈ Python with，都是 RAII 模式");
            Console.WriteLine("  2. IDisposable.Dispose ≈ Python __exit__");
            Console.WriteLine("  3. C# Dispose 无法访问异常信息，Python __exit__ 可以");
            Console.WriteLine("  4. Python @contextmanager 简化了编写（C# 没有等价物）");
            Console.WriteLine("  5. C# await using ≈ Python async with");
            Console.WriteLine("  6. Python 支持一行嵌套多个上下文");
            Console.WriteLine("============================================================");
        }
    }
}
