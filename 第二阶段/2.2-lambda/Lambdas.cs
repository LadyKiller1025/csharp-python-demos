// ============================================================
// C# Lambda 表达式示例 —— C# 老兵的 Python 修炼手册 第二阶段 2.2
// ============================================================
// 这个文件展示 C# 对应的 Lambda 用法，和 Python 版本对照学习
// Python 同学：C# 的 Lambda 比你们的 lambda 强大得多（也复杂得多）

using System;
using System.Collections.Generic;
using System.Linq;

class Lambdas
{
    static void Main(string[] args)
    {
        // ============================================================
        // 1. 基础语法：Func / Action 委托
        // ============================================================
        // Python 等价：square = lambda x: x * x
        // C# 需要先声明委托类型，Python 直接写就行
        // C# 优势：类型安全，IDE 能补全

        Console.WriteLine("=== 1. 基础语法：Func/Action ===");

        // Func<T, TResult>：有返回值的 Lambda
        Func<int, int> square = x => x * x;
        Func<int, int, int> add = (a, b) => a + b;

        Console.WriteLine($"square(5) = {square(5)}");      // 25
        Console.WriteLine($"add(3, 4) = {add(3, 4)}");      // 7

        // Action<T>：无返回值的 Lambda
        Action<string> printMsg = msg => Console.WriteLine($"  {msg}");
        printMsg("这是 Action，相当于 Python 的 lambda x: print(x)");

        // Python 写法：square = lambda x: x * x  —— 比 C# 简洁多了！
        // C# 写法：Func<int, int> square = x => x * x;
        // 结论：Python 的 lambda 是"穷人版"，C# 的 Lambda 是"满血版"


        // ============================================================
        // 2. 带代码块的 Lambda
        // ============================================================
        // Python 等价：❌ 不支持！Python lambda 只能写一个表达式
        // C# 可以在 Lambda 里写完整的代码块——这是 C# 的超能力

        Console.WriteLine("\n=== 2. 带代码块的 Lambda ===");

        Func<int, int, int> divide = (a, b) =>
        {
            if (b == 0)
                throw new DivideByZeroException("除数不能为零！");
            return a / b;
        };
        Console.WriteLine($"divide(10, 3) = {divide(10, 3)}");
        Console.WriteLine("Python lambda 不能写 if/for/try 等语句");
        Console.WriteLine("C# 的 Lambda 可以写任意复杂的代码块！");


        // ============================================================
        // 3. LINQ 中的 Lambda（Select / Where / Aggregate）
        // ============================================================
        // Python 等价：
        //   doubled = list(map(lambda x: x * 2, numbers))
        //   evens = list(filter(lambda x: x % 2 == 0, numbers))
        // C# 的 LINQ 比 Python 的 map/filter 强大得多

        Console.WriteLine("\n=== 3. LINQ 中的 Lambda ===");
        var numbers = new List<int> { 1, 2, 3, 4, 5 };

        // Select ≈ map
        var doubled = numbers.Select(x => x * 2).ToList();
        Console.WriteLine($"Select(x*2): [{string.Join(", ", doubled)}]");

        // Where ≈ filter
        var evens = numbers.Where(x => x % 2 == 0).ToList();
        Console.WriteLine($"Where(偶数): [{string.Join(", ", evens)}]");

        // Aggregate ≈ functools.reduce
        var sum = numbers.Aggregate(0, (acc, x) => acc + x);
        Console.WriteLine($"Aggregate(累加): {sum}");

        // C# LINQ 的优势：链式调用非常流畅
        var result = numbers
            .Where(x => x > 2)
            .Select(x => x * 10)
            .OrderByDescending(x => x)
            .ToList();
        Console.WriteLine($"链式调用: [{string.Join(", ", result)}]");
        Console.WriteLine("Python 要实现同样的效果需要嵌套的 map/filter，不太优雅");


        // ============================================================
        // 4. 排序中的 Lambda
        // ============================================================
        // Python 等价：sorted(users, key=lambda u: u["name"])
        // C# 需要传入 Comparer 或 Lambda 返回 int
        // Python 更简洁：指定排序键就行

        Console.WriteLine("\n=== 4. 排序中的 Lambda ===");
        var users = new List<User>
        {
            new User { Name = "张三", Age = 25 },
            new User { Name = "李四", Age = 30 },
            new User { Name = "王五", Age = 22 },
            new User { Name = "赵六", Age = 35 },
        };

        // Sort + Lambda
        var sortedByName = users.OrderBy(u => u.Name).ToList();
        Console.WriteLine("按名字排序:");
        foreach (var u in sortedByName)
            Console.WriteLine($"  {u.Name} ({u.Age}岁)");

        // 多键排序（Python 等价：key=lambda s: (-s["math"], s["english"])）
        var students = new List<Student>
        {
            new Student { Name = "张三", Math = 90, English = 85 },
            new Student { Name = "李四", Math = 85, English = 92 },
            new Student { Name = "王五", Math = 90, English = 78 },
        };

        var sortedStudents = students
            .OrderByDescending(s => s.Math)   // 数学降序
            .ThenBy(s => s.English)          // 英语升序
            .ToList();

        Console.WriteLine("\n多键排序（数学降序、英语升序）:");
        foreach (var s in sortedStudents)
            Console.WriteLine($"  {s.Name}: 数学={s.Math}, 英语={s.English}");

        // Python 等价：sorted(students, key=lambda s: (-s["math"], s["english"]))
        // C# 的 ThenBy 比 Python 的负号技巧更清晰


        // ============================================================
        // 5. Lambda 闭包
        // ============================================================
        // Python 等价：返回 lambda，捕获外部变量
        // 两个语言都支持闭包，但有细微差别：
        // Python 用 nonlocal 修改外部变量，C# 也能捕获变量引用

        Console.WriteLine("\n=== 5. Lambda 闭包 ===");

        // 乘法器
        Func<int, Func<int, int>> multiplier = factor =>
            x => x * factor;

        var triple = multiplier(3);
        var double_ = multiplier(2);
        Console.WriteLine($"triple(5) = {triple(5)}");    // 15
        Console.WriteLine($"double_(5) = {double_(5)}");  // 10

        // 累加器
        Func<int> MakeCounter()
        {
            int count = 0;
            return () => ++count;  // Lambda 捕获 count 变量
        }

        var counter = MakeCounter();
        Console.WriteLine($"counter() = {counter()}");  // 1
        Console.WriteLine($"counter() = {counter()}");  // 2
        Console.WriteLine($"counter() = {counter()}");  // 3
        Console.WriteLine("C# 和 Python 都能实现闭包——Lambda 捕获外部变量");


        // ============================================================
        // 6. Lambda 作为参数
        // ============================================================
        // Python 等价：apply(lambda x: x * 2, 5)
        // C# 需要声明 Func<T, TResult> 类型
        // Python 直接传 lambda 就行，不需要类型声明

        Console.WriteLine("\n=== 6. Lambda 作为参数 ===");

        // 自定义 Apply 方法（Python 等价：def apply(func, value): return func(value)）
        Console.WriteLine($"Apply(x => x * 2, 5) = {Apply(x => x * 2, 5)}");
        Console.WriteLine($"Apply(x => x * x, 5) = {Apply(x => x * x, 5)}");

        // 实际应用：数据转换
        var names = new List<string> { "alice", "bob", "charlie" };
        var upperNames = names.Select(n => n.ToUpper()).ToList();
        Console.WriteLine($"大写转换: [{string.Join(", ", upperNames)}]");


        // ============================================================
        // 7. 三元条件表达式
        // ============================================================
        // Python 等价：status = "成年" if age >= 18 else "未成年"
        // C# 等价：var status = age >= 18 ? "成年" : "未成年";
        // 顺序不同：C# 是 condition?true:false，Python 是 true if condition else false

        Console.WriteLine("\n=== 7. 三元条件表达式 ===");

        int age = 20;
        string status = age >= 18 ? "成年" : "未成年";
        Console.WriteLine($"年龄 {age}: {status}");

        // Lambda 中使用三元
        Func<int, string> classify = x =>
            x > 0 ? "正数" : (x == 0 ? "零" : "负数");
        Console.WriteLine($"classify(5) = {classify(5)}");
        Console.WriteLine($"classify(-3) = {classify(-3)}");
        Console.WriteLine($"classify(0) = {classify(0)}");

        Console.WriteLine("Python 写法：\"正数\" if x > 0 else (\"零\" if x == 0 else \"负数\")");
        Console.WriteLine("注意：Python 是 true if condition else false");
        Console.WriteLine("      C#    是 condition ? true : false");
        Console.WriteLine("顺序完全相反！小心别写反了！");


        // ============================================================
        // 8. 常见陷阱
        // ============================================================
        Console.WriteLine("\n=== 8. 常见陷阱 ===");
        Console.WriteLine(@"
⚠️  C# Lambda 注意事项：
  1. 循环闭包陷阱：for 中的 Lambda 捕获的是变量引用，不是值！
  2. 需要显式声明委托类型（Func/Action），Python 不需要
  3. Lambda 不能用 ref/out 参数
  4. 表达式树 Lambda（Expression<Func>）不能有代码块
  5. C# Lambda 比 Python lambda 强大得多——但别滥用
");

        // 循环闭包陷阱演示
        Console.WriteLine("循环闭包陷阱（经典面试题）:");
        var actions = new List<Action>();
        for (int i = 0; i < 5; i++)
        {
            // 错误写法：所有 Lambda 捕获的是同一个 i
            // actions.Add(() => Console.Write($"{i} "));
        }
        // 如果不注释掉，输出会是 5 5 5 5 5 而不是 0 1 2 3 4

        // 正确写法：用局部变量复制
        var correctActions = new List<Action>();
        for (int i = 0; i < 5; i++)
        {
            int copy = i;  // 关键：复制一份
            correctActions.Add(() => Console.Write($"{copy} "));
        }
        Console.Write("正确: ");
        foreach (var action in correctActions) action();
        Console.WriteLine();

        // Python 也有同样的问题：
        // actions = [lambda: print(i) for i in range(5)]  # 输出 4 4 4 4 4
        // Python 解决方案：使用默认参数 lambda i=i: print(i)


        // ============================================================
        // 总结对比
        // ============================================================
        Console.WriteLine("\n" + new string('=', 50));
        Console.WriteLine("📋 C# vs Python Lambda 速查表");
        Console.WriteLine(new string('=', 50));
        Console.WriteLine(@"
┌───────────────────────────┬──────────────────────────────┐
│          C#               │          Python              │
├───────────────────────────┼──────────────────────────────┤
│ x => x * x               │ lambda x: x * x             │
│ (x, y) => x + y          │ lambda x, y: x + y          │
│ x => { ... }             │ ❌ 不支持代码块             │
│ Func<int, int>            │ 直接赋值给变量              │
│ .Select(x => ...)        │ map(lambda x: ..., list)    │
│ .Where(x => ...)         │ filter(lambda x: ..., list) │
│ .OrderBy(x => ...)       │ sorted(key=lambda x: ...)   │
│ .Aggregate(...)          │ functools.reduce(...)       │
│ condition ? a : b        │ a if condition else b       │
│ 支持 async/await          │ ❌ 不支持                    │
│ 表达式树 Expression<>     │ ❌ 不支持                    │
│ 需要声明委托类型           │ 直接写就行                  │
└───────────────────────────┴──────────────────────────────┘
");
    }

    // ============================================================
    // 辅助方法
    // ============================================================

    /// <summary>
    /// 通用 Apply 方法——Python 等价：def apply(func, value): return func(value)
    /// C# 需要声明 Func<T, TResult> 参数类型
    /// </summary>
    static TResult Apply<T, TResult>(Func<T, TResult> func, T value)
    {
        return func(value);
    }
}

// ============================================================
// 用 record 类型定义数据结构（C# 9.0+）
// Python 等价：等价于 dataclass 或简单的 dict
// record 自动提供 ToString、Equals、GetHashCode
// ============================================================

record User
{
    public string Name { get; init; } = "";
    public int Age { get; init; }
}

record Student
{
    public string Name { get; init; } = "";
    public int Math { get; init; }
    public int English { get; init; }
}
