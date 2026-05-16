# Python 变量与类型示例
# 对应文章：1.2 变量与类型系统

print("=== 基础赋值 ===")
# Python 天生就是"推断"的，不需要声明类型
x = 5              # int
name = "张三"      # str
price = 9.99       # float
is_true = True     # bool

# 也可以加类型注解（但解释器不理你，只给 IDE 和 mypy 用）
y: int = 10
name2: str = "李四"
print(f"x={x}, y={y}, name2={name2}")

# ==================== 变量可以改变类型（动态类型！） ====================
print("\n=== 动态类型 ===")
x = 5
print(f"x = {x}, type = {type(x)}")       # <class 'int'>
x = "hello"
print(f"x = {x}, type = {type(x)}")       # <class 'str'>
# C# 对比：C# 的 var 一旦推断出类型就不能变了

# ==================== 类型检查 ====================
print("\n=== 类型检查 ===")
print(f"isinstance(5, int)    = {isinstance(5, int)}")       # True
print(f"isinstance(5, (int, float)) = {isinstance(5, (int, float))}")  # True（可以检查多个类型）
print(f"type(5).__name__      = {type(5).__name__}")          # "int"
# 推荐用 isinstance() 而不是 type() == ，因为 isinstance 支持继承

# ==================== 类型转换 ====================
print("\n=== 类型转换 ===")
s = "123"
n = int(s)                     # 123
f = float("3.14")              # 3.14
b = bool(0)                    # False
b2 = bool(1)                   # True
b3 = bool("")                  # False
print(f"int('123')      = {n}")
print(f"float('3.14')   = {f}")
print(f"bool(0)         = {b}")
print(f"bool('')        = {b3}")

# 安全转换（Python 没有 TryParse，需要 try-except）
def safe_int(s):
    """安全地将字符串转为整数，失败返回 (None, False)"""
    try:
        return int(s), True
    except ValueError:
        return None, False

val, ok = safe_int("abc")
print(f"safe_int('abc') = ({val}, {ok})")
val, ok = safe_int("42")
print(f"safe_int('42')  = ({val}, {ok})")

# ==================== 常量约定 ====================
print("\n=== 常量约定 ===")
# Python 没有 const 关键字，靠全大写命名约定
PI = 3.14159
GREETING = "Hello"
# PI = 999  # 不会报错！但违反约定，linter 会警告
print(f"PI = {PI}")

# 如果需要真正不可变，可以用 dataclass(frozen=True) 或 typing.Final
from typing import Final
MAX_SIZE: Final = 100  # 类型提示：这是一个常量
print(f"MAX_SIZE = {MAX_SIZE}")
