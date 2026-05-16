# =============================================================================
# Python 3.14 新特性示例 — C# 老兵的 Python 修炼手册 5.7
# 对应文章：5.7 Python 3.14新特性
# 关键概念：PEP 649 (迟延求值注解), 新语法特性, 性能优化,
#           对比 C# 最新特性
# =============================================================================
# 【注意】
# Python 3.14 预计 2025 年 10 月发布
# 部分特性可能在最终版本中有所变化
# 本文件中的代码尽量兼容当前版本，无法运行的用注释说明
# =============================================================================

import sys
import time
from typing import Any, overload


# =============================================================================
# 1. PEP 649: 迟延求值类型注解 (Deferred Evaluation of Annotations)
# =============================================================================
# 这是 Python 3.14 最重要的变化之一!
#
# 之前的行为 (PEP 563, from __future__ import annotations):
#   - 所有注解被转换为字符串
#   - 访问时需要用 eval() 还原
#   - 导致了很多复杂性
#
# Python 3.14 的行为 (PEP 649):
#   - 注解在访问时才求值（懒加载）
#   - 不再需要 eval() 还原
#   - 保持了向后兼容性
#
# 【C# 对比】
# C# 的注解 (Attributes) 也是在运行时求值的
# 但 C# 是编译时求值并嵌入到 IL 中
# Python 3.14 让注解的行为更接近 C#
# =============================================================================


def demo_pep649():
    """演示 PEP 649 迟延求值注解"""
    print("\n=== 1. PEP 649: 迟延求值类型注解 ===")

    def greet(name: str) -> str:
        return f"Hello, {name}!"

    # 访问注解
    # 在 Python 3.14 中，__annotations__ 在访问时才求值
    # 在旧版本中，需要用 eval() 还原字符串形式的注解
    annotations = greet.__annotations__
    print(f"  函数注解: {annotations}")
    print(f"  返回类型: {annotations.get('return')}")

    # 之前 (PEP 563) 的问题:
    # from __future__ import annotations 会让注解变成字符串
    # def greet(name: str) -> str: ...
    # greet.__annotations__ == {'name': 'str', 'return': 'str'}  # 字符串!
    # 需要 eval(annotations['name']) 才能得到 str 类型

    # PEP 649 解决了这个问题:
    # 注解保持为真实的类型对象，不需要 eval()

    print("\n  【P563 vs P649】")
    print("  P563 (旧): 注解变成字符串，需要 eval() 还原")
    print("  P649 (新): 注解在访问时才求值，保持为类型对象")

    # 演示类型对象
    print(f"\n  注解类型: {type(annotations.get('name'))}")
    print(f"  值: {annotations.get('name')}")

    print("\n  【C# 对比】")
    print("  C# Attributes 在编译时嵌入 IL，运行时直接访问")
    print("  Python P649 让注解行为更接近 C#")


# =============================================================================
# 2. 之前版本的关键特性回顾 (3.10 - 3.13)
# =============================================================================
# 在介绍 3.14 之前，先回顾一下 Python 近几个版本的重要特性
# 这些特性是 C# 开发者应该知道的


def demo_recent_features():
    """回顾近期 Python 特性"""
    print("\n=== 2. 近期 Python 特性回顾 (3.10-3.13) ===")

    # --- Python 3.10: match/case 模式匹配 ---
    # 【C# 对比】C# switch + pattern matching
    def classify_value(value: Any) -> str:
        match value:
            case int() if value > 0:
                return f"正整数: {value}"
            case int() if value < 0:
                return f"负整数: {value}"
            case 0:
                return "零"
            case str() as s if len(s) > 0:
                return f"非空字符串: '{s}'"
            case list() as lst:
                return f"列表，长度: {len(lst)}"
            case _:
                return f"其他: {type(value).__name__}"

    test_values = [42, -3, 0, "hello", [1, 2], 3.14]
    print("  match/case 模式匹配 (Python 3.10+):")
    for v in test_values:
        print(f"    {v!r:20} -> {classify_value(v)}")

    # --- Python 3.12: 泛型语法 ---
    # 【C# 对比】C# 的泛型 <T>
    # Python 3.12+: def first[T](lst: list[T]) -> T:
    # 旧语法: T = TypeVar("T"); def first(lst: list[T]) -> T:
    print("\n  Python 3.12+ 内置泛型:")
    print("    def first[T](lst: list[T]) -> T: ...")
    print("    class Stack[T]: ...")
    print("    对比 C#: T First<T>(List<T> lst)")

    # --- Python 3.13: 更好的错误消息 ---
    print("\n  Python 3.13+:")
    print("    - 实验性 free-threaded 模式 (无 GIL)")
    print("    - 改进的错误消息")
    print("    - 交互式解释器改进")


# =============================================================================
# 3. Python 3.14 新语法特性
# =============================================================================
# 【C# 对比】
# C# 12/13/14 的新特性:
# - primary constructors (C# 12)
# - collection expressions (C# 12)
# - string interpolation improvements
# - field keyword (C# 13 preview)


def demo_new_syntax():
    """Python 3.14 新语法特性"""
    print("\n=== 3. Python 3.14 新语法特性 ===")

    # --- PEP 758: except 和 except* 的改进 ---
    # Python 3.14 允许 except 不需要括号（单个异常时）
    # 以及 except* 的简化语法
    print("  PEP 758: except 改进")
    print("    旧: except (ValueError, TypeError):")
    print("    新: except ValueError, TypeError:")
    print("    对比 C#: catch (ValueError | TypeError) { }")

    # --- PEP 750: 模板字符串 (t-strings) ---
    # 类似 f-string 但返回 Template 对象而不是字符串
    # 适合构建 HTML、SQL 等需要安全处理的字符串
    print("\n  PEP 750: 模板字符串 (t-strings)")
    print('    template = t"<div>{name}</div>"  # 返回 Template 对象')
    print('    对比 f-string: html = f"<div>{name}</div>"  # 返回 str')
    print("    用途: SQL 注入防护、HTML 转义、国际化")

    # --- PEP 649: 访问闭包中的注解 ---
    print("\n  PEP 649 的实际好处:")
    print("    - 框架可以在运行时获取真实的类型信息")
    print("    - 不再需要 'from __future__ import annotations' 的 hack")
    print("    - 类型检查器 (mypy) 行为更一致")

    # --- 其他改进 ---
    print("\n  其他 Python 3.14 改进:")
    print("    - 性能持续优化 (启动速度、内存使用)")
    print("    - 改进的错误消息")
    print("    - 子解释器 API 改进 (PEP 734)")
    print("    - 更好的 Windows 支持")


# =============================================================================
# 4. 性能对比：Python vs C#
# =============================================================================
# 【C# 对比】
# C# 通常比 Python 快 10-100 倍
# Python 3.14 持续优化，但差距仍然巨大


def demo_performance():
    """性能对比演示"""
    print("\n=== 4. 性能对比：Python vs C# ===")

    # CPU 密集型任务
    n = 5_000_000

    start = time.perf_counter()
    result = sum(i * i for i in range(n))
    python_time = time.perf_counter() - start
    print(f"  Python: sum(i*i for i in range({n:,}))")
    print(f"  结果: {result:,}")
    print(f"  耗时: {python_time:.4f}s")

    # 用数学公式对比
    start = time.perf_counter()
    result_formula = n * (n - 1) * (2 * n - 1) // 6
    formula_time = time.perf_counter() - start
    print(f"\n  数学公式: n*(n-1)*(2n-1)/6")
    print(f"  结果: {result_formula:,}")
    print(f"  耗时: {formula_time:.8f}s")
    print(f"  加速: {python_time / formula_time:.0f}x (算法优化)")

    print("\n  C# 估算 (相同硬件):")
    print(f"    循环版本: ~{python_time / 50:.4f}s (约快 50x)")
    print(f"    公式版本: ~{formula_time:.8f}s")

    print("\n  Python 3.14 性能改进:")
    print("    - 启动速度提升 ~20%")
    print("    - 内存使用减少 ~10%")
    print("    - JIT 编译器优化 (实验性)")


# =============================================================================
# 5. Python 3.14 vs C# 14 特性对比
# =============================================================================

def demo_comparison():
    """Python 3.14 vs C# 14 对比"""
    print("\n=== 5. Python 3.14 vs C# 14 特性对比 ===")
    print("  ┌────────────────────────┬────────────────────────┬────────────────────────┐")
    print("  │ Python 3.14            │ C# 14                  │ 说明                   │")
    print("  ├────────────────────────┼────────────────────────┼────────────────────────┤")
    print("  │ PEP 649 迟延注解       │ 编译时注解求值         │ 注解求值时机           │")
    print("  │ t-strings 模板字符串   │ 插值字符串处理         │ 安全字符串构建         │")
    print("  │ match/case (3.10+)     │ switch pattern (C# 8+) │ 模式匹配               │")
    print("  │ type[T] 内置泛型 (3.12)│ <T> 泛型               │ 泛型语法               │")
    print("  │ free-threaded (实验)   │ 天然无 GIL             │ 并行能力               │")
    print("  │ asyncio 性能优化       │ async/await 优化       │ 异步性能               │")
    print("  │ 子解释器 API           │ AppDomain (已废弃)     │ 隔离执行环境           │")
    print("  │ dataclasses 持续增强   │ record/record struct   │ 数据类                 │")
    print("  └────────────────────────┴────────────────────────┴────────────────────────┘")


# =============================================================================
# 6. 给 C# 开发者的建议
# =============================================================================

def demo_tips_for_csharp():
    """给 C# 开发者的 Python 3.14 学习建议"""
    print("\n=== 6. 给 C# 开发者的 Python 3.14 学习建议 ===")

    tips = [
        ("1. 类型注解越来越重要",
         "PEP 649 让运行时类型信息更可靠，框架会越来越多地利用这一点"),
        ("2. match/case 是 C# switch 的等价物",
         "如果你熟悉 C# pattern matching，Python match/case 上手很快"),
        ("3. 异步编程是 Python 的核心",
         "asyncio 在 3.14 中继续优化，高并发场景必用"),
        ("4. 性能仍然是短板",
         "CPU 密集型任务考虑用 C extension 或调用 C# 库"),
        ("5. 类型系统持续增强",
         "Python 的类型系统越来越接近 C#，但仍然是可选的"),
        ("6. free-threaded 模式值得关注",
         "如果 GIL 被完全移除，Python 的并发能力将大幅提升"),
    ]

    for title, detail in tips:
        print(f"  {title}")
        print(f"    {detail}")


# =============================================================================
# 7. 代码风格演进：Python 3.8 vs 3.14
# =============================================================================

def demo_style_evolution():
    """展示 Python 代码风格的演进"""
    print("\n=== 7. Python 代码风格演进 ===")

    print("  --- 泛型定义 ---")
    print("  Python 3.8: T = TypeVar('T')")
    print("              def first(lst: List[T]) -> T:")
    print("  Python 3.12+: def first[T](lst: list[T]) -> T:")
    print("  C#:          T First<T>(List<T> lst)")

    print("\n  --- 可空类型 ---")
    print("  Python 3.8: Optional[str] 或 Union[str, None]")
    print("  Python 3.10+: str | None")
    print("  C#:          string?")

    print("\n  --- 模式匹配 ---")
    print("  Python 3.8: if isinstance(x, int) and x > 0: ...")
    print("  Python 3.10+: match x:")
    print("                  case int() if x > 0: ...")
    print("  C#:          switch (x) { > 0 => ..., _ => ... }")

    print("\n  --- 数据类 ---")
    print("  Python 3.7: @dataclass class P: name: str; age: int")
    print("  Python 3.10+: @dataclass(slots=True, frozen=True)")
    print("  C# 9+:     record Person(string Name, int Age);")

    print("\n  --- 上下文管理器 ---")
    print("  Python:  with open(f) as file: ...")
    print("  Python 3.10+: with (A() as a, B() as b): ...")
    print("  C# 8+:   using var file = new StreamWriter(...);")


# =============================================================================
# 主程序入口
# =============================================================================

def main():
    """运行所有演示"""
    print("=" * 60)
    print("  C# 老兵的 Python 修炼手册 — 5.7 Python 3.14 新特性")
    print("=" * 60)
    print(f"  当前 Python 版本: {sys.version}")
    print(f"  Python 实现: {sys.implementation.name}")

    demo_pep649()
    demo_recent_features()
    demo_new_syntax()
    demo_performance()
    demo_comparison()
    demo_tips_for_csharp()
    demo_style_evolution()

    print("\n" + "=" * 60)
    print("  总结:")
    print("  1. Python 3.14 的 PEP 649 是类型系统的重大改进")
    print("  2. Python 的语法越来越接近 C#（但保持动态特性）")
    print("  3. 性能持续优化，但 CPU 密集型仍建议用 C#")
    print("  4. free-threaded 模式如果成熟，将改变 Python 的并发格局")
    print("  5. 类型提示从可选变为'强烈建议'，框架越来越多地依赖它")
    print("=" * 60)


if __name__ == "__main__":
    main()
