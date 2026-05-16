using System;
using System.Diagnostics;
using System.Runtime.ExceptionServices;

/// <summary>
/// C# 异常处理完整示例
/// 对应文章：4.1 异常处理
///
/// Python 对比：
///   C# try/catch/when/finally  ≈  Python try/except/else/finally
///   C# 没有 else 子句，else 的逻辑通常放在 try 末尾
///   C# 的 when 过滤器  ≈  Python 的 except 中用 if 判断
/// </summary>
class ExceptionHandling
{
    static void Main()
    {
        // =============================================================
        // 1. 基础 try-catch-finally
        // =============================================================
        // Python 对比：
        //   try:
        //       result = 10 / int("0")
        //   except ZeroDivisionError as e:
        //       print(f"除零错误: {e}")
        //   except ValueError as e:
        //       print(f"格式错误: {e}")
        //   except Exception as e:
        //       print(f"其他错误: {e}")
        //   finally:
        //       print("不管出不出错都执行")
        // =============================================================
        Console.WriteLine("============================================================");
        Console.WriteLine("1. 基础 try-catch-finally");
        Console.WriteLine("============================================================");

        try
        {
            int result = 10 / int.Parse("0");
            Console.WriteLine(result);
        }
        catch (DivideByZeroException ex)
        {
            // Python 中对应：except ZeroDivisionError as e
            Console.WriteLine($"除零错误: {ex.Message}");
        }
        catch (FormatException ex)
        {
            // Python 中对应：except ValueError as e
            Console.WriteLine($"格式错误: {ex.Message}");
        }
        catch (Exception ex)
        {
            // Python 中对应：except Exception as e — 兜底捕获
            Console.WriteLine($"其他错误: {ex.Message}");
        }
        finally
        {
            // Python 和 C# 的 finally 行为一致：无论是否异常都执行
            Console.WriteLine("不管出不出错都执行 (finally)");
        }

        // =============================================================
        // 2. 多类型捕获 — 一个 catch 捕获多种异常
        // =============================================================
        // Python 对比：
        //   except (KeyError, TypeError) as e:
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("2. 多类型捕获 — 一个 catch 捕获多种异常");
        Console.WriteLine("============================================================");

        try
        {
            var data = new System.Collections.Generic.Dictionary<string, string> { { "name", "Alice" } };
            string value = data["age"]; // KeyNotFoundException
            int num = int.Parse(value);
        }
        catch (System.Collections.Generic.KeyNotFoundException | FormatException ex)
        {
            // C# 8+ 支持管道符合并多种异常类型
            Console.WriteLine($"键或格式错误: {ex.GetType().Name}: {ex.Message}");
        }

        // =============================================================
        // 3. 异常过滤器 — when 关键字 (C# 6+)
        // =============================================================
        // Python 对比：
        //   Python 没有 when 过滤器，只能在 except 中用 if 判断：
        //   except ValueError as e:
        //       if "invalid" in str(e):
        //           ...
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("3. 异常过滤器 — when 关键字 (C# 6+)");
        Console.WriteLine("============================================================");

        try
        {
            throw new HttpRequestException("Not Found", inner: null,
                System.Net.HttpStatusCode.NotFound);
        }
        catch (HttpRequestException ex) when (ex.StatusCode == System.Net.HttpStatusCode.NotFound)
        {
            // when 过滤器：只在条件满足时捕获（Python 无直接等价物）
            Console.WriteLine($"HTTP 404: 页面不存在");
        }
        catch (HttpRequestException ex) when (ex.StatusCode == System.Net.HttpStatusCode.Unauthorized)
        {
            Console.WriteLine($"HTTP 401: 未授权");
        }
        catch (HttpRequestException ex)
        {
            Console.WriteLine($"HTTP 错误: {ex.StatusCode}");
        }

        // =============================================================
        // 4. 异常链 — Inner Exception
        // =============================================================
        // Python 对比：
        //   raise RuntimeError("处理失败") from original_exception
        //   # 或 raise RuntimeError("处理失败") from None 抑制链
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("4. 异常链 — Inner Exception");
        Console.WriteLine("============================================================");

        try
        {
            try
            {
                int.Parse("not_a_number");
            }
            catch (FormatException original)
            {
                // 将原始异常作为 innerException 传递（等同 Python 的 from）
                throw new ApplicationException("数据转换失败", original);
            }
        }
        catch (ApplicationException ex)
        {
            Console.WriteLine($"外层异常: {ex.Message}");
            Console.WriteLine($"原始异常 (InnerException): {ex.InnerException?.Message}");
        }

        // =============================================================
        // 5. ExceptionDispatchInfo — 保留完整堆栈重新抛出
        // =============================================================
        // Python 对比：
        //   raise  # 在 except 块中直接 raise 即可保留堆栈
        //   # 或 ExceptionDispatchInfo.Capture(ex).Throw() 更加接近
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("5. ExceptionDispatchInfo — 保留完整堆栈重新抛出");
        Console.WriteLine("============================================================");

        try
        {
            try
            {
                int.Parse("bad");
            }
            catch (Exception ex)
            {
                // ExceptionDispatchInfo 保留原始堆栈信息
                // Python 中直接 raise 即可保留堆栈
                ExceptionDispatchInfo.Capture(ex).Throw();
            }
        }
        catch (FormatException ex)
        {
            Console.WriteLine($"捕获到异常: {ex.Message}");
            Console.WriteLine($"堆栈跟踪保留了原始位置");
        }

        // =============================================================
        // 6. 内置异常层次结构
        // =============================================================
        // Python 对比：
        //   BaseException > Exception > LookupError > KeyError
        //   Python 的异常层级通过 MRO (方法解析顺序) 查看
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("6. 内置异常层次结构");
        Console.WriteLine("============================================================");

        Console.WriteLine("C# 异常层级:");
        Console.WriteLine("  System.Object > System.Exception > System.SystemException");
        Console.WriteLine("      > ArgumentException, InvalidOperationException ...");
        Console.WriteLine("  System.Object > System.Exception > System.ApplicationException");
        Console.WriteLine();

        // 查看异常继承链
        var keyEx = new KeyNotFoundException("test");
        Console.WriteLine("KeyNotFoundException 的继承链:");
        Type? t = keyEx.GetType();
        while (t != null)
        {
            Console.WriteLine($"  {t.Name}");
            t = t.BaseType;
        }

        // is 运算符判断异常关系（等同 Python 的 issubclass）
        Console.WriteLine();
        Console.WriteLine($"KeyNotFoundException 是 LookupException 的子类? {keyEx is LookupException}");
        Console.WriteLine($"KeyNotFoundException 是 Exception 的子类? {keyEx is Exception}");

        // =============================================================
        // 7. using 语句 — 上下文管理器的等价物
        // =============================================================
        // Python 对比：
        //   with open("file.txt") as f:
        //       content = f.read()
        //   # 离开 with 块自动调用 __exit__ 关闭文件
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("7. using 语句 — 上下文管理器的等价物");
        Console.WriteLine("============================================================");

        string testFile = "_temp_demo_cs.txt";

        // 写入文件
        using (var writer = new StreamWriter(testFile))
        {
            writer.WriteLine("Hello, C# 异常处理!");
            writer.WriteLine("第二行内容");
        }
        // 离开 using 块，writer 自动 Dispose 关闭文件

        // 读取文件
        using (var reader = new StreamReader(testFile))
        {
            string? content = reader.ReadToEnd();
            Console.WriteLine($"文件内容:\n{content}");
        }

        // C# 8+ using 声明（更简洁）
        using var reader2 = new StreamReader(testFile);
        Console.WriteLine($"using 声明方式读取: {reader2.ReadToEnd()}");
        // reader2 在当前作用域结束时自动释放

        // 清理
        File.Delete(testFile);

        // =============================================================
        // 8. IDisposable 与异常安全的资源管理
        // =============================================================
        // Python 对比：
        //   class ManagedResource:
        //       def __enter__(self): ...   # 获取资源
        //       def __exit__(self, ...): ... # 释放资源 + 处理异常
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("8. IDisposable 与异常安全的资源管理");
        Console.WriteLine("============================================================");

        // 场景 1：正常执行
        Console.WriteLine("场景 1 - 正常执行:");
        using (var resource = new ManagedResource())
        {
            Console.WriteLine("  [主逻辑] 正常工作");
        }

        // 场景 2：异常发生时自动释放
        Console.WriteLine("\n场景 2 - 异常发生时自动释放:");
        try
        {
            using (var resource = new ManagedResource())
            {
                Console.WriteLine("  [主逻辑] 即将出错");
                throw new InvalidOperationException("出错了!");
            }
        }
        catch (InvalidOperationException ex)
        {
            Console.WriteLine($"  [外部] 捕获到异常: {ex.Message}");
        }

        // =============================================================
        // 9. 异常处理最佳实践总结
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("9. 异常处理最佳实践总结");
        Console.WriteLine("============================================================");
        Console.WriteLine();
        Console.WriteLine("C#                                     | Python");
        Console.WriteLine("---------------------------------------|----------------------------------");
        Console.WriteLine("catch (Exception ex)                   | except Exception as e");
        Console.WriteLine("catch (A | B ex)               (C# 8+) | except (A, B) as e");
        Console.WriteLine("catch (Ex ex) when (condition)         | except Ex as e: if condition: ...");
        Console.WriteLine("throw new X(\"msg\", innerEx)             | raise X(\"msg\") from original");
        Console.WriteLine("try { } finally { }                    | try: ... finally: ...");
        Console.WriteLine("using (var x = ...)                    | with ... as x:");
        Console.WriteLine("catch (AggregateException)             | except*: ExceptionGroup");
        Console.WriteLine();

        // 反面示例：不要用 catch (Exception) 做流程控制
        Console.WriteLine("反面示例 — 不要用 catch(Exception) 做流程控制:");
        try
        {
            try
            {
                int.Parse("bad");
            }
            catch (Exception)
            {
                // 捕获所有异常来处理已知的 FormatException — 不推荐
                Console.WriteLine("  catch(Exception 范围过大，可能掩盖未知错误");
            }
        }
        catch { }

        Console.WriteLine("\n推荐做法 — 明确指定异常类型:");
        try
        {
            int.Parse("bad");
        }
        catch (FormatException ex)
        {
            Console.WriteLine($"  明确捕获 FormatException: {ex.Message}");
        }

        // =============================================================
        // 10. 异常与性能 (异常不是流程控制工具)
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("10. 异常与性能 (异常不是流程控制工具)");
        Console.WriteLine("============================================================");

        // C# 异常比 Python 更重量级，性能开销更大
        // 因此更应该避免用异常做流程控制
        var testDict = new System.Collections.Generic.Dictionary<int, int>();
        for (int i = 0; i < 1000; i++) testDict[i] = i;

        // 正常方式：先检查再操作
        var sw = Stopwatch.StartNew();
        for (int i = 0; i < 100000; i++)
        {
            _ = testDict.ContainsKey(500) ? testDict[500] : -1;
            _ = testDict.ContainsKey(9999) ? testDict[9999] : -1;
        }
        sw.Stop();
        double normalTime = sw.Elapsed.TotalSeconds;

        // 异常方式
        sw.Restart();
        for (int i = 0; i < 100000; i++)
        {
            try { _ = testDict[500]; }
            catch (KeyNotFoundException) { _ = -1; }
            try { _ = testDict[9999]; }
            catch (KeyNotFoundException) { _ = -1; }
        }
        sw.Stop();
        double exceptionTime = sw.Elapsed.TotalSeconds;

        Console.WriteLine($"正常方式 (ContainsKey) 10万次: {normalTime:F4}s");
        Console.WriteLine($"异常方式 (try-catch) 10万次:   {exceptionTime:F4}s");
        Console.WriteLine("结论: C# 异常开销比 Python 大得多，绝对不要用异常做流程控制");
        Console.WriteLine("      推荐使用 TryGetValue / ContainsKey 等模式");

        Console.WriteLine();
        Console.WriteLine("所有异常处理示例运行完毕！");
    }
}

/// <summary>
/// 模拟一个需要资源管理的类（类似 Python 的上下文管理器）
/// Python 等价：
///   class ManagedResource:
///       def __enter__(self): ...
///       def __exit__(self, exc_type, exc_val, exc_tb): ...
/// </summary>
class ManagedResource : IDisposable
{
    public void Dispose()
    {
        Console.WriteLine("  [Dispose] 释放资源 (等同 Python 的 __exit__)");
        GC.SuppressFinalize(this);
    }
}
