using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;

/// <summary>
/// C# JSON 处理完整示例
/// 对应文章：4.4 JSON 处理
///
/// Python 对比：
///   C# JsonSerializer.Serialize/Deserialize  ≈  Python json.dumps/loads
///   C# JsonConverter<T>                      ≈  Python json.JSONEncoder
///   C# System.Text.Json                      ≈  Python orjson (高性能)
///   C# Newtonsoft.Json                       ≈  Python json 模块 (功能丰富)
/// </summary>
class JsonHandling
{
    static void Main()
    {
        // =============================================================
        // 1. JsonSerializer.Serialize — 对象 → JSON 字符串 (序列化)
        // =============================================================
        // Python 对比：
        //   json_str = json.dumps(person)
        //   json_str = json.dumps(person, indent=2, ensure_ascii=False)
        // =============================================================
        Console.WriteLine("============================================================");
        Console.WriteLine("1. JsonSerializer.Serialize — 序列化");
        Console.WriteLine("============================================================");

        var person = new Person { Name = "Alice", Age = 25, IsStudent = false };

        // 基础序列化
        string json1 = JsonSerializer.Serialize(person);
        Console.WriteLine($"基础序列化: {json1}");

        // 格式化输出 (Python: indent=2)
        var optionsPretty = new JsonSerializerOptions
        {
            WriteIndented = true,
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        };
        string prettyJson = JsonSerializer.Serialize(person, optionsPretty);
        Console.WriteLine($"格式化序列化:\n{prettyJson}");

        // 字典序列化
        var data = new Dictionary<string, object>
        {
            ["message"] = "你好世界",
            ["city"] = "北京",
            ["numbers"] = new[] { 1, 2, 3 }
        };
        var optionsNoEscape = new JsonSerializerOptions
        {
            WriteIndented = true,
            Encoder = System.Text.Encodings.Web.JavaScriptEncoder.UnsafeRelaxedJsonEscaping
        };
        string jsonCn = JsonSerializer.Serialize(data, optionsNoEscape);
        Console.WriteLine($"保留中文:\n{jsonCn}");

        // =============================================================
        // 2. JsonSerializer.Deserialize — JSON 字符串 → 对象
        // =============================================================
        // Python 对比：
        //   person = json.loads(json_string)
        //   people = json.loads(json_array)
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("2. JsonSerializer.Deserialize — 反序列化");
        Console.WriteLine("============================================================");

        string jsonString = "{\"Name\":\"Alice\",\"Age\":25}";

        // 反序列化为强类型对象
        var deserialized = JsonSerializer.Deserialize<Person>(jsonString);
        Console.WriteLine($"反序列化为 Person: {deserialized}");

        // 反序列化为字典
        var dict = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(jsonString);
        Console.WriteLine("反序列化为 Dictionary:");
        foreach (var kv in dict)
            Console.WriteLine($"  {kv.Key}: {kv.Value}");

        // 反序列化列表
        string jsonArray = "[{\"Name\":\"Alice\",\"Age\":25},{\"Name\":\"Bob\",\"Age\":30}]";
        var people = JsonSerializer.Deserialize<List<Person>>(jsonArray);
        Console.WriteLine($"反序列化为 List<Person>: 共 {people?.Count} 人");
        foreach (var p in people!)
            Console.WriteLine($"  {p}");

        // =============================================================
        // 3. 文件读写 JSON
        // =============================================================
        // Python 对比：
        //   json.dump(data, f, indent=2)
        //   data = json.load(f)
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("3. 文件读写 JSON");
        Console.WriteLine("============================================================");

        string testDir = "_temp_json_demo_cs";
        Directory.CreateDirectory(testDir);
        string dataFile = Path.Combine(testDir, "data.json");

        // 写入文件 (Python: json.dump(data, f, indent=2))
        var userData = new
        {
            Users = new[]
            {
                new { Name = "Alice", Age = 25, Email = "alice@example.com" },
                new { Name = "Bob", Age = 30, Email = "bob@example.com" },
            },
            Total = 2
        };
        File.WriteAllText(dataFile, JsonSerializer.Serialize(userData, optionsPretty));
        Console.WriteLine($"写入文件: {dataFile}");

        // 读取文件 (Python: data = json.load(f))
        string readBack = File.ReadAllText(dataFile);
        var loaded = JsonSerializer.Deserialize<JsonElement>(readBack);
        Console.WriteLine($"读取文件: 总数={loaded.GetProperty("Total")}");

        // =============================================================
        // 4. JSON 类型对应关系
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("4. JSON 类型对应关系");
        Console.WriteLine("============================================================");
        Console.WriteLine("C# 类型          →  JSON 类型  →  Python 类型");
        Console.WriteLine("string           →  string     →  str");
        Console.WriteLine("int/long         →  number     →  int");
        Console.WriteLine("double/decimal   →  number     →  float");
        Console.WriteLine("bool             →  true/false →  True/False");
        Console.WriteLine("null             →  null       →  None");
        Console.WriteLine("List<T>/Array    →  array      →  list");
        Console.WriteLine("Dictionary       →  object     →  dict");

        // =============================================================
        // 5. 自定义 JsonConverter — 处理特殊类型
        // =============================================================
        // Python 对比：
        //   class PersonEncoder(json.JSONEncoder):
        //       def default(self, obj): ...
        //   json.dumps(person, cls=PersonEncoder)
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("5. 自定义 JsonConverter — 处理 DateTime");
        Console.WriteLine("============================================================");

        var event_ = new CalendarEvent
        {
            Title = "Python 学习",
            Date = new DateTime(2024, 6, 15, 10, 0, 0),
            Attendees = new List<string> { "Alice", "Bob" }
        };

        var optionsWithConverter = new JsonSerializerOptions
        {
            WriteIndented = true,
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
            Converters = { new DateTimeConverter() }
        };

        string eventJson = JsonSerializer.Serialize(event_, optionsWithConverter);
        Console.WriteLine($"自定义 DateTime 转换器:\n{eventJson}");

        // 反序列化
        var loadedEvent = JsonSerializer.Deserialize<CalendarEvent>(eventJson, optionsWithConverter);
        Console.WriteLine($"反序列化: {loadedEvent?.Title}, 日期={loadedEvent?.Date}");

        // =============================================================
        // 6. 命名策略 — camelCase / snake_case
        // =============================================================
        // Python 中字典 key 通常就是 snake_case
        // C# 默认使用 PascalCase，JSON 中通常用 camelCase
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("6. 命名策略 — camelCase / snake_case");
        Console.WriteLine("============================================================");

        var optionsCamel = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        };

        var optionsSnake = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower
        };

        var optionsOriginal = new JsonSerializerOptions
        {
            // PropertyNamingPolicy = null 保留原始命名
        };

        Console.WriteLine($"PascalCase: {JsonSerializer.Serialize(new Person { Name = "Alice", Age = 25 })}");
        Console.WriteLine($"camelCase:  {JsonSerializer.Serialize(new Person { Name = "Alice", Age = 25 }, optionsCamel)}");
        Console.WriteLine($"snake_case: {JsonSerializer.Serialize(new Person { Name = "Alice", Age = 25 }, optionsSnake)}");

        // =============================================================
        // 7. JsonElement — 动态 JSON 访问
        // =============================================================
        // Python 对比：
        //   data = json.loads(json_str)
        //   data["name"]  # 动态访问
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("7. JsonElement — 动态 JSON 访问");
        Console.WriteLine("============================================================");

        string complexJson = """
        {
            "company": "TechCorp",
            "departments": [
                {
                    "name": "Engineering",
                    "employees": [
                        {"name": "Alice", "skills": ["Python", "C#"], "level": "senior"},
                        {"name": "Bob", "skills": ["Java"], "level": "junior"}
                    ]
                }
            ]
        }
        """;

        using var doc = JsonDocument.Parse(complexJson);
        var root = doc.RootElement;

        Console.WriteLine($"公司: {root.GetProperty("company").GetString()}");
        Console.WriteLine($"部门: {root.GetProperty("departments")[0].GetProperty("name").GetString()}");

        // 遍历嵌套结构
        Console.WriteLine("所有员工:");
        foreach (var dept in root.GetProperty("departments").EnumerateArray())
        {
            string deptName = dept.GetProperty("name").GetString()!;
            foreach (var emp in dept.GetProperty("employees").EnumerateArray())
            {
                string empName = emp.GetProperty("name").GetString()!;
                string level = emp.GetProperty("level").GetString()!;
                Console.WriteLine($"  [{deptName}] {empName} - 级别: {level}");
            }
        }

        // =============================================================
        // 8. 错误处理
        // =============================================================
        // Python 对比：
        //   except json.JSONDecodeError as e:
        //       print(f"解析错误: {e.msg}")
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("8. 错误处理");
        Console.WriteLine("============================================================");

        string[] invalidJsons = {
            "not json",
            "{\"name\": }",
            "{\"trailing\": \"comma\",}"
        };

        foreach (var invalid in invalidJsons)
        {
            try
            {
                JsonSerializer.Deserialize<JsonElement>(invalid);
                Console.WriteLine($"  解析成功: {invalid}");
            }
            catch (JsonException ex)
            {
                // Python 等价：except json.JSONDecodeError as e
                Console.WriteLine($"  JsonException: {invalid} → {ex.Message}");
            }
        }

        // =============================================================
        // 9. System.Text.Json vs Newtonsoft.Json
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("9. System.Text.Json vs Newtonsoft.Json");
        Console.WriteLine("============================================================");
        Console.WriteLine();
        Console.WriteLine("System.Text.Json (内置):");
        Console.WriteLine("  + 内置，无需额外安装");
        Console.WriteLine("  + 性能优秀 (类似 Python orjson)");
        Console.WriteLine("  + AOT 友好");
        Console.WriteLine("  - 功能相对较少");
        Console.WriteLine("  - 需要 C# 类型映射");
        Console.WriteLine();
        Console.WriteLine("Newtonsoft.Json (第三方):");
        Console.WriteLine("  + 功能丰富 (类似 Python json 模块)");
        Console.WriteLine("  + 灵活的动态类型支持");
        Console.WriteLine("  + 更好的向后兼容");
        Console.WriteLine("  - 需要 NuGet 安装");
        Console.WriteLine("  - 性能略低");
        Console.WriteLine();
        Console.WriteLine("Python 对比:");
        Console.WriteLine("  System.Text.Json  ≈  orjson (高性能，内置)");
        Console.WriteLine("  Newtonsoft.Json   ≈  json 模块 (功能丰富，标准库)");

        // =============================================================
        // 10. JSON 处理最佳实践总结
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("10. JSON 处理最佳实践总结");
        Console.WriteLine("============================================================");
        Console.WriteLine();
        Console.WriteLine("C# vs Python JSON 处理对比:");
        Console.WriteLine("  C# JsonSerializer.Serialize      ≈  Python json.dumps");
        Console.WriteLine("  C# JsonSerializer.Deserialize    ≈  Python json.loads");
        Console.WriteLine("  C# File.WriteAllText + Serialize  ≈  Python json.dump");
        Console.WriteLine("  C# File.ReadAllText + Deserialize ≈  Python json.load");
        Console.WriteLine("  C# JsonConverter<T>               ≈  Python json.JSONEncoder");
        Console.WriteLine("  C# JsonNamingPolicy.CamelCase     ≈  (Python 默认 snake_case)");
        Console.WriteLine();
        Console.WriteLine("最佳实践:");
        Console.WriteLine("  1. 默认用 System.Text.Json (C#) / orjson (Python)");
        Console.WriteLine("  2. 复杂场景用 Newtonsoft.Json (C#) / 自定义 default (Python)");
        Console.WriteLine("  3. 使用强类型反序列化，避免手动解析");
        Console.WriteLine("  4. 始终处理 JsonException / JSONDecodeError");
        Console.WriteLine("  5. 大文件用流式处理 (Utf8JsonReader)");

        // 清理
        Directory.Delete(testDir, true);

        Console.WriteLine();
        Console.WriteLine("所有 JSON 处理示例运行完毕！");
    }
}

// =============================================================
// 辅助类定义
// =============================================================

/// <summary>
/// Person 类
/// Python 等价：
///   class Person:
///       def __init__(self, name, age): ...
/// </summary>
public class Person
{
    public string Name { get; set; } = "";
    public int Age { get; set; }
    public bool IsStudent { get; set; }

    public override string ToString() => $"Person(Name={Name}, Age={Age})";
}

/// <summary>
/// 日历事件类 — 包含 DateTime 类型
/// </summary>
public class CalendarEvent
{
    public string Title { get; set; } = "";
    public DateTime Date { get; set; }
    public List<string> Attendees { get; set; } = new();
}

/// <summary>
/// 自定义 DateTime 转换器
/// Python 等价：
///   class EventEncoder(json.JSONEncoder):
///       def default(self, obj):
///           if isinstance(obj, datetime):
///               return obj.isoformat()
///           return super().default(obj)
/// </summary>
public class DateTimeConverter : JsonConverter<DateTime>
{
    private const string Format = "yyyy-MM-dd HH:mm:ss";

    public override DateTime Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
    {
        string? dateString = reader.GetString();
        if (DateTime.TryParse(dateString, out DateTime result))
            return result;
        throw new JsonException($"无法解析日期: {dateString}");
    }

    public override void Write(Utf8JsonWriter writer, DateTime value, JsonSerializerOptions options)
    {
        writer.WriteStringValue(value.ToString(Format));
    }
}
