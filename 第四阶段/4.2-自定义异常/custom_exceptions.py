"""
Python 自定义异常完整示例
对应文章：4.2 自定义异常

C# 对比：
  Python 自定义异常继承 Exception    ≈  C# 自定义异常继承 Exception
  Python __init__ with context       ≈  C# 构造函数 with innerException
  Python raise X from Y             ≈  C# throw new X("msg", innerEx)
  Python 无需 [Serializable]        ≈  C# 传统上需要 [Serializable] (跨 AppDomain)
"""

print("=" * 60)
print("1. 基础自定义异常")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   public class BusinessException : Exception
#   {
#       public int ErrorCode { get; }
#       public BusinessException(string message, int errorCode)
#           : base(message) { ErrorCode = errorCode; }
#   }
# -------------------------------------------------------
class BusinessException(Exception):
    """业务异常基类 — 带错误码"""
    def __init__(self, message: str, error_code: int):
        # 调用 Exception.__init__(message) — 等同 C# 的 base(message)
        super().__init__(message)
        self.error_code = error_code

    def __str__(self):
        return f"[{self.error_code}] {self.args[0]}"


# 使用
try:
    raise BusinessException("用户不存在", 404)
except BusinessException as e:
    print(f"捕获业务异常: {e}")
    print(f"  错误码: {e.error_code}")
    print(f"  消息: {e.args[0]}")

print()
print("=" * 60)
print("2. 异常继承 — 带上下文信息的 __init__")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   public BusinessException(string message, int errorCode, Exception innerException)
#       : base(message, innerException)
#   {
#       ErrorCode = errorCode;
#   }
# -------------------------------------------------------
class DatabaseError(Exception):
    """数据库异常 — 带连接信息和查询上下文"""
    def __init__(self, message: str, connection_string: str = "", query: str = ""):
        super().__init__(message)
        self.connection_string = connection_string
        self.query = query

    def __str__(self):
        base = super().__str__()
        details = []
        if self.connection_string:
            details.append(f"连接: {self.connection_string}")
        if self.query:
            details.append(f"查询: {self.query}")
        return f"{base} ({', '.join(details)})" if details else base


try:
    raise DatabaseError(
        "查询超时",
        connection_string="server=localhost;db=mydb",
        query="SELECT * FROM users"
    )
except DatabaseError as e:
    print(f"数据库异常: {e}")

print()
print("=" * 60)
print("3. raise...from — 异常链保留原始异常")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   throw new BusinessException("处理失败", 500, originalException);
#   // 或 ExceptionDispatchInfo.Capture(ex).Throw() 保留堆栈
# -------------------------------------------------------
class ServiceException(Exception):
    """服务层异常 — 包装底层异常"""
    def __init__(self, message: str, cause: Exception = None):
        super().__init__(message)
        self.__cause__ = cause  # 手动设置 cause（等同 raise...from）


def process_order(order_id: int) -> dict:
    """模拟一个处理流程，底层异常被包装为业务异常"""
    try:
        # 模拟数据库查询
        if order_id < 0:
            raise ValueError(f"无效的订单ID: {order_id}")
        if order_id > 1000:
            raise ConnectionError("数据库连接超时")
        return {"id": order_id, "status": "ok"}
    except ValueError as e:
        # raise...from 保留原始异常作为 __cause__
        raise BusinessException("参数验证失败", 400) from e
    except ConnectionError as e:
        # from None 表示不保留原始异常
        raise ServiceException("服务暂时不可用，请稍后重试") from None


# 场景 1：原始异常被保留
print("场景 1 - raise...from (保留原始异常):")
try:
    process_order(-1)
except BusinessException as e:
    print(f"  业务异常: {e}")
    print(f"  原始异常 (__cause__): {e.__cause__}")

# 场景 2：原始异常被抑制
print("\n场景 2 - raise...from None (抑制原始异常):")
try:
    process_order(9999)
except ServiceException as e:
    print(f"  服务异常: {e}")
    print(f"  __cause__: {e.__cause__}")  # None — 原始异常被抑制

print()
print("=" * 60)
print("4. 异常层次结构 — 分层捕获")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   public class AppException : Exception { }
#   public class DatabaseException : AppException { }
#   public class ConnectionException : DatabaseException { }
#
#   catch (AppException)       // 捕获所有应用异常
#   catch (DatabaseException)  // 只捕获数据库异常
# -------------------------------------------------------
class AppError(Exception):
    """应用错误基类 — 所有业务异常的根"""
    pass

class DatabaseError2(AppError):
    """数据库错误"""
    pass

class ConnectionError2(DatabaseError2):
    """连接错误 — 继承自数据库错误"""
    pass

class QueryError2(DatabaseError2):
    """查询错误"""
    pass


# 演示分层捕获
errors_to_test = [
    AppError("通用应用错误"),
    DatabaseError2("数据库错误"),
    ConnectionError2("连接失败"),
    QueryError2("查询语法错误"),
]

for err in errors_to_test:
    try:
        raise err
    except ConnectionError2 as e:
        # 最具体的异常优先捕获
        print(f"  [连接层] {type(e).__name__}: {e}")
    except QueryError2 as e:
        print(f"  [查询层] {type(e).__name__}: {e}")
    except DatabaseError2 as e:
        # 捕获所有数据库相关异常（ConnectionError2 和 QueryError2 也会走到这里如果没有更具体的）
        print(f"  [数据库层] {type(e).__name__}: {e}")
    except AppError as e:
        print(f"  [应用层] {type(e).__name__}: {e}")

print()
print("=" * 60)
print("5. 验证异常 — 带详细错误信息")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   public class ValidationException : Exception
#   {
#       public IDictionary<string, string> Errors { get; }
#       // ...
#   }
# -------------------------------------------------------
class ValidationException(Exception):
    """验证异常 — 携带多个字段的验证错误"""
    def __init__(self, errors: dict[str, str]):
        # 把所有错误信息拼接成一条消息
        summary = f"验证失败: {'; '.join(f'{k}={v}' for k, v in errors.items())}"
        super().__init__(summary)
        self.errors = errors  # 字段名 -> 错误信息


def validate_user(data: dict) -> dict:
    """模拟用户数据验证"""
    errors = {}
    if not data.get("name"):
        errors["name"] = "名字不能为空"
    if not data.get("age"):
        errors["age"] = "年龄必须大于0"
    elif not isinstance(data["age"], int) or data["age"] <= 0:
        errors["age"] = "年龄必须是正整数"
    if not data.get("email"):
        errors["email"] = "邮箱不能为空"

    if errors:
        raise ValidationException(errors)
    return data


# 正常场景
print("正常验证:")
try:
    user = validate_user({"name": "Alice", "age": 25, "email": "alice@example.com"})
    print(f"  验证通过: {user}")
except ValidationException as e:
    print(f"  {e}")

# 失败场景
print("\n失败验证:")
try:
    validate_user({"name": "", "age": -1})
except ValidationException as e:
    print(f"  {e}")
    print(f"  错误详情:")
    for field, message in e.errors.items():
        print(f"    {field}: {message}")

print()
print("=" * 60)
print("6. 异常的 __traceback__ 与堆栈信息")
print("=" * 60)

# -------------------------------------------------------
# Python 特有：异常对象自带 __traceback__ 属性
# C# 对比：通过 ex.StackTrace 字符串获取
# -------------------------------------------------------
import traceback

def level3():
    raise RuntimeError("深层错误")

def level2():
    level3()

def level1():
    level2()

try:
    level1()
except RuntimeError as e:
    print(f"异常消息: {e}")
    print(f"异常类型: {type(e).__name__}")
    print("完整堆栈:")
    # traceback.format_exception 返回堆栈字符串列表
    tb_lines = traceback.format_exception(type(e), e, e.__traceback__)
    for line in tb_lines:
        print(f"  {line}", end="")

print()
print("=" * 60)
print("7. 异常作为字典 — 结构化错误信息")
print("=" * 60)

# -------------------------------------------------------
# 实际项目中，自定义异常常携带结构化数据
# C# 中通常通过自定义属性实现
# -------------------------------------------------------
class APIError(Exception):
    """API 异常 — 带有 HTTP 状态码、错误码和响应体"""
    def __init__(self, status_code: int, error_code: str, message: str, details: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}

    def to_dict(self) -> dict:
        """转换为字典，方便序列化为 JSON 返回给前端"""
        return {
            "status_code": self.status_code,
            "error_code": self.error_code,
            "message": self.args[0],
            "details": self.details,
        }


try:
    raise APIError(
        status_code=422,
        error_code="VALIDATION_ERROR",
        message="请求参数无效",
        details={"field": "email", "reason": "格式不正确"}
    )
except APIError as e:
    print(f"API 异常: {e}")
    print(f"结构化信息: {e.to_dict()}")

print()
print("=" * 60)
print("8. except 块中使用 raise 重新抛出")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   catch { throw; }  // 重新抛出，保留堆栈
#   catch (Exception ex) { throw new X("msg", ex); }  // 包装后抛出
# -------------------------------------------------------
def handle_database_operation():
    """演示在 except 中处理后重新抛出"""
    try:
        raise ConnectionError("数据库连接池已满")
    except ConnectionError as e:
        # 方式 1：直接 raise — 保留原始异常和堆栈（推荐）
        print(f"  日志: 捕获到连接错误，重新抛出...")
        raise  # 重新抛出，完全保留原始异常

try:
    handle_database_operation()
except ConnectionError as e:
    print(f"  上层捕获: {e}")

print()
print("=" * 60)
print("9. 自定义异常最佳实践总结")
print("=" * 60)
print("""
Python 自定义异常最佳实践:
  1. 继承 Exception 而非 BaseException（BaseException 用于系统退出等）
  2. 在 __init__ 中接收并存储上下文信息
  3. 提供有意义的 __str__ 方法
  4. 使用 raise...from 保留异常链
  5. 设计合理的异常层次结构（基类 -> 具体类）

C# 对比:
  1. 继承 Exception（传统上还需 [Serializable] 用于跨 AppDomain）
  2. 提供多个构造函数：(message), (message, inner), (serialization, streaming)
  3. 标记为 Serializable（.NET Core+ 不再强制要求）
  4. 使用 throw new X("msg", innerEx) 保留异常链
  5. 设计合理的异常层次结构
""")

print("所有自定义异常示例运行完毕！")
