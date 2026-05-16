// C# 字典与集合示例
// 对应文章：1.9 字典与集合

using System;
using System.Collections.Generic;
using System.Linq;

// ==================== 字典创建 ====================
Console.WriteLine("=== 字典创建 ===");
var dict1 = new Dictionary<string, int>();
var dict2 = new Dictionary<string, int>
{
    { "Alice", 25 },
    { "Bob", 30 },
    { "Charlie", 35 }
};

// C# 9+ 集合初始化
var dict3 = new Dictionary<string, int>
{
    ["Alice"] = 25,
    ["Bob"] = 30
};
Console.WriteLine($"dict2: Alice={dict2["Alice"]}, Bob={dict2["Bob"]}");

// ==================== 添加/修改/访问 ====================
Console.WriteLine("\n=== 添加/修改/访问 ===");
var scores = new Dictionary<string, int> { { "Alice", 95 }, { "Bob", 87 } };

scores.Add("Charlie", 92);         // 添加（重复键会抛异常！）
scores["Alice"] = 98;              // 修改
scores.TryAdd("David", 0);         // 尝试添加（不抛异常）
Console.WriteLine($"Alice: {scores["Alice"]}");

// 安全访问（C# 必须用 TryGetValue，Python 用 get 一行搞定）
if (scores.TryGetValue("David", out int val))
{
    Console.WriteLine($"David: {val}");
}

// ==================== 删除 ====================
Console.WriteLine("\n=== 删除 ===");
scores.Remove("Bob");              // 删除指定键
bool removed = scores.Remove("NonExist");  // 返回是否成功
Console.WriteLine($"删除 Bob 后: {string.Join(", ", scores.Select(kvp => $"{kvp.Key}={kvp.Value}"))}");

// ==================== 判断和遍历 ====================
Console.WriteLine("\n=== 判断和遍历 ===");
Console.WriteLine($"ContainsKey('Alice'): {scores.ContainsKey("Alice")}");
Console.WriteLine($"ContainsValue(95):    {scores.ContainsValue(95)}");

foreach (var kvp in scores)
{
    Console.WriteLine($"  {kvp.Key}: {kvp.Value}");
}

// ==================== LINQ 操作 ====================
Console.WriteLine("\n=== LINQ 操作 ===");
var passed = scores.Where(kvp => kvp.Value >= 90)
                   .ToDictionary(kvp => kvp.Key, kvp => kvp.Value);
Console.WriteLine($"及格(>=90): {string.Join(", ", passed.Select(kvp => $"{kvp.Key}={kvp.Value}"))}");

// ==================== 集合 ====================
Console.WriteLine("\n=== HashSet 集合 ===");
var set1 = new HashSet<int> { 1, 2, 3, 4, 5 };
var set2 = new HashSet<int> { 4, 5, 6, 7, 8 };

// C# 的集合运算需要方法调用（不如 Python 的运算符简洁）
var union = new HashSet<int>(set1);
union.UnionWith(set2);
Console.WriteLine($"并集: {{{string.Join(", ", union)}}}");

var intersect = new HashSet<int>(set1);
intersect.IntersectWith(set2);
Console.WriteLine($"交集: {{{string.Join(", ", intersect)}}}");

var except = new HashSet<int>(set1);
except.ExceptWith(set2);
Console.WriteLine($"差集: {{{string.Join(", ", except)}}}");

var symmetric = new HashSet<int>(set1);
symmetric.SymmetricExceptWith(set2);
Console.WriteLine($"对称差: {{{string.Join(", ", symmetric)}}}");

// 去重
var list = new List<int> { 1, 2, 2, 3, 3, 3, 4, 4, 4, 4 };
var unique = list.Distinct().ToList();
Console.WriteLine($"去重: [{string.Join(", ", list)}] -> [{string.Join(", ", unique)}]");
