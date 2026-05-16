# Python 泛型 typing 示例
# 对应文章：3.7 泛型typing与CSharp泛型

from typing import (
    TypeVar, Generic, List, Dict, Optional,
    Callable, Protocol, Type, Any
)
from dataclasses import dataclass

# ========== 1. TypeVar —— 类型变量 ==========
T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

# ========== 2. 泛型类 ==========
class Stack(Generic[T]):
    """泛型栈"""
    def __init__(self) -> None:
        self._items: List[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("栈为空")
        return self._items.pop()

    def peek(self) -> T:
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

# 使用
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
print(f"整数栈弹出: {int_stack.pop()}")  # 2

str_stack: Stack[str] = Stack()
str_stack.push("hello")
print(f"字符串栈弹出: {str_stack.pop()}")  # hello

# ========== 3. 泛型函数 ==========
def first(items: List[T]) -> Optional[T]:
    """返回列表第一个元素"""
    return items[0] if items else None

def merge(dict1: Dict[K, V], dict2: Dict[K, V]) -> Dict[K, V]:
    """合并两个字典"""
    return {**dict1, **dict2}

print(f"first: {first([1, 2, 3])}")
print(f"merge: {merge({'a': 1}, {'b': 2})}")

# ========== 4. 类型约束 (bound) ==========
Number = TypeVar("Number", int, float, complex)

def add(a: Number, b: Number) -> Number:
    return a + b

print(f"add(1, 2) = {add(1, 2)}")
print(f"add(1.5, 2.5) = {add(1.5, 2.5)}")

# ========== 5. Protocol —— 结构化子类型（鸭子类型的类型化） ==========
class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:
    def draw(self) -> str:
        return "○"

class Square:
    def draw(self) -> str:
        return "□"

def draw_shape(shape: Drawable) -> None:
    print(f"绘制: {shape.draw()}")

draw_shape(Circle())  # [OK] Circle 有 draw 方法
draw_shape(Square())  # [OK] Square 有 draw 方法
# draw_shape("hello")  # [X] str 没有 draw 方法

# ========== 6. 实际场景：泛型仓储模式 ==========
@dataclass
class User:
    id: int
    name: str

@dataclass
class Product:
    id: int
    title: str
    price: float

class Repository(Generic[T]):
    def __init__(self, items: Optional[List[T]] = None):
        self._items = items or []

    def add(self, item: T) -> None:
        self._items.append(item)

    def get_all(self) -> List[T]:
        return self._items.copy()

    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        return next((item for item in self._items if predicate(item)), None)

user_repo: Repository[User] = Repository()
user_repo.add(User(1, "Alice"))
user_repo.add(User(2, "Bob"))

product_repo: Repository[Product] = Repository()
product_repo.add(Product(1, "Laptop", 999.99))

print(f"用户: {user_repo.find(lambda u: u.name == 'Alice')}")
print(f"商品: {product_repo.find(lambda p: p.price > 500)}")
