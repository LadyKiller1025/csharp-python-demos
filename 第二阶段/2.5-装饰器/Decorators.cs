// ============================================================================
// C# Attribute 与拦截器 —— 对应 Python 装饰器
// 对应文章：2.5 装饰器
// ============================================================================
//
// 【C# 程序员的 Python 修炼手册】
//
// 这个文件展示 C# 中与 Python 装饰器等价的各种模式：
//   1. Attribute（元数据标注）      ← 最基础，但本身不能拦截调用
//   2. 装饰器模式（Decorator Pattern）← GoF 经典设计模式
//   3. 拦截器（Method Interception） ← Castle DynamicProxy / RealProxy
//   4. Action Filter               ← ASP.NET Core 最接近 Python 装饰器
//
// 核心区别：
// - Python 装饰器：@ 语法糖直接包装函数，运行时生效
// - C# Attribute：需要框架（ASP.NET Core、Castle）配合反射读取才能拦截
// - C# 更安全（类型检查），Python 更灵活（动态包装）
// ============================================================================

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Threading;

// ============================================================================
// 1. 基础 Attribute —— Python @decorator 的最简等价物
// ============================================================================
//
// 【Python 等价】
// def log(func):
//     def wrapper(*args, **kwargs):
//         print(f"调用 {func.__name__}")
//         return func(*args, **kwargs)
//     return wrapper
//
// 重要区别：
// - Python 装饰器在定义时就包装了函数（编译期等价）
// - C# Attribute 只是元数据标签，需要反射在运行时读取
// - 仅贴上 [Log] 标签不会产生任何效果！

/// <summary>
/// 日志 Attribute —— 标记需要记录日志的方法
/// 【对比 Python @timer / @log 装饰器】
/// </summary>
[AttributeUsage(AttributeTargets.Method, AllowMultiple = true)]
public class LogAttribute : Attribute
{
    public string Message { get; set; }

    public LogAttribute(string message = "")
    {
        Message = message;
    }
}

/// <summary>
/// 缓存 Attribute
/// 【对比 Python @cache(maxsize=128) 装饰器】
/// </summary>
[AttributeUsage(AttributeTargets.Method)]
public class CacheAttribute : Attribute
{
    public int DurationSeconds { get; set; } = 60;
}

/// <summary>
/// 权限检查 Attribute
/// 【对比 Python @require_role("Admin") 装饰器】
/// </summary>
[AttributeUsage(AttributeTargets.Method)]
public class AuthorizeAttribute : Attribute
{
    public string Roles { get; set; } = "";
}

/// <summary>
/// 计时 Attribute
/// 【对比 Python @timer 装饰器】
/// </summary>
[AttributeUsage(AttributeTargets.Method)]
public class TimedAttribute : Attribute { }


// ============================================================================
// 2. 方法拦截器（Method Interceptor）—— 真正实现"装饰"效果
// ============================================================================
//
// 【Python 等价】
// Python 装饰器本质上就是一个高阶函数包装：
//   @timer
//   def func(): ...
//   # 等价于 func = timer(func)
//
// C# 中要实现同样的效果，需要用接口 + 反射 + 代理
// 框架层面：Castle DynamicProxy, Autofac Interceptor, DispatchProxy
//
// 这里用 DispatchProxy（.NET 内置）演示核心原理

/// <summary>
/// 方法拦截信息 —— 对应 Python 装饰器 wrapper 函数的参数
/// </summary>
public class InterceptedMethod
{
    public string MethodName { get; set; } = "";
    public object?[] Args { get; set; } = Array.Empty<object?>();
    public Stopwatch Timer { get; set; } = new();
}

/// <summary>
/// 拦截代理 —— C# 版的"函数包装器"
/// 【核心概念】这等价于 Python 装饰器的 wrapper 函数
///
/// Python:
///   def wrapper(*args, **kwargs):
///       print(f"调用 {func.__name__}")
///       result = func(*args, **kwargs)
///       print(f"返回 {result}")
///       return result
///
/// C# (DispatchProxy):
///   protected override object? Invoke(MethodInfo targetMethod, object?[] args)
///   {
///       // 在目标方法前后添加逻辑 = 装饰器的 wrapper
///   }
/// </summary>
public class MethodInterceptionProxy<T> : DispatchProxy where T : class
{
    private T? _decorated = null!;
    private readonly List<Action<InterceptedMethod>> _interceptors = new();

    /// <summary>
    /// 注册拦截行为 —— 类似于给同一个函数堆叠多个 Python 装饰器
    /// </summary>
    public void AddInterceptor(Action<InterceptedMethod> interceptor)
    {
        _interceptors.Add(interceptor);
    }

    protected override object? Invoke(MethodInfo targetMethod, object?[]? args)
    {
        var info = new InterceptedMethod
        {
            MethodName = targetMethod.Name,
            Args = args ?? Array.Empty<object?>()
        };

        // 前置拦截（对应 Python 装饰器中 func 调用前的代码）
        foreach (var interceptor in _interceptors)
        {
            interceptor(info);
        }

        info.Timer.Start();
        try
        {
            // 调用原始方法
            var result = targetMethod.Invoke(_decorated, args);
            info.Timer.Stop();

            // 后置拦截（对应 Python 装饰器中 func 调用后的代码）
            Console.WriteLine($"  [C# Interceptor] {targetMethod.Name} 完成，" +
                            $"耗时 {info.Timer.ElapsedMilliseconds}ms，返回 {result}");
            return result;
        }
        catch (TargetInvocationException ex) when (ex.InnerException != null)
        {
            info.Timer.Stop();
            Console.WriteLine($"  [C# Interceptor] {targetMethod.Name} 异常: {ex.InnerException.Message}");
            throw ex.InnerException;
        }
    }

    /// <summary>
    /// 创建代理实例
    /// </summary>
    public static T Create(T decorated)
    {
        var proxy = Create<T, MethodInterceptionProxy<T>>() as MethodInterceptionProxy<T>;
        proxy!._decorated = decorated;
        return proxy as T ?? throw new InvalidOperationException("无法创建代理");
    }
}


// ============================================================================
// 3. Action Filter 模式 —— ASP.NET Core 风格
// ============================================================================
//
// 这是 ASP.NET Core 中最接近 Python 装饰器的模式
// 每个 Filter 就是一个装饰器，可以堆叠

/// <summary>
/// Filter 执行上下文
/// </summary>
public class FilterContext
{
    public string MethodName { get; set; } = "";
    public Dictionary<string, object?> Parameters { get; set; } = new();
    public bool IsCancelled { get; set; }
    public string? CancellationReason { get; set; }
}

/// <summary>
/// IActionFilter —— 等价于 Python 装饰器的接口
///
/// Python:
///   def decorator(func):
///       def wrapper(*args, **kwargs):
///           # Before
///           result = func(*args, **kwargs)
///           # After
///           return result
///       return wrapper
///
/// C#:
///   void OnBefore(FilterContext context);   // 函数调用前
///   void OnAfter(FilterContext context);     // 函数调用后
/// </summary>
public interface IActionFilter
{
    void OnBefore(FilterContext context);
    void OnAfter(FilterContext context);
}

/// <summary>
/// 计时 Filter —— 等价于 Python @timer
/// </summary>
public class TimerFilter : IActionFilter
{
    private Stopwatch? _stopwatch;

    public void OnBefore(FilterContext context)
    {
        _stopwatch = Stopwatch.StartNew();
        Console.WriteLine($"  [TimerFilter] 开始计时: {context.MethodName}");
    }

    public void OnAfter(FilterContext context)
    {
        _stopwatch?.Stop();
        Console.WriteLine($"  [TimerFilter] {context.MethodName} 耗时: {_stopwatch?.ElapsedMilliseconds}ms");
    }
}

/// <summary>
/// 日志 Filter —— 等价于 Python @log
/// </summary>
public class LogFilter : IActionFilter
{
    public void OnBefore(FilterContext context)
    {
        var paramStr = string.Join(", ", context.Parameters.Select(p => $"{p.Key}={p.Value}"));
        Console.WriteLine($"  [LogFilter] 调用 {context.MethodName}({paramStr})");
    }

    public void OnAfter(FilterContext context)
    {
        Console.WriteLine($"  [LogFilter] {context.MethodName} 执行完成");
    }
}

/// <summary>
/// 权限 Filter —— 等价于 Python @require_role
/// </summary>
public class AuthorizeFilter : IActionFilter
{
    private readonly string _requiredRole;

    public AuthorizeFilter(string requiredRole)
    {
        _requiredRole = requiredRole;
    }

    public void OnBefore(FilterContext context)
    {
        if (context.Parameters.TryGetValue("userRole", out var role))
        {
            if (role?.ToString() != _requiredRole)
            {
                context.IsCancelled = true;
                context.CancellationReason = $"需要 {_requiredRole} 角色，当前角色: {role}";
                Console.WriteLine($"  [AuthorizeFilter] 权限不足: {context.CancellationReason}");
            }
        }
    }

    public void OnAfter(FilterContext context) { }
}


// ============================================================================
// 4. Filter Pipeline 执行器 —— 等价于 Python 装饰器堆叠
// ============================================================================
//
// 【Python 堆叠装饰器】
//   @timer          ← 最外层，最后包装
//   @log            ← 中间层
//   @authorize      ← 最内层，最先包装
//   def func(): ...
//
// 调用时: timer.wrapper → log.wrapper → authorize.wrapper → func
//
// C# Filter Pipeline 是同样的思路，只是实现方式不同

/// <summary>
/// Filter Pipeline —— 管理多个 Action Filter 的执行
/// </summary>
public static class FilterPipeline
{
    public static T Execute<T>(Func<T> action, string methodName,
        Dictionary<string, object?>? parameters = null,
        params IActionFilter[] filters)
    {
        var context = new FilterContext
        {
            MethodName = methodName,
            Parameters = parameters ?? new()
        };

        // 执行所有 OnBefore（对应 Python 装饰器从外到内执行）
        foreach (var filter in filters)
        {
            filter.OnBefore(context);
            if (context.IsCancelled)
            {
                Console.WriteLine($"  [Pipeline] 请求被取消: {context.CancellationReason}");
                return default!;
            }
        }

        try
        {
            // 执行目标方法
            var result = action();

            // 执行所有 OnAfter（反向，对应 Python 装饰器返回时从内到外）
            foreach (var filter in filters.Reverse())
            {
                filter.OnAfter(context);
            }

            return result;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"  [Pipeline] 方法执行异常: {ex.Message}");
            throw;
        }
    }
}


// ============================================================================
// 5. 装饰器模式（Decorator Pattern）—— GoF 设计模式
// ============================================================================
//
// 这是最传统的 C# 装饰方式，虽然啰嗦但类型安全

/// <summary>
/// 接口定义
/// </summary>
public interface IDataService
{
    string GetData(int id);
}

/// <summary>
/// 基础服务 —— 等价于 Python 的原始函数
/// </summary>
public class DataService : IDataService
{
    public string GetData(int id)
    {
        Console.WriteLine($"  [DataService] 从数据库获取 id={id}");
        return $"Data-{id}";
    }
}

/// <summary>
/// 缓存装饰器 —— 等价于 Python @cache
/// </summary>
public class CachedDataService : IDataService
{
    private readonly IDataService _inner;
    private readonly Dictionary<int, string> _cache = new();

    public CachedDataService(IDataService inner)
    {
        _inner = inner;  // 保存原始服务引用（类似 Python __wrapped__）
    }

    public string GetData(int id)
    {
        if (_cache.TryGetValue(id, out var cached))
        {
            Console.WriteLine($"  [Cached] id={id} 命中缓存");
            return cached;
        }

        var result = _inner.GetData(id);
        _cache[id] = result;
        return result;
    }
}

/// <summary>
/// 日志装饰器 —— 等价于 Python @timer / @log
/// </summary>
public class LoggingDataService : IDataService
{
    private readonly IDataService _inner;

    public LoggingDataService(IDataService inner)
    {
        _inner = inner;
    }

    public string GetData(int id)
    {
        var sw = Stopwatch.StartNew();
        Console.WriteLine($"  [Logging] GetData({id}) 开始");
        var result = _inner.GetData(id);
        sw.Stop();
        Console.WriteLine($"  [Logging] GetData({id}) 完成，耗时 {sw.ElapsedMilliseconds}ms");
        return result;
    }
}


// ============================================================================
// 6. 主程序入口
// ============================================================================

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine(new string('=', 70));
        Console.WriteLine("  C# Attribute 与拦截器 —— Python 装饰器的 C# 等价物");
        Console.WriteLine("  C# 程序员的 Python 修炼手册 —— 2.5");
        Console.WriteLine(new string('=', 70));

        // --- 1. Attribute 的本质：只是元数据标签 ---
        Console.WriteLine("\n--- 1. Attribute 本质：元数据标签（需要反射才能生效）---");
        Console.WriteLine("  [Log], [Cache], [Authorize] 只是标签，单独使用不会拦截任何调用");
        Console.WriteLine("  必须配合反射或框架（如 ASP.NET Core）才能产生实际效果\n");

        // 通过反射读取 Attribute —— 框架的工作
        var method = typeof(Program).GetMethod(nameof(DemoMethod))!;
        var attrs = method.GetCustomAttributes<LogAttribute>(inherit: true);
        Console.WriteLine($"  DemoMethod 上的 [Log] 属性数量: {attrs.Count()}");
        foreach (var attr in attrs)
        {
            Console.WriteLine($"    Message = \"{attr.Message}\"");
        }

        // --- 2. Decorator Pattern（经典装饰器模式）---
        Console.WriteLine("\n--- 2. Decorator Pattern（经典 GoF 装饰器）---");
        Console.WriteLine("  这是最传统的 C# 装饰方式：用接口 + 组合\n");

        // 链式包装：DataService → CachedDataService → LoggingDataService
        // 等价于 Python 的 @timer @cache def func()
        IDataService service = new DataService();
        service = new CachedDataService(service);  // 内层
        service = new LoggingDataService(service);  // 外层

        Console.WriteLine("  第一次调用（缓存未命中，穿透到数据库）:");
        Console.WriteLine($"  结果: {service.GetData(1)}");

        Console.WriteLine("\n  第二次调用（缓存命中）:");
        Console.WriteLine($"  结果: {service.GetData(1)}");

        // --- 3. Action Filter Pipeline（ASP.NET Core 风格）---
        Console.WriteLine("\n--- 3. Action Filter Pipeline（ASP.NET Core 风格）---");
        Console.WriteLine("  这是 ASP.NET Core 最接近 Python 装饰器的模式\n");

        // 场景1: 正常执行（timer + log 两个 filter 堆叠）
        Console.WriteLine("  场景1: 正常调用（timer + log filter）");
        var result = FilterPipeline.Execute(
            () =>
            {
                Thread.Sleep(10);  // 模拟耗时操作
                return 42;
            },
            "CalculateResult",
            new Dictionary<string, object?> { { "input", 10 } },
            new TimerFilter(),     // 装饰器1
            new LogFilter()        // 装饰器2
        );
        Console.WriteLine($"  返回值: {result}");

        // 场景2: 权限检查失败
        Console.WriteLine("\n  场景2: 权限检查（authorize + timer filter）");
        var deleteResult = FilterPipeline.Execute(
            () =>
            {
                Console.WriteLine("  [执行] 用户已被删除");
                return true;
            },
            "DeleteUser",
            new Dictionary<string, object?> { { "userId", 42 }, { "userRole", "Viewer" } },
            new AuthorizeFilter("Admin"),  // 装饰器1: 权限检查
            new TimerFilter()               // 装饰器2: 计时
        );
        if (deleteResult != null && !deleteResult.Equals(true))
        {
            Console.WriteLine($"  被取消: 返回默认值 {deleteResult}");
        }

        // --- 4. DispatchProxy 拦截器（最接近 Python 动态装饰）---
        Console.WriteLine("\n--- 4. DispatchProxy（动态代理拦截器）---");
        Console.WriteLine("  最接近 Python 装饰器的动态包装机制\n");

        var calculator = new Calculator();
        var proxy = MethodInterceptionProxy<ICalculator>.Create(calculator);
        // proxy 现在就是包装后的版本，每次调用都会被拦截

        Console.WriteLine("  调用 Add(3, 5)：");
        Console.WriteLine($"  结果: {proxy.Add(3, 5)}");

        Console.WriteLine("\n  调用 Multiply(4, 7)：");
        Console.WriteLine($"  结果: {proxy.Multiply(4, 7)}");

        // --- 总结 ---
        Console.WriteLine("\n" + new string('=', 70));
        Console.WriteLine("  总结：C# vs Python 的装饰器/AOP 对比");
        Console.WriteLine(new string('-', 70));
        Console.WriteLine("  | Python              | C#                        |");
        Console.WriteLine("  |---------------------|---------------------------|");
        Console.WriteLine("  | @decorator          | [Attribute] + 反射/框架   |");
        Console.WriteLine("  | 嵌套函数包装         | Decorator Pattern(接口)    |");
        Console.WriteLine("  | 动态替换函数         | DispatchProxy / 代理      |");
        Console.WriteLine("  | 堆叠装饰器           | Action Filter Pipeline    |");
        Console.WriteLine("  | func.__wrapped__    | 保留原始对象引用           |");
        Console.WriteLine(new string('-', 70));
        Console.WriteLine("  关键区别:");
        Console.WriteLine("  - Python: 装饰器就是函数，@ 只是语法糖");
        Console.WriteLine("  - C#: Attribute 只是元数据，需要框架配合才能拦截");
        Console.WriteLine("  - Python 更灵活（运行时包装），C# 更安全（编译时检查）");
        Console.WriteLine(new string('=', 70));
    }

    /// <summary>
    /// 用于演示 Attribute 反射读取的方法
    /// </summary>
    [Log("方法开始执行")]
    [Log("记录执行日志")]
    [Cache(DurationSeconds = 300)]
    [Authorize(Roles = "Admin")]
    public static string DemoMethod(int id)
    {
        return $"Result-{id}";
    }
}

// ============================================================================
// 7. 接口定义（供 DispatchProxy 使用）
// ============================================================================

/// <summary>
/// 计算器接口 —— DispatchProxy 必须基于接口创建
/// </summary>
public interface ICalculator
{
    int Add(int a, int b);
    int Multiply(int a, int b);
}

/// <summary>
/// 计算器实现
/// </summary>
public class Calculator : ICalculator
{
    public int Add(int a, int b) => a + b;
    public int Multiply(int a, int b) => a * b;
}
