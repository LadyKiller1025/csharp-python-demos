"""
Python 异常处理完整示例
对应文章：4.1 异常处理

C# 对比：
  Python try/except/else/finally  ≈  C# try/catch/when/finally
  Python 没有 catch 关键字，用 except 代替
  Python 没有 when 过滤器，但可以在 except 中用 if 判断
"""
import sys
import traceback

print("=" * 60)
print("1. 基础 try-except-finally")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   try { ... }
#   catch (DivideByZeroException ex) { ... }
#   catch (FormatException ex) { ... }
#   catch (Exception ex) { ... }
#   finally { ... }
# -------------------------------------------------------
try:
    result = 10 / int("0")
    print(result)
except ZeroDivisionError as e:
    # C# 中对应：catch (DivideByZeroException ex)
    print(f"除零错误: {e}")
except ValueError as e:
    # C# 中对应：catch (FormatException ex)
    print(f"格式错误: {e}")
except Exception as e:
    # C# 中对应：catch (Exception ex) — 兜底捕获
    print(f"其他错误: {e}")
finally:
    # Python 和 C# 的 finally 行为一致：无论是否异常都执行
    print("不管出不出错都执行 (finally)")

print()
print("=" * 60)
print("2. 多类型捕获 — 一个 except 捕获多种异常")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   catch (InvalidOperationException | ArgumentException ex)
#   C# 8+ 也支持管道符合并多种异常类型
# -------------------------------------------------------
data = {"name": "Alice"}
try:
    value = data["age"]           # KeyError
    result = int(value)           # 如果存在但无法转换则 ValueError
except (KeyError, TypeError) as e:
    # Python 允许用元组一次性捕获多种异常
    print(f"值或类型错误: {type(e).__name__}: {e}")

print()
print("=" * 60)
print("3. try-except-else-finally 完整流程")
print("=" * 60)

# -------------------------------------------------------
# C# 没有 else 子句，通常把 else 的逻辑放在 try 块末尾
# Python 的 else 只在 try 成功（无异常）时执行
# -------------------------------------------------------
try:
    num = int("42")   # 此处用字符串代替 input()，便于无交互运行
except ValueError:
    print("请输入有效数字")
else:
    # 只在 try 没有异常时执行（C# 中需自行放在 try 末尾）
    print(f"转换成功，结果是: {num}")
finally:
    # 无论如何都执行
    print("处理完成 (finally)")

print()
print("=" * 60)
print("4. 异常链 — raise...from (Exception Chaining)")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   throw new ApplicationException("处理失败", innerException);
#   或 ExceptionDispatchInfo.Capture(ex).Throw(); 保留完整堆栈
# -------------------------------------------------------
try:
    try:
        value = int("not_a_number")
    except ValueError as original:
        # raise...from 保留原始异常作为 __context__
        raise RuntimeError("数据转换失败") from original
except RuntimeError as e:
    print(f"外层异常: {e}")
    print(f"原始异常 (通过 __cause__): {e.__cause__}")
    print(f"自动链 (__context__): {e.__context__}")

print()
print("=" * 60)
print("5. 手动抑制异常链 — raise...from None")
print("=" * 60)

# -------------------------------------------------------
# raise...from None 表示「我知道原始异常，但不想暴露给调用者」
# C# 中没有直接等价物，通常通过只传递 Message 来实现
# -------------------------------------------------------
try:
    try:
        int("bad")
    except ValueError:
        # from None 表示不保留原始异常
        raise ValueError("输入格式不正确，请重试") from None
except ValueError as e:
    print(f"异常: {e}")
    print(f"__cause__ 为: {e.__cause__}")   # None

print()
print("=" * 60)
print("6. Exception Group (Python 3.11+)")
print("=" * 60)

# -------------------------------------------------------
# ExceptionGroup 是 Python 3.11 新增的，用于同时抛出多个异常
# C# 没有等价物，通常需要收集异常后逐一处理或用 AggregateException
# -------------------------------------------------------
if sys.version_info >= (3, 11):
    # except* 语法是 Python 3.11+ 新增的（ExceptionGroup）
    # 注意：except* 在 Python 3.10 及更早版本中是语法错误
    # 即使放在 if 块中也会在解析阶段报错，因此必须用 exec() 动态执行
    _code = '''
try:
    raise ExceptionGroup("多个验证错误", [
        ValueError("用户名为空"),
        TypeError("年龄必须是整数"),
        KeyError("缺少 email 字段"),
    ])
except* ValueError as eg:
    print(f"捕获到 ValueError 子异常:")
    for exc in eg.exceptions:
        print(f"  - {exc}")
except* TypeError as eg:
    print(f"捕获到 TypeError 子异常:")
    for exc in eg.exceptions:
        print(f"  - {exc}")
'''
    exec(_code)
else:
    print(f"[跳过] except* 语法需要 Python 3.11+，当前版本: {sys.version.split()[0]}")
    print("  ExceptionGroup 和 except* 是 Python 3.11 新增功能")
    print("  C# 对应概念: AggregateException + 逐个 catch")
    # 模拟 ExceptionGroup 的概念（Python 3.10 没有内置 ExceptionGroup）
    errors = [
        ValueError("用户名为空"),
        TypeError("年龄必须是整数"),
        KeyError("缺少 email 字段"),
    ]
    print(f"  模拟 ExceptionGroup - 包含 {len(errors)} 个异常:")
    for exc in errors:
        print(f"    - {type(exc).__name__}: {exc}")
    print("  Python 3.11+ 使用 except* 语法按类型匹配子异常")

print()
print("=" * 60)
print("7. 内置异常层次结构")
print("=" * 60)

# -------------------------------------------------------
# C# 异常层级：
#   System.Object > System.Exception > System.SystemException
#       > ArgumentException, InvalidOperationException ...
#   System.Object > System.Exception > System.ApplicationException
#
# Python 异常层级：
#   BaseException
#    +-- KeyboardInterrupt
#    +-- SystemExit
#    +-- GeneratorExit
#    +-- Exception
#         +-- ArithmeticError (ZeroDivisionError, OverflowError)
#         +-- LookupError (IndexError, KeyError)
#         +-- OSError (FileNotFoundError, PermissionError)
#         +-- ValueError, TypeError, AttributeError ...
# -------------------------------------------------------
print("BaseException 是所有异常的基类 (对应 C# System.Exception)")
print("Exception 继承自 BaseException，是大多数业务异常的基类")
print()

# 查看某个异常的继承链
exc = KeyError("test")
print(f"KeyError 的 MRO (方法解析顺序):")
for cls in type(exc).__mro__:
    print(f"  {cls.__name__}")

# 用 issubclass 判断异常关系（类似 C# 的 is / when）
print()
print(f"KeyError 是否是 LookupError 的子类? {issubclass(KeyError, LookupError)}")
print(f"KeyError 是否是 Exception 的子类? {issubclass(KeyError, Exception)}")

print()
print("=" * 60)
print("8. sys.exc_info() — 获取当前异常的详细信息")
print("=" * 60)

# -------------------------------------------------------
# C# 中可以通过 catch (Exception ex) 的 ex 对象获取信息
# Python 的 sys.exc_info() 返回 (异常类型, 异常实例, 回溯对象)
# 在 except 块外部也可以使用
# -------------------------------------------------------
try:
    int("not_a_number")
except:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print(f"异常类型: {exc_type.__name__}")
    print(f"异常实例: {exc_value}")
    print(f"回溯对象: {exc_traceback}")
    # 使用 traceback 模块格式化堆栈
    print("完整堆栈:")
    traceback.print_exc()

print()
print("=" * 60)
print("9. with 语句 — 上下文管理器处理异常")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   using (var reader = new StreamReader("file.txt")) { ... }
#   // 离开 using 块自动 Dispose，效果等同 Python 的 with
#
# Python 的 with 语句会在 __exit__ 中自动处理异常
# -------------------------------------------------------
import os

# 创建临时文件用于演示
test_file = "_temp_demo.txt"
with open(test_file, "w", encoding="utf-8") as f:
    f.write("Hello, Python 异常处理!\n")
    f.write("第二行内容")

# with 自动关闭文件，等同 C# 的 using
with open(test_file, "r", encoding="utf-8") as f:
    content = f.read()
    print(f"文件内容: {content}")

# 清理临时文件
os.remove(test_file)

print()
print("=" * 60)
print("10. 自定义上下文管理器与异常处理")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   实现 IDisposable 接口，Dispose() 方法中处理清理逻辑
# -------------------------------------------------------
class ManagedResource:
    """模拟一个需要资源管理的类（类似 C# 的 IDisposable）"""
    def __enter__(self):
        print("  [__enter__] 获取资源")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # exc_type: 异常类型（无异常时为 None）
        # exc_val:  异常实例
        # exc_tb:   回溯对象
        if exc_type is not None:
            print(f"  [__exit__] 捕获到异常: {exc_type.__name__}: {exc_val}")
        print("  [__exit__] 释放资源")
        # 返回 True 表示异常已被处理，不再向外传播
        # 返回 False 或 None 表示异常继续传播
        return False

# 场景 1：无异常
print("场景 1 - 正常执行:")
with ManagedResource():
    print("  [主逻辑] 正常工作")

# 场景 2：有异常，不抑制
print("\n场景 2 - 异常不抑制 (返回 None):")
try:
    with ManagedResource():
        print("  [主逻辑] 即将出错")
        raise ValueError("出错了!")
except ValueError as e:
    print(f"  [外部] 捕获到异常: {e}")

# 场景 3：有异常，抑制
print("\n场景 3 - 异常被抑制 (返回 True):")

class SuppressingResource:
    """与 ManagedResource 相同，但 __exit__ 返回 True 抑制异常"""
    def __enter__(self):
        print("  [__enter__] 获取资源")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"  [__exit__] 捕获到异常: {exc_type.__name__}: {exc_val}")
        print("  [__exit__] 释放资源")
        return True  # 返回 True 抑制异常

with SuppressingResource():
    print("  [主逻辑] 即将出错")
    raise ValueError("这个异常被上下文管理器吞掉了")
print("  [外部] 程序继续执行，异常被吞掉")

print()
print("=" * 60)
print("11. 异常处理最佳实践总结")
print("=" * 60)

# -------------------------------------------------------
# 最佳实践对比：
#
# Python                              | C#
# ------------------------------------|----------------------------------
# except Exception as e:              | catch (Exception ex)
# except (A, B) as e:                 | catch (A | B ex)          (C# 8+)
# except ValueError as e:             | catch (ValueError ex) when (...)
# raise ValueError("msg") from orig   | throw new X("msg", orig)
# try: ... finally: cleanup()         | try { ... } finally { ... }
# with open(...) as f:                | using (var f = ...)
# except*: ExceptionGroup            | catch (AggregateException)
# -------------------------------------------------------

# 反面示例：不要用裸 except
print("\n反面示例 — 不要用裸 except:")
try:
    int("bad")
except:  # 不推荐！会捕获 KeyboardInterrupt, SystemExit 等
    print("  裸 except 会捕获所有异常，包括 KeyboardInterrupt")

print("\n推荐做法 — 明确指定异常类型:")
try:
    int("bad")
except ValueError as e:
    print(f"  明确捕获 ValueError: {e}")

print()
print("=" * 60)
print("12. 异常与性能 (异常不是流程控制工具)")
print("=" * 60)

# -------------------------------------------------------
# C# 同理：异常有性能开销，不应用于正常控制流
# Python 异常比 C# 更轻量，但仍不应滥用
# -------------------------------------------------------
import time

# 正常方式 vs 异常方式的性能差异
def find_in_dict_normal(d, key):
    """推荐：先检查再操作"""
    if key in d:
        return d[key]
    return None

def find_in_dict_exception(d, key):
    """不推荐：用异常做流程控制"""
    try:
        return d[key]
    except KeyError:
        return None

test_dict = {i: i for i in range(1000)}
key_present = 500
key_absent = 9999

# 性能测试
start = time.perf_counter()
for _ in range(100000):
    find_in_dict_normal(test_dict, key_present)
    find_in_dict_normal(test_dict, key_absent)
normal_time = time.perf_counter() - start

start = time.perf_counter()
for _ in range(100000):
    find_in_dict_exception(test_dict, key_present)
    find_in_dict_exception(test_dict, key_absent)
exception_time = time.perf_counter() - start

print(f"正常方式 (key 存在+不存在) 10万次: {normal_time:.4f}s")
print(f"异常方式 (key 存在+不存在) 10万次: {exception_time:.4f}s")
print(f"结论: 当 key 不存在时，异常方式更慢; 当 key 通常存在时，正常方式更快")
print(f"       Python 中 EAFP (先做再说) 原则有时也适用，要视场景而定")

print()
print("所有异常处理示例运行完毕！")
