// C# 字符串操作示例
// 对应文章：1.5 字符串操作

using System;

// ==================== 字符串创建 ====================
string s1 = "Hello";
string s2 = "World";
string s3 = @"C:\path\to\file";       // 原始字符串（@前缀）
string s4 = $@"Hello {s1}";           // 插值原始字符串

// ==================== 字符串拼接与插值 ====================
string result = s1 + " " + s2;         // 拼接
string interpolated = $"{s1} {s2}";    // 插值（推荐）

// ==================== 字符串格式化 ====================
Console.WriteLine("=== 字符串格式化 ===");
decimal price = 12.345m;
string name = "Alice";
decimal balance = 1234567.89m;

Console.WriteLine($"Price: {price:F2}");          // "Price: 12.35"
Console.WriteLine($"Name: {name,10}");            // "Name:      Alice"（右对齐）
Console.WriteLine($"Name: {-name,-10}");          // "Name: Alice     "（左对齐）
Console.WriteLine($"Balance: {balance:C}");       // "Balance: ¥1,234,567.89"（货币）
Console.WriteLine($"Hex: {255:X}");               // "Hex: FF"
Console.WriteLine($"Padded: {42:D5}");            // "Padded: 00042"

// ==================== 字符串访问与切片 ====================
Console.WriteLine("\n=== 字符串切片 ===");
string s = "Hello, World!";

// 单个字符访问
char first = s[0];               // 'H'
char last = s[s.Length - 1];     // '!'（C# 没有负数索引）

// C# 8.0+ 范围语法
string sub1 = s[..5];            // "Hello"（等同于 s[0:5]）
string sub2 = s[7..];            // "World!"（等同于 s[7:]）
string sub3 = s[..^1];           // "Hello, World"（去掉最后一个字符）
string sub5 = new string(s.Reverse().ToArray());  // 反转

Console.WriteLine($"原字符串:  {s}");
Console.WriteLine($"s[..5]:    {sub1}");
Console.WriteLine($"s[7..]:    {sub2}");
Console.WriteLine($"反转:      {sub5}");

// ==================== 常用字符串方法 ====================
Console.WriteLine("\n=== 常用方法 ===");
int index = s.IndexOf("World");          // 7
bool contains = s.Contains("Hello");     // true
bool starts = s.StartsWith("Hello");     // true
bool ends = s.EndsWith("World!");        // true

string replaced = s.Replace("World", "Python");  // "Hello, Python!"
string[] parts = s.Split(',');           // ["Hello", " World!"]
string joined = string.Join("-", new[] { "a", "b", "c" });  // "a-b-c"

Console.WriteLine($"IndexOf:  {index}");
Console.WriteLine($"Contains: {contains}");
Console.WriteLine($"Replace:  {replaced}");
Console.WriteLine($"Split:    [{string.Join(", ", parts)}]");
Console.WriteLine($"Join:     {joined}");

// 大小写与去空格
Console.WriteLine($"ToUpper:  {"hello".ToUpper()}");      // HELLO
Console.WriteLine($"ToLower:  {"HELLO".ToLower()}");      // hello
Console.WriteLine($"Trim:     {"  hello  ".Trim()}");     // hello

// ==================== 字符串不可变性 ====================
Console.WriteLine("\n=== 字符串不可变性 ===");
// C# 和 Python 的字符串都是不可变的！
// s[0] = 'h';  // 编译错误！

// 需要"修改"时，创建新字符串
string newS = "h" + s1[1..];     // "hello"
Console.WriteLine($"修改后: {newS}");

// 大量拼接用 StringBuilder（高效）
var sb = new System.Text.StringBuilder();
for (int i = 0; i < 5; i++)
{
    sb.Append(i);
    if (i < 4) sb.Append(",");
}
Console.WriteLine($"StringBuilder: {sb}");  // "0,1,2,3,4"

// ==================== 字符串比较 ====================
Console.WriteLine("\n=== 字符串比较 ===");
Console.WriteLine($"'abc' < 'abd':  {"abc" < "abd"}");     // True
Console.WriteLine($"'abc' == 'abc': {"abc" == "abc"}");    // True
Console.WriteLine($"'abc' != 'ABC': {"abc" != "ABC"}");    // True
// 注意：C# 默认区分大小写，Ordinal 比较
