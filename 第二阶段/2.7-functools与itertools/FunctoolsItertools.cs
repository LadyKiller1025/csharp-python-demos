// C# LINQ + Func 示例
// 对应文章：2.7 functools与itertools
//
// C# 老兵的 Python 修炼手册：
// Python 的 functools + itertools 组合拳，在 C# 中主要靠 LINQ + Func 闭包来接招。
// 有些功能 C# 更强（如真正的泛型、类型安全），有些 Python 更爽（如排列组合内置支持）。

using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;

public class FunctoolsItertoolsDemo
{
    // ================================================================
    //                       functools 对应部分
    // ================================================================

    // 1. Aggregate（等价于 Python 的 reduce）
    // Python: reduce(lambda acc, x: acc + x, numbers)
    // C#:     numbers.Aggregate((acc, x) => acc + x)
    static void ReduceExample()
    {
        var numbers = new[] { 1, 2, 3, 4, 5 };
        int total = numbers.Aggregate((acc, x) => acc + x);
        int productResult = numbers.Aggregate(1, (acc, x) => acc * x);
        Console.WriteLine($"  求和: {total}");      // 15
        Console.WriteLine($"  求积: {productResult}"); // 120
    }

    // 2. Memoize（等价于 Python 的 lru_cache）
    // Python: @lru_cache(maxsize=128)
    // C#:     手动维护 Dictionary（或 .NET 8+ 的 [Memoize] 特性）
    private static Dictionary<int, long> _fibCache = new();
    static long Fibonacci(int n)
    {
        if (n < 2) return n;
        if (_fibCache.TryGetValue(n, out var cached))
            return cached;
        long result = Fibonacci(n - 1) + Fibonacci(n - 2);
        _fibCache[n] = result;
        return result;
    }

    // 3. Func 偏函数（等价于 Python 的 partial）
    // Python: square = partial(power, exponent=2)
    // C#:     var square = Power(2);  —— 用闭包实现
    static Func<int, int> Power(int exponent)
    {
        return baseValue => (int)Math.Pow(baseValue, exponent);
    }

    // 4. Concat（等价于 Python 的 chain）
    // Python: chain(list1, list2, list3)
    // C#:     list1.Cast<object>().Concat(list2.Cast<object>())...
    //         （因为 C# 是强类型的，不同类型合并需要统一类型）
    static void ChainExample()
    {
        var list1 = new[] { 1, 2, 3 };
        var list2 = new[] { "a", "b", "c" };
        var list3 = new[] { 100, 200 };
        // C# 中类型需一致，这里用 object 演示
        var combined = list1.Cast<object>()
            .Concat(list2.Cast<object>())
            .Concat(list3.Cast<object>())
            .ToList();
        Console.WriteLine($"  chain: [{string.Join(", ", combined)}]");
    }

    // 5. Take（等价于 Python 的 islice）
    // Python: islice(count(1), 5)
    // C#:     Enumerable.Range(1, 5)
    static void IsliceExample()
    {
        var firstFive = Enumerable.Range(1, 5).ToList();
        Console.WriteLine($"  前5个自然数: [{string.Join(", ", firstFive)}]");
    }

    // 6. Where + 索引（等价于 Python 的 compress）
    // Python: compress(data, mask)
    // C#:     data.Where((_, i) => mask[i])
    static void CompressExample()
    {
        var data = new[] { "A", "B", "C", "D", "E" };
        var mask = new[] { true, false, true, false, true };
        var filtered = data.Where((_, i) => mask[i]).ToList();
        Console.WriteLine($"  compress: [{string.Join(", ", filtered)}]");
    }

    // 7. GroupBy（等价于 Python 的 groupby）
    // Python: groupby(data, key=itemgetter(0)) —— 要求预排序！
    // C#:     data.GroupBy(x => x.Item1) —— 不要求预排序，更方便
    static void GroupByExample()
    {
        var data = new (string, int)[]
        {
            ("A", 1), ("A", 2), ("B", 3), ("B", 4), ("A", 5)
        };
        // C# GroupBy 不要求预排序，这是比 Python 更强的地方
        foreach (var group in data.GroupBy(x => x.Item1))
        {
            Console.WriteLine($"  组 {group.Key}: [{string.Join(", ", group)}]");
        }
    }

    // 8. Cartesian Product（等价于 Python 的 product）
    // Python: product(suits, ranks)
    // C#:     suits.SelectMany(s => ranks, (s, r) => (s, r))
    static void ProductExample()
    {
        var suits = new[] { "♠", "♥" };
        var ranks = new[] { "A", "K", "Q" };
        var cards = suits.SelectMany(s => ranks, (s, r) => $"({s},{r})").ToList();
        Console.WriteLine($"  扑克牌: [{string.Join(", ", cards)}]");
    }

    // 9. Select + 索引（等价于 Python 的 starmap）
    // Python: starmap(mul, pairs)
    // C#:     pairs.Select(p => p.Item1 * p.Item2)
    static void StarmapExample()
    {
        var pairs = new[] { (2, 3), (4, 5), (6, 7) };
        var results = pairs.Select(p => p.Item1 * p.Item2).ToList();
        Console.WriteLine($"  starmap mul: [{string.Join(", ", results)}]");
    }

    // 10. TakeWhile / SkipWhile（等价于 Python 的 takewhile / dropwhile）
    // Python: takewhile(lambda x: x < 5, numbers)
    // C#:     numbers.TakeWhile(n => n < 5)
    // Python: dropwhile(lambda x: x < 5, numbers)
    // C#:     numbers.SkipWhile(n => n < 5)
    static void TakeWhileDropWhileExample()
    {
        var numbers = new[] { 1, 3, 5, 2, 4, 6, 8 };
        var taken = numbers.TakeWhile(n => n < 5).ToList();
        var dropped = numbers.SkipWhile(n => n < 5).ToList();
        Console.WriteLine($"  原始数据: [{string.Join(", ", numbers)}]");
        Console.WriteLine($"  TakeWhile(x < 5): [{string.Join(", ", taken)}]");
        Console.WriteLine($"  SkipWhile(x < 5): [{string.Join(", ", dropped)}]");
        Console.WriteLine($"  C# 的 TakeWhile/SkipWhile 和 Python 几乎一模一样！");
    }

    // 11. Zip（等价于 Python 的 zip_longest 的简化版）
    // Python: zip_longest(names, scores, fillvalue="(缺考)")
    // C#:     names.Zip(scores, (n, s) => (n, s)) —— 默认以短的为准
    //         要实现 fillvalue 效果需要手动处理
    static void ZipLongestExample()
    {
        var names = new[] { "Alice", "Bob", "Charlie", "Diana" };
        var scores = new[] { 95, 87, 91 };
        // C# 的 Zip 默认以短的为准
        var normalZip = names.Zip(scores, (n, s) => $"({n},{s})").ToList();
        Console.WriteLine($"  普通 Zip: [{string.Join(", ", normalZip)}]");
        // 模拟 zip_longest（C# 没有内置的 zip_longest）
        var longZip = names.Select((n, i) =>
            i < scores.Length ? $"({n},{scores[i]})" : $"({n},(缺考))").ToList();
        Console.WriteLine($"  模拟 zip_longest: [{string.Join(", ", longZip)}]");
        Console.WriteLine($"  C# 没有内置的 zip_longest，需要手动处理");
    }

    // 12. 排列组合（等价于 Python 的 permutations / combinations）
    // Python: list(permutations(items, 2)) —— 内置！超方便！
    // C#:     需要自己写递归实现，或用 MoreLINQ 等第三方库
    // 这是 Python itertools 最让 C# 羡慕的功能之一！
    static List<List<T>> Permutations<T>(List<T> items, int k)
    {
        var result = new List<List<T>>();
        PermuteHelper(items, k, new HashSet<int>(), new List<T>(), result);
        return result;
    }

    static void PermuteHelper<T>(List<T> items, int k,
        HashSet<int> used, List<T> current, List<List<T>> result)
    {
        if (current.Count == k)
        {
            result.Add(new List<T>(current));
            return;
        }
        for (int i = 0; i < items.Count; i++)
        {
            if (used.Contains(i)) continue;
            used.Add(i);
            current.Add(items[i]);
            PermuteHelper(items, k, used, current, result);
            current.RemoveAt(current.Count - 1);
            used.Remove(i);
        }
    }

    static List<List<T>> Combinations<T>(List<T> items, int k)
    {
        var result = new List<List<T>>();
        CombineHelper(items, k, 0, new List<T>(), result);
        return result;
    }

    static void CombineHelper<T>(List<T> items, int k, int start,
        List<T> current, List<List<T>> result)
    {
        if (current.Count == k)
        {
            result.Add(new List<T>(current));
            return;
        }
        for (int i = start; i < items.Count; i++)
        {
            current.Add(items[i]);
            CombineHelper(items, k, i + 1, current, result);
            current.RemoveAt(current.Count - 1);
        }
    }

    static void PermutationCombinationExample()
    {
        var items = new List<string> { "A", "B", "C" };

        var perms = Permutations(items, 2);
        var permStrings = perms.Select(p => $"({string.Join(",", p)})").ToList();
        Console.WriteLine($"  permutations(ABC, 2): [{string.Join(", ", permStrings)}]");
        Console.WriteLine($"  共 {perms.Count} 种排列（顺序不同算不同）");

        var combos = Combinations(items, 2);
        var comboStrings = combos.Select(c => $"({string.Join(",", c)})").ToList();
        Console.WriteLine($"  combinations(ABC, 2): [{string.Join(", ", comboStrings)}]");
        Console.WriteLine($"  共 {combos.Count} 种组合（顺序相同算同一种）");

        var fullPerms = Permutations(items, 3);
        Console.WriteLine($"  全排列: {fullPerms.Count} = 3! 种");
        Console.WriteLine($"  C# 没有内置排列组合，需要自己写递归或用 MoreLINQ 等库");
    }

    static void Main()
    {
        Console.WriteLine("===== functools & itertools 对比 =====\n");

        Console.WriteLine("--- 1. reduce vs Aggregate ---");
        ReduceExample();

        Console.WriteLine("\n--- 2. lru_cache vs 手动缓存 ---");
        Console.WriteLine($"  fib(30) = {Fibonacci(30)}");

        Console.WriteLine("\n--- 3. partial vs Func 闭包 ---");
        var square = Power(2);
        var cube = Power(3);
        Console.WriteLine($"  平方: {square(5)}");  // 25
        Console.WriteLine($"  立方: {cube(5)}");    // 125

        Console.WriteLine("\n--- 4. chain vs Concat ---");
        ChainExample();

        Console.WriteLine("\n--- 5. islice vs Take ---");
        IsliceExample();

        Console.WriteLine("\n--- 6. compress vs Where ---");
        CompressExample();

        Console.WriteLine("\n--- 7. groupby vs GroupBy ---");
        GroupByExample();

        Console.WriteLine("\n--- 8. product vs SelectMany ---");
        ProductExample();

        Console.WriteLine("\n--- 9. starmap vs Select ---");
        StarmapExample();

        Console.WriteLine("\n--- 10. takewhile/dropwhile vs TakeWhile/SkipWhile ---");
        TakeWhileDropWhileExample();

        Console.WriteLine("\n--- 11. zip_longest vs Zip ---");
        ZipLongestExample();

        Console.WriteLine("\n--- 12. permutations/combinations vs 手写递归 ---");
        PermutationCombinationExample();

        Console.WriteLine("\n===== 总结: LINQ 已经很强了，但 Python 的排列组合真的很香！=====");
    }
}
