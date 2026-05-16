// =============================================================================
// C# 反射与元编程示例 — C# 老兵的 Python 修炼手册 5.5
// 对应文章：5.5 元类与反射
// 关键概念：Type class, Activator, PropertyInfo, MethodInfo,
//           Expression Trees, Attributes
// =============================================================================
// 【C# vs Python 对比】
// C# 没有元类概念，但有强大的反射系统和代码生成能力
// C# Type 类 ≈ Python type()
// C# PropertyInfo ≈ Python getattr/setattr
// C# Source Generators ≈ Python 元类
// =============================================================================

using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using System.Reflection;

namespace ReflectionDemo
{
    // =========================================================================
    // 1. Type 类——查看类型信息
    // =========================================================================
    // 【Python 对比】
    // Python: type(obj) 获取类型
    // Python: type("Person", (Base,), {"attr": value}) 动态创建类
    //
    // C#: typeof(T) 或 obj.GetType() 获取 Type 对象

    public class Person
    {
        public string Name { get; set; } = "";
        public int Age { get; set; }

        public Person() { }

        public Person(string name, int age)
        {
            Name = name;
            Age = age;
        }

        public string Greet() => $"Hello, I'm {Name}";

        public override string ToString() => $"Person(Name={Name}, Age={Age})";
    }

    public static class TypeExamples
    {
        /// <summary>
        /// 演示 Type 类的使用
        /// 【Python 对比】type(obj) 和 type.__name__
        /// </summary>
        public static void DemoTypeClass()
        {
            Console.WriteLine("\n=== 1. Type 类（对比 Python type()） ===");

            // 获取 Type 对象
            // 【Python 对比】type(p) 或 type(Person)
            Type type1 = typeof(Person);        // 编译时
            Type type2 = typeof(Person).GetNestedType("Person") ?? typeof(Person);
            Type type3 = new Person().GetType(); // 运行时

            Console.WriteLine($"  typeof(Person).Name: {type1.Name}");
            Console.WriteLine($"  typeof(Person).FullName: {type1.FullName}");
            Console.WriteLine($"  typeof(Person).Namespace: {type1.Namespace}");

            // 类型检查
            Console.WriteLine($"  Is class: {type1.IsClass}");
            Console.WriteLine($"  Is value type: {type1.IsValueType}");
            Console.WriteLine($"  Is abstract: {type1.IsAbstract}");
            Console.WriteLine($"  BaseType: {type1.BaseType?.Name}");

            Console.WriteLine("  【Python 对比】Python: cls.__name__, cls.__bases__");
        }

        /// <summary>
        /// 演示获取属性和方法信息
        /// 【Python 对比】dir(obj), getattr(obj, '__dict__')
        /// </summary>
        public static void DemoReflectionInfo()
        {
            Console.WriteLine("\n=== 2. 获取属性和方法信息 ===");

            Type type = typeof(Person);

            // 获取所有公共属性
            // 【Python 对比】[k for k in dir(Person) if not k.startswith('_')]
            Console.WriteLine("  公共属性:");
            foreach (PropertyInfo prop in type.GetProperties())
            {
                Console.WriteLine($"    {prop.Name}: {prop.PropertyType.Name} "
                    + $"(CanRead={prop.CanRead}, CanWrite={prop.CanWrite})");
            }

            // 获取所有公共方法
            // 【Python 对比】[m for m in dir(Person) if callable(getattr(Person, m))]
            Console.WriteLine("  公共方法:");
            foreach (MethodInfo method in type.GetMethods(
                BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly))
            {
                string parameters = string.Join(", ",
                    method.GetParameters().Select(p => $"{p.ParameterType.Name} {p.Name}"));
                Console.WriteLine($"    {method.ReturnType.Name} {method.Name}({parameters})");
            }
        }
    }

    // =========================================================================
    // 2. Activator——动态创建实例
    // =========================================================================
    // 【Python 对比】
    // Python: cls(*args, **kwargs)  —— 直接调用类
    // Python: type("Name", bases, ns) —— 动态创建新类
    //
    // C#: Activator.CreateInstance(type) —— 根据 Type 动态创建实例

    public static class ActivatorExamples
    {
        /// <summary>
        /// 演示 Activator 动态创建实例
        /// </summary>
        public static void DemoActivator()
        {
            Console.WriteLine("\n=== 3. Activator 动态创建实例 ===");

            Type type = typeof(Person);

            // 创建默认实例
            // 【Python 对比】Person()
            object obj1 = Activator.CreateInstance(type);
            Console.WriteLine($"  默认实例: {obj1}");

            // 创建带参数的实例
            // 【Python 对比】Person("Alice", 25)
            object obj2 = Activator.CreateInstance(type, "Alice", 25);
            Console.WriteLine($"  带参实例: {obj2}");

            // 动态设置属性
            // 【Python 对比】setattr(obj, "Name", "Bob")
            PropertyInfo nameProp = type.GetProperty("Name");
            nameProp?.SetValue(obj1, "Bob");
            Console.WriteLine($"  设置后: {obj1}");

            // 动态调用方法
            // 【Python 对比】getattr(obj, "Greet")()
            MethodInfo greetMethod = type.GetMethod("Greet");
            string result = (string)greetMethod?.Invoke(obj1, null)!;
            Console.WriteLine($"  调用方法: {result}");

            Console.WriteLine("  【Python 对比】Python 更简洁: getattr(obj, 'name')");
        }
    }

    // =========================================================================
    // 3. 特性 (Attributes) —— C# 独有的元编程方式
    // =========================================================================
    // 【Python 对比】
    // Python 用装饰器 + 元类实现类似功能:
    //   @validate_name
    //   class Person: ...
    //
    // C# 用 Attribute + 反射:
    //   [Required, MaxLength(50)]
    //   public string Name { get; set; }

    [AttributeUsage(AttributeTargets.Class | AttributeTargets.Property)]
    public class DescriptionAttribute : Attribute
    {
        public string Description { get; }
        public DescriptionAttribute(string description) => Description = description;
    }

    [AttributeUsage(AttributeTargets.Property)]
    public class RangeAttribute : Attribute
    {
        public int Min { get; }
        public int Max { get; }
        public RangeAttribute(int min, int max) { Min = min; Max = max; }
    }

    [Description("产品信息")]
    public class Product
    {
        [Description("产品名称")]
        public string Name { get; set; } = "";

        [Description("产品价格"), Range(0, 10000)]
        public decimal Price { get; set; }

        [Description("库存数量"), Range(0, 1000000)]
        public int Stock { get; set; }
    }

    public static class AttributeExamples
    {
        /// <summary>
        /// 演示 Attribute 反射
        /// </summary>
        public static void DemoAttributes()
        {
            Console.WriteLine("\n=== 4. 特性 Attribute（C# 独有） ===");

            // 获取类的特性
            Type type = typeof(Product);
            var classAttr = type.GetCustomAttribute<DescriptionAttribute>();
            Console.WriteLine($"  类描述: {classAttr?.Description}");

            // 获取属性的特性
            Console.WriteLine("  属性特性:");
            foreach (PropertyInfo prop in type.GetProperties())
            {
                var desc = prop.GetCustomAttribute<DescriptionAttribute>();
                var range = prop.GetCustomAttribute<RangeAttribute>();
                Console.WriteLine($"    {prop.Name}: "
                    + $"描述=\"{desc?.Description}\" "
                    + (range != null ? $"范围=[{range.Min}, {range.Max}]" : ""));
            }

            // 验证属性值
            Product product = new Product { Name = "Test", Price = 100, Stock = 50 };
            ValidateProduct(product);

            Console.WriteLine("  【Python 对比】Python 用装饰器实现类似功能");
        }

        static void ValidateProduct(Product product)
        {
            Type type = typeof(Product);
            foreach (PropertyInfo prop in type.GetProperties())
            {
                var range = prop.GetCustomAttribute<RangeAttribute>();
                if (range != null)
                {
                    var value = (int)Convert.ChangeType(prop.GetValue(product), typeof(int));
                    if (value < range.Min || value > range.Max)
                    {
                        Console.WriteLine($"    验证失败: {prop.Name}={value} "
                            + $"超出范围 [{range.Min}, {range.Max}]");
                    }
                }
            }
            Console.WriteLine("  验证通过");
        }
    }

    // =========================================================================
    // 4. 动态方法调用——对比 Python getattr + callable
    // =========================================================================

    public static class DynamicInvocationExamples
    {
        /// <summary>
        /// 演示动态方法调用
        /// 【Python 对比】getattr(obj, method_name)(*args)
        /// </summary>
        public static void DemoDynamicInvocation()
        {
            Console.WriteLine("\n=== 5. 动态方法调用 ===");

            Person person = new Person("Alice", 25);
            Type type = person.GetType();

            // 动态调用方法
            string methodName = "Greet";
            MethodInfo method = type.GetMethod(methodName);
            if (method != null)
            {
                string result = (string)method.Invoke(person, null)!;
                Console.WriteLine($"  动态调用 {methodName}(): {result}");
            }

            // 动态调用 ToString
            MethodInfo toStringMethod = type.GetMethod("ToString");
            string toStringResult = (string)toStringMethod?.Invoke(person, null)!;
            Console.WriteLine($"  动态调用 ToString(): {toStringResult}");

            Console.WriteLine("  【Python 对比】Python: getattr(obj, method_name)()");
        }
    }

    // =========================================================================
    // 5. Expression Trees——动态生成代码
    // =========================================================================
    // 【Python 对比】
    // Python 没有直接对应，但有:
    //   - exec() / eval() 执行字符串代码
    //   - lambda 表达式
    //   - ast 模块操作抽象语法树
    //
    // C# Expression Trees 可以在运行时构建和编译代码树

    public static class ExpressionTreeExamples
    {
        /// <summary>
        /// 演示 Expression Trees
        /// </summary>
        public static void DemoExpressionTrees()
        {
            Console.WriteLine("\n=== 6. Expression Trees（动态代码生成） ===");

            // 构建一个简单的表达式: (x, y) => x + y
            // 【Python 对比】lambda x, y: x + y
            ParameterExpression xParam = Expression.Parameter(typeof(int), "x");
            ParameterExpression yParam = Expression.Parameter(typeof(int), "y");
            BinaryExpression addExpr = Expression.Add(xParam, yParam);
            Expression<Func<int, int, int>> addLambda =
                Expression.Lambda<Func<int, int, int>>(addExpr, xParam, yParam);

            // 编译并执行
            Func<int, int, int> addFunc = addLambda.Compile();
            Console.WriteLine($"  Expression 编译: addFunc(3, 4) = {addFunc(3, 4)}");

            // 构建一个条件表达式: x => x > 0 ? x * 2 : 0
            ParameterExpression x = Expression.Parameter(typeof(int), "x");
            ConditionalExpression condition = Expression.Condition(
                Expression.GreaterThan(x, Expression.Constant(0)),
                Expression.Multiply(x, Expression.Constant(2)),
                Expression.Constant(0)
            );
            Expression<Func<int, int>> doublePositive =
                Expression.Lambda<Func<int, int>>(condition, x);

            Func<int, int> doublePositiveFunc = doublePositive.Compile();
            Console.WriteLine($"  条件表达式: doublePositive(5) = {doublePositiveFunc(5)}");
            Console.WriteLine($"  条件表达式: doublePositive(-3) = {doublePositiveFunc(-3)}");

            Console.WriteLine("  【Python 对比】Python: lambda x: x * 2 if x > 0 else 0");
        }
    }

    // =========================================================================
    // 6. __init_subclass__ 的 C# 等价物——Attribute + 反射注册
    // =========================================================================

    /// <summary>
    /// 插件接口
    /// </summary>
    public interface IPlugin
    {
        string Name { get; }
        string Process(string input);
    }

    /// <summary>
    /// 插件注册特性
    /// 【Python 对比】__init_subclass__ 中的自动注册
    /// </summary>
    [AttributeUsage(AttributeTargets.Class)]
    public class PluginAttribute : Attribute
    {
        public string PluginName { get; }
        public PluginAttribute(string name) => PluginName = name;
    }

    [Plugin("json")]
    public class JsonPlugin : IPlugin
    {
        public string Name => "JSON Plugin";
        public string Process(string input) => $"{{\"processed\": \"{input}\"}}";
    }

    [Plugin("csv")]
    public class CsvPlugin : IPlugin
    {
        public string Name => "CSV Plugin";
        public string Process(string input) => $"csv,{input}";
    }

    public static class PluginRegistry
    {
        private static Dictionary<string, Type> _plugins = new();

        static PluginRegistry()
        {
            // 扫描所有带 [Plugin] 特性的类
            // 【Python 对比】Python 元类的 __new__ 或 __init_subclass__
            foreach (Type type in AppDomain.CurrentDomain.GetAssemblies()
                .SelectMany(a => a.GetTypes())
                .Where(t => typeof(IPlugin).IsAssignableFrom(t) && !t.IsInterface))
            {
                var attr = type.GetCustomAttribute<PluginAttribute>();
                if (attr != null)
                {
                    _plugins[attr.PluginName] = type;
                    Console.WriteLine($"  [注册插件] {attr.PluginName} -> {type.Name}");
                }
            }
        }

        public static IPlugin? GetPlugin(string name)
        {
            if (_plugins.TryGetValue(name, out Type? type))
            {
                return (IPlugin?)Activator.CreateInstance(type);
            }
            return null;
        }
    }

    public static class PluginExamples
    {
        public static void DemoPlugins()
        {
            Console.WriteLine("\n=== 7. 插件注册（对比 __init_subclass__） ===");

            // 获取插件
            IPlugin? jsonPlugin = PluginRegistry.GetPlugin("json");
            if (jsonPlugin != null)
            {
                Console.WriteLine($"  {jsonPlugin.Name}: {jsonPlugin.Process("data")}");
            }

            IPlugin? csvPlugin = PluginRegistry.GetPlugin("csv");
            if (csvPlugin != null)
            {
                Console.WriteLine($"  {csvPlugin.Name}: {csvPlugin.Process("data")}");
            }

            Console.WriteLine("  【Python 对比】Python __init_subclass__ 自动注册更简洁");
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
            Console.WriteLine("  C# 老兵的 Python 修炼手册 — 5.5 元类与反射");
            Console.WriteLine("============================================================");

            TypeExamples.DemoTypeClass();
            TypeExamples.DemoReflectionInfo();
            ActivatorExamples.DemoActivator();
            AttributeExamples.DemoAttributes();
            DynamicInvocationExamples.DemoDynamicInvocation();
            ExpressionTreeExamples.DemoExpressionTrees();
            PluginExamples.DemoPlugins();

            Console.WriteLine("\n============================================================");
            Console.WriteLine("  核心结论：");
            Console.WriteLine("  1. C# Type 类 = Python type()，但更强大");
            Console.WriteLine("  2. C# Attribute = Python 装饰器 + 元类");
            Console.WriteLine("  3. C# Expression Trees = Python exec/eval + ast");
            Console.WriteLine("  4. C# 受类型系统约束更安全，Python 更灵活");
            Console.WriteLine("  5. C# Source Generators 是编译时元编程");
            Console.WriteLine("============================================================");
        }
    }
}
