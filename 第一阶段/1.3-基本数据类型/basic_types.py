# Python 基本数据类型示例
# 对应文章：1.3 基本数据类型

# ==================== 整数类型（统一的 int，无上限！） ====================
print("=== 整数类型 ===")
a = 255
b = 32767
c = 2147483647
d = 9223372036854775807
# Python 的 int 没有上限，随便算！
e = 2 ** 1000
print(f"2^1000 的位数: {len(str(e))}")  # 302 位！C# 需要 BigInteger

# 不同进制表示
print(f"二进制:  {0b1010}")      # 10
print(f"八进制:  {0o17}")        # 15
print(f"十六进制: {0xFF}")       # 255

# ==================== 浮点数 ====================
print("\n=== 浮点数 ===")
f1 = 3.14       # 64位双精度（Python 没有 float32/decimal 区分）
f2 = 3.14e10    # 科学计数法 = 3.14 × 10^10
f3 = 1.5e-4     # 0.00015
print(f"3.14e10 = {f2}")

# 浮点数精度问题（所有语言都有！）
print(f"0.1 + 0.2 = {0.1 + 0.2}")         # 0.30000000000000004
print(f"0.1 + 0.2 == 0.3? {0.1 + 0.2 == 0.3}")  # False！
# 精确计算用 decimal 模块
from decimal import Decimal
print(f"Decimal: {Decimal('0.1') + Decimal('0.2')}")  # 0.3

# ==================== 复数（C# 没有的！） ====================
print("\n=== 复数 ===")
h = 3 + 4j     # Python 原生支持复数
print(f"复数: {h}")
print(f"实部: {h.real}")    # 3.0
print(f"虚部: {h.imag}")    # 4.0
print(f"模: {abs(h)}")      # 5.0（勾股定理）

# ==================== 布尔类型（就是整数！） ====================
print("\n=== 布尔类型 ===")
a1 = True
b1 = False
print(f"True and False = {True and False}")  # False
print(f"True or False  = {True or False}")   # True
print(f"not True       = {not True}")        # False

# 布尔就是整数！（C# 做不到！）
print(f"\nTrue + True     = {True + True}")     # 2
print(f"False * 10      = {False * 10}")       # 0
print(f"True * 5 + False = {True * 5 + False}") # 5
print(f"sum([True, True, False, True]) = {sum([True, True, False, True])}")  # 3

# ==================== 字符串类型 ====================
print("\n=== 字符串类型 ===")
s1 = "Hello"
s2 = 'World'         # 单引号和双引号一样
s3 = s1 + " " + s2   # 拼接
s4 = f"{s1} {s2}"    # f-string（推荐，Python 3.6+）
print(f"拼接: {s3}")
print(f"f-string: {s4}")

# 字符串是不可变的序列
length = len(s1)           # 5（函数，不是属性！C# 用 .Length）
upper = s1.upper()         # "HELLO"
sub = s1[1:4]              # "ell"（切片语法）
print(f"长度: {len('Hello')}, 大写: {'hello'.upper()}, 切片: {'Hello'[1:4]}")

# ==================== 空值 None ====================
print("\n=== 空值 None ===")
s = None
x = None
print(f"s is None: {s is None}")   # True（推荐用 is 判断 None）
print(f"s is not None: {s is not None}")  # False
# C# 对比：None ≈ null，但 None 是单例对象
# 判断用 is 不用 ==，因为 == 可能被 __eq__ 重载
