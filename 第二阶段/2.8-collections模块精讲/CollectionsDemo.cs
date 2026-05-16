// C# 集合类示例
// 对应文章：2.8 collections模块精讲
//
// C# 老兵的 Python 修炼手册：
// Python 的 collections 是"精品集合店"，C# 的 System.Collections.Generic + ConcurrentCollections
// 是"大型超市" —— 品类更全，但 Python 的每个单品都打磨得特别好用。
// C# 的强项是类型安全和并发支持，Python 的强项是简洁和"开箱即用"。

using System;
using System.Collections.Generic;
using System.Collections.Concurrent;
using System.Collections.Specialized;
using System.Linq;

public class CollectionsDemo
{
    static void Main()
    {
        Console.WriteLine("===== collections 模块精讲（C# 对照版）=====\n");

        // ================================================================
        // 1. Counter → LINQ GroupBy + ToDictionary
        // ================================================================
        Console.WriteLine("===== 1. Counter vs LINQ GroupBy =====\n");

        // 基础计数
        Console.WriteLine("--- 1.1 基础词频统计 ---");
        var words = new[] { "apple", "banana", "apple", "cherry", "banana", "apple" };
        // Python: Counter(words)
        // C#:     需要 GroupBy + ToDictionary 三行代码...
        var wordCount = words.GroupBy(w => w)
            .OrderByDescending(g => g.Count())
            .ToDictionary(g => g.Key, g => g.Count());
        foreach (var kv in wordCount)
            Console.WriteLine($"  {kv.Key}: {kv.Value}");
        Console.WriteLine($"  最常见的: {wordCount.First().Key} ({wordCount.First().Value}次)");

        // 字符频率统计
        Console.WriteLine("\n--- 1.2 字符频率统计 ---");
        var text = "hello world";
        var charCount = text.GroupBy(c => c)
            .OrderByDescending(g => g.Count())
            .ToDictionary(g => g.Key, g => g.Count());
        Console.Write($"  字符频率: ");
        foreach (var kv in charCount)
            Console.Write($"'{kv.Key}'={kv.Count} ");
        Console.WriteLine();

        // C# 的优势：可以用 ConcurrentDictionary 在多线程下安全计数
        Console.WriteLine("\n--- 1.3 线程安全计数（C# 的优势！）---");
        Console.WriteLine("  Python 的 Counter 不是线程安全的，多线程需要用 Lock");
        Console.WriteLine("  C# 有 ConcurrentDictionary，天然支持多线程安全计数:");
        Console.WriteLine("  var counter = new ConcurrentDictionary<string, int>();");
        Console.WriteLine("  counter.AddOrUpdate(word, 1, (_, count) => count + 1);");
        Console.WriteLine("  这是 C# 比 Python 强的地方！");

        // ================================================================
        // 2. defaultdict → Dictionary + TryGetValue / GetOrAdd
        // ================================================================
        Console.WriteLine("\n===== 2. defaultdict vs Dictionary =====\n");

        Console.WriteLine("--- 2.1 按首字母分组 ---");
        // Python: groups = defaultdict(list) —— 一行搞定
        // C#:     需要手动检查 key 是否存在
        var groups = new Dictionary<char, List<string>>();
        foreach (var name in new[] { "Alice", "Bob", "Anna", "Charlie", "Bob" })
        {
            var key = name[0];
            // C# 的方式1：手动检查（和 Python 的 defaultdict 最接近）
            if (!groups.ContainsKey(key))
                groups[key] = new List<string>();
            groups[key].Add(name);

            // C# 的方式2：用 GetOrAdd（ConcurrentDictionary 也有这个方法）
            // groups.GetOrAdd(key, _ => new List<string>()).Add(name);
        }
        foreach (var kv in groups)
            Console.WriteLine($"  {kv.Key}: [{string.Join(", ", kv.Value)}]");

        // ================================================================
        // 3. deque → LinkedList / ConcurrentQueue
        // ================================================================
        Console.WriteLine("\n===== 3. deque vs LinkedList =====\n");

        Console.WriteLine("--- 3.1 基础操作 ---");
        var dq = new LinkedList<int>(new[] { 1, 2, 3 });
        dq.AddFirst(0);    // 左侧添加
        dq.AddLast(4);     // 右侧添加
        dq.RemoveFirst();  // 左侧弹出
        Console.Write("  LinkedList: ");
        foreach (var item in dq) Console.Write($"{item} ");
        Console.WriteLine();

        // 固定长度队列
        Console.WriteLine("\n--- 3.2 固定长度队列（模拟 deque(maxlen=N)）---");
        var recent = new FixedQueue<int>(3);
        for (int i = 0; i < 5; i++)
        {
            recent.Enqueue(i);
            Console.WriteLine($"  添加 {i}: [{string.Join(", ", recent)}]");
        }

        // 线程安全性对比
        Console.WriteLine("\n--- 3.3 线程安全性对比 ---");
        Console.WriteLine("  Python deque:  线程安全（append/pop 是原子操作）");
        Console.WriteLine("  C# LinkedList: 不是线程安全的！需要手动加锁");
        Console.WriteLine("  C# 替代方案:   ConcurrentQueue（仅支持尾部操作）");
        Console.WriteLine("                 ConcurrentStack（仅支持头部操作）");
        Console.WriteLine("                 要实现双端线程安全队列，需要自己封装 ConcurrentBag + 锁");
        Console.WriteLine("  Python 在这点上反而更方便！");

        // ================================================================
        // 4. OrderedDict → Dictionary（已内置保序）
        // ================================================================
        Console.WriteLine("\n===== 4. OrderedDict vs Dictionary =====\n");

        Console.WriteLine("--- 4.1 保序字典 ---");
        Console.WriteLine("  Python 3.7+ 普通 dict 已经保序");
        Console.WriteLine("  C# Dictionary<K,V> 自动保持插入顺序（.NET Core+）");
        Console.WriteLine("  额外功能需用 SortedList/KVP 按键排序");

        // 演示 C# Dictionary 的保序性
        var orderedDict = new Dictionary<string, int>();
        orderedDict["first"] = 1;
        orderedDict["second"] = 2;
        orderedDict["third"] = 3;
        Console.Write("  C# Dictionary 保序: ");
        foreach (var kv in orderedDict)
            Console.Write($"{kv.Key}={kv.Value} ");
        Console.WriteLine();

        // ================================================================
        // 5. namedtuple → record / ValueTuple
        // ================================================================
        Console.WriteLine("\n===== 5. namedtuple vs record / ValueTuple =====\n");

        Console.WriteLine("--- 5.1 基础用法 ---");
        // Python: Point = namedtuple("Point", ["x", "y"])
        // C#:     用 ValueTuple 最接近，或用 record（C# 9+）获得不可变性
        var p = (X: 3, Y: 4);
        Console.WriteLine($"  点: {p.X}, {p.Y}, 距离: {Math.Sqrt(p.X * p.X + p.Y * p.Y):F2}");

        // 用 record 模拟 namedtuple（不可变 + 值相等性）
        Console.WriteLine("\n--- 5.2 用 record 模拟（更接近 namedtuple 的语义）---");
        var point = new PointRecord(3, 4);
        var point2 = point with { X = 10 };  // 模拟 _replace()
        Console.WriteLine($"  原始点: {point}");
        Console.WriteLine($"  替换 X 后: {point2}");
        Console.WriteLine($"  原始点不变: X = {point.X}");
        Console.WriteLine($"  C# 的 with 表达式 = Python 的 _replace()，都是不可变更新！");

        // ================================================================
        // 6. ChainMap → 自定义实现 / 配置合并
        // ================================================================
        Console.WriteLine("\n===== 6. ChainMap vs 手动合并 =====\n");

        Console.WriteLine("--- 6.1 配置合并 ---");
        var defaults = new Dictionary<string, object>
        {
            ["color"] = "red", ["user"] = "guest", ["debug"] = false
        };
        var config = new Dictionary<string, object>
        {
            ["color"] = "blue", ["debug"] = true
        };
        var configMap = new ChainMapSample(defaults, config);
        Console.WriteLine($"  color: {configMap["color"]}");
        Console.WriteLine($"  user: {configMap["user"]}");

        // 模拟作用域链
        Console.WriteLine("\n--- 6.2 作用域链模拟 ---");
        var localVars = new Dictionary<string, object> { ["x"] = 10 };
        var globalVars = new Dictionary<string, object> { ["x"] = 20, ["y"] = 30 };
        var builtinVars = new Dictionary<string, object> { ["x"] = 40, ["z"] = 50 };
        var scope = new ChainMapSample(localVars, globalVars, builtinVars);
        Console.WriteLine($"  作用域查找 x: {scope["x"]}");  // 10
        Console.WriteLine($"  作用域查找 y: {scope["y"]}");  // 30
        Console.WriteLine($"  作用域查找 z: {scope["z"]}");  // 40

        // C# 中类似 ChainMap 的实现思路
        Console.WriteLine("\n--- 6.3 C# 中的替代方案 ---");
        Console.WriteLine("  C# 没有内置的 ChainMap，但可以用以下方式:");
        Console.WriteLine("  1. 手动实现（如上面的 ChainMapSample）");
        Console.WriteLine("  2. 用 Dictionary 合并: defaults.Concat(config).ToDictionary(...)");
        Console.WriteLine("  3. 用 .NET 8+ 的 FrozenDictionary 做不可变快照");
        Console.WriteLine("  Python 的 ChainMap 不复制数据，只做查找代理，更省内存！");

        Console.WriteLine("\n===== 总结: Python 的 collections 更'贴心'，C# 的更'强壮' =====");
    }
}

// record 类型（模拟 Python 的 namedtuple）
// C# 9+ 语法，自带 ToString、值相等性、不可变性
public record PointRecord(double X, double Y);

// 固定长度队列（模拟 Python deque(maxlen=N)）
// Python 的 deque 内置支持 maxlen，C# 需要自己封装
public class FixedQueue<T> : Queue<T>
{
    private readonly int _maxSize;
    public FixedQueue(int maxSize) => _maxSize = maxSize;
    public new void Enqueue(T item)
    {
        if (Count >= _maxSize) Dequeue();
        base.Enqueue(item);
    }
    public override string ToString() => string.Join(", ", this);
}

// ChainMap 简化实现（模拟 Python 的 collections.ChainMap）
// Python 的 ChainMap 支持 new_child()、maps 属性等，这里只实现核心的查找功能
public class ChainMapSample
{
    private readonly List<Dictionary<string, object>> _maps;
    public ChainMapSample(params Dictionary<string, object>[] maps)
        => _maps = maps.ToList();

    public object this[string key]
    {
        get
        {
            foreach (var map in _maps)
                if (map.ContainsKey(key))
                    return map[key];
            throw new KeyNotFoundException($"Key '{key}' not found");
        }
    }
}
