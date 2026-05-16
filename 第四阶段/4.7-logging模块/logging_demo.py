# ============================================================
# Python logging 模块完全指南
# 对应文章：4.7 logging 模块 —— 专业的日志系统
# C# 对比：ILogger / Serilog / NLog
# ============================================================
#
# 【核心对比】
#   Python logging   →  内置模块，基于 Logger + Handler + Formatter 架构
#   C# logging      →  Microsoft.Extensions.Logging (ILogger)
#                      + Serilog（结构化日志，最流行）
#                      + NLog（配置灵活，功能全面）
#
# 关键概念映射：
#   Python Logger    ↔  C# ILogger
#   Python Handler   ↔  C# Sink (Serilog) / Target (NLog)
#   Python Formatter ↔  C# OutputTemplate (Serilog) / Layout (NLog)
#   Python Level     ↔  C# LogLevel
# ============================================================

import logging
import sys
import os
from logging.handlers import RotatingFileHandler

print("=" * 60)
print("logging 模块 vs C# Microsoft.Extensions.Logging / Serilog")
print("=" * 60)


# ============================================================
# 1. basicConfig —— 快速配置日志（一行搞定）
# ============================================================
# 【C# 等价】
#   // Serilog:
#   Log.Logger = new LoggerConfiguration()
#       .MinimumLevel.Debug()
#       .WriteTo.Console()
#       .CreateLogger();
#
#   // Microsoft.Extensions.Logging:
#   builder.Logging.SetMinimumLevel(LogLevel.Debug);
# ============================================================
print("\n===== 1. basicConfig 快速配置 =====")

# basicConfig 是 Python 独有的快捷方式，C# 没有对应物
# 它只在第一次调用时生效，后续调用无效（除非 force=True）
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    # stream=sys.stdout,  # 默认输出到 stderr
)

logger = logging.getLogger("basic_demo")
logger.debug("这是调试信息 — 看不到因为 root logger 传播规则")
logger.info("这是普通信息")
logger.warning("这是警告信息")
logger.error("这是错误信息")
logger.critical("这是严重错误")

# 【C# 对比】
# C# 的日志配置通常在 DI 容器中完成，比 Python 复杂得多
# Python: logging.basicConfig(level=logging.DEBUG) 一行搞定
# C#: 需要在 Startup/Program 中配置 ServiceCollection


# ============================================================
# 2. 日志级别 —— DEBUG < INFO < WARNING < ERROR < CRITICAL
# ============================================================
# 【C# 等价】
#   LogLevel.Trace   (Python 没有，但有第三方 loguru)
#   LogLevel.Debug
#   LogLevel.Information
#   LogLevel.Warning
#   LogLevel.Error
#   LogLevel.Critical
# ============================================================
print("\n===== 2. 日志级别 =====")

# Python 日志级别数值（方便记忆）
# NOTSET=0, DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50
levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

print("Python 日志级别:")
for name, value in levels.items():
    print(f"  {name:10s} = {value}")

# 【C# 对比】
# C#: LogLevel 枚举值从 0(Trace) 到 6(Critical)
# Python: 用整数 10/20/30/40/50 表示
# 两者都是数字越大越严重


# ============================================================
# 3. getLogger —— 命名 Logger（层级结构）
# ============================================================
# 【C# 等价】
#   ILogger<T> logger = LoggerFactory.CreateLogger<T>();
#   ILogger logger = LoggerFactory.CreateLogger("MyApp.Service");
#
# Python 的 Logger 按 '.' 分隔符形成层级
# "myapp" 是 "myapp.service.user" 的父 Logger
# ============================================================
print("\n===== 3. getLogger 命名 Logger =====")

# 创建层级 Logger
root_logger = logging.getLogger("myapp")
root_logger.setLevel(logging.DEBUG)

# 子 logger（用 . 分隔，自动形成层级）
service_logger = logging.getLogger("myapp.service")
user_logger = logging.getLogger("myapp.service.user")

# 每个 Logger 向上冒泡到父 Logger（传播机制）
user_logger.info("用户操作: 查询用户")  # 会传播到 myapp Logger

# 【Python 特有】Logger 层级传播
# "myapp.service.user" 的日志会传播到 "myapp.service" 再到 "myapp"
# 这和 C# 的 Logger 互相独立不同
# C# 每个 Logger<T> 是独立的，没有传播机制
print(f"  root_logger.name = {root_logger.name}")
print(f"  service_logger.name = {service_logger.name}")
print(f"  user_logger.name = {user_logger.name}")


# ============================================================
# 4. Handler —— 日志输出到不同目标
# ============================================================
# 【C# 等价】
#   .WriteTo.Console()          → StreamHandler
#   .WriteTo.File("app.log")   → FileHandler
#   .WriteTo.File(..., rollingInterval: RollingInterval.Day)
#                                 → RotatingFileHandler
#   .WriteTo.Seq(...)           → 没有直接对应
#
# Handler 负责日志输出到哪里（控制台/文件/网络等）
# Formatter 负责日志输出格式
# ============================================================
print("\n===== 4. Handler 处理器 =====")

# --- 4a. StreamHandler（输出到流，默认 stderr）---
# 【C# 等价】Serilog 的 .WriteTo.Console()
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter("[%(levelname)s] %(message)s")
console_handler.setFormatter(console_format)

# --- 4b. FileHandler（输出到文件）---
# 【C# 等价】Serilog 的 .WriteTo.File("app.log")
# 注意：FileHandler 是全量写入，不会自动轮转
file_handler = logging.FileHandler("app.log", encoding="utf-8", errors="replace")
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
file_handler.setFormatter(file_format)

# --- 4c. RotatingFileHandler（自动轮转文件）---
# 【C# 等价】Serilog 的 .WriteTo.File(..., rollingInterval: RollingInterval.Day)
#            NLog 的 <target xsi:type="File" fileName="app.log" archiveEvery="Day"/>
rotating_handler = RotatingFileHandler(
    "rotating.log",
    maxBytes=1024 * 1024,   # 1MB
    backupCount=3,           # 保留 3 个备份
    encoding="utf-8",
    errors="replace"
)
rotating_handler.setLevel(logging.DEBUG)
rotating_handler.setFormatter(file_format)

# 组装 Logger
app_logger = logging.getLogger("myapp")
app_logger.setLevel(logging.DEBUG)
app_logger.addHandler(console_handler)
app_logger.addHandler(file_handler)
app_logger.addHandler(rotating_handler)

app_logger.info("应用启动")
app_logger.debug("加载配置完成")
app_logger.warning("配置项缺失，使用默认值")
app_logger.error("连接数据库失败", exc_info=True)

# 【C# vs Python Handler 对比】
# Python: Handler 可以动态添加/移除
# C#: Sink/Target 通常在启动时配置，运行时修改较复杂
# 两者都支持多目标输出（同时写控制台和文件）


# ============================================================
# 5. NullHandler —— 库开发者的最佳实践
# ============================================================
# 【C# 等价】
#   C# 没有 NullHandler 对应物
#   C# 库通常不配置日志，由使用者决定
# ============================================================
print("\n===== 5. NullHandler（库开发最佳实践）=====")

# 如果你开发一个 Python 库，应该添加 NullHandler
# 这样库的日志不会因为没有配置而报错或输出到 stderr
library_logger = logging.getLogger("mypackage")
library_logger.addHandler(logging.NullHandler())

# NullHandler 什么都不做，只是抑制 "No handler found" 警告
library_logger.info("这条日志不会输出，但也不会报错")
print("NullHandler 已添加到 mypackage logger（静默处理）")

# 【C# 对比】
# C# 库一般不注册任何日志 provider，由应用程序配置
# Python 需要 NullHandler 来避免 stderr 告警


# ============================================================
# 6. Logger 层级与传播机制
# ============================================================
# 【C# 等价】
#   C# 的 Logger 没有自动传播机制
#   C# 需要手动在每个类中注入 ILogger<T>
# ============================================================
print("\n===== 6. Logger 层级与传播 =====")

# 清除之前添加的 handler，避免重复输出
for h in app_logger.handlers[:]:
    app_logger.removeHandler(h)

# 重新配置简洁的控制台输出
simple_handler = logging.StreamHandler(sys.stdout)
simple_handler.setFormatter(logging.Formatter("[%(name)s] %(levelname)s: %(message)s"))
app_logger.addHandler(simple_handler)

# 父 Logger 设置级别，子 Logger 继承
app_logger.setLevel(logging.WARNING)  # 只输出 WARNING 及以上
app_logger.debug("这条不会输出（被父 Logger 过滤）")
app_logger.warning("这条会输出")

# 子 Logger 可以设置更低级别
service_logger.setLevel(logging.DEBUG)
service_logger.debug("子 Logger 可以输出 DEBUG")

# propagate = False 可以阻止日志向上传播
no_propagate = logging.getLogger("myapp.noprop")
no_propagate.addHandler(logging.StreamHandler(sys.stdout))
no_propagate.propagate = False  # 不传播到父 Logger
no_propagate.info("这条只输出到自己的 handler")

# 【C# 对比】
# Python: propagate=True 时日志向父 Logger 冒泡
# C#: 每个 Logger 是独立的，没有冒泡机制
# Python 的层级传播很强大，但也容易造成重复输出


# ============================================================
# 7. dictConfig —— 用字典配置日志系统
# ============================================================
# 【C# 等价】
#   appsettings.json 中配置 Logging 节点
#   Serilog: .ReadFrom.Configuration(configuration)
# ============================================================
print("\n===== 7. dictConfig 字典配置 =====")

import logging.config

# 用字典一次性配置整个日志系统（比 basicConfig 更灵活）
LOGGING_CONFIG = {
    "version": 1,  # 必须是 1
    "disable_existing_loggers": False,

    # 格式化器
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
        "simple": {
            "format": "[%(levelname)s] %(message)s"
        },
    },

    # 处理器
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": "dictconfig_demo.log",
            "encoding": "utf-8",
            "errors": "replace",
        },
    },

    # 根 Logger 配置
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    },
}

# 应用字典配置
logging.config.dictConfig(LOGGING_CONFIG)

dict_logger = logging.getLogger("dictconfig_demo")
dict_logger.info("dictConfig 配置的 Logger")
dict_logger.debug("这条会写入文件但不输出到控制台")

print("dictConfig 配置完成（类比 C# 的 appsettings.json）")

# 【C# vs Python】
# C# 用 appsettings.json + .ReadFrom.Configuration()
# Python 用 dictConfig() + 字典（也可以从 YAML/JSON 加载）
# 本质一样：外部化配置，代码不硬编码


# ============================================================
# 8. 实际场景：类中使用 Logger
# ============================================================
# 【C# 等价】
#   public class UserService
#   {
#       private readonly ILogger<UserService> _logger;
#       public UserService(ILogger<UserService> logger)
#       {
#           _logger = logger;
#       }
#   }
# ============================================================
print("\n===== 8. 实际场景：类中使用 Logger =====")


class UserService:
    """用 Logger 记录服务操作 —— 和 C# 的注入模式类似"""

    def __init__(self):
        # Python: 用 __name__ 自动获取模块名作为 Logger 名
        # C#: 用泛型 ILogger<UserService> 自动以类名命名
        self.logger = logging.getLogger(__name__)

    def get_user(self, user_id):
        self.logger.info(f"查询用户: {user_id}")
        if user_id <= 0:
            self.logger.error(f"无效的用户ID: {user_id}")
            raise ValueError(f"无效的用户ID: {user_id}")
        self.logger.debug(f"用户 {user_id} 查询成功")
        return {"id": user_id, "name": f"User_{user_id}"}


# 测试
service = UserService()
try:
    user = service.get_user(1)
    service.get_user(-1)  # 触发错误
except ValueError:
    pass

# 清理：先关闭所有 handler，释放文件锁，再删除临时文件
import logging.config as _logconfig

# 关闭 root logger 上的所有 handler
root = logging.getLogger()
for h in root.handlers[:]:
    h.flush()
    h.close()
    root.removeHandler(h)

# 关闭 app_logger 上的所有 handler
for h in app_logger.handlers[:]:
    h.flush()
    h.close()
    app_logger.removeHandler(h)

# 关闭 file_handler 和 rotating_handler（显式引用）
for h in [file_handler, rotating_handler]:
    try:
        h.flush()
        h.close()
    except Exception:
        pass

# 删除临时文件
for fname in ["app.log", "rotating.log", "dictconfig_demo.log"]:
    if os.path.exists(fname):
        try:
            os.remove(fname)
        except PermissionError:
            pass  # 文件被占用时跳过


# ============================================================
# 总结对比表
# ============================================================
print("\n" + "=" * 60)
print("总结：Python logging vs C# 日志框架")
print("=" * 60)
comparison = """
┌──────────────────────┬──────────────────────────┬───────────────────────────────┐
│      概念            │    Python logging        │    C# 日志框架                │
├──────────────────────┼──────────────────────────┼───────────────────────────────┤
│ 核心接口             │ Logger                   │ ILogger<T>                    │
│ 输出目标             │ Handler                  │ Sink / Target                 │
│ 输出格式             │ Formatter                │ OutputTemplate / Layout       │
│ 日志级别             │ DEBUG/INFO/WARNING/...   │ LogLevel.Debug/Info/...       │
│ 快速配置             │ basicConfig()            │ 无（需手动配置 DI）            │
│ 字典/配置文件配置    │ dictConfig()             │ appsettings.json              │
│ 命名 Logger          │ getLogger("name")        │ LoggerFactory.CreateLogger()  │
│ 库静默处理           │ NullHandler              │ 无需（由应用配置）             │
│ 层级传播             │ propagate=True           │ 无传播机制                    │
│ 文件轮转             │ RotatingFileHandler      │ rollingInterval (Serilog)     │
│ 结构化日志           │ 无内置（loguru 第三方）  │ Serilog 原生支持              │
│ DI 集成              │ 手动 getLogger           │ 依赖注入 ILogger<T>           │
└──────────────────────┴──────────────────────────┴───────────────────────────────┘
"""
print(comparison)
print("完成!")
