// ============================================================
// C# 日志系统完全指南（对标 Python logging 模块）
// 对应文章：4.7 logging 模块 —— 专业的日志系统
// Python 对比：logging 模块
// ============================================================
//
// 【核心对比】
//   Python logging   →  内置模块，基于 Logger + Handler + Formatter 架构
//   C# logging      →  Microsoft.Extensions.Logging (ILogger)
//                      + Serilog（结构化日志，最流行）
//                      + NLog（配置灵活，功能全面）
//
// 本示例用 Console.WriteLine 模拟日志输出，展示 API 对比
// 实际项目中请使用 NuGet 包 Microsoft.Extensions.Logging
// ============================================================

using System;
using System.Collections.Generic;

// ============================================================
// 模拟框架：模拟 ILogger / LoggerFactory / LogLevel
// 实际项目使用 Microsoft.Extensions.Logging
// ============================================================
public enum LogLevel
{
    Trace = 0,
    Debug = 1,
    Information = 2,
    Warning = 3,
    Error = 4,
    Critical = 5,
    None = 6
}

// 模拟 ILogger 接口（实际项目使用 Microsoft.Extensions.Logging.ILogger）
// 【Python 等价】logging.Logger
public interface ILogger
{
    string Name { get; }
    LogLevel MinLevel { get; set; }
    void Log(LogLevel level, string message);
    void LogDebug(string message);
    void LogInformation(string message);
    void LogWarning(string message);
    void LogError(string message, Exception ex = null);
    void LogCritical(string message);
    void AddHandler(ILoggerHandler handler);
    void RemoveHandler(ILoggerHandler handler);
}

// 模拟 Handler 接口（对标 Python logging.Handler）
// 【Python 等价】logging.Handler (StreamHandler / FileHandler)
public interface ILoggerHandler
{
    string Name { get; }
    LogLevel MinLevel { get; set; }
    void Emit(LogLevel level, string name, string message);
}

// 控制台 Handler（对标 Python StreamHandler）
// 【Python 等价】logging.StreamHandler(sys.stdout)
public class ConsoleHandler : ILoggerHandler
{
    public string Name => "Console";
    public LogLevel MinLevel { get; set; } = LogLevel.Information;

    public void Emit(LogLevel level, string name, string message)
    {
        string color = level switch
        {
            LogLevel.Debug => "\u001b[37m",       // 灰色
            LogLevel.Information => "\u001b[32m",  // 绿色
            LogLevel.Warning => "\u001b[33m",      // 黄色
            LogLevel.Error => "\u001b[31m",        // 红色
            LogLevel.Critical => "\u001b[35m",     // 紫色
            _ => "\u001b[0m"
        };
        Console.WriteLine($"{color}[{level}] {name}: {message}\u001b[0m");
    }
}

// 文件 Handler（对标 Python FileHandler）
// 【Python 等价】logging.FileHandler("app.log")
public class FileHandler : ILoggerHandler
{
    private readonly string _filePath;
    public string Name => "File";
    public LogLevel MinLevel { get; set; } = LogLevel.Debug;

    public FileHandler(string filePath)
    {
        _filePath = filePath;
    }

    public void Emit(LogLevel level, string name, string message)
    {
        string line = $"{DateTime.Now:yyyy-MM-dd HH:mm:ss} [{level}] {name}: {message}\n";
        System.IO.File.AppendAllText(_filePath, line);
    }
}

// NullHandler（对标 Python NullHandler —— 库开发最佳实践）
// 【Python 等价】logging.NullHandler()
public class NullHandler : ILoggerHandler
{
    public string Name => "Null";
    public LogLevel MinLevel { get; set; } = LogLevel.None;
    public void Emit(LogLevel level, string name, string message) { }
}

// 模拟 Logger 实现
public class LoggerImpl : ILogger
{
    private readonly List<ILoggerHandler> _handlers = new();
    public string Name { get; }
    public LogLevel MinLevel { get; set; } = LogLevel.Debug;

    public LoggerImpl(string name)
    {
        Name = name;
    }

    public void AddHandler(ILoggerHandler handler) => _handlers.Add(handler);
    public void RemoveHandler(ILoggerHandler handler) => _handlers.Remove(handler);

    public void Log(LogLevel level, string message)
    {
        if (level < MinLevel) return;
        foreach (var handler in _handlers)
        {
            if (level >= handler.MinLevel)
                handler.Emit(level, Name, message);
        }
    }

    public void LogDebug(string message) => Log(LogLevel.Debug, message);
    public void LogInformation(string message) => Log(LogLevel.Information, message);
    public void LogWarning(string message) => Log(LogLevel.Warning, message);
    public void LogError(string message, Exception ex = null)
        => Log(LogLevel.Error, ex != null ? $"{message} {ex.Message}" : message);
    public void LogCritical(string message) => Log(LogLevel.Critical, message);
}

// 模拟 LoggerFactory
// 【Python 等价】logging.getLogger("name")
public static class LoggerFactory
{
    private static readonly Dictionary<string, LoggerImpl> _loggers = new();

    public static ILogger CreateLogger<T>() => CreateLogger(typeof(T).Name);

    public static ILogger CreateLogger(string name)
    {
        if (!_loggers.ContainsKey(name))
        {
            _loggers[name] = new LoggerImpl(name);
        }
        return _loggers[name];
    }
}


public class LoggingDemo
{
    static void Main()
    {
        Console.WriteLine("============================================");
        Console.WriteLine("C# 日志系统 vs Python logging 模块");
        Console.WriteLine("============================================");

        // ============================================================
        // 1. 基础用法 —— 快速创建 Logger
        // ============================================================
        // 【Python 等价】
        //   logging.basicConfig(level=logging.DEBUG, ...)
        //   logger = logging.getLogger("MyApp")
        // ============================================================
        Console.WriteLine("\n===== 1. 基础用法 =====");

        // C# 需要手动创建 Logger 并配置 Handler
        // Python: logging.basicConfig() 一行搞定
        var logger = LoggerFactory.CreateLogger("MyApp");
        logger.AddHandler(new ConsoleHandler { MinLevel = LogLevel.Information });

        logger.LogDebug("这是调试信息");
        logger.LogInformation("这是普通信息");
        logger.LogWarning("这是警告信息");
        logger.LogError("这是错误信息");
        logger.LogCritical("这是严重错误");

        // 【C# vs Python】
        // Python: basicConfig() 一行配置所有
        // C#: 需要分别创建 Logger + Handler 并组装


        // ============================================================
        // 2. 日志级别
        // ============================================================
        // 【Python 等价】
        //   logging.DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50
        // ============================================================
        Console.WriteLine("\n===== 2. 日志级别 =====");

        Console.WriteLine("C# 日志级别 (LogLevel 枚举):");
        foreach (var level in Enum.GetValues<LogLevel>())
        {
            Console.WriteLine($"  {level,-14s} = {(int)level}");
        }
        // 【C# vs Python】
        // C#:  枚举值 Trace=0 到 Critical=5
        // Python: 整数 10/20/30/40/50
        // 本质相同：数字越大越严重


        // ============================================================
        // 3. 多 Handler 输出 —— 同时写控制台和文件
        // ============================================================
        // 【Python 等价】
        //   logger.addHandler(console_handler)
        //   logger.addHandler(file_handler)
        //   logger.addHandler(rotating_handler)
        // ============================================================
        Console.WriteLine("\n===== 3. 多 Handler 输出 =====");

        var multiLogger = LoggerFactory.CreateLogger("MultiTarget");
        multiLogger.AddHandler(new ConsoleHandler { MinLevel = LogLevel.Warning });
        multiLogger.AddHandler(new FileHandler("cs_demo.log") { MinLevel = LogLevel.Debug });

        multiLogger.LogDebug("只写入文件（DEBUG 级别低于 ConsoleHandler 阈值）");
        multiLogger.LogWarning("同时输出到控制台和文件");
        multiLogger.LogError("同时输出到控制台和文件（含异常信息）",
            new InvalidOperationException("模拟异常"));

        // 【C# 对比】
        // Serilog: .WriteTo.Console().WriteTo.File("log.txt")
        // NLog: 同时配置 Console Target 和 File Target
        // Python: addHandler() 动态添加，C# 通常在启动时配置


        // ============================================================
        // 4. NullHandler —— 库开发最佳实践
        // ============================================================
        // 【Python 等价】
        //   library_logger = logging.getLogger("mypackage")
        //   library_logger.addHandler(logging.NullHandler())
        // ============================================================
        Console.WriteLine("\n===== 4. NullHandler（库开发最佳实践）=====");

        var libraryLogger = LoggerFactory.CreateLogger("MyLibrary");
        libraryLogger.AddHandler(new NullHandler());
        libraryLogger.LogInformation("这条日志被 NullHandler 静默处理");
        Console.WriteLine("NullHandler 已添加（静默处理，不会报错）");

        // 【C# vs Python】
        // C#:  库一般不注册任何日志 provider，由应用程序配置
        // Python: 需要 NullHandler 来避免 "No handler found" 警告


        // ============================================================
        // 5. Logger 命名约定
        // ============================================================
        // 【Python 等价】
        //   self.logger = logging.getLogger(__name__)
        //   → 自动使用模块名作为 Logger 名称
        // ============================================================
        Console.WriteLine("\n===== 5. Logger 命名约定 =====");

        // Python: logging.getLogger(__name__) → "module.ClassName"
        // C#: ILogger<T> → T 的完整类名（泛型自动推断）
        var userLogger = LoggerFactory.CreateLogger<UserService>();
        var orderLogger = LoggerFactory.CreateLogger<OrderService>();

        Console.WriteLine($"  UserService Logger: {userLogger.Name}");
        Console.WriteLine($"  OrderService Logger: {orderLogger.Name}");

        // 【C# vs Python】
        // C#:  ILogger<T> 泛型自动推断类名，更类型安全
        // Python: __name__ 是字符串，更灵活但容易拼错


        // ============================================================
        // 6. 实际场景：依赖注入风格的 Logger
        // ============================================================
        // 【Python 等价】
        //   class UserService:
        //       def __init__(self):
        //           self.logger = logging.getLogger(__name__)
        // ============================================================
        Console.WriteLine("\n===== 6. 实际场景：类中使用 Logger =====");

        // C# 风格：通过构造函数注入 ILogger<T>
        // 实际项目中：public UserService(ILogger<UserService> logger)
        var service = new UserService((ILogger)userLogger);
        try
        {
            var user = service.GetUser(1);
            service.GetUser(-1);  // 触发错误
        }
        catch (ArgumentException)
        {
            // 预期的错误
        }

        // 清理临时文件
        if (System.IO.File.Exists("cs_demo.log"))
            System.IO.File.Delete("cs_demo.log");


        // ============================================================
        // 7. dictConfig vs appsettings.json 配置对比
        // ============================================================
        Console.WriteLine("\n===== 7. 配置方式对比 =====");
        Console.WriteLine(@"
Python logging 配置:
    LOGGING_CONFIG = {
        'version': 1,
        'handlers': {
            'console': {'class': 'logging.StreamHandler'},
            'file': {'class': 'logging.FileHandler', 'filename': 'app.log'},
        },
        'root': {'level': 'DEBUG', 'handlers': ['console', 'file']},
    }
    logging.config.dictConfig(LOGGING_CONFIG)

C# appsettings.json 配置 (Serilog):
    {
      "Serilog": {
        "MinimumLevel": "Debug",
        "WriteTo": [
          { "Name": "Console" },
          { "Name": "File", "Args": { "path": "app.log" } }
        ]
      }
    }
    Log.Logger = new LoggerConfiguration()
        .ReadFrom.Configuration(configuration)
        .CreateLogger();
");


        // ============================================================
        // 总结对比表
        // ============================================================
        Console.WriteLine("============================================");
        Console.WriteLine("总结：C# 日志框架 vs Python logging");
        Console.WriteLine("============================================");
        Console.WriteLine(@"
┌──────────────────────┬──────────────────────────┬───────────────────────────────┐
│      概念            │    C# 日志框架           │    Python logging             │
├──────────────────────┼──────────────────────────┼───────────────────────────────┤
│ 核心接口             │ ILogger<T>               │ Logger                        │
│ 输出目标             │ Sink / Target            │ Handler                       │
│ 输出格式             │ OutputTemplate           │ Formatter                     │
│ 日志级别             │ LogLevel 枚举            │ 整数常量 10/20/30/40/50       │
│ 快速配置             │ 无（需手动配置 DI）       │ basicConfig() 一行搞定        │
│ 配置文件             │ appsettings.json         │ dictConfig() + 字典           │
│ 命名 Logger          │ ILogger<T> 泛型推断      │ getLogger(__name__) 字符串    │
│ 库静默处理           │ 无需（由应用配置）        │ NullHandler                   │
│ 层级传播             │ 无传播机制               │ propagate=True 自动冒泡       │
│ 文件轮转             │ rollingInterval(Serilog) │ RotatingFileHandler           │
│ 结构化日志           │ Serilog 原生支持          │ loguru / structlog 第三方     │
│ DI 集成              │ 依赖注入 ILogger<T>     │ 手动 getLogger()              │
│ 类型安全             │ 泛型编译时检查            │ 字符串名称，运行时才报错       │
└──────────────────────┴──────────────────────────┴───────────────────────────────┘
");
        Console.WriteLine("完成!");
    }
}

// ============================================================
// 服务类 —— 展示 Logger 在类中的使用方式
// ============================================================

// C# 风格：通过构造函数注入 ILogger（DI 模式）
// 【Python 等价】
//   class UserService:
//       def __init__(self):
//           self.logger = logging.getLogger(__name__)
public class UserService
{
    private readonly ILogger _logger;

    // 实际项目中：public UserService(ILogger<UserService> logger)
    public UserService(ILogger logger)
    {
        _logger = logger;
    }

    public object GetUser(int userId)
    {
        _logger.LogInformation($"查询用户: {userId}");
        if (userId <= 0)
        {
            _logger.LogError($"无效的用户ID: {userId}");
            throw new ArgumentException($"无效的用户ID: {userId}");
        }
        _logger.LogDebug($"用户 {userId} 查询成功");
        return new { Id = userId, Name = $"User_{userId}" };
    }
}

// 服务类示例
public class OrderService
{
    private readonly ILogger _logger;

    public OrderService(ILogger logger)
    {
        _logger = logger;
    }

    public void CreateOrder(int orderId)
    {
        _logger.LogInformation($"创建订单: {orderId}");
    }
}
