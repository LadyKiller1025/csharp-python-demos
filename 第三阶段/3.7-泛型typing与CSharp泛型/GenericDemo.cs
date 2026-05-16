// C# 泛型示例
// 对应文章：3.7 泛型typing与CSharp泛型

using System;
using System.Collections.Generic;
using System.Linq;

public class GenericDemo
{
    // 1. 泛型类
    public class Stack<T>
    {
        private readonly List<T> _items = new();

        public void Push(T item) => _items.Add(item);

        public T Pop()
        {
            if (_items.Count == 0)
                throw new InvalidOperationException("栈为空");
            var item = _items[^1];
            _items.RemoveAt(_items.Count - 1);
            return item;
        }

        public T Peek() => _items[^1];
        public bool IsEmpty => _items.Count == 0;
        public int Count => _items.Count;
    }

    // 2. 泛型函数
    static T? First<T>(List<T> items) where T : class
        => items.FirstOrDefault();

    static Dictionary<K, V> Merge<K, V>(Dictionary<K, V> d1, Dictionary<K, V> d2)
    {
        var result = new Dictionary<K, V>(d1);
        foreach (var kv in d2) result[kv.Key] = kv.Value;
        return result;
    }

    // 3. 类型约束
    static T Add<T>(T a, T b) where T : INumber<T>
        => a + b;

    // 接口约束示例
    public interface IRepository<T> where T : class
    {
        void Add(T item);
        List<T> GetAll();
        T? Find(Func<T, bool> predicate);
    }

    // 4. 实际场景：泛型仓储
    public record User(int Id, string Name);
    public record Product(int Id, string Title, decimal Price);

    public class Repository<T> : IRepository<T> where T : class
    {
        private readonly List<T> _items = new();

        public void Add(T item) => _items.Add(item);
        public List<T> GetAll() => _items.ToList();
        public T? Find(Func<T, bool> predicate) => _items.FirstOrDefault(predicate);
    }

    static void Main()
    {
        Console.WriteLine("===== 泛型：typing.Generic vs C# 泛型 =====\n");

        // 1. 泛型栈
        Console.WriteLine("--- 1. 泛型栈 ---");
        var intStack = new Stack<int>();
        intStack.Push(1);
        intStack.Push(2);
        Console.WriteLine($"整数栈弹出: {intStack.Pop()}");

        var strStack = new Stack<string>();
        strStack.Push("hello");
        Console.WriteLine($"字符串栈弹出: {strStack.Pop()}");

        // 2. 泛型函数
        Console.WriteLine("\n--- 2. 泛型函数 ---");
        var nums = new List<int> { 1, 2, 3 };
        Console.WriteLine($"first: {First(nums)}");

        var d1 = new Dictionary<string, int> { ["a"] = 1 };
        var d2 = new Dictionary<string, int> { ["b"] = 2 };
        var merged = Merge(d1, d2);
        Console.WriteLine($"merge: {string.Join(", ", merged.Select(kv => $"{kv.Key}:{kv.Value}"))}");

        // 3. 泛型仓储
        Console.WriteLine("\n--- 3. 泛型仓储 ---");
        var userRepo = new Repository<User>();
        userRepo.Add(new User(1, "Alice"));
        userRepo.Add(new User(2, "Bob"));

        var productRepo = new Repository<Product>();
        productRepo.Add(new Product(1, "Laptop", 999.99m));

        var user = userRepo.Find(u => u.Name == "Alice");
        Console.WriteLine($"用户: {user}");

        var product = productRepo.Find(p => p.Price > 500);
        Console.WriteLine($"商品: {product}");
    }
}
