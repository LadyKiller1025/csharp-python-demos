// ============================================================
// C# 正则表达式完全指南（对标 Python re 模块）
// 对应文章：4.8 正则表达式 —— 文本处理的瑞士军刀
// Python 对比：re 模块
// ============================================================
//
// 【核心对比】
//   Python re        →  内置模块，函数式 API (re.search, re.findall)
//   C# Regex         →  System.Text.RegularExpressions 命名空间
//                       参数顺序与 Python 相反！
//
// 最重要的差异：参数顺序
//   Python: re.search(pattern, text)   → 模式在前
//   C#:     Regex.Match(text, pattern) → 文本在前（完全反过来！）
// ============================================================

using System;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using System.Linq;

public class RegexDemo
{
    static void Main()
    {
        Console.WriteLine("============================================");
        Console.WriteLine("C# 正则表达式 vs Python re 模块");
        Console.WriteLine("============================================");

        // ============================================================
        // 1. 从开头匹配 —— Python re.match 的效果
        // ============================================================
        // 【Python 等价】
        //   m = re.match(r'\D+', text)   从开头匹配字母
        //   m = re.match(r'\d+', text)   从开头匹配数字（失败）
        // ============================================================
        Console.WriteLine("\n===== 1. 从开头匹配 =====");

        string text = "Hello 123 World 456";

        // C# Regex.Match 从任意位置匹配（类似 Python re.search）
        // 要实现 Python re.match 效果，需要 ^ 锚点
        var m = Regex.Match(text, @"^\d+");  // 开头没有数字
        Console.WriteLine($"match 数字: {m.Success ? m.Value : "无匹配"}");

        m = Regex.Match(text, @"^\D+");      // 开头是字母
        Console.WriteLine($"match 字母: {m.Value}");  // Hello

        var m2 = Regex.Match(text, @"\d+");  // 搜索数字（任意位置）
        Console.WriteLine($"search 数字: {m2.Value}");  // 123

        // 【C# vs Python】
        // C# 没有 re.match 等价方法
        // 要实现从头匹配，加 ^ 锚点
        // 这是 C# 新手从 Python 转来时最容易困惑的地方


        // ============================================================
        // 2. 搜索第一个匹配 —— Regex.Match
        // ============================================================
        // 【Python 等价】
        //   match = re.search(pattern, text)
        // ============================================================
        Console.WriteLine("\n===== 2. 搜索第一个匹配 =====");

        string text2 = "Hello, my email is alice@example.com, phone is 138-1234-5678";

        // 【Python 等价】match = re.search(r'[\w.+-]+@[\w-]+\.[\w.]+', text2)
        var emailMatch = Regex.Match(text2, @"[\w.+-]+@[\w-]+\.[\w.]+");
        if (emailMatch.Success)
        {
            Console.WriteLine($"找到邮箱: {emailMatch.Value}");           // alice@example.com
            Console.WriteLine($"  起始位置: {emailMatch.Index}");         // int 索引
            Console.WriteLine($"  匹配长度: {emailMatch.Length}");         // int 长度
        }

        // 搜索手机号
        var phoneMatch = Regex.Match(text2, @"1[3-9]\d-\d{4}-\d{4}");
        if (phoneMatch.Success)
            Console.WriteLine($"找到手机: {phoneMatch.Value}");  // 138-1234-5678


        // ============================================================
        // 3. 查找所有匹配 —— Regex.Matches
        // ============================================================
        // 【Python 等价】
        //   emails = re.findall(r'pattern', text)
        // ============================================================
        Console.WriteLine("\n===== 3. 查找所有匹配 =====");

        string text3 = "联系邮箱: admin@test.com 或 support@example.org，备用: dev@company.net";

        // 【Python 等价】emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+', text3)
        var emails = Regex.Matches(text3, @"[\w.+-]+@[\w-]+\.[\w.]+");
        Console.Write("所有邮箱: ");
        foreach (Match m3 in emails) Console.Write($"{m3.Value} ");
        Console.WriteLine($"\n共 {emails.Count} 个");

        // 【C# vs Python findall】
        // Python findall 直接返回字符串列表: ["a@test.com", "b@test.com"]
        // C# 返回 MatchCollection，需要遍历取 .Value
        // C# 要达到 findall 效果：matches.Cast<Match>().Select(m => m.Value).ToList()


        // ============================================================
        // 4. 替换 —— Regex.Replace
        // ============================================================
        // 【Python 等价】
        //   re.sub(pattern, replacement, text)
        // ============================================================
        Console.WriteLine("\n===== 4. 替换 =====");

        string text4 = "电话: 138-1234-5678, 备用: 139-8765-4321";

        // 简单替换
        // 【Python 等价】censored = re.sub(r'(\d{3})-\d{4}-(\d{4})', r'\1-****-\2', text4)
        string censored = Regex.Replace(text4, @"(\d{3})-\d{4}-(\d{4})", "$1-****-$2");
        Console.WriteLine($"脱敏: {censored}");

        // 动态替换（使用 MatchEvaluator 委托）
        // 【Python 等价】re.sub(r'\d+', lambda m: str(int(m.group()) * 2), text5)
        string text5 = "a=10, b=20, c=30";
        string doubled = Regex.Replace(text5, @"\d+", m => (int.Parse(m.Value) * 2).ToString());
        Console.WriteLine($"翻倍: {doubled}");

        // 限制替换次数
        // 【Python 等价】re.sub(r'aaa', 'XXX', text6, count=1)
        string text6 = "aaa bbb aaa bbb aaa";
        string once = Regex.Replace(text6, @"aaa", "XXX", 1);  // 第3个参数是 count
        Console.WriteLine($"只替换第一个: {once}");


        // ============================================================
        // 5. 分割 —— Regex.Split
        // ============================================================
        // 【Python 等价】
        //   parts = re.split(r'[,;|\s]+', text)
        // ============================================================
        Console.WriteLine("\n===== 5. 分割 =====");

        string text7 = "apple,banana;cherry|date orange";

        // 【Python 等价】parts = re.split(r'[,;|\s]+', text7)
        string[] parts = Regex.Split(text7, @"[,;|\s]+");
        Console.WriteLine($"分割结果: [{string.Join(", ", parts)}]");
        Console.WriteLine($"共 {parts.Length} 个");

        // 限制分割次数
        // 【Python 等价】re.split(pattern, text, maxsplit=2)
        string[] partsLimited = Regex.Split(text7, @"[,;|\s]+", 3);  // C# limit 参数在前
        Console.WriteLine($"限制 3 次分割: [{string.Join(", ", partsLimited)}]");


        // ============================================================
        // 6. 分组与捕获
        // ============================================================
        // 【Python 等价】
        //   match.groups()    → 所有分组
        //   match.group(1)    → 第一个分组
        //   match.group("name") → 命名分组
        // ============================================================
        Console.WriteLine("\n===== 6. 分组与捕获 =====");

        // --- 6a. 命名分组 ---
        // 【Python 等价】(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})
        string dateStr = "今天是 2026-05-15，明天是 2026-05-16";

        // 注意：C# 用 (?<name>...)，Python 用 (?P<name>...)
        var datePattern = new Regex(@"(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})");
        foreach (Match m4 in datePattern.Matches(dateStr))
        {
            // 【Python 等价】m.group("year")
            Console.WriteLine($"日期: {m4.Groups["year"].Value}年{m4.Groups["month"].Value}月{m4.Groups["day"].Value}日");
        }

        // --- 6b. 普通分组 ---
        // 【Python 等价】m.groups(), m.group(1), m.group(2)
        var dateMatch = datePattern.Match(dateStr);
        if (dateMatch.Success)
        {
            Console.WriteLine($"group(0): {dateMatch.Groups[0].Value}");  // 整个匹配
            Console.WriteLine($"group(1): {dateMatch.Groups[1].Value}");  // 2026
            Console.WriteLine($"group(2): {dateMatch.Groups[2].Value}");  // 05
            Console.WriteLine($"group(3): {dateMatch.Groups[3].Value}");  // 15

            // 【C# 独有】Groups.Count 查看分组数量
            Console.WriteLine($"分组数量: {dateMatch.Groups.Count}");
        }

        // --- 6c. 非捕获分组 ---
        // 【Python 等价】(?:http|https)://([\w.]+)
        // 语法完全一样！
        var urlMatch = Regex.Match("https://www.example.com", @"(?:http|https)://([\w.]+)");
        if (urlMatch.Success)
        {
            Console.WriteLine($"域名: {urlMatch.Groups[1].Value}");       // www.example.com
            Console.WriteLine($"完整匹配: {urlMatch.Groups[0].Value}");   // https://www.example.com
        }


        // ============================================================
        // 7. 编译正则 —— 性能优化
        // ============================================================
        // 【Python 等价】
        //   email_re = re.compile(r'pattern')
        //   email_re.findall(text)
        // ============================================================
        Console.WriteLine("\n===== 7. 编译正则 =====");

        // C# 默认就会编译正则，RegexOptions.Compiled 进一步 JIT 编译
        // 【Python 等价】email_re = re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+')
        var emailRegex = new Regex(@"[\w.+-]+@[\w-]+\.[\w.]+", RegexOptions.Compiled);
        var compiledEmails = emailRegex.Matches("contact: admin@test.com, support@test.com");
        Console.Write("编译后查找: ");
        foreach (Match m5 in compiledEmails) Console.Write($"{m5.Value} ");
        Console.WriteLine();

        // 动态替换
        string text8 = "价格 $100 和 $200";
        var priceRegex = new Regex(@"\$(\d+)", RegexOptions.Compiled);
        string result = priceRegex.Replace(text8, m => $"${int.Parse(m.Groups[1].Value) * 2}");
        Console.WriteLine($"编译后替换: {result}");

        // 【C# vs Python】
        // C#:  new Regex() 已经会编译，Compiled 额外 JIT 编译
        // Python: re.compile() 是可选优化
        // 建议：高频调用时都用编译版本


        // ============================================================
        // 8. 正则标志位 —— RegexOptions 枚举
        // ============================================================
        // 【Python 等价】
        //   re.IGNORECASE → RegexOptions.IgnoreCase
        //   re.DOTALL     → RegexOptions.Singleline
        //   re.MULTILINE  → RegexOptions.Multiline
        // ============================================================
        Console.WriteLine("\n===== 8. 正则标志位 =====");

        // --- 8a. IgnoreCase (Python re.IGNORECASE) ---
        string text9 = "Hello HELLO hello HeLLo";
        // 【Python 等价】re.findall(r'hello', text9, re.IGNORECASE)
        var ignoreCaseMatches = Regex.Matches(text9, "hello", RegexOptions.IgnoreCase);
        Console.Write("忽略大小写: ");
        foreach (Match m6 in ignoreCaseMatches) Console.Write($"{m6.Value} ");
        Console.WriteLine();

        // --- 8b. Singleline (Python re.DOTALL) ---
        // . 默认不匹配换行符，Singleline 使 . 可以匹配 \n
        string text10 = "<div>\n内容跨多行\n</div>";
        // 【Python 等价】re.search(r'<div>(.*?)</div>', text10, re.DOTALL)
        var dotallMatch = Regex.Match(text10, @"<div>(.*?)</div>", RegexOptions.Singleline);
        if (dotallMatch.Success)
            Console.WriteLine($"Singleline: {dotallMatch.Groups[1].Value.Trim()}");

        // --- 8c. Multiline (Python re.MULTILINE) ---
        // 默认 ^$ 只匹配整个字符串首尾，Multiline 使 ^$ 匹配每行
        string text11 = "第一行\n第二行\n第三行";
        // 【Python 等价】re.findall(r'^第.*$', text11, re.MULTILINE)
        var multilineMatches = Regex.Matches(text11, @"^第.*$", RegexOptions.Multiline);
        Console.Write("Multiline 逐行: ");
        foreach (Match m7 in multilineMatches) Console.Write($"'{m7.Value}' ");
        Console.WriteLine();

        // --- 8d. 组合多个标志 ---
        // 【Python 等价】re.IGNORECASE | re.DOTALL
        var combinedMatch = Regex.Match("<DIV>跨\n行</DIV>", @"<div>(.*?)</div>",
            RegexOptions.IgnoreCase | RegexOptions.Singleline);
        if (combinedMatch.Success)
            Console.WriteLine($"组合标志: {combinedMatch.Groups[1].Value}");

        // 【C# vs Python 标志位命名差异】
        // Python re.DOTALL     → C# RegexOptions.Singleline
        // Python re.MULTILINE  → C# RegexOptions.Multiline
        // Python re.IGNORECASE → C# RegexOptions.IgnoreCase
        // 注意：DOTALL 和 Singleline 名字不同但功能相同！


        // ============================================================
        // 9. 前瞻与后顾 —— lookahead / lookbehind
        // ============================================================
        // Python 和 C# 语法完全一样：
        //   (?=...)  正向前瞻
        //   (?!...)  负向前瞻
        //   (?<=...) 正向后顾
        //   (?<!...) 负向后顾
        // ============================================================
        Console.WriteLine("\n===== 9. 前瞻与后顾 =====");

        // --- 9a. 正向前瞻 (?=...) ---
        // 匹配后面跟 "元" 的数字
        // 【Python 等价】re.search(r'\d+(?=元)', "100元 200元 300美元")
        var lookaheadMatch = Regex.Match("100元 200元 300美元", @"\d+(?=元)");
        if (lookaheadMatch.Success)
            Console.WriteLine($"正向前瞻: {lookaheadMatch.Value}");  // 100

        // --- 9b. 负向前瞻 (?!...) ---
        // 匹配后面不是 "美元" 的数字
        // 【Python 等价】re.findall(r'\d+(?!美元)', text)
        var negativeLookahead = Regex.Matches("100 200 300美元", @"\d+(?!美元)");
        Console.Write("负向前瞻: ");
        foreach (Match m8 in negativeLookahead) Console.Write($"{m8.Value} ");
        Console.WriteLine();

        // --- 9c. 正向后顾 (?<=...) ---
        // 匹配 $ 后面的数字
        // 【Python 等价】re.findall(r'(?<=\$)\d+', text)
        string text12 = "价格: $100, 数量: 5件, 折扣: $20";
        var lookbehindMatches = Regex.Matches(text12, @"(?<=\$)\d+");
        Console.Write("正向后顾: ");
        foreach (Match m9 in lookbehindMatches) Console.Write($"{m9.Value} ");
        Console.WriteLine();

        // --- 9d. 负向后顾 (?<!...) ---
        // 匹配前面不是 $ 的数字
        // 【Python 等价】re.findall(r'(?<!\$)\b\d+\b', text)
        var negativeLookbehind = Regex.Matches(text12, @"(?<!\$)\b\d+\b");
        Console.Write("负向后顾: ");
        foreach (Match m10 in negativeLookbehind) Console.Write($"{m10.Value} ");
        Console.WriteLine();

        // --- 9e. 前瞻 + 后顾组合 ---
        // 提取被引号包围的单词
        // 【Python 等价】re.findall(r'(?<=")\w+(?=")', text)
        string text13 = "他说 \"hello\" 然后说 world";
        var quotedWords = Regex.Matches(text13, @"(?<="")\w+(?="")");
        Console.Write("引号中的词: ");
        foreach (Match m11 in quotedWords) Console.Write($"{m11.Value} ");
        Console.WriteLine();

        // 【C# vs Python 前瞻后顾】
        // 语法完全一样！这是正则表达式标准化的好处
        // 两者在前瞻后顾上几乎没有差异


        // ============================================================
        // 10. 实际场景：日志解析
        // ============================================================
        Console.WriteLine("\n===== 10. 实际场景：日志解析 =====");

        string logLine = "2026-05-15 10:30:45 [ERROR] Connection timeout - server=192.168.1.100:8080";

        // 【Python 等价】
        //   log_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.+)')
        //   m = log_pattern.match(log_line)
        var logPattern = new Regex(@"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.+)");
        var logMatch = logPattern.Match(logLine);
        if (logMatch.Success)
        {
            Console.WriteLine($"  时间: {logMatch.Groups[1].Value}");
            Console.WriteLine($"  级别: {logMatch.Groups[2].Value}");
            Console.WriteLine($"  消息: {logMatch.Groups[3].Value}");
        }

        // 提取 IP 地址
        // 【Python 等价】re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', logLine)
        var ipMatches = Regex.Matches(logLine, @"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b");
        Console.Write("  IP 地址: ");
        foreach (Match m12 in ipMatches) Console.Write($"{m12.Value} ");
        Console.WriteLine();


        // ============================================================
        // 总结对比表
        // ============================================================
        Console.WriteLine("\n============================================");
        Console.WriteLine("总结：C# Regex vs Python re");
        Console.WriteLine("============================================");
        Console.WriteLine(@"
┌────────────────────────┬──────────────────────────┬───────────────────────────────┐
│      操作              │    C# Regex              │    Python re                  │
├────────────────────────┼──────────────────────────┼───────────────────────────────┤
│ 参数顺序               │ Regex.Match(text, pat)   │ re.search(pat, text) 反的！   │
│ 从开头匹配             │ Regex.Match(t, @"^"+pat) │ re.match(pat, text)           │
│ 搜索第一个             │ Regex.Match(text, pat)   │ re.search(pat, text)          │
│ 查找所有               │ Regex.Matches(text, pat) │ re.findall(pat, text)         │
│ 替换                   │ Regex.Replace(t, pat,r)  │ re.sub(pat, rep, t)           │
│ 分割                   │ Regex.Split(text, pat)   │ re.split(pat, text)           │
│ 预编译                 │ new Regex(pat, Compiled)  │ re.compile(pat)               │
│ 忽略大小写             │ RegexOptions.IgnoreCase  │ re.IGNORECASE                 │
│ .匹配换行              │ RegexOptions.Singleline  │ re.DOTALL                     │
│ 每行匹配^$             │ RegexOptions.Multiline   │ re.MULTILINE                  │
│ 命名分组               │ (?<name>...)             │ (?P<name>...)                 │
│ 匹配结果               │ match.Value              │ match.group()                 │
│ 分组取值               │ match.Groups[1].Value    │ match.group(1)                │
│ 命名分组               │ match.Groups["name"]     │ match.group("name")           │
└────────────────────────┴──────────────────────────┴───────────────────────────────┘

关键差异：
1. 参数顺序完全相反！（Python 模式在前，C# 文本在前）
2. DOTALL 在 C# 叫 Singleline（名字不同功能一样）
3. 命名分组语法不同：Python (?P<name>) vs C# (?<name>)
4. C# 没有 re.match，需要用 ^ 锚点模拟
");
        Console.WriteLine("完成!");
    }
}
