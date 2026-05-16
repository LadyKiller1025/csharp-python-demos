# Python 条件判断示例
# 对应文章：1.6 条件判断

x = 5

# ==================== 基本 if-elif-else ====================
print("=== 基本条件判断 ===")
if x > 0:
    print("正数")
elif x < 0:
    print("负数")
else:
    print("零")

# 注意：Python 用 elif 而不是 else if！
# 不需要括号包围条件，但需要冒号和缩进

# ==================== 三元表达式 ====================
print("\n=== 三元表达式 ===")
result = "正数" if x > 0 else "非正数"
print(f"{x} 是 {result}")

# ==================== 真值判断（Python 独有） ====================
print("\n=== 真值判断 ===")
s = "hello"
n = 0
lst = [1, 2, 3]
empty_list = []
none_val = None

# Python 的 if 可以接受任何对象，不只是布尔值
if s:        # 非空字符串为 True
    print(f"s='{s}' 不为空")
if not n:    # 0 为 False
    print(f"n={n} 为零（falsy）")
if lst:      # 非空列表为 True
    print(f"lst={lst} 不为空")
if not empty_list:  # 空列表为 False
    print("空列表是 falsy")

# Python 的真值表
# False: None, False, 0, 0.0, 0j, "", [], {}, set(), frozenset(), tuple()
# True: 其他所有值
print(f"\nbool(None)     = {bool(None)}")      # False
print(f"bool(0)        = {bool(0)}")           # False
print(f"bool('')       = {bool('')}")          # False
print(f"bool([])       = {bool([])}")          # False
print(f"bool('hello')  = {bool('hello')}")     # True
print(f"bool([1,2,3])  = {bool([1,2,3])}")     # True
print(f"bool(42)       = {bool(42)}")          # True

# ==================== and/or 短路求值 ====================
print("\n=== and/or 短路求值 ===")
# and/or 返回实际值，不一定是布尔值！
print(f"None or 'default'  = {None or 'default'}")  # "default"（短路：None 为 falsy，返回右边）
print(f"'hello' or 'world' = {'hello' or 'world'}")  # "hello"（短路：'hello' 为 truthy，直接返回）
print(f"0 or 42            = {0 or 42}")             # 42
print(f"'' or 'fallback'   = {'' or 'fallback'}")    # "fallback"

# 实际用途：设置默认值
name = ""
display_name = name or "匿名用户"
print(f"显示名称: {display_name}")

# ==================== any() 和 all() ====================
print("\n=== any() 和 all() ===")
numbers = [2, 4, 6, 8, 10]
odd_numbers = [1, 3, 5, 7, 9]
mixed = [1, 2, 3, 4, 5]

print(f"all(全是偶数): {all(n % 2 == 0 for n in numbers)}")    # True
print(f"all(全是偶数): {all(n % 2 == 0 for n in odd_numbers)}") # False
print(f"any(有偶数):   {any(n % 2 == 0 for n in mixed)}")       # True
print(f"any(全是偶数): {any(n % 2 == 0 for n in odd_numbers)}") # False

# ==================== match-case（Python 3.10+） ====================
print("\n=== match-case 模式匹配（Python 3.10+） ===")
# 类似 C# 的 switch 表达式
status = 404
match status:
    case 200:
        print("OK")
    case 404:
        print("Not Found")
    case 500:
        print("Server Error")
    case _:
        print(f"未知状态码: {status}")

# 带守卫条件的模式匹配
age = 25
match age:
    case n if n < 0:
        print("无效年龄")
    case n if n < 18:
        print("未成年")
    case n if n < 65:
        print("成年人")
    case _:
        print("老年人")

# 序列模式
point = (1, 0)
match point:
    case (0, 0):
        print("原点")
    case (x, 0):
        print(f"X 轴上，x={x}")
    case (0, y):
        print(f"Y 轴上，y={y}")
    case (x, y):
        print(f"坐标 ({x}, {y})")

# 映射模式（Python 独有！匹配字典）
config = {"debug": True, "version": "3.0"}
match config:
    case {"debug": True, "version": ver}:
        print(f"调试模式，版本: {ver}")
    case {"debug": False}:
        print("生产模式")
