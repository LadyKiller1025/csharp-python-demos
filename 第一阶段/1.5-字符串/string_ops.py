# Python 字符串操作示例
# 对应文章：1.5 字符串操作

# ==================== 字符串创建 ====================
s1 = "Hello"
s2 = "World"
s3 = r"C:\path\to\file"          # 原始字符串（不转义）
s4 = f"Hello {s1}"               # f-string（推荐，Python 3.6+）
s5 = """多行
字符串"""                          # 三引号多行字符串

# ==================== 字符串拼接与插值 ====================
result = s1 + " " + s2           # 拼接
interpolated = f"{s1} {s2}"      # f-string 插值（推荐）

# ==================== f-string 格式化（重点！） ====================
print("=== f-string 格式化 ===")
price = 12.345
name = "Alice"
balance = 1234567.89

# 基础格式化
print(f"Price: {price:.2f}")         # "Price: 12.35"（保留2位小数）
print(f"Name: {name:>10}")           # "Name:      Alice"（右对齐，宽度10）
print(f"Name: {name:<10}")           # "Name: Alice     "（左对齐）
print(f"Name: {name:^10}")           # "Name:   Alice   "（居中）
print(f"Name: {name:*^10}")          # "Name: ***Alice**"（居中填充*）
print(f"Balance: {balance:,.2f}")    # "Balance: 1,234,567.89"（千分位）
print(f"Hex: {255:#x}")             # "Hex: 0xff"（十六进制带前缀）
print(f"Percent: {0.756:.1%}")       # "Percent: 75.6%"（百分比）
print(f"Debug: {price=}")            # "Debug: price=12.345"（调试语法3.8+）

# 填充与对齐
print(f"{'left':<15}")              # "left           "
print(f"{'right':>15}")             # "          right"
print(f"{'center':^15}")            # "     center     "
print(f"{42:05d}")                  # "00042"（零填充）

# ==================== 字符串访问与切片 ====================
print("\n=== 字符串切片 ===")
s = "Hello, World!"

# 单个字符访问
first = s[0]        # 'H'
last = s[-1]        # '!'（负数索引！）

# 切片（Python 的杀手锏！）
sub1 = s[0:5]       # "Hello"
sub2 = s[7:]        # "World!"
sub3 = s[:5]        # "Hello"
sub4 = s[::2]       # "Hlo ol!"（每隔一个字符）
sub5 = s[::-1]      # "!dlroW ,olleH"（反转！C# 需要 ToCharArray() + Array.Reverse()）

print(f"原字符串:  {s}")
print(f"s[0:5]:    {sub1}")
print(f"s[7:]:     {sub2}")
print(f"s[::-1]:   {sub5}")

# ==================== 常用字符串方法 ====================
print("\n=== 常用方法 ===")
index = s.find("World")            # 7（找不到返回 -1）
contains = "Hello" in s            # True（用 in 运算符，不是方法！）
starts = s.startswith("Hello")     # True
ends = s.endswith("World!")        # True

replaced = s.replace("World", "Python")  # "Hello, Python!"
parts = s.split(',')              # ["Hello", " World!"]
joined = "-".join(["a", "b", "c"])  # "a-b-c"

print(f"find('World'):  {index}")
print(f"'Hello' in s:   {contains}")
print(f"replace:        {replaced}")
print(f"split:          {parts}")
print(f"join:           {joined}")

# 大小写与去空格
print(f"upper:  {'hello'.upper()}")       # HELLO
print(f"lower:  {'HELLO'.lower()}")       # hello
print(f"title:  {'hello world'.title()}") # Hello World
print(f"strip:  {'  hello  '.strip()}")   # hello（去两端空格）
print(f"lstrip: {'  hello  '.lstrip()}")  # hello  （去左空格）
print(f"rstrip: {'  hello  '.rstrip()}")  #   hello（去右空格）

# ==================== 字符串不可变性 ====================
print("\n=== 字符串不可变性 ===")
# 字符串创建后不能修改！
s = "Hello"
# s[0] = "h"  # TypeError! 字符串不支持单个字符赋值

# 需要"修改"时，创建新字符串
new_s = "h" + s[1:]    # "hello"
print(f"修改后: {new_s}")

# 大量拼接用 list + join（高效）
parts_list = []
for i in range(5):
    parts_list.append(str(i))
result = ",".join(parts_list)
print(f"join结果: {result}")  # "0,1,2,3,4"

# ==================== 字符串比较 ====================
print("\n=== 字符串比较 ===")
print(f"'abc' < 'abd':  {'abc' < 'abd'}")    # True（按字典序）
print(f"'abc' == 'abc': {'abc' == 'abc'}")   # True
print(f"'abc' != 'ABC': {'abc' != 'ABC'}")   # True（区分大小写）
