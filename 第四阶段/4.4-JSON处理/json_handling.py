"""
Python JSON 处理完整示例
对应文章：4.4 JSON 处理

C# 对比：
  Python json.dumps/loads      ≈  C# JsonSerializer.Serialize/Deserialize
  Python json.dump/load        ≈  C# JsonSerializer + FileStream
  Python json.JSONEncoder      ≈  C# 自定义 JsonConverter
  Python 或json(orjson)        ≈  C# Newtonsoft.Json (性能优先场景)
"""
import json
import os
from datetime import datetime, date

# =============================================================
# 1. json.dumps() — 对象 → JSON 字符串 (序列化)
# =============================================================
# C# 对比：
#   string json = JsonSerializer.Serialize(person);
#   string json = JsonConvert.SerializeObject(person);  // Newtonsoft
# =============================================================
print("=" * 60)
print("1. json.dumps() — 对象 → JSON 字符串")
print("=" * 60)

# 基础序列化
person = {"name": "Alice", "age": 25, "is_student": False, "courses": ["Python", "C#"]}
json_str = json.dumps(person)
print(f"基础序列化: {json_str}")

# 带格式化的序列化 (Python: indent=2)
# C# 等价：JsonSerializer.Serialize(obj, new JsonSerializerOptions { WriteIndented = true })
pretty_json = json.dumps(person, indent=2, ensure_ascii=False)
print(f"格式化序列化:\n{pretty_json}")

# sort_keys 排序
json_sorted = json.dumps(person, indent=2, sort_keys=True, ensure_ascii=False)
print(f"按键排序:\n{json_sorted}")

# ensure_ascii=False 保留中文 (C# 默认就保留 Unicode)
data_chinese = {"message": "你好世界", "city": "北京"}
json_cn = json.dumps(data_chinese, ensure_ascii=False, indent=2)
print(f"保留中文:\n{json_cn}")

print()
print("=" * 60)
print("2. json.loads() — JSON 字符串 → 对象 (反序列化)")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   var person = JsonSerializer.Deserialize<Person>(jsonString);
#   var dict = JsonSerializer.Deserialize<Dictionary<string, object>>(jsonString);
# -------------------------------------------------------
json_string = '{"name": "Alice", "age": 25, "scores": [90, 85, 92]}'

# 反序列化为字典
person = json.loads(json_string)
print(f"反序列化为 dict: {person}")
print(f"  类型: {type(person)}")
print(f"  name: {person['name']}")

# 反序列化为列表
json_array = '[{"name": "Alice"}, {"name": "Bob"}]'
people = json.loads(json_array)
print(f"反序列化为 list: {people}")
print(f"  类型: {type(people)}, 第一个元素类型: {type(people[0])}")

# 嵌套结构
nested_json = '''
{
    "company": "TechCorp",
    "employees": [
        {"name": "Alice", "skills": ["Python", "C#"]},
        {"name": "Bob", "skills": ["Java", "Go"]}
    ]
}
'''
data = json.loads(nested_json)
print(f"嵌套结构: company={data['company']}, 员工数={len(data['employees'])}")

print()
print("=" * 60)
print("3. json.dump/load — 直接读写文件")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   File.WriteAllText(path, JsonSerializer.Serialize(data, options));
#   var data = JsonSerializer.Deserialize<T>(File.ReadAllText(path));
#   // 或使用 FileStream
#   using var fs = File.OpenWrite(path);
#   JsonSerializer.Serialize(fs, data);
# -------------------------------------------------------
test_dir = "_temp_json_demo"
os.makedirs(test_dir, exist_ok=True)
data_file = os.path.join(test_dir, "data.json")
pretty_file = os.path.join(test_dir, "pretty.json")

# json.dump — 写入文件
data = {
    "users": [
        {"name": "Alice", "age": 25, "email": "alice@example.com"},
        {"name": "Bob", "age": 30, "email": "bob@example.com"},
    ],
    "total": 2
}

with open(data_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"json.dump() 写入: {data_file}")

# json.load — 从文件读取
with open(data_file, "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
print(f"json.load() 读取: 用户数={loaded_data['total']}")

# 排序写入
with open(pretty_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)
print(f"json.dump(sort_keys=True) 写入: {pretty_file}")

print()
print("=" * 60)
print("4. JSON 类型对应关系")
print("=" * 60)

# -------------------------------------------------------
# Python 类型  →  JSON 类型   →  C# 类型
# dict        →  object      →  Dictionary / 自定义类
# list        →  array       →  List<T> / Array
# str         →  string      →  string
# int         →  number      →  int / long
# float       →  number      →  double / decimal
# True        →  true        →  true
# False       →  false       →  false
# None        →  null        →  null
# -------------------------------------------------------
type_demo = {
    "string": "hello",
    "integer": 42,
    "float": 3.14,
    "boolean_true": True,
    "boolean_false": False,
    "null_value": None,
    "list": [1, 2, 3],
    "nested": {"key": "value"}
}
json_str = json.dumps(type_demo, indent=2)
print(f"类型映射:\n{json_str}")

# 注意：datetime 不是 JSON 标准类型，需要自定义处理
print(f"\n注意: datetime 不是 JSON 标准类型")
print(f"  datetime → json.dumps 会报错: TypeError")
print(f"  C# 同理: DateTime 需要 JsonSerializerOptions 配置")

print()
print("=" * 60)
print("5. default 参数 — 处理不可序列化的类型")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   options.Converters.Add(new DateTimeConverter());
#   JsonSerializer.Serialize(obj, options);
# -------------------------------------------------------
def json_serial(obj):
    """自定义序列化函数，处理默认不支持的类型"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, set):
        return list(obj)
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors="replace")
    raise TypeError(f"类型 {type(obj)} 不支持 JSON 序列化")


# 使用 default 参数
data_with_date = {
    "name": "Alice",
    "created_at": datetime(2024, 1, 15, 10, 30, 0),
    "tags": {"python", "csharp"},  # set 不是 JSON 标准类型
}

json_str = json.dumps(data_with_date, default=json_serial, indent=2, ensure_ascii=False)
print(f"自定义 default 序列化:\n{json_str}")

# 反序列化后类型会变化
print(f"\n注意反序列化后:")
loaded = json.loads(json_str)
print(f"  created_at 类型: {type(loaded['created_at'])} (从 datetime 变成 str)")
print(f"  tags 类型: {type(loaded['tags'])} (从 set 变成 list)")

print()
print("=" * 60)
print("6. 自定义 JSONEncoder — 面向对象的序列化方式")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   public class PersonConverter : JsonConverter<Person>
#   {
#       public override Person Read(ref Utf8JsonReader reader, ...)
#       public override void Write(Utf8JsonWriter writer, Person value, ...)
#   }
# -------------------------------------------------------

class Person:
    def __init__(self, name: str, age: int, email: str = ""):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age})"


class PersonEncoder(json.JSONEncoder):
    """自定义编码器 — 继承 json.JSONEncoder"""
    def default(self, obj):
        if isinstance(obj, Person):
            return {
                "__type__": "Person",
                "name": obj.name,
                "age": obj.age,
                "email": obj.email,
            }
        # 对于不支持的类型，调用父类的 default 方法
        return super().default(obj)


person = Person("Alice", 25, "alice@example.com")
# 使用 cls 参数指定自定义编码器
# C# 等价：JsonSerializer.Serialize(person, options) 其中 options 包含 Converter
json_str = json.dumps(person, cls=PersonEncoder, indent=2, ensure_ascii=False)
print(f"自定义编码器序列化:\n{json_str}")

# 自定义解码（手动处理 __type__ 标记）
def decode_person(dct):
    """自定义解码函数，配合 object_hook 参数使用"""
    if "__type__" in dct and dct["__type__"] == "Person":
        return Person(dct["name"], dct["age"], dct.get("email", ""))
    return dct

# object_hook: 每个 JSON 对象解析完毕后调用
# C# 等价：JsonConverter<T>.Read() 方法
loaded = json.loads(json_str, object_hook=decode_person)
print(f"\n自定义解码: {loaded}")
print(f"  类型: {type(loaded)}")
print(f"  name: {loaded.name}")

print()
print("=" * 60)
print("7. JSONPath / 嵌套数据访问")
print("=" * 60)

complex_data = {
    "company": "TechCorp",
    "departments": [
        {
            "name": "Engineering",
            "employees": [
                {"name": "Alice", "skills": ["Python", "C#"], "level": "senior"},
                {"name": "Bob", "skills": ["Java"], "level": "junior"},
            ]
        },
        {
            "name": "Marketing",
            "employees": [
                {"name": "Charlie", "skills": ["SEO"], "level": "mid"},
            ]
        }
    ]
}

# 嵌套访问
print(f"公司: {complex_data['company']}")
print(f"部门 1: {complex_data['departments'][0]['name']}")
print(f"员工 1 技能: {complex_data['departments'][0]['employees'][0]['skills']}")

# 遍历嵌套结构
print("\n所有员工:")
for dept in complex_data["departments"]:
    for emp in dept["employees"]:
        print(f"  [{dept['name']}] {emp['name']} - 级别: {emp['level']}, 技能: {emp['skills']}")

# 列表推导式提取（C# LINQ 的等价物）
senior_employees = [
    emp["name"]
    for dept in complex_data["departments"]
    for emp in dept["employees"]
    if emp["level"] == "senior"
]
print(f"\n高级员工: {senior_employees}")

# C# 等价：
# var seniorEmployees = data.departments
#     .SelectMany(d => d.employees)
#     .Where(e => e.level == "senior")
#     .Select(e => e.name)
#     .ToList();

print()
print("=" * 60)
print("8. JSON 验证与错误处理")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   try { JsonSerializer.Deserialize<T>(json); }
#   catch (JsonException ex) { ... }
# -------------------------------------------------------

# 无效 JSON
invalid_json_strings = [
    ("非 JSON 字符串", "hello world"),
    ("尾随逗号", '{"name": "Alice",}'),
    ("缺少引号", "{name: Alice}"),
    ("不完整 JSON", '{"name": "Alice"'),
]

for desc, invalid_json in invalid_json_strings:
    try:
        json.loads(invalid_json)
        print(f"  [{desc}] 解析成功")
    except json.JSONDecodeError as e:
        # C# 等价：catch (JsonException ex)
        print(f"  [{desc}] JSONDecodeError: {e.msg}")

print()
print("=" * 60)
print("9. JSON 工具函数")
print("=" * 60)

# 格式化 JSON 字符串
compact_json = '{"name":"Alice","age":25,"scores":[90,85,92]}'
formatted = json.dumps(json.loads(compact_json), indent=2, ensure_ascii=False)
print(f"紧凑 → 格式化:\n{formatted}")

# JSON 比较
json_a = json.dumps({"b": 2, "a": 1}, sort_keys=True)
json_b = json.dumps({"a": 1, "b": 2}, sort_keys=True)
print(f"\nJSON 比较 (排序后): {json_a == json_b}")

# 安全解析 (类似 JavaScript 的 JSON.parse，失败返回默认值)
def safe_json_loads(json_str, default=None):
    """安全解析 JSON，失败返回默认值"""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default

result = safe_json_loads("invalid", default={})
print(f"安全解析: {result}")

result2 = safe_json_loads('{"ok": true}', default={})
print(f"安全解析: {result2}")

print()
print("=" * 60)
print("10. json.tool — 命令行工具")
print("=" * 60)
print("""
Python 内置 json.tool 模块，可在命令行使用:

  echo '{{"name": "Alice"}}' | python -m json.tool
  python -m json.tool input.json > output.json    # 格式化文件
  python -m json.tool input.json --compact         # 紧凑输出
  python -m json.tool --sort-keys input.json       # 键排序

C# 没有内置命令行 JSON 工具，但有很多第三方选择:
  - jq (跨平台)
  - dotnet 工具: dotnet tool install -g dotnet-script
  - Visual Studio / VS Code 内置 JSON 格式化
""")

print("=" * 60)
print("11. orjson — 高性能 JSON 库 (推荐)")
print("=" * 60)
print("""
orjson 是 Python 中最快的 JSON 库:
  pip install orjson

import orjson

# 序列化 (比 json.dumps 快 10 倍)
data = {"name": "Alice", "age": 25}
json_bytes = orjson.dumps(data)       # 返回 bytes
json_str = orjson.dumps(data).decode()  # 返回 str

# 反序列化
obj = orjson.loads(json_bytes)

# 自动支持 datetime, set, bytes, numpy 等类型
# 无需自定义 encoder

C# 对比:
  C# System.Text.Json 性能已经很好（类似 orjson 的定位）
  Newtonsoft.Json 更灵活但稍慢（类似 Python json 模块）
  没有一个明显「最快」的选择，两者都足够好
""")

# 清理
import shutil
shutil.rmtree(test_dir)

print("=" * 60)
print("12. JSON 处理最佳实践总结")
print("=" * 60)
print("""
Python vs C# JSON 处理对比:
  Python json.dumps            ≈  C# JsonSerializer.Serialize
  Python json.loads            ≈  C# JsonSerializer.Deserialize
  Python json.dump             ≈  C# JsonSerializer.Serialize + FileStream
  Python json.load             ≈  C# FileStream + JsonSerializer.Deserialize
  Python json.JSONEncoder      ≈  C# JsonConverter<T>
  Python default=func          ≈  C# options.Converters.Add(converter)
  Python orjson                ≈  C# System.Text.Json (高性能)
  Python json 模块             ≈  C# Newtonsoft.Json (功能丰富)

最佳实践:
  1. 确保 ensure_ascii=False 处理中文
  2. 生产环境使用 orjson (Python) 或 System.Text.Json (C#)
  3. 复杂类型用自定义 Encoder/Converter
  4. 始终处理 JSONDecodeError / JsonException
  5. 大文件用流式处理，避免一次性加载到内存
""")

print("所有 JSON 处理示例运行完毕！")
