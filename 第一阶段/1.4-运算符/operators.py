# Python 运算符示例
# 对应文章：1.4 运算符与表达式

a, b = 10, 3

# ==================== 算术运算符 ====================
print("=== 算术运算符 ===")
print(f"a + b  = {a + b}")      # 13
print(f"a - b  = {a - b}")      # 7
print(f"a * b  = {a * b}")      # 30
print(f"a / b  = {a / b}")      # 3.333...（Python 的 / 始终返回浮点数！）
print(f"a // b = {a // b}")     # 3（整除，向下取整）
print(f"a % b  = {a % b}")     # 1（取余）
print(f"2 ** 10 = {2 ** 10}")   # 1024（幂运算，内置运算符！C# 需要 Math.Pow()）

# 注意：Python 的 / 即使能整除也返回浮点数
print(f"10 / 2 = {10 / 2}")    # 5.0（不是 5！）

# ==================== 链式比较（Python 独有） ====================
print("\n=== 链式比较 ===")
x = 5
# Python 可以这样写，C# 不行！
print(f"0 < x < 10  => {0 < x < 10}")      # True
print(f"1 < x < 3   => {1 < x < 3}")       # False
print(f"1 <= x <= 5  => {1 <= x <= 5}")     # True
# 等价于 C# 的：x > 0 && x < 10

# ==================== 逻辑运算符 ====================
print("\n=== 逻辑运算符 ===")
a1, b1 = True, False
print(f"True and False  = {a1 and b1}")   # False
print(f"True or False   = {a1 or b1}")    # True
print(f"not True        = {not a1}")      # False

# Python 的 and/or 返回"实际值"，不一定是布尔值！
print("\n=== and/or 返回实际值（重要！） ===")
print(f"None or 'default'  = {None or 'default'}")  # "default"
print(f"0 or 42            = {0 or 42}")             # 42
print(f"'hello' or 'world' = {'hello' or 'world'}")  # "hello"
print(f"'' or 'fallback'   = {'' or 'fallback'}")    # "fallback"
# 规律：and 返回第一个为 False 的值，or 返回第一个为 True 的值

# ==================== 赋值运算符 ====================
print("\n=== 赋值运算符 ===")
x = 10
x += 3   # x = x + 3  => 13
print(f"x += 3  => {x}")
x -= 2   # x = x - 2  => 11
print(f"x -= 2  => {x}")
x *= 2   # x = x * 2  => 22
print(f"x *= 2  => {x}")
x //= 3  # x = x // 3 => 7（Python 独有的整除赋值）
print(f"x //= 3 => {x}")
x **= 2  # x = x ** 2 => 49（Python 独有的幂赋值）
print(f"x **= 2 => {x}")

# ==================== 三元表达式 ====================
print("\n=== 三元表达式 ===")
value = 5
result = "正数" if value > 0 else "非正数"
print(f"{value} 是 {result}")

# ==================== 身份运算符 vs 相等运算符 ====================
print("\n=== 身份运算符 is vs == ===")
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(f"a == b  => {a == b}")   # True（值相等）
print(f"a is b  => {a is b}")   # False（不是同一个对象！）
print(f"a is c  => {a is c}")   # True（c 指向同一个对象）
print(f"a is not b => {a is not b}")  # True

# is 通常用于判断 None
x = None
print(f"x is None => {x is None}")  # True（推荐用 is 判断 None）

# ==================== 海象运算符（3.8+） ====================
print("\n=== 海象运算符 := ===")
# 在表达式内部赋值，避免重复计算
if (n := len([1, 2, 3])) > 2:
    print(f"列表长度 {n} > 2")

# 在 while 循环中使用
data = [1, 2, 3, 4, 5]
idx = 0
while (val := data[idx]) < 4:
    print(f"  读取到 {val}")
    idx += 1
