// C# 命名空间和 using 示例
// 对应文章：3.5 模块与包
// 对比 Python 的 import 系统

// =====================================================================
// 1. using 指令（等价 Python 的 import）
// =====================================================================

// 标准库引入（等价 Python: import os, import sys）
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

// using 别名（等价 Python: from datetime import datetime as dt）
using DT = System.DateTime;

// using static（等价 Python: from math import sqrt）
using static System.Math;

// =====================================================================
// 2. 命名空间（等价 Python 的包结构）
// =====================================================================
// Python: from mypackage.subpackage import module
// C#:     using MyApp.Models;

namespace MyApp.Models
{
    public class Person
    {
        public string Name { get; set; } = "";
        public int Age { get; set; }
    }
}

// =====================================================================
// 3. 文件级命名空间（C# 10+, 等价 Python 模块级定义）
// =====================================================================
// Python 没有嵌套的 namespace 语法，文件本身就是作用域
// C# 10 之前的 namespace { } 会增加缩进层级

namespace MyApp.Services
{
    public class Calculator
    {
        public static int Add(int a, int b) => a + b;
    }
}

// =====================================================================
// 4. 全局 using（C# 10+, Python 没有等价物）
// =====================================================================
// Python 的 "全局导入" 只在当前文件生效
// C# 10 的 global using 让 using 在整个项目中生效（所有文件自动引入）
//
// 示例（通常放在 GlobalUsings.cs 或 Directory.Build.props）：
//   global using System;
//   global using System.Collections.Generic;
//   global using System.Linq;
//
// Python 没有对应功能 —— 每个文件需要自己 import

// =====================================================================
// 5. 项目结构对比
// =====================================================================
// Python 包结构:                   C# 项目结构:
//   mypackage/                       MyApp/
//     __init__.py                      MyApp.csproj
//     models.py                        GlobalUsings.cs  (全局 using)
//     services.py                      Models/
//     subpackage/                        Person.cs
//       __init__.py                    Services/
//       utils.py                         Calculator.cs
//                                      Program.cs

// =====================================================================
// 6. 主程序入口
// =====================================================================
public class ModulesDemo
{
    static void Main()
    {
        Console.WriteLine("===== 3.5 模块与包 =====\n");

        // --- using 指令演示 ---
        Console.WriteLine("--- 1. using 指令（等价 Python import）---");

        // 等价 Python: import os; os.getcwd()
        Console.WriteLine($"当前目录: {Directory.GetCurrentDirectory()}");

        // 等价 Python: from datetime import datetime as dt
        var now = DT.Now;
        Console.WriteLine($"当前时间: {now:yyyy-MM-dd HH:mm:ss}");

        // 等价 Python: from math import sqrt
        Console.WriteLine($"sqrt(16) = {Sqrt(16)}");

        // --- 别名 ---
        Console.WriteLine("\n--- 2. using 别名 ---");
        Console.WriteLine("using DT = System.DateTime —— 等价 Python: from datetime import datetime as dt");

        // --- using static ---
        Console.WriteLine("\n--- 3. using static ---");
        Console.WriteLine("using static System.Math —— 等价 Python: from math import sqrt");
        Console.WriteLine($"直接调用 Sqrt(25) = {Sqrt(25)}");

        // --- 命名空间 ---
        Console.WriteLine("\n--- 4. 命名空间（等价 Python 包结构）---");
        var person = new MyApp.Models.Person { Name = "Alice", Age = 25 };
        var sum = MyApp.Services.Calculator.Add(3, 4);
        Console.WriteLine($"MyApp.Models.Person: {person.Name}, {person.Age}");
        Console.WriteLine($"MyApp.Services.Calculator.Add(3,4) = {sum}");

        // --- 文件级命名空间 ---
        Console.WriteLine("\n--- 5. 文件级命名空间（C# 10+, 减少缩进）---");
        Console.WriteLine("namespace MyApp.Services;  // C# 10+: 等价 Python 模块级定义");

        // --- global using ---
        Console.WriteLine("\n--- 6. global using（C# 10+, Python 无等价物）---");
        Console.WriteLine("global using System;  // 全项目生效，每个文件无需重复 using");
        Console.WriteLine("Python 没有对应功能 —— 每个文件必须自己 import");

        // --- 对比总结 ---
        Console.WriteLine("\n--- 7. Python import vs C# using 对比 ---");
        Console.WriteLine("  | 概念              | C#                       | Python                    |");
        Console.WriteLine("  |-------------------|--------------------------|---------------------------|");
        Console.WriteLine("  | 引入模块          | using System.IO          | import os                 |");
        Console.WriteLine("  | 引入特定成员      | using static System.Math | from math import sqrt     |");
        Console.WriteLine("  | 别名              | using DT = DateTime      | from datetime import ...   |");
        Console.WriteLine("  | 包 / 命名空间     | namespace MyApp.Models   | mypackage/models.py       |");
        Console.WriteLine("  | 全局引入(C#10)    | global using System      | 无等价物                  |");
        Console.WriteLine("  | 动态加载          | Assembly.Load            | importlib.import_module   |");
    }
}
