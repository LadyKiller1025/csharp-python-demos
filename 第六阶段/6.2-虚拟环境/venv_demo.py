"""
=================================================================
6.2 虚拟环境 —— Python 项目隔离 vs .NET 全局管理
对应文章：6.2 虚拟环境
=================================================================

C# 开发者的痛点：Python 没有像 .NET 那样的全局包管理
  - .NET: NuGet 全局缓存 + 项目级引用，天然隔离
  - Python: 全局安装 → 包冲突 → "在我机器上能跑"

虚拟环境就是解决这个问题的利器。
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

print("=" * 65)
print("  Python 虚拟环境 —— 项目隔离的艺术")
print("=" * 65)

# =====================================================================
# 第一部分：为什么需要虚拟环境？
# =====================================================================
print("\n" + "=" * 65)
print("  第一部分：为什么需要虚拟环境？")
print("=" * 65)

print("""
┌─────────────────────────────────────────────────────────────────┐
│  问题场景                                                        │
│                                                                  │
│  项目 A 需要 requests==2.28                                      │
│  项目 B 需要 requests==2.31（API 不兼容升级）                    │
│                                                                  │
│  如果全局安装：                                                   │
│  pip install requests==2.28  → requests 2.28 安装了              │
│  pip install requests==2.31  → requests 2.31 覆盖了 2.28！       │
│  项目 A 崩了 [CRASH]                                                   │
│                                                                  │
│  解决方案：每个项目一个独立的"小世界"（虚拟环境）                 │
└─────────────────────────────────────────────────────────────────┘

对比 C#：
  C# 项目天然隔离 —— 每个 .csproj 独立引用 NuGet 包，
  即使两个项目引用不同版本也不冲突（全局缓存 + 按需加载）。

  Python 的全局 site-packages 是共享的 → 必须用虚拟环境隔离。
""")

# =====================================================================
# 第二部分：venv —— Python 内置虚拟环境
# =====================================================================
print("\n" + "=" * 65)
print("  第二部分：venv —— Python 内置虚拟环境")
print("=" * 65)

print("""
venv 是 Python 3.3+ 内置的虚拟环境模块，无需额外安装。

命令对照：
  ┌──────────────────────────────────┬──────────────────────────────────┐
  │ Python                           │ C#/.NET                          │
  ├──────────────────────────────────┼──────────────────────────────────┤
  │ python -m venv .venv             │ dotnet new console -n MyApp      │
  │ .venv\\Scripts\\activate (Win)      │ （无需，.NET 天然隔离）           │
  │ source .venv/bin/activate (Unix) │                                  │
  │ deactivate                       │ （无需）                          │
  │ pip install <pkg>                │ dotnet add package <pkg>         │
  │ pip freeze > requirements.txt    │ dotnet list package              │
  └──────────────────────────────────┴──────────────────────────────────┘
""")

# 演示 venv 创建过程（不实际执行，仅展示结构）
print("--- venv 目录结构 ---")
print("""
  .venv/
  ├── Scripts/              # Windows
  │   ├── python.exe        ← 虚拟环境的 Python 解释器
  │   ├── pip.exe           ← 虚拟环境的 pip
  │   ├── activate          ← 激活脚本（修改 PATH）
  │   └── deactivate        ← 退出脚本
  ├── Lib/
  │   └── site-packages/    ← 虚拟环境的包安装目录
  │       ├── pip/
  │       ├── setuptools/
  │       └── ...           ← 你安装的包都在这里
  └── pyvenv.cfg            ← 虚拟环境配置（指向系统 Python）
""")

# 实际演示：显示当前 Python 环境信息
print("--- 当前环境信息 ---")
print(f"  Python 解释器:    {sys.executable}")
print(f"  Python 版本:      {sys.version.split()[0]}")
print(f"  VIRTUAL_ENV 环境变量: {os.environ.get('VIRTUAL_ENV', '(未在虚拟环境中)')}")
print(f"  是否在 venv 中:   {'是' if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else '否'}")
print(f"  sys.prefix:       {sys.prefix}")
print(f"  sys.base_prefix:  {sys.base_prefix if hasattr(sys, 'base_prefix') else 'N/A'}")

# =====================================================================
# 第三部分：虚拟环境实战操作
# =====================================================================
print("\n" + "=" * 65)
print("  第三部分：虚拟环境实战操作（演示创建和使用）")
print("=" * 65)

def demonstrate_venv():
    """在临时目录中演示 venv 的创建和使用"""
    tmp_dir = tempfile.mkdtemp(prefix="venv_demo_")
    venv_path = os.path.join(tmp_dir, ".venv")

    try:
        # 创建虚拟环境
        print(f"\n  [步骤 1] 创建虚拟环境: python -m venv .venv")
        result = subprocess.run(
            [sys.executable, "-m", "venv", venv_path],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print(f"  [OK] 创建成功: {venv_path}")
        else:
            print(f"  [X] 创建失败: {result.stderr}")
            return

        # 确定虚拟环境的 Python 路径
        if os.name == "nt":
            venv_python = os.path.join(venv_path, "Scripts", "python.exe")
            venv_pip = os.path.join(venv_path, "Scripts", "pip.exe")
        else:
            venv_python = os.path.join(venv_path, "bin", "python")
            venv_pip = os.path.join(venv_path, "bin", "pip")

        # 查看虚拟环境信息
        print(f"\n  [步骤 2] 查看虚拟环境信息")
        result = subprocess.run(
            [venv_python, "-c",
             "import sys; print(f'  Python: {sys.executable}'); "
             "print(f'  版本: {sys.version.split()[0]}'); "
             "print(f'  prefix: {sys.prefix}'); "
             "print(f'  base_prefix: {sys.base_prefix}'); "
             "print(f'  在虚拟环境中: {sys.prefix != sys.base_prefix}')"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            print(result.stdout.strip())

        # 安装包到虚拟环境
        print(f"\n  [步骤 3] 在虚拟环境中安装包")
        result = subprocess.run(
            [venv_pip, "install", "pip", "--quiet"],
            capture_output=True, text=True, timeout=30
        )
        print(f"  pip 已更新")

        # 列出虚拟环境中的包
        print(f"\n  [步骤 4] 列出虚拟环境中的包（pip list）")
        result = subprocess.run(
            [venv_pip, "list", "--format=columns"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            for line in lines[:8]:  # 只显示前 8 行
                print(f"    {line}")
            if len(lines) > 8:
                print(f"    ... (共 {len(lines) - 2} 个包)")

        # 对比：系统 Python 的包列表
        print(f"\n  [步骤 5] 对比系统 Python 的包数量")
        result_system = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=columns"],
            capture_output=True, text=True, timeout=10
        )
        system_count = len(result_system.stdout.strip().split("\n")) - 2 if result_system.returncode == 0 else 0

        result_venv = subprocess.run(
            [venv_pip, "list", "--format=columns"],
            capture_output=True, text=True, timeout=10
        )
        venv_count = len(result_venv.stdout.strip().split("\n")) - 2 if result_venv.returncode == 0 else 0

        print(f"    系统 Python 包数量: {system_count}")
        print(f"    虚拟环境包数量:     {venv_count}")
        print(f"    → 虚拟环境是干净的，只包含基础包")

    except Exception as e:
        print(f"  演示出错: {e}")
    finally:
        # 清理临时目录
        shutil.rmtree(tmp_dir, ignore_errors=True)
        print(f"\n  [清理] 临时虚拟环境已删除")

demonstrate_venv()


# =====================================================================
# 第四部分：其他虚拟环境工具
# =====================================================================
print("\n" + "=" * 65)
print("  第四部分：虚拟环境工具全景")
print("=" * 65)

tools = {
    "venv": {
        "说明": "Python 3.3+ 内置，无需安装",
        "优点": "官方标准，轻量，无额外依赖",
        "缺点": "功能基础，不管理 Python 版本",
        "适用": "大多数项目的默认选择",
        "命令": "python -m venv .venv",
    },
    "virtualenv": {
        "说明": "第三方库，venv 的增强版",
        "优点": "支持 Python 2，更快（并行创建），可复制系统包",
        "缺点": "需要额外安装",
        "适用": "需要 Python 2 支持或更快创建速度",
        "命令": "virtualenv .venv",
    },
    "conda": {
        "说明": "Anaconda 的环境管理器",
        "优点": "管理非 Python 依赖（C 库等），数据科学生态完善",
        "缺点": "体积大，与 pip 可能冲突",
        "适用": "数据科学/机器学习项目",
        "命令": "conda create -n myenv python=3.11",
    },
    "pyenv": {
        "说明": "Python 版本管理器（不管理包）",
        "优点": "轻松切换多个 Python 版本",
        "缺点": "不管理依赖包，通常配合 venv 使用",
        "适用": "需要多个 Python 版本并存",
        "命令": "pyenv install 3.12.0 && pyenv local 3.12.0",
    },
    "uv": {
        "说明": "Rust 实现的超快虚拟环境 + 包管理",
        "优点": "极快，一个工具替代 venv + pip + pip-tools",
        "缺点": "较新（2024+），生态还在完善",
        "适用": "追求速度的新项目（推荐）",
        "命令": "uv venv && uv pip install requests",
    },
}

for name, info in tools.items():
    print(f"\n  [{name}]")
    for key, value in info.items():
        print(f"    {key:6s}: {value}")


# =====================================================================
# 第五部分：.python-version 与版本管理
# =====================================================================
print("\n" + "=" * 65)
print("  第五部分：.python-version —— Python 版本锁定")
print("=" * 65)

print("""
┌─────────────────────────────────────────────────────────────────┐
│  概念对照                                                        │
│                                                                  │
│  C#                          Python                              │
│  ────                        ──────                              │
│  global.json                 .python-version                     │
│  { "sdk": { "version": } }   3.12.0                              │
│  控制 SDK 版本               控制 Python 解释器版本               │
│                                                                  │
│  Dockerfile                 .python-version                      │
│  FROM mcr.microsoft.com/    3.12.0                               │
│    dotnet/sdk:8.0           (pyenv/virtualenv 自动识别)          │
└─────────────────────────────────────────────────────────────────┘

.python-version 文件内容示例：
  3.12.0

配合工具使用：
  - pyenv:       自动切换到指定版本
  - uv:          uv python install 读取此文件
  - tox:         按此版本运行测试
  - GitHub Actions: setup-python action 读取此文件
""")


# =====================================================================
# 第六部分：Docker 中的虚拟环境
# =====================================================================
print("\n" + "=" * 65)
print("  第六部分：Docker 中的虚拟环境策略")
print("=" * 65)

print("""
=== 策略一：Docker 内使用 venv（推荐）===

  FROM python:3.12-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN python -m venv /opt/venv \\
      && /opt/venv/bin/pip install -r requirements.txt
  ENV PATH="/opt/venv/bin:$PATH"
  COPY . .
  CMD ["python", "main.py"]

  优点：精确控制 Python 版本 + 包版本
  类比 C#：FROM mcr.microsoft.com/dotnet/aspnet:8.0

=== 策略二：系统级 pip（简单但不推荐）===

  FROM python:3.12-slim
  COPY requirements.txt .
  RUN pip install -r requirements.txt

  缺点：污染系统 Python，可能与系统包冲突

=== 与 C# Docker 对比 ===

  # C# 多阶段构建（Python 也可以）
  FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
  RUN dotnet publish -c Release

  FROM mcr.microsoft.com/dotnet/aspnet:8.0
  COPY --from=build /app/out .
  ENTRYPOINT ["dotnet", "MyApp.dll"]

  # Python 多阶段构建
  FROM python:3.12 AS build
  RUN pip install --user -r requirements.txt

  FROM python:3.12-slim
  COPY --from=build /root/.local /root/.local
  ENV PATH="/root/.local/bin:$PATH"
  CMD ["python", "main.py"]
""")


# =====================================================================
# 第七部分：最佳实践总结
# =====================================================================
print("\n" + "=" * 65)
print("  第七部分：虚拟环境最佳实践")
print("=" * 65)

best_practices = """
  [OK] DO（推荐做法）:
  ├── 每个项目创建独立虚拟环境
  ├── .gitignore 中添加 .venv/
  ├── 使用 requirements.txt 或 pyproject.toml 锁定依赖
  ├── 在 Docker 中也使用虚拟环境
  ├── 使用 .python-version 锁定 Python 版本
  └── CI/CD 中也创建虚拟环境

  [X] DON'T（避免做法）:
  ├── 全局 pip install（项目间互相污染）
  ├── 虚拟环境目录加入版本控制
  ├── 不锁版本（requirements.txt 没有版本号）
  ├── 在虚拟环境中 sudo pip install
  └── 多个项目共用同一个虚拟环境
"""
print(best_practices)

# .gitignore 示例
print("--- .gitignore 中应包含 ---")
gitignore = """
  # Python 虚拟环境
  .venv/
  venv/
  env/

  # Python 缓存
  __pycache__/
  *.py[cod]
  *$py.class

  # 发行文件
  dist/
  build/
  *.egg-info/

  # Poetry
  poetry.lock        # 是否提交有争议，库不提交，应用提交

  # uv
  .python-version    # 如果使用 pyenv 管理
"""
print(gitignore)

print("\n" + "=" * 65)
print("  总结：虚拟环境选择指南")
print("=" * 65)

summary = """
  ┌─────────────────────┬────────────────────────────────────────┐
  │ 场景                 │ 推荐方案                               │
  ├─────────────────────┼────────────────────────────────────────┤
  │ 普通项目开发         │ venv（内置，够用）                     │
  │ 追求速度             │ uv（Rust，极快）                       │
  │ 数据科学             │ conda + venv（管理 C 库依赖）          │
  │ 需要多 Python 版本   │ pyenv + venv                           │
  │ 生产部署             │ Docker（包含虚拟环境）                 │
  │ 快速原型             │ uv（uv run 直接运行，无需手动激活）    │
  └─────────────────────┴────────────────────────────────────────┘

  对 C# 开发者的直觉翻译：
  ├── venv  ≈  每个项目一个独立的 NuGet 包缓存
  ├── conda ≈  Docker（管理操作系统级依赖）
  ├── pyenv ≈  global.json（SDK 版本管理）
  └── uv    ≈  dotnet CLI（快速 + 简洁 + 一站式）
"""
print(summary)
