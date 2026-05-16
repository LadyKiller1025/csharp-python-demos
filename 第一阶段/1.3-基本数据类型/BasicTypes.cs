// C# 基本数据类型示例
// 对应文章：1.3 基本数据类型

using System;
using System.Numerics;

// ==================== 整数类型（多种精度！） ====================
Console.WriteLine("=== 整数类型 ===");
byte a = 255;                    // 8位，0-255
short b = 32767;                 // 16位
int c = 2147483647;              // 32位，最常用
long d = 9223372036854775807;    // 64位

Console.WriteLine($"byte:   {a} (8位)");
Console.WriteLine($"short:  {b} (16位)");
Console.WriteLine($"int:    {c} (32位，最常用)");
Console.WriteLine($"long:   {d} (64位)");

// C# 没有无限精度整数，需要 BigInteger
BigInteger big = BigInteger.Pow(2, 1000);
Console.WriteLine($"2^1000 的位数: {big.ToString().Length}");  // 302 位！

// 不同进制表示
Console.WriteLine($"二进制:  {Convert.ToInt32("1010", 2)}");   // 10
Console.WriteLine($"十六进制: 0x{255:X}");                      // 0xFF

// ==================== 浮点数 ====================
Console.WriteLine("\n=== 浮点数 ===");
float e = 3.14f;       // 32位单精度（注意 f 后缀！）
double f = 3.14;       // 64位双精度，最常用
decimal g = 3.14m;     // 128位，金融计算（注意 m 后缀！）

Console.WriteLine($"float:   {e} (32位)");
Console.WriteLine($"double:  {f} (64位，最常用)");
Console.WriteLine($"decimal: {g} (128位，金融计算)");

// 浮点数精度问题
Console.WriteLine($"0.1 + 0.2 = {0.1 + 0.2}");          // 0.30000000000000004
Console.WriteLine($"0.1 + 0.2 == 0.3? {0.1 + 0.2 == 0.3}");  // False!
// C# 的 decimal 不会有这个问题
Console.WriteLine($"decimal: {0.1m + 0.2m == 0.3m}");    // True

// ==================== 布尔类型 ====================
Console.WriteLine("\n=== 布尔类型 ===");
bool a1 = true;
bool b1 = false;
Console.WriteLine($"true && false = {true && false}");  // false
Console.WriteLine($"true || false = {true || false}");  // true
Console.WriteLine($"!true         = {!true}");          // false

// C# 的 bool 不能当数字用！
// int x = (int)true;  // 编译错误！需要显式转换
Console.WriteLine($"(int)true = {(int)true}");           // 1（需要显式转换）
Console.WriteLine($"(int)false = {(int)false}");         // 0

// ==================== 字符串类型 ====================
Console.WriteLine("\n=== 字符串类型 ===");
string s1 = "Hello";
string s2 = "World";
string s3 = s1 + " " + s2;     // 拼接
string s4 = $"{s1} {s2}";      // 插值（推荐）
Console.WriteLine($"拼接: {s3}");
Console.WriteLine($"插值: {s4}");

// 字符串是不可变的
int len = s1.Length;            // 5（属性，不是函数！Python 用 len()）
string upper = s1.ToUpper();   // "HELLO"
string sub = s1.Substring(1, 3);  // "ell"
Console.WriteLine($"长度: {len}, 大写: {upper}, 子串: {sub}");

// ==================== 空值 ====================
Console.WriteLine("\n=== 空值 ===");
string s = null;
int? x = null;            // 可空类型（C# 独有！Python 没有）
double? y = null;
Console.WriteLine($"s == null: {s == null}");           // true
Console.WriteLine($"x has value: {x.HasValue}");       // false
Console.WriteLine($"x ?? default: {x ?? 0}");          // 0（空合并运算符）
