// ============================================================
// C# LINQ vs Python 列表推导式
// 对应文章：2.3 列表推导式 vs LINQ
// ============================================================
// 一句话总结：C# 的 LINQ ≈ Python 的列表推导式
// 但 C# 版更类型安全，Python 版更简洁。
// 你推导式用得溜，LINQ 就无师自通！
// ============================================================

using System;
using System.Collections.Generic;
using System.Linq;

class Program
{
    static void Main()
    {
        var numbers = new List<int> { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };

        // ============================================================
        // 1. 基础：筛选 + 转换
        // ============================================================
        // Python 对应：[x for x in numbers if x % 2 == 0]
        var evens = numbers.Where(x => x % 2 == 0).ToList();
        Console.WriteLine($"筛选偶数: [{string.Join(", ", evens)}]");

        // Python 对应：[x * 2 for x in numbers]
        var doubled = numbers.Select(x => x * 2).ToList();
        Console.WriteLine($"全部翻倍: [{string.Join(", ", doubled)}]");

        // Python 对应：[x * 2 for x in numbers if x > 3]
        // 即 filter + transform 一步到位
        var filteredTransformed = numbers
            .Where(x => x > 3)
            .Select(x => x * 2)
            .ToList();
        Console.WriteLine($"筛选 > 3 再翻倍: [{string.Join(", ", filteredTransformed)}]");

        // ============================================================
        // 2. 三元运算符在 LINQ 中
        // ============================================================
        // Python 对应：[x * 2 if x > 3 else x for x in numbers]
        // 注意：Python 用 if-else（顺序不同！），C# 用 ? :
        var resultIfElse = numbers
            .Select(x => x > 3 ? x * 2 : x)
            .ToList();
        Console.WriteLine($"三元运算符: [{string.Join(", ", resultIfElse)}]");

        // 奇偶标记
        // Python 对应：["偶" if x % 2 == 0 else "奇" for x in numbers]
        var labels = numbers
            .Select(x => x % 2 == 0 ? "偶" : "奇")
            .ToList();
        Console.WriteLine($"奇偶标记: [{string.Join(", ", labels)}]");

        // ============================================================
        // 3. 排序
        // ============================================================
        // Python 对应：sorted(numbers, reverse=True)
        var sortedDesc = numbers.OrderByDescending(x => x).ToList();
        Console.WriteLine($"降序排序: [{string.Join(", ", sortedDesc)}]");

        // 按自定义规则排序
        // Python 对应：sorted(numbers, key=lambda x: x % 10)
        var sortedCustom = numbers.OrderBy(x => x % 10).ToList();
        Console.WriteLine($"按个位数排序: [{string.Join(", ", sortedCustom)}]");

        // ============================================================
        // 4. 聚合操作
        // ============================================================
        // Python 对应：sum(numbers) / len(numbers) / min(numbers) / max(numbers)
        var total = numbers.Sum();
        var avg = numbers.Average();
        var minVal = numbers.Min();
        var maxVal = numbers.Max();
        Console.WriteLine($"求和: {total}, 平均值: {avg}, 最小: {minVal}, 最大: {maxVal}");

        // Python 对应：functools.reduce(lambda acc, x: acc * x, numbers)
        var product = numbers.Aggregate((acc, x) => acc * x);
        Console.WriteLine($"累乘: {product}");

        // ============================================================
        // 5. 链式操作（LINQ 的精髓）
        // ============================================================
        // Python 对应：sorted([x * 2 for x in numbers if x > 3])
        // C# 的链式调用从上往下读，Python 推导式从右往左读——方向不同，效果相同！
        var result = numbers
            .Where(x => x > 3)
            .Select(x => x * 2)
            .OrderBy(x => x)
            .ToList();
        Console.WriteLine($"链式操作（筛选 > 3 → 翻倍 → 排序）: [{string.Join(", ", result)}]");

        // ============================================================
        // 6. GroupBy 分组
        // ============================================================
        // Python 没有直接的 GroupBy 推导式，需要用 dict + 推导式模拟：
        //   {k: [x for x in numbers if f(x) == k] for k in set(f(x) for x in numbers)}
        // C# 的 GroupBy 是内置的，这是 LINQ 比推导式强的地方！
        var groups = numbers
            .GroupBy(x => x % 2)
            .Select(g => new { Key = g.Key, Items = g.ToList() })
            .ToList();
        foreach (var g in groups)
        {
            Console.WriteLine($"  分组 Key={g.Key}: [{string.Join(", ", g.Items)}]");
        }

        // ============================================================
        // 7. 字典
        // ============================================================
        // Python 对应：{x: x ** 2 for x in numbers}
        var squareDict = numbers.ToDictionary(x => x, x => x * x);
        Console.WriteLine($"字典推导: {{{string.Join(", ", squareDict.Select(kvp => $"{kvp.Key}: {kvp.Value}"))}}}");

        // 带条件的字典
        var evenDict = numbers
            .Where(x => x % 2 == 0)
            .ToDictionary(x => x, x => x * x);
        Console.WriteLine($"偶数的平方字典: {{{string.Join(", ", evenDict.Select(kvp => $"{kvp.Key}: {kvp.Value}"))}}}");

        // ============================================================
        // 8. 笛卡尔积（SelectMany）
        // ============================================================
        // Python 对应：[(c, s) for c in colors for s in sizes]
        // SelectMany 就是 Python 推导式里嵌套两个 for 的效果
        var colors = new[] { "红", "蓝", "绿" };
        var sizes = new[] { "S", "M", "L" };
        var combinations = colors
            .SelectMany(c => sizes, (c, s) => $"({c}, {s})")
            .ToList();
        Console.WriteLine($"笛卡尔积: [{string.Join(", ", combinations)}]");
        Console.WriteLine($"组合数: {combinations.Count} (3 颜色 × 3 尺码)");

        // ============================================================
        // 9. SelectMany 展平（Flatten）
        // ============================================================
        // Python 对应：[x for row in matrix for x in row]
        var matrix = new List<List<int>>
        {
            new List<int> { 1, 2, 3 },
            new List<int> { 4, 5, 6 },
            new List<int> { 7, 8, 9 }
        };
        var flattened = matrix.SelectMany(row => row).ToList();
        Console.WriteLine($"矩阵展平: [{string.Join(", ", flattened)}]");

        // 每行最大值
        // Python 对应：[max(row) for row in matrix]
        var rowMaxes = matrix.Select(row => row.Max()).ToList();
        Console.WriteLine($"每行最大值: [{string.Join(", ", rowMaxes)}]");

        // 对角线元素（C# 比 Python 更啰嗦，但更类型安全）
        // Python 对应：[matrix[i][i] for i in range(len(matrix))]
        var diagonal = matrix.Select((row, i) => row[i]).ToList();
        Console.WriteLine($"对角线元素: [{string.Join(", ", diagonal)}]");

        // ============================================================
        // 10. 延迟求值（IEnumerable 的惰性特性）
        // ============================================================
        // Python 对应：(x ** 2 for x in numbers)  —— 生成器表达式
        // C# 的 IEnumerable 默认就是惰性的，Python 需要用 () 圆括号
        var squaresLazy = numbers.Select(x => x * x);  // 此时还没计算！
        Console.WriteLine("延迟求值：以下调用时才真正计算...");
        foreach (var sq in squaresLazy)
        {
            Console.Write($"{sq} ");
        }
        Console.WriteLine();

        // ============================================================
        // 11. 没有直接对应的部分
        // ============================================================
        // Python 的海象运算符 := 没有 C# 对应
        // 最接近的方式是用匿名类型
        // Python: [y := x**2 for x in range(10) if y > 10]
        var walrusEquivalent = Enumerable.Range(0, 10)
            .Select(x => new { x, y = x * x })
            .Where(obj => obj.y > 10)
            .Select(obj => obj.y)
            .ToList();
        Console.WriteLine($"模拟海象运算符: [{string.Join(", ", walrusEquivalent)}]");

        // 用 None 过滤
        // Python 对应：[x for x in data if x is not None]
        // C# 的 null 对应 Python 的 None
        var data = new List<int?> { 1, null, 3, null, 5, null, 7 };
        var cleaned = data.Where(x => x.HasValue).Select(x => x.Value).ToList();
        Console.WriteLine($"过滤 null: [{string.Join(", ", cleaned)}]");

        // ============================================================
        Console.WriteLine();
        Console.WriteLine("=== LINQ vs 列表推导式 演示完成！===");
        Console.WriteLine("记住：C# 追求类型安全，Python 追求简洁。");
        Console.WriteLine("两种风格各有千秋，关键是选对场景！");
    }
}
