# ============================================================
# Python 类定义 —— 对比 C# 理解 Python 类
# 对应文章：3.1 类的定义
# ============================================================
# C# 等价：class 是引用类型，Python 的 class 同样如此，
# 但 Python 的类本身也是对象（一切都是对象）。
# ============================================================

from dataclasses import dataclass, field

# ============================================================
# 1. 基本类定义 & __init__
# ============================================================
# Python __init__ ≈ C# 构造函数
# 注意：Python 没有"字段"和"属性"的语法区分，
# 所有成员都通过 self.xxx 访问

class Person:
    # 类变量 —— C# 等价：static 字段
    instance_count = 0

    def __init__(self, name, age):
        # 实例变量 —— C# 等价：字段
        self.name = name          # public —— 任何地方都能访问
        self._age = age           # _ 前缀 —— 约定为"受保护"
        self.__secret = "hidden"  # __ 前缀 —— 名称改写（name mangling）
        Person.instance_count += 1

    def greet(self):
        return f"Hello, I'm {self.name}, age {self._age}"

    # __str__ —— 对象的"友好字符串"
    # C# 等价：重写 ToString()
    def __str__(self):
        return f"Person(name={self.name}, age={self._age})"

    # __repr__ —— 对象的"开发者字符串"，用于调试
    # C# 没有直接等价，最接近的是 debuggerDisplay 属性
    def __repr__(self):
        return f"Person(name={self.name!r}, age={self._age!r})"


print("=" * 50)
print("1. 基本类定义 & __init__")
print("=" * 50)

person = Person("Alice", 25)
print(person.greet())           # Hello, I'm Alice, age 25
print(f"str:  {str(person)}")   # Person(name=Alice, age=25)
print(f"repr: {repr(person)}")  # Person(name='Alice', age=25)
print(f"实例计数: {Person.instance_count}")

# 也可以只重写 __repr__，Python 会用 __repr__ 作为 __str__ 的后备
# 但最好两个都写——__str__ 给用户看，__repr__ 给开发者看


# ============================================================
# 2. @property —— Python 的"属性"语法
# ============================================================
# C# 等价：get/set 属性（Property）
# Python 用 @property 装饰器实现类似效果

class PersonWithProperty:
    def __init__(self, name, age):
        self._name = name   # _ 前缀表示"请通过 property 访问"
        self._age = age

    # 只读 property（只有 getter）
    @property
    def name(self):
        """只读属性 —— C# 等价：{ get; }"""
        return self._name

    # 可读可写 property（有 getter 和 setter）
    @property
    def age(self):
        """可读可写属性 —— C# 等价：{ get; set; }"""
        return self._age

    @age.setter
    def age(self, value):
        if value < 0 or value > 150:
            raise ValueError(f"年龄 {value} 不在合理范围内")
        self._age = value


print("\n" + "=" * 50)
print("2. @property —— Python 的属性语法")
print("=" * 50)

pp = PersonWithProperty("Bob", 30)
print(f"姓名: {pp.name}")     # Bob —— 只读，不能 pp.name = "xxx"
print(f"年龄: {pp.age}")       # 30
pp.age = 31
print(f"新年龄: {pp.age}")    # 31

try:
    pp.name = "Charlie"        # AttributeError —— 没有 setter
except AttributeError as e:
    print(f"设置只读属性报错: {e}")

try:
    pp.age = -5                # ValueError
except ValueError as e:
    print(f"设置非法年龄报错: {e}")


# ============================================================
# 3. 类变量 vs 实例变量
# ============================================================
# 类变量：所有实例共享 —— C# 等价：static 字段
# 实例变量：每个实例独有 —— C# 等价：实例字段

class Counter:
    total_count = 0            # 类变量

    def __init__(self, label):
        self.label = label     # 实例变量
        self.count = 0         # 实例变量
        Counter.total_count += 1


print("\n" + "=" * 50)
print("3. 类变量 vs 实例变量")
print("=" * 50)

c1 = Counter("A")
c2 = Counter("B")
print(f"c1.label={c1.label}, c1.count={c1.count}")
print(f"c2.label={c2.label}, c2.count={c2.count}")
print(f"Counter.total_count = {Counter.total_count}")  # 2
# 类变量通过类名访问，也可以通过实例访问（不推荐）
# 实例同名属性会"遮蔽"类变量


# ============================================================
# 4. __slots__ —— 限制实例可以拥有的属性
# ============================================================
# C# 等价：没有直接等价物，最接近的是 readonly struct
# __slots__ 的好处：
#   1. 节省内存（不创建 __dict__）
#   2. 防止拼写错误导致意外创建属性
#   3. 加速属性访问

class SlottedPerson:
    __slots__ = ('name', 'age')   # 只允许这两个属性

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"SlottedPerson(name={self.name!r}, age={self.age!r})"


print("\n" + "=" * 50)
print("4. __slots__ —— 限制实例属性")
print("=" * 50)

sp = SlottedPerson("David", 40)
print(sp)
print(f"有 __dict__ 吗？{hasattr(sp, '__dict__')}")  # False

try:
    sp.email = "david@example.com"   # AttributeError!
except AttributeError as e:
    print(f"添加未声明属性报错: {e}")

# __slots__ 继承注意：子类需要再次声明 __slots__
# 否则子类仍会创建 __dict__


# ============================================================
# 5. 运算符重载
# ============================================================
# C# 等价：运算符重载（operator overloading）
# Python 通过双下划线方法（dunder methods）实现

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """运算符 + —— C# 等价：public static Vector operator +(Vector a, Vector b)"""
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        """运算符 * —— C# 等价：public static Vector operator *(Vector a, double b)"""
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        """运算符 == —— C# 等价：重写 Equals + IEquatable<T>"""
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"


print("\n" + "=" * 50)
print("5. 运算符重载")
print("=" * 50)

v1 = Vector(1, 2)
v2 = Vector(3, 4)
v3 = v1 + v2
print(f"v1 = {v1}")
print(f"v2 = {v2}")
print(f"v1 + v2 = {v3}")           # (4, 6)
print(f"v1 * 3 = {v1 * 3}")        # (3, 6)
print(f"v1 == Vector(1, 2)? {v1 == Vector(1, 2)}")  # True
print(f"v1 == v2? {v1 == v2}")     # False


# ============================================================
# 6. @dataclass —— 自动生成 __init__, __repr__, __eq__ 等
# ============================================================
# C# 9+ 等价：record 类型
# dataclass 自动为字段生成 __init__, __repr__, __eq__
# 省去了手写样板代码

@dataclass
class PersonDC:
    name: str
    age: int
    email: str = ""

    def greet(self):
        return f"Hello, I'm {self.name}"

# dataclass 自动提供：
#   __init__  => 等价于 C# 的主构造函数
#   __repr__  => 等价于 C# record 的 ToString()
#   __eq__    => 等价于 C# record 的 value-based 相等比较
#   还可以加 field() 实现更复杂的配置

@dataclass
class EmployeeDC:
    name: str
    salary: float
    tags: list = field(default_factory=list)  # 可变默认值要用 field
    id: int = field(default=0)                 # 带默认值的字段必须放在后面


print("\n" + "=" * 50)
print("6. @dataclass —— 等价于 C# 9+ record")
print("=" * 50)

pd1 = PersonDC("Alice", 25)
pd2 = PersonDC("Alice", 25)
pd3 = PersonDC("Bob", 30)
print(f"pd1 = {pd1}")                       # PersonDC(name='Alice', age=25, email='')
print(f"pd2 = {pd2}")
print(f"pd1 == pd2? {pd1 == pd2}")          # True（value-based 比较）
print(f"pd1 == pd3? {pd1 == pd3}")          # False
print(f"pd1.greet(): {pd1.greet()}")

emp = EmployeeDC("Charlie", 80000, id=1)
print(f"emp = {emp}")                       # EmployeeDC(name='Charlie', salary=80000.0, tags=[], id=1)


# ============================================================
# 7. frozen=True dataclass —— 不可变数据类
# ============================================================
# C# 等价：record struct（C# 10+）或 readonly struct
# frozen dataclass 创建后字段不可修改，且可哈希（可作字典 key / 集合元素）

@dataclass(frozen=True)
class Point:
    x: float
    y: float
    # frozen=True 自动设置 __hash__，使其可哈希
    # 不可修改：赋值会抛出 FrozenInstanceError


print("\n" + "=" * 50)
print("7. frozen=True dataclass —— 不可变数据类")
print("=" * 50)

p1 = Point(3.0, 4.0)
p2 = Point(3.0, 4.0)
p3 = Point(1.0, 2.0)
print(f"p1 = {p1}")
print(f"p1 == p2? {p1 == p2}")          # True
print(f"hash(p1) == hash(p2)? {hash(p1) == hash(p2)}")  # True

# 可以放入集合或作为字典 key
points = {p1, p2, p3}
print(f"集合中有 {len(points)} 个不同的 Point")  # 2

try:
    p1.x = 10   # FrozenInstanceError
except Exception as e:
    print(f"修改 frozen 属性报错: {type(e).__name__}: {e}")


# ============================================================
# 8. 类作为命名空间（无实例类模式）
# ============================================================
# Python 允许定义一个"只用类变量/静态方法"的类，
# 从不实例化——仅作为命名空间组织代码
# C# 等价：static class（C# 2.0+）

class MathUtils:
    """一个纯静态方法容器 —— C# 等价：static class"""
    PI = 3.14159265358979

    @staticmethod
    def circle_area(radius):
        return MathUtils.PI * radius ** 2

    @staticmethod
    def factorial(n):
        if n <= 1:
            return 1
        return n * MathUtils.factorial(n - 1)


print("\n" + "=" * 50)
print("8. 类作为命名空间 —— 无实例类")
print("=" * 50)

print(f"PI = {MathUtils.PI}")
print(f"circle_area(5) = {MathUtils.circle_area(5):.2f}")
print(f"factorial(5) = {MathUtils.factorial(5)}")
# 更 Pythonic 的做法是用模块级别函数，但在组织大量工具函数时很有用


# ============================================================
# 9. 综合对比总结
# ============================================================

print("\n" + "=" * 50)
print("9. C# vs Python 类定义对比总结")
print("=" * 50)

summary = """
| 概念                | C#                       | Python                      |
|---------------------|--------------------------|-----------------------------|
| 类定义              | class Person { }         | class Person:               |
| 构造函数            | public Person(...)       | def __init__(self, ...)     |
| 属性                | public string Name { }   | @property                   |
| 静态字段            | static int Count         | 类变量                      |
| 静态方法            | static void Foo()        | @staticmethod               |
| 不可变类            | readonly struct / record | @dataclass(frozen=True)     |
| 值类型              | struct / record struct   | @dataclass(frozen=True)+hash|
| 字段限制            | readonly 修饰符          | __slots__                   |
| 隐藏实现            | private / internal       | _ 前缀约定                  |
| 命名空间工具类      | static class             | 类 + @staticmethod          |
| ToString()          | override string ToString | __str__ / __repr__          |
| 相等比较            | IEquatable<T>            | __eq__（@dataclass 自动生成）|
"""
print(summary)
