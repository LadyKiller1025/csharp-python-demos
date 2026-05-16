// ============================================================================
// C# 闭包与作用域 —— 对应 Python 闭包
// 对应文章：2.6 闭包与作用域
// ============================================================================
//
// 【C# 程序员的 Python 修炼手册】
//
// 闭包 = 内部 lambda + 它引用的外部变量
//
// C# 闭包 vs Python 闭包的核心区别：
// - C# 的 lambda 捕获变量后，编译器自动生成一个"闭包类"（Closure Class）
// - Python 在函数的 __closure__ 属性中存储被捕获的变量
// - C# 编译器会在 IL 层面将捕获的变量提升到编译器生成的类中
// - Python 更动态，运行时可以随意修改被捕获的变量（需要 nonlocal）
//
// | Python        | C#                          | 说明                       |
// |---------------|-----------------------------|----------------------------|
// | 闭包          | Lambda 捕获局部变量          | 都捕获变量引用              |
// | nonlocal      | 无直接等价（编译器自动处理）  | C# 的 lambda 可直接修改     |
// | global        | static 变量                  | 修改模块/类级别的变量       |
// | LEGB          | 作用域链                     | 查找顺序类似                |
// | __closure__   | 编译器生成的 Closure Class   | 内部实现方式不同            |
// ============================================================================

using System;
using System.Collections.Generic;
using System.Linq;

// ============================================================================
// 1. 基础闭包 —— Lambda 捕获外部变量
// ============================================================================
//
// 【Python 等价】
// def make_multiplier(factor):
//     return lambda x: x * factor
//
// C# 编译器的魔法：
// 当你写 Func<int, int> triple = MakeMultiplier(3);
// 编译器实际生成了一个隐藏类：
//   class Closure { public int factor; public int Invoke(int x) => x * factor; }
// 然后 MakeMultiplier 返回这个类的实例

static class ClosuresDemo
{
    static Func<int, int> MakeMultiplier(int factor)
    {
        // factor 被 lambda 捕获 —— C# 编译器会创建闭包类来保存它
        return x => x * factor;
    }

    // ============================================================================
    // 2. 闭包捕获变量引用（不是值）
    // ============================================================================
    //
    // 【Python 等价】
    // def make_counter():
    //     count = 0
    //     def counter():
    //         nonlocal count
    //         count += 1
    //         return count
    //     return counter
    //
    // 重要区别：
    // - Python 需要 nonlocal 关键字才能修改外部变量
    // - C# 的 lambda 可以直接修改捕获的变量（编译器自动处理）

    static Func<int> MakeCounter()
    {
        int count = 0;  // 这个变量会被"提升"到编译器生成的闭包类中

        return () =>
        {
            count++;    // C# 不需要 nonlocal，直接修改
            return count;
        };
    }

    // ============================================================================
    // 3. 循环闭包陷阱 —— C# 和 Python 共有的坑
    // ============================================================================
    //
    // 【Python 等价】
    // funcs = []
    // for i in range(5):
    //     funcs.append(lambda: i)  # 所有 lambda 捕获同一个 i
    // for f in funcs:
    //     print(f())  # 全输出 4！
    //
    // 陷阱原理：
    //   C# 和 Python 的闭包都捕获"变量的引用"而非"值"
    //   循环变量 i 在整个循环中是同一个变量
    //   所有 lambda 捕获的是同一个 i，循环结束后 i = 4（C#）或 i = 4（Python range 为 0-4）
    //
    // 【C# 特有】
    // 在 C# 5.0（.NET 4.5）之前这是一个重大 Bug，
    // 微软后来修复了 foreach 的变量捕获行为，但 for 循环仍然有这个问题！

    // ============================================================================
    // 4. 闭包作为状态机 —— 封装可变状态
    // ============================================================================
    //
    // 【Python 等价】
    // def make_accumulator(initial=0):
    //     total = initial
    //     def accumulate(value):
    //         nonlocal total
    //         total += value
    //         return total
    //     return accumulate

    /// <summary>
    /// 累加器工厂 —— 每次调用返回值累加
    /// </summary>
    static Func<int, int> MakeAccumulator(int initial = 0)
    {
        int total = initial;
        return value =>
        {
            total += value;
            return total;
        };
    }

    /// <summary>
    /// 移动平均计算器 —— 闭包封装复杂状态
    /// </summary>
    static Func<double, double> MakeMovingAverage(int windowSize)
    {
        var values = new List<double>();

        return (newValue) =>
        {
            values.Add(newValue);
            if (values.Count > windowSize)
                values.RemoveAt(0);  // 保留最近 N 个值
            return values.Average();
        };
    }

    /// <summary>
    /// 简易状态机 —— 交通灯
    /// </summary>
    static Func<string> MakeTrafficLight()
    {
        var states = new[] { "GREEN", "YELLOW", "RED" };
        int index = 0;

        return () =>
        {
            string current = states[index];
            index = (index + 1) % states.Length;
            return current;
        };
    }

    // ============================================================================
    // 5. 闭包实现私有状态（模拟 private 字段）
    // ============================================================================
    //
    // 【Python 等价】
    // def make_bank_account(owner, initial_balance=0):
    //     balance = initial_balance
    //     def deposit(amount): ...
    //     def withdraw(amount): ...
    //     return deposit, withdraw, get_balance
    //
    // C# 通常用 class + private 字段，但闭包也能做到类似效果

    static (Action<int> Deposit, Action<int> Withdraw, Func<int> GetBalance)
        MakeBankAccount(string owner, int initialBalance = 0)
    {
        int balance = initialBalance;  // 私有！外部无法直接访问

        void Deposit(int amount)
        {
            if (amount <= 0) throw new ArgumentException("存款金额必须为正");
            balance += amount;
            Console.WriteLine($"    存入 {amount}，余额: {balance}");
        }

        void Withdraw(int amount)
        {
            if (amount > balance)
                throw new InvalidOperationException($"余额不足: {balance} < {amount}");
            balance -= amount;
            Console.WriteLine($"    取出 {amount}，余额: {balance}");
        }

        int GetBalance() => balance;

        return (Deposit, Withdraw, GetBalance);
    }

    // ============================================================================
    // 主程序
    // ============================================================================

    static void Main(string[] args)
    {
        Console.WriteLine(new string('=', 70));
        Console.WriteLine("  C# 闭包与作用域演示");
        Console.WriteLine("  C# 程序员的 Python 修炼手册 —— 2.6");
        Console.WriteLine(new string('=', 70));

        // --- 1. 基础闭包 ---
        Console.WriteLine("\n--- 1. 基础闭包（Lambda 捕获外部变量）---");
        Console.WriteLine("  说明: C# 编译器会自动创建闭包类来保存被捕获的变量\n");

        var triple = MakeMultiplier(3);   // factor=3 被记住
        var double_ = MakeMultiplier(2);  // factor=2 被记住

        Console.WriteLine($"  triple(5)  = {triple(5)}");    // 15
        Console.WriteLine($"  double_(5) = {double_(5)}");   // 10
        Console.WriteLine($"  triple(10) = {triple(10)}");   // 30

        // --- 2. 闭包捕获变量引用 ---
        Console.WriteLine("\n--- 2. 闭包捕获变量引用（可直接修改，不需要 nonlocal）---");
        Console.WriteLine("  关键区别: C# lambda 可以直接修改捕获的变量");
        Console.WriteLine("  Python 则需要 nonlocal 关键字\n");

        var counter = MakeCounter();
        Console.WriteLine($"  counter() = {counter()}");  // 1
        Console.WriteLine($"  counter() = {counter()}");  // 2
        Console.WriteLine($"  counter() = {counter()}");  // 3

        var counter2 = MakeCounter();  // 独立的另一个计数器
        Console.WriteLine($"  counter2() = {counter2()}");  // 1（从 0 开始）

        // --- 3. 循环闭包陷阱 ---
        Console.WriteLine("\n--- 3. 循环闭包陷阱（C# 和 Python 共有的坑）---");
        Console.WriteLine("  陷阱: for 循环中的 lambda 捕获的是变量引用，不是值\n");

        // 陷阱重现
        Console.WriteLine("  陷阱重现:");
        var actions = new List<Action>();
        for (int i = 0; i < 5; i++)
        {
            actions.Add(() => Console.WriteLine($"    输出: {i}"));
        }
        Console.WriteLine("  期望: 0, 1, 2, 3, 4");
        Console.Write("  实际: ");
        foreach (var action in actions)
        {
            action();  // 全输出 5！
        }

        // 解决方法1: 创建局部变量（最常用）
        Console.WriteLine("\n  解决方法1: 创建局部变量（每次循环创建新的作用域）");
        var actions2 = new List<Action>();
        for (int i = 0; i < 5; i++)
        {
            int temp = i;  // 关键！创建局部副本
            actions2.Add(() => Console.WriteLine($"    输出: {temp}"));
        }
        foreach (var action in actions2)
        {
            action();  // 0, 1, 2, 3, 4
        }

        // 解决方法2: 使用 LINQ（函数式风格）
        Console.WriteLine("\n  解决方法2: 使用 LINQ（更函数式）");
        var actions3 = Enumerable.Range(0, 5)
            .Select(i => new Action(() => Console.WriteLine($"    输出: {i}")))
            .ToList();
        foreach (var action in actions3)
        {
            action();  // 0, 1, 2, 3, 4
        }

        // --- 4. 闭包作为状态机 ---
        Console.WriteLine("\n--- 4. 闭包作为状态机 ---");

        // 累加器
        Console.WriteLine("  4.1 累加器（Accumulator）:");
        var acc = MakeAccumulator();
        Console.WriteLine($"    acc(10) = {acc(10)}");   // 10
        Console.WriteLine($"    acc(20) = {acc(20)}");   // 30
        Console.WriteLine($"    acc(5)  = {acc(5)}");    // 35

        // 移动平均
        Console.WriteLine("\n  4.2 移动平均（Moving Average）:");
        var avg = MakeMovingAverage(3);  // 窗口大小 3
        Console.WriteLine($"    avg(10) = {avg(10):F2}");  // 10.00
        Console.WriteLine($"    avg(20) = {avg(20):F2}");  // 15.00
        Console.WriteLine($"    avg(30) = {avg(30):F2}");  // 20.00
        Console.WriteLine($"    avg(5)  = {avg(5):F2}");   // 18.33 (窗口: 20, 30, 5)

        // 状态机
        Console.WriteLine("\n  4.3 简易状态机（交通灯）:");
        var light = MakeTrafficLight();
        for (int i = 0; i < 6; i++)
        {
            string state = light();
            Console.WriteLine($"    当前状态: {state}");
        }

        // --- 5. 闭包实现私有状态 ---
        Console.WriteLine("\n--- 5. 闭包实现私有状态（模拟 private 字段）---");
        Console.WriteLine("  说明: Python 的闭包也能做到，C# 通常用 class + private 字段\n");

        var (deposit, withdraw, getBalance) = MakeBankAccount("Alice", 1000);
        deposit(500);                        // 存入 500，余额: 1500
        withdraw(200);                       // 取出 200，余额: 1300
        Console.WriteLine($"    查询余额: {getBalance()}");  // 1300

        // balance 变量无法从外部直接访问 —— 真正的私有！

        // --- 6. 闭包 vs 类 ---
        Console.WriteLine("\n--- 6. 闭包 vs 类 的选择指南 ---");
        Console.WriteLine("""
            +-----------+------------------------+------------------------------------+
            | 特性      | 闭包 (Lambda)          | 类 (class)                         |
            +-----------+------------------------+------------------------------------+
            | 状态      | 捕获变量（编译器处理）  | this.字段                          |
            | 隐私      | 局部变量天然私有        | 需要 private 修饰符                |
            | 代码量    | 少（一行搞定）          | 多（需要构造函数等）               |
            | 可测试性  | 差（无法单独测试内部）  | 好（方法可独立测试）               |
            | 继承      | 不支持                 | 支持                               |
            | 适用场景  | 简单回调、工厂函数      | 复杂状态管理、可测试代码           |
            +-----------+------------------------+------------------------------------+
            """);

        // --- 总结 ---
        Console.WriteLine(new string('=', 70));
        Console.WriteLine("  总结：C# 闭包 vs Python 闭包");
        Console.WriteLine(new string('-', 70));
        Console.WriteLine("  | 特性           | C#                        | Python            |");
        Console.WriteLine("  |----------------|---------------------------|-------------------|");
        Console.WriteLine("  | 捕获变量修改   | 直接修改（编译器自动处理） | 需要 nonlocal     |");
        Console.WriteLine("  | 循环陷阱       | for 循环有，foreach 无     | for 循环有        |");
        Console.WriteLine("  | 底层实现       | 编译器生成闭包类           | __closure__ 元组  |");
        Console.WriteLine("  | 闭包查看       | 无法直接查看               | func.__closure__  |");
        Console.WriteLine("  | 可变性控制     | C# 8+ 有明确限制           | 完全开放          |");
        Console.WriteLine(new string('-', 70));
        Console.WriteLine("  关键知识点:");
        Console.WriteLine("  - C# 编译器将闭包变量提升到隐藏类中");
        Console.WriteLine("  - C# lambda 可直接修改捕获变量，Python 需要 nonlocal");
        Console.WriteLine("  - 循环闭包陷阱：两者都捕获变量引用，非值的副本");
        Console.WriteLine("  - 闭包适合简单状态封装，复杂场景用类更好");
        Console.WriteLine("  - C# 的 Func<T> / Action<T> 就是函数类型的闭包载体");
        Console.WriteLine(new string('=', 70));
    }
}
