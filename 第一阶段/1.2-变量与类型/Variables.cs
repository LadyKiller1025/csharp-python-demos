// C# 变量与类型示例
// 对应文章：1.2 变量与类型系统

using System;
using System.Collections.Generic;

// ==================== 显式类型声明 ====================
Console.WriteLine("=== 显式类型声明 ===");
int x = 5;
string name = "张三";
double price = 9.99;
bool isTrue = true;

// ==================== 类型推断（var）====================
Console.WriteLine("\n=== 类型推断 var ===");
var y = 10;        // 编译器推断为 int（一旦确定不能变）
var msg = "hello"; // 编译器推断为 string
Console.WriteLine($"y = {y}, msg = {msg}");

// ==================== 动态类型 ====================
Console.WriteLine("\n=== 动态类型 dynamic ===");
dynamic z = 5;     // 运行时才确定类型
z = "hello";       // 可以改变类型（但失去编译时类型安全！）
Console.WriteLine($"z = {z}");

// ==================== 类型检查 ====================
Console.WriteLine("\n=== 类型检查 ===");
Console.WriteLine($"x is int:       {x is int}");           // true
Console.WriteLine($"x.GetType():    {x.GetType()}");        // System.Int32
Console.WriteLine($"x is > 0:       {x is > 0}");           // true（模式匹配）

// ==================== 类型转换 ====================
Console.WriteLine("\n=== 类型转换 ===");
string s = "123";
int n = int.Parse(s);                          // 123（失败抛异常）
bool success = int.TryParse(s, out int result);  // 安全转换（推荐！）
Console.WriteLine($"int.Parse('123')   = {n}");
Console.WriteLine($"TryParse('123')    = {success}, {result}");
Console.WriteLine($"TryParse('abc')    = {int.TryParse("abc", out _)}, {int.TryParse("abc", out int r2)}");

// ==================== 常量 ====================
Console.WriteLine("\n=== 常量 ===");
const double Pi = 3.14159;     // 编译时常量
const string Greeting = "Hello";
// Pi = 999;  // 编译错误！常量不可修改
Console.WriteLine($"Pi = {Pi}");

// readonly（运行时常量，可在构造函数中赋值）
readonly int MaxRetries = 3;   // 只能在类中使用
