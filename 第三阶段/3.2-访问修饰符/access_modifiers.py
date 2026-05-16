# ============================================================
# Python 访问修饰符 —— 对比 C# 理解 Python 的访问控制
# 对应文章：3.2 访问修饰符
# ============================================================
# 核心区别：C# 有语法级别的访问控制（public/private/protected/internal），
# Python 没有真正的访问控制，完全靠命名约定。
# ============================================================

# ============================================================
# 1. Python 的"访问修饰符"—— 纯靠约定
# ============================================================
# C# 等价：public / private / protected / internal
# Python 实际只有三个约定：
#   - 无前缀：public（公开）
#   - _ 单下划线：protected（约定私有，外部仍可访问）
#   - __ 双下划线：name mangling（名称改写，非真正私有）

class Person:
    def __init__(self, name, age):
        self.name = name          # public —— 任何地方都能访问
        self._age = age           # _ 前缀 —— 约定为"内部使用"
        self.__secret = "hidden"  # __ 前缀 —— 名称改写（name mangling）

    def greet(self):
        """public 方法 —— C# 等价：public void Greet()"""
        return f"Hello, I'm {self.name}"

    def _internal_helper(self):
        """_ 前缀方法 —— C# 等价：internal / protected"""
        return f"内部调用: age={self._age}"

    def __private_method(self):
        """__ 前缀方法 —— C# 等价：private"""
        return self.__secret


print("=" * 50)
print("1. Python 的访问约定")
print("=" * 50)

p = Person("Alice", 25)

# public —— 完全正常访问
print(f"public:  p.name = {p.name}")

# _ protected —— 能访问，但"约定不该访问"
print(f"_约定:   p._age = {p._age}")

# __ name mangling —— 直接访问会报错
try:
    _ = p.__secret
except AttributeError as e:
    print(f"__:      p.__secret -> {e}")

# 但通过名称改写后的名字仍可访问（Python 不做真正保护）
print(f"改写后:  p._Person__secret = {p._Person__secret}")

# 方法同理
print(f"public:  p.greet() = {p.greet()}")
print(f"_约定:   p._internal_helper() = {p._internal_helper()}")

try:
    _ = p.__private_method()
except AttributeError as e:
    print(f"__方法:  p.__private_method() -> {e}")

print(f"改写后:  p._Person__private_method() = {p._Person__private_method()}")


# ============================================================
# 2. 名称改写（Name Mangling）的目的
# ============================================================
# 名称改写不是为了安全性，而是为了避免子类意外覆盖父类成员
# C# 中用 private 实现相同目的——子类天然看不到父类的 private 成员

class Parent:
    def __init__(self):
        self.__secret = "parent's secret"  # 会变成 _Parent__secret

    def reveal(self):
        print(f"  Parent.reveal() -> {self.__secret}")


class Child(Parent):
    def __init__(self):
        super().__init__()
        self.__secret = "child's secret"   # 会变成 _Child__secret（不同名称！）

    def reveal(self):
        print(f"  Child.reveal()  -> {self.__secret}")


print("\n" + "=" * 50)
print("2. 名称改写的目的 —— 避免子类意外覆盖")
print("=" * 50)

parent = Parent()
child = Child()

print("parent.reveal():")
parent.reveal()
print("child.reveal():")
child.reveal()

# 两者互不干扰——这就是名称改写的价值
print(f"parent._Parent__secret = {parent._Parent__secret}")
print(f"child._Child__secret   = {child._Child__secret}")


# ============================================================
# 3. @property —— Python 实现"受控访问"的核心手段
# ============================================================
# C# 等价：private set + validation in setter
# Python 没有 private set，但 @property 的 setter 可以加验证逻辑

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance  # "私有"余额

    @property
    def balance(self):
        """只读属性 —— C# 等价：public decimal Balance { get; }"""
        return self.__balance

    @balance.setter
    def balance(self, value):
        """带验证的 setter —— C# 等价：private set + 验证逻辑"""
        if value < 0:
            raise ValueError("余额不能为负数")
        self.__balance = value

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("存款金额必须为正")
        self.__balance += amount
        return f"存入 {amount}，余额 {self.__balance}"

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("取款金额必须为正")
        if amount > self.__balance:
            raise ValueError("余额不足")
        self.__balance -= amount
        return f"取出 {amount}，余额 {self.__balance}"


print("\n" + "=" * 50)
print("3. @property —— Python 的'受控访问'")
print("=" * 50)

account = BankAccount("Alice", 1000)
print(f"户主: {account.owner}")
print(f"余额: {account.balance}")
print(account.deposit(500))
print(account.withdraw(200))
print(f"最终余额: {account.balance}")

# 尝试设置非法值
try:
    account.balance = -100
except ValueError as e:
    print(f"非法设置余额: {e}")

# 尝试直接修改"私有"余额——不推荐，但技术上可行
account._BankAccount__balance = 99999
print(f"直接修改后余额: {account.balance}  (不推荐！)")


# ============================================================
# 4. __all__ —— 模块级别的访问控制
# ============================================================
# C# 等价：internal / [InternalsVisibleTo]
# __all__ 控制 from module import * 时导出哪些名称
# 这是 Python 中唯一真正的"模块级"访问控制

# 假设这是一个模块的 __all__ 声明：
_all_example_names = ["PublicClass", "public_function"]
__private_module_var = "这是模块私有变量"

class PublicClass:
    """会被 __all__ 导出"""
    pass

class _PrivateClass:
    """约定私有——__all__ 不会包含它"""
    pass

def public_function():
    """公开函数"""
    return "我是公开函数"

def _private_function():
    """私有函数"""
    return "我是私有函数"


print("\n" + "=" * 50)
print("4. __all__ —— 模块级访问控制")
print("=" * 50)

# 演示 __all__ 的效果
print(f"__all__ 声明导出: {_all_example_names}")
print(f"public_function() = {public_function()}")
print(f"PublicClass = {PublicClass}")
print(f"_PrivateClass = {_PrivateClass}")          # 仍可访问，只是约定不访问
print(f"_private_function() = {_private_function()}")  # 同上

# 实际使用：
# from this_module import *  -> 只会导入 PublicClass 和 public_function
# import this_module         -> 所有名称都可通过 this_module.xxx 访问


# ============================================================
# 5. 名称约定汇总
# ============================================================

print("\n" + "=" * 50)
print("5. C# vs Python 访问控制对比总结")
print("=" * 50)

summary = """
| 概念           | C#           | Python                 |
|----------------|--------------|------------------------|
| 公开           | public       | 无前缀（name）         |
| 私有           | private      | __ 前缀（名称改写）    |
| 受保护         | protected    | _ 前缀（仅约定）       |
| 程序集内部     | internal     | __all__ 控制 * 导入    |
| 只读属性       | { get; }     | @property 只有 getter  |
| 带验证的属性   | private set  | @property + setter     |
| 常量           | const        | 全大写 + _ 分隔        |
| 枚举           | enum         | class + 类变量 或 Enum |
| 接口约束       | interface    | Protocol（typing）     |
"""
print(summary)

print("要点：Python 的访问控制全靠约定（'we are all consenting adults'）")
print("      C# 由编译器强制执行，Python 由程序员自觉遵守")
