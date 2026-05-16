"""
=================================================================
6.5 迁移策略 -- C# <-> Python 混合开发与渐进式迁移
对应文章：6.5 迁移策略
=================================================================

当你有一个成熟的 C# 项目，想引入 Python（或反过来），怎么办？

本文件展示四种核心策略：
  1. 进程间通信（子进程 / REST / gRPC）
  2. 代码模式对照（Repository / Service / DI）
  3. 共享数据层（数据库 / Protobuf / JSON）
  4. 原生互操作（pybind11 / ctypes / pythonnet）
"""

import os
import sys
import json
import subprocess
from dataclasses import dataclass, field, asdict
from typing import Optional, Protocol
from abc import ABC, abstractmethod
from datetime import datetime

print("=" * 65)
print("  C# <-> Python 迁移策略 -- 四种混合开发模式")
print("=" * 65)


# =====================================================================
# 第一部分：迁移策略概览
# =====================================================================
print("\n" + "=" * 65)
print("  第一部分：四种迁移策略概览")
print("=" * 65)

print("""
┌─────────────────────────────────────────────────────────────────┐
│  策略对比                                                        │
│                                                                  │
│  策略              耦合度    复杂度    性能     适用场景           │
│  ────────          ──────    ──────    ──────   ────────          │
│  1. 子进程调用      低       低       中等     简单脚本调用       │
│  2. REST/gRPC       低       中       高       微服务架构         │
│  3. 共享数据库      中       中       高       数据密集型         │
│  4. 原生互操作      高       高       最高     高性能计算         │
│                                                                  │
│  C# 的对应技术：                                                 │
│  1. Process.Start()                                             │
│  2. HttpClient / gRPC                                           │
│  3. 共享 EF Core / Dapper 连接                                   │
│  4. Python.NET (pythonnet) / C++/CLI                             │
└─────────────────────────────────────────────────────────────────┘
""")

# 策略选择决策树
print("--- 策略选择决策树 ---")
print("""
  你的需求是什么？
  │
  ├── 只是调用 Python 脚本/工具？
  │   └── → 策略1：子进程调用（subprocess / Process.Start）
  │
  ├── Python 和 C# 需要双向通信？
  │   ├── 同一网络内？
  │   │   └── → 策略2：REST API 或 gRPC
  │   └── 需要共享状态？
  │       └── → 策略3：共享数据库
  │
  ├── 需要极致性能（每秒百万次调用）？
  │   └── → 策略4：原生互操作
  │
  └── 不确定？
      └── → 从策略2（gRPC）开始，最灵活
""")


# =====================================================================
# 第二部分：策略1 —— 子进程调用
# =====================================================================
print("\n" + "=" * 65)
print("  第二部分：策略1 —— 子进程调用（最简单）")
print("=" * 65)

print("""
  Python 调用 C#:
    import subprocess
    result = subprocess.run(
        ["dotnet", "run", "--project", "MyCSharpProject"],
        capture_output=True, text=True
    )
    print(result.stdout)

  C# 调用 Python:
    var process = new Process
    {
        StartInfo = new ProcessStartInfo
        {
            FileName = "python",
            Arguments = "my_script.py",
            RedirectStandardOutput = true,
            UseShellExecute = false,
        }
    };
    process.Start();
    string output = process.StandardOutput.ReadToEnd();
""")

# 实际演示：Python 调用系统命令
print("--- 实际演示：Python subprocess 调用 ---\n")

# 演示1：获取 Python 版本
print("  [演示1] 获取 Python 版本信息")
result = subprocess.run(
    [sys.executable, "--version"],
    capture_output=True, text=True, timeout=10
)
print(f"    命令: python --version")
print(f"    输出: {result.stdout.strip()}")

# 演示2：列出当前目录
print("\n  [演示2] 执行 dir/ls 命令")
if os.name == "nt":
    result = subprocess.run(["dir", "README.md"], capture_output=True, text=True, timeout=10, shell=True)
else:
    result = subprocess.run(["ls", "-la", "README.md"], capture_output=True, text=True, timeout=10)

if result.returncode == 0:
    for line in result.stdout.strip().split("\n")[:3]:
        print(f"    {line}")
else:
    print(f"    命令执行完成 (returncode={result.returncode})")

# 演示3：传递 JSON 数据
print("\n  [演示3] 通过 stdin/stdout 传递 JSON 数据")

# Python 脚本内容（模拟一个数据处理服务）
python_worker = '''
import sys
import json

# 从 stdin 读取输入
data = json.loads(sys.stdin.read())

# 处理数据
result = {
    "input_count": len(data["items"]),
    "total": sum(data["items"]),
    "average": sum(data["items"]) / len(data["items"]),
    "max": max(data["items"]),
    "min": min(data["items"]),
}

# 输出到 stdout
print(json.dumps(result, indent=2))
'''

# 写入临时文件并执行
import tempfile
with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(python_worker)
    temp_script = f.name

try:
    input_data = json.dumps({"items": [10, 20, 30, 40, 50]})
    result = subprocess.run(
        [sys.executable, temp_script],
        input=input_data,
        capture_output=True, text=True, timeout=10
    )
    if result.returncode == 0:
        output = json.loads(result.stdout)
        print(f"    输入: items = [10, 20, 30, 40, 50]")
        print(f"    输出: {json.dumps(output, indent=6)}")
    else:
        print(f"    执行失败: {result.stderr}")
finally:
    os.unlink(temp_script)


# =====================================================================
# 第三部分：策略2 —— gRPC 通信
# =====================================================================
print("\n\n" + "=" * 65)
print("  第三部分：策略2 —— gRPC / REST 通信")
print("=" * 65)

print("""
  gRPC 是跨语言通信的首选方案：

  1. 定义 .proto 文件（公共契约）
  2. C# 和 Python 各自生成客户端/服务端代码
  3. 通过 HTTP/2 双向流通信

  ┌─────────────────────────────────────────────────┐
  │                                                   │
  │  C# gRPC Server        Python gRPC Client        │
  │  ┌──────────────┐      ┌──────────────┐          │
  │  │ UserService  │<----->│ UserService  │          │
  │  │ (实现服务)    │ gRPC │ (调用服务)    │          │
  │  └──────────────┘      └──────────────┘          │
  │         │                      │                   │
  │         └────── .proto ────────┘                   │
  │              (共享契约)                             │
  └─────────────────────────────────────────────────┘
""")

# 展示 .proto 文件
print("--- .proto 文件示例（C# 和 Python 共享）---")
print("""
  // user_service.proto
  syntax = "proto3";

  package user;

  service UserService {
      rpc GetUser (GetUserRequest) returns (UserResponse);
      rpc ListUsers (ListUsersRequest) returns (ListUsersResponse);
      rpc CreateUser (CreateUserRequest) returns (UserResponse);
  }

  message GetUserRequest {
      int32 user_id = 1;
  }

  message UserResponse {
      int32 id = 1;
      string name = 2;
      int32 age = 3;
      string email = 4;
  }

  message ListUsersRequest {
      int32 page = 1;
      int32 page_size = 2;
  }

  message ListUsersResponse {
      repeated UserResponse users = 1;
      int32 total = 2;
  }

  message CreateUserRequest {
      string name = 1;
      int32 age = 2;
      string email = 3;
  }
""")

# 模拟 gRPC 通信
print("--- 模拟 gRPC 通信演示 ---\n")

# 模拟 protobuf 序列化/反序列化
@dataclass
class GRPCUser:
    id: int = 0
    name: str = ""
    age: int = 0
    email: str = ""

    def SerializeToString(self) -> bytes:
        """模拟 Protobuf 序列化"""
        return json.dumps(asdict(self)).encode()

    @classmethod
    def FromString(cls, data: bytes) -> 'GRPCUser':
        """模拟 Protobuf 反序列化"""
        d = json.loads(data)
        return cls(**d)


# 模拟 gRPC 服务端（Python 侧）
class UserServiceServicer:
    """Python gRPC 服务实现"""

    def __init__(self):
        self.users = [
            GRPCUser(id=1, name="Alice", age=30, email="alice@example.com"),
            GRPCUser(id=2, name="Bob", age=25, email="bob@example.com"),
        ]

    def GetUser(self, request_data: dict) -> GRPCUser:
        user_id = request_data["user_id"]
        for u in self.users:
            if u.id == user_id:
                return u
        raise ValueError(f"User {user_id} not found")

    def ListUsers(self, request_data: dict) -> list:
        page = request_data.get("page", 1)
        page_size = request_data.get("page_size", 10)
        start = (page - 1) * page_size
        return self.users[start:start + page_size]


# 模拟 gRPC 客户端（C# 侧调用）
service = UserServiceServicer()

# GetUser 调用
print("  [gRPC 调用] GetUser(user_id=1)")
request = {"user_id": 1}
user = service.GetUser(request)
print(f"    请求: GetUserRequest {{ user_id: 1 }}")
print(f"    响应: UserResponse {{ id={user.id}, name=\"{user.name}\", age={user.age} }}")

# ListUsers 调用
print("\n  [gRPC 调用] ListUsers(page=1, page_size=10)")
users = service.ListUsers({"page": 1, "page_size": 10})
print(f"    请求: ListUsersRequest {{ page: 1, page_size: 10 }}")
print(f"    响应: {len(users)} 个用户")
for u in users:
    print(f"      UserResponse {{ id={u.id}, name=\"{u.name}\", age={u.age} }}")

# 序列化演示
print("\n  [Protobuf 序列化演示]")
serialized = user.SerializeToString()
print(f"    序列化大小: {len(serialized)} bytes")
print(f"    原始数据:   {serialized.decode()[:80]}...")
deserialized = GRPCUser.FromString(serialized)
print(f"    反序列化:   {deserialized}")


# =====================================================================
# 第四部分：代码模式对照 —— Repository / Service / DI
# =====================================================================
print("\n\n" + "=" * 65)
print("  第四部分：代码模式对照（Python vs C#）")
print("=" * 65)


# --- Repository 模式 ---
print("\n--- Repository 模式 ---\n")

# Python 版（鸭子类型，无需接口定义）
class UserRepository:
    """Python 版 UserRepository

    对比 C#：
      public interface IUserRepository
      {
          User? GetUser(int userId);
          bool SaveUser(User user);
      }

    Python 不需要显式定义接口，"如果它走路像鸭子..."
    """

    def __init__(self):
        self._users = {
            1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
            2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
        }
        self._next_id = 3

    def get_user(self, user_id: int) -> Optional[dict]:
        """查询用户"""
        return self._users.get(user_id)

    def list_users(self) -> list[dict]:
        """获取所有用户"""
        return list(self._users.values())

    def save_user(self, user: dict) -> dict:
        """保存用户"""
        if "id" not in user or user["id"] is None:
            user["id"] = self._next_id
            self._next_id += 1
        self._users[user["id"]] = user
        return user

    def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False


# --- Service 模式 ---
print("--- Service 层 ---\n")

class UserService:
    """Python 版 UserService

    对比 C#：
      public class UserService
      {
          private readonly IUserRepository _repo;
          public UserService(IUserRepository repo) => _repo = repo;
      }

    Python 通过构造函数注入（和 C# 一样），但没有接口约束。
    """

    def __init__(self, repo: UserRepository):
        self._repo = repo

    def get_user(self, user_id: int) -> Optional[dict]:
        user = self._repo.get_user(user_id)
        if not user:
            return None
        # 业务逻辑：脱敏
        return {
            **user,
            "email": user["email"].split("@")[0] + "***",
        }

    def create_user(self, name: str, email: str) -> dict:
        """创建用户（含业务验证）"""
        # 验证
        if not name or len(name.strip()) == 0:
            raise ValueError("用户名不能为空")
        if "@" not in email:
            raise ValueError("邮箱格式无效")

        # 检查重复
        existing = [u for u in self._repo.list_users() if u["email"] == email]
        if existing:
            raise ValueError(f"邮箱已被注册: {email}")

        return self._repo.save_user({"name": name, "email": email})

    def get_user_stats(self) -> dict:
        """用户统计"""
        users = self._repo.list_users()
        return {
            "total_users": len(users),
            "user_names": [u["name"] for u in users],
        }


# --- 依赖注入容器 ---
print("--- 简单 DI 容器 ---\n")

class Container:
    """简单的依赖注入容器

    对比 C#：
      services.AddScoped<IUserRepository, UserRepository>();
      services.AddScoped<IUserService, UserService>();

    Python 的 dependency-injector 库提供了更完整的 DI 实现。
    """

    def __init__(self):
        self._singletons = {}
        self._factories = {}

    def register_singleton(self, interface, implementation):
        """注册单例（每次 Resolve 返回同一实例）"""
        self._singletons[interface] = implementation

    def register_factory(self, interface, factory_func):
        """注册工厂（每次 Resolve 调用工厂创建新实例）"""
        self._factories[interface] = factory_func

    def resolve(self, interface):
        """解析依赖"""
        if interface in self._factories:
            return self._factories[interface]()
        if interface in self._singletons:
            return self._singletons[interface]
        raise KeyError(f"未注册的服务: {interface}")


# 演示完整的 DI + Repository + Service 流程
print("--- 完整流程演示 ---\n")

# 注册依赖
container = Container()
container.register_singleton(UserRepository, UserRepository())
container.register_factory(UserService, lambda: UserService(container.resolve(UserRepository)))

# 解析服务
user_service = container.resolve(UserService)

# 创建用户
print("  [创建用户]")
try:
    new_user = user_service.create_user("Charlie", "charlie@example.com")
    print(f"    创建成功: {new_user}")
except ValueError as e:
    print(f"    创建失败: {e}")

# 获取用户（脱敏）
print("\n  [获取用户（含脱敏）]")
user = user_service.get_user(1)
print(f"    Alice 的脱敏信息: {user}")

# 统计
print("\n  [用户统计]")
stats = user_service.get_user_stats()
print(f"    {stats}")


# =====================================================================
# 第五部分：策略3 —— 共享数据层
# =====================================================================
print("\n\n" + "=" * 65)
print("  第五部分：策略3 —— 共享数据层")
print("=" * 65)

print("""
  C# 和 Python 通过共享数据库通信：

  ┌──────────┐     ┌──────────┐     ┌──────────┐
  │  C# API  │────>| Database |<----| Python   │
  │ (写入)    │     │(PostgreSQL│     │ (分析)   │
  └──────────┘     │  MySQL)  │     └──────────┘
                   └──────────┘

  数据格式对照：
  ┌──────────────────────────────────────────────────────┐
  │ 方式              C#                   Python         │
  ├──────────────────────────────────────────────────────┤
  │ JSON 序列化       System.Text.Json     json 模块      │
  │ Protobuf          Google.Protobuf      protobuf       │
  │ CSV               CsvHelper            csv 模块       │
  │ Parquet           Parquet.NET          pyarrow        │
  │ 数据库            EF Core / Dapper     SQLAlchemy     │
  └──────────────────────────────────────────────────────┘
""")

# 演示 JSON 序列化兼容性
print("--- JSON 数据交换演示 ---\n")

# C# 风格的 JSON（驼峰命名）
csharp_json = '{"userId": 1, "userName": "Alice", "createdAt": "2024-01-15T10:30:00"}'
data = json.loads(csharp_json)
print(f"  C# 生成的 JSON: {csharp_json}")
print(f"  Python 解析:    {data}")

# Python 风格的 JSON（蛇形命名）
python_data = {"user_id": 1, "user_name": "Alice", "created_at": "2024-01-15T10:30:00"}
csharp_format = json.dumps(python_data, ensure_ascii=False)
print(f"\n  Python 生成: {csharp_format}")

print("""
  [WARN] 命名风格注意：
  C# 使用 camelCase:   userId, userName, createdAt
  Python 使用 snake_case: user_id, user_name, created_at

  解决方案：
  1. API 层统一用 camelCase（FastAPI 的 alias 参数）
  2. 数据库层用 snake_case
  3. 中间层做转换
""")


# =====================================================================
# 第六部分：策略4 —— 原生互操作
# =====================================================================
print("\n" + "=" * 65)
print("  第六部分：策略4 —— 原生互操作（高性能）")
print("=" * 65)

print("""
  当性能要求极高时，可以使用原生互操作：

  ┌─────────────────────────────────────────────────────────────┐
  │  方式                  Python 侧         C# 侧              │
  ├─────────────────────────────────────────────────────────────┤
  │  pythonnet             import clr         Python.Runtime     │
  │  ctypes                ctypes.CDLL        P/Invoke           │
  │  pybind11              C++ 扩展           无直接对应          │
  │  C++/CLI               C++ 桥接           C++/CLI 桥接       │
  │  COM 互操作            comtypes           System.Runtime     │
  │                       comtypes            .InteropServices   │
  └─────────────────────────────────────────────────────────────┘
""")

# Python 调用 C 库的示例（通过 ctypes）
print("--- ctypes 调用 C 标准库演示 ---\n")

try:
    import ctypes

    # Windows 上的 msvcrt
    if os.name == "nt":
        libc = ctypes.CDLL("msvcrt")
        result = libc.printf(b"  [C printf] Hello from C library! (ctypes)\n")
    else:
        libc = ctypes.CDLL("libc.so.6")
        result = libc.printf(b"  [C printf] Hello from C library! (ctypes)\n")

    print(f"  ctypes 调用成功，返回值: {result}")

except Exception as e:
    print(f"  ctypes 调用示例（跳过）: {e}")

print("""
  对比 C# 的 P/Invoke：

  // C# 调用 C 库
  [DllImport("msvcrt")]
  static extern int printf(string format);

  Python ctypes 调用：
  import ctypes
  libc = ctypes.CDLL("msvcrt")
  libc.printf(b"Hello from C!")

  性能考虑：
  ├── ctypes:        每次调用有 marshalling 开销
  ├── pybind11:      C++ 直接调用，开销最小
  ├── pythonnet:     .NET CLR 内嵌，有 GC 压力
  └── gRPC:          网络开销，但跨语言最灵活
""")


# =====================================================================
# 第七部分：渐进式迁移实战 —— 完整检查清单
# =====================================================================
print("\n" + "=" * 65)
print("  第七部分：渐进式迁移检查清单")
print("=" * 65)

checklist = {
    "1. 评估阶段": [
        "识别需要迁移的模块（优先 Python 优势领域：AI/ML、数据处理）",
        "评估模块间耦合度",
        "确定通信方式（gRPC / REST / 共享数据库）",
        "制定迁移路线图（先易后难）",
    ],
    "2. 基础设施": [
        "设置 Python 虚拟环境管理（Poetry / uv）",
        "配置 CI/CD（Python 测试 + C# 测试）",
        "设置代码质量工具（ruff + Roslyn analyzers）",
        "配置 Docker 多语言构建",
    ],
    "3. 接口层": [
        "定义共享的 API 契约（OpenAPI / .proto）",
        "实现服务发现机制",
        "配置认证/授权（JWT 共享）",
        "设置日志聚合（统一日志格式）",
    ],
    "4. 数据层": [
        "统一数据模型（命名风格：snake_case vs camelCase）",
        "配置数据库连接（连接池共享）",
        "设置数据迁移工具（Alembic / EF Core Migrations）",
        "实现数据验证（Pydantic / FluentValidation）",
    ],
    "5. 测试策略": [
        "编写集成测试（跨语言调用）",
        "性能基准测试",
        "回归测试套件",
        "端到端测试",
    ],
    "6. 监控运维": [
        "分布式追踪（Jaeger / Zipkin）",
        "健康检查（C# 和 Python 服务）",
        "告警规则",
        "部署脚本",
    ],
}

for phase, items in checklist.items():
    print(f"\n  {phase}")
    for i, item in enumerate(items, 1):
        print(f"    [{i}] {item}")


# =====================================================================
# 第八部分：混合使用最佳实践
# =====================================================================
print("\n\n" + "=" * 65)
print("  第八部分：混合使用最佳实践")
print("=" * 65)

best_practices = {
    "AI/ML 集成": {
        "模式": "Python 训练 → ONNX → C# 推理",
        "工具": "ONNX Runtime (C# 和 Python 通用)",
        "场景": "推荐系统、NLP、计算机视觉",
        "C# 代码": "using Microsoft.ML.OnnxRuntime;",
        "Python 代码": "import onnxruntime as ort;",
    },
    "数据管道": {
        "模式": "Python ETL → 共享数据库 → C# API",
        "工具": "Pandas/Polars + SQLAlchemy",
        "场景": "数据分析、报表生成",
        "C# 代码": "EF Core 读取处理后的数据",
        "Python 代码": "df.to_sql('results', engine)",
    },
    "微服务架构": {
        "模式": "gRPC 服务间通信",
        "工具": "Grpc.Net (C#) + grpcio (Python)",
        "场景": "新服务用 Python，旧服务保留 C#",
        "C# 代码": "app.MapGrpcService<UserService>();",
        "Python 代码": "class UserService(user_pb2_grpc.UserServiceServicer):",
    },
    "脚本自动化": {
        "模式": "C# 主程序调用 Python 脚本",
        "工具": "Process.Start (C#) / subprocess (Python)",
        "场景": "数据迁移、批量处理、报表生成",
        "C# 代码": "Process.Start(\"python\", \"script.py\");",
        "Python 代码": "# 脚本独立运行",
    },
}

for pattern_name, info in best_practices.items():
    print(f"\n  [{pattern_name}]")
    for key, value in info.items():
        print(f"    {key:12s}: {value}")


# =====================================================================
# 总结
# =====================================================================
print("\n\n" + "=" * 65)
print("  总结：迁移策略选择指南")
print("=" * 65)

summary = """
  ┌────────────────────────────────────────────────────────────┐
  │ 场景                        │ 推荐策略                     │
  ├─────────────────────────────┼──────────────────────────────┤
  │ 快速原型，验证 Python 可行性 │ 子进程调用                   │
  │ 微服务，逐步迁移            │ gRPC / REST                  │
  │ 数据密集型，共享状态         │ 共享数据库                   │
  │ 高性能计算，毫秒级响应       │ pybind11 / pythonnet         │
  │ AI/ML 集成                  │ ONNX（Python 训练 → C# 推理）│
  └─────────────────────────────┴──────────────────────────────┘

  [TARGET] 核心原则：
  ├── 1. 不要重写能工作的代码
  ├── 2. 用 Python 做它擅长的（AI/数据/脚本）
  ├── 3. 用 C# 做它擅长的（性能/类型安全/企业级）
  ├── 4. 通过清晰的接口层（gRPC/REST）连接两者
  └── 5. 渐进式迁移，不要大爆炸式重写
"""
print(summary)
