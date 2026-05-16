"""
=================================================================
6.4 Web 开发 —— Flask vs FastAPI vs Django 全面对比
对应文章：6.4 Web开发
=================================================================

C# 开发者最熟悉的 Web 框架是 ASP.NET Core。
本文件展示 Python Web 框架的核心概念，
并提供可直接运行的代码示例（无需启动服务器）。

对比 C# ASP.NET Core：
  - FastAPI ≈ ASP.NET Core Minimal APIs（最接近）
  - Flask   ≈ ASP.NET Core（更轻量）
  - Django  ≈ ASP.NET MVC + EF Core + Admin（全功能）
"""

import json
import time
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime
from enum import Enum

# 注意：FastAPI 和 Pydantic 是可选依赖
# 本文件使用标准库模拟核心概念，确保无需安装即可运行
# 如果安装了 FastAPI，文末会展示真实的 FastAPI 代码

print("=" * 65)
print("  Python Web 开发全览 —— 从 ASP.NET Core 到 Flask/FastAPI/Django")
print("=" * 65)


# =====================================================================
# 第一部分：请求/响应模型（Pydantic vs C# Models）
# =====================================================================
print("\n" + "=" * 65)
print("  第一部分：请求/响应模型（Pydantic vs C# Models）")
print("=" * 65)

print("""
┌─────────────────────────────────────────────────────────────────┐
│  概念对照                                                        │
│                                                                  │
│  C# ASP.NET Core          Python FastAPI                        │
│  ───────────────          ───────────────                        │
│  record User(             class User(BaseModel):                 │
│    int Id,                  name: str                            │
│    string Name,             age: int                             │
│    int Age                  email: str | None = None             │
│  )                       # Pydantic 自动验证 + 序列化             │
│                                                                  │
│  [Required]               Field(..., min_length=1)              │
│  [Range(0, 150)]          Field(ge=0, le=150)                   │
│  [StringLength(100)]      Field(max_length=100)                  │
│  [EmailAddress]           EmailStr（需 email-validator）         │
└─────────────────────────────────────────────────────────────────┘
""")

# 使用 dataclass 模拟 Pydantic 的数据验证
# （实际 FastAPI 项目中应使用 pydantic.BaseModel）

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

@dataclass
class UserCreate:
    """创建用户的请求模型（类似 C# 的 DTO）"""
    name: str
    age: int
    email: Optional[str] = None
    gender: Optional[str] = None

    def __post_init__(self):
        """数据验证（Pydantic 的 __init__ 自动做这些）"""
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("name 不能为空")
        if len(self.name) > 100:
            raise ValueError("name 不能超过 100 个字符")
        if self.age < 0 or self.age > 150:
            raise ValueError(f"age 必须在 0-150 之间，当前值: {self.age}")
        if self.email and "@" not in self.email:
            raise ValueError(f"email 格式无效: {self.email}")

    def model_dump(self) -> dict:
        """类似 Pydantic 的 model_dump()，C# 用 JsonSerializer.Serialize()"""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class UserResponse:
    """响应模型"""
    id: int
    name: str
    age: int
    email: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def model_dump(self) -> dict:
        return asdict(self)


@dataclass
class PaginatedResponse:
    """分页响应（类似 C# 的 PagedResult<T>）"""
    items: list
    total: int
    page: int
    page_size: int

    @property
    def total_pages(self) -> int:
        return (self.total + self.page_size - 1) // self.page_size

    def model_dump(self) -> dict:
        return {
            "items": self.items,
            "total": self.total,
            "page": self.page,
            "page_size": self.page_size,
            "total_pages": self.total_pages,
        }


# 演示模型创建和验证
print("--- 演示：Pydantic 风格的数据验证 ---\n")

# 创建用户（验证通过）
user1 = UserCreate(name="Alice", age=30, email="alice@example.com")
print(f"  创建成功: {user1.model_dump()}")

# 创建用户（无 email，可选字段）
user2 = UserCreate(name="Bob", age=25)
print(f"  创建成功（无 email）: {user2.model_dump()}")

# 验证失败示例
print("\n--- 数据验证失败演示 ---")
validation_tests = [
    {"name": "", "age": 30},
    {"name": "X" * 101, "age": 30},
    {"name": "Charlie", "age": -1},
    {"name": "Diana", "age": 200},
    {"name": "Eve", "age": 25, "email": "invalid-email"},
]

for test_data in validation_tests:
    try:
        user = UserCreate(**test_data)
        print(f"  [OK] 创建成功: {user.model_dump()}")
    except (ValueError, TypeError) as e:
        print(f"  [X] 验证失败: {test_data} -> {e}")

print("""
对比 C# 的模型验证：
  // C# ASP.NET Core
  public class UserCreateDto
  {
      [Required]
      [StringLength(100)]
      public string Name { get; set; }

      [Range(0, 150)]
      public int Age { get; set; }

      [EmailAddress]
      public string? Email { get; set; }
  }

  Python FastAPI（使用 Pydantic）：
  class UserCreate(BaseModel):
      name: str = Field(..., min_length=1, max_length=100)
      age: int = Field(..., ge=0, le=150)
      email: EmailStr | None = None
""")


# =====================================================================
# 第二部分：路由定义（路由 vs 控制器）
# =====================================================================
print("\n" + "=" * 65)
print("  第二部分：路由定义")
print("=" * 65)

# 模拟路由表
routes = []

def route(method: str, path: str):
    """装饰器，模拟 FastAPI/Flask 的路由注册"""
    def decorator(func):
        routes.append({
            "method": method,
            "path": path,
            "handler": func.__name__,
            "doc": func.__doc__ or "",
        })
        return func
    return decorator

# --- Flask 风格 ---
print("\n--- Flask 风格路由 ---")
print("""
  # Flask: 装饰器 + 函数
  @app.route('/users', methods=['GET'])
  def get_users():
      return jsonify(users)

  @app.route('/users/<int:user_id>', methods=['GET'])
  def get_user(user_id: int):
      return jsonify(find_user(user_id))

  @app.route('/users', methods=['POST'])
  def create_user():
      data = request.get_json()
      return jsonify(data), 201
""")

# --- FastAPI 风格 ---
print("--- FastAPI 风格路由（最接近 ASP.NET Core）---")
print("""
  # FastAPI: 类型安全 + 自动文档
  @app.get("/users")
  async def get_users() -> list[UserResponse]:
      return users

  @app.get("/users/{user_id}")
  async def get_user(user_id: int) -> UserResponse:
      return find_user(user_id)

  @app.post("/users", status_code=201)
  async def create_user(user: UserCreate) -> UserResponse:
      return save_user(user)

  @app.put("/users/{user_id}")
  async def update_user(user_id: int, user: UserCreate) -> UserResponse:
      return update(user_id, user)

  @app.delete("/users/{user_id}", status_code=204)
  async def delete_user(user_id: int):
      delete_user(user_id)
""")

# --- Django 风格 ---
print("--- Django 风格路由（类似 ASP.NET MVC）---")
print("""
  # Django urls.py
  urlpatterns = [
      path('users/', views.user_list),
      path('users/<int:pk>/', views.user_detail),
  ]

  # Django views.py（类视图）
  class UserListView(View):
      def get(self, request):
          return JsonResponse({'users': list(User.objects.values())})

      def post(self, request):
          data = json.loads(request.body)
          user = User.objects.create(**data)
          return JsonResponse({'id': user.id}, status=201)
""")

# 路由对照表
print("\n--- 路由语法对照 ---")
route_comparison = [
    ("GET /users",           "app.get(\"/users\")",              "@app.route('/users')",          "GET"),
    ("GET /users/{id}",      "app.get(\"/users/{id}\")",         "@app.route('/users/<int:id>')",  "GET"),
    ("POST /users",          "app.post(\"/users\")",             "@app.route('/users', POST)",     "POST"),
    ("PUT /users/{id}",      "app.put(\"/users/{id}\")",         "— (需 flask-restful)",           "PUT"),
    ("DELETE /users/{id}",   "app.delete(\"/users/{id}\")",      "— (需 flask-restful)",           "DELETE"),
]

print("  {:25s} {:30s} {:30s}".format("HTTP", "FastAPI", "Flask"))
print("  " + "-" * 85)
for http, fastapi, flask, _ in route_comparison:
    print(f"  {http:25s} {fastapi:30s} {flask:30s}")


# =====================================================================
# 第三部分：中间件（Middleware）
# =====================================================================
print("\n\n" + "=" * 65)
print("  第三部分：中间件")
print("=" * 65)

print("""
┌─────────────────────────────────────────────────────────────────┐
│  中间件概念完全一致：在请求/响应管道中插入处理逻辑               │
│                                                                  │
│  C#                          Python                              │
│  ────                        ──────                              │
│  app.UseMiddleware<T>()      @app.middleware("http")             │
│  app.UseAuthentication()     — (用 Depends 实现)                │
│  app.UseCors()               CORSMiddleware                      │
│  app.UseRateLimiting()       slowapi / fastapi-limiter           │
│  app.UseSwagger()            FastAPI 内置 /doc                   │
└─────────────────────────────────────────────────────────────────┘
""")

# 模拟中间件执行
class MiddlewareSimulator:
    """模拟 ASP.NET Core 和 FastAPI 的中间件管道"""

    def __init__(self):
        self.middlewares = []
        self.request_count = 0

    def use(self, name: str, func):
        """注册中间件"""
        self.middlewares.append((name, func))

    def process(self, request: dict) -> dict:
        """处理请求（模拟中间件管道）"""
        response = {"status": 200, "body": "OK", "headers": {}}

        # 按注册顺序执行中间件
        for name, middleware_func in self.middlewares:
            result = middleware_func(request, response)
            if result is not None:
                request, response = result

        return response


# 定义中间件
def logging_middleware(request: dict, response: dict):
    """日志中间件（类比 Serilog RequestLoggingMiddleware）"""
    print(f"    [日志] {request['method']} {request['path']}")
    return request, response


def timing_middleware(request: dict, response: dict):
    """计时中间件（类比 ASP.NET Core 的 UseHttpMetrics）"""
    request["_start_time"] = time.time()
    return request, response


def auth_middleware(request: dict, response: dict):
    """认证中间件（类比 ASP.NET Core 的 UseAuthentication）"""
    token = request.get("headers", {}).get("Authorization", "")
    if token.startswith("Bearer "):
        request["user"] = {"id": 1, "name": "authenticated_user"}
    else:
        response["status"] = 401
        response["body"] = "Unauthorized"
    return request, response


# 演示中间件执行
print("--- 中间件执行演示 ---\n")

app = MiddlewareSimulator()
app.use("Logging", logging_middleware)
app.use("Timing", timing_middleware)
app.use("Auth", auth_middleware)

# 请求 1：带认证
print("  请求 1: GET /api/users （带 Bearer Token）")
request1 = {"method": "GET", "path": "/api/users", "headers": {"Authorization": "Bearer abc123"}}
response1 = app.process(request1)
print(f"    响应: status={response1['status']}, body={response1['body']}\n")

# 请求 2：无认证
print("  请求 2: GET /api/users （无 Token）")
request2 = {"method": "GET", "path": "/api/users", "headers": {}}
response2 = app.process(request2)
print(f"    响应: status={response2['status']}, body={response2['body']}\n")

# 请求 3：POST
print("  请求 3: POST /api/users （带 Bearer Token）")
request3 = {"method": "POST", "path": "/api/users", "headers": {"Authorization": "Bearer abc123"}}
response3 = app.process(request3)
print(f"    响应: status={response3['status']}, body={response3['body']}")

print("""
对比 C# 中间件：
  // C# ASP.NET Core
  app.UseMiddleware<LoggingMiddleware>();
  app.UseMiddleware<TimingMiddleware>();
  app.UseAuthentication();
  app.UseAuthorization();

  # Python FastAPI
  app.add_middleware(LoggingMiddleware)
  app.add_middleware(TimingMiddleware)
  # 认证通过 Depends 注入实现
""")


# =====================================================================
# 第四部分：ORM（SQLAlchemy vs EF Core）
# =====================================================================
print("\n\n" + "=" * 65)
print("  第四部分：ORM —— SQLAlchemy vs EF Core")
print("=" * 65)

# 使用 dataclass 模拟 ORM 模型
@dataclass
class Article:
    """模拟 SQLAlchemy 模型"""
    id: int = 0
    title: str = ""
    content: str = ""
    author_id: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    tags: list = field(default_factory=list)

    def __str__(self):
        return f"Article(id={self.id}, title='{self.title}')"


# 模拟数据库
fake_db = {
    "articles": [
        Article(id=1, title="Python 入门", content="Python 是一门...", author_id=1, tags=["python", "入门"]),
        Article(id=2, title="FastAPI 教程", content="FastAPI 是...", author_id=1, tags=["fastapi", "web"]),
        Article(id=3, title="C# 对比", content="从 C# 到 Python...", author_id=2, tags=["csharp", "对比"]),
    ]
}

print("""
--- SQLAlchemy vs EF Core 代码对照 ---

C# EF Core:
  // 定义模型
  public class Article
  {
      public int Id { get; set; }
      public string Title { get; set; }
      public string Content { get; set; }
      public int AuthorId { get; set; }
      public DateTime CreatedAt { get; set; }
  }

  // 查询
  var articles = await context.Articles
      .Where(a => a.CreatedAt > DateTime.Now.AddDays(-7))
      .OrderByDescending(a => a.CreatedAt)
      .ToListAsync();

Python SQLAlchemy:
  # 定义模型
  class Article(Base):
      __tablename__ = 'articles'
      id = Column(Integer, primary_key=True)
      title = Column(String(200))
      content = Column(Text)
      author_id = Column(Integer, ForeignKey('users.id'))
      created_at = Column(DateTime, default=datetime.utcnow)

  # 查询
  articles = session.query(Article)
      .filter(Article.created_at > datetime.now() - timedelta(days=7))
      .order_by(Article.created_at.desc())
      .all()
""")

# 模拟 ORM 查询
print("--- 模拟 ORM 查询演示 ---\n")

articles = fake_db["articles"]

# 基础查询
print("  所有文章:")
for a in articles:
    print(f"    {a}")

# 过滤（模拟 WHERE）
print("\n  过滤: author_id == 1")
filtered = [a for a in articles if a.author_id == 1]
for a in filtered:
    print(f"    {a}")

# 排序（模拟 ORDER BY）
print("\n  排序: 按 id 降序")
sorted_articles = sorted(articles, key=lambda a: a.id, reverse=True)
for a in sorted_articles:
    print(f"    {a}")

# 标签过滤
print("\n  标签过滤: 含 'python' 标签")
tagged = [a for a in articles if "python" in a.tags]
for a in tagged:
    print(f"    {a}")

# 聚合
print(f"\n  聚合: 总文章数 = {len(articles)}")
author_counts = {}
for a in articles:
    author_counts[a.author_id] = author_counts.get(a.author_id, 0) + 1
print(f"  每个作者的文章数: {author_counts}")


# =====================================================================
# 第五部分：依赖注入（Depends vs ASP.NET Core DI）
# =====================================================================
print("\n\n" + "=" * 65)
print("  第五部分：依赖注入")
print("=" * 65)

print("""
┌─────────────────────────────────────────────────────────────────┐
│  FastAPI 的 Depends 是最接近 ASP.NET Core DI 的机制             │
│                                                                  │
│  C#                          Python (FastAPI)                    │
│  ────                        ─────────────────                   │
│  services.AddScoped<T>()    (自动创建，请求级作用域)             │
│  services.AddSingleton<T>() 全局变量/单例                        │
│  services.AddTransient<T>() Depends (每次请求新建)              │
│  [Inject] 属性             Depends(func) 参数注入                │
│  IConfiguration             Settings(BaseModel)                  │
│  ILogger<T>                 logging.getLogger(__name__)          │
└─────────────────────────────────────────────────────────────────┘
""")

# 模拟 FastAPI Depends 机制
class FakeDB:
    """模拟数据库连接"""
    def query(self, table: str):
        return fake_db.get(table, [])

    def close(self):
        pass

def get_db():
    """FastAPI 依赖注入示例（请求级数据库连接）"""
    db = FakeDB()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: dict):
    """FastAPI 认证依赖示例"""
    token = request.get("headers", {}).get("Authorization", "")
    if not token.startswith("Bearer "):
        raise ValueError("未认证")
    return {"id": 1, "name": "current_user"}

# 模拟路由处理函数
def list_articles(db: FakeDB, user: dict) -> list:
    """使用依赖注入的路由处理函数"""
    articles = db.query("articles")
    return [{"id": a.id, "title": a.title} for a in articles]

# 演示依赖注入
print("--- 依赖注入演示 ---\n")

db = FakeDB()
user = {"id": 1, "name": "current_user"}
result = list_articles(db, user)
print(f"  获取到 {len(result)} 篇文章:")
for item in result:
    print(f"    {item}")

print("""
FastAPI Depends 用法：

  # 定义依赖
  def get_db():
      db = SessionLocal()
      try:
          yield db
      finally:
          db.close()

  def get_current_user(token: str = Header(...)):
      return verify_token(token)

  # 路由中使用
  @app.get("/users")
  def list_users(
      db: Session = Depends(get_db),          # 数据库连接
      user: User = Depends(get_current_user)  # 当前用户
  ):
      return db.query(User).all()

  # 类比 C#:
  // [ApiController]
  // [Route("api/[controller]")]
  // public class UsersController : ControllerBase
  // {
  //     private readonly AppDbContext _db;
  //     private readonly IUserService _userService;
  //
  //     public UsersController(AppDbContext db, IUserService userService)
  //     {
  //         _db = db;
  //         _userService = userService;
  //     }
  // }
""")


# =====================================================================
# 第六部分：Flask vs FastAPI vs Django 完整对比
# =====================================================================
print("\n" + "=" * 65)
print("  第六部分：三大框架完整对比")
print("=" * 65)

features = [
    ("性能",            "中等",         "高（async）",     "中等"),
    ("学习曲线",        "低",           "低",              "高"),
    ("自动 API 文档",   "需 flask-apispec","内置 /docs",  "需 DRF"),
    ("异步支持",        "有限",         "原生 async",      "3.1+"),
    ("ORM",             "无",           "无（可选）",      "内置 Django ORM"),
    ("Admin 后台",      "需 Flask-Admin","无",             "内置 Admin"),
    ("认证系统",        "需 Flask-Login","需实现",          "内置 Auth"),
    ("表单验证",        "需 WTForms",   "Pydantic 自动",   "内置 Forms"),
    ("模板引擎",        "Jinja2",       "无（专注 API）",   "DTL/Jinja2"),
    ("WebSocket",       "需扩展",       "原生支持",         "Channels"),
    ("适用场景",        "微服务/原型",  "API/微服务",       "全功能 Web 应用"),
    ("C# 类比",         "Minimal APIs", "ASP.NET Core",    "ASP.NET MVC"),
]

print("\n  {:14s} {:16s} {:16s} {:16s}".format("特性", "Flask", "FastAPI", "Django"))
print("  " + "-" * 65)
for feature, flask, fastapi, django in features:
    print(f"  {feature:14s} {flask:16s} {fastapi:16s} {django:16s}")


# =====================================================================
# 第七部分：完整的 FastAPI 应用示例（代码展示）
# =====================================================================
print("\n\n" + "=" * 65)
print("  第七部分：完整 FastAPI 应用示例")
print("=" * 65)

fastapi_full_app = '''
"""
完整 FastAPI 应用示例（等价于 ASP.NET Core Web API）

安装: pip install fastapi uvicorn
运行: uvicorn app:app --reload
文档: http://localhost:8000/docs
"""

from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Optional

# --- 数据模型（类似 C# DTO + FluentValidation）---

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)
    email: Optional[str] = Field(None)

class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    email: Optional[str] = None

class PaginatedResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    page_size: int

# --- 依赖注入（类似 C# 的 DI + 中间件）---

async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未认证")
    return {"id": 1, "name": "current_user"}

# --- 应用实例 ---

app = FastAPI(title="用户管理 API", version="1.0.0")

# 模拟数据库
users_db: list[dict] = []
next_id = 1

# --- 路由（类似 C# Controller）---

@app.get("/users", response_model=PaginatedResponse)
async def list_users(
    page: int = 1,
    page_size: int = 10,
    user: dict = Depends(get_current_user),  # 认证依赖
):
    """获取用户列表（类似 C# [HttpGet]）"""
    return PaginatedResponse(
        items=users_db[(page-1)*page_size : page*page_size],
        total=len(users_db),
        page=page,
        page_size=page_size,
    )

@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    user: dict = Depends(get_current_user),
):
    """创建用户（类似 C# [HttpPost]）"""
    global next_id
    new_user = {"id": next_id, **user_data.model_dump()}
    users_db.append(new_user)
    next_id += 1
    return new_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """获取单个用户（类似 C# [HttpGet("{id}")]）"""
    for u in users_db:
        if u["id"] == user_id:
            return u
    raise HTTPException(status_code=404, detail="用户不存在")

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserCreate,
    user: dict = Depends(get_current_user),
):
    """更新用户（类似 C# [HttpPut]）"""
    for i, u in enumerate(users_db):
        if u["id"] == user_id:
            users_db[i] = {"id": user_id, **user_data.model_dump()}
            return users_db[i]
    raise HTTPException(status_code=404, detail="用户不存在")

@app.delete("/users/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    user: dict = Depends(get_current_user),
):
    """删除用户（类似 C# [HttpDelete]）"""
    global users_db
    users_db = [u for u in users_db if u["id"] != user_id]

# --- 启动命令 ---
# uvicorn app:app --reload --host 0.0.0.0 --port 8000
'''
print(fastapi_full_app)


# =====================================================================
# 第八部分：项目结构对比
# =====================================================================
print("=" * 65)
print("  第八部分：项目结构对比")
print("=" * 65)

print("""
=== C# ASP.NET Core 项目结构 ===

  MyApi/
  ├── MyApi.csproj
  ├── Program.cs                    # 入口 + 配置
  ├── appsettings.json              # 配置文件
  ├── Controllers/                  # 控制器
  │   └── UsersController.cs
  ├── Models/                       # 数据模型
  │   ├── User.cs
  │   └── UserCreateDto.cs
  ├── Services/                     # 业务逻辑层
  │   └── UserService.cs
  ├── Data/                         # 数据访问层
  │   └── AppDbContext.cs
  ├── Middleware/                   # 自定义中间件
  │   └── RequestTimingMiddleware.cs
  └── Tests/
      └── UsersControllerTests.cs

=== Python FastAPI 项目结构 ===

  my_api/
  ├── pyproject.toml                # 项目配置 + 依赖
  ├── main.py                       # 入口（创建 app）
  ├── app/
  │   ├── __init__.py
  │   ├── core/                     # 核心配置
  │   │   ├── config.py             # Settings (pydantic-settings)
  │   │   ├── security.py           # 认证逻辑
  │   │   └── dependencies.py       # 公共依赖
  │   ├── models/                   # 数据模型（Pydantic）
  │   │   └── user.py
  │   ├── routers/                  # 路由（类似 Controllers）
  │   │   └── users.py
  │   ├── services/                 # 业务逻辑
  │   │   └── user_service.py
  │   └── db/                       # 数据库
  │       └── database.py           # SQLAlchemy 连接
  ├── tests/
  │   └── test_users.py
  └── Dockerfile

=== Python Flask 项目结构 ===

  my_flask_app/
  ├── requirements.txt
  ├── app/
  │   ├── __init__.py               # create_app() 工厂函数
  │   ├── routes/                   # 路由模块
  │   │   └── users.py
  │   ├── models/                   # 数据模型
  │   │   └── user.py
  │   ├── services/
  │   │   └── user_service.py
  │   └── templates/                # HTML 模板
  │       └── base.html
  └── tests/
""")


# =====================================================================
# 总结
# =====================================================================
print("=" * 65)
print("  总结：如何选择 Python Web 框架？")
print("=" * 65)

summary = """
  ┌────────────────────────────────────────────────────────────┐
  │ 场景                        │ 推荐框架                     │
  ├─────────────────────────────┼──────────────────────────────┤
  │ REST API / 微服务           │ FastAPI（首选）              │
  │ 全功能 Web 应用             │ Django                       │
  │ 快速原型 / 简单脚本         │ Flask                        │
  │ ML 模型服务化               │ FastAPI + uvicorn            │
  │ 实时应用（WebSocket）       │ FastAPI / Django Channels    │
  │ 来自 C# 背景               │ FastAPI（最接近 ASP.NET Core）│
  └─────────────────────────────┴──────────────────────────────┘

  对 C# 开发者的建议：
  ├── FastAPI 的学习曲线最低（路由+模型+依赖注入 都很像）
  ├── Django 功能最全但学习曲线高（自带 ORM/Admin/Auth）
  ├── Flask 最灵活但需要自己组装（类似 .NET Framework 时代）
  ├── 异步优先选 FastAPI，同步优先选 Django
  └── 无论选哪个，都要用 Pydantic 管理数据模型
"""
print(summary)
