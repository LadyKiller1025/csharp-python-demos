/*
=================================================================
6.5 迁移策略 —— C# 侧的迁移策略实现
对应文章：6.5 迁移策略
=================================================================

本文件展示从 C# 侧实现迁移策略的代码：
  1. 调用 Python 脚本/服务
  2. Repository / Service / DI 模式对照
  3. gRPC 通信（C# 服务端）
  4. 共享数据层（JSON 序列化）
  5. 原生互操作（Python.NET / P/Invoke）
*/

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Text.Json.Serialization;

public class MigrationDemo
{
    static void Main()
    {
        Console.WriteLine("===========================================================");
        Console.WriteLine("  C# ↔ Python 迁移策略 —— C# 侧实现");
        Console.WriteLine("===========================================================\n");

        // =====================================================================
        // 第一部分：调用 Python 脚本
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第一部分：C# 调用 Python 脚本");
        Console.WriteLine("===========================================================\n");

        Console.WriteLine("  C# 调用 Python 的三种方式：\n");

        Console.WriteLine("  方式1：Process.Start（最简单）");
        Console.WriteLine("  ─────────────────────────────");
        Console.WriteLine("""
            // 直接调用 Python 脚本
            var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = "python",
                    Arguments = "script.py --arg1 value1",
                    RedirectStandardOutput = true,
                    RedirectStandardInput = true,
                    UseShellExecute = false,
                }
            };
            process.Start();
            string output = process.StandardOutput.ReadToEnd();
            process.WaitForExit();
            """);

        Console.WriteLine("  方式2：通过 JSON 交换数据");
        Console.WriteLine("  ───────────────────────────");
        Console.WriteLine("""
            // C# 发送 JSON 到 Python stdin
            var data = new { items = new[] { 10, 20, 30 } };
            string json = JsonSerializer.Serialize(data);

            process.StandardInput.WriteLine(json);
            process.StandardInput.Close();

            string result = process.StandardOutput.ReadToEnd();
            var response = JsonSerializer.Deserialize<Output>(result);
            """);

        Console.WriteLine("  方式3：gRPC 通信（推荐生产使用）");
        Console.WriteLine("  ─────────────────────────────────");
        Console.WriteLine("""
            // C# gRPC 客户端
            var channel = GrpcChannel.ForAddress("https://localhost:5001");
            var client = new UserService.UserServiceClient(channel);
            var response = await client.GetUserAsync(
                new GetUserRequest { UserId = 1 });
            Console.WriteLine($"User: {response.Name}");
            """);

        // 实际演示：调用 Python 获取版本信息
        Console.WriteLine("--- 实际演示：C# 调用 Python ---\n");
        try
        {
            var psi = new ProcessStartInfo
            {
                FileName = "python",
                Arguments = "--version",
                RedirectStandardOutput = true,
                UseShellExecute = false,
            };
            var process = Process.Start(psi);
            if (process != null)
            {
                string output = process.StandardOutput.ReadToEnd().Trim();
                process.WaitForExit();
                Console.WriteLine($"  Python 版本: {output}");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"  Python 未安装或无法调用: {ex.Message}");
        }
        Console.WriteLine();


        // =====================================================================
        // 第二部分：Repository / Service / DI 模式
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第二部分：C# 代码模式（Python 对照）");
        Console.WriteLine("===========================================================\n");

        // --- Repository 模式 ---
        Console.WriteLine("--- Repository 模式 ---\n");
        Console.WriteLine("  C# 需要显式定义接口，Python 不需要（鸭子类型）。\n");

        var container = new SimpleContainer();
        container.RegisterSingleton<IUserRepository, InMemoryUserRepository>();
        container.RegisterFactory<IUserService>(
            () => new UserService(container.Resolve<IUserRepository>()));

        var userService = container.Resolve<IUserService>();

        // 创建用户
        Console.WriteLine("  [创建用户]");
        try
        {
            var user = userService.CreateUser("Charlie", "charlie@example.com");
            Console.WriteLine($"    创建成功: {user}");
        }
        catch (ArgumentException ex)
        {
            Console.WriteLine($"    创建失败: {ex.Message}");
        }

        // 获取用户（脱敏）
        Console.WriteLine("\n  [获取用户（含脱敏）]");
        var alice = userService.GetUser(1);
        Console.WriteLine($"    Alice 的脱敏信息: {alice}");

        // 统计
        Console.WriteLine("\n  [用户统计]");
        var stats = userService.GetUserStats();
        Console.WriteLine($"    总用户数: {stats["total_users"]}");
        Console.WriteLine($"    用户列表: {string.Join(", ", (List<string>)stats["user_names"])}");

        // 对比 Python 代码
        Console.WriteLine("""
  Python 等价代码：
  ─────────────────
  # Python 不需要接口定义
  class UserRepository:        # 无需 IUserRepository 接口
      def get_user(self, user_id):
          return self._users.get(user_id)

  class UserService:
      def __init__(self, repo):  # 构造函数注入
          self._repo = repo

  # DI 容器
  container.register_singleton(UserRepository, UserRepository())
  user_service = container.resolve(UserService)
""");
        Console.WriteLine();


        // =====================================================================
        // 第三部分：gRPC 通信
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第三部分：gRPC 通信（C# 服务端）");
        Console.WriteLine("===========================================================\n");

        Console.WriteLine("  gRPC 项目结构：");
        Console.WriteLine("""
  MyGrpcService/
  ├── Protos/
  │   └── user_service.proto      # 共享契约（Python 和 C# 通用）
  ├── Services/
  │   └── UserService.cs          # C# 服务端实现
  ├── MyGrpcService.csproj        # C# 项目
  └── Program.cs

  Python 客户端：
  pip install grpcio grpcio-tools
  python -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/user_service.proto
        """);

        Console.WriteLine("  C# gRPC 服务端实现：\n");
        Console.WriteLine("""
            // UserService.cs
            public class UserService : UserService.UserServiceBase
            {
                private readonly IUserRepository _repo;

                public UserService(IUserRepository repo)
                {
                    _repo = repo;
                }

                public override Task<UserResponse> GetUser(
                    GetUserRequest request, ServerCallContext context)
                {
                    var user = _repo.GetUser(request.UserId);
                    if (user == null)
                        throw new RpcException(
                            new Status(StatusCode.NotFound, "User not found"));

                    return Task.FromResult(new UserResponse
                    {
                        Id = user.Id,
                        Name = user.Name,
                        Email = user.Email,
                    });
                }

                public override Task<ListUsersResponse> ListUsers(
                    ListUsersRequest request, ServerCallContext context)
                {
                    var users = _repo.ListUsers()
                        .Skip((request.Page - 1) * request.PageSize)
                        .Take(request.PageSize)
                        .Select(u => new UserResponse
                        {
                            Id = u.Id, Name = u.Name, Email = u.Email
                        });

                    return Task.FromResult(new ListUsersResponse
                    {
                        Total = _repo.ListUsers().Count(),
                    });
                }
            }
            """);

        // 模拟 gRPC 通信
        Console.WriteLine("  模拟 gRPC 通信演示：\n");

        var grpcService = new GrpcUserService();
        var grpcRequest = new GrpcGetUserRequest { UserId = 1 };
        var grpcResponse = grpcService.GetUser(grpcRequest);
        Console.WriteLine($"    GetUser 请求: {{ UserId: 1 }}");
        Console.WriteLine($"    GetUser 响应: {{ Id: {grpcResponse.Id}, Name: \"{grpcResponse.Name}\", Age: {grpcResponse.Age} }}");
        Console.WriteLine();


        // =====================================================================
        // 第四部分：JSON 序列化对比
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第四部分：JSON 数据交换");
        Console.WriteLine("===========================================================\n");

        // C# 对象 → JSON
        var userObj = new UserDto
        {
            UserId = 1,
            UserName = "Alice",
            Email = "alice@example.com",
            CreatedAt = DateTime.Now,
        };

        var options = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
            WriteIndented = true,
        };

        string json = JsonSerializer.Serialize(userObj, options);
        Console.WriteLine("  C# → JSON（camelCase）:");
        Console.WriteLine($"  {json}");

        // JSON → C# 对象
        string pythonJson = """
            {
                "user_id": 1,
                "user_name": "Bob",
                "email": "bob@example.com",
                "created_at": "2024-01-15T10:30:00"
            }
            """;

        // 注意：Python 的 snake_case 需要特殊的反序列化
        Console.WriteLine("\n  Python JSON（snake_case）→ C#:");
        Console.WriteLine("""
            // 方式1：使用 JsonPropertyName 属性
            public class UserDto
            {
                [JsonPropertyName("user_id")]
                public int UserId { get; set; }

                [JsonPropertyName("user_name")]
                public string UserName { get; set; }
            }

            // 方式2：自定义命名策略
            // Python snake_case → C# camelCase 通常需要手动映射
            """);

        Console.WriteLine("  ⚠ 命名风格差异：");
        Console.WriteLine("    C#:     userId, userName, createdAt (camelCase)");
        Console.WriteLine("    Python: user_id, user_name, created_at (snake_case)");
        Console.WriteLine("    解决:   API 层统一命名，或使用 JSON 转换器");
        Console.WriteLine();


        // =====================================================================
        // 第五部分：渐进式迁移策略
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第五部分：渐进式迁移策略");
        Console.WriteLine("===========================================================\n");

        Console.WriteLine("  推荐的迁移顺序：\n");

        var migrationSteps = new List<(string Phase, string Action, string Details)>
        {
            ("1. 识别",    "找出适合 Python 的模块",
                "AI/ML、数据处理、脚本自动化"),
            ("2. 接口",    "定义通信契约",
                "gRPC .proto / OpenAPI spec"),
            ("3. 实现",    "用 Python 重写选中模块",
                "保持输入输出格式不变"),
            ("4. 测试",    "集成测试",
                "确保 C# → Python 调用正确"),
            ("5. 切换",    "灰度切换流量",
                "从 1% 开始，逐步增加"),
            ("6. 监控",    "性能和错误监控",
                "日志聚合 + 分布式追踪"),
            ("7. 清理",    "移除旧代码",
                "确认稳定后删除 C# 旧实现"),
        };

        foreach (var (phase, action, details) in migrationSteps)
        {
            Console.WriteLine($"  {phase}: {action}");
            Console.WriteLine($"         {details}\n");
        }

        Console.WriteLine("  对比 C# 的类似场景：");
        Console.WriteLine("    .NET Framework → .NET 8 迁移");
        Console.WriteLine("    ASP.NET MVC → ASP.NET Core 迁移");
        Console.WriteLine("    Windows Service → Docker 容器化");
        Console.WriteLine("    共同点：渐进式、可回滚、有监控");
        Console.WriteLine();


        // =====================================================================
        // 第六部分：混合架构最佳实践
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第六部分：混合架构最佳实践");
        Console.WriteLine("===========================================================\n");

        var practices = new List<(string Practice, string Why, string How)>
        {
            ("接口层用 gRPC",
                "类型安全 + 高性能 + 自动代码生成",
                ".proto 文件 C# 和 Python 共享"),
            ("共享数据用 Protobuf",
                "比 JSON 更小更快",
                "序列化/反序列化自动处理"),
            ("AI 模型用 ONNX",
                "Python 训练 → C# 部署推理",
                "ONNX Runtime 支持两种语言"),
            ("日志统一格式",
                "便于聚合分析",
                "结构化日志 (JSON 格式)"),
            ("认证共享 JWT",
                "一次签发，两端验证",
                "C# 和 Python 都有 JWT 库"),
            ("CI/CD 分开构建",
                "各管各的构建和测试",
                "GitHub Actions 矩阵构建"),
        };

        Console.WriteLine($"  {"实践":20s} {"原因":35s} {"方法"}");
        Console.WriteLine("  " + new string('-', 80));
        foreach (var (practice, why, how) in practices)
        {
            Console.WriteLine($"  {practice:20s} {why:35s} {how}");
        }
        Console.WriteLine();


        // =====================================================================
        // 总结
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  总结：C# 开发者的 Python 迁移指南");
        Console.WriteLine("===========================================================");
        Console.WriteLine();
        Console.WriteLine("  🔑 核心原则：");
        Console.WriteLine("    1. 不重写 —— 能调用就不重写");
        Console.WriteLine("    2. 先解耦 —— 通过清晰接口分离 C# 和 Python");
        Console.WriteLine("    3. 渐进式 —— 一个模块一个模块地迁移");
        Console.WriteLine("    4. 可回滚 —— 任何阶段都能切回 C# 实现");
        Console.WriteLine("    5. 监控先行 —— 迁移前先建好监控");
        Console.WriteLine();
        Console.WriteLine("  🛠 推荐技术栈：");
        Console.WriteLine("    通信:   gRPC（首选）/ REST（备选）");
        Console.WriteLine("    数据:   Protobuf（首选）/ JSON（备选）");
        Console.WriteLine("    AI:     ONNX Runtime（Python 训练 → C# 推理）");
        Console.WriteLine("    部署:   Docker（每种语言一个容器）");
        Console.WriteLine("    监控:   OpenTelemetry + Jaeger");
        Console.WriteLine("    日志:   Serilog (C#) + structlog (Python) → ELK");
    }
}

// =====================================================================
// 辅助类定义
// =====================================================================

/// <summary>
/// 用户 DTO（Data Transfer Object）
/// Python 对应：Pydantic BaseModel 或 dataclass
/// </summary>
public class UserDto
{
    [JsonPropertyName("user_id")]
    public int UserId { get; set; }

    [JsonPropertyName("user_name")]
    public string UserName { get; set; } = "";

    [JsonPropertyName("email")]
    public string Email { get; set; } = "";

    [JsonPropertyName("created_at")]
    public DateTime CreatedAt { get; set; }

    public override string ToString() =>
        $"{{ UserId: {UserId}, UserName: \"{UserName}\", Email: \"{Email}\" }}";
}

/// <summary>
/// 用户实体
/// Python 对应：@dataclass class User
/// </summary>
public record User(int Id, string Name, string Email);

/// <summary>
/// 用户仓库接口
/// Python 对应：不需要接口，鸭子类型即可
/// C# 有接口 → Python 没有接口 = Python 的优势（更灵活）
/// </summary>
public interface IUserRepository
{
    User? GetUser(int userId);
    List<User> ListUsers();
    User SaveUser(string name, string email);
    bool DeleteUser(int userId);
}

/// <summary>
/// 内存用户仓库（类似 Python 的内存字典存储）
/// </summary>
public class InMemoryUserRepository : IUserRepository
{
    private readonly Dictionary<int, User> _users = new();
    private int _nextId = 1;

    public User? GetUser(int userId) =>
        _users.TryGetValue(userId, out var user) ? user : null;

    public List<User> ListUsers() => _users.Values.ToList();

    public User SaveUser(string name, string email)
    {
        var user = new User(_nextId++, name, email);
        _users[user.Id] = user;
        return user;
    }

    public bool DeleteUser(int userId) => _users.Remove(userId);
}

/// <summary>
/// 用户服务
/// Python 对应：class UserService: def __init__(self, repo): self._repo = repo
/// </summary>
public class UserService
{
    private readonly IUserRepository _repo;

    // 构造函数注入（和 Python 一样）
    public UserService(IUserRepository repo) => _repo = repo;

    public User? GetUser(int userId)
    {
        var user = _repo.GetUser(userId);
        return user == null ? null : new User(user.Id, user.Name,
            user.Email.Split('@')[0] + "***");
    }

    public User CreateUser(string name, string email)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new ArgumentException("用户名不能为空");
        if (!email.Contains('@'))
            throw new ArgumentException($"邮箱格式无效: {email}");
        return _repo.SaveUser(name, email);
    }

    public Dictionary<string, object> GetUserStats()
    {
        var users = _repo.ListUsers();
        return new Dictionary<string, object>
        {
            ["total_users"] = users.Count,
            ["user_names"] = users.Select(u => u.Name).ToList(),
        };
    }
}

/// <summary>
/// 简单的依赖注入容器
/// Python 对应：class Container (见 migration_demo.py)
/// C# 生产环境：使用内置 DI 或 Autofac
/// </summary>
public class SimpleContainer
{
    private readonly Dictionary<Type, Func<object>> _factories = new();
    private readonly Dictionary<Type, object> _singletons = new();

    public void RegisterSingleton<TInterface, TImpl>() where TImpl : TInterface, new()
    {
        _singletons[typeof(TInterface)] = new TImpl();
    }

    public void RegisterSingleton<TInterface>(TInterface instance)
    {
        _singletons[typeof(TInterface)] = instance!;
    }

    public void RegisterFactory<TInterface>(Func<object> factory)
    {
        _factories[typeof(TInterface)] = factory;
    }

    public T Resolve<T>()
    {
        var type = typeof(T);
        if (_factories.TryGetValue(type, out var factory))
            return (T)factory();
        if (_singletons.TryGetValue(type, out var singleton))
            return (T)singleton;
        throw new KeyNotFoundException($"未注册的服务: {type.Name}");
    }
}

// =====================================================================
// 模拟 gRPC 通信的辅助类
// =====================================================================

public class GrpcGetUserRequest
{
    public int UserId { get; set; }
}

public class GrpcUserResponse
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public int Age { get; set; }
    public string Email { get; set; } = "";
}

/// <summary>
/// 模拟 gRPC 服务端实现
/// Python 对应：class UserServiceServicer(user_pb2_grpc.UserServiceServicer)
/// </summary>
public class GrpcUserService
{
    private readonly List<GrpcUserResponse> _users = new()
    {
        new() { Id = 1, Name = "Alice", Age = 30, Email = "alice@example.com" },
        new() { Id = 2, Name = "Bob", Age = 25, Email = "bob@example.com" },
    };

    public GrpcUserResponse GetUser(GrpcGetUserRequest request)
    {
        return _users.FirstOrDefault(u => u.Id == request.UserId)
            ?? throw new Exception($"User {request.UserId} not found");
    }
}
