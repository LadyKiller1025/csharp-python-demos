// C# 接口示例
// 对应文章：3.4 鸭子类型 vs 接口
// 对比 Python 的鸭子类型 —— C# 必须显式声明接口

using System;
using System.Collections;
using System.Collections.Generic;

// ========== 1. 接口定义：Python 不需要，C# 必须声明 ==========
// C# 等价：Python 的鸭子类型（只要有 speak 方法就行）

public interface ISpeakable
{
    string Speak();
}

// 类必须显式实现接口
public class Dog : ISpeakable
{
    public string Speak() => "汪汪！";
}

public class Cat : ISpeakable
{
    public string Speak() => "喵喵！";
}

// 方法参数必须声明接口类型
// Python 等价：def make_speak(animal): animal.speak()
public static void MakeSpeak(ISpeakable animal)
{
    Console.WriteLine(animal.Speak());
}

// ========== 2. IEnumerable：Python 的 __iter__ / __next__ ==========
// Python 等价：class CountDown: __iter__ + __next__

public class CountDown : IEnumerable<int>
{
    private readonly int _start;

    public CountDown(int start)
    {
        _start = start;
    }

    // Python 等价：def __iter__(self): return self
    public IEnumerator<int> GetEnumerator()
    {
        for (int i = _start; i > 0; i--)
        {
            // Python 等价：yield return i（类似 Python 的 yield i）
            yield return i;
        }
    }

    // Python 没有非泛型版本的等价物
    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}

// ========== 3. IDisposable：Python 的 __enter__ / __exit__ ==========
// Python 等价：with MyResource() as r: ...

public class MyResource : IDisposable
{
    public string Name { get; }

    public MyResource(string name)
    {
        Name = name;
        Console.WriteLine($"  [获取资源] {Name}");
    }

    // Python 等价：def __enter__(self): return self
    // C# 在 using 语句声明时自动调用构造函数（等价于 __enter__）

    // Python 等价：def __exit__(self, ...): ...
    public void Dispose()
    {
        Console.WriteLine($"  [释放资源] {Name}");
    }
}

// ========== 4. IComparable：Python 的 __lt__ ==========
// Python 等价：class Person: def __lt__(self, other): return self.age < other.age

public class Person : IComparable<Person>
{
    public string Name { get; }
    public int Age { get; }

    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }

    // Python 等价：def __lt__(self, other): return self.age < other.age
    public int CompareTo(Person? other)
    {
        if (other is null) return 1;
        return Age.CompareTo(other.Age);
    }

    public override string ToString() => $"{Name}({Age})";
}

public class Program
{
    static void Main()
    {
        Console.WriteLine("===== 3.4 鸭子类型 vs 接口 =====\n");

        // 1. 接口调用
        Console.WriteLine("--- 1. 接口调用 ---");
        // Python 等价：make_speak(Dog())
        MakeSpeak(new Dog());   // OK
        MakeSpeak(new Cat());   // OK
        // MakeSpeak("hello");  // 编译错误！string 没有实现 ISpeakable

        // 2. IEnumerable 迭代器
        Console.WriteLine("\n--- 2. IEnumerable 迭代器 ---");
        // Python 等价：for x in CountDown(5)
        var countdown = new List<int>();
        foreach (var n in new CountDown(5))
        {
            countdown.Add(n);
        }
        Console.WriteLine($"CountDown(5): [{string.Join(", ", countdown)}]");

        // 3. IDisposable 上下文管理
        Console.WriteLine("\n--- 3. IDisposable 上下文管理 ---");
        // Python 等价：with MyResource("数据库连接") as r:
        using (var resource = new MyResource("数据库连接"))
        {
            Console.WriteLine($"  [使用资源] {resource.Name} —— 执行业务逻辑");
        }
        // Python 的 __exit__ 会被自动调用（等价于 Dispose()）

        Console.WriteLine("\n嵌套 using:");
        using var outer = new MyResource("外层文件");
        using var inner = new MyResource("内层文件");
        Console.WriteLine($"  [使用] {outer.Name} + {inner.Name}");

        // 4. IComparable 排序
        Console.WriteLine("\n--- 4. IComparable 排序 ---");
        // Python 等价：people.sort() 使用 __lt__
        var people = new List<Person>
        {
            new Person("Bob", 30),
            new Person("Alice", 25),
            new Person("Charlie", 20)
        };
        people.Sort();  // 使用 IComparable<Person>.CompareTo
        Console.WriteLine($"按年龄排序: [{string.Join(", ", people)}]");

        people.Sort((a, b) => b.Age.CompareTo(a.Age));  // 逆序
        Console.WriteLine($"逆序排序:   [{string.Join(", ", people)}]");

        // 5. 总结
        Console.WriteLine("\n--- 5. C# vs Python 鸭子类型总结 ---");
        Console.WriteLine("  | 概念         | C#                    | Python                |");
        Console.WriteLine("  |--------------|-----------------------|-----------------------|");
        Console.WriteLine("  | 接口约束     | interface ISpeakable  | Protocol (可选)       |");
        Console.WriteLine("  | 迭代器       | IEnumerable<T>        | __iter__ + __next__   |");
        Console.WriteLine("  | 上下文管理   | IDisposable + using   | __enter__ + __exit__  |");
        Console.WriteLine("  | 排序         | IComparable<T>        | __lt__                |");
    }
}
