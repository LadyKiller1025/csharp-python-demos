# ============================================================
# Python 正则表达式 re 模块完全指南
# 对应文章：4.8 正则表达式 —— 文本处理的瑞士军刀
# C# 对比：System.Text.RegularExpressions.Regex
# ============================================================
#
# 【核心对比】
#   Python re        →  内置模块，函数式 API (re.search, re.findall 等)
#   C# Regex         →  System.Text.RegularExpressions 命名空间
#                       Regex 类的静态方法 + 实例方法
#
# 语法基本一致（都用 PCRE 风格），但 API 风格不同：
#   Python: re.search(pattern, text)     → 函数调用
#   C#:     Regex.Match(text, pattern)   → 参数顺序相反！
#
# 标志位差异：
#   Python: re.IGNORECASE / re.DOTALL / re.MULTILINE
#   C#:     RegexOptions.IgnoreCase / RegexOptions.Singleline / RegexOptions.Multiline
# ============================================================

import re

print("=" * 60)
print("正则表达式：Python re vs C# Regex")
print("=" * 60)


# ============================================================
# 1. re.match —— 从字符串开头匹配
# ============================================================
# 【C# 等价】
#   // C# 没有直接的 match-at-start 方法
#   // 需要在模式前加 ^ 锚点
#   var match = Regex.Match(text, @"^pattern");
# ============================================================
print("\n===== 1. re.match 从开头匹配 =====")

text = "Hello 123 World 456"
m = re.match(r'\d+', text)       # 开头没有数字，匹配失败
print(f"match 数字: {m}")        # None

m = re.match(r'\D+', text)       # 开头是字母，匹配成功
print(f"match 字母: {m.group()}")  # Hello

# match vs search 的区别
m2 = re.search(r'\d+', text)     # search 从任意位置搜索
print(f"search 数字: {m2.group()}")  # 123

# 【C# 对比】
# C# Regex.Match() 从任意位置匹配（类似 Python re.search）
# C# 要实现 re.match 的效果，需要 ^ 锚点：
#   var m = Regex.Match(text, @"^\d+");


# ============================================================
# 2. re.search —— 从任意位置搜索第一个匹配
# ============================================================
# 【C# 等价】
#   var match = Regex.Match(text, pattern);
#   参数顺序不同！C# 是 text 在前，pattern 在后
# ============================================================
print("\n===== 2. re.search 搜索第一个匹配 =====")

text = "Hello, my email is alice@example.com, phone is 138-1234-5678"

# 搜索邮箱
# 【C# 等价】var m = Regex.Match(text, @"[\w.+-]+@[\w-]+\.[\w.]+");
email_pattern = r'[\w.+-]+@[\w-]+\.[\w.]+'
match = re.search(email_pattern, text)
if match:
    print(f"找到邮箱: {match.group()}")          # alice@example.com
    print(f"  起始位置: {match.start()}")         # 字符索引
    print(f"  结束位置: {match.end()}")            # 字符索引
    print(f"  匹配范围: {match.span()}")           # (start, end) 元组

# 搜索手机号
phone_pattern = r'1[3-9]\d-\d{4}-\d{4}'
phone = re.search(phone_pattern, text)
if phone:
    print(f"找到手机: {phone.group()}")           # 138-1234-5678
    print(f"  位置: {phone.span()}")

# 【C# vs Python 参数顺序差异 —— 最容易踩的坑！】
# Python: re.search(pattern, string)
# C#:     Regex.Match(string, pattern)
# C# 是 string 在前！新手从 Python 转 C# 经常搞反


# ============================================================
# 3. re.findall —— 查找所有匹配（返回列表）
# ============================================================
# 【C# 等价】
#   var matches = Regex.Matches(text, pattern);
#   // C# 返回 MatchCollection，需要遍历取 Value
# ============================================================
print("\n===== 3. re.findall 查找所有匹配 =====")

text = "联系邮箱: admin@test.com 或 support@example.org，备用: dev@company.net"

# 查找所有邮箱
# 【C# 等价】
#   var matches = Regex.Matches(text, pattern);
#   List<string> emails = matches.Cast<Match>().Select(m => m.Value).ToList();
emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+', text)
print(f"所有邮箱: {emails}")
print(f"共 {len(emails)} 个")

# findall 带分组时返回分组内容（不是整个匹配）
text2 = "2026-05-15 和 2026-06-01"
dates = re.findall(r'(\d{4})-(\d{2})-(\d{2})', text2)
print(f"带分组: {dates}")   # [('2026', '05', '15'), ('2026', '06', '01')]

# 【C# 对比】
# C# 没有直接的 findall
# C#: Regex.Matches(text, pattern) 返回 MatchCollection
# 然后 foreach (Match m in matches) 取 m.Value


# ============================================================
# 4. re.finditer —— 返回迭代器（含完整位置信息）
# ============================================================
# 【C# 等价】
#   MatchCollection matches = Regex.Matches(text, pattern);
#   foreach (Match m in matches) { ... }
# ============================================================
print("\n===== 4. re.finditer 返回迭代器 =====")

text3 = "价格: $12.50, 数量: 3, 折扣: $7.25"
for m in re.finditer(r'\$[\d.]+', text3):
    print(f"  金额 '{m.group()}' 在位置 {m.start()}-{m.end()}")

# 【C# vs Python】
# Python finditer: 返回惰性迭代器，内存友好
# C# Matches:     返回 MatchCollection，也是惰性求值
# 两者行为相似，C# 的 Matches 更像 Python 的 finditer


# ============================================================
# 5. re.sub —— 替换匹配内容
# ============================================================
# 【C# 等价】
#   string result = Regex.Replace(text, pattern, replacement);
# ============================================================
print("\n===== 5. re.sub 替换 =====")

text4 = "电话: 138-1234-5678, 备用: 139-8765-4321"

# 替换手机号中间四位为 ****
# 【C# 等价】string censored = Regex.Replace(text, @"(\d{3})-\d{4}-(\d{4})", "$1-****-$2");
censored = re.sub(r'(\d{3})-\d{4}-(\d{4})', r'\1-****-\2', text4)
print(f"脱敏: {censored}")

# 使用函数进行动态替换
# 【C# 等价】
#   string result = Regex.Replace(text, pattern, match => {
#       return match.Value.ToUpper();
#   });
def double_number(match):
    """将数字翻倍"""
    num = int(match.group())
    return str(num * 2)

text5 = "a=10, b=20, c=30"
doubled = re.sub(r'\d+', double_number, text5)
print(f"翻倍: {doubled}")  # a=20, b=40, c=60

# count 参数：限制替换次数
text6 = "aaa bbb aaa bbb aaa"
once = re.sub(r'aaa', 'XXX', text6, count=1)
print(f"只替换第一个: {once}")  # XXX bbb aaa bbb aaa

# 【C# 对比】
# C# Regex.Replace 也支持 MatchEvaluator 委托实现动态替换
# Python 的 re.sub 更简洁，直接传函数
# C#: new Regex(...).Replace(text, m => {...})


# ============================================================
# 6. re.split —— 按模式分割字符串
# ============================================================
# 【C# 等价】
#   string[] parts = Regex.Split(text, pattern);
# ============================================================
print("\n===== 6. re.split 分割 =====")

text7 = "apple,banana;cherry|date orange"

# 按多种分隔符分割
# 【C# 等价】string[] parts = Regex.Split(text7, "[,;|\\s]+");
parts = re.split(r'[,;|\s]+', text7)
print(f"分割结果: {parts}")
print(f"共 {len(parts)} 个")

# maxsplit 限制分割次数
parts_limited = re.split(r'[,;|\s]+', text7, maxsplit=2)
print(f"限制 2 次分割: {parts_limited}")


# ============================================================
# 7. 分组与捕获 —— groups() / group(n) / groupdict()
# ============================================================
# 【C# 等价】
#   match.Groups[0]  → 整个匹配（等价于 match.group()）
#   match.Groups[1]  → 第一个分组（等价于 match.group(1)）
#   match.Groups["name"] → 命名分组（等价于 match.group("name")）
# ============================================================
print("\n===== 7. 分组与捕获 =====")

# --- 7a. 命名分组 ---
# 【C# 等价】(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})
pattern = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
date_str = "今天是 2026-05-15，明天是 2026-05-16"

for m in re.finditer(pattern, date_str):
    # Python: match.group("year")
    # C#:     match.Groups["year"].Value
    print(f"日期: {m.group('year')}年{m.group('month')}月{m.group('day')}日")

# --- 7b. 命名分组字典 ---
first_match = re.search(pattern, date_str)
if first_match:
    # Python 独有！groupdict() 返回所有命名分组的字典
    # C# 没有直接对应，需要手动构建 Dictionary
    print(f"groupdict: {first_match.groupdict()}")

# --- 7c. 普通分组 ---
pattern2 = r'(\d{4})-(\d{2})-(\d{2})'
m = re.search(pattern2, date_str)
if m:
    print(f"groups():   {m.groups()}")         # ('2026', '05', '15')
    print(f"group(0):   {m.group(0)}")          # 2026-05-15 (整个匹配)
    print(f"group(1):   {m.group(1)}")          # 2026
    print(f"group(2,3): {m.group(2, 3)}")       # ('05', '15')

# --- 7d. 非捕获分组 ---
# 【C# 等价】(?:http|https)://([\w.]+)
pattern3 = r'(?:http|https)://([\w.]+)'
url_match = re.search(pattern3, "https://www.example.com")
if url_match:
    print(f"域名: {url_match.group(1)}")  # www.example.com
    print(f"完整匹配: {url_match.group(0)}")  # https://www.example.com
    # (?:...) 不参与分组编号，所以 groups() 只返回一个


# ============================================================
# 8. compile —— 预编译正则（性能优化）
# ============================================================
# 【C# 等价】
#   var regex = new Regex(pattern, RegexOptions.Compiled);
#   // C# 默认就会编译，RegexOptions.Compiled 额外 JIT 编译
# ============================================================
print("\n===== 8. compile 预编译 =====")

# 当同一模式多次使用时，compile 提升性能
# 【C# 等价】var emailRegex = new Regex(pattern, RegexOptions.Compiled);
email_re = re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+')

text8 = "联系: admin@test.com, support@test.com"
emails = email_re.findall(text8)
print(f"编译后查找: {emails}")

# 用编译后的对象做替换
text9 = "价格 $100 和 $200"
price_re = re.compile(r'\$(\d+)')
doubled = price_re.sub(lambda m: f"${int(m.group(1)) * 2}", text9)
print(f"编译后替换: {doubled}")

# 【C# vs Python】
# C#:  new Regex(pattern) 内部就会编译
#       RegexOptions.Compiled 进一步 JIT 编译，性能更好
# Python: re.compile() 是可选的，不编译也能用
# 建议：高频调用时用 compile / Compiled 提升性能


# ============================================================
# 9. 正则标志位 —— re.DOTALL / re.IGNORECASE 等
# ============================================================
# 【C# 等价】
#   RegexOptions.Singleline    → re.DOTALL (. 匹配换行)
#   RegexOptions.IgnoreCase    → re.IGNORECASE
#   RegexOptions.Multiline     → re.MULTILINE (^$ 匹配每行)
# ============================================================
print("\n===== 9. 正则标志位 =====")

# --- 9a. re.IGNORECASE (C# RegexOptions.IgnoreCase) ---
text10 = "Hello HELLO hello HeLLo"
# 【C# 等价】Regex.Matches(text, "hello", RegexOptions.IgnoreCase)
matches = re.findall(r'hello', text10, re.IGNORECASE)
print(f"忽略大小写: {matches}")

# --- 9b. re.DOTALL (C# RegexOptions.Singleline) ---
# . 默认不匹配换行符，加 DOTALL 后 . 可以匹配任何字符包括 \n
text11 = """<div>
内容跨多行
</div>"""
# 【C# 等价】Regex.Match(text, @"<div>.*?</div>", RegexOptions.Singleline)
m = re.search(r'<div>(.*?)</div>', text11, re.DOTALL)
if m:
    print(f"DOTALL 匹配: {m.group(1).strip()}")

# 不加 DOTALL 的情况
m2 = re.search(r'<div>(.*?)</div>', text11)  # 默认不匹配跨行
print(f"无 DOTALL: {m2}")  # None

# --- 9c. re.MULTILINE (C# RegexOptions.Multiline) ---
# 默认 ^$ 只匹配整个字符串的开头/结尾
# MULTILINE 使 ^$ 匹配每行的开头/结尾
text12 = "第一行\n第二行\n第三行"
# 【C# 等价】Regex.Matches(text, @"^第.*$", RegexOptions.Multiline)
lines = re.findall(r'^第.*$', text12, re.MULTILINE)
print(f"MULTILINE 逐行: {lines}")

# --- 9d. 组合多个标志 ---
# 【C# 等价】RegexOptions.IgnoreCase | RegexOptions.Singleline
m = re.search(r'<div>(.*?)</div>', '<DIV>跨\n行</DIV>',
              re.IGNORECASE | re.DOTALL)
if m:
    print(f"组合标志: {m.group(1)}")

# 【C# 对比】
# C# 用位或运算符组合标志: RegexOptions.IgnoreCase | RegexOptions.Singleline
# Python 用 | 运算符: re.IGNORECASE | re.DOTALL
# 语法几乎一样！


# ============================================================
# 10. 前瞻 / 后顾 —— lookahead / lookbehind
# ============================================================
# 【C# 等价】
#   (?=...)  正向前瞻  →  (?=...)  完全一样
#   (?!...)  负向前瞻  →  (?!...)  完全一样
#   (?<=...) 正向后顾  →  (?<=...) 完全一样
#   (?<!...) 负向后顾  →  (?<!...) 完全一样
# ============================================================
print("\n===== 10. 前瞻与后顾 =====")

text13 = "价格: $100, 数量: 5件, 折扣: $20"

# --- 10a. 正向前瞻 (?=...) ---
# 匹配后面跟着"元"的数字
# 【C# 等价】Regex.Match(text, @"\d+(?=元)")
m = re.search(r'\d+(?=元)', "100元 200元 300美元")
if m:
    print(f"正向前瞻: {m.group()}")   # 100

# --- 10b. 负向前瞻 (?!...) ---
# 匹配后面不是"美元"的价格数字
# 【C# 等价】Regex.Matches(text, @"\d+(?!美元)")
m = re.findall(r'\$?\d+(?!美元)', "价格$100, 折扣$50, 跨度300美元")
print(f"负向前瞻: {m}")

# --- 10c. 正向后顾 (?<=...) ---
# 匹配 $ 后面的数字
# 【C# 等价】Regex.Matches(text, @"(?<=\$)\d+")
prices = re.findall(r'(?<=\$)\d+', text13)
print(f"正向后顾: {prices}")  # ['100', '20']

# --- 10d. 负向后顾 (?<!...) ---
# 匹配前面不是 $ 的数字
numbers = re.findall(r'(?<!\$)\b\d+\b', text13)
print(f"负向后顾: {numbers}")  # ['5']

# --- 10e. 前瞻 + 后顾组合 ---
# 提取被引号包围的单词
text14 = '他说 "hello" 然后说 world'
quoted = re.findall(r'(?<=")\w+(?=")', text14)
print(f"引号中的词: {quoted}")  # ['hello']

# 【C# vs Python 对比】
# 语法完全一样：(?=...) (?!) (?<=...) (?<!...)
# 唯一区别：Python re.LOOKAROUND 默认启用
# C# 需要 .NET 2.0+，现代版本都支持
# 两者在前瞻后顾上几乎没有差异


# ============================================================
# 11. 实际场景：日志解析
# ============================================================
print("\n===== 11. 实际场景：日志解析 =====")

log_line = '2026-05-15 10:30:45 [ERROR] Connection timeout - server=192.168.1.100:8080'

# 解析日志各字段
# 【C# 等价】
# var logPattern = new Regex(@"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.+)");
log_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.+)')
m = log_pattern.match(log_line)
if m:
    timestamp, level, message = m.groups()
    print(f"  时间: {timestamp}")
    print(f"  级别: {level}")
    print(f"  消息: {message}")

# 提取 IP 地址（用 findall）
# 【C# 等价】var ips = Regex.Matches(text, @"\d+\.\d+\.\d+\.\d+");
ips = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', log_line)
print(f"  IP 地址: {ips}")


# ============================================================
# 总结对比表
# ============================================================
print("\n" + "=" * 60)
print("总结：Python re vs C# Regex")
print("=" * 60)
comparison = """
┌────────────────────────┬──────────────────────────┬───────────────────────────────┐
│      操作              │    Python re             │    C# Regex                   │
├────────────────────────┼──────────────────────────┼───────────────────────────────┤
│ 参数顺序               │ re.search(pattern, text) │ Regex.Match(text, pattern)    │
│ 从开头匹配             │ re.match(pat, text)      │ Regex.Match(text, @"^"+pat)   │
│ 搜索第一个             │ re.search(pat, text)     │ Regex.Match(text, pat)        │
│ 查找所有               │ re.findall(pat, text)    │ Regex.Matches(text, pat)      │
│ 迭代匹配               │ re.finditer(pat, text)   │ Regex.Matches(text, pat)      │
│ 替换                   │ re.sub(pat, rep, text)   │ Regex.Replace(text, pat, rep) │
│ 分割                   │ re.split(pat, text)      │ Regex.Split(text, pat)        │
│ 预编译                 │ re.compile(pat)          │ new Regex(pat, Compiled)      │
│ 忽略大小写             │ re.IGNORECASE            │ RegexOptions.IgnoreCase       │
│ .匹配换行              │ re.DOTALL                │ RegexOptions.Singleline       │
│ 每行匹配^$             │ re.MULTILINE             │ RegexOptions.Multiline        │
│ 命名分组               │ (?P<name>...)            │ (?<name>...)                  │
│ 正向前瞻               │ (?=...)                  │ (?=...)                       │
│ 正向后顾               │ (?<=...)                 │ (?<=...)                      │
│ 匹配结果               │ match.group()            │ match.Value                   │
│ 分组取值               │ match.group(1)           │ match.Groups[1].Value         │
│ 命名分组取值           │ match.group("name")      │ match.Groups["name"].Value    │
│ 所有分组               │ match.groups()           │ match.Groups (遍历)           │
│ 分组字典               │ match.groupdict()        │ 需手动构建 Dictionary         │
└────────────────────────┴──────────────────────────┴───────────────────────────────┘

注意：Python 和 C# 的正则语法（PCRE 风格）几乎完全一致！
主要差异在于 API 调用方式和参数顺序。
"""
print(comparison)
print("完成!")
