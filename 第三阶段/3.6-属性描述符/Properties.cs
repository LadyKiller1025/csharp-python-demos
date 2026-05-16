// C# 属性示例
// 对应文章：3.6 属性与描述符
// 对比 Python 的 @property 描述符机制

using System;
using System.Collections.Generic;

// =====================================================================
// 1. 基本属性（等价 Python @property）
// =====================================================================

public class Person
{
    // 自动属性（C# 编译器自动生成 backing field）
    // Python 等价：self.name = name（普通属性，无验证）
    public string Name { get; set; }

    // 只读属性（C# 8+ expression-bodied）
    // Python 等价：@property def description(self): return f"..."
    public string Description => $"{Name} is {Age} years old";

    // 带验证的属性
    // Python 等价：@email.setter 带 if not value: raise ValueError(...)
    private string _email = "";
    public string Email
    {
        get => _email;
        set
        {
            if (string.IsNullOrEmpty(value))
                throw new ArgumentException("邮箱不能为空");
            _email = value;
        }
    }

    // 计算属性
    // Python 等价：@property def is_adult(self): return self.age >= 18
    public bool IsAdult => Age >= 18;

    public int Age { get; set; }
}

// =====================================================================
// 2. init-only 属性（C# 9+）
// =====================================================================
// Python 等价：在 __init__ 中赋值，之后不可修改
// C# init-only：构造时可赋值，之后只读

public class Temperature
{
    // C# 9+ init-only setter —— 构造时可赋值，之后只读
    // Python 等价：在 __init__ 中 self._celsius = celsius，无 setter
    public double Celsius { get; init; }

    // 计算属性（只读）
    // Python 等价：@property def fahrenheit(self): return self._celsius * 9/5 + 32
    public double Fahrenheit => Celsius * 9 / 5 + 32;

    // Python 等价：@property def kelvin(self): return self._celsius + 273.15
    public double Kelvin => Celsius + 273.15;

    // C# 用构造函数设置 init-only 值
    public Temperature(double celsius)
    {
        Celsius = celsius;
    }
}

// =====================================================================
// 3. required 成员（C# 11+）
// =====================================================================
// Python 等价：__init__ 的必填参数
// C# required：调用者必须设置，编译器强制检查

public class Product
{
    // C# 11+ required：调用者必须初始化此属性
    // Python 等价：def __init__(self, name: str, price: float): ...
    public required string Name { get; init; }
    public required decimal Price { get; init; }

    // 可选属性
    public string? Description { get; init; }

    public override string ToString() =>
        $"{Name}: ${Price}{(Description != null ? $" ({Description})" : "")}";
}

// =====================================================================
// 4. readonly struct（等价 Python __slots__）
// =====================================================================
// Python __slots__：限制属性 + 节省内存
// C# readonly struct：值类型不可变，编译器保证

public readonly struct Point
{
    // 只有 get，没有 set —— 不可变
    // Python 等价：class Point: __slots__ = ['x', 'y'] 且无 setter
    public double X { get; }
    public double Y { get; }

    public Point(double x, double y)
    {
        X = x;
        Y = y;
    }

    public override string ToString() => $"({X}, {Y})";
}

// =====================================================================
// 5. 主程序
// =====================================================================
public class PropertiesDemo
{
    static void Main()
    {
        Console.WriteLine("===== 3.6 属性与描述符 =====\n");

        // 1. 基本属性
        Console.WriteLine("--- 1. @property 等价：C# 属性 ---");
        var person = new Person { Name = "Alice", Age = 25, Email = "alice@example.com" };
        Console.WriteLine($"name:  {person.Name}");
        Console.WriteLine($"email: {person.Email}");
        Console.WriteLine($"desc:  {person.Description}");
        Console.WriteLine($"adult: {person.IsAdult}");

        // 带验证
        try
        {
            person.Email = "";  // 触发验证
        }
        catch (ArgumentException e)
        {
            Console.WriteLine($"验证拦截: {e.Message}");
        }

        // 2. init-only 属性
        Console.WriteLine("\n--- 2. init-only (C# 9+) ---");
        var temp = new Temperature(100);
        Console.WriteLine($"100°C = {temp.Fahrenheit}°F = {temp.Kelvin}K");
        // temp.Celsius = 0;  // 编译错误！init-only 不能在构造后赋值
        Console.WriteLine("temp.Celsius = 0;  // 编译错误！init-only 只能在构造时设置");

        // 3. required 成员
        Console.WriteLine("\n--- 3. required (C# 11+) ---");
        var product = new Product
        {
            Name = "Laptop",          // 必须设置（required）
            Price = 999.99m,          // 必须设置（required）
            Description = "高性能"     // 可选
        };
        Console.WriteLine($"product: {product}");
        Console.WriteLine("（编译器强制要求初始化 Name 和 Price）");

        // 4. readonly struct
        Console.WriteLine("\n--- 4. readonly struct（等价 Python __slots__）---");
        var point = new Point(1.5, 2.5);
        Console.WriteLine($"Point: {point}");
        // point.X = 3;  // 编译错误！readonly struct 不可修改
        Console.WriteLine("point.X = 3;  // 编译错误！readonly struct 不可变");

        // 5. 对比总结
        Console.WriteLine("\n--- 5. C# vs Python 属性对比 ---");
        Console.WriteLine("  | 概念          | C#                    | Python                 |");
        Console.WriteLine("  |---------------|-----------------------|------------------------|");
        Console.WriteLine("  | 属性          | { get; set; }        | @property              |");
        Console.WriteLine("  | 带验证        | set { throw; }        | @xxx.setter + 验证     |");
        Console.WriteLine("  | 计算属性      => expr                    | @property return expr  |");
        Console.WriteLine("  | init-only     | { get; init; } (C# 9) | __init__ 中赋值        |");
        Console.WriteLine("  | required      | required (C# 11)      | __init__ 参数          |");
        Console.WriteLine("  | 不可变        | readonly struct        | __slots__ + 无 setter  |");
    }
}
