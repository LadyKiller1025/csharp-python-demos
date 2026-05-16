using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Runtime.Serialization;

/// <summary>
/// C# 自定义异常完整示例
/// 对应文章：4.2 自定义异常
///
/// Python 对比：
///   C# 继承 Exception + [Serializable]  ≈  Python 继承 Exception
///   C# 构造函数 (msg, innerEx)          ≈  Python __init__(msg, cause)
///   C# throw new X("msg", innerEx)      ≈  Python raise X("msg") from original
/// </summary>
class CustomExceptions
{
    static void Main()
    {
        // =============================================================
        // 1. 基础自定义异常
        // =============================================================
        // Python 对比：
        //   class BusinessException(Exception):
        //       def __init__(self, message, error_code):
        //           super().__init__(message)
        //           self.error_code = error_code
        // =============================================================
        Console.WriteLine("============================================================");
        Console.WriteLine("1. 基础自定义异常");
        Console.WriteLine("============================================================");

        try
        {
            throw new BusinessException("用户不存在", 404);
        }
        catch (BusinessException ex)
        {
            Console.WriteLine($"捕获业务异常: {ex}");
            Console.WriteLine($"  错误码: {ex.ErrorCode}");
            Console.WriteLine($"  消息: {ex.Message}");
        }

        // =============================================================
        // 2. 异常继承 — 带上下文信息的构造函数
        // =============================================================
        // Python 对比：
        //   class DatabaseError(Exception):
        //       def __init__(self, message, connection_string="", query=""):
        //           super().__init__(message)
        //           self.connection_string = connection_string
        //           self.query = query
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("2. 异常继承 — 带上下文信息的构造函数");
        Console.WriteLine("============================================================");

        try
        {
            throw new DatabaseException(
                "查询超时",
                "server=localhost;db=mydb",
                "SELECT * FROM users"
            );
        }
        catch (DatabaseException ex)
        {
            Console.WriteLine($"数据库异常: {ex}");
        }

        // =============================================================
        // 3. Inner Exception — 异常链
        // =============================================================
        // Python 对比：
        //   raise BusinessException("处理失败") from original_exception
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("3. Inner Exception — 异常链");
        Console.WriteLine("============================================================");

        try
        {
            try
            {
                int.Parse("not_a_number");
            }
            catch (FormatException original)
            {
                // 将原始异常作为 innerException 传递
                // 等同 Python 的: raise BusinessException("处理失败") from original
                throw new BusinessException("参数验证失败", 400, original);
            }
        }
        catch (BusinessException ex)
        {
            Console.WriteLine($"业务异常: {ex.Message}");
            Console.WriteLine($"错误码: {ex.ErrorCode}");
            Console.WriteLine($"原始异常 (InnerException): {ex.InnerException?.Message}");
        }

        // =============================================================
        // 4. [Serializable] — 跨 AppDomain 传输
        // =============================================================
        // Python 对比：
        //   Python 异常天然可 pickle（序列化），无需额外标记
        //   C# 在跨 AppDomain / 远程调用时需要 [Serializable]
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("4. [Serializable] — 跨 AppDomain 传输");
        Console.WriteLine("============================================================");
        Console.WriteLine("C# 传统上需要 [Serializable] 特性标记自定义异常");
        Console.WriteLine("用于跨 AppDomain 边界传输异常（如 .NET Remoting）");
        Console.WriteLine(".NET Core / .NET 5+ 中已不再强制要求");
        Console.WriteLine("但实现 ISerializable 仍是最佳实践");
        Console.WriteLine();
        Console.WriteLine("Python 等价：");
        Console.WriteLine("  Python 异常天然支持 pickle 序列化");
        Console.WriteLine("  无需额外标记，可直接跨进程传输");

        // =============================================================
        // 5. 异常层次结构 — 分层捕获
        // =============================================================
        // Python 对比：
        //   class AppError(Exception): pass
        //   class DatabaseError(AppError): pass
        //   class ConnectionError(DatabaseError): pass
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("5. 异常层次结构 — 分层捕获");
        Console.WriteLine("============================================================");

        // 最具体的异常优先捕获
        Exception[] errorsToTest = new Exception[]
        {
            new AppException("通用应用错误"),
            new DatabaseException2("数据库错误"),
            new ConnectionException2("连接失败"),
            new QueryException2("查询语法错误"),
        };

        foreach (var err in errorsToTest)
        {
            try
            {
                throw err;
            }
            catch (ConnectionException2 e)
            {
                Console.WriteLine($"  [连接层] {e.GetType().Name}: {e.Message}");
            }
            catch (QueryException2 e)
            {
                Console.WriteLine($"  [查询层] {e.GetType().Name}: {e.Message}");
            }
            catch (DatabaseException2 e)
            {
                Console.WriteLine($"  [数据库层] {e.GetType().Name}: {e.Message}");
            }
            catch (AppException e)
            {
                Console.WriteLine($"  [应用层] {e.GetType().Name}: {e.Message}");
            }
        }

        // =============================================================
        // 6. 验证异常 — 带详细错误信息
        // =============================================================
        // Python 对比：
        //   class ValidationException(Exception):
        //       def __init__(self, errors: dict):
        //           super().__init__("验证失败")
        //           self.errors = errors
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("6. 验证异常 — 带详细错误信息");
        Console.WriteLine("============================================================");

        var validationErrors = new Dictionary<string, string>
        {
            ["name"] = "名字不能为空",
            ["age"] = "年龄必须大于0",
            ["email"] = "邮箱格式不正确"
        };

        try
        {
            throw new ValidationException(validationErrors);
        }
        catch (ValidationException ex)
        {
            Console.WriteLine($"验证异常: {ex.Message}");
            Console.WriteLine("错误详情:");
            foreach (var kv in ex.Errors)
            {
                Console.WriteLine($"  {kv.Key}: {kv.Value}");
            }
        }

        // =============================================================
        // 7. API 异常 — 结构化错误信息
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("7. API 异常 — 结构化错误信息");
        Console.WriteLine("============================================================");

        try
        {
            throw new ApiException(
                statusCode: 422,
                errorCode: "VALIDATION_ERROR",
                message: "请求参数无效",
                details: new Dictionary<string, object>
                {
                    ["field"] = "email",
                    ["reason"] = "格式不正确"
                }
            );
        }
        catch (ApiException ex)
        {
            Console.WriteLine($"API 异常: {ex.Message}");
            Console.WriteLine($"结构化信息: {ex.ToJson()}");
        }

        // =============================================================
        // 8. throw 重新抛出 — 保留堆栈
        // =============================================================
        // Python 对比：
        //   except ConnectionError:
        //       print("日志: 捕获到连接错误")
        //       raise  # 重新抛出，完全保留原始异常
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("8. throw 重新抛出 — 保留堆栈");
        Console.WriteLine("============================================================");

        try
        {
            try
            {
                HandleDatabaseOperation();
            }
            catch (ConnectionException2)
            {
                Console.WriteLine("  日志: 捕获到连接错误，重新抛出...");
                throw;  // 重新抛出，完全保留原始异常和堆栈（等同 Python 的 raise）
            }
        }
        catch (ConnectionException2 e)
        {
            Console.WriteLine($"  上层捕获: {e.Message}");
        }

        // =============================================================
        // 9. 自定义异常最佳实践总结
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("9. 自定义异常最佳实践总结");
        Console.WriteLine("============================================================");
        Console.WriteLine();
        Console.WriteLine("C# 自定义异常最佳实践:");
        Console.WriteLine("  1. 继承 Exception 类");
        Console.WriteLine("  2. 提供多个构造函数: (message), (message, inner), (serialization)");
        Console.WriteLine("  3. 添加 [Serializable] (传统要求，现代可选)");
        Console.WriteLine("  4. 实现 ISerializable 接口 (可选)");
        Console.WriteLine("  5. 使用 throw new X(\"msg\", innerEx) 保留异常链");
        Console.WriteLine();
        Console.WriteLine("Python 对比:");
        Console.WriteLine("  1. 继承 Exception (不是 BaseException)");
        Console.WriteLine("  2. 在 __init__ 中接收并存储上下文");
        Console.WriteLine("  3. 提供有意义的 __str__ 方法");
        Console.WriteLine("  4. 使用 raise...from 保留异常链");
        Console.WriteLine("  5. 无需额外标记，天然支持序列化");

        Console.WriteLine();
        Console.WriteLine("所有自定义异常示例运行完毕！");
    }
}

// =============================================================
// 自定义异常类定义
// =============================================================

/// <summary>
/// 业务异常基类 — 带错误码
/// Python 等价：
///   class BusinessException(Exception):
///       def __init__(self, message, error_code):
///           super().__init__(message)
///           self.error_code = error_code
/// </summary>
[Serializable]
public class BusinessException : Exception
{
    public int ErrorCode { get; }

    public BusinessException(string message, int errorCode)
        : base(message)
    {
        ErrorCode = errorCode;
    }

    public BusinessException(string message, int errorCode, Exception innerException)
        : base(message, innerException)
    {
        ErrorCode = errorCode;
    }

    // 序列化构造函数（.NET Framework 传统要求）
    protected BusinessException(SerializationInfo info, StreamingContext context)
        : base(info, context)
    {
        ErrorCode = info.GetInt32(nameof(ErrorCode));
    }

    public override string ToString()
    {
        return $"[{ErrorCode}] {Message}";
    }
}

/// <summary>
/// 数据库异常 — 带连接信息和查询上下文
/// Python 等价：
///   class DatabaseError(Exception):
///       def __init__(self, message, connection_string="", query=""):
///           ...
/// </summary>
[Serializable]
public class DatabaseException : Exception
{
    public string ConnectionString { get; }
    public string Query { get; }

    public DatabaseException(string message, string connectionString = "", string query = "")
        : base(message)
    {
        ConnectionString = connectionString;
        Query = query;
    }

    public override string ToString()
    {
        var base_msg = base.ToString();
        var details = new List<string>();
        if (!string.IsNullOrEmpty(ConnectionString)) details.Add($"连接: {ConnectionString}");
        if (!string.IsNullOrEmpty(Query)) details.Add($"查询: {Query}");
        return details.Count > 0
            ? $"{base_msg} ({string.Join(", ", details)})"
            : base_msg;
    }
}

// =============================================================
// 异常层次结构
// =============================================================

/// <summary>
/// 应用错误基类 — 所有业务异常的根
/// Python 等价：class AppError(Exception): pass
/// </summary>
[Serializable]
public class AppException : Exception
{
    public AppException(string message) : base(message) { }
    public AppException(string message, Exception inner) : base(message, inner) { }
}

/// <summary>
/// 数据库错误
/// Python 等价：class DatabaseError(AppError): pass
/// </summary>
[Serializable]
public class DatabaseException2 : AppException
{
    public DatabaseException2(string message) : base(message) { }
    public DatabaseException2(string message, Exception inner) : base(message, inner) { }
}

/// <summary>
/// 连接错误
/// Python 等价：class ConnectionError(DatabaseError): pass
/// </summary>
[Serializable]
public class ConnectionException2 : DatabaseException2
{
    public ConnectionException2(string message) : base(message) { }
    public ConnectionException2(string message, Exception inner) : base(message, inner) { }
}

/// <summary>
/// 查询错误
/// Python 等价：class QueryError(DatabaseError): pass
/// </summary>
[Serializable]
public class QueryException2 : DatabaseException2
{
    public QueryException2(string message) : base(message) { }
    public QueryException2(string message, Exception inner) : base(message, inner) { }
}

/// <summary>
/// 验证异常 — 携带多个字段的验证错误
/// Python 等价：
///   class ValidationException(Exception):
///       def __init__(self, errors: dict):
///           super().__init__("验证失败")
///           self.errors = errors
/// </summary>
public class ValidationException : Exception
{
    public Dictionary<string, string> Errors { get; }

    public ValidationException(Dictionary<string, string> errors)
        : base($"验证失败: {string.Join("; ", errors.Select(kv => $"{kv.Key}={kv.Value}"))}")
    {
        Errors = errors;
    }

    public ValidationException(Dictionary<string, string> errors, Exception innerException)
        : base("验证失败", innerException)
    {
        Errors = errors;
    }
}

/// <summary>
/// API 异常 — 带有 HTTP 状态码、错误码和响应体
/// Python 等价：
///   class APIError(Exception):
///       def __init__(self, status_code, error_code, message, details=None):
///           ...
/// </summary>
public class ApiException : Exception
{
    public int StatusCode { get; }
    public string ErrorCode { get; }
    public Dictionary<string, object> Details { get; }

    public ApiException(int statusCode, string errorCode, string message,
                        Dictionary<string, object>? details = null)
        : base(message)
    {
        StatusCode = statusCode;
        ErrorCode = errorCode;
        Details = details ?? new Dictionary<string, object>();
    }

    /// <summary>
    /// 转换为 JSON 字符串，方便返回给前端
    /// Python 等价：
    ///   def to_dict(self): return {"status_code": ..., "error_code": ..., ...}
    /// </summary>
    public string ToJson()
    {
        var detailsStr = string.Join(", ",
            Details.Select(kv => $"\"{kv.Key}\": \"{kv.Value}\""));
        return $"{{\"status_code\": {StatusCode}, \"error_code\": \"{ErrorCode}\", " +
               $"\"message\": \"{Message}\", \"details\": {{{detailsStr}}}}}";
    }
}

// =============================================================
// 辅助方法
// =============================================================

static class HelperMethods
{
    public static void HandleDatabaseOperation()
    {
        throw new ConnectionException2("数据库连接池已满");
    }
}
