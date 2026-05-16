# Python 元组与解包示例
# 对应文章：1.10 元组与解包

# ==================== 元组创建 ====================
print("=== 元组创建 ===")
t1 = (1, "hello")           # 标准写法
t2 = 1, "hello"             # 不加括号也行！
t3 = (1,)                   # 单元素元组（必须加逗号！不加就是 int）
t4 = tuple([1, 2, 3])      # 从列表创建

print(f"t1 = {t1}")
print(f"t3 = {t3}  (注意逗号！)")
print(f"(1) 的类型: {type((1))}")     # <class 'int'>（不是元组！）
print(f"(1,) 的类型: {type((1,))}")   # <class 'tuple'>

# ==================== 访问 ====================
print("\n=== 访问 ===")
print(f"t1[0]  = {t1[0]}")    # 1
print(f"t1[-1] = {t1[-1]}")   # "hello"（支持负数索引）
# 元组是不可变的！
# t1[0] = 99  # TypeError!

# ==================== 解包赋值 ====================
print("\n=== 解包赋值 ===")
age, name = t1
print(f"{name} is {age}")

# 交换变量（不需要临时变量！Python 独有的优雅）
x, y = 1, 2
x, y = y, x
print(f"交换后: x={x}, y={y}")

# 忽略值（用 _）
_, name = 1, "Alice"
print(f"忽略第一个: {name}")

# * 接收多余值
first, *rest = [1, 2, 3, 4]
print(f"first={first}, rest={rest}")  # first=1, rest=[2, 3, 4]

# *middle 接收中间部分
first, *middle, last = [1, 2, 3, 4, 5]
print(f"first={first}, middle={middle}, last={last}")
# first=1, middle=[2, 3, 4], last=5

# 嵌套解构
(a, b), (c, d) = (1, 2), (3, 4)
print(f"a={a}, b={b}, c={c}, d={d}")

# ==================== 函数多值返回 ====================
print("\n=== 函数多值返回 ===")
def divide(a, b):
    """返回商和余数"""
    return a // b, a % b  # 自动打包成元组

quotient, remainder = divide(10, 3)
print(f"10 ÷ 3 = {quotient} 余 {remainder}")

# 返回多个值（实际就是返回元组）
def get_user_info():
    return "Alice", 25, "alice@example.com"

name, age, email = get_user_info()
print(f"用户: {name}, {age}岁, {email}")

# ==================== 命名元组 ====================
print("\n=== 命名元组 ===")
from collections import namedtuple

Person = namedtuple('Person', ['name', 'age', 'email'])
p = Person("Alice", 25, "alice@example.com")
print(f"名字: {p.name}")    # "Alice"（按名字访问）
print(f"年龄: {p[1]}")      # 25（也可以用索引访问）
print(f"元组: {p}")         # Person(name='Alice', age=25, email='alice@example.com')

# 带默认值的命名元组
Point = namedtuple('Point', ['x', 'y'], defaults=[0, 0])
p1 = Point(1, 2)
p2 = Point(3)        # y 使用默认值 0
print(f"p1={p1}, p2={p2}")

# ==================== typing.NamedTuple（推荐） ====================
print("\n=== typing.NamedTuple（更现代的写法） ===")
from typing import NamedTuple

class User(NamedTuple):
    name: str
    age: int
    email: str = ""   # 带默认值

u = User("Bob", 30)
print(f"User: {u}")
print(f"名字: {u.name}")

# ==================== *args 和 **kwargs ====================
print("\n=== *args 和 **kwargs ===")

# *args：接收任意数量的位置参数（打包成元组）
def sum_numbers(*args):
    print(f"  args = {args}")      # (1, 2, 3, 4, 5)
    return sum(args)

total = sum_numbers(1, 2, 3, 4, 5)
print(f"  sum = {total}")

# **kwargs：接收任意数量的关键字参数（打包成字典）
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

print_info(name="Alice", age=25, email="alice@example.com")

# 混合使用（顺序：普通参数 -> *args -> 默认参数 -> **kwargs）
def flexible(a, b, *args, option=True, **kwargs):
    print(f"  a={a}, b={b}, args={args}, option={option}, kwargs={kwargs}")

flexible(1, 2, 3, 4, option=False, x=10, y=20)

# 解包参数
args_list = [1, 2, 3]
kwargs_dict = {"name": "Alice", "age": 25}
def show(a, b, c, name="", age=0):
    print(f"  a={a}, b={b}, c={c}, name={name}, age={age}")
show(*args_list, **kwargs_dict)
