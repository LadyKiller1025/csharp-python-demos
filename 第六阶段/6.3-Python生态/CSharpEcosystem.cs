/*
=================================================================
6.3 Python 生态 —— C#/.NET 生态速查（Python 开发者的对照表）
对应文章：6.3 Python生态
=================================================================

本文件从 Python 开发者的视角，展示 C#/.NET 的生态全貌。
帮助 Python 开发者快速找到"我熟悉的 Python 库在 C# 中的等价物"。
*/

using System;
using System.Collections.Generic;
using System.Linq;

public class CSharpEcosystem
{
    static void Main()
    {
        Console.WriteLine("===========================================================");
        Console.WriteLine("  C#/.NET 生态全景 —— Python 开发者的 C# 导航图");
        Console.WriteLine("===========================================================\n");

        // =====================================================================
        // 第一部分：Web 框架
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第一部分：Web 框架");
        Console.WriteLine("===========================================================\n");

        Console.WriteLine("  C# Web 框架对照 Python：\n");

        var webFrameworks = new List<(string Name, string Python, string Description)>
        {
            ("ASP.NET Core",       "FastAPI",          "现代高性能 Web 框架，支持 Minimal APIs"),
            ("Blazor",             "— (Streamlit?)",   "前端 C#（WebAssembly），Python 无等价物"),
            ("Minimal APIs",       "Flask/FastAPI",    "轻量级 API，一行代码一个端点"),
            ("ASP.NET MVC",        "Django",           "全功能 MVC 框架，约定大于配置"),
            ("SignalR",            "WebSockets",       "实时通信（WebSocket 封装）"),
            ("gRPC",               "grpcio",           "高性能 RPC 通信"),
        };

        Console.WriteLine($"  {"C# 框架":20s} {"Python 等价":18s} {"说明"}");
        Console.WriteLine("  " + new string('-', 70));
        foreach (var (name, python, desc) in webFrameworks)
        {
            Console.WriteLine($"  {name:20s} {python:18s} {desc}");
        }

        Console.WriteLine("\n  Minimal API 示例（C# 最接近 FastAPI 的写法）：");
        Console.WriteLine("""
            // C# Minimal API（类似 FastAPI）
            var builder = WebApplication.CreateBuilder(args);
            var app = builder.Build();

            app.MapGet("/hello/{name}", (string name) => $"Hello, {name}!");
            app.MapGet("/users", () => new[] { "Alice", "Bob" });
            app.MapPost("/users", (User user) => Results.Ok($"Created {user.name}"));

            app.Run();
            """);

        Console.WriteLine("  等价的 FastAPI（Python）：");
        Console.WriteLine("""
            # Python FastAPI
            app = FastAPI()

            @app.get("/hello/{name}")
            def hello(name: str): return f"Hello, {name}!"

            @app.get("/users")
            def get_users(): return ["Alice", "Bob"]

            @app.post("/users")
            def create_user(user: User): return {"message": f"Created {user.name}"}
            """);
        Console.WriteLine();


        // =====================================================================
        // 第二部分：数据科学与 ML
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第二部分：数据科学与机器学习");
        Console.WriteLine("===========================================================\n");

        Console.WriteLine("  ⚠ 注意：这是 C# 生态最薄弱的领域\n");

        var dataScience = new List<(string Python, string CSharp, string Gap)>
        {
            ("NumPy",              "System.Numerics / Math.NET",  "C# 可用但生态小得多"),
            ("Pandas",             "DataTable / Deedle",          "差距大，无 DataFrame 等价物"),
            ("Matplotlib/Plotly",  "ScottPlot / LiveCharts",      "C# 可用但种类少"),
            ("PyTorch/TensorFlow", "ML.NET / TorchSharp",         "ML.NET 仅限传统 ML"),
            ("scikit-learn",       "ML.NET",                      "最接近的替代"),
            ("Hugging Face",       "—",                           "C# 无等价物"),
            ("Jupyter",            "Polyglot Notebooks",          "C# 可在 Jupyter 中运行"),
            ("ONNX Runtime",       "Microsoft.ML.OnnxRuntime",    "C# 和 Python 互通"),
        };

        Console.WriteLine($"  {"Python 库":20s} {"C#/.NET 替代":25s} {"差距评估"}");
        Console.WriteLine("  " + new string('-', 70));
        foreach (var (python, csharp, gap) in dataScience)
        {
            Console.WriteLine($"  {python:20s} {csharp:25s} {gap}");
        }
        Console.WriteLine();


        // =====================================================================
        // 第三部分：ORM 与数据库
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第三部分：ORM 与数据库访问");
        Console.WriteLine("===========================================================\n");

        Console.WriteLine("  C# 在 ORM 领域比 Python 更成熟：\n");

        var ormComparison = new List<(string Name, string Python, string Notes)>
        {
            ("EF Core",         "SQLAlchemy",       "功能最全面的 ORM，LINQ 查询"),
            ("Dapper",          "— (raw SQL style)","轻量级 ORM，性能极高"),
            ("NHibernate",      "SQLAlchemy (old)",  "老牌 ORM，企业级"),
            ("EF Core Code First","Alembic",         "数据库迁移"),
            ("Pomelo MySQL",    "PyMySQL",           "MySQL 驱动"),
            ("Npgsql",          "psycopg2",          "PostgreSQL 驱动"),
        };

        Console.WriteLine($"  {"C# ORM":20s} {"Python 等价":18s} {"说明"}");
        Console.WriteLine("  " + new string('-', 60));
        foreach (var (name, python, notes) in ormComparison)
        {
            Console.WriteLine($"  {name:20s} {python:18s} {notes}");
        }

        Console.WriteLine("\n  EF Core vs SQLAlchemy 代码对比：");
        Console.WriteLine("""
            // C# EF Core
            var users = await context.Users
                .Where(u => u.Age > 18)
                .OrderBy(u => u.Name)
                .ToListAsync();

            # Python SQLAlchemy
            # users = session.query(User)
            #     .filter(User.age > 18)
            #     .order_by(User.name)
            #     .all()
            """);
        Console.WriteLine();


        // =====================================================================
        // 第四部分：测试框架
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第四部分：测试框架");
        Console.WriteLine("===========================================================\n");

        var testFrameworks = new List<(string Name, string Python, string特点)>
        {
            ("xUnit",       "pytest",           "现代测试框架，基于属性"),
            ("NUnit",       "unittest",         "老牌测试框架，基于属性"),
            ("MSTest",      "unittest",         "微软官方"),
            ("Moq",         "pytest-mock",      "Mock 框架"),
            ("NSubstitute", "unittest.mock",    "Mock 框架（更简洁）"),
            ("FluentAssertions","—",            "流式断言（Python 无直接等价）"),
            ("Bogus",       "Faker",            "假数据生成"),
            ("coverlet",    "pytest-cov",       "代码覆盖率"),
            ("Playwright",  "playwright",       "浏览器自动化测试"),
        };

        Console.WriteLine($"  {"C# 测试库":20s} {"Python 等价":18s} {"说明"}");
        Console.WriteLine("  " + new string('-', 55));
        foreach (var (name, python, 特点) in testFrameworks)
        {
            Console.WriteLine($"  {name:20s} {python:18s} {特点}");
        }
        Console.WriteLine();


        // =====================================================================
        // 第五部分：开发工具
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第五部分：开发工具");
        Console.WriteLine("===========================================================\n");

        var devTools = new List<(string Purpose, string CSharp, string Python)>
        {
            ("包管理",       "NuGet / dotnet CLI",     "pip / poetry / uv"),
            ("代码检查",     "Roslyn Analyzers",        "ruff / pylint / mypy"),
            ("格式化",       "dotnet format",           "ruff format / black"),
            ("构建系统",     "MSBuild / dotnet build",  "hatchling / setuptools"),
            ("任务运行",     "dotnet run / Cake",       "invoke / make / just"),
            ("文档生成",     "DocFX",                   "mkdocs / sphinx"),
            ("代码生成",     "T4 / Source Generator",   "Jinja2 / Cookiecutter"),
            ("分析工具",     "dotnet-trace / perfview", "cProfile / py-spy"),
            ("依赖图",       "dotnet list package /v",  "pipdeptree / uv tree"),
        };

        Console.WriteLine($"  {"用途":12s} {"C#/.NET":28s} {"Python":28s}");
        Console.WriteLine("  " + new string('-', 70));
        foreach (var (purpose, csharp, python) in devTools)
        {
            Console.WriteLine($"  {purpose:12s} {csharp:28s} {python:28s}");
        }
        Console.WriteLine();


        // =====================================================================
        // 第六部分：中间件与生态组件
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第六部分：中间件与常用组件");
        Console.WriteLine("===========================================================\n");

        var middleware = new List<(string Category, string CSharp, string Python)>
        {
            ("认证/授权",    "ASP.NET Identity / JWT",  "Authlib / PyJWT"),
            ("缓存",         "IDistributedCache / Redis","redis-py / cachetools"),
            ("日志",         "ILogger + Serilog",       "logging + loguru"),
            ("配置",         "IConfiguration",          "pydantic-settings"),
            ("DI 容器",      "内置 DI",                 "dependency-injector"),
            ("消息队列",     "MassTransit / Rebus",     "Celery / RabbitMQ"),
            ("限流",         "AspNetCoreRateLimit",     "fastapi-limiter"),
            ("Swagger",      "Swashbuckle / NSwag",     "FastAPI 内置"),
            ("Health Check", "ASP.NET Health Checks",   "自定义中间件"),
            ("gRPC",         "Grpc.Net",                "grpcio"),
            ("WebSocket",    "SignalR",                 "websockets"),
        };

        Console.WriteLine($"  {"类别":12s} {"C#/.NET":30s} {"Python":28s}");
        Console.WriteLine("  " + new string('-', 72));
        foreach (var (category, csharp, python) in middleware)
        {
            Console.WriteLine($"  {category:12s} {csharp:30s} {python:28s}");
        }
        Console.WriteLine();


        // =====================================================================
        // 第七部分：C# 独有优势领域
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第七部分：C# 独有优势领域");
        Console.WriteLine("===========================================================\n");

        Console.WriteLine("""
  以下领域 C# 比 Python 更强或有独到之处：

  1. 性能
     ├── Span<T>/Memory<T> → 零分配内存操作
     ├── AOT 编译 → Native AOT（比 CPython 快 10-100 倍）
     └── SIMD → 向量化计算（System.Numerics.Vector）

  2. 并发
     ├── async/await → 原生异步（Python asyncio 是后加的）
     ├── Task Parallel Library → 数据并行
     └── Channel<T> → 生产者消费者模式

  3. 类型安全
     ├── 泛型 → 编译时类型检查（Python 泛型是运行时的）
     ├── Nullable Reference Types → 空引用检查
     └── Pattern Matching → 强大的模式匹配

  4. 工具链
     ├── Roslyn → 编译器即服务（可编程的编译器）
     ├── Source Generators → 编译时代码生成
     └── Hot Reload → 运行时代码修改

  5. 企业级
     ├── WCF → 企业级 SOA（Python 无等价物）
     ├── EF Core → 比 SQLAlchemy 更成熟
     └── 内置 DI → Python 需要第三方库
        """);

        // 实际演示：展示 C# 的一些 Python 没有的能力
        Console.WriteLine("--- C# 类型系统演示 ---\n");

        // 泛型方法
        Console.WriteLine("  泛型方法（Python 没有编译时泛型）:");
        Console.WriteLine($"    Max(3, 7) = {Max(3, 7)}");
        Console.WriteLine($"    Max(3.14, 2.72) = {Max(3.14, 2.72)}");
        Console.WriteLine($"    Max(\"apple\", \"banana\") = {Max("apple", "banana")}");

        // ValueTuples
        Console.WriteLine("\n  ValueTuple（Python 的 tuple 是引用类型）:");
        var point = (X: 10, Y: 20);
        Console.WriteLine($"    point = ({point.X}, {point.Y})");

        // LINQ
        Console.WriteLine("\n  LINQ（Python 的列表推导式更简洁但功能更少）:");
        var numbers = Enumerable.Range(1, 10);
        var result = numbers
            .Where(n => n % 2 == 0)
            .Select(n => n * n)
            .ToList();
        Console.WriteLine($"    偶数的平方: [{string.Join(", ", result)}]");

        // Pattern Matching
        Console.WriteLine("\n  模式匹配（C# 9+）:");
        object obj = 42;
        string description = obj switch
        {
            int n when n > 0 => $"正整数: {n}",
            int n when n < 0 => $"负整数: {n}",
            0 => "零",
            string s => $"字符串: {s}",
            _ => "其他类型"
        };
        Console.WriteLine($"    {obj} → {description}");


        // =====================================================================
        // 第八部分：完整生态对比表
        // =====================================================================
        Console.WriteLine("\n===========================================================");
        Console.WriteLine("  第八部分：Python vs C# 完整对比");
        Console.WriteLine("===========================================================\n");

        var fullComparison = new List<(string Area, string PythonStrength, string CSharpStrength)>
        {
            ("Web 开发",     "FastAPI 更简洁",        "ASP.NET Core 性能更好"),
            ("数据科学",     "Python 完胜",           "C# 仅 ML.NET"),
            ("AI/ML",        "Python 完胜",           "C# 可用 ONNX 消费模型"),
            ("ORM",          "SQLAlchemy 强大但复杂", "EF Core 更易用"),
            ("测试",         "pytest 简洁",           "xUnit + FluentAssertions 更丰富"),
            ("类型系统",     "动态类型，灵活",        "静态类型，安全"),
            ("性能",         "CPython 较慢",          "Native AOT 极快"),
            ("并发",         "asyncio + GIL 限制",    "async/await 无 GIL 限制"),
            ("工具链",       "ruff 越来越强",         "Roslyn 编译器即服务"),
            ("部署",         "Docker + venv",         "Docker + 自包含发布"),
        };

        Console.WriteLine($"  {"领域":12s} {"Python 优势":30s} {"C# 优势":30s}");
        Console.WriteLine("  " + new string('-', 75));
        foreach (var (area, pyStr, csStr) in fullComparison)
        {
            Console.WriteLine($"  {area:12s} {pyStr:30s} {csStr:30s}");
        }


        // =====================================================================
        // 总结
        // =====================================================================
        Console.WriteLine("\n===========================================================");
        Console.WriteLine("  总结：给 Python 开发者的 C# 导航建议");
        Console.WriteLine("===========================================================");
        Console.WriteLine();
        Console.WriteLine("  🎯 你的目标                    → 推荐的 C# 库");
        Console.WriteLine("  ─────────────────────────────────────────────────");
        Console.WriteLine("  Web API 开发                   → ASP.NET Core Minimal APIs");
        Console.WriteLine("  ORM/数据库                     → EF Core + Npgsql");
        Console.WriteLine("  测试                          → xUnit + Moq + FluentAssertions");
        Console.WriteLine("  日志                          → Serilog");
        Console.WriteLine("  配置管理                      → IOptions<T> + appsettings.json");
        Console.WriteLine("  DI                           → 内置 DI 容器");
        Console.WriteLine("  实时通信                      → SignalR");
        Console.WriteLine("  任务调度                      → Hangfire");
        Console.WriteLine("  高性能                        → Native AOT + Span<T>");
        Console.WriteLine();
        Console.WriteLine("  💡 关键认知：");
        Console.WriteLine("  ├── C# 的优势在类型安全、性能、企业级工具链");
        Console.WriteLine("  ├── C# 的劣势在数据科学/AI 生态");
        Console.WriteLine("  ├── 最佳策略：Python 做 AI/数据，C# 做服务/性能");
        Console.WriteLine("  └── 两者通过 gRPC/REST/ONNX 互通");
    }

    /// <summary>
    /// 泛型方法演示 —— Python 没有编译时泛型
    /// Python 的 typing.Generic 是运行时的，不提供性能优化
    /// </summary>
    static T Max<T>(T a, T b) where T : IComparable<T>
    {
        return a.CompareTo(b) > 0 ? a : b;
    }
}
