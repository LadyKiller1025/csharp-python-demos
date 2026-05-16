// ============================================================
// C# 访问修饰符 —— 对比 Python 理解 C# 的访问控制
// 对应文章：3.2 访问修饰符
// ============================================================
// 核心区别：C# 有语法级别的访问控制（编译器强制执行），
// Python 完全靠命名约定（"we are all consenting adults"）。
// ============================================================

using System;

// ============================================================
// 1. 基本访问修饰符
// ============================================================
// Python 等价：无前缀 = public, _ = protected(约定), __ = name mangling

public class Person
{
    // public —— Python 等价：无前缀 self.name
    public string Name { get; set; }

    // private —— Python 等价：__ 前缀（仅靠约定，不强制）
    private int _age;

    // protected —— Python 等价：_ 前缀（仅靠约定）
    protected string Secret;

    // internal —— Python 等价：__all__ 控制模块导入
    internal string InternalNote = "internal data";

    public Person(string name, int age)
    {
        Name = name;
        _age = age;
        Secret = "hidden";
    }

    // private 方法 —— Python 等价：__method()
    private int GetAge()
    {
        return _age;
    }

    // protected 方法 —— Python 等价：_method()
    protected void RevealSecret()
    {
        Console.WriteLine($"  Secret: {Secret}");
    }

    // public 方法调用 private 和 protected
    public void ShowInfo()
    {
        Console.WriteLine($"  Name={Name}, Age={GetAge()}");  // 可以调用 private
        RevealSecret();  // 可以调用 protected
        Console.WriteLine($"  Internal: {InternalNote}");
    }
}

// ============================================================
// 2. 只读属性（C# 的受控访问）
// ============================================================
// Python 等价：@property 只有 getter

public class BankAccount
{
    public string Owner { get; }
    public decimal Balance { get; private set; }  // 只有类内部能 set

    public BankAccount(string owner, decimal initialBalance)
    {
        Owner = owner;
        Balance = initialBalance;
    }

    public void Deposit(decimal amount)
    {
        if (amount <= 0)
            throw new ArgumentException("存款金额必须为正");
        Balance += amount;
        Console.WriteLine($"  存入 {amount}，余额 {Balance}");
    }

    public void Withdraw(decimal amount)
    {
        if (amount <= 0)
            throw new ArgumentException("取款金额必须为正");
        if (amount > Balance)
            throw new InvalidOperationException("余额不足");
        Balance -= amount;
        Console.WriteLine($"  取出 {amount}，余额 {Balance}");
    }
}

// ============================================================
// 3. sealed class —— 不可继承
// ============================================================
// Python 没有等价机制（Python 不限制继承）
// C# 用 sealed 阻止继承，常用于安全/性能优化

public sealed class FinalClass
{
    public string Message { get; } = "我是 sealed 类，不能被继承";

    public override string ToString() => $"FinalClass({Message})";
}

// sealed class 用于子类——标记不允许再被继承
public class Animal
{
    public virtual string Speak() => "...";
}

public sealed class Dog : Animal   // sealed：不能再有子类继承 Dog
{
    public override string Speak() => "汪汪！";
}

// class Puppy : Dog { }  // 编译错误！Dog 是 sealed

// ============================================================
// 4. abstract class —— 不能实例化，必须被继承
// ============================================================
// Python 等价：from abc import ABC, abstractmethod

public abstract class Shape
{
    public abstract double Area { get; }          // 抽象属性
    public abstract double CalculateArea();       // 抽象方法

    // 非抽象方法——可以有实现
    public void Describe()
    {
        Console.WriteLine($"  面积是 {CalculateArea():F2}");
    }
}

public class Circle : Shape
{
    public double Radius { get; }

    public Circle(double radius) => Radius = radius;

    public override double Area => CalculateArea();

    public override double CalculateArea()
        => Math.PI * Radius * Radius;
}

// ============================================================
// 5. Main 方法 —— 运行演示
// ============================================================

public static class Program
{
    public static void Main()
    {
        // 1. 基本访问修饰符
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine("1. C# 四种访问修饰符");
        Console.WriteLine("=" + new string('=', 49));

        var p = new Person("Alice", 25);
        Console.WriteLine($"public:  p.Name = {p.Name}");
        // Console.WriteLine(p._age);      // 编译错误！private
        // Console.WriteLine(p.Secret);     // 编译错误！protected
        Console.WriteLine($"internal: p.InternalNote = {p.InternalNote}");

        Console.WriteLine("通过 public 方法访问所有成员:");
        p.ShowInfo();

        Console.WriteLine("\n对比 Python: C# 编译器强制检查，Python 运行时才报错");
        Console.WriteLine("  C#:  private x;   -> 直接访问 -> 编译错误");
        Console.WriteLine("  Py:  self.__x     -> 直接访问 -> AttributeError (运行时)");

        // 2. 只读 / private set
        Console.WriteLine();
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine("2. private set —— Python @property setter 等价");
        Console.WriteLine("=" + new string('=', 49));

        var account = new BankAccount("Alice", 1000);
        Console.WriteLine($"户主: {account.Owner}");
        Console.WriteLine($"余额: {account.Balance}");
        account.Deposit(500);
        account.Withdraw(200);
        Console.WriteLine($"最终余额: {account.Balance}");
        // account.Balance = -100;  // 编译错误！private set
        // 对比 Python: 可以 account._BankAccount__balance = 99999（绕过保护）

        // 3. sealed class
        Console.WriteLine();
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine("3. sealed class —— 不可继承（Python 无等价机制）");
        Console.WriteLine("=" + new string('=', 49));

        var final = new FinalClass();
        Console.WriteLine(final);
        Console.WriteLine("C# sealed vs Java final class vs Python: 无限制");

        var dog = new Dog();
        Console.WriteLine($"Dog.Speak() = {dog.Speak()}");
        Console.WriteLine("Dog 被 sealed，不能再有子类");

        // 4. abstract class
        Console.WriteLine();
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine("4. abstract class —— Python 等价：ABC + @abstractmethod");
        Console.WriteLine("=" + new string('=', 49));

        // var s = new Shape();  // 编译错误！不能实例化抽象类
        var circle = new Circle(5);
        Console.WriteLine($"Circle(radius={circle.Radius})");
        circle.Describe();

        // 5. 对比总结
        Console.WriteLine();
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine("5. Python vs C# 访问控制对比总结");
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine(@"
| 概念           | C#            | Python                  |
|----------------|---------------|-------------------------|
| 公开           | public        | 无前缀                  |
| 私有           | private       | __ 前缀（约定）         |
| 受保护         | protected     | _ 前缀（约定）          |
| 程序集内部     | internal      | __all__ 控制模块导入    |
| 强制执行       | 编译器检查    | 运行时才会报错          |
| 只读属性       | { get; }      | @property 只有 getter   |
| 带验证的 set   | private set   | @property setter        |
| 不可继承       | sealed class  | 无（Python 不限制继承） |
| 抽象类         | abstract      | ABC + @abstractmethod   |
");
    }
}
