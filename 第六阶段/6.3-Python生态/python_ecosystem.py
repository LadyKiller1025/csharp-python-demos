"""
=================================================================
6.3 Python 生态 —— C# 开发者的 Python 库全景指南
对应文章：6.3 Python生态
=================================================================

Python 生态系统是其最大优势之一。
本文件帮助 C# 开发者快速找到"Python 侧的等价物"，
同时了解 Python 独有的生态优势领域（数据科学、AI/ML）。
"""

import sys
import json
import math
from dataclasses import dataclass, field
from typing import Any

print("=" * 65)
print("  Python 生态全景 —— 从 C# 视角理解 Python 库")
print("=" * 65)


# =====================================================================
# 第一部分：Web 框架
# =====================================================================
print("\n" + "=" * 65)
print("  第一部分：Web 框架")
print("=" * 65)

print("""
┌─────────────────────────────────────────────────────────────────┐
│  Web 框架对照                                                    │
│                                                                  │
│  Python              C#                    定位                  │
│  ──────              ──                    ──                    │
│  Flask               Minimal APIs          轻量、灵活             │
│  FastAPI             ASP.NET Core          现代、异步、自动文档   │
│  Django              ASP.NET MVC           全功能、自带 Admin     │
│  Starlette           —                     ASGI 底层框架          │
│  Litestar            —                     FastAPI 替代品        │
└─────────────────────────────────────────────────────────────────┘
""")

# Web 框架详细对比
web_frameworks = {
    "Flask": {
        "定位": "微框架",
        "C# 类比": "ASP.NET Core Minimal APIs",
        "特点": "简单灵活，按需扩展",
        "适合": "API 服务、原型开发、微服务",
        "路由": "@app.route('/hello')",
        "中间件": "通过装饰器/扩展",
        "ORM": "无（选 SQLAlchemy/Tortoise）",
        "模板": "Jinja2",
    },
    "FastAPI": {
        "定位": "现代异步框架",
        "C# 类比": "ASP.NET Core（最接近）",
        "特点": "自动 API 文档、类型安全、高性能",
        "适合": "REST API、微服务、ML 服务",
        "路由": "@app.get('/hello')",
        "中间件": "middleware 装饰器",
        "ORM": "无（选 SQLAlchemy/Tortoise）",
        "模板": "无（专注 API）",
    },
    "Django": {
        "定位": "全功能框架",
        "C# 类比": "ASP.NET MVC + Entity Framework + Admin",
        "特点": "自带 ORM、Admin、Auth、模板引擎",
        "适合": "内容管理、电商、复杂 Web 应用",
        "路由": "urlpatterns = [path('hello/')]",
        "中间件": "MIDDLEWARE 配置",
        "ORM": "Django ORM（内置）",
        "模板": "Django 模板语言",
    },
}

for name, info in web_frameworks.items():
    print(f"  [{name}]")
    for key, value in info.items():
        print(f"    {key:8s}: {value}")
    print()


# =====================================================================
# 第二部分：数据科学生态
# =====================================================================
print("=" * 65)
print("  第二部分：数据科学 —— Python 的王牌领域")
print("=" * 65)

print("""
┌─────────────────────────────────────────────────────────────────┐
│  这是 C# 生态相对薄弱的领域，也是 Python 最大的优势。            │
│  C# 有 ML.NET 和 Math.NET，但生态成熟度远不及 Python。           │
└─────────────────────────────────────────────────────────────────┘
""")

# 演示 math 模块（标准库，无需安装）
print("--- Python math 模块（标准库）---")
print(f"  pi = {math.pi}")
print(f"  e = {math.e}")
print(f"  sqrt(144) = {math.sqrt(144)}")
print(f"  log(100, 10) = {math.log(100, 10)}")
print(f"  sin(pi/2) = {math.sin(math.pi / 2):.6f}")
print()

# 演示基本数据处理（不依赖第三方库）
print("--- Python 内置数据处理能力 ---")
# 模拟 NumPy 的基本操作
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"  原始数据: {data}")
print(f"  列表推导式 (类比 NumPy 向量化): {[x**2 for x in data]}")
print(f"  sum = {sum(data)}, avg = {sum(data)/len(data):.1f}")
print(f"  min = {min(data)}, max = {max(data)}")
print(f"  sorted (降序): {sorted(data, reverse=True)}")
print()

# NumPy/Pandas 概念介绍
data_science_libs = {
    "NumPy": {
        "用途": "数值计算基础库",
        "C# 类比": "System.Numerics + Math.NET Numerics",
        "核心概念": "ndarray（多维数组），比 list 快 10-100 倍",
        "安装": "pip install numpy",
        "代码示例": "np.array([1,2,3]) * 2  →  [2,4,6]",
    },
    "Pandas": {
        "用途": "数据分析和处理",
        "C# 类比": "LINQ + DataTable（但更强大）",
        "核心概念": "DataFrame（表格数据）、Series（列数据）",
        "安装": "pip install pandas",
        "代码示例": "df.groupby('city').agg({'salary': 'mean'})",
    },
    "Matplotlib": {
        "用途": "基础绑图库",
        "C# 类比": "ScottPlot / LiveCharts",
        "核心概念": "pyplot 接口，类似 MATLAB",
        "安装": "pip install matplotlib",
        "代码示例": "plt.plot(x, y); plt.show()",
    },
    "Polars": {
        "用途": "高性能 DataFrame（Rust 实现）",
        "C# 类比": "无直接对应，可类比高性能 LINQ",
        "核心概念": "惰性求值、多线程、零拷贝",
        "安装": "pip install polars",
        "代码示例": "pl.scan_csv('data.csv').filter(col('a') > 1).collect()",
    },
}

print("--- 数据科学核心库 ---")
for name, info in data_science_libs.items():
    print(f"\n  [{name}]")
    for key, value in info.items():
        print(f"    {key:10s}: {value}")


# =====================================================================
# 第三部分：AI/ML 生态
# =====================================================================
print("\n\n" + "=" * 65)
print("  第三部分：AI/ML —— Python 的另一个王牌")
print("=" * 65)

print("""
AI/ML 领域 Python 几乎是唯一的主流选择。
C# 有 ML.NET 和 ONNX Runtime，但模型训练生态远不及 Python。
""")

ai_libs = {
    "PyTorch": {
        "定位": "动态计算图，研究首选",
        "C# 类比": "无直接对应",
        "特点": "Pythonic API，调试方便，学术界标准",
        "安装": "pip install torch",
        "使用场景": "模型研究、论文复现、快速原型",
    },
    "TensorFlow": {
        "定位": "静态计算图（已转向动态），工业部署",
        "C# 类比": "TensorFlow.NET（官方绑定）",
        "特点": "生产部署成熟，TF Serving",
        "安装": "pip install tensorflow",
        "使用场景": "大规模训练、移动端部署",
    },
    "scikit-learn": {
        "定位": "传统机器学习",
        "C# 类比": "ML.NET",
        "特点": "统一 API（fit/predict），包含常见算法",
        "安装": "pip install scikit-learn",
        "使用场景": "分类、回归、聚类、降维",
    },
    "Hugging Face": {
        "定位": "NLP/LLM 生态平台",
        "C# 类比": "无直接对应",
        "特点": "transformers 库 + 模型市场 + 数据集",
        "安装": "pip install transformers",
        "使用场景": "NLP、LLM 微调、文本生成",
    },
    "ONNX Runtime": {
        "定位": "跨框架模型推理",
        "C# 类比": "Microsoft.ML.OnnxRuntime（C# 也有）",
        "特点": "Python 训练 → ONNX → C#/Python/JS 部署",
        "安装": "pip install onnxruntime",
        "使用场景": "模型部署（C# 和 Python 共享）",
    },
}

for name, info in ai_libs.items():
    print(f"\n  [{name}]")
    for key, value in info.items():
        print(f"    {key:10s}: {value}")


# =====================================================================
# 第四部分：自动化与测试
# =====================================================================
print("\n\n" + "=" * 65)
print("  第四部分：自动化与测试")
print("=" * 65)

print("""
┌─────────────────────────────────────────────────────────────────┐
│  测试框架对照                                                    │
│                                                                  │
│  Python              C#                    特点                  │
│  ──────              ──                    ──                    │
│  pytest              xUnit                 现代、简洁、插件丰富   │
│  unittest            NUnit/MSTest          内置、面向对象         │
│  pytest-mock         Moq                   Mock 框架              │
│  pytest-cover        coverlet              代码覆盖率             │
│  Hypothesis          —                     属性测试（Python 独有）│
│  Playwright          Playwright            浏览器自动化           │
│  Selenium            Selenium              浏览器自动化（老牌）   │
└─────────────────────────────────────────────────────────────────┘
""")

# 展示 pytest 的简洁性
print("--- pytest vs xUnit 对比 ---")
print("""
  # Python pytest
  def test_add():
      assert 1 + 1 == 2

  def test_string_upper():
      assert "hello".upper() == "HELLO"

  # 运行: pytest test_example.py -v

  // C# xUnit
  [Fact]
  public void TestAdd()
  {
      Assert.Equal(2, 1 + 1);
  }

  [Fact]
  public void TestStringUpper()
  {
      Assert.Equal("HELLO", "hello".ToUpper());
  }

  // 运行: dotnet test

  → pytest 更简洁，无需类包装，自动发现测试
  → xUnit 需要 [Fact] 属性和 Assert 类
""")

# 自动化工具
automation_libs = {
    "自动化脚本": {
        "Python": "Fabric, Invoke, subprocess",
        "C#": "Process 类, Cake Build",
    },
    "浏览器自动化": {
        "Python": "Playwright, Selenium",
        "C#": "Playwright.NET, Selenium WebDriver",
    },
    "爬虫": {
        "Python": "Scrapy, BeautifulSoup, httpx",
        "C#": "HtmlAgilityPack, ScrapySharp",
    },
    "任务调度": {
        "Python": "APScheduler, Celery",
        "C#": "Hangfire, Quartz.NET",
    },
    "文件处理": {
        "Python": "openpyxl (Excel), PyPDF2, Pillow",
        "C#": "EPPlus, iTextSharp, System.Drawing",
    },
}

print("--- 自动化工具对照 ---")
for category, tools in automation_libs.items():
    print(f"\n  [{category}]")
    print(f"    Python: {tools['Python']}")
    print(f"    C#:     {tools['C#']}")


# =====================================================================
# 第五部分：开发工具生态
# =====================================================================
print("\n\n" + "=" * 65)
print("  第五部分：开发工具生态")
print("=" * 65)

print("""
┌─────────────────────────────────────────────────────────────────┐
│  开发工具对照                                                    │
│                                                                  │
│  Python              C#                    用途                  │
│  ──────              ──                    ──                    │
│  ruff                Roslyn analyzers      代码检查（lint）       │
│  black               dotnet format         代码格式化             │
│  mypy                nullable reference    静态类型检查           │
│                      types                 类型系统               │
│  isort               dotnet format         import 排序            │
│  pre-commit          git hooks             Git 提交钩子           │
│  tox                 —                     多环境测试             │
│  nox                  —                    多环境测试（Python 版）│
│  mkdocs              DocFX                 文档生成               │
│  uv                  dotnet CLI            包管理 + 虚拟环境      │
└─────────────────────────────────────────────────────────────────┘
""")

# 展示 ruff 的速度优势
print("--- ruff：用 Rust 写的 Python linter ---")
print("""
  ruff 是 Python 社区的新星工具：
  - 用 Rust 编写，比传统 Python linter (pylint/flake8) 快 10-100 倍
  - 集成了 flake8、isort、pylint 等多个工具的功能
  - 可以替代 pre-commit 中的多个 hook

  # 安装
  pip install ruff

  # 检查代码
  ruff check .

  # 自动修复
  ruff check --fix .

  # 格式化（替代 black）
  ruff format .

  对比 C#：
  - ruff ≈ Roslyn analyzers + dotnet format（但更快）
  - ruff 的配置在 pyproject.toml 中（单一配置文件）
""")


# =====================================================================
# 第六部分：完整生态对比表
# =====================================================================
print("=" * 65)
print("  第六部分：Python vs C# 完整生态对比")
print("=" * 65)

print("\n  {:16s} {:30s} {:30s}".format("领域", "Python", "C#/.NET"))
print("  " + "-" * 80)

comparisons = [
    ("Web 框架",       "FastAPI/Django/Flask",          "ASP.NET Core/Blazor"),
    ("数据科学",       "NumPy/Pandas/Polars",           "ML.NET/Math.NET"),
    ("AI/ML",          "PyTorch/TensorFlow",            "ML.NET/ONNX Runtime"),
    ("ORM",            "SQLAlchemy/Tortoise ORM",       "EF Core/Dapper"),
    ("测试",           "pytest/unittest",               "xUnit/NUnit/MSTest"),
    ("Mock",           "pytest-mock/unittest.mock",     "Moq/NSubstitute"),
    ("包管理",         "pip/poetry/uv",                 "NuGet/dotnet CLI"),
    ("虚拟环境",       "venv/conda/uv",                 ".csproj 天然隔离"),
    ("代码检查",       "ruff/mypy/pylint",              "Roslyn analyzers"),
    ("格式化",         "ruff format/black",             "dotnet format"),
    ("文档",           "mkdocs/sphinx",                 "DocFX"),
    ("CI/CD",          "tox/nox + GitHub Actions",      "dotnet CLI + GH Actions"),
    ("容器化",         "Docker + venv",                 "Docker + NuGet"),
    ("消息队列",       "Celery/RQ/Dramatiq",           "Hangfire/Rebus"),
    ("缓存",           "Redis (redis-py)",              "StackExchange.Redis"),
    ("日志",           "logging/structlog/loguru",      "Serilog/NLog"),
    ("配置",           "pydantic-settings/dotenv",      "IConfiguration"),
    ("任务调度",       "APScheduler/Celery Beat",       "Quartz.NET/Hangfire"),
    ("API 文档",       "FastAPI 自动生成",              "Swashbuckle/NSwag"),
    ("RPC",            "gRPC (grpcio)",                 "gRPC (.NET)"),
]

for area, py, cs in comparisons:
    print(f"  {area:16s} {py:30s} {cs:30s}")

print()


# =====================================================================
# 第七部分：Python 独有的优势领域
# =====================================================================
print("=" * 65)
print("  第七部分：Python 独有的优势领域")
print("=" * 65)

print("""
这些领域是 C# 生态明显不足的，也是学习 Python 的核心动力：

  1. 数据科学
     ├── NumPy/Pandas/Polars → 数据处理（C# 没有等价物）
     ├── Matplotlib/Plotly/Seaborn → 可视化（ScottPlot 可用但差距大）
     └── Jupyter Notebook → 交互式计算（C# 有 Polyglot Notebooks 但生态小）

  2. AI/机器学习
     ├── PyTorch/TensorFlow → 模型训练（C# 无法竞争）
     ├── Hugging Face → NLP/LLM 生态（C# 完全没有）
     └── ONNX → 跨语言部署桥梁（C# 可消费 Python 训练的模型）

  3. 科学计算
     ├── SciPy → 科学算法库
     ├── SymPy → 符号计算
     └── Statsmodels → 统计建模

  4. 网络爬虫
     ├── Scrapy → 全功能爬虫框架
     ├── BeautifulSoup → HTML 解析
     └── httpx → 异步 HTTP 客户端

  5. 胶水语言特性
     ├── subprocess → 调用系统命令
     ├── ctypes/cffi → 调用 C 库
     └── pythonnet → 调用 .NET 库
""")


# =====================================================================
# 第八部分：实战 —— 用标准库模拟数据处理
# =====================================================================
print("=" * 65)
print("  第八部分：实战 —— 用 Python 标准库处理数据")
print("=" * 65)

print("\n（无需安装任何第三方库，展示 Python 内置数据处理能力）\n")

# 模拟数据
employees = [
    {"name": "Alice",   "dept": "Engineering", "salary": 120000, "years": 5},
    {"name": "Bob",     "dept": "Engineering", "salary": 135000, "years": 8},
    {"name": "Charlie", "dept": "Marketing",   "salary": 95000,  "years": 3},
    {"name": "Diana",   "dept": "Marketing",   "salary": 105000, "years": 6},
    {"name": "Eve",     "dept": "Engineering", "salary": 150000, "years": 10},
    {"name": "Frank",   "dept": "Sales",       "salary": 88000,  "years": 2},
    {"name": "Grace",   "dept": "Sales",       "salary": 110000, "years": 7},
]

print("--- 员工数据 ---")
print(f"  {'Name':10s} {'Dept':15s} {'Salary':>10s} {'Years':>6s}")
print("  " + "-" * 45)
for emp in employees:
    print(f"  {emp['name']:10s} {emp['dept']:15s} {emp['salary']:>10,} {emp['years']:>6d}")

# 按部门分组统计
print("\n--- 按部门分组统计（模拟 Pandas groupby）---")
depts = {}
for emp in employees:
    dept = emp["dept"]
    if dept not in depts:
        depts[dept] = {"count": 0, "total_salary": 0, "names": []}
    depts[dept]["count"] += 1
    depts[dept]["total_salary"] += emp["salary"]
    depts[dept]["names"].append(emp["name"])

print(f"  {'Department':15s} {'Count':>6s} {'Avg Salary':>12s} {'Members'}")
print("  " + "-" * 60)
for dept, stats in sorted(depts.items()):
    avg = stats["total_salary"] / stats["count"]
    names = ", ".join(stats["names"])
    print(f"  {dept:15s} {stats['count']:>6d} {avg:>12,.0f} {names}")

# 筛选和排序
print("\n--- 筛选：年薪 > 100000 的员工 ---")
high_earners = [e for e in employees if e["salary"] > 100000]
high_earners.sort(key=lambda e: e["salary"], reverse=True)
for emp in high_earners:
    print(f"  {emp['name']:10s} {emp['dept']:15s} ${emp['salary']:,}")

# 使用 map/filter/reduce 风格
print("\n--- 函数式风格操作 ---")
all_salaries = list(map(lambda e: e["salary"], employees))
print(f"  所有薪资: {all_salaries}")
print(f"  总薪资:   ${sum(all_salaries):,}")
print(f"  最高薪资: ${max(all_salaries):,}")
print(f"  最低薪资: ${min(all_salaries):,}")
print(f"  平均薪资: ${sum(all_salaries) / len(all_salaries):,.0f}")

# 列表推导式（Python 的 LINQ）
print("\n--- 列表推导式（Python 版 LINQ）---")
eng_salaries = [e["salary"] for e in employees if e["dept"] == "Engineering"]
print(f"  工程部薪资: {eng_salaries}")
print(f"  工程部平均: ${sum(eng_salaries) / len(eng_salaries):,.0f}")

senior = [f"{e['name']} ({e['years']}年)" for e in employees if e["years"] >= 5]
print(f"  资深员工 (>=5年): {senior}")

# 字典推导式
print("\n--- 字典推导式 ---")
name_to_salary = {e["name"]: e["salary"] for e in employees}
print(f"  name → salary 映射: {name_to_salary}")

# 排序
print("\n--- 多级排序 ---")
by_salary = sorted(employees, key=lambda e: (-e["salary"], e["name"]))
print(f"  按薪资降序:")
for emp in by_salary:
    print(f"    {emp['name']:10s} ${emp['salary']:>10,}")


# =====================================================================
# 第九部分：C# 对比代码片段
# =====================================================================
print("\n\n" + "=" * 65)
print("  第九部分：等价 C# 代码片段对比")
print("=" * 65)

print("""
  // C# 等价写法（LINQ）
  var highEarners = employees
      .Where(e => e.Salary > 100_000)
      .OrderByDescending(e => e.Salary)
      .Select(e => $"{e.Name}: ${e.Salary:N0}");

  // Python 写法
  # high_earners = [f"{e['name']}: ${e['salary']:,}"
  #                 for e in employees if e['salary'] > 100_000]

  // C# 分组统计
  var deptGroups = employees
      .GroupBy(e => e.Dept)
      .Select(g => new {
          Dept = g.Key,
          Count = g.Count(),
          AvgSalary = g.Average(e => e.Salary)
      });

  // Python 分组统计
  # from itertools import groupby
  # from operator import itemgetter
  # sorted_emps = sorted(employees, key=itemgetter('dept'))
  # for dept, group in groupby(sorted_emps, key=itemgetter('dept')):
  #     items = list(group)
  #     avg = sum(e['salary'] for e in items) / len(items)
  #     print(f"{dept}: avg=${avg:,.0f}")
""")


# =====================================================================
# 总结
# =====================================================================
print("=" * 65)
print("  总结：Python 生态选择指南")
print("=" * 65)

summary = """
  对 C# 开发者的建议：

  [TARGET] 你的目标领域            -> 推荐的 Python 库
  ─────────────────────────────────────────────────────
  Web API 开发               → FastAPI（最接近 ASP.NET Core 体验）
  数据处理/分析              → Pandas + NumPy
  机器学习/深度学习          → PyTorch + scikit-learn
  自动化脚本                → subprocess + pathlib
  测试                      → pytest + pytest-mock
  爬虫                      → httpx + BeautifulSoup
  CLI 工具                  → click + rich
  日志                      → loguru（比 logging 更友好）

  [TIP] 关键认知：
  ├── Python 的优势在数据科学/AI，不在 Web 框架
  ├── 不要用 Python 做它不擅长的事（高性能计算、强类型）
  ├── Python + C# 混合使用是最佳策略（Python 做 AI，C# 做服务）
  └── 利用 Python 生态补足 C# 生态的短板
"""
print(summary)
