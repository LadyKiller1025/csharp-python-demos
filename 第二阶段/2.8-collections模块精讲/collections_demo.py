# Python collections 模块示例
# 对应文章：2.8 collections模块精讲
#
# C# 老兵的 Python 修炼手册：
# collections 是 Python 标准库的"精品集合店"，提供了一堆比内置数据结构更好用的容器。
# 相当于 C# 的 System.Collections.Generic + ConcurrentDictionary 的一些功能，
# 但 Python 的版本更"贴心"，很多常用模式都帮你封装好了。

from collections import Counter, defaultdict, OrderedDict, deque, namedtuple, ChainMap

# ================================================================
#                       1. Counter —— 计数器
# ================================================================

print("=" * 60)
print("               1. Counter —— 计数器中的瑞士军刀")
print("=" * 60)

# 基础用法：词频统计
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
word_count = Counter(words)
print(f"\n--- 基础计数 ---")
print(f"  词频统计: {word_count}")  # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(f"  最常见的2个: {word_count.most_common(2)}")

# 计数器运算（Counter 支持 + - & | 等集合运算，比 C# 的 Dictionary 灵活多了）
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(f"\n--- 计数器运算 ---")
print(f"  相加: {c1 + c2}")  # Counter({'a': 4, 'b': 3})
print(f"  相减: {c1 - c2}")  # Counter({'a': 2})
print(f"  交集: {c1 & c2}")  # Counter({'a': 1, 'b': 1})
print(f"  并集: {c1 | c2}")  # Counter({'a': 3, 'b': 2})

# 实战1：字符频率统计
print(f"\n--- 实战1：字符频率统计 ---")
text = "hello world"
char_count = Counter(text)
print(f"  字符频率: {dict(char_count.most_common())}")
print(f"  最常出现的字符: {char_count.most_common(1)[0]}")
# 找出只出现一次的字符
singles = [char for char, count in char_count.items() if count == 1]
print(f"  只出现一次的字符: {singles}")

# 实战2：从列表创建 Counter 并批量更新
print(f"\n--- 实战2：批量更新 ---")
shopping = Counter()
shopping.update(["apple", "banana", "apple"])
shopping.update(["apple", "cherry", "cherry", "cherry"])
print(f"  购物车: {shopping}")  # Counter({'apple': 3, 'cherry': 3, 'banana': 1})

# 实战3：正负过滤 —— 找出高频词和低频词
print(f"\n--- 实战3：正负过滤 ---")
corpus = Counter({"the": 500, "is": 400, "a": 300, "apple": 5, "banana": 2, "python": 10})
# 正数保留，负数排除
stopwords = Counter({"the": 500, "is": 400, "a": 300})
important = corpus - stopwords  # 去掉常见停用词
print(f"  去掉停用词后: {dict(important)}")

# C# 对应: 没有内置的 Counter，需要自己用 LINQ GroupBy + ToDictionary 实现
#           但 C# 的 LINQ 更通用，Counter 只是计数这一个场景

# ================================================================
#                       2. defaultdict —— 带默认值的字典
# ================================================================

print("\n" + "=" * 60)
print("               2. defaultdict —— 懒人字典")
print("=" * 60)

# 按首字母分组（经典用法）
groups = defaultdict(list)
for name in ["Alice", "Bob", "Anna", "Charlie", "Bob"]:
    groups[name[0]].append(name)
print(f"\n--- 按首字母分组 ---")
print(f"  结果: {dict(groups)}")

# 嵌套字典（多层默认值）
tree = defaultdict(lambda: defaultdict(list))
tree["animal"]["mammal"].append("cat")
tree["animal"]["bird"].append("eagle")
print(f"\n--- 嵌套结构 ---")
print(f"  树形结构: {dict(tree)}")

# C# 对应: Dictionary 不存在 key 时需要手动检查
#           或用 GetOrAdd() 方法（ConcurrentDictionary 也有）
#           但 defaultdict 写起来更简洁

# ================================================================
#                       3. deque —— 双端队列
# ================================================================

print("\n" + "=" * 60)
print("               3. deque —— 双端队列")
print("=" * 60)

dq = deque([1, 2, 3])
dq.appendleft(0)    # 左侧添加
dq.append(4)        # 右侧添加
dq.popleft()         # 左侧弹出
print(f"\n--- 基础操作 ---")
print(f"  deque: {dq}")  # deque([1, 2, 3, 4])

# 固定长度（自动丢弃另一端，非常适合做"最近N条"的场景）
print(f"\n--- 固定长度队列（自动丢弃）---")
recent = deque(maxlen=3)
for i in range(5):
    recent.append(i)
    print(f"  添加 {i}: {list(recent)}")

# 线程安全性说明
print(f"\n--- 线程安全性 ---")
print("  Python 的 deque 是线程安全的！（append/pop 操作是原子的）")
print("  但注意: 复合操作（如先检查再添加）不是原子的")
print("  对比 C#: ConcurrentQueue<T> / ConcurrentStack<T>")
print("  C# 的 LinkedList 不是线程安全的，需要手动加锁")
print("  Python 的 deque 在 C# 中最接近的是 ConcurrentQueue（但 deque 支持双端操作）")

# 实战：用 deque 做滑动窗口
print(f"\n--- 实战：滑动窗口 ---")
data = [10, 20, 30, 40, 50, 60]
window_size = 3
window = deque(maxlen=window_size)
for item in data:
    window.append(item)
    if len(window) == window_size:
        print(f"  窗口 {list(window)}, 平均值: {sum(window)/len(window):.1f}")

# ================================================================
#                       4. OrderedDict —— 有序字典
# ================================================================

print("\n" + "=" * 60)
print("               4. OrderedDict —— 老牌有序字典")
print("=" * 60)

od = OrderedDict()
od["first"] = 1
od["second"] = 2
od["third"] = 3
od.move_to_end("first")  # 移到末尾
print(f"\n--- 基础操作 ---")
print(f"  OrderedDict: {list(od.items())}")

# OrderedDict 的额外优势
print(f"\n--- OrderedDict vs 普通 dict ---")
print("  Python 3.7+ 普通 dict 已经保序，OrderedDict 的额外优势:")
print("  1. move_to_end() —— 可以把元素移到开头或末尾")
print("  2. 相等性比较考虑顺序: {a:1,b:2} != {b:2,a:1}")
print("  3. popitem(last=True/False) —— 可以从两端弹出")
print("  C# 对应: Dictionary<K,V> 默认保序（.NET Core+）")
print("  额外功能用 SortedList/KVP 按键排序")

# ================================================================
#                       5. namedtuple —— 命名元组
# ================================================================

print("\n" + "=" * 60)
print("               5. namedtuple —— 轻量级不可变对象")
print("=" * 60)

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(f"\n--- 基础用法 ---")
print(f"  点: {p.x}, {p.y}, 距离原点: {(p.x**2 + p.y**2)**0.5:.2f}")

# 带默认值
User = namedtuple("User", ["name", "age", "email"], defaults=["unknown", 0, ""])
user = User("Alice")
print(f"  用户: {user}")

# _replace() 方法 —— 创建修改后的新对象（不可变更新）
print(f"\n--- _replace() 不可变更新 ---")
p2 = p._replace(x=10)  # 创建新对象，原对象不变
print(f"  原始点: {p}")
print(f"  替换 x 后: {p2}")
print(f"  原始点不变: {p.x} == 3")  # 原对象没有被修改！
print("  C# 对比: record 类型的 With 表达式类似: p with { X = 10 }")

# _asdict() 转字典
print(f"\n--- _asdict() 转字典 ---")
print(f"  Point 转字典: {p._asdict()}")
print(f"  C# 对比: 类似 record 的 ToDictionary() 或匿名类型转换")

# 实战：函数返回多个值
print(f"\n--- 实战：函数返回多个值 ---")
def get_user_stats(users):
    """返回用户统计数据"""
    Stats = namedtuple("Stats", ["total", "active", "avg_age"])
    total = len(users)
    active = sum(1 for u in users if u.get("active", False))
    avg_age = sum(u.get("age", 0) for u in users) / total if total else 0
    return Stats(total=total, active=active, avg_age=avg_age)

users = [{"name": "Alice", "age": 30, "active": True},
         {"name": "Bob", "age": 25, "active": True},
         {"name": "Charlie", "age": 35, "active": False}]
stats = get_user_stats(users)
print(f"  统计: 总数={stats.total}, 活跃={stats.active}, 平均年龄={stats.avg_age:.1f}")

# ================================================================
#                       6. ChainMap —— 链式映射
# ================================================================

print("\n" + "=" * 60)
print("               6. ChainMap —— 链式映射（配置管理神器）")
print("=" * 60)

defaults = {"color": "red", "user": "guest", "debug": False}
config = {"color": "blue", "debug": True}
override = {"user": "admin"}

config_map = ChainMap(override, config, defaults)
print(f"\n--- 基础用法（配置合并）---")
print(f"  合并配置: {dict(config_map)}")
print(f"  color: {config_map['color']}")  # blue (优先级: override > config > defaults)
print(f"  user: {config_map['user']}")    # admin

# 模拟作用域链（Python 解释器就是这样处理作用域的！）
print(f"\n--- 作用域链模拟 ---")
local_vars = {"x": 10}
global_vars = {"x": 20, "y": 30}
builtin_vars = {"x": 40, "z": 50}
scope = ChainMap(local_vars, global_vars, builtin_vars)
print(f"  作用域查找 x: {scope['x']}")  # 10（局部优先）
print(f"  作用域查找 y: {scope['y']}")  # 30（全局）
print(f"  作用域查找 z: {scope['z']}")  # 50（内置）

# new_child() 方法 —— 创建子映射（在头部插入新层）
print(f"\n--- new_child() 创建子作用域 ---")
child_scope = scope.new_child({"x": 99, "w": 100})
print(f"  子作用域查找 x: {child_scope['x']}")  # 99
print(f"  子作用域查找 w: {child_scope['w']}")  # 100
print(f"  原作用域查找 x: {scope['x']}")         # 10（没被影响）
print(f"  C# 对比: 类似嵌套的 Dictionary 查找，但 ChainMap 不复制数据")
print(f"  ChainMap 只是把多个 dict 串起来，查找时按顺序找第一个匹配的")

# new_child() 的典型用途：临时覆盖配置
print(f"\n--- 实战：临时配置覆盖 ---")
base_config = {"timeout": 30, "retries": 3, "debug": False}
# 临时在测试环境中覆盖一些配置
test_config = ChainMap({"debug": True, "retries": 0}, base_config)
print(f"  基础配置: {base_config}")
print(f"  测试环境: {dict(test_config)}")
print(f"  测试完毕，丢弃 test_config 即可恢复，不会污染 base_config！")

print("\n" + "=" * 60)
print("  总结: collections 模块 = Python 的「精品集合店」")
print("  Counter 让计数变得优雅，deque 让队列操作飞起")
print("  namedtuple 让你不用写 class 就能拥有不可变对象")
print("  ChainMap 让配置管理变得简单又安全")
print("=" * 60)
