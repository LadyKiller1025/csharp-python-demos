# Python 模块与包示例
# 对应文章：3.5 模块与包
#
# C# 等价：namespace + using 指令
# Python 的模块系统比 C# 的 namespace 更灵活 —— 模块就是文件，包就是文件夹

# =====================================================================
# 1. 导入顺序（PEP 8 规范）
# =====================================================================
# Python 的导入顺序有严格规范，C# 类似但更宽松
#
#   # 1. 标准库（等价 C# 的 using System.*）
#   import os
#   import sys
#
#   # 2. 第三方库（等价 C# 的 NuGet 包）
#   import requests
#
#   # 3. 本地模块（等价 C# 的项目内 using）
#   from myapp.models import Person
#
# 各组之间用空行分隔

# =====================================================================
# 2. 基本导入方式
# =====================================================================

# --- 标准库导入（等价 C# using System; using System.IO;）---
import os          # 导入整个模块
import sys         # 等价 C# using System
from datetime import datetime, timedelta  # 等价 C# using static（导入特定成员）
from collections import OrderedDict       # 等价 C# using System.Collections.Generic
import importlib   # Python 独有：动态导入

# --- 别名（等价 C# 的 using 别名）---
# Python: import numpy as np
# C#:     using Np = NumPy.Numpy;
from datetime import datetime as dt
from collections import OrderedDict as OD

# =====================================================================
# 3. __name__ == "__main__" 模式
# =====================================================================
# Python 独有的入口守卫 —— C# 没有对应概念
# C# 等价：只有 Program.Main() 是入口点
# Python：被 import 时 __name__ 是模块名，直接运行时是 "__main__"

print("=" * 60)
print("3.5 模块与包")
print("=" * 60)

print("\n--- 1. __name__ 检查 ---")
print(f"当前文件的 __name__ = '{__name__}'")  # 直接运行时为 '__main__'
print(f"当前文件的 __file__ = '{__file__}'")
print(f"Python 版本: {sys.version.split()[0]}")

if __name__ == "__main__":
    print("这段代码只在直接运行时执行，被 import 时不会执行")
    # C# 等价：这段逻辑放在 Main() 里

# =====================================================================
# 4. 常用标准库演示
# =====================================================================
print("\n--- 2. os 模块（文件系统操作）---")
print(f"当前工作目录: {os.getcwd()}")
print(f"目录分隔符: {os.sep!r}")  # Windows 是 '\\'

print("\n--- 3. datetime 模块 ---")
now = dt.now()           # 使用别名导入
print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
tomorrow = now + timedelta(days=1)
print(f"明天:     {tomorrow.strftime('%Y-%m-%d')}")

print("\n--- 4. collections 模块 ---")
# OrderedDict 保持插入顺序（Python 3.7+ 普通 dict 也保序）
od = OD([("first", 1), ("second", 2), ("third", 3)])
print(f"OrderedDict: {od}")

# =====================================================================
# 5. 动态导入 importlib.reload
# =====================================================================
# C# 等价：Assembly.Load / Type.GetType（反射加载）
# Python：importlib 可以在运行时动态加载和重载模块

print("\n--- 5. 动态导入 importlib ---")
math_mod = importlib.import_module("math")  # 等价 C#：Assembly.Load("Math")
print(f"动态导入 math.pi = {math_mod.pi:.6f}")
print(f"math 模块类型: {type(math_mod)}")

# reload：重新加载已修改的模块（开发时有用）
reloaded = importlib.reload(math_mod)
print(f"reload 后 math.pi = {reloaded.pi:.6f}")

# =====================================================================
# 6. sys.path 与模块搜索路径
# =====================================================================
# C# 等价：AppDomain.CurrentDomain.GetAssemblies() + AssemblyResolve
# Python 按 sys.path 的顺序搜索模块

print("\n--- 6. sys.path 模块搜索路径 ---")
print(f"搜索路径数量: {len(sys.path)}")
for i, p in enumerate(sys.path[:5]):
    display = p if p else "(空字符串 = 当前目录)"
    print(f"  [{i}] {display}")
if len(sys.path) > 5:
    print(f"  ... 还有 {len(sys.path) - 5} 条路径")

# 动态添加搜索路径（C# 等价：修改 AppDomain 的 probing path）
print(f"\nsys.path.append('/tmp/custom') — 运行时添加搜索路径")
print(f"sys.modules 已加载模块数: {len(sys.modules)}")

# =====================================================================
# 7. 包结构图解
# =====================================================================
print("\n--- 7. Python 包结构 vs C# 项目结构 ---")
print("""
  Python 包结构:               C# 等价:
  mypackage/                   MyApp/
    __init__.py                  MyApp.csproj    (包标识)
    module1.py                   Models/
    module2.py                     Person.cs
    subpackage/                  Services/
      __init__.py                  Calculator.cs
      sub_module.py

  __init__.py 标识这是一个包 —— C# 用 .csproj 标识项目
  Python 包可以直接 import mypackage.module1
  C# 用 namespace MyApp.Models 来组织
""")

# =====================================================================
# 8. import * 的危险性
# =====================================================================
print("--- 8. from xxx import * 的危害 ---")
# from os import *  # 不推荐！会把 os 的所有名字导入当前命名空间
# 等价 C#：using static System.*;（一样会造成名字污染）
print("from os import * 会污染当前命名空间，不推荐使用")
print("建议：始终使用 from xxx import yyy 或 import xxx")

# =====================================================================
# 9. 模块的内置属性
# =====================================================================
print("\n--- 9. 模块内置属性 ---")
print(f"__name__:      {__name__!r}")      # 模块名
print(f"__file__:      {__file__!r}")      # 文件路径
print(f"__doc__:       {__doc__!r}")       # 文档字符串
print(f"sys.version:   {sys.version.split()[0]}")  # Python 版本
print(f"os.name:       {os.name!r}")       # 操作系统名称（'nt' = Windows）

# =====================================================================
# 10. 按 PEP 8 规范排列的导入示例
# =====================================================================
print("\n--- 10. PEP 8 导入规范总结 ---")
print("""
  # ===== PEP 8 导入顺序 =====
  # 1. 标准库
  import os
  import sys
  from datetime import datetime

  # 2. 第三方库（pip install 的）
  # import requests
  # import numpy as np

  # 3. 本地模块 / 包内导入
  # from myapp import models
  # from myapp.models import Person

  # 各组之间用空行分隔，每组内按字母排序
""")
