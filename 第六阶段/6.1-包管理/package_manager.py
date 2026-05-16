"""
=================================================================
6.1 包管理 —— Python vs C# 的依赖管理全景
对应文章：6.1 包管理
=================================================================

C# 开发者熟悉的：
  NuGet + .csproj (PackageReference) + dotnet CLI
  dotnet add package Newtonsoft.Json
  dotnet restore / dotnet build

Python 对应的：
  pip + requirements.txt / pyproject.toml
  pip install requests
  pip freeze > requirements.txt

本文件演示：pip、requirements.txt、pyproject.toml、Poetry、uv、依赖组
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from textwrap import dedent

print("=" * 65)
print("  Python 包管理全览 —— 从 C# NuGet 到 pip/poetry/uv")
print("=" * 65)

# =====================================================================
# 第一部分：pip —— 最基础的包管理器（类比 NuGet）
# =====================================================================
print("\n" + "=" * 65)
print("  第一部分：pip —— 最基础的包管理器")
print("=" * 65)

print("""
┌─────────────────────────────────────────────────────────────────┐
│  概念对照                                                        │
│                                                                  │
│  C# NuGet                     Python pip                        │
│  ─────────────                ─────────────                      │
│  dotnet add package X         pip install X                      │
│  dotnet remove package X      pip uninstall X                    │
│  dotnet list package          pip list                           │
│  dotnet restore               pip install -r requirements.txt    │
│  NuGet.org                    PyPI (pypi.org)                    │
│  packages.config              requirements.txt                   │
│  .csproj PackageReference     pyproject.toml                     │
└─────────────────────────────────────────────────────────────────┘
""")

# pip 常用命令演示
print("--- pip 常用命令速查 ---")
pip_commands = [
    ("pip install requests",              "安装最新版 requests"),
    ("pip install flask==3.0.0",          "安装指定版本"),
    ("pip install 'pandas>=2.0,<3.0'",    "安装版本范围"),
    ("pip install --upgrade requests",    "升级到最新版"),
    ("pip uninstall requests",            "卸载包"),
    ("pip show requests",                 "查看包详细信息"),
    ("pip list",                          "列出所有已安装包"),
    ("pip freeze > requirements.txt",     "导出依赖（锁版本）"),
    ("pip install -r requirements.txt",   "从文件批量安装"),
    ("pip install --dry-run requests",    "仅模拟安装，不实际执行"),
]

for cmd, desc in pip_commands:
    print(f"  {cmd:45s} # {desc}")

# 实际演示：查看当前环境的已安装包
print("\n--- 当前环境信息 ---")
print(f"  Python 路径:   {sys.executable}")
print(f"  Python 版本:   {sys.version.split()[0]}")
print(f"  pip 版本:      ", end="")
try:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "--version"],
        capture_output=True, text=True, timeout=10
    )
    print(result.stdout.strip().split("(")[0].strip() if result.returncode == 0 else "未安装")
except Exception:
    print("未安装")

# 演示 pip show
print("\n--- pip show 演示（查看 setuptools 信息）---")
try:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", "pip"],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode == 0:
        for line in result.stdout.strip().split("\n")[:5]:
            print(f"  {line}")
    else:
        print("  无法获取包信息")
except Exception:
    print("  pip 不可用")


# =====================================================================
# 第二部分：requirements.txt —— 依赖锁定文件
# =====================================================================
print("\n" + "=" * 65)
print("  第二部分：requirements.txt —— 依赖锁定文件")
print("=" * 65)

print("""
┌─────────────────────────────────────────────────────────────────┐
│  概念对照                                                        │
│                                                                  │
│  C#                          Python                              │
│  ─────                       ──────                              │
│  .csproj (PackageReference)  pyproject.toml (声明依赖)           │
│  packages.lock.json          requirements.txt (锁定版本)         │
│  NuGet 包源配置              pip.conf / pyproject.toml [tool]     │
└─────────────────────────────────────────────────────────────────┘
""")

# 展示 requirements.txt 的常见格式
print("--- requirements.txt 常见格式 ---")
req_examples = dedent("""\
    # 精确版本锁定（推荐生产环境）
    requests==2.31.0
    flask==3.0.0
    sqlalchemy==2.0.23

    # 版本范围（开发环境灵活些）
    requests>=2.28,<3.0
    flask>=3.0

    # 不固定版本（不推荐，可能导致环境不一致）
    requests

    # 引用其他文件
    -r base.txt

    # 环境条件（Python 3.7+）
    importlib-metadata>=4.0; python_version < "3.8"

    # 可选依赖组
    # pytest  # 开发依赖，单独文件管理
""")
print(req_examples)


# =====================================================================
# 第三部分：pyproject.toml —— 现代 Python 项目配置
# =====================================================================
print("=" * 65)
print("  第三部分：pyproject.toml —— 现代 Python 项目配置")
print("=" * 65)

print("""
pyproject.toml 是 Python 的"现代化 .csproj"：
  - PEP 518 定义构建系统
  - PEP 621 定义项目元数据
  - 工具配置集中管理（替代 setup.cfg、tox.ini 等）
""")

pyproject_example = dedent("""\
    [build-system]
    requires = ["hatchling"]            # 构建工具（类似 MSBuild）
    build-backend = "hatchling.build"

    [project]
    name = "my-python-app"              # 项目名
    version = "1.0.0"                   # 版本号
    description = "一个示例 Python 项目"
    readme = "README.md"
    license = "MIT"
    requires-python = ">=3.10"          # Python 版本要求
    authors = [
        { name = "张三", email = "zhangsan@example.com" },
    ]

    # 核心依赖（类比 .csproj 的 PackageReference）
    dependencies = [
        "requests>=2.28",
        "fastapi>=0.100",
        "pydantic>=2.0",
    ]

    # 可选依赖组（类比 C# 的条件编译引用）
    [project.optional-dependencies]
    dev = [
        "pytest>=7.0",
        "pytest-cov",
        "ruff",
        "mypy",
    ]
    docs = [
        "sphinx",
        "sphinx-rtd-theme",
    ]
    test = [
        "pytest>=7.0",
        "pytest-asyncio",
        "httpx",        # 用于测试 FastAPI
    ]

    # 工具配置（替代各种 .cfg、.ini 文件）
    [tool.ruff]
    line-length = 88
    target-version = "py310"

    [tool.ruff.lint]
    select = ["E", "F", "I", "N", "UP"]

    [tool.pytest.ini_options]
    testpaths = ["tests"]
    addopts = "-v --tb=short"

    [tool.mypy]
    python_version = "3.10"
    strict = true
""")
print("--- pyproject.toml 示例 ---")
print(pyproject_example)

print("对比 C# .csproj:")
csproj_comparison = dedent("""\
    <!-- C# .csproj -->
    <Project Sdk="Microsoft.NET.Sdk">
      <PropertyGroup>
        <TargetFramework>net8.0</TargetFramework>
        <Version>1.0.0</Version>
      </PropertyGroup>
      <ItemGroup>
        <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
        <PackageReference Include="Serilog" Version="3.1.1" />
      </ItemGroup>
    </Project>
""")
print(csproj_comparison)


# =====================================================================
# 第四部分：Poetry —— Python 的"NuGet + MSBuild"一体化方案
# =====================================================================
print("=" * 65)
print("  第四部分：Poetry —— 一体化包管理与构建工具")
print("=" * 65)

print("""
Poetry 解决的问题：
  1. 依赖解析 + 版本锁定 → poetry.lock（类似 packages.lock.json）
  2. 虚拟环境自动管理 → 无需手动 venv
  3. 打包发布 → poetry build / poetry publish
  4. 脚本入口 → pyproject.toml [tool.poetry.scripts]
""")

poetry_commands = [
    ("poetry init",                  "交互式创建 pyproject.toml"),
    ("poetry add requests",          "添加依赖（自动更新 pyproject.toml + lock）"),
    ("poetry add --group dev pytest", "添加开发依赖组"),
    ("poetry remove requests",       "移除依赖"),
    ("poetry install",               "安装所有依赖（含 lock 文件）"),
    ("poetry update",                "更新依赖到兼容版本"),
    ("poetry lock",                  "仅锁定版本，不安装"),
    ("poetry run python main.py",    "在虚拟环境中运行命令"),
    ("poetry build",                 "构建 sdist + wheel"),
    ("poetry publish",               "发布到 PyPI"),
    ("poetry shell",                 "激活虚拟环境 shell"),
    ("poetry env info",              "查看虚拟环境信息"),
]

print("--- Poetry 常用命令 ---")
for cmd, desc in poetry_commands:
    print(f"  {cmd:45s} # {desc}")

print("\n--- Poetry pyproject.toml 示例 ---")
poetry_pyproject = dedent("""\
    [tool.poetry]
    name = "my-app"
    version = "1.0.0"
    description = "Poetry 管理的项目"
    authors = ["张三 <zhangsan@example.com>"]

    [tool.poetry.dependencies]
    python = "^3.10"
    requests = "^2.31"
    fastapi = "^0.100"

    [tool.poetry.group.dev.dependencies]
    pytest = "^7.0"
    ruff = "^0.1"
    mypy = "^1.0"

    [tool.poetry.scripts]
    my-cli = "my_app.cli:main"      # 入口点，类似 C# 的 Top-level statements
""")
print(poetry_pyproject)


# =====================================================================
# 第五部分：uv —— Rust 驱动的超快包管理器（2024 年新星）
# =====================================================================
print("=" * 65)
print("  第五部分：uv —— Rust 实现的极速包管理器")
print("=" * 65)

print("""
uv 是 Astral 团队（ruff 作者）用 Rust 开发的包管理器：
  - 比 pip 快 10-100 倍
  - 兼容 pip、pip-tools、virtualenv 的命令
  - 可替代 pip + venv + pip-tools 的组合
  - 2024 年已成为 Python 社区趋势
""")

uv_commands = [
    ("uv pip install requests",             "安装包（速度极快）"),
    ("uv pip install -r requirements.txt",  "从文件安装"),
    ("uv pip compile requirements.in",      "生成锁文件（类似 poetry lock）"),
    ("uv pip sync requirements.txt",        "同步环境到锁文件状态"),
    ("uv venv .venv",                       "创建虚拟环境"),
    ("uv run python main.py",               "运行脚本（自动管理环境）"),
    ("uv run pytest",                       "运行工具（自动管理环境）"),
    ("uv init my-project",                  "创建新项目"),
    ("uv add requests",                     "添加依赖"),
    ("uv add --dev pytest",                 "添加开发依赖"),
    ("uv tree",                             "查看依赖树"),
    ("uv python install 3.12",              "安装 Python 版本"),
]

print("--- uv 常用命令速查 ---")
for cmd, desc in uv_commands:
    print(f"  {cmd:45s} # {desc}")

print("""
uv 的优势：
  ├── 用 Rust 编写，单二进制文件，安装简单
  ├── 兼容 pip 命令格式，迁移成本低
  ├── 全局缓存 + 硬链接，节省磁盘空间
  ├── 跨平台（Windows/macOS/Linux）
  └── 可管理 Python 版本（替代 pyenv）
""")


# =====================================================================
# 第六部分：依赖组管理 —— 开发/测试/生产依赖分离
# =====================================================================
print("=" * 65)
print("  第六部分：依赖组 —— 开发/测试/生产分离")
print("=" * 65)

print("""
┌─────────────────────────────────────────────────────────────────┐
│  概念对照                                                        │
│                                                                  │
│  C#                              Python                          │
│  ────                            ──────                          │
│  <PackageReference Condition=    [project.optional-dependencies]  │
│    "'$(Configuration)'=='Debug'"> pyproject.toml                  │
│  dotnet-tools.json (local tools) poetry group add dev pytest     │
│  Directory.Build.props           requirements-dev.txt             │
└─────────────────────────────────────────────────────────────────┘
""")

print("--- 依赖组最佳实践 ---")
dep_groups = {
    "核心依赖 (dependencies)": {
        "说明": "生产运行必需的包",
        "C# 类比": ".csproj 中无条件的 PackageReference",
        "示例": "requests, fastapi, sqlalchemy",
    },
    "开发依赖 (dev)": {
        "说明": "开发工具：linter、formatter、type checker",
        "C# 类比": "dotnet-format, analyzers",
        "示例": "ruff, mypy, black, pre-commit",
    },
    "测试依赖 (test)": {
        "说明": "测试框架和工具",
        "C# 类比": "xUnit, Moq, FluentAssertions",
        "示例": "pytest, pytest-cov, pytest-asyncio, httpx",
    },
    "文档依赖 (docs)": {
        "说明": "文档生成工具",
        "C# 类比": "DocFX",
        "示例": "sphinx, sphinx-rtd-theme, mkdocs",
    },
}

for group, info in dep_groups.items():
    print(f"\n  [{group}]")
    for key, value in info.items():
        print(f"    {key}: {value}")

print("\n--- 依赖组导出示例（pip-tools）---")
print("""
  # 创建依赖声明文件
  echo "requests>=2.28" > requirements.in
  echo "flask>=3.0" >> requirements.in

  # 生成精确锁文件
  pip-compile requirements.in

  # 安装（使用锁文件）
  pip install -r requirements.txt

  # 开发依赖单独管理
  pip-compile requirements-dev.in -o requirements-dev.txt
""")


# =====================================================================
# 第七部分：实战对比 —— 完整项目依赖管理流程
# =====================================================================
print("\n" + "=" * 65)
print("  第七部分：实战对比 —— 创建项目的完整流程")
print("=" * 65)

print("""
=== C# 新建项目流程 ===

  dotnet new console -n MyApp
  cd MyApp
  dotnet add package Newtonsoft.Json
  dotnet add package Serilog
  dotnet add package --group dev xUnit
  dotnet restore
  dotnet build

  # 项目文件：
  # MyApp/
  #   MyApp.csproj          ← 依赖声明 + 构建配置
  #   MyApp.sln             ← 解决方案
  #   Program.cs            ← 入口
  #   global.json           ← SDK 版本锁定（可选）

=== Python 新建项目流程（pip 方式）===

  mkdir my-app && cd my-app
  python -m venv .venv
  .venv\\Scripts\\activate        # Windows
  pip install requests flask
  pip freeze > requirements.txt

  # 项目文件：
  # my-app/
  #   requirements.txt      ← 依赖列表（版本锁定）
  #   .venv/                ← 虚拟环境（不入版本控制）
  #   main.py               ← 入口

=== Python 新建项目流程（Poetry 方式）===

  poetry init --name my-app
  poetry add requests flask
  poetry add --group dev pytest
  poetry install

  # 项目文件：
  # my-app/
  #   pyproject.toml        ← 依赖声明 + 项目配置
  #   poetry.lock           ← 精确版本锁
  #   src/my_app/           ← 源代码包
  #   tests/                ← 测试

=== Python 新建项目流程（uv 方式）===

  uv init my-app
  cd my-app
  uv add requests flask
  uv add --group dev pytest

  # 项目文件：
  # my-app/
  #   pyproject.toml        ← 依赖声明
  #   uv.lock               ← 精确版本锁
  #   main.py               ← 入口
""")


# =====================================================================
# 第八部分：版本约束语法对比
# =====================================================================
print("=" * 65)
print("  第八部分：版本约束语法对比")
print("=" * 65)

version_rules = [
    ("==2.31.0",     "==2.31.0",      "精确版本"),
    (">=2.0,<3.0",   "[2.0,3.0)",     "范围约束"),
    ("~=2.31",       ">=2.31,<2.32",  "兼容版本（ ~= ）"),
    (">=2.28",       ">=2.28",        "最低版本"),
    ("!=2.30",       "!=2.30",        "排除版本"),
    ("^2.0 (Poetry)", ">=2.0,<3.0",   "Poetry 插入符"),
    ("* (Poetry)",    ">=0.0",         "任意版本"),
]

print(f"  {'Python 约束':25s} {'等价含义':25s} {'说明'}")
print("  " + "-" * 70)
for py_constraint, meaning, desc in version_rules:
    print(f"  {py_constraint:25s} {meaning:25s} {desc}")

print("""
对比 C# NuGet 版本约束：
  [2.0,3.0)     →  NuGet 范围语法（等同 Python 的 >=2.0,<3.0）
  [2.0,]        →  最低版本（NuGet 2.0+）
  2.31.0        →  精确版本
""")


# =====================================================================
# 总结
# =====================================================================
print("\n" + "=" * 65)
print("  总结：如何选择包管理方案？")
print("=" * 65)

summary = """
  ┌────────────────┬─────────────────────────────────────────────┐
  │ 方案           │ 适用场景                                     │
  ├────────────────┼─────────────────────────────────────────────┤
  │ pip            │ 快速验证、脚本、CI/CD 中的简单安装            │
  │ pip + pip-tools│ 需要锁文件但不想引入新工具                    │
  │ Poetry         │ 标准项目开发，需要打包发布                    │
  │ uv             │ 追求速度，新项目首选（2024+趋势）             │
  │ conda          │ 数据科学/机器学习（管理非 Python 依赖）       │
  └────────────────┴─────────────────────────────────────────────┘

  对 C# 开发者的建议：
  ├── 如果你习惯 NuGet 的简洁 → 用 uv（最接近 dotnet add package 的体验）
  ├── 如果你需要完整项目管理 → 用 Poetry（最接近 dotnet new + .csproj）
  ├── 如果你在做数据科学 → 用 conda + pip 混合
  └── 小脚本/快速原型 → pip 足够，别过度工程化
"""
print(summary)
