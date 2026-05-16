# ============================================================
# Python 继承与多态 —— 对比 C# 理解 Python 的继承体系
# 对应文章：3.3 继承与多态
# ============================================================
# 核心区别：
#   C# 只支持单继承（类），多继承通过接口实现
#   Python 支持多继承（类和接口都可以多继承）
# ============================================================

from abc import ABC, abstractmethod
import json


# ============================================================
# 1. 单继承 —— Python 和 C# 最相似的部分
# ============================================================
# C# 等价：public class Dog : Animal { }

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name!r})"


class Dog(Animal):
    def speak(self):
        return "汪汪！"


class Cat(Animal):
    def speak(self):
        return "喵喵！"


print("=" * 50)
print("1. 单继承 & 方法重写")
print("=" * 50)

dog = Dog("旺财")
cat = Cat("咪咪")
print(f"dog = {dog}, speak = {dog.speak()}")
print(f"cat = {cat}, speak = {cat.speak()}")
# 多态：同一个 speak() 方法，不同行为
animals = [dog, cat]
for animal in animals:
    print(f"  {animal.name} says: {animal.speak()}")


# ============================================================
# 2. 多继承 —— Python 的独特能力
# ============================================================
# C# 等价：用多个接口（interface）实现，接口可带 default 方法（C# 8+）
# Python 直接继承多个类，没有接口的概念

class Flyable:
    def fly(self):
        return "在天空翱翔"


class Swimmable:
    def swim(self):
        return "在水中畅游"


class Duck(Animal, Flyable, Swimmable):
    def speak(self):
        return "嘎嘎！"


print("\n" + "=" * 50)
print("2. 多继承 —— Python 独有（C# 用接口实现）")
print("=" * 50)

duck = Duck("唐老鸭")
print(f"duck = {duck}")
print(f"speak: {duck.speak()}")    # 继承自 Animal
print(f"fly:   {duck.fly()}")      # 继承自 Flyable
print(f"swim:  {duck.swim()}")     # 继承自 Swimmable


# ============================================================
# 3. super() 调用父类
# ============================================================
# C# 等价：base.Method()
# Python 的 super() 支持多继承，按 MRO 顺序调用

class Parent:
    def __init__(self, name):
        self.name = name
        print(f"  Parent.__init__({name})")

    def method(self):
        return "Parent.method"


class Child(Parent):
    def __init__(self, name, extra):
        super().__init__(name)     # 调用父类 __init__
        self.extra = extra
        print(f"  Child.__init__({name}, {extra})")

    def method(self):
        parent_result = super().method()  # 调用父类 method
        return f"{parent_result} -> Child.method"


print("\n" + "=" * 50)
print("3. super() 调用父类 —— C# 等价：base.Method()")
print("=" * 50)

child = Child("小明", "附加数据")
print(f"child.name = {child.name}")
print(f"child.extra = {child.extra}")
print(f"method() 调用链: {child.method()}")


# ============================================================
# 4. MRO（方法解析顺序）
# ============================================================
# C# 没有 MRO——单继承链一目了然
# Python 用 C3 线性化算法确定多继承时的方法查找顺序
# C3 算法确保：子类始终在父类之前，兄弟类保持声明顺序

class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):
    pass


print("\n" + "=" * 50)
print("4. MRO（方法解析顺序）—— Python 独有")
print("=" * 50)

print(f"D 的 MRO: {[c.__name__ for c in D.__mro__]}")
# ['D', 'B', 'C', 'A', 'object']

d = D()
print(f"D.method() = {d.method()}")
# 按 MRO 顺序查找：D -> B -> C -> A -> object
# 所以返回 "B"

# 验证：从右到左看 MRO，确认 C3 线性化规则
print(f"\nD 的继承链详解:")
for i, cls in enumerate(D.__mro__):
    arrow = "->" if i < len(D.__mro__) - 1 else ""
    print(f"  [{i}] {cls.__name__} {arrow}")


# ============================================================
# 5. isinstance() 和 issubclass()
# ============================================================
# C# 等价：is 运算符 + is T 子类判断
# Python 的 isinstance 支持检查元组中的任一类型

class Base:
    pass

class Derived(Base):
    pass

class Unrelated:
    pass


print("\n" + "=" * 50)
print("5. isinstance() 和 issubclass() —— 运行时类型检查")
print("=" * 50)

obj = Derived()
print(f"isinstance(obj, Derived) = {isinstance(obj, Derived)}")  # True
print(f"isinstance(obj, Base)    = {isinstance(obj, Base)}")     # True（继承关系）
print(f"isinstance(obj, (Base, Unrelated)) = {isinstance(obj, (Base, Unrelated))}")  # True（元组任一）

print(f"issubclass(Derived, Base) = {issubclass(Derived, Base)}")    # True
print(f"issubclass(Base, Derived) = {issubclass(Base, Derived)}")    # False
print(f"issubclass(Dog, Animal)   = {issubclass(Dog, Animal)}")      # True
print(f"issubclass(Duck, Flyable) = {issubclass(Duck, Flyable)}")    # True

# Python 还支持自定义 isinstance 行为（__instancecheck__）
class CustomMeta(type):
    """自定义元类，覆盖 isinstance 的行为"""
    def __instancecheck__(cls, instance):
        # 任何有 "duck_type" 属性的对象都被视为 DuckType 的实例
        return hasattr(instance, "duck_type") and instance.duck_type == "duck"

class DuckType(metaclass=CustomMeta):
    pass

class FakeDuck:
    duck_type = "duck"

print(f"\n自定义 __instancecheck__:")
print(f"isinstance(FakeDuck(), DuckType) = {isinstance(FakeDuck(), DuckType)}")  # True!
print("  -> FakeDuck 没有继承 DuckType，但有 duck_type 属性")
print("  -> 这就是 'If it walks like a duck...'")


# ============================================================
# 6. Mixins 模式 —— Python 多继承的经典用法
# ============================================================
# C# 等价：C# 8+ 接口默认方法 (default interface methods)
# Mixin 不独立使用，而是通过多继承"混入"功能

class JsonMixin:
    """Mixin: 为任何类添加 JSON 序列化能力"""

    def to_json(self):
        """将对象转换为 JSON 字符串"""
        return json.dumps(self.__dict__, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, json_str):
        """从 JSON 字符串创建对象"""
        data = json.loads(json_str)
        return cls(**data)


class PrintableMixin:
    """Mixin: 为任何类添加格式化打印能力"""

    def pretty_print(self):
        """格式化打印对象所有属性"""
        cls_name = type(self).__name__
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{cls_name}({attrs})"


class LoggableMixin:
    """Mixin: 为任何类添加日志能力"""

    def log(self, message):
        cls_name = type(self).__name__
        print(f"  [{cls_name}] {message}")


# 使用 Mixin：一个类同时获得多种能力
class User(JsonMixin, PrintableMixin, LoggableMixin):
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def greet(self):
        self.log(f"Hello, I'm {self.name}")
        return f"Hello, I'm {self.name}"


print("\n" + "=" * 50)
print("6. Mixins 模式 —— Python 多继承的经典用法")
print("=" * 50)
print("（C# 8+ 用接口默认方法实现类似效果）\n")

user = User("Alice", "alice@example.com")

# 从 JsonMixin 获得的能力
json_str = user.to_json()
print(f"to_json():\n{json_str}")

# 从 PrintableMixin 获得的能力
print(f"\npretty_print(): {user.pretty_print()}")

# 从 LoggableMixin 获得的能力
print(f"\ngreet() 输出:")
user.greet()

# 从 JsonMixin 恢复对象
user2 = User.from_json(json_str)
print(f"\nfrom_json() -> user2.pretty_print(): {user2.pretty_print()}")
print(f"user == user2? name={user.name == user2.name}, email={user.email == user2.email}")


# ============================================================
# 7. 抽象类 —— 强制子类实现特定接口
# ============================================================
# C# 等价：abstract class + abstract method
# Python 用 ABC（Abstract Base Class）和 @abstractmethod

class Shape(ABC):
    """抽象基类 —— C# 等价：public abstract class Shape"""

    @property
    @abstractmethod
    def area(self):
        """抽象属性 —— C# 等价：public abstract double Area { get; }"""
        pass

    @abstractmethod
    def calculate_area(self):
        """抽象方法 —— C# 等价：public abstract double CalculateArea()"""
        pass

    # 非抽象方法——可以有默认实现
    def describe(self):
        """非抽象方法 —— 子类可以直接使用"""
        return f"面积 = {self.calculate_area():.2f}"


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return self.calculate_area()

    def calculate_area(self):
        return 3.14159 * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.calculate_area()

    def calculate_area(self):
        return self.width * self.height


print("\n" + "=" * 50)
print("7. 抽象类 —— 强制子类实现接口")
print("=" * 50)

# shape = Shape()  # TypeError: Can't instantiate abstract class

circle = Circle(5)
rect = Rectangle(4, 6)

print(f"Circle(r=5).area      = {circle.area:.2f}")
print(f"Circle(r=5).describe() = {circle.describe()}")
print(f"Rectangle(4,6).area    = {rect.area:.2f}")
print(f"Rectangle(4,6).describe() = {rect.describe()}")

# 多态：通过抽象基类统一调用
shapes = [circle, rect]
print(f"\n所有形状:")
for s in shapes:
    print(f"  {type(s).__name__}: {s.describe()}")


# ============================================================
# 8. 综合对比总结
# ============================================================

print("\n" + "=" * 50)
print("8. C# vs Python 继承多态对比总结")
print("=" * 50)

summary = """
| 概念               | C#                          | Python                       |
|--------------------|-----------------------------|------------------------------|
| 单继承             | class Dog : Animal          | class Dog(Animal)            |
| 多继承             | class D : A, IB, IC         | class D(A, B, C)             |
| 接口               | interface IFoo              | Protocol / 普通类 + Mixin    |
| 调用父类           | base.Method()              | super().method()             |
| 抽象类             | abstract class Shape        | class Shape(ABC)             |
| 抽象方法           | abstract void Foo()         | @abstractmethod              |
| 方法重写           | override void Foo()         | def foo(self)                |
| 虚方法(可重写)     | virtual void Foo()          | 普通方法(默认可重写)         |
| sealed(不可继承)   | sealed class Dog            | 无等价机制                   |
| 运行时类型检查     | is / as / GetType()         | isinstance() / issubclass()  |
| 多态               | 虚方法 + override           | 方法重写 + duck typing        |
| MRO                | 无(单继承)                  | C3 线性化(__mro__)           |
| Mixin              | 接口默认方法(C# 8+)         | 多继承 + 普通类              |
"""
print(summary)

print("要点：")
print("  1. Python 多继承是核心特性，Mixin 是经典模式")
print("  2. C# 通过接口 + 默认方法逼近 Python 的 Mixin")
print("  3. Python 的 duck typing 让 '类型' 没那么重要")
print("  4. MRO 让多继承的方法查找变得可预测")
