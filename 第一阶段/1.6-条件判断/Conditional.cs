// C# 条件判断示例
// 对应文章：1.6 条件判断

using System;

int x = 5;

// ==================== 基本 if-else ====================
Console.WriteLine("=== 基本条件判断 ===");
if (x > 0)
{
    Console.WriteLine("正数");
}
else if (x < 0)
{
    Console.WriteLine("负数");
}
else
{
    Console.WriteLine("零");
}

// C# 需要括号和大括号，Python 不需要
// 注意：C# 用 else if，Python 用 elif

// ==================== 三元表达式 ====================
Console.WriteLine("\n=== 三元表达式 ===");
string result = x > 0 ? "正数" : "非正数";
Console.WriteLine($"{x} 是 {result}");

// ==================== 模式匹配（C# 9+） ====================
Console.WriteLine("\n=== 模式匹配（C# 9+） ===");
string result2 = x switch
{
    > 0 => "正数",
    < 0 => "负数",
    _ => "零"
};
Console.WriteLine($"switch 表达式: {result2}");

// 类型模式匹配
object obj = "hello";
if (obj is string s && s.Length > 3)
{
    Console.WriteLine($"是长度大于3的字符串: {s}");
}

// 属性模式（C# 8+）
var person = new { Name = "Alice", Age = 25 };
string desc = person switch
{
    { Age: < 18 } => "未成年",
    { Age: >= 18 and < 65 } => "成年人",
    _ => "老年人"
};
Console.WriteLine($"{person.Name}: {desc}");

// ==================== 真值判断 ====================
Console.WriteLine("\n=== 真值判断 ===");
// C# 没有 Python 那样的隐式真值判断
string s = "hello";
int n = 0;
var list = new System.Collections.Generic.List<int>();

// C# 需要显式检查每一项
if (s != null && s.Length > 0) Console.WriteLine("s 不为空");
if (n == 0) Console.WriteLine("n 为零");
if (list.Count == 0) Console.WriteLine("list 为空");

// C# 没有 any()/all()，需要用 LINQ
var numbers = new[] { 2, 4, 6, 8, 10 };
bool allEven = numbers.All(n => n % 2 == 0);  // true
bool anyOdd = numbers.Any(n => n % 2 != 0);   // false
Console.WriteLine($"All even: {allEven}, Any odd: {anyOdd}");
