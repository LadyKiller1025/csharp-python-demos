// =============================================================================
// C# 最新特性对比 — C# 老兵的 Python 修炼手册 5.7
// 对应文章：5.7 Python 3.14新特性
// 关键概念：C# 12-14 新特性，与 Python 3.14 的对比
// =============================================================================
// 本文件展示 C# 最新版本的新特性，与 Python 3.14 进行对比
// 帮助 C# 开发者理解两种语言的演进方向
// =============================================================================

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace NewFeaturesCS
{
    // =========================================================================
    // 1. Primary Constructors (C# 12) —— 对比 Python __init__
    // =========================================================================
    // 【Python 对比】
    // Python class 自带类似语法:
    //   class Person:
    //       def __init__(self, name: str, age: int):
    //           self.name = name
    //           self.age = age
    //
    // C# 12 primary constructor 将参数直接放在类声明中

    /// <summary>
    /// C# 12 Primary Constructor
    /// 【Python 对比】Python 的 __init__ 天然就是这种模式
    /// </summary>
    public class PersonPC(string Name, int Age)
    {
        // Name 和 Age 可以在类体中使用
        public string Description => $"{Name} is {Age} years old";
    }

    /// <summary>
    /// Primary constructor + 额外逻辑
    /// 【Python 对比】Python 的 __init__ 可以包含更多逻辑
    /// </summary>
    public class EmployeePC(string Name, int Age, decimal Salary)
    {
        // 参数直接可用
        public string Level => Salary > 100000 ? "Senior" : "Junior";

        // 如果需要在构造函数中执行额外逻辑，还是需要普通构造函数
        public void Validate()
        {
            if (Age < 18) throw new ArgumentException("Must be 18+");
        }
    }

    public static class PrimaryConstructorExamples
    {
        public static void DemoPrimaryConstructors()
        {
            Console.WriteLine("\n=== 1. Primary Constructors (C# 12) ===");

            var person = new PersonPC("Alice", 25);
            Console.WriteLine($"  Person: {person.Description}");

            var emp = new EmployeePC("Bob", 30, 120000);
            Console.WriteLine($"  Employee: {emp.Name}, Level={emp.Level}");

            Console.WriteLine("  【Python 对比】");
            Console.WriteLine("  Python class 天然支持这种模式:");
            Console.WriteLine("    class PersonPC:");
            Console.WriteLine("        def __init__(self, name, age):");
            Console.WriteLine("            self.name = name");
            Console.WriteLine("            self.age = age");
        }
    }

    // =========================================================================
    // 2. Collection Expressions (C# 12) —— 更简洁的集合初始化
    // =========================================================================
    // 【Python 对比】
    // Python 列表: numbers = [1, 2, 3]
    // Python 集合: unique = {1, 2, 3}
    // Python 字典: d = {"a": 1}
    // C# 12 之前: var numbers = new List<int> { 1, 2, 3 };
    // C# 12:      List<int> numbers = [1, 2, 3];

    public static class CollectionExpressionExamples
    {
        public static void DemoCollectionExpressions()
        {
            Console.WriteLine("\n=== 2. Collection Expressions (C# 12) ===");

            // C# 12 集合表达式
            // 【Python 对比】Python 一直就是这种简洁语法
            List<int> numbers = [1, 2, 3, 4, 5];
            int[] array = [10, 20, 30];
            HashSet<string> set = ["apple", "banana", "cherry"];

            Console.WriteLine($"  List: [{string.Join(", ", numbers)}]");
            Console.WriteLine($"  Array: [{string.Join(", ", array)}]");
            Console.WriteLine($"  Set: [{string.Join(", ", set)}]");

            // Spread 运算符 ..
            // 【Python 对比】Python: [*list1, *list2]
            List<int> combined = [..numbers, ..array];
            Console.WriteLine($"  合并: [{string.Join(", ", combined)}]");

            Console.WriteLine("  【Python 对比】Python 的 [1, 2, 3] 语法一直就是这么简洁");
        }
    }

    // =========================================================================
    // 3. 原始字符串字面量 (C# 11) —— 对比 Python 三引号
    // =========================================================================
    // 【Python 对比】
    // Python: """多行字符串"""
    // C# 11: """多行字符串"""
    // 两者语法几乎一样!

    public static class RawStringExamples
    {
        public static void DemoRawStrings()
        {
            Console.WriteLine("\n=== 3. 原始字符串 (C# 11) ===");

            // Python 三引号
            // python_code = """
            //     def hello():
            //         print("Hello!")
            //     """

            // C# 11 原始字符串——语法几乎相同!
            string json = """
                {
                    "name": "Alice",
                    "age": 25,
                    "hobbies": ["reading", "coding"]
                }
                """;

            Console.WriteLine($"  JSON:\n{json}");

            // 插值
            string name = "Bob";
            string template = $"""
                {{
                    "name": "{name}",
                    "greeting": "Hello, {name}!"
                }}
                """;

            Console.WriteLine($"  模板:\n{template}");

            Console.WriteLine("  【Python 对比】Python 的 f\"\"\" 和 \"\"\" 语法几乎一样");
        }
    }

    // =========================================================================
    // 4. Pattern Matching 增强 (C# 8-12)
    // =========================================================================
    // 【Python 对比】
    // Python 3.10: match/case 模式匹配
    // C# 8-12: 持续增强的 pattern matching

    public static class PatternMatchingExamples
    {
        /// <summary>
        /// C# 12 pattern matching
        /// 【Python 对比】Python match/case
        /// </summary>
        public static string Classify(object obj)
        {
            // 类型模式 + 条件
            // 【Python 对比】case int() if value > 0:
            if (obj is int > 0 and < 100)
                return $"正小整数: {obj}";

            if (obj is string { Length: > 0 } s)
                return $"非空字符串: \"{s}\"";

            // 列表模式 (C# 11+)
            // 【Python 对比】case [first, *rest]:
            if (obj is List<int> { Count: > 0 } list)
                return $"列表: [{string.Join(", ", list)}]";

            if (obj is null)
                return "null";

            return $"其他: {obj?.GetType().Name}";
        }

        public static void DemoPatternMatching()
        {
            Console.WriteLine("\n=== 4. Pattern Matching 增强 ===");

            object[] values = { 42, "hello", new List<int> { 1, 2, 3 }, null, -5 };
            foreach (var val in values)
            {
                Console.WriteLine($"  {val?.ToString() ?? "null",25} -> {Classify(val)}");
            }

            Console.WriteLine("  【Python 对比】");
            Console.WriteLine("  Python match/case (3.10+):");
            Console.WriteLine("    match value:");
            Console.WriteLine("        case int() if 0 < value < 100:");
            Console.WriteLine("            return f'正小整数: {value}'");
        }
    }

    // =========================================================================
    // 5. 字段关键字 (C# 13 preview) —— 对比 Python @property
    // =========================================================================
    // 【Python 对比】
    // Python:
    //   class Circle:
    //       def __init__(self, radius):
    //           self.radius = radius
    //       @property
    //       def area(self):
    //           return 3.14 * self.radius ** 2
    //
    // C# 13 preview: field 关键字简化属性访问器

    /// <summary>
    /// C# 13 preview: field 关键字
    /// 注意: 这是 preview 特性，可能在最终版本中变化
    /// </summary>
    public class CircleDemo
    {
        // C# 13 preview 之前:
        private double _radius;
        public double Radius
        {
            get => _radius;
            set => _radius = value;
        }

        public double Area => 3.14 * Radius * Radius;

        // C# 13 preview 之后 (概念):
        // public double Radius { get; set; }
        // public double Area => 3.14 * field * field;  // field 代替 backing field

        // Python 对应:
        // class Circle:
        //     def __init__(self, radius: float):
        //         self.radius = radius
        //     @property
        //     def area(self) -> float:
        //         return 3.14 * self.radius ** 2
    }

    public static class FieldKeywordExamples
    {
        public static void DemoFieldKeyword()
        {
            Console.WriteLine("\n=== 5. 字段关键字 (C# 13 preview) ===");

            var circle = new CircleDemo { Radius = 5.0 };
            Console.WriteLine($"  半径: {circle.Radius}");
            Console.WriteLine($"  面积: {circle.Area}");

            Console.WriteLine("  【Python 对比】Python @property 实现类似功能:");
            Console.WriteLine("    @property");
            Console.WriteLine("    def area(self):");
            Console.WriteLine("        return 3.14 * self.radius ** 2");
        }
    }

    // =========================================================================
    // 6. async/await 持续增强
    // =========================================================================
    // 【Python 对比】Python asyncio 在 3.14 中继续优化

    public static class AsyncEnhancements
    {
        /// <summary>
        /// C# 异步增强
        /// 【Python 对比】Python asyncio 性能优化
        /// </summary>
        public static async Task DemoAsyncEnhancements()
        {
            Console.WriteLine("\n=== 6. async/await 增强 ===");

            // Task.WhenEach (C# 13) —— 逐个获取完成的任务
            // 【Python 对比】asyncio.as_completed()
            var tasks = new[]
            {
                Task.Delay(300).ContinueWith(_ => "Task 1"),
                Task.Delay(100).ContinueWith(_ => "Task 2"),
                Task.Delay(200).ContinueWith(_ => "Task 3"),
            };

            // C# 13: await foreach (var task in Task.WhenEach(tasks))
            // 逐个获取完成的任务

            // 传统方式
            await Task.WhenAll(tasks);

            Console.WriteLine("  C# 13: Task.WhenEach 逐个获取完成的任务");
            Console.WriteLine("  Python: asyncio.as_completed() 实现类似功能");

            // C# 异步流
            Console.WriteLine("  C# 8+: IAsyncEnumerable<T>");
            Console.WriteLine("  Python: async def + yield (异步生成器)");
        }
    }

    // =========================================================================
    // 7. Python 3.14 vs C# 14 完整对比
    // =========================================================================

    public static class ComparisonSummary
    {
        public static void PrintFullComparison()
        {
            Console.WriteLine("\n=== 7. Python 3.14 vs C# 14 完整对比 ===");

            Console.WriteLine("  ┌────────────────────────┬────────────────────────┬────────────────────────┐");
            Console.WriteLine("  │ Python 3.14            │ C# 14                  │ 共同趋势               │");
            Console.WriteLine("  ├────────────────────────┼────────────────────────┼────────────────────────┤");
            Console.WriteLine("  │ PEP 649 迟延注解       │ 编译时注解求值         │ 类型系统增强           │");
            Console.WriteLine("  │ t-strings 模板字符串   │ 插值字符串             │ 安全字符串构建         │");
            Console.WriteLine("  │ match/case             │ switch pattern         │ 模式匹配               │");
            Console.WriteLine("  │ type[T] 内置泛型       │ <T> 泛型               │ 泛型语法               │");
            Console.WriteLine("  │ free-threaded (实验)   │ 天然无 GIL             │ 并发能力               │");
            Console.WriteLine("  │ asyncio 持续优化       │ async/await 增强       │ 异步优先               │");
            Console.WriteLine("  │ @dataclass 增强        │ record/record struct   │ 数据类                 │");
            Console.WriteLine("  │ Protocol 增强          │ interface + default    │ 接口/协议              │");
            Console.WriteLine("  │ 无 GIL 实验            │ 天然多核               │ 并行计算               │");
            Console.WriteLine("  │ 类型系统可选增强       │ 类型系统强制增强       │ 类型安全               │");
            Console.WriteLine("  └────────────────────────┴────────────────────────┴────────────────────────┘");

            Console.WriteLine("\n  语言演进的共同趋势:");
            Console.WriteLine("  1. 类型安全 —— 两种语言都在增强类型系统");
            Console.WriteLine("  2. 模式匹配 —— 都在增强条件表达能力");
            Console.WriteLine("  3. 并发能力 —— 都在优化异步和并行");
            Console.WriteLine("  4. 简洁语法 —— 都在减少样板代码");
            Console.WriteLine("  5. 性能优化 —— 都在持续提升运行速度");
        }
    }

    // =========================================================================
    // 主程序入口
    // =========================================================================
    class Program
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine("============================================================");
            Console.WriteLine("  C# 老兵的 Python 修炼手册 — 5.7 Python 3.14 新特性");
            Console.WriteLine("  (C# 12-14 最新特性对比)");
            Console.WriteLine("============================================================");

            PrimaryConstructorExamples.DemoPrimaryConstructors();
            CollectionExpressionExamples.DemoCollectionExpressions();
            RawStringExamples.DemoRawStrings();
            PatternMatchingExamples.DemoPatternMatching();
            FieldKeywordExamples.DemoFieldKeyword();
            await AsyncEnhancements.DemoAsyncEnhancements();
            ComparisonSummary.PrintFullComparison();

            Console.WriteLine("\n============================================================");
            Console.WriteLine("  核心结论：");
            Console.WriteLine("  1. C# 12-14 持续简化语法，减少样板代码");
            Console.WriteLine("  2. Python 3.14 增强类型系统，更接近 C#");
            Console.WriteLine("  3. 两种语言在模式匹配、泛型、异步方面趋同");
            Console.WriteLine("  4. C# 仍然在性能和类型安全方面领先");
            Console.WriteLine("  5. Python 在灵活性和快速开发方面仍然有优势");
            Console.WriteLine("============================================================");
        }
    }
}
