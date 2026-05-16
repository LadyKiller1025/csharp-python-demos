// =============================================================================
// C# 类型系统示例 — C# 老兵的 Python 修炼手册 5.3
// 对应文章：5.3 类型提示
// 关键概念：nullable reference types, pattern matching,
//           record, init-only, generic constraints
// =============================================================================
// 【C# vs Python 对比】
// C# 是静态类型语言，编译时强制类型检查
// Python 是动态类型语言，类型提示是可选的
// C# 的类型系统远比 Python 强大和安全
// =============================================================================

using System;
using System.Collections.Generic;
using System.Diagnostics.CodeAnalysis;

namespace TypeHintsDemo
{
    // =========================================================================
    // 1. 基础类型声明
    // =========================================================================
    // 【Python 对比】
    // Python: name: str = "Alice"   (可选的类型提示)
    // C#:     string name = "Alice" (强制的类型声明)

    public static class BasicTypeExamples
    {
        /// <summary>
        /// C# 是强类型语言——每个变量必须声明类型
        /// 【Python 对比】Python 可以不写类型，但建议写
        /// </summary>
        public static void DemoBasicTypes()
        {
            Console.WriteLine("\n=== 1. 基础类型声明 ===");

            // C# 值类型（存储在栈上）
            int age = 25;              // Python: age: int = 25
            double price = 9.99;       // Python: price: float = 9.99
            bool isActive = true;      // Python: is_active: bool = True
            char grade = 'A';          // Python: 没有 char，用 str

            // C# 引用类型（存储在堆上）
            string name = "Alice";     // Python: name: str = "Alice"

            // C# 特有: 精确数值类型
            decimal money = 19.99m;    // Python 没有 decimal 字面类型
            long bigNumber = 1_000_000_000L;

            Console.WriteLine($"  int: {age}");
            Console.WriteLine($"  double: {price}");
            Console.WriteLine($"  bool: {isActive}");
            Console.WriteLine($"  string: {name}");
            Console.WriteLine($"  decimal: {money}");

            // 类型推断 var —— 类似 Python 的动态类型但编译时确定
            // 【Python 对比】Python 始终是动态类型
            var inferred = 42;        // 编译器推断为 int
            var message = "hello";    // 编译器推断为 string
            Console.WriteLine($"  var inferred: {inferred.GetType().Name}");
            Console.WriteLine($"  var message: {message.GetType().Name}");
        }

        /// <summary>
        /// 方法签名必须有类型声明
        /// 【Python 对比】def add(a: int, b: int) -> int: (可选)
        /// </summary>
        public static int Add(int a, int b) => a + b;
        // Python: def add(a: int, b: int) -> int: return a + b
    }

    // =========================================================================
    // 2. Nullable Reference Types —— 对比 Python 的 Optional
    // =========================================================================
    // 【Python 对比】
    // Python: name: Optional[str] = None
    // C#:     string? name = null;  (C# 8+ nullable reference types)
    //
    // 两者概念相似，但 C# 编译器会检查 null 使用

    public static class NullableExamples
    {
        /// <summary>
        /// 演示 nullable 类型
        /// </summary>
        public static void DemoNullableTypes()
        {
            Console.WriteLine("\n=== 2. Nullable 类型（对比 Python Optional） ===");

            // 可空值类型
            int? nullableInt = null;       // Python: x: int | None = None
            double? nullableDouble = 3.14;

            // 可空引用类型 (C# 8+)
            string? nullableString = null;  // Python: name: Optional[str] = null
            string nonNullString = "hello";

            Console.WriteLine($"  int?: {nullableInt?.ToString() ?? "null"}");
            Console.WriteLine($"  string?: {nullableString ?? "null"}");
            Console.WriteLine($"  string: {nonNullString}");

            // 空合并运算符 ?? —— Python 没有直接对应
            // 【Python 对比】name or "default" (不完全一样，0 也是 falsy)
            string result = nullableString ?? "默认值";
            Console.WriteLine($"  ?? 运算符: {result}");

            // 空条件运算符 ?. —— Python 没有直接对应
            // 【Python 对比】需要 if obj: obj.method()
            int? length = nullableString?.Length;
            Console.WriteLine($"  ?. 运算符: {length?.ToString() ?? "null"}");
        }
    }

    // =========================================================================
    // 3. Pattern Matching —— 对比 Python 的 TypeGuard/isinstance
    // =========================================================================
    // 【Python 对比】
    // Python: if isinstance(x, int): ... (运行时检查)
    // C#:     if (x is int n) { ... } (编译时优化 + 运行时检查)
    //
    // C# pattern matching 远比 Python 的 isinstance 强大

    public static class PatternMatchingExamples
    {
        /// <summary>
        /// 演示 pattern matching
        /// 【Python 对比】isinstance + TypeGuard
        /// </summary>
        public static string Classify(object obj)
        {
            // 类型模式 —— Python: isinstance(obj, int)
            if (obj is int n and > 0)
            {
                return $"正整数: {n}";
            }

            // 属性模式 —— Python 没有直接对应
            if (obj is string { Length: > 0 } s)
            {
                return $"非空字符串: \"{s}\"";
            }

            // 元组模式 —— Python: if isinstance(x, tuple) and len(x) == 2
            if (obj is (int a, int b))
            {
                return $"整数元组: ({a}, {b})";
            }

            // 常量模式 —— Python: if x == None
            if (obj is null)
            {
                return "null 值";
            }

            return $"其他类型: {obj?.GetType().Name ?? "null"}";
        }

        public static void DemoPatternMatching()
        {
            Console.WriteLine("\n=== 3. Pattern Matching（对比 Python isinstance） ===");

            object[] values = { 42, "hello", (1, 2), null, -3.14, "" };
            foreach (var val in values)
            {
                Console.WriteLine($"  {val?.ToString() ?? "null",10} -> {Classify(val)}");
            }

            Console.WriteLine("  【Python 对比】");
            Console.WriteLine("  Python: if isinstance(x, int) and x > 0: ...");
            Console.WriteLine("  C#:     if (x is int n and > 0) { ... } — 更强大");
        }
    }

    // =========================================================================
    // 4. Record 类型 —— 对比 Python TypedDict/dataclass
    // =========================================================================
    // 【Python 对比】
    // Python:
    //   @dataclass
    //   class Person:
    //       name: str
    //       age: int
    //
    // C# record 自带不可变、值相等、ToString、解构

    /// <summary>
    /// C# record 类型 —— 对比 Python @dataclass(frozen=True)
    /// </summary>
    public record Person(string Name, int Age);

    public record Point(double X, double Y);

    /// <summary>
    /// 带额外方法的 record
    /// </summary>
    public record Student(string Name, int Age, double GPA) : Person(Name, Age)
    {
        public string Honors => GPA >= 3.5 ? "优等生" : "普通学生";
    }

    // init-only 属性 —— Python dataclass 没有直接对应
    public class PersonClass
    {
        public string Name { get; init; }  // 只能在初始化时设置
        public int Age { get; init; }
    }

    public static class RecordExamples
    {
        /// <summary>
        /// 演示 record 类型
        /// </summary>
        public static void DemoRecords()
        {
            Console.WriteLine("\n=== 4. Record 类型（对比 Python dataclass） ===");

            var p1 = new Person("Alice", 25);
            var p2 = new Person("Alice", 25);

            // 值相等 —— Python: @dataclass 自动生成 __eq__
            Console.WriteLine($"  p1 == p2: {p1 == p2}  (值相等)");
            Console.WriteLine($"  p1: {p1}  (自动生成 ToString)");

            // 解构 —— Python: name, age = person
            var (name, age) = p1;
            Console.WriteLine($"  解构: name={name}, age={age}");

            // 继承
            var student = new Student("Bob", 20, 3.8);
            Console.WriteLine($"  Student: {student}");
            Console.WriteLine($"  荣誉: {student.Honors}");

            // init-only 属性
            var person = new PersonClass { Name = "Charlie", Age = 30 };
            // person.Name = "Dave";  // 编译错误! init-only
            Console.WriteLine($"  init-only: {person.Name}");

            Console.WriteLine("  【Python 对比】");
            Console.WriteLine("  @dataclass 自动生成 __init__, __repr__, __eq__");
            Console.WriteLine("  C# record 还提供 value equality + deconstruction");
        }
    }

    // =========================================================================
    // 5. Generic Constraints —— 泛型约束
    // =========================================================================
    // 【Python 对比】
    // Python: def first[T: supports_comparison](lst: list[T]) -> T (3.12+)
    // C#:     T First<T>(List<T> list) where T : IComparable<T>
    //
    // Python 用 Protocol 做结构化约束，C# 用 interface 做名义约束

    public static class GenericExamples
    {
        /// <summary>
        /// 泛型方法 —— 对比 Python TypeVar
        /// </summary>
        public static T First<T>(List<T> list)
        {
            // 【Python 对比】def first[T](lst: list[T]) -> T:
            if (list.Count == 0)
                throw new ArgumentException("列表为空");
            return list[0];
        }

        /// <summary>
        /// 泛型约束 —— Python 没有直接对应
        /// </summary>
        public static T MaxValue<T>(T a, T b) where T : IComparable<T>
        {
            // where T : IComparable<T> 要求 T 实现 IComparable<T>
            // 【Python 对比】Python 用 Protocol 做类似的事
            return a.CompareTo(b) > 0 ? a : b;
        }

        /// <summary>
        /// 多种约束组合
        /// </summary>
        public static T CreateAndInit<T>() where T : class, IComparable<T>, new()
        {
            // class: 必须是引用类型
            // IComparable<T>: 必须可比较
            // new(): 必须有无参构造函数
            return new T();
        }

        public static void DemoGenerics()
        {
            Console.WriteLine("\n=== 5. 泛型约束（对比 Python Protocol） ===");

            var numbers = new List<int> { 1, 2, 3, 4, 5 };
            Console.WriteLine($"  First<int>: {First(numbers)}");

            var names = new List<string> { "Alice", "Bob" };
            Console.WriteLine($"  First<string>: {First(names)}");

            Console.WriteLine($"  MaxValue(3, 7): {MaxValue(3, 7)}");
            Console.WriteLine($"  MaxValue('a', 'z'): {MaxValue("a", "z")}");

            Console.WriteLine("  【Python 对比】");
            Console.WriteLine("  Python 用 Protocol 做结构化约束（鸭子类型）");
            Console.WriteLine("  C# 用 where 子句做名义约束（显式接口）");
        }
    }

    // =========================================================================
    // 6. 综合对比
    // =========================================================================
    public static class ComparisonSummary
    {
        public static void PrintComparison()
        {
            Console.WriteLine("\n=== 6. Python vs C# 类型系统对比 ===");
            Console.WriteLine("  ┌────────────────────┬────────────────────┬────────────────────┐");
            Console.WriteLine("  │ Python             │ C#                 │ 说明               │");
            Console.WriteLine("  ├────────────────────┼────────────────────┼────────────────────┤");
            Console.WriteLine("  │ name: str          │ string name        │ 基础类型           │");
            Console.WriteLine("  │ list[int]          │ List<int>          │ 泛型集合           │");
            Console.WriteLine("  │ str | None         │ string?            │ 可空类型           │");
            Console.WriteLine("  │ @dataclass         │ record             │ 数据类             │");
            Console.WriteLine("  │ Literal['a','b']   │ enum               │ 限定值             │");
            Console.WriteLine("  │ TypeGuard          │ is pattern         │ 类型窄化           │");
            Console.WriteLine("  │ Protocol           │ interface          │ 结构化子类型       │");
            Console.WriteLine("  │ TypeVar [T]        │ <T> where T : ...  │ 泛型               │");
            Console.WriteLine("  └────────────────────┴────────────────────┴────────────────────┘");
            Console.WriteLine("  核心区别: C# 编译时强制，Python 运行时可选");
        }
    }

    // =========================================================================
    // 主程序入口
    // =========================================================================
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("============================================================");
            Console.WriteLine("  C# 老兵的 Python 修炼手册 — 5.3 类型提示");
            Console.WriteLine("============================================================");

            BasicTypeExamples.DemoBasicTypes();
            NullableExamples.DemoNullableTypes();
            PatternMatchingExamples.DemoPatternMatching();
            RecordExamples.DemoRecords();
            GenericExamples.DemoGenerics();
            ComparisonSummary.PrintComparison();

            Console.WriteLine("\n============================================================");
            Console.WriteLine("  核心结论：");
            Console.WriteLine("  1. C# 类型系统是强制的，Python 是可选的");
            Console.WriteLine("  2. C# record 比 Python dataclass 更强大");
            Console.WriteLine("  3. C# pattern matching 比 Python isinstance 更强大");
            Console.WriteLine("  4. C# 泛型约束比 Python Protocol 更严格");
            Console.WriteLine("============================================================");
        }
    }
}
