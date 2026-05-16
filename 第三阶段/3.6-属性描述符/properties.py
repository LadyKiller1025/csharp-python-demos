# Python 属性与描述符示例
# 对应文章：3.6 属性与描述符
#
# C# 等价：Property (get/set) + C# 8 readonly / C# 9 init-only
# Python 用 @property 装饰器实现，用描述符实现更高级的属性控制

print("=" * 60)
print("3.6 属性与描述符")
print("=" * 60)

# =====================================================================
# 1. @property：Python 的属性访问器
# =====================================================================
# C# 等价：public string Name { get; set; }
# Python 的 @property 让方法调用看起来像属性访问

print("\n--- 1. @property 基本用法 ---")


class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self._email = email  # 下划线前缀表示"受保护"（约定，非强制）

    @property
    def email(self):
        """getter。C# 等价：get => _email;"""
        return self._email

    @email.setter
    def email(self, value):
        """setter 带验证。C# 等价：set { if (...) throw ...; _email = value; }"""
        if not value:
            raise ValueError("邮箱不能为空")
        self._email = value

    @property
    def description(self):
        """只读属性（没有 setter）。C# 等价：public string Description => ...;"""
        return f"{self.name} is {self.age} years old"

    @property
    def is_adult(self):
        """计算属性。C# 等价：public bool IsAdult => Age >= 18;"""
        return self.age >= 18


p = Person("Alice", 25, "alice@example.com")
print(f"name:  {p.name}")          # 访问普通属性
print(f"email: {p.email}")         # 调用 getter
print(f"desc:  {p.description}")   # 只读属性
print(f"adult: {p.is_adult}")      # 计算属性

# 通过 setter 修改
p.email = "new@example.com"
print(f"修改后 email: {p.email}")

# 验证生效
try:
    p.email = ""  # 触发 ValueError
except ValueError as e:
    print(f"验证拦截: {e}")


# =====================================================================
# 2. 温度转换：@property 的计算属性示例
# =====================================================================
# C# 等价：属性的 get/set 可以做计算转换
# Python 用 @property 装饰器实现同样的效果

print("\n--- 2. 温度转换属性 ---")


class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        self._celsius = value

    @property
    def fahrenheit(self):
        """摄氏 -> 华氏。C# 等价：get => _celsius * 9 / 5 + 32;"""
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        """华氏 -> 摄氏。C# 等价：set => _celsius = (value - 32) * 5 / 9;"""
        self._celsius = (value - 32) * 5 / 9

    @property
    def kelvin(self):
        return self._celsius + 273.15

    @kelvin.setter
    def kelvin(self, value):
        self._celsius = value - 273.15


temp = Temperature(100)
print(f"100°C = {temp.fahrenheit}°F = {temp.kelvin}K")

temp.fahrenheit = 32
print(f"32°F  = {temp.celsius}°C = {temp.kelvin}K")

temp.kelvin = 373.15
print(f"373.15K = {temp.celsius}°C = {temp.fahrenheit}°F")


# =====================================================================
# 3. 描述符（Descriptor）：属性控制的底层机制
# =====================================================================
# C# 等价：自定义验证逻辑（DataAnnotations / 自定义 ValidationAttribute）
# Python 的描述符是 @property 的底层机制，可以复用验证逻辑

print("\n--- 3. 描述符（Descriptor）---")


class Validated:
    """验证描述符 —— 自动验证属性值。C# 等价：自定义 ValidationAttribute"""

    def __init__(self, validator):
        self.validator = validator

    def __set_name__(self, owner, name):
        """Python 3.6+ 自动获取属性名。C# 无等价物（C# 通过反射获取）"""
        self.name = name

    def __get__(self, obj, objtype=None):
        """属性访问时调用。C# 等价：get 访问器"""
        if obj is None:
            return self
        return getattr(obj, f'_{self.name}', None)

    def __set__(self, obj, value):
        """属性赋值时调用。C# 等价：set 访问器"""
        if not self.validator(value):
            raise ValueError(f"{self.name} 验证失败: {value!r}")
        setattr(obj, f'_{self.name}', value)


class PersonValidated:
    name = Validated(lambda v: bool(v))   # 非空
    age = Validated(lambda v: isinstance(v, int) and v >= 0)  # 非负整数

    def __init__(self, name, age):
        self.name = name  # 触发 Validated.__set__
        self.age = age

    def __repr__(self):
        return f"PersonValidated(name={self.name!r}, age={self.age})"


person = PersonValidated("Alice", 25)
print(f"创建成功: {person}")
print(f"name = {person.name}")  # 触发 Validated.__get__
print(f"age  = {person.age}")

# 验证失败
try:
    bad = PersonValidated("", 25)  # name 为空字符串
except ValueError as e:
    print(f"name 验证失败: {e}")

try:
    bad = PersonValidated("Bob", -1)  # age 为负数
except ValueError as e:
    print(f"age 验证失败: {e}")


# =====================================================================
# 4. __slots__：限制属性，节省内存
# =====================================================================
# C# 等价：readonly struct / 不可变类型
# Python 对象默认用 __dict__ 存储属性（字典，灵活但占内存）
# __slots__ 强制只允许声明的属性，禁止动态添加

print("\n--- 4. __slots__ ---")


class Point:
    __slots__ = ['x', 'y']  # 只允许 x 和 y 两个属性

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


p = Point(1, 2)
print(f"创建 Point: {p}")
print(f"hasattr(p, '__dict__'): {hasattr(p, '__dict__')}")  # False
print(f"hasattr(p, '__slots__'): {hasattr(p, '__slots__')}")  # True

# 禁止动态添加属性
try:
    p.z = 3  # AttributeError
except AttributeError as e:
    print(f"禁止添加属性: {e}")

# __slots__ 的内存优势
print("（多个 Point 实例共享属性定义，每个实例只存 slot 值，不存 __dict__ 字典）")


# =====================================================================
# 5. __init_subclass__：子类注册机制
# =====================================================================
# C# 等价：C# 8 的 base() 在模式匹配中，或注册表模式
# Python 3.6+：父类可以在子类创建时自动执行代码

print("\n--- 5. __init_subclass__ ---")


class Plugin:
    """插件基类 —— 子类注册时自动加入注册表"""
    _registry = {}  # 类变量，存储所有子类

    def __init_subclass__(cls, plugin_name=None, **kwargs):
        """C# 等价：静态构造函数 + 类型注册"""
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__
        Plugin._registry[name] = cls
        print(f"  [注册插件] {name} -> {cls.__name__}")

    @classmethod
    def get_all_plugins(cls):
        return dict(cls._registry)


# 定义子类时自动触发 __init_subclass__
class JsonPlugin(Plugin, plugin_name="json"):
    def process(self):
        return "处理 JSON"


class XmlPlugin(Plugin, plugin_name="xml"):
    def process(self):
        return "处理 XML"


class CsvPlugin(Plugin):  # 没指定 plugin_name，默认用类名
    def process(self):
        return "处理 CSV"


print(f"\n所有已注册插件: {list(Plugin.get_all_plugins().keys())}")

# 使用注册表
for name, cls in Plugin.get_all_plugins().items():
    instance = cls()
    print(f"  {name}: {instance.process()}")


# =====================================================================
# 6. 等价对比总结
# =====================================================================
print("\n--- 6. C# vs Python 属性对比总结 ---")
print("""
  | 概念              | C#                          | Python                     |
  |-------------------|-----------------------------|----------------------------|
  | 属性              | { get; set; }              | @property                  |
  | 只读属性          | { get; }                    | @property (无 setter)      |
  | 带验证            | set { if(...) throw; }      | @xxx.setter + 验证逻辑     |
  | 计算属性          => expression                   | @property return expr      |
  | init-only (C# 9)  | { get; init; }             | __init__ 中赋值            |
  | required (C# 11)  | required string Name        | __init__ 参数              |
  | 不可变            | readonly struct             | __slots__ + 无 setter      |
  | 描述符            | DataAnnotations             | Descriptor 协议            |
  | 子类注册          | [Attribute] + 反射          | __init_subclass__          |
""")
