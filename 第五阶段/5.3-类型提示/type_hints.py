# =============================================================================
# Python 类型提示示例 — C# 老兵的 Python 修炼手册 5.3
# 对应文章：5.3 类型提示
# 关键概念：Type hints, TypedDict, Literal, Final, @overload, TypeGuard,
#           对比 C# nullable reference types, pattern matching
# =============================================================================
# 【C# vs Python 对比】
# C# 是静态类型语言，编译时强制类型检查
# Python 是动态类型语言，类型提示是可选的（运行时不做检查）
# Python 类型提示 = C# 的注释 + IDE 的智能提示 + mypy 静态检查
#
# 本质区别:
# C#: string name = "Alice";      // 编译器保证 name 是 string
# Python: name: str = "Alice"      # 只是提示，name 可以随时变成 int
# =============================================================================

from typing import (
    List, Dict, Optional, Union, Tuple, Set,
    Any, Callable, Iterator, TypeVar, Generic,
    TypedDict, Literal, Final, ClassVar, TypeGuard,
    overload, runtime_checkable, Protocol
)
import sys

# =============================================================================
# 1. 基础类型注解 —— C# 程序员最熟悉的部分
# =============================================================================
# 【C# 对比】
# C#: string name = "Alice";          Python: name: str = "Alice"
# C#: int age = 25;                   Python: age: int = 25
# C#: double price = 9.99;            Python: price: float = 9.99
# C#: bool is_active = true;          Python: is_active: bool = True


def demo_basic_types():
    """基础类型注解"""
    print("\n=== 1. 基础类型注解 ===")

    # 标量类型
    name: str = "Alice"            # C#: string
    age: int = 25                  # C#: int
    price: float = 9.99            # C#: double (Python float = C# double)
    is_active: bool = True         # C#: bool

    print(f"  str: {name} (类型: {type(name).__name__})")
    print(f"  int: {age} (类型: {type(age).__name__})")
    print(f"  float: {price} (类型: {type(price).__name__})")
    print(f"  bool: {is_active} (类型: {type(is_active).__name__})")

    # 动态类型仍然允许——类型提示只是"建议"
    # 【C# 对比】C# 不允许 string 变成 int（除非用 dynamic）
    name = 42  # Python: 合法，但 mypy 会报错
    print(f"  name 现在是: {name} (Python 允许，C# 不允许)")


# =============================================================================
# 2. 容器类型 —— 对比 C# 泛型集合
# =============================================================================
# 【C# 对比】
# C#: List<int> numbers = new List<int> { 1, 2, 3 };
# Python: numbers: list[int] = [1, 2, 3]  (Python 3.9+)
#
# C#: Dictionary<string, int> dict = new Dictionary<string, int>();
# Python: mapping: dict[str, int] = {}  (Python 3.9+)
#
# Python 3.9 之前需要用 typing 模块: List[int], Dict[str, int]
# Python 3.9+ 可以直接用内置类型: list[int], dict[str, int]


def demo_container_types():
    """容器类型注解"""
    print("\n=== 2. 容器类型（对比 C# 泛型集合） ===")

    # list - 对比 C# List<T> / T[]
    numbers: list[int] = [1, 2, 3, 4, 5]          # C#: List<int>
    names: List[str] = ["Alice", "Bob"]            # C#: string[]

    # dict - 对比 C# Dictionary<TKey, TValue>
    scores: dict[str, int] = {"Alice": 95, "Bob": 87}  # C#: Dictionary<string, int>

    # tuple - 对比 C# Tuple<T1, T2> 或 ValueTuple (T1, T2)
    point: tuple[float, float] = (3.14, 2.72)     # C#: (double, double)
    person: tuple[str, int] = ("Alice", 25)        # C#: (string, int)

    # set - 对比 C# HashSet<T>
    unique_ids: set[int] = {1, 2, 3}              # C#: HashSet<int>

    # 嵌套类型
    matrix: list[list[int]] = [[1, 2], [3, 4]]     # C#: List<List<int>>
    lookup: dict[str, list[int]] = {"a": [1, 2]}   # C#: Dictionary<string, List<int>>

    print(f"  list[int]: {numbers}")
    print(f"  dict[str, int]: {scores}")
    print(f"  tuple[float, float]: {point}")
    print(f"  set[int]: {unique_ids}")
    print(f"  list[list[int]]: {matrix}")


# =============================================================================
# 3. Optional 和 Union —— 对比 C# 的 nullable
# =============================================================================
# 【C# 对比】
# C#: string? name = null;              // nullable reference type (C# 8+)
# Python: name: Optional[str] = None   # 或 name: str | None = None (3.10+)
#
# C#: int? value = null;                // nullable value type
# Python: value: int | None = None
#
# C#: object obj = GetStringOrInt();    // Union 类似 object + 运行时检查
# Python: value: int | str = get_value()


def demo_optional_union():
    """Optional 和 Union 类型"""
    print("\n=== 3. Optional/Union（对比 C# nullable） ===")

    # Optional[str] = str | None = Union[str, None]
    # 【C# 对比】string? name = null;
    def find_user(user_id: int) -> Optional[str]:
        """返回用户名或 None"""
        # 【C# 对比】string? FindUser(int userId)
        users = {1: "Alice", 2: "Bob"}
        return users.get(user_id)  # 可能返回 None

    result = find_user(1)
    print(f"  find_user(1): {result}")
    result = find_user(999)
    print(f"  find_user(999): {result}")

    # Union — 多种类型之一
    # 【C# 对比】C# 用 object 或泛型约束，Python 直接声明多种类型
    def process_value(value: int | str) -> str:
        """接收 int 或 str"""
        # 【C# 对比】C# 用 pattern matching: switch (value) { int i => ..., string s => ... }
        if isinstance(value, int):
            return f"整数: {value * 2}"
        else:
            return f"字符串: {value.upper()}"

    print(f"  process_value(42): {process_value(42)}")
    print(f"  process_value('hello'): {process_value('hello')}")

    # Python 3.10+ 新语法: X | Y 替代 Union[X, Y]
    print(f"  Python 3.10+: int | str 替代 Union[int, str]")


# =============================================================================
# 4. TypedDict —— 对比 C# 的 class/record 作为数据结构
# =============================================================================
# 【C# 对比】
# C#: public record Person { string Name { get; init; } int Age { get; init; } }
# Python: class Person(TypedDict): name: str; age: int
#
# TypedDict 的特殊之处：它本质上还是 dict，但有固定的键和值类型
# 适合处理 JSON/API 响应等结构化数据


class UserProfile(TypedDict):
    """用户资料 —— 对比 C# 的 record 或 class"""
    name: str
    age: int
    email: str
    is_active: bool


class APIResponse(TypedDict, total=False):
    """API 响应（total=False 表示所有字段可选）"""
    data: dict
    error: str
    status_code: int


def demo_typed_dict():
    """TypedDict 使用演示"""
    print("\n=== 4. TypedDict（对比 C# record/class） ===")

    # 创建 TypedDict 实例（实际就是 dict）
    profile: UserProfile = {
        "name": "Alice",
        "age": 25,
        "email": "alice@example.com",
        "is_active": True,
    }

    print(f"  UserProfile: {profile}")
    print(f"  访问: profile['name'] = {profile['name']}")

    # 比普通 dict 多了类型检查
    # 【C# 对比】C# 的 record 会自动实现 Equals, GetHashCode, ToString
    # TypedDict 不会，它只是给 dict 加了类型信息

    # total=False 的 TypedDict —— 所有字段可选
    response: APIResponse = {"status_code": 200, "data": {"key": "value"}}
    print(f"  APIResponse (部分字段): {response}")

    print("  【C# 对比】C# record 天然不可变，TypedDict 是可变的 dict")


# =============================================================================
# 5. Literal —— 限定具体的字面量值
# =============================================================================
# 【C# 对比】
# C#: 无直接对应，用 enum 或 string + pattern matching
# C#: public enum Color { Red, Green, Blue }
# Python: color: Literal["red", "green", "blue"]


def set_color(color: Literal["red", "green", "blue"]) -> str:
    """设置颜色——只接受三个字面量值"""
    # 【C# 对比】C# 用 enum Color { Red, Green, Blue }
    return f"颜色设置为: {color}"


def demo_literal():
    """Literal 类型演示"""
    print("\n=== 5. Literal（对比 C# enum） ===")

    # Literal 限定参数只能是特定的字面量值
    print(f"  set_color('red'): {set_color('red')}")
    print(f"  set_color('green'): {set_color('green')}")

    # 配合 overload 使用
    # 【C# 对比】C# enum 更强大，可以关联值和方法
    print("  Literal 适合: 参数是有限的字符串/数字集合")
    print("  C# enum 适合: 需要关联值的场景")


# =============================================================================
# 6. Final —— 常量声明
# =============================================================================
# 【C# 对比】
# C#: public const double PI = 3.14159;
# C#: public static readonly string DEFAULT_NAME = "Alice";
# Python: PI: Final[float] = 3.14159  (告诉类型检查器不可修改)


# 模块级常量
PI: Final[float] = 3.14159
MAX_RETRIES: Final[int] = 3
DEFAULT_NAME: Final[str] = "Alice"


def demo_final():
    """Final 类型演示"""
    print("\n=== 6. Final（对比 C# const/readonly） ===")

    # Final 标记不可修改的变量
    # 【C# 对比】const = 编译时常量，readonly = 运行时常量
    print(f"  PI = {PI}")
    print(f"  MAX_RETRIES = {MAX_RETRIES}")
    print(f"  DEFAULT_NAME = {DEFAULT_NAME}")

    # Python 运行时仍然可以修改，但 mypy 会报错
    # PI = 3.0  # mypy error: Cannot reassign final name "PI"
    print("  Final 只是类型提示，运行时仍可修改（mypy 会报错）")
    print("  【C# 对比】const/readonly 是编译器强制的")


# =============================================================================
# 7. @overload —— 同一函数多种签名
# =============================================================================
# 【C# 对比】
# C# 本身支持方法重载（同名不同参数）
# Python 不支持方法重载，但用 @overload 告诉类型检查器不同的签名


@overload
def double_value(x: int) -> int: ...


@overload
def double_value(x: str) -> str: ...


def double_value(x: int | str) -> int | str:
    """根据输入类型返回不同结果
    
    【C# 对比】C# 直接写两个同名方法：
    public int DoubleValue(int x) => x * 2;
    public string DoubleValue(string s) => s + s;
    """
    if isinstance(x, int):
        return x * 2
    elif isinstance(x, str):
        return x * 2
    raise TypeError(f"不支持的类型: {type(x)}")


def demo_overload():
    """@overload 使用演示"""
    print("\n=== 7. @overload（对比 C# 方法重载） ===")

    print(f"  double_value(5): {double_value(5)}")
    print(f"  double_value('hi'): {double_value('hi')}")
    print("  Python 不支持真正的重载，@overload 只是类型提示")


# =============================================================================
# 8. TypeGuard —— 类型窄化
# =============================================================================
# 【C# 对比】
# C# pattern matching:
#   if (obj is string s) { /* s 是 string 类型 */ }
#   if (value is > 0 and < 100) { ... }
#
# Python TypeGuard:
#   def is_string(val: Any) -> TypeGuard[str]: ...
#   if is_string(val): /* mypy 知道 val 是 str */


def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    """检查列表中所有元素是否都是字符串
    
    TypeGuard 告诉类型检查器：
    如果返回 True，那么 val 的类型是 list[str]
    
    【C# 对比】C# pattern matching + is-expression
    """
    return all(isinstance(x, str) for x in val)


def is_positive_int(val: int) -> bool:
    """简单的类型检查"""
    return isinstance(val, int) and val > 0


def demo_type_guard():
    """TypeGuard 使用演示"""
    print("\n=== 8. TypeGuard（对比 C# pattern matching） ===")

    mixed_list: list[object] = ["hello", "world"]
    if is_string_list(mixed_list):
        # mypy 知道 mixed_list 是 list[str]
        joined = " ".join(mixed_list)
        print(f"  TypeGuard 窄化: '{joined}'")

    not_strings: list[object] = ["hello", 42]
    if not is_string_list(not_strings):
        print("  TypeGuard: 包含非字符串元素")

    print("  【C# 对比】C# pattern matching 更强大:")
    print("    if (obj is string s and { Length: > 0 }) { ... }")


# =============================================================================
# 9. Protocol —— 结构化子类型（鸭子类型的形式化）
# =============================================================================
# 【C# 对比】
# C#: interface IComparable<T> { int CompareTo(T other); }
# Python Protocol: 不需要显式继承，只要有相同的方法就是"兼容"的


class Drawable(Protocol):
    """可绘制对象的协议（不需要显式继承）"""
    def draw(self) -> str: ...


class Circle:
    """圆形——没有继承 Drawable，但实现了 draw 方法"""
    def draw(self) -> str:
        return "绘制圆形"


class Square:
    """正方形——也没有继承 Drawable"""
    def draw(self) -> str:
        return "绘制正方形"


def draw_shape(shape: Drawable) -> None:
    """接受任何实现了 draw 方法的对象"""
    print(f"  {shape.draw()}")


def demo_protocol():
    """Protocol 使用演示"""
    print("\n=== 9. Protocol（对比 C# interface） ===")

    # Circle 和 Square 都没有继承 Drawable
    # 但它们有 draw 方法，所以符合 Drawable 协议
    draw_shape(Circle())
    draw_shape(Square())
    print("  Python: 鸭子类型 + Protocol = 不需要显式实现接口")
    print("  C#: 必须显式实现 interface")


# =============================================================================
# 10. TypeVar 和 Generic —— 泛型
# =============================================================================
# 【C# 对比】
# C#: public T First<T>(List<T> list) { return list[0]; }
# Python: def first[T](lst: list[T]) -> T: return lst[0]  (Python 3.12+)

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)  # 协变


def first(lst: list[T]) -> T:
    """返回列表第一个元素"""
    # 【C# 对比】public T First<T>(List<T> list)
    return lst[0]


def demo_generics():
    """泛型使用演示"""
    print("\n=== 10. 泛型（对比 C# 泛型） ===")

    # Python 3.12+ 语法: def first[T](lst: list[T]) -> T
    # 旧语法: T = TypeVar("T"); def first(lst: list[T]) -> T
    print(f"  first([1, 2, 3]): {first([1, 2, 3])}")
    print(f"  first(['a', 'b']): {first(['a', 'b'])}")
    print("  Python 泛型 = C# 泛型，但 Python 是鸭子类型，不需要约束")


# =============================================================================
# 11. 综合对比
# =============================================================================

def demo_comparison():
    """Python vs C# 类型系统对比"""
    print("\n=== 11. Python vs C# 类型系统对比 ===")
    print("  ┌────────────────────┬────────────────────┬────────────────────┐")
    print("  │ Python             │ C#                 │ 说明               │")
    print("  ├────────────────────┼────────────────────┼────────────────────┤")
    print("  │ name: str          │ string name        │ 基础类型           │")
    print("  │ list[int]          │ List<int>          │ 泛型集合           │")
    print("  │ str | None         │ string?            │ 可空类型           │")
    print("  │ TypedDict          │ record/class       │ 结构化数据         │")
    print("  │ Literal['a','b']   │ enum               │ 限定值             │")
    print("  │ Final[x]           │ const/readonly     │ 不可变常量         │")
    print("  │ @overload          │ 方法重载           │ 多签名             │")
    print("  │ TypeGuard          │ is pattern         │ 类型窄化           │")
    print("  │ Protocol           │ interface          │ 结构化子类型       │")
    print("  │ TypeVar / [T]      │ <T>                │ 泛型               │")
    print("  └────────────────────┴────────────────────┴────────────────────┘")
    print("  核心区别: C# 编译时强制，Python 运行时可选 (mypy 静态检查)")


# =============================================================================
# 主程序入口
# =============================================================================

def main():
    """运行所有类型提示演示"""
    print("=" * 60)
    print("  C# 老兵的 Python 修炼手册 — 5.3 类型提示")
    print("=" * 60)

    demo_basic_types()
    demo_container_types()
    demo_optional_union()
    demo_typed_dict()
    demo_literal()
    demo_final()
    demo_overload()
    demo_type_guard()
    demo_protocol()
    demo_generics()
    demo_comparison()

    print("\n" + "=" * 60)
    print("  核心结论：")
    print("  1. Python 类型提示是可选的，C# 是强制的")
    print("  2. Python 用 mypy/pyright 做静态检查，类似 Roslyn")
    print("  3. Python 3.10+ 语法越来越接近 C#")
    print("  4. Protocol 实现了结构化子类型（鸭子类型的形式化）")
    print("=" * 60)


if __name__ == "__main__":
    main()
