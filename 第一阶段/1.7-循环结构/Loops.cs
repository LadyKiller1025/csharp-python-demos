// C# 循环结构示例
// 对应文章：1.7 循环结构

using System;
using System.Linq;

// ==================== 传统 for 循环 ====================
Console.WriteLine("=== 传统 for 循环 ===");
for (int i = 0; i < 5; i++)
{
    Console.Write($"{i} ");  // 0 1 2 3 4
}
Console.WriteLine();

// ==================== foreach 循环 ====================
Console.WriteLine("\n=== foreach 循环 ===");
int[] numbers = { 1, 2, 3, 4, 5 };
foreach (var num in numbers)
{
    Console.Write($"{num} ");
}
Console.WriteLine();

// 倒序遍历
Console.Write("倒序: ");
for (int i = numbers.Length - 1; i >= 0; i--)
{
    Console.Write($"{numbers[i]} ");
}
Console.WriteLine();

// ==================== 带索引的遍历 ====================
Console.WriteLine("\n=== 带索引遍历 ===");
// C# 的 foreach 没有内置 index，需要手动维护或用 LINQ
for (int i = 0; i < numbers.Length; i++)
{
    Console.WriteLine($"  [{i}] = {numbers[i]}");
}
// LINQ 方式（C# 等价于 Python 的 enumerate）
foreach (var (num, i) in numbers.Select((n, i) => (n, i)))
{
    Console.WriteLine($"  第{i + 1}个: {num}");
}

// ==================== while 循环 ====================
Console.WriteLine("\n=== while 循环 ===");
int i2 = 0;
while (i2 < 5)
{
    Console.Write($"{i2} ");
    i2++;
}
Console.WriteLine();

// ==================== do-while 循环（Python 没有）====================
Console.WriteLine("\n=== do-while 循环 ===");
int j = 0;
do
{
    Console.Write($"{j} ");
    j++;
} while (j < 5);
Console.WriteLine();
// Python 模拟：while True + break

// ==================== break 和 continue ====================
Console.WriteLine("\n=== break 和 continue ===");
Console.Write("跳过 5，到 10 停止: ");
for (int k = 0; k < 20; k++)
{
    if (k == 5) continue;  // 跳过 5
    if (k == 10) break;    // 遇到 10 停止
    Console.Write($"{k} ");  // 0 1 2 3 4 6 7 8 9
}
Console.WriteLine();

// ==================== LINQ 查询（C# 独有的声明式循环） ====================
Console.WriteLine("\n=== LINQ 查询 ===");
var evenNumbers = numbers.Where(n => n % 2 == 0).ToList();
var doubled = numbers.Select(n => n * 2).ToList();
int sum = numbers.Sum();
Console.WriteLine($"偶数: [{string.Join(", ", evenNumbers)}]");
Console.WriteLine($"翻倍: [{string.Join(", ", doubled)}]");
Console.WriteLine($"求和: {sum}");
// Python 对应：列表推导式 [n for n in numbers if n % 2 == 0]
