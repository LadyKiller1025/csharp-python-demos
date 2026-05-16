// C# 运算符示例
// 对应文章：1.4 运算符与表达式

using System;

int a = 10, b = 3;

// ==================== 算术运算符 ====================
Console.WriteLine("=== 算术运算符 ===");
Console.WriteLine($"a + b  = {a + b}");          // 13
Console.WriteLine($"a - b  = {a - b}");          // 7
Console.WriteLine($"a * b  = {a * b}");          // 30
Console.WriteLine($"a / b  = {(double)a / b}");  // 3.333...（需要类型转换！）
Console.WriteLine($"a / b  = {a / b}");          // 3（整数 / 整数 = 整数，直接截断！）
Console.WriteLine($"a % b  = {a % b}");          // 1（取余）
Console.WriteLine($"2 ^ 10 = {Math.Pow(2, 10)}");  // 1024（需要 Math.Pow()）

// C# 的 / 对整数直接截断，不像 Python 返回浮点数
Console.WriteLine($"10 / 2 = {10 / 2}");     // 5（整数除法）
Console.WriteLine($"10 / 3 = {10 / 3}");     // 3（截断，不是 3.333）

// ==================== 赋值运算符 ====================
Console.WriteLine("\n=== 赋值运算符 ===");
int x = 10;
x += 3;   // x = x + 3  => 13
Console.WriteLine($"x += 3  => {x}");
x -= 2;   // x = x - 2  => 11
Console.WriteLine($"x -= 2  => {x}");
x *= 2;   // x = x * 2  => 22
Console.WriteLine($"x *= 2  => {x}");
// 注意：C# 没有 //= 和 **= 这样的运算符

// ==================== 三元表达式 ====================
Console.WriteLine("\n=== 三元表达式 ===");
int value = 5;
string result = value > 0 ? "正数" : "非正数";
Console.WriteLine($"{value} 是 {result}");

// ==================== 模式匹配（C# 9+） ====================
Console.WriteLine("\n=== 模式匹配（C# 9+） ===");
string result2 = value switch
{
    > 0 => "正数",
    < 0 => "负数",
    _ => "零"
};
Console.WriteLine($"模式匹配结果: {result2}");

// 类型模式匹配
object obj = 42;
if (obj is int number)
{
    Console.WriteLine($"类型模式匹配: 是 int，值为 {number}");
}

// 属性模式（C# 8+）
var person = new { Name = "Alice", Age = 25 };
if (person is { Age: > 18 })
{
    Console.WriteLine($"{person.Name} 已成年");
}
