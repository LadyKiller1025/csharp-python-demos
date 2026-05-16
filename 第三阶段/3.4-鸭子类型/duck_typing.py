# Python 鸭子类型示例
# 对应文章：3.4 鸭子类型 vs 接口
#
# 核心思想："如果它走起来像鸭子，叫起来像鸭子，那它就是鸭子"
# C# 等价：interface 约束 —— Python 不需要声明接口，只要对象有对应方法即可

print("=" * 60)
print("3.4 鸭子类型 vs 接口")
print("=" * 60)

# ========== 1. 基本鸭子类型：没有接口，只要方法匹配 ==========
# C# 等价：interface ISpeakable { void Speak(); }
# Python：不需要任何接口定义，只要有 speak() 方法就行

print("\n--- 1. 基本鸭子类型 ---")


class Dog:
    def speak(self):
        return "汪汪！"


class Cat:
    def speak(self):
        return "喵喵！"


# 方法参数不需要类型声明 —— 只要有 speak 方法就能传入
def make_speak(animal):
    """只要 animal 有 speak() 方法，就能调用。C# 等价：MakeSpeak(ISpeakable animal)"""
    return animal.speak()


print(f"Dog():  {make_speak(Dog())}")   # OK
print(f"Cat():  {make_speak(Cat())}")   # OK
# make_speak("hello")  # 运行时报错：str 没有 speak 方法


# ========== 2. 鸭子类型的威力：任何有 draw() 的对象 ==========
print("\n--- 2. draw_all：多态绘图 ---")


class Circle:
    def draw(self):
        return "画圆 ●"


class Rectangle:
    def draw(self):
        return "画矩形 ■"


class Arrow:
    def draw(self):
        return "画箭头 →"


# 任何有 draw() 方法的对象都能传入
# C# 等价：void DrawAll(IEnumerable<IDrawable> drawables)
def draw_all(drawables):
    results = []
    for d in drawables:
        results.append(d.draw())
    return results


shapes = [Circle(), Rectangle(), Arrow()]
print(f"draw_all: {draw_all(shapes)}")


# ========== 3. 迭代器协议 __iter__ / __next__ ==========
# C# 等价：IEnumerable<T> / IEnumerator<T>
# Python 鸭子类型：只要有 __iter__() 和 __next__() 就是迭代器

print("\n--- 3. 迭代器协议 __iter__ / __next__ ---")


class CountDown:
    """倒计时迭代器。C# 等价：实现 IEnumerable<int> 的GetEnumerator()"""
    def __init__(self, start):
        self.start = start
        self.current = start

    def __iter__(self):
        """返回迭代器自身。C# 等价：GetEnumerator()"""
        return self

    def __next__(self):
        """返回下一个值，耗尽时抛 StopIteration。C# 等价：MoveNext() + Current"""
        if self.current <= 0:
            raise StopIteration  # C# 等价：return false（MoveNext 返回 false）
        value = self.current
        self.current -= 1
        return value


# for 循环会自动调用 __iter__() 和 __next__()
countdown = [x for x in CountDown(5)]
print(f"CountDown(5): {countdown}")  # [5, 4, 3, 2, 1]

# 手动迭代演示
print("手动迭代:", end=" ")
it = iter(CountDown(3))  # 等价于调用 __iter__()
print(next(it), end=" ")  # 3
print(next(it), end=" ")  # 2
print(next(it))           # 1


# ========== 4. 上下文管理器协议 __enter__ / __exit__ ==========
# C# 等价：IDisposable + using 语句
# Python：只要有 __enter__() 和 __exit__() 方法，就能用 with 语句

print("\n--- 4. 上下文管理器协议 __enter__ / __exit__ ---")


class MyResource:
    """模拟资源管理。C# 等价：class MyResource : IDisposable"""
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        """获取资源。C# 等价：构造函数 / 初始化"""
        print(f"  [获取资源] {self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """释放资源（即使异常也会执行）。C# 等价：Dispose()"""
        print(f"  [释放资源] {self.name}")
        return False  # 不吞异常。C# 等价：不返回 true


# with 语句自动调用 __enter__ 和 __exit__
with MyResource("数据库连接") as r:
    print(f"  [使用资源] {r.name} —— 执行业务逻辑")

print(f"  [已退出] 资源已自动释放")

# 嵌套 with
print("\n嵌套 with:")
with MyResource("外层文件") as f1:
    with MyResource("内层文件") as f2:
        print(f"  [使用] {f1.name} + {f2.name}")


# ========== 5. 排序协议 __lt__ ==========
# C# 等价：IComparable<T> 接口
# Python：只需定义 __lt__，sort() 就能使用

print("\n--- 5. 排序协议 __lt__ ---")


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __lt__(self, other):
        """小于比较。C# 等价：int CompareTo(Person other) < 0"""
        return self.age < other.age

    def __repr__(self):
        return f"{self.name}({self.age})"


people = [Person("Bob", 30), Person("Alice", 25), Person("Charlie", 20)]
people.sort()  # 使用 __lt__ 排序
print(f"按年龄排序: {people}")

# 还可以配合 reverse=True
people.sort(reverse=True)
print(f"逆序排序:   {people}")


# ========== 6. Protocol：结构化子类型检查 ==========
# C# 等价：interface + 编译时检查
# Python 3.8+: typing.Protocol + runtime_checkable 可以在运行时做 isinstance 检查

print("\n--- 6. Protocol + runtime_checkable ---")

from typing import Protocol, runtime_checkable


@runtime_checkable  # 允许 isinstance() 检查
class Speakable(Protocol):
    """协议：只要对象有 speak() 方法且返回 str，就是 Speakable"""
    def speak(self) -> str: ...


@runtime_checkable  # 允许 isinstance() 检查
class Drawable(Protocol):
    """协议：只要有 draw() 方法"""
    def draw(self) -> str: ...


class Dog2:
    def speak(self) -> str:
        return "汪汪！"


class NotSpeakable:
    pass


def describe_speaker(animal: Speakable) -> None:
    """C# 等价：void DescribeSpeaker<T>(T animal) where T : ISpeakable"""
    print(f"  {animal.speak()}")


describe_speaker(Dog2())
# describe_speaker(NotSpeakable())  # 类型检查器会警告

# runtime_checkable 让 isinstance 在运行时生效
print(f"  Dog2 是 Drawable? {isinstance(Dog2(), Drawable)}")           # False (没有 draw)
print(f"  Circle 是 Drawable? {isinstance(Circle(), Drawable)}")       # True (有 draw)
print(f"  Circle 是 Speakable? {isinstance(Circle(), Speakable)}")    # False (没有 speak)


# ========== 7. 等价对比总结 ==========
print("\n--- 7. C# vs Python 鸭子类型总结 ---")
print("""
  | 概念              | C#                          | Python                     |
  |-------------------|-----------------------------|----------------------------|
  | 接口约束          | interface ISpeakable        | Protocol (可选，可不写)     |
  | 迭代器            | IEnumerable<T>              | __iter__ + __next__        |
  | 上下文管理        | IDisposable + using         | __enter__ + __exit__       |
  | 排序              | IComparable<T>              | __lt__                     |
  | 运行时类型检查    | is ISpeakable               | isinstance() + Protocol   |
""")
