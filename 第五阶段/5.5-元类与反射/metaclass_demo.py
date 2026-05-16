# =============================================================================
# Python 元类与反射示例 — C# 老兵的 Python 修炼手册 5.5
# 对应文章：5.5 元类与反射
# 关键概念：metaclass, __new__, type(), __init_subclass__,
#           getattr/setattr/delattr, dataclasses.fields()
# =============================================================================
# 【C# vs Python 对比】
# Python 元类 = "类的类"，控制类的创建方式
# C# 没有元类概念，但有类似的：
#   - Type 类 + 运行时反射（动态创建类型）
#   - 特性 (Attributes) + 反射（读取/修改元数据）
#   - Expression Trees（动态生成代码）
#
# 核心区别:
# Python: class 是运行时对象，可以动态修改
# C#: Type 是编译时确定的，反射可以读取但修改有限
# =============================================================================

import sys
from dataclasses import dataclass, fields
from typing import Any, Optional


# =============================================================================
# 1. type() 函数 —— 查看和创建类型
# =============================================================================
# 【C# 对比】
# C#: typeof(object) 获取 Type 对象
# Python: type(obj) 获取类型，type(name, bases, dict) 创建类型
#
# Python 中，class 本身就是 type 的实例


def demo_type_function():
    """演示 type() 的两种用法"""
    print("\n=== 1. type() 函数 ===")

    # 查看类型
    x = 42
    print(f"  type(42) = {type(x)}")
    print(f"  type('hello') = {type('hello')}")
    print(f"  type([1,2,3]) = {type([1, 2, 3])}")

    # 【C# 对比】typeof(int), x.GetType()

    # 动态创建类——type(name, bases, dict)
    # 【C# 对比】C# 用 Type.GetType() + Activator.CreateInstance()
    # 但 C# 不能这样动态创建新类型（需要 Reflection.Emit 或 Expression Trees）
    Person = type("Person", (), {
        "greet": lambda self: f"Hello, I'm {self.name}",
        "__init__": lambda self, name: setattr(self, "name", name),
    })

    p = Person("Alice")
    print(f"\n  动态创建类: {type(p)}")
    print(f"  调用方法: {p.greet()}")

    # type() 的本质
    print(f"\n  type 的类型: {type(type)}")  # <class 'type'>
    print("  type 是所有类的元类——'元类的元类'")


# =============================================================================
# 2. 元类基础 —— 控制类的创建
# =============================================================================
# 【C# 对比】
# C# 没有元类，但有类似功能:
#   - 编译器代码生成 (source generators)
#   - 运行时类型创建 (Reflection.Emit)
#   - 特性 + 反射 (Attribute + reflection)
#
# 元类的核心思想：
# 当你写 class MyClass(metaclass=Meta): ...
# Python 不会直接创建 MyClass，而是调用 Meta("MyClass", bases, dict)
# 这意味着你可以拦截类的创建过程，修改类的定义


class ValidatedMeta(type):
    """验证元类：确保类的属性有类型注解
    
    【C# 对比】C# 的源代码生成器 (Source Generator) 可以做类似的事
    但发生在编译时，而不是运行时
    """
    def __new__(mcs, name, bases, namespace):
        """__new__ 在类创建时被调用
        
        【C# 对比】C# 编译器在编译时做类似检查
        Python 在运行时做，更灵活但也更容易出错
        """
        # 跳过基类（不验证基类本身）
        if bases:
            for key, value in namespace.items():
                if not key.startswith('_') and not callable(value):
                    # 检查是否有类型注解
                    if key not in namespace.get('__annotations__', {}):
                        raise TypeError(
                            f"类 '{name}' 的属性 '{key}' 缺少类型注解"
                        )

        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace):
        """__init__ 在类创建后被调用（__new__ 之后）"""
        super().__init__(name, bases, namespace)


class ValidatedClass(metaclass=ValidatedMeta):
    """使用验证元类的基类"""
    pass


def demo_metaclass_basics():
    """演示元类基础"""
    print("\n=== 2. 元类基础 (metaclass) ===")

    # 正确使用：有类型注解
    class GoodPerson(ValidatedClass):
        name: str
        age: int

        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age

    p = GoodPerson("Alice", 25)
    print(f"  GoodPerson: name={p.name}, age={p.age}")

    # 错误使用：缺少类型注解
    try:
        class BadPerson(ValidatedClass):
            name = "test"  # 缺少类型注解!
    except TypeError as e:
        print(f"  验证失败: {e}")

    print("  【C# 对比】C# 编译器在编译时强制检查，不需要元类")


# =============================================================================
# 3. 实用元类模式——单例模式
# =============================================================================
# 【C# 对比】
# C# 单例可以用:
#   - static 属性
#   - Lazy<T>
#   - sealed class + private constructor
# Python 用元类实现最简洁


class SingletonMeta(type):
    """单例元类——确保每个类只有一个实例
    
    【C# 对比】
    C#:
    public sealed class Singleton
    {
        private static readonly Lazy<Singleton> _instance = new(() => new Singleton());
        public static Singleton Instance => _instance.Value;
        private Singleton() { }
    }
    """
    _instances: dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):
        """拦截类的实例化过程"""
        if cls not in cls._instances:
            # 第一次创建实例
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    """单例数据库连接"""

    def __init__(self):
        self.connection = "connected"
        print("  [Database] 新建数据库连接")

    def query(self, sql: str) -> str:
        return f"执行: {sql}"


def demo_singleton():
    """演示单例元类"""
    print("\n=== 3. 单例元类模式 ===")

    # 两次创建实际上是同一个实例
    db1 = Database()
    db2 = Database()

    print(f"  db1 == db2: {db1 is db2}")  # True
    print(f"  db1.connection: {db1.connection}")
    print(f"  db2.query('SELECT 1'): {db2.query('SELECT 1')}")

    # 修改一个会影响另一个
    db1.connection = "reconnected"
    print(f"  db2.connection: {db2.connection}")  # 也变了

    print("  【C# 对比】C# 用 static Lazy<T> 实现单例更常见")


# =============================================================================
# 4. __init_subclass__ —— 简化元类（Python 3.6+）
# =============================================================================
# 【C# 对比】
# C# 没有直接对应，但类似:
#   - 静态构造函数 (static constructor)
#   - 属性初始化器
#   - 特性 (Attributes)
#
# __init_subclass__ 比元类更简单，适合大多数场景
# 元类适合更复杂的类创建控制


class PluginBase:
    """插件基类——用 __init_subclass__ 自动注册子类
    
    【C# 对比】C# 用特性 + 反射实现类似功能:
    [Plugin("my-plugin")]
    class MyPlugin : PluginBase { ... }
    """
    _registry: dict[str, type] = {}

    def __init_subclass__(cls, plugin_name: str = "", **kwargs):
        """当子类继承 PluginBase 时自动调用
        
        【C# 对比】类似 C# 的 [Attribute] 标记 + 扫描注册
        """
        super().__init_subclass__(**kwargs)
        if plugin_name:
            PluginBase._registry[plugin_name] = cls
            print(f"  [注册插件] {plugin_name} -> {cls.__name__}")

    @classmethod
    def get_plugin(cls, name: str) -> Optional["PluginBase"]:
        """根据名称获取插件实例"""
        plugin_class = cls._registry.get(name)
        if plugin_class:
            return plugin_class()
        return None


class JsonPlugin(PluginBase, plugin_name="json"):
    def process(self, data: dict) -> str:
        import json
        return json.dumps(data)


class CsvPlugin(PluginBase, plugin_name="csv"):
    def process(self, data: dict) -> str:
        return ",".join(f"{k}:{v}" for k, v in data.items())


def demo_init_subclass():
    """演示 __init_subclass__"""
    print("\n=== 4. __init_subclass__（简化元类） ===")

    # 自动注册已经在类定义时发生
    print(f"  已注册插件: {list(PluginBase._registry.keys())}")

    # 使用插件
    plugin1 = PluginBase.get_plugin("json")
    if plugin1:
        result = plugin1.process({"name": "Alice", "age": 25})
        print(f"  JSON: {result}")

    plugin2 = PluginBase.get_plugin("csv")
    if plugin2:
        result = plugin2.process({"name": "Bob", "age": 30})
        print(f"  CSV: {result}")

    # 不存在的插件
    plugin3 = PluginBase.get_plugin("xml")
    print(f"  XML: {plugin3}")  # None

    print("  【C# 对比】C# 用 Attribute + 反射注册，需要手动扫描")


# =============================================================================
# 5. 反射——getattr/setattr/delattr
# =============================================================================
# 【C# 对比】
# C# 反射:
#   PropertyInfo prop = typeof(T).GetProperty("Name");
#   prop.GetValue(obj);  // 获取
#   prop.SetValue(obj, value);  // 设置
# Python 反射:
#   getattr(obj, "name")  # 获取
#   setattr(obj, "name", value)  # 设置
#   delattr(obj, "name")  # 删除
#
# Python 的反射更简洁，因为一切皆对象


class Person:
    """用于反射演示的类"""

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Hello, I'm {self.name}"

    def __repr__(self) -> str:
        return f"Person(name='{self.name}', age={self.age})"


def demo_reflection():
    """演示反射操作"""
    print("\n=== 5. 反射 getattr/setattr/delattr ===")

    p = Person("Alice", 25)

    # getattr —— 动态获取属性
    # 【C# 对比】typeof(Person).GetProperty("Name").GetValue(p)
    print(f"  getattr(p, 'name'): {getattr(p, 'name')}")
    print(f"  getattr(p, 'age'): {getattr(p, 'age')}")

    # getattr 带默认值（属性不存在时不报错）
    # 【C# 对比】需要先 null 检查
    print(f"  getattr(p, 'email', 'N/A'): {getattr(p, 'email', 'N/A')}")

    # getattr 获取方法
    # 【C# 对比】typeof(Person).GetMethod("Greet").Invoke(p, null)
    greet_method = getattr(p, "greet")
    print(f"  调用方法: {greet_method()}")

    # setattr —— 动态设置属性
    # 【C# 对比】typeof(Person).GetProperty("Name").SetValue(p, "Bob")
    setattr(p, "name", "Bob")
    print(f"  setattr 后: {p}")

    # 动态添加新属性
    setattr(p, "email", "bob@example.com")
    print(f"  新增属性: email = {p.email}")

    # delattr —— 动态删除属性
    # 【C# 对比】C# 没有直接对应（属性不能运行时删除）
    delattr(p, "email")
    has_email = hasattr(p, "email")
    print(f"  删除后 has_email: {has_email}")

    # hasattr —— 检查属性是否存在
    # 【C# 对比】typeof(Person).GetProperty("name") != null
    print(f"  hasattr(p, 'name'): {hasattr(p, 'name')}")
    print(f"  hasattr(p, 'salary'): {hasattr(p, 'salary')}")

    print("  【C# 对比】C# 反射需要类型信息，Python 只需要字符串名称")


# =============================================================================
# 6. dataclasses.fields() —— 反射 dataclass 字段
# =============================================================================
# 【C# 对比】
# C# record:
#   typeof(Person).GetProperties() 获取所有属性
# Python dataclass:
#   fields(Person) 获取所有字段信息


@dataclass
class Employee:
    """员工数据类"""
    name: str
    age: int
    department: str
    salary: float = 50000.0


@dataclass(frozen=True)
class Point:
    """不可变点"""
    x: float
    y: float


def demo_dataclass_reflection():
    """演示 dataclass 字段反射"""
    print("\n=== 6. dataclasses.fields() 反射 ===")

    # 获取字段信息
    # 【C# 对比】typeof(Employee).GetProperties()
    for field in fields(Employee):
        print(f"  字段: {field.name}, 类型: {field.type}, "
              f"默认值: {field.default}")

    print()

    # 实际应用：序列化为字典
    def to_dict(obj: Any) -> dict:
        """将 dataclass 转为字典（反射实现）"""
        return {f.name: getattr(obj, f.name) for f in fields(type(obj))}

    emp = Employee("Alice", 30, "Engineering", 85000)
    d = to_dict(emp)
    print(f"  to_dict: {d}")
    print(f"  类型: {type(d)}")

    # 比较两个 dataclass
    emp2 = Employee("Alice", 30, "Engineering", 85000)
    print(f"\n  emp == emp2: {emp == emp2}")  # True（dataclass 自动生成 __eq__）

    pt1 = Point(1.0, 2.0)
    pt2 = Point(1.0, 2.0)
    print(f"  Point(1,2) == Point(1,2): {pt1 == pt2}")

    print("  【C# 对比】C# record 自带值相等比较")


# =============================================================================
# 7. 综合对比
# =============================================================================

def demo_comparison():
    """元类与反射对比"""
    print("\n=== 7. Python vs C# 元类与反射对比 ===")
    print("  ┌─────────────────────┬─────────────────────┬─────────────────────┐")
    print("  │ Python              │ C#                  │ 说明                │")
    print("  ├─────────────────────┼─────────────────────┼─────────────────────┤")
    print("  │ type(cls)           │ typeof(T)           │ 获取类型            │")
    print("  │ type(\"C\",bases,ns)  │ Activator           │ 动态创建类型        │")
    print("  │ metaclass           │ (无直接对应)         │ 控制类创建          │")
    print("  │ __init_subclass__   │ Attribute+反射       │ 子类自动注册        │")
    print("  │ getattr(obj,k)      │ PropertyInfo.GetValue│ 动态获取属性        │")
    print("  │ setattr(obj,k,v)    │ PropertyInfo.SetValue│ 动态设置属性        │")
    print("  │ delattr(obj,k)      │ (不支持)             │ 动态删除属性        │")
    print("  │ fields(dc)          │ GetProperties()     │ 获取字段/属性列表   │")
    print("  └─────────────────────┴─────────────────────┴─────────────────────┘")
    print("  核心区别: Python 一切皆对象，反射更灵活; C# 反射受类型系统约束")


# =============================================================================
# 主程序入口
# =============================================================================

def main():
    """运行所有演示"""
    print("=" * 60)
    print("  C# 老兵的 Python 修炼手册 — 5.5 元类与反射")
    print("=" * 60)

    demo_type_function()
    demo_metaclass_basics()
    demo_singleton()
    demo_init_subclass()
    demo_reflection()
    demo_dataclass_reflection()
    demo_comparison()

    print("\n" + "=" * 60)
    print("  核心结论：")
    print("  1. Python 元类控制类的创建，C# 没有直接对应")
    print("  2. __init_subclass__ 是元类的简化替代方案")
    print("  3. Python 反射比 C# 更简洁（getattr/setattr/delattr）")
    print("  4. Python type() 可以动态创建类型，C# 需要 Expression Trees")
    print("  5. dataclasses.fields() 提供 dataclass 的字段反射")
    print("  6. Python 元类 = C# 特性 + 反射 + 代码生成的组合")
    print("=" * 60)


if __name__ == "__main__":
    main()
