// ============================================================
// C# 继承与多态 —— 对比 Python 理解 C# 的继承体系
// 对应文章：3.3 继承与多态
// ============================================================
// 核心区别：
//   Python 支持多继承（类和接口都可以多继承）
//   C# 只支持单继承（类），多继承通过接口实现
//   Python 的方法默认可重写，C# 需要 virtual/override 显式声明
// ============================================================

using System;
using System.Collections.Generic;

// ============================================================
// 1. 单继承 & 方法重写
// ============================================================
// Python 等价：class Dog(Animal): def speak(self):

public class Animal
{
    public string Name { get; }

    public Animal(string name)
    {
        Name = name;
    }

    // virtual = 可以被子类重写
    // Python 等价：所有方法默认可重写（Python 没有 virtual 关键字）
    public virtual string Speak() => "...";

    public override string ToString() => $"{GetType().Name}(Name={Name})";
}

public class Dog : Animal
{
    public Dog(string name) : base(name) { }

    // override —— Python 等价：直接定义同名方法即可
    public override string Speak() => "汪汪！";
}

public class Cat : Animal
{
    public Cat(string name) : base(name) { }

    public override string Speak() => "喵喵！";
}

// ============================================================
// 2. 接口多继承 —— Python 多继承的 C# 等价
// ============================================================
// Python 等价：class Duck(Animal, Flyable, Swimmable)
// C# 用 interface 实现"多继承"
// C# 8+ 接口可以有 default 方法——更接近 Python 的 Mixin

public interface IFlyable
{
    void Fly();
}

public interface ISwimmable
{
    void Swim();
}

// C# 8+ 接口默认方法 —— Python Mixin 的 C# 等价
public interface ILoggable
{
    // 接口默认方法（C# 8+）—— 子类自动获得此能力
    void Log(string message)
    {
        Console.WriteLine($"  [{GetType().Name}] {message}");
    }
}

public class Duck : Animal, IFlyable, ISwimmable, ILoggable
{
    public Duck(string name) : base(name) { }

    public override string Speak() => "嘎嘎！";

    public void Fly()
    {
        Console.WriteLine("  鸭子在飞");
    }

    public void Swim()
    {
        Console.WriteLine("  鸭子在游泳");
    }
}

// ============================================================
// 3. sealed class —— 不可继承（Python 无等价机制）
// ============================================================
// Python 不限制任何继承，C# 可以用 sealed 阻止

public sealed class FinalDog : Animal
{
    public FinalDog(string name) : base(name) { }
    public override string Speak() => "我是 sealed 的汪汪！";
}

// class Puppy : FinalDog { }  // 编译错误！FinalDog 是 sealed

// ============================================================
// 4. abstract class —— 强制子类实现
// ============================================================
// Python 等价：from abc import ABC, abstractmethod

public abstract class Shape
{
    // 抽象属性 —— Python 等价：@property @abstractmethod
    public abstract double Area { get; }

    // 抽象方法 —— Python 等价：@abstractmethod
    public abstract double CalculateArea();

    // 非抽象方法 —— Python 等价：普通方法
    public void Describe()
    {
        Console.WriteLine($"  面积 = {CalculateArea():F2}");
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

public class Rectangle : Shape
{
    public double Width { get; }
    public double Height { get; }

    public Rectangle(double width, double height)
    {
        Width = width;
        Height = height;
    }

    public override double Area => CalculateArea();

    public override double CalculateArea() => Width * Height;
}

// ============================================================
// 5. 继承中的构造函数链
// ============================================================
// Python 等价：super().__init__()

public class Base
{
    public string Message { get; }

    public Base(string message)
    {
        Message = message;
        Console.WriteLine($"  Base.__init__(\"{message}\")");
    }
}

public class Derived : Base
{
    public string Extra { get; }

    public Derived(string message, string extra) : base(message)
    {
        Extra = extra;
        Console.WriteLine($"  Derived.__init__(\"{message}\", \"{extra}\")");
    }
}

// ============================================================
// 6. Main 方法 —— 运行演示
// ============================================================

public static class Program
{
    public static void Main()
    {
        // 1. 单继承 & 多态
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine("1. 单继承 & 方法重写（多态）");
        Console.WriteLine("=" + new string('=', 49));

        var dog = new Dog("旺财");
        var cat = new Cat("咪咪");
        Console.WriteLine($"dog = {dog}, Speak = {dog.Speak()}");
        Console.WriteLine($"cat = {cat}, Speak = {cat.Speak()}");

        // 多态：通过基类引用调用
        Console.WriteLine("\n多态调用:");
        Animal[] animals = { dog, cat };
        foreach (var animal in animals)
        {
            Console.WriteLine($"  {animal.Name} says: {animal.Speak()}");
        }

        // 2. 接口多继承
        Console.WriteLine();
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine("2. 接口多继承 —— Python 多继承的 C# 等价");
        Console.WriteLine("=" + new string('=', 49));

        var duck = new Duck("唐老鸭");
        Console.WriteLine($"duck = {duck}");
        Console.WriteLine($"Speak: {duck.Speak()}");
        duck.Fly();    // IFlyable
        duck.Swim();   // ISwimmable

        // 接口默认方法（C# 8+）
        Console.WriteLine("\nILoggable 接口默认方法（类似 Python Mixin）:");
        duck.Log("Hello from Duck!");

        // 接口类型检查 —— Python 等价：isinstance(obj, IFlyable)
        Console.WriteLine($"\nduck is IFlyable? {duck is IFlyable}");
        Console.WriteLine($"duck is ISwimmable? {duck is ISwimmable}");

        // 3. sealed class
        Console.WriteLine();
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine("3. sealed class —— 不可继承（Python 无等价机制）");
        Console.WriteLine("=" + new string('=', 49));

        var finalDog = new FinalDog("小黑");
        Console.WriteLine(finalDog);
        Console.WriteLine($"Speak: {finalDog.Speak()}");
        Console.WriteLine("Python 不提供 sealed 功能——任何类都可以被继承");

        // 4. abstract class
        Console.WriteLine();
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine("4. abstract class —— Python 等价：ABC + @abstractmethod");
        Console.WriteLine("=" + new string('=', 49));

        // var s = new Shape();  // 编译错误！不能实例化抽象类
        var circle = new Circle(5);
        var rect = new Rectangle(4, 6);

        Console.WriteLine($"Circle(r=5).Area = {circle.Area:F2}");
        circle.Describe();
        Console.WriteLine($"Rectangle(4,6).Area = {rect.Area:F2}");
        rect.Describe();

        // 多态：通过抽象基类统一调用
        Console.WriteLine("\n所有形状:");
        Shape[] shapes = { circle, rect };
        foreach (var s in shapes)
        {
            Console.WriteLine($"  {s.GetType().Name}: 面积 = {s.Area:F2}");
        }

        // 5. 构造函数链
        Console.WriteLine();
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine("5. 构造函数链 —— base() vs Python super().__init__()");
        Console.WriteLine("=" + new string('=', 49));

        Console.WriteLine("创建 Derived 对象时的构造函数调用链:");
        var derived = new Derived("hello", "world");
        Console.WriteLine($"derived.Message = {derived.Message}");
        Console.WriteLine($"derived.Extra = {derived.Extra}");

        // 6. 对比总结
        Console.WriteLine();
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine("6. Python vs C# 继承多态对比总结");
        Console.WriteLine("=" + new string('=', 49));
        Console.WriteLine(@"
| 概念               | C#                           | Python                      |
|--------------------|------------------------------|-----------------------------|
| 单继承             | class Dog : Animal           | class Dog(Animal)           |
| 多继承             | class D : A, IB, IC          | class D(A, B, C)            |
| 接口               | interface IFoo               | Protocol / 普通类 + Mixin   |
| 接口默认方法       | C# 8+ default method         | 普通类 + 多继承(Mixin)      |
| 调用父类           | base.Method()               | super().method()            |
| 抽象类             | abstract class Shape         | class Shape(ABC)            |
| 抽象方法           | abstract void Foo()          | @abstractmethod             |
| 方法重写           | virtual + override           | 直接定义同名方法            |
| sealed(不可继承)   | sealed class Dog             | 无等价机制                  |
| 运行时类型检查     | is / as / GetType()          | isinstance() / issubclass() |
| 多态               | 虚方法 + override            | 方法重写 + duck typing       |
| 构造函数链         | base(...)                    | super().__init__()          |
");
    }
}
