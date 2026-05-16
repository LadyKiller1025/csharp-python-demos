# =============================================================================
# Python 数据类示例 — C# 老兵的 Python 修炼手册 5.6
# 对应文章：5.6 dataclass
# 关键概念：@dataclass, field(), frozen, order, __post_init__,
#           __slots__, dataclass as dict
# =============================================================================
# 【C# vs Python 对比】
# C#: record, record struct, class with init-only properties
# Python: @dataclass —— 自动生成 __init__, __repr__, __eq__ 等方法
#
# C# record 比 Python dataclass 更强大：
#   - record 天然不可变 (init-only)
#   - record 自带 value equality
#   - record 支持 deconstruction
#
# Python dataclass 的优势：
#   - frozen=True 实现不可变
#   - __post_init__ 实现自定义初始化
#   - field() 精细控制每个字段
# =============================================================================

from dataclasses import dataclass, field, asdict, astuple, fields, replace
from typing import ClassVar
import json


# =============================================================================
# 1. 基础 dataclass —— 自动生成 __init__, __repr__, __eq__
# =============================================================================
# 【C# 对比】
# C#: public record Person(string Name, int Age);
# Python:
#   @dataclass
#   class Person:
#       name: str
#       age: int
#
# 两者都自动生成构造函数、ToString、Equals

@dataclass
class Person:
    """基础数据类——对比 C# record"""
    name: str
    age: int
    # @dataclass 自动生成:
    # __init__(self, name, age)
    # __repr__(self) -> "Person(name='Alice', age=25)"
    # __eq__(self, other) -> 值比较


@dataclass
class Point:
    """二维点"""
    x: float
    y: float


def demo_basic_dataclass():
    """演示基础 dataclass"""
    print("\n=== 1. 基础 @dataclass（对比 C# record） ===")

    # 创建实例
    p = Person("Alice", 25)
    print(f"  创建: {p}")  # 自动调用 __repr__

    # 值相等
    p2 = Person("Alice", 25)
    print(f"  p == p2: {p == p2}")  # True（自动调用 __eq__）

    # 不同值不等
    p3 = Person("Bob", 30)
    print(f"  p == p3: {p == p3}")  # False

    # Point
    pt = Point(3.14, 2.72)
    print(f"  Point: {pt}")

    # 访问属性
    print(f"  p.name: {p.name}")
    print(f"  p.age: {p.age}")

    print("  【C# 对比】C# record 自带这些功能 + deconstruction")


# =============================================================================
# 2. field() —— 精细控制字段行为
# =============================================================================
# 【C# 对比】
# C# record 的每个参数都可以控制:
#   public record Person(string Name, int Age = 0);
# Python 用 field() 提供更丰富的选项


@dataclass
class Employee:
    """员工——演示 field() 的各种用法"""
    name: str
    department: str

    # 默认值——不用 field() 也行
    age: int = 25

    # field(default_factory=list) 避免可变默认值陷阱
    # 【C# 对比】C# record 没有这个问题（不可变）
    skills: list[str] = field(default_factory=list)

    # field(repr=False) 不在 __repr__ 中显示
    # 【C# 对比】C# [JsonIgnore] 类似
    internal_id: int = field(default=0, repr=False)

    # field(compare=False) 不参与 __eq__ 比较
    salary: float = field(default=50000.0, compare=False)

    # field(init=False) 不在 __init__ 参数中
    # 【C# 对比】C# 没有直接对应
    hire_date: str = field(init=False, default="2024-01-01")


def demo_field():
    """演示 field() 用法"""
    print("\n=== 2. field() 精细控制 ===")

    emp1 = Employee("Alice", "Engineering", skills=["Python", "C#"])
    emp2 = Employee("Alice", "Engineering", skills=["Python", "C#"])

    print(f"  emp1: {emp1}")  # hire_date 和 internal_id 不显示
    print(f"  emp1 == emp2: {emp1 == emp2}")  # salary 不参与比较

    # field(default_factory) 避免可变默认值陷阱
    emp3 = Employee("Bob", "Marketing")
    emp4 = Employee("Charlie", "Sales")
    print(f"  emp3.skills: {emp3.skills}")
    print(f"  emp4.skills: {emp4.skills}")
    # 每个实例有独立的 skills 列表（不会共享）

    print("  【C# 对比】C# record 的 init-only 属性更简洁")


# =============================================================================
# 3. frozen=True —— 不可变 dataclass
# =============================================================================
# 【C# 对比】
# C#: public record Point(double X, double Y);  (天然不可变)
# Python: @dataclass(frozen=True) 实现不可变
#
# frozen=True 做了什么：
# 1. 所有字段变成只读
# 2. 自动生成 __hash__ (可以作为 dict 的 key)
# 3. 赋值会抛出 FrozenInstanceError


@dataclass(frozen=True)
class ImmutablePoint:
    """不可变点——对比 C# record"""
    x: float
    y: float

    def distance_to(self, other: "ImmutablePoint") -> float:
        """计算两点距离"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


def demo_frozen():
    """演示 frozen=True"""
    print("\n=== 3. frozen=True（对比 C# record 不可变） ===")

    p1 = ImmutablePoint(3.0, 4.0)
    p2 = ImmutablePoint(6.0, 8.0)

    print(f"  p1: {p1}")
    print(f"  p2: {p2}")
    print(f"  距离: {p1.distance_to(p2):.2f}")

    # frozen=True 使实例可以哈希
    point_set = {p1, p2}
    print(f"  作为 set 元素: {len(point_set)} 个点")

    # 尝试修改会报错
    try:
        p1.x = 10.0  # FrozenInstanceError!
    except AttributeError as e:
        print(f"  尝试修改: {e}")

    print("  【C# 对比】C# record 天然不可变，不需要 frozen 参数")


# =============================================================================
# 4. order=True —— 自动生成比较方法
# =============================================================================
# 【C# 对比】
# C# record 默认实现 <, >, <=, >= (IComparable)
# Python dataclass 默认不生成比较方法（需要显式设置 order=True）


@dataclass(order=True)
class Student:
    """学生——支持比较操作"""
    grade: float
    name: str
    age: int


def demo_order():
    """演示 order=True"""
    print("\n=== 4. order=True（自动生成比较方法） ===")

    students = [
        Student(3.8, "Alice", 20),
        Student(3.5, "Bob", 22),
        Student(3.9, "Charlie", 21),
        Student(3.8, "David", 19),
    ]

    # 排序——按字段顺序比较
    sorted_students = sorted(students)
    print("  排序后:")
    for s in sorted_students:
        print(f"    {s}")

    # 比较操作
    s1 = Student(3.8, "Alice", 20)
    s2 = Student(3.5, "Bob", 22)
    print(f"\n  {s1.name} > {s2.name}: {s1 > s2}")  # True (grade: 3.8 > 3.5)

    print("  【C# 对比】C# record 默认实现 IComparable")


# =============================================================================
# 5. __post_init__ —— 自定义初始化逻辑
# =============================================================================
# 【C# 对比】
# C# 没有直接对应，需要:
#   - init-only 属性 + 构造函数逻辑
#   - record with 表达式
#   - 主构造函数 + 方法
#
# __post_init__ 在 __init__ 之后自动调用
# 可以修改字段、添加验证、计算派生字段


@dataclass
class Rectangle:
    """矩形——演示 __post_init__"""
    width: float
    height: float

    # __post_init__ 在 __init__ 之后调用
    # 可以访问所有字段，可以修改字段
    # 【C# 对比】C# init-only 属性无法在构造函数后修改
    def __post_init__(self):
        """自定义初始化逻辑"""
        if self.width < 0 or self.height < 0:
            raise ValueError("宽高不能为负数")
        # 添加计算字段
        # 注意: 需要用 object.__setattr__ 因为 frozen dataclass 会阻止赋值
        # 但这个 dataclass 不是 frozen，所以可以直接赋值

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


@dataclass(frozen=True)
class Circle:
    """圆——演示 frozen + __post_init__"""
    radius: float
    # 计算字段（init=False 避免在 __init__ 中传递）
    area: float = field(init=False)
    circumference: float = field(init=False)

    def __post_init__(self):
        """frozen dataclass 中用 object.__setattr__ 设置计算字段"""
        if self.radius < 0:
            raise ValueError("半径不能为负数")
        # frozen dataclass 不能直接赋值，需要绕过
        object.__setattr__(self, 'area', 3.14159 * self.radius ** 2)
        object.__setattr__(self, 'circumference', 2 * 3.14159 * self.radius)


def demo_post_init():
    """演示 __post_init__"""
    print("\n=== 5. __post_init__（对比 C# 构造函数逻辑） ===")

    rect = Rectangle(10.0, 5.0)
    print(f"  Rectangle: {rect}")
    print(f"  面积: {rect.area}")
    print(f"  周长: {rect.perimeter}")

    # 验证
    try:
        bad_rect = Rectangle(-1, 5)
    except ValueError as e:
        print(f"  验证: {e}")

    # Circle with frozen
    circle = Circle(5.0)
    print(f"\n  Circle: radius={circle.radius}")
    print(f"  面积: {circle.area:.2f}")
    print(f"  周长: {circle.circumference:.2f}")

    print("  【C# 对比】C# 用构造函数 + init-only 属性实现类似功能")


# =============================================================================
# 6. __slots__ —— 节省内存
# =============================================================================
# 【C# 对比】
# C# struct 是值类型，天然在栈上分配
# Python 对象都在堆上，__slots__ 可以减少内存开销
#
# __slots__ 做了什么：
# 1. 限制只能设置 __slots__ 中声明的属性
# 2. 使用固定大小的数组而不是字典存储属性
# 3. 减少内存使用（每个实例节省约 40-50% 内存）
# 4. 提高属性访问速度


@dataclass(slots=True)  # Python 3.10+
class OptimizedPoint:
    """使用 __slots__ 优化的点"""
    x: float
    y: float


def demo_slots():
    """演示 __slots__ 优化"""
    print("\n=== 6. __slots__（节省内存） ===")

    # 创建实例
    p = OptimizedPoint(3.0, 4.0)
    print(f"  OptimizedPoint: {p}")
    print(f"  可用属性: {dir(p)}")

    # 无法添加新属性（__slots__ 限制）
    try:
        p.z = 5.0  # AttributeError!
    except AttributeError as e:
        print(f"  限制新属性: {e}")

    # 内存对比（概念演示）
    import sys
    regular_pt = Point(3.0, 4.0)
    optimized_pt = OptimizedPoint(3.0, 4.0)
    print(f"  Point 大小: ~{sys.getsizeof(regular_pt)} bytes (估算)")
    print(f"  OptimizedPoint 大小: ~{sys.getsizeof(optimized_pt)} bytes (估算)")

    print("  【C# 对比】C# struct 是值类型，天然更省内存")


# =============================================================================
# 7. asdict / astuple —— 转换为字典和元组
# =============================================================================
# 【C# 对比】
# C# record 自带 ToDictionary() 或手动映射
# Python dataclass 提供 asdict() 和 astuple()


@dataclass
class UserConfig:
    """用户配置"""
    username: str
    email: str
    theme: str = "dark"
    language: str = "zh-CN"


def demo_asdict():
    """演示 asdict 和 astuple"""
    print("\n=== 7. asdict / astuple（序列化） ===")

    config = UserConfig("alice", "alice@example.com", theme="light")

    # 转为字典
    # 【C# 对比】record.ToDictionary() 或手动映射
    config_dict = asdict(config)
    print(f"  asdict: {config_dict}")
    print(f"  类型: {type(config_dict)}")

    # 转为 JSON
    json_str = json.dumps(config_dict, ensure_ascii=False, indent=2)
    print(f"  JSON:\n{json_str}")

    # 转为元组
    config_tuple = astuple(config)
    print(f"  astuple: {config_tuple}")

    # 从字典创建（用 ** 解包）
    new_config = UserConfig(**{"username": "bob", "email": "bob@example.com"})
    print(f"  从字典创建: {new_config}")

    print("  【C# 对比】C# 需要手写 ToDictionary 或用第三方库")


# =============================================================================
# 8. replace() —— 不可变更新
# =============================================================================
# 【C# 对比】
# C# record: var updated = person with { Name = "Bob" };
# Python: updated = replace(person, name="Bob")


def demo_replace():
    """演示 replace() 不可变更新"""
    print("\n=== 8. replace()（对比 C# with 表达式） ===")

    original = Person("Alice", 25)
    print(f"  原始: {original}")

    # 创建新实例并修改部分字段
    # 【C# 对比】var updated = person with { Age = 26 };
    updated = replace(original, age=26)
    print(f"  更新: {updated}")
    print(f"  原始不变: {original}")  # 原始实例不变
    print(f"  原始 == 更新: {original == updated}")  # False

    # 多个字段
    config = UserConfig("alice", "alice@example.com")
    new_config = replace(config, theme="light", language="en-US")
    print(f"\n  原始配置: {config}")
    print(f"  新配置: {new_config}")

    print("  【C# 对比】C# with 表达式语法更简洁: person with { Age = 26 }")


# =============================================================================
# 9. 继承与组合
# =============================================================================

@dataclass
class Address:
    """地址"""
    street: str
    city: str
    country: str = "中国"


@dataclass
class EmployeeWithAddress:
    """带地址的员工——演示组合"""
    name: str
    department: str
    address: Address


def demo_inheritance_composition():
    """演示继承和组合"""
    print("\n=== 9. 组合模式 ===")

    addr = Address("中关村大街1号", "北京")
    emp = EmployeeWithAddress("Alice", "Engineering", addr)

    print(f"  员工: {emp}")
    print(f"  地址: {emp.address}")
    print(f"  城市: {emp.address.city}")

    # asdict 会递归转换嵌套 dataclass
    emp_dict = asdict(emp)
    print(f"  asdict: {emp_dict}")

    print("  【C# 对比】C# record 同样支持嵌套组合")


# =============================================================================
# 10. 综合对比
# =============================================================================

def demo_comparison():
    """Python dataclass vs C# record 对比"""
    print("\n=== 10. Python dataclass vs C# record 对比 ===")
    print("  ┌──────────────────────┬──────────────────────┬──────────────────────┐")
    print("  │ Python dataclass     │ C# record            │ 说明                 │")
    print("  ├──────────────────────┼──────────────────────┼──────────────────────┤")
    print("  │ @dataclass           │ record               │ 基础数据类           │")
    print("  │ frozen=True          │ record (天然不可变)  │ 不可变               │")
    print("  │ order=True           │ IComparable          │ 比较操作             │")
    print("  │ __post_init__        │ 构造函数逻辑         │ 自定义初始化         │")
    print("  │ slots=True           │ struct               │ 内存优化             │")
    print("  │ asdict()             │ ToDictionary()       │ 序列化               │")
    print("  │ replace()            │ with 表达式          │ 不可变更新           │")
    print("  │ field()              │ init-only            │ 字段控制             │")
    print("  └──────────────────────┴──────────────────────┴──────────────────────┘")
    print("  核心区别: C# record 天然不可变+值相等，Python 需要显式配置")


# =============================================================================
# 主程序入口
# =============================================================================

def main():
    """运行所有演示"""
    print("=" * 60)
    print("  C# 老兵的 Python 修炼手册 — 5.6 数据类")
    print("=" * 60)

    demo_basic_dataclass()
    demo_field()
    demo_frozen()
    demo_order()
    demo_post_init()
    demo_slots()
    demo_asdict()
    demo_replace()
    demo_inheritance_composition()
    demo_comparison()

    print("\n" + "=" * 60)
    print("  核心结论：")
    print("  1. Python @dataclass ≈ C# record，但 C# record 更简洁")
    print("  2. frozen=True 实现不可变，C# record 天然不可变")
    print("  3. __post_init__ 实现自定义初始化（C# 用构造函数）")
    print("  4. asdict() 方便序列化，replace() 实现不可变更新")
    print("  5. field() 精细控制字段行为")
    print("  6. Python 3.10+ slots=True 优化内存")
    print("=" * 60)


if __name__ == "__main__":
    main()
