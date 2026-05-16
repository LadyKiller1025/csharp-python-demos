// C# 元组与解包示例
// 对应文章：1.10 元组与解包

using System;

// ==================== 元组创建 ====================
Console.WriteLine("=== 元组创建 ===");
var t1 = (1, "hello");                      // 未命名元组
var t2 = (X: 1, Y: "hello");               // 命名元组
(int Age, string Name) t3 = (25, "Alice");  // 声明式命名
Console.WriteLine($"t1 = {t1}");
Console.WriteLine($"t2 = {t2}");

// ==================== 访问 ====================
Console.WriteLine("\n=== 访问 ===");
Console.WriteLine($"t1.Item1  = {t1.Item1}");   // 1
Console.WriteLine($"t2.X      = {t2.X}");        // 1
Console.WriteLine($"t3.Name   = {t3.Name}");     // "Alice"

// ==================== 解构 ====================
Console.WriteLine("\n=== 解构 ===");
var (age, name) = t2;
Console.WriteLine($"{name} is {age}");

// 交换变量
int x = 1, y = 2;
(x, y) = (y, x);  // x=2, y=1
Console.WriteLine($"交换后: x={x}, y={y}");

// 忽略值
var (_, name2) = (1, "Alice");
Console.WriteLine($"忽略第一个: {name2}");

// ==================== 函数多值返回 ====================
Console.WriteLine("\n=== 函数多值返回 ===");
// C# 有两种方式：元组返回（现代）和 out 参数（传统）

// 方式1：元组返回（推荐，等价于 Python 的 return a, b）
static (int Quotient, int Remainder) Divide(int a, int b)
{
    return (a / b, a % b);
}
var (quotient, remainder) = Divide(10, 3);
Console.WriteLine($"10 ÷ 3 = {quotient} 余 {remainder}");

// 方式2：out 参数（传统方式，Python 没有对应概念）
static void Divide2(int a, int b, out int q, out int r)
{
    q = a / b;
    r = a % b;
}
Divide2(10, 3, out int q2, out int r2);
Console.WriteLine($"out 参数: {q2} 余 {r2}");

// ==================== Record 类型（C# 9+，等价于 Python 的 namedtuple）====================
Console.WriteLine("\n=== Record 类型（C# 9+）===");
record Person(string Name, int Age, string Email);
var p = new Person("Alice", 25, "alice@example.com");
Console.WriteLine($"名字: {p.Name}");
Console.WriteLine($"record: {p}");  // 自动生成 ToString
// record 支持值相等比较
var p2 = new Person("Alice", 25, "alice@example.com");
Console.WriteLine($"相等: {p == p2}");  // true

// ==================== 值元组 vs 引用类型 ====================
Console.WriteLine("\n=== 值元组是值类型 ===");
// C# 的 ValueTuple 是值类型（栈上存储），Python 的 tuple 是引用类型
var a = (1, 2, 3);
var b = a;  // 复制值
b.Item1 = 99;
Console.WriteLine($"a = {a}");   // (1, 2, 3)（不受影响）
Console.WriteLine($"b = {b}");   // (99, 2, 3)
