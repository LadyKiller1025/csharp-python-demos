// ============================================================
// C# 类定义 —— 对比 Python 理解 C# 类
// 对应文章：3.1 类的定义
// ============================================================
// Python 等价：Python class 是动态的，C# class 是静态类型的。
// C# 的类是引用类型（值类型用 struct）。
// ============================================================

using System;
using System.Collections.Generic;

// ============================================================
// 1. 基本类定义
// ============================================================
// Python 等价：class Person: def __init__(self, name, age):
// C# 构造函数名必须与类名相同，Python 用 __init__

public class Person
{
    // 字段（private）—— Python 中约定用 _ 前缀
    private string name;
    private int age;

    // 类变量（static 字段）—— Python 中直接写在类体中
    public static int InstanceCount = 0;

    // 构造函数
    public Person(string name, int age)
    {
        this.name = name;
        this.age = age;
        InstanceCount++;
    }

    // 属性（get/set）—— Python 等价：@property + @xxx.setter
    public string Name
    {
        get { return name; }
        set { name = value; }
    }

    public int Age
    {
        get { return age; }
        set { age = value; }
    }

    // 只读属性（只有 get）—— Python 等价：@property 只有 getter
    public string ReadOnlyName => name;

    // 方法
    public string Greet()
    {
        return $"Hello, I'm {name}, age {age}";
    }

    // 重写 ToString() —— Python 等价：__str__
    public override string ToString()
    {
        return $"Person(name={Name}, age={Age})";
    }
}

// ============================================================
// 2. 自动属性 —— 简洁写法
// ============================================================
// Python 等价：dataclass 自动生成的属性

public class PersonAuto
{
    public string Name { get; set; }   // 自动实现的属性
    public int Age { get; set; }

    public PersonAuto(string name, int age)
    {
        Name = name;
        Age = age;
    }
}

// ============================================================
// 3. 只读属性（init-only）—— C# 9+
// ============================================================
// Python 等价：frozen=True dataclass 的字段

public class PersonReadOnly
{
    public string Name { get; }  // 只能在构造函数中赋值
    public int Age { get; }

    public PersonReadOnly(string name, int age)
    {
        Name = name;
        Age = age;
    }

    public override string ToString() => $"PersonReadOnly({Name}, {Age})";
}

// ============================================================
// 4. record 类型（C# 9+）—— Python @dataclass 的最佳等价
// ============================================================
// 自动生成：ToString, Equals, GetHashCode, Deconstruct
// value-based 相等比较（跟 Python @dataclass 一致）

public record PersonRecord(string Name, int Age);

// 带默认值的 record
public record Employee(string Name, float Salary, string[] Tags = null);

// ============================================================
// 5. readonly struct —— Python 等价：frozen=True dataclass
// ============================================================

public readonly struct Vector
{
    public double X { get; }
    public double Y { get; }

    public Vector(double x, double y)
    {
        X = x;
        Y = y;
    }

    // 运算符重载 —— Python 等价：__add__, __mul__ 等
    public static Vector operator +(Vector a, Vector b)
        => new(a.X + b.X, a.Y + b.Y);

    public static Vector operator *(Vector a, double scalar)
        => new(a.X * scalar, a.Y * scalar);

    public override string ToString() => $"({X}, {Y})";
}

// ============================================================
// 6. static class —— Python 等价：类作为命名空间（纯静态方法容器）
// ============================================================
// C# 的 static class 不能被实例化
// Python 没有语法限制，靠约定（不写 __init__，只写 @staticmethod）

public static class MathUtils
{
    public const double PI = 3.14159265358979;

    public static double CircleArea(double radius)
        => PI * radius * radius;

    public static long Factorial(int n)
        => n <= 1 ? 1 : n * Factorial(n - 1);
}

// ============================================================
// 7. Main 方法 —— 运行演示
// ============================================================

public static class Program
{
    public static void Main()
    {
        // 1. 基本类
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine("1. 基本类定义 & 构造函数");
        Console.WriteLine("=" + new string('=', 49));

        var person = new Person("Alice", 25);
        Console.WriteLine(person.Greet());
        Console.WriteLine($"str:  {person}");
        Console.WriteLine($"repr: {person.ToString()}");  // C# 无 repr，最接近是 debuggerDisplay
        Console.WriteLine($"实例计数: {Person.InstanceCount}");

        // 2. 自动属性
        Console.WriteLine();
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine("2. 自动属性");
        Console.WriteLine("=" + new string('=', 49));

        var p2 = new PersonAuto("Bob", 30);
        Console.WriteLine($"姓名: {p2.Name}, 年龄: {p2.Age}");
        p2.Age = 31;
        Console.WriteLine($"新年龄: {p2.Age}");

        // 3. 只读属性
        Console.WriteLine();
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine("3. 只读属性 (C# 有语法保护，Python 仅靠约定)");
        Console.WriteLine("=" + new string('=', 49));

        var pr = new PersonReadOnly("Charlie", 35);
        Console.WriteLine(pr);
        // pr.Name = "Dave";  // 编译错误！C# 有语法强制

        // 4. record 类型
        Console.WriteLine();
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine("4. record 类型 —— Python @dataclass 的最佳等价");
        Console.WriteLine("=" + new string('=', 49));

        var r1 = new PersonRecord("Alice", 25);
        var r2 = new PersonRecord("Alice", 25);
        var r3 = new PersonRecord("Bob", 30);
        Console.WriteLine($"r1 = {r1}");
        Console.WriteLine($"r1 == r2? {r1 == r2}");  // True (value-based)
        Console.WriteLine($"r1 == r3? {r1 == r3}");  // False

        // record 支持解构
        var (name, age) = r1;
        Console.WriteLine($"解构: name={name}, age={age}");

        // 5. readonly struct
        Console.WriteLine();
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine("5. 运算符重载 (readonly struct)");
        Console.WriteLine("=" + new string('=', 49));

        var v1 = new Vector(1, 2);
        var v2 = new Vector(3, 4);
        Console.WriteLine($"v1 = {v1}");
        Console.WriteLine($"v2 = {v2}");
        Console.WriteLine($"v1 + v2 = {v1 + v2}");
        Console.WriteLine($"v1 * 3 = {v1 * 3}");

        // 6. static class
        Console.WriteLine();
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine("6. static class —— 不能实例化");
        Console.WriteLine("=" + new string('=', 49));

        Console.WriteLine($"PI = {MathUtils.PI}");
        Console.WriteLine($"circle_area(5) = {MathUtils.CircleArea(5):F2}");
        Console.WriteLine($"factorial(5) = {MathUtils.Factorial(5)}");

        // 7. 对比总结
        Console.WriteLine();
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine("7. Python vs C# 类定义对比总结");
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine(@"
| 概念            | C#                        | Python               |
|-----------------|---------------------------|----------------------|
| 构造函数        | public Person(...)        | def __init__(...)    |
| 属性            | public string Name { }    | @property            |
| 静态字段        | static int Count          | 类变量               |
| 静态方法        | static void Foo()         | @staticmethod        |
| 不可变类        | record / readonly struct  | @dataclass(frozen)   |
| 字段限制        | readonly 修饰符           | __slots__            |
| 隐藏实现        | private / internal        | _ 前缀约定           |
| 命名空间工具类  | static class              | 类 + @staticmethod   |
| ToString()      | override string ToString  | __str__ / __repr__   |
| 相等比较        | record / IEquatable<T>    | __eq__               |
");
    }
}
