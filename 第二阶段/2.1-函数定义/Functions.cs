// ============================================================
// C# 函数定义示例 —— C# 老兵的 Python 修炼手册 第二阶段 2.1
// ============================================================
// 这个文件展示 C# 对应的函数定义方式，和 Python 版本对照学习
// Python 同学：这些就是你们 def 背后的"真身"

using System;
using System.Collections.Generic;
using System.Linq;

class Functions
{
    static void Main(string[] args)
    {
        // ============================================================
        // 1. 基础语法：必须声明返回类型和参数类型
        // ============================================================
        // Python 等价：def greet(name): return f"Hello, {name}!"
        // C# 的仪式感：返回类型 + 参数类型 + 大括号，三件套不能少

        Console.WriteLine("=== 1. 基础语法 ===");
        Console.WriteLine(Greet("CSharp"));

        // ============================================================
        // 2. 无返回值用 void
        // ============================================================
        // Python 等价：def say_hello(): print("Hello!")
        // Python 不写 return 返回 None，C# 必须用 void 声明

        Console.WriteLine("\n=== 2. 无返回值 ===");
        SayHello();

        // ============================================================
        // 3. 多参数
        // ============================================================
        // Python 等价：def add(a: int, b: int) -> int: return a + b
        // C# 的类型系统比 Python 严格得多——传错类型编译就报错

        Console.WriteLine("\n=== 3. 多参数与类型系统 ===");
        Console.WriteLine($"add(3, 5) = {Add(3, 5)}");
        // 下面这行在 C# 中编译不通过，Python 却能跑：
        // Add("Hello", " World");  // ❌ 编译错误：不能将 string 转为 int
        Console.WriteLine("Python: '类型提示？我看看就好，不检查的。'");
        Console.WriteLine("C#：'类型？必须的！编译器说了算！'");

        // ============================================================
        // 4. 默认参数
        // ============================================================
        // Python 等价：def greet2(name, greeting="Hello"):
        // 规则一样：有默认值的参数放后面
        // ⚠️ C# 有个 Python 没有的限制：默认值必须在编译时确定
        //    Python 允许 mutable 默认值（虽然这是个坑）

        Console.WriteLine("\n=== 4. 默认参数 ===");
        Console.WriteLine(Greet2("World"));
        Console.WriteLine(Greet2("World", "你好"));

        // ============================================================
        // 5. params 可变参数
        // ============================================================
        // Python 等价：def sum_numbers(*args): return sum(args)
        // C# 的 params 是个语法糖，编译器会自动把参数打包成数组
        // Python 的 *args 更灵活——打包成 tuple

        Console.WriteLine("\n=== 5. params 可变参数 ===");
        Console.WriteLine($"Sum(1, 2, 3) = {Sum(1, 2, 3)}");
        Console.WriteLine($"Sum(10, 20) = {Sum(10, 20)}");

        // ============================================================
        // 6. 命名参数
        // ============================================================
        // Python 没有显式等价物，Python 调用时天然可以写 keyword=value
        // C# 要求参数必须在定义时加上名称，调用时用 名称: 值 传递
        // 用途：跳过中间的默认参数，提高可读性

        Console.WriteLine("\n=== 6. 命名参数 ===");
        PrintInfo(name: "张三", email: "zhangsan@example.com");
        // 等价于 PrintInfo("张三", 0, "zhangsan@example.com");
        Console.WriteLine("Python 调用时天然就能写 name='张三'");
        Console.WriteLine("C# 需要在定义时就标记参数名称");

        // ============================================================
        // 7. Func/Action 委托（函数作为参数）
        // ============================================================
        // Python 等价：def apply(func, value): return func(value)
        // Python 函数是一等公民，直接传函数名就行
        // C# 需要定义委托类型——但 Func<T> 内置了，也不麻烦

        Console.WriteLine("\n=== 7. Func/Action 委托 ===");
        Console.WriteLine($"Apply(x => x * 2, 5) = {Apply(x => x * 2, 5)}");
        Console.WriteLine($"Apply(str, 42) = {Apply(x => x.ToString(), 42)}");

        // ============================================================
        // 8. 多个返回值（命名元组）
        // ============================================================
        // Python 等价：def divide(a, b): return a // b, a % b
        // Python 天然返回 tuple，C# 需要声明 ValueTuple
        // C# 的优势：可以给字段命名，更清晰

        Console.WriteLine("\n=== 8. 命名元组多返回值 ===");
        var (quotient, remainder) = Divide(10, 3);
        Console.WriteLine($"10 / 3 = {quotient} 余 {remainder}");

        // ============================================================
        // 9. 本地函数（C# 7.0+）
        // ============================================================
        // Python 等价：嵌套函数 + nonlocal
        // C# 本地函数可以递归，可以有泛型参数
        // Python 的 nonlocal 允许修改外部变量，C# 本地函数也能捕获变量

        Console.WriteLine("\n=== 9. 本地函数与闭包 ===");
        var counter = MakeCounter(10);
        Console.WriteLine($"计数器: {counter()}");  // 11
        Console.WriteLine($"计数器: {counter()}");  // 12
        Console.WriteLine($"计数器: {counter()}");  // 13

        // ============================================================
        // 10. Lambda 表达式（预告）
        // ============================================================
        // Python 等价：lambda x: x ** 2
        // C# 的 Lambda 比 Python 强大：可以有多行、能捕获变量、支持 async
        // 这是下一节的内容，这里先预热

        Console.WriteLine("\n=== 10. Lambda 表达式预告 ===");
        Func<int, int> square = x => x * x;
        Func<int, int, int> addLambda = (a, b) => a + b;
        Console.WriteLine($"square(5) = {square(5)}");
        Console.WriteLine($"addLambda(3, 4) = {addLambda(3, 4)}");

        // ============================================================
        // 11. 局部变量 + lambda 闭包
        // ============================================================
        // Python 等价：nonlocal 修改外部变量
        // C# Lambda 可以捕获外部变量（闭包），但行为有区别：
        // C# 的闭包捕获的是变量的"引用"，不是值
        Console.WriteLine("\n=== 11. 闭包 ===");
        Func<int, int> adder = CreateAdder(5);
        Console.WriteLine($"adder(3) = {adder(3)}");   // 8
        Console.WriteLine($"adder(10) = {adder(10)}");  // 15

        // ============================================================
        // 12. 方法重载 vs 默认参数
        // ============================================================
        // Python 不支持方法重载（同名函数会覆盖）
        // C# 通过方法重载和默认参数两种方式处理

        Console.WriteLine("\n=== 12. 方法重载 vs 默认参数 ===");
        Console.WriteLine($"Multiply(3, 4) = {Multiply(3, 4)}");
        Console.WriteLine($"Multiply(3) = {Multiply(3)}");

        // ============================================================
        // 总结对比
        // ============================================================
        Console.WriteLine("\n" + new string('=', 50));
        Console.WriteLine("📋 C# vs Python 函数定义 速查表");
        Console.WriteLine(new string('=', 50));
        Console.WriteLine(@"
┌─────────────────────┬──────────────────────────────┐
│       C#            │          Python              │
├─────────────────────┼──────────────────────────────┤
│ void Method()       │ def func():                  │
│ int Add(int a, int b)│ def add(a: int, b: int) -> int│
│ params int[] nums   │ *args                       │
│ Dictionary<...>     │ **kwargs                    │
│ 默认参数在最后       │ 同上                        │
│ Func<T,R> 委托      │ 直接传函数名/lambda          │
│ ValueTuple 多返回值  │ 直接 return a, b            │
│ 本地函数             │ 嵌套函数 + nonlocal          │
│ 方法重载             │ 不支持（用默认参数代替）      │
│ 必须声明类型         │ 类型提示可选                 │
└─────────────────────┴──────────────────────────────┘
");
    }

    // ============================================================
    // 1. 基础语法
    // ============================================================
    static string Greet(string name)
    {
        return $"Hello, {name}!";
    }

    // ============================================================
    // 2. 无返回值
    // ============================================================
    static void SayHello()
    {
        Console.WriteLine("Hello!");
    }

    // ============================================================
    // 3. 多参数
    // ============================================================
    static int Add(int a, int b)
    {
        return a + b;
    }

    // ============================================================
    // 4. 默认参数
    // ============================================================
    static string Greet2(string name, string greeting = "Hello")
    {
        return $"{greeting}, {name}!";
    }

    // ============================================================
    // 5. params 可变参数
    // ============================================================
    static int Sum(params int[] numbers)
    {
        return numbers.Sum();
    }

    // ============================================================
    // 6. 命名参数
    // ============================================================
    static void PrintInfo(string name, int age = 0, string email = "")
    {
        Console.WriteLine($"  {name}, 年龄: {age}, 邮箱: {email}");
    }

    // ============================================================
    // 7. 函数作为参数（Func 委托）
    // ============================================================
    static int Apply(Func<int, int> func, int value)
    {
        return func(value);
    }

    // ============================================================
    // 8. 命名元组多返回值
    // ============================================================
    static (int Quotient, int Remainder) Divide(int a, int b)
    {
        return (a / b, a % b);
    }

    // ============================================================
    // 9. 本地函数与闭包
    // ============================================================
    static Func<int> MakeCounter(int start)
    {
        int count = start;

        // 本地函数：C# 7.0+，Python 等价：嵌套函数
        int Counter()
        {
            count++;  // 捕获外部变量 count
            return count;
        }

        return Counter;
    }

    // ============================================================
    // 11. 闭包
    // ============================================================
    static Func<int, int> CreateAdder(int baseValue)
    {
        // Lambda 捕获 baseValue（闭包）
        return x => baseValue + x;
    }

    // ============================================================
    // 12. 方法重载
    // ============================================================
    static int Multiply(int a, int b)
    {
        return a * b;
    }

    // 重载：Python 没有这个概念，同名函数会直接覆盖
    static int Multiply(int a)
    {
        return a * 2;
    }
}
