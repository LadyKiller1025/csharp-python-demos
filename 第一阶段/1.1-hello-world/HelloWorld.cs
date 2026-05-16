// C# Hello World 示例
// 对应文章：1.1 Hello World 与程序结构

using System;

// ==================== 传统写法（C# 1.0 ~ 8.0）====================
// C# 需要 namespace + class + Main 方法，结构严谨但啰嗦
namespace MyApp
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello, World!");
        }
    }
}

// ==================== C# 9+ 顶级语句（推荐！）====================
// 直接在文件顶层写代码，编译器自动生成 namespace/class/Main
// 这时候 C# 和 Python 一样简洁了！
//
// Console.WriteLine("Hello, World!");

// 顶级语句的完整示例：
// string name = "World";
// Console.WriteLine($"Hello, {name}!");
//
// 编译器会自动生成等价的传统结构
// 注意：顶级语句只能在一个文件中使用
