// =============================================================================
// C# 数据类示例 — C# 老兵的 Python 修炼手册 5.6
// 对应文章：5.6 dataclass
// 关键概念：record, record struct, init-only, with 表达式,
//           value equality, deconstruction
// =============================================================================
// 【C# vs Python 对比】
// C# record 是 Python @dataclass 的超集
// C# record 自带不可变、值相等、ToString、解构
// Python 需要 frozen=True, __post_init__ 等额外配置
// =============================================================================

using System;
using System.Collections.Generic;
using System.Linq;

namespace DataClassDemo
{
    // =========================================================================
    // 1. record 类型——C# 的数据类
    // =========================================================================
    // 【Python 对比】
    // Python:
    //   @dataclass
    //   class Person:
    //       name: str
    //       age: int
    //
    // C#: public record Person(string Name, int Age);
    // 一行搞定，自动生成: 构造函数, Equals, GetHashCode, ToString, Deconstruct

    /// <summary>
    /// 基础 record——对比 Python @dataclass
    /// </summary>
    public record Person(string Name, int Age);

    /// <summary>
    /// 带默认值的 record
    /// 【Python 对比】@dataclass + field(default=...)
    /// </summary>
    public record Point(double X, double Y);

    /// <summary>
    /// 继承的 record
    /// </summary>
    public record Student(string Name, int Age, double GPA) : Person(Name, Age)
    {
        public string Honors => GPA >= 3.5 ? "优等生" : "普通学生";
    }

    // =========================================================================
    // 2. 不可变性——record 天然不可变
    // =========================================================================
    // 【Python 对比】
    // Python: @dataclass(frozen=True) 需要显式设置
    // C#: record 天然不可变，init-only 属性只能在初始化时设置

    /// <summary>
    /// 不可变地址——对比 Python @dataclass(frozen=True)
    /// </summary>
    public record Address(string Street, string City, string Country = "中国");

    /// <summary>
    /// 演示不可变性
    /// </summary>
    public static class ImmutabilityExamples
    {
        public static void DemoImmutability()
        {
            Console.WriteLine("\n=== 1. 不可变性（对比 frozen=True） ===");

            var address = new Address("中关村大街1号", "北京");
            Console.WriteLine($"  地址: {address}");

            // 尝试修改会编译错误
            // address.Street = "新地址";  // 编译错误! init-only

            // 用 with 表达式创建新实例
            // 【Python 对比】replace(address, city="上海")
            var newAddress = address with { City = "上海" };
            Console.WriteLine($"  修改后: {newAddress}");
            Console.WriteLine($"  原始不变: {address}");

            Console.WriteLine("  【Python 对比】Python: replace(obj, field=value)");
        }
    }

    // =========================================================================
    // 3. 值相等——record 自动实现
    // =========================================================================
    // 【Python 对比】
    // Python: @dataclass 自动生成 __eq__，但默认比较所有字段
    // C#: record 自动生成 Equals，按值比较

    public static class EqualityExamples
    {
        public static void DemoEquality()
        {
            Console.WriteLine("\n=== 2. 值相等（对比 __eq__） ===");

            var p1 = new Person("Alice", 25);
            var p2 = new Person("Alice", 25);
            var p3 = new Person("Bob", 30);

            // 值相等
            Console.WriteLine($"  p1 == p2: {p1 == p2}");  // True
            Console.WriteLine($"  p1 == p3: {p1 == p3}");  // False

            // 引用相等
            Console.WriteLine($"  ReferenceEquals: {ReferenceEquals(p1, p2)}");  // False

            // HashCode 一致
            Console.WriteLine($"  p1.GetHashCode(): {p1.GetHashCode()}");
            Console.WriteLine($"  p2.GetHashCode(): {p2.GetHashCode()}");
            Console.WriteLine($"  HashCode 相等: {p1.GetHashCode() == p2.GetHashCode()}");

            // 可以用作 Dictionary 的 key
            var dict = new Dictionary<Person, string>
            {
                [p1] = "第一个"
            };
            Console.WriteLine($"  dict[p2]: {dict[p2]}");  // 找到 p1（值相等）

            Console.WriteLine("  【Python 对比】Python @dataclass 默认比较所有字段");
        }
    }

    // =========================================================================
    // 4. with 表达式——不可变更新
    // =========================================================================
    // 【Python 对比】
    // Python: replace(person, age=26)
    // C#: person with { Age = 26 }

    /// <summary>
    /// 用户配置——演示 with 表达式
    /// </summary>
    public record UserConfig(
        string Username,
        string Email,
        string Theme = "dark",
        string Language = "zh-CN"
    );

    public static class WithExpressionExamples
    {
        public static void DemoWithExpression()
        {
            Console.WriteLine("\n=== 3. with 表达式（对比 replace()） ===");

            var config = new UserConfig("alice", "alice@example.com");
            Console.WriteLine($"  原始: {config}");

            // with 表达式——创建新实例并修改部分字段
            // 【Python 对比】replace(config, theme="light")
            var updated = config with { Theme = "light" };
            Console.WriteLine($"  更新: {updated}");
            Console.WriteLine($"  原始不变: {config}");

            // 多个字段
            var fullyUpdated = config with
            {
                Theme = "light",
                Language = "en-US",
                Email = "alice@new.com"
            };
            Console.WriteLine($"  完全更新: {fullyUpdated}");

            Console.WriteLine("  【Python 对比】Python: replace(obj, field1=v1, field2=v2)");
        }
    }

    // =========================================================================
    // 5. 解构——record 自动支持
    // =========================================================================
    // 【Python 对比】
    // Python: name, age = person (需要 __iter__ 或手写)
    // C#: var (name, age) = person (自动生成 Deconstruct)

    public static class DeconstructionExamples
    {
        public static void DemoDeconstruction()
        {
            Console.WriteLine("\n=== 4. 解构（自动 Deconstruct） ===");

            var person = new Person("Alice", 25);

            // 解构
            // 【Python 对比】Python 需要手写 __iter__ 或 @dataclass 中用 tuple()
            var (name, age) = person;
            Console.WriteLine($"  解构: name={name}, age={age}");

            // Student 解构（包含继承的字段）
            var student = new Student("Bob", 20, 3.8);
            var (sName, sAge, sGpa) = student;
            Console.WriteLine($"  Student 解构: name={sName}, age={sAge}, gpa={sGpa}");

            // 属性解构
            var (sName2, _) = student;
            Console.WriteLine($"  部分解构: name={sName2}");

            Console.WriteLine("  【Python 对比】Python 用 tuple() 或 __iter__ 实现");
        }
    }

    // =========================================================================
    // 6. ToString 自动重写
    // =========================================================================
    // 【Python 对比】
    // Python @dataclass 自动生成 __repr__
    // C# record 自动生成 ToString (带所有属性)

    public static class ToStringExamples
    {
        public static void DemoToString()
        {
            Console.WriteLine("\n=== 5. ToString（对比 __repr__） ===");

            var person = new Person("Alice", 25);

            // 自动 ToString
            // Python: repr(person) -> "Person(name='Alice', age=25)"
            // C#: person.ToString() -> "Person { Name = Alice, Age = 25 }"
            Console.WriteLine($"  ToString: {person}");

            // 可以自定义
            var student = new Student("Bob", 20, 3.8);
            Console.WriteLine($"  Student ToString: {student}");

            Console.WriteLine("  两者都自动生成可读的字符串表示");
        }
    }

    // =========================================================================
    // 7. record struct——值类型数据类
    // =========================================================================
    // 【Python 对比】
    // Python 没有 record struct 对应物（Python 一切皆对象/引用类型）
    // C# record struct 是栈上分配的不可变值类型
    // C# 10+: record struct 提供 record 的便利性 + struct 的性能

    /// <summary>
    /// record struct——栈上分配的数据类
    /// 【Python 对比】Python 没有对应物（Python 没有值类型）
    /// </summary>
    public readonly record struct Coordinate(double Latitude, double Longitude);

    /// <summary>
    /// 可变 record struct
    /// </summary>
    public record struct MutablePoint(double X, double Y)
    {
        public double X { get; set; } = X;  // 可以修改
    }

    public static class RecordStructExamples
    {
        public static void DemoRecordStruct()
        {
            Console.WriteLine("\n=== 6. record struct（Python 没有对应物） ===");

            // readonly record struct
            var coord1 = new Coordinate(39.9, 116.4);
            var coord2 = new Coordinate(39.9, 116.4);
            Console.WriteLine($"  Coordinate: {coord1}");
            Console.WriteLine($"  值相等: {coord1 == coord2}");

            // 可变 record struct
            var point = new MutablePoint(3.0, 4.0);
            Console.WriteLine($"  MutablePoint: {point}");
            point.X = 5.0;  // 可以修改
            Console.WriteLine($"  修改后: {point}");

            Console.WriteLine("  【Python 对比】Python 一切皆引用类型，没有栈分配");
        }
    }

    // =========================================================================
    // 8. init-only 属性——class 中的不可变字段
    // =========================================================================
    // 【Python 对比】
    // Python: @dataclass 中字段默认就是 init-only（通过 __init__ 设置）
    // C# init-only: 只能在构造函数或对象初始化器中设置

    /// <summary>
    /// 使用 init-only 属性的普通类
    /// 【Python 对比】Python dataclass 的字段类似
    /// </summary>
    public class PersonClass
    {
        public string Name { get; init; }    // 只能在初始化时设置
        public int Age { get; init; }
        public DateTime CreatedAt { get; init; } = DateTime.Now;

        public override string ToString() =>
            $"PersonClass(Name={Name}, Age={Age}, CreatedAt={CreatedAt:yyyy-MM-dd})";
    }

    public static class InitOnlyExamples
    {
        public static void DemoInitOnly()
        {
            Console.WriteLine("\n=== 7. init-only 属性 ===");

            var person = new PersonClass
            {
                Name = "Alice",
                Age = 25
                // CreatedAt 自动设置
            };

            Console.WriteLine($"  创建: {person}");

            // person.Name = "Bob";  // 编译错误! init-only

            Console.WriteLine("  init-only 属性只能在初始化时设置");
            Console.WriteLine("  【Python 对比】Python dataclass 字段天然类似");
        }
    }

    // =========================================================================
    // 9. 综合对比
    // =========================================================================

    public static class ComparisonSummary
    {
        public static void PrintComparison()
        {
            Console.WriteLine("\n=== 8. Python dataclass vs C# record 对比 ===");
            Console.WriteLine("  ┌──────────────────────┬──────────────────────┬──────────────────────┐");
            Console.WriteLine("  │ Python dataclass     │ C# record            │ 说明                 │");
            Console.WriteLine("  ├──────────────────────┼──────────────────────┼──────────────────────┤");
            Console.WriteLine("  │ @dataclass           │ record               │ 基础数据类           │");
            Console.WriteLine("  │ frozen=True          │ record (天然不可变)  │ 不可变               │");
            Console.WriteLine("  │ order=True           │ IComparable          │ 比较操作             │");
            Console.WriteLine("  │ __post_init__        │ 构造函数逻辑         │ 自定义初始化         │");
            Console.WriteLine("  │ slots=True           │ record struct        │ 内存优化             │");
            Console.WriteLine("  │ asdict()             │ 手动映射             │ 序列化               │");
            Console.WriteLine("  │ replace()            │ with 表达式          │ 不可变更新           │");
            Console.WriteLine("  │ field()              │ init-only            │ 字段控制             │");
            Console.WriteLine("  └──────────────────────┴──────────────────────┴──────────────────────┘");
            Console.WriteLine("  核心区别: C# record 天然不可变+值相等，Python 需要显式配置");
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
            Console.WriteLine("  C# 老兵的 Python 修炼手册 — 5.6 数据类");
            Console.WriteLine("============================================================");

            ImmutabilityExamples.DemoImmutability();
            EqualityExamples.DemoEquality();
            WithExpressionExamples.DemoWithExpression();
            DeconstructionExamples.DemoDeconstruction();
            ToStringExamples.DemoToString();
            RecordStructExamples.DemoRecordStruct();
            InitOnlyExamples.DemoInitOnly();
            ComparisonSummary.PrintComparison();

            Console.WriteLine("\n============================================================");
            Console.WriteLine("  核心结论：");
            Console.WriteLine("  1. C# record 比 Python dataclass 更简洁更强大");
            Console.WriteLine("  2. C# record 天然不可变，Python 需要 frozen=True");
            Console.WriteLine("  3. C# with 表达式比 Python replace() 更直观");
            Console.WriteLine("  4. C# record struct 提供值类型性能（Python 无对应物）");
            Console.WriteLine("  5. C# 自动解构，Python 需要额外配置");
            Console.WriteLine("============================================================");
        }
    }
}
