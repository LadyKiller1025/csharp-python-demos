// ============================================================
// C# 迭代器 vs Python 生成器
// 对应文章：2.4 生成器与迭代器
// ============================================================
// 一句话总结：C# 的 yield return ≈ Python 的 yield
// 但 Python 更简洁——一个 yield 搞定一切，
// C# 需要返回 IEnumerable<T> / IEnumerator<T>。
// 本质是同一个设计模式：用的时候才算，算完就扔，省内存！
// ============================================================

using System;
using System.Collections.Generic;
using System.Linq;

class Program
{
    // ============================================================
    // 1. 最简单的迭代器方法
    // ============================================================
    // Python 对应：
    //   def get_numbers(count):
    //       for i in range(count):
    //           yield i
    //
    // C# 的 yield return ≈ Python 的 yield
    // 区别：C# 需要声明返回类型 IEnumerable<T>，Python 不需要
    static IEnumerable<int> GetNumbers(int count)
    {
        for (int i = 0; i < count; i++)
        {
            yield return i;  // 暂停，返回值，下次从这里继续
        }
    }

    // ============================================================
    // 2. MoveNext / Current 协议（迭代器的底层原理）
    // ============================================================
    // C# 的迭代器自动实现了 IEnumerator<T> 接口：
    //   MoveNext() → 返回 bool（没有更多值时返回 false）
    //   Current     → 获取当前值
    //
    // Python 对应：__next__() 方法
    //   返回下一个值，没有更多值时抛出 StopIteration
    //
    // 本质上是同一个设计模式，只是：
    //   C#   → MoveNext() 返回 bool 表示"还有没有"
    //   Python → __next__() 抛异常表示"没了"

    // ============================================================
    // 3. 斐波那契迭代器（经典面试题）
    // ============================================================
    // Python 对应：
    //   def fibonacci(count):
    //       a, b = 0, 1
    //       for _ in range(count):
    //           yield a
    //           a, b = b, a + b
    static IEnumerable<int> Fibonacci(int count)
    {
        int a = 0, b = 1;
        for (int i = 0; i < count; i++)
        {
            yield return a;
            (a, b) = (b, a + b);  // C# 也支持元组解包了！
        }
    }

    // ============================================================
    // 4. yield break 提前结束（≈ Python 的 return）
    // ============================================================
    // Python 对应：
    //   def get_positive_numbers(numbers):
    //       for num in numbers:
    //           if num <= 0:
    //               return  # 提前结束（≈ yield break）
    //           yield num
    static IEnumerable<int> GetPositiveNumbers(int[] numbers)
    {
        foreach (var num in numbers)
        {
            if (num <= 0)
                yield break;  // 提前结束迭代（≈ Python 的 return）
            yield return num;
        }
    }

    // ============================================================
    // 5. 委托子迭代器（≈ Python 的 yield from）
    // ============================================================
    // Python 对应：
    //   def concat(first, second):
    //       yield from first
    //       yield from second
    //
    // C# 没有 yield from，需要手动 foreach 委托
    static IEnumerable<T> Concat<T>(IEnumerable<T> first, IEnumerable<T> second)
    {
        foreach (var item in first)
            yield return item;
        foreach (var item in second)
            yield return item;
    }

    // ============================================================
    // 6. Take 按需取值（≈ Python 的 islice）
    // ============================================================
    // Python 对应：list(islice(infinite_fibonacci(), 10))
    // C# 的 Take() 是 LINQ 扩展方法，功能等价
    static IEnumerable<int> InfiniteFibonacci()
    {
        int a = 0, b = 1;
        while (true)  // 无限循环！但不会撑爆内存
        {
            yield return a;
            (a, b) = (b, a + b);
        }
    }

    // ============================================================
    // 7. 迭代器管道（数据流处理）
    // ============================================================
    // Python 对应：
    //   def read_data():
    //       for i in range(20): yield i
    //   def filter_positive(data):
    //       for x in data:
    //           if x > 0: yield x
    //   def double_values(data):
    //       for x in data: yield x * 2
    //
    // C# 的 LINQ 链式调用就是管道，但用 yield return 可以手写管道
    static IEnumerable<int> ReadData()
    {
        for (int i = 0; i < 20; i++)
            yield return i;
    }

    static IEnumerable<int> FilterPositive(IEnumerable<int> data)
    {
        foreach (var x in data)
        {
            if (x > 0)
                yield return x;
        }
    }

    static IEnumerable<int> DoubleValues(IEnumerable<int> data)
    {
        foreach (var x in data)
            yield return x * 2;
    }

    static void Main()
    {
        // ============================================================
        // 1. 基础迭代器
        // ============================================================
        Console.WriteLine("=== 1. 基础迭代器 ===");
        foreach (var num in GetNumbers(5))
        {
            Console.Write($"  {num}");
        }
        Console.WriteLine();

        // ============================================================
        // 2. MoveNext / Current 手动调用
        // ============================================================
        Console.WriteLine("\n=== 2. MoveNext / Current 手动调用 ===");
        var enumerator = GetNumbers(3).GetEnumerator();
        while (enumerator.MoveNext())
        {
            Console.Write($"  {enumerator.Current}");
        }
        Console.WriteLine();
        Console.WriteLine("  （Python 对应：while True: val = next(gen)）");

        // ============================================================
        // 3. 斐波那契迭代器
        // ============================================================
        Console.WriteLine("\n=== 3. 斐波那契迭代器 ===");
        var fibList = Fibonacci(10).ToList();
        Console.WriteLine($"  前 10 个斐波那契数: [{string.Join(", ", fibList)}]");

        // ============================================================
        // 4. yield break 提前结束
        // ============================================================
        Console.WriteLine("\n=== 4. yield break 提前结束（≈ Python 的 return）===");
        var data = new[] { 3, 1, 4, -1, 5, -2, 9 };
        var positives = GetPositiveNumbers(data).ToList();
        Console.WriteLine($"  输入: [{string.Join(", ", data)}]");
        Console.WriteLine($"  输出（遇到负数就停）: [{string.Join(", ", positives)}]");

        // ============================================================
        // 5. 委托子迭代器（≈ yield from）
        // ============================================================
        Console.WriteLine("\n=== 5. 委托子迭代器（≈ Python 的 yield from）===");
        var first = new[] { 1, 2, 3 };
        var second = new[] { "a", "b", "c" };
        var concatResult = Concat(first, second.Select(c => c.GetHashCode()));
        Console.WriteLine($"  Concat([1,2,3], ['a','b','c']) 的哈希值: [{string.Join(", ", concatResult)}]");
        Console.WriteLine("  （C# 没有 yield from，需要手动 foreach 委托）");

        // ============================================================
        // 6. Take 按需取值（≈ Python 的 islice）
        // ============================================================
        Console.WriteLine("\n=== 6. Take 按需取值（≈ Python 的 islice）===");
        var fib10 = InfiniteFibonacci().Take(10).ToList();
        Console.WriteLine($"  前 10 个斐波那契数: [{string.Join(", ", fib10)}]");

        // 跳过前 10 个，取 5 个
        var fibSlice = InfiniteFibonacci().Skip(10).Take(5).ToList();
        Console.WriteLine($"  第 10~15 个斐波那契数: [{string.Join(", ", fibSlice)}]");

        // ============================================================
        // 7. 迭代器管道
        // ============================================================
        Console.WriteLine("\n=== 7. 迭代器管道 ===");
        var pipeline = DoubleValues(FilterPositive(ReadData())).Take(5).ToList();
        Console.WriteLine($"  管道结果（读取 → 过滤正数 → 翻倍 → 取前5个）: [{string.Join(", ", pipeline)}]");

        // 用 LINQ 链式调用更优雅
        var pipelineLinq = ReadData()
            .Where(x => x > 0)
            .Select(x => x * 2)
            .Take(5)
            .ToList();
        Console.WriteLine($"  LINQ 管道: [{string.Join(", ", pipelineLinq)}]");

        // ============================================================
        // 8. 延迟执行的优势
        // ============================================================
        Console.WriteLine("\n=== 8. 延迟执行的优势 ===");
        Console.WriteLine("  创建迭代器（此时还没执行任何计算！）...");
        var lazyQuery = ReadData()
            .Where(x => { Console.Write($"."); return x > 15; })
            .Select(x => x * 10);
        Console.WriteLine();
        Console.WriteLine("  开始执行（Take 会触发求值）:");
        var lazyResult = lazyQuery.Take(3).ToList();
        Console.WriteLine();
        Console.WriteLine($"  结果: [{string.Join(", ", lazyResult)}]");
        Console.WriteLine("  （只处理了必要的元素，没有遍历全部数据！）");

        // ============================================================
        // 9. 迭代器只能遍历一次！
        // ============================================================
        // Python 对应：
        //   gen = numbers()
        //   list(gen)  # [1, 2, 3]
        //   list(gen)  # []  空了！
        //
        // 但 C# 的 IEnumerable<T> 可以反复 foreach
        // （每次 foreach 都会重新调用GetEnumerator()，重新执行方法）
        // 如果是真正的 IEnumerator<T>（只调用一次GetEnumerator），也是一次性的
        Console.WriteLine("\n=== 9. 迭代器 vs 生成器的遍历差异 ===");
        var iterator = GetNumbers(3).GetEnumerator();
        var firstPass = new List<int>();
        while (iterator.MoveNext()) firstPass.Add(iterator.Current);
        Console.WriteLine($"  第一次: [{string.Join(", ", firstPass)}]");

        var secondPass = new List<int>();
        while (iterator.MoveNext()) secondPass.Add(iterator.Current);  // 空了！
        Console.WriteLine($"  第二次: [{string.Join(", ", secondPass)}] （IEnumerator 用完就没了！）");

        Console.WriteLine("  但 IEnumerable 可以反复遍历（每次重新创建）:");
        var list1 = GetNumbers(3).ToList();
        var list2 = GetNumbers(3).ToList();
        Console.WriteLine($"  第一次: [{string.Join(", ", list1)}]");
        Console.WriteLine($"  第二次: [{string.Join(", ", list2)}]");

        // ============================================================
        // 10. 没有直接对应的部分
        // ============================================================
        Console.WriteLine("\n=== 10. C# 没有对应的部分 ===");
        Console.WriteLine("  Python 的 send() 方法——向生成器发送值");
        Console.WriteLine("  （C# 需要 Rx.NET 或自己实现状态机来模拟）");
        Console.WriteLine("  Python 的生成器表达式：(x**2 for x in range(10))");
        Console.WriteLine("  （C# 对应：Enumerable.Range(0,10).Select(x => x*x)）");

        // ============================================================
        Console.WriteLine();
        Console.WriteLine("=== 迭代器 vs 生成器 演示完成！===");
        Console.WriteLine("记住：C# 的 yield return 虽然啰嗦一点，但思路跟 Python 生成器完全一样！");
        Console.WriteLine("yield 是懒加载的灵魂，用好了能省大量内存！");
    }
}
