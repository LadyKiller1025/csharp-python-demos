# ============================================================
# Python datetime 时间处理完全指南
# 对应文章：4.9 datetime —— 时间日期处理
# C# 对比：DateTime / DateTimeOffset / TimeZoneInfo / NodaTime
# ============================================================
#
# 【核心对比】
#   Python datetime   →  内置模块，datetime/date/time 三个核心类
#   C# 时间处理      →  DateTime（值类型，不可变）
#                       DateTimeOffset（带偏移量）
#                       TimeZoneInfo（时区）
#                       NodaTime（第三方，功能最强，类似 Python dateutil）
#
# 【最大差异】
#   Python 的 datetime 是不可变类（但 tzinfo 需要额外库处理时区）
#   C# 的 DateTime 是值类型（struct），默认无时区（类似 naive datetime）
#   C# 11+ / .NET 8+ 支持 DateOnly / TimeOnly（类似 Python date/time）
# ============================================================

from datetime import datetime, timedelta, timezone, date, time
from zoneinfo import ZoneInfo  # Python 3.9+ 内置时区支持

print("=" * 60)
print("时间处理：Python datetime vs C# DateTime")
print("=" * 60)


# ============================================================
# 1. 创建时间对象 —— 对比 C# DateTime
# ============================================================
# 【C# 等价】
#   DateTime now = DateTime.Now;         → datetime.now()
#   DateTime today = DateTime.Today;     → date.today()
#   DateTime utcNow = DateTime.UtcNow;   → datetime.now(timezone.utc)
#   DateTime specific = new DateTime(2026, 5, 15, 10, 30, 0);
# ============================================================
print("\n===== 1. 创建时间对象 =====")

now = datetime.now()                        # 当前本地时间（naive）
today = date.today()                        # 今天日期
utc_now = datetime.now(timezone.utc)        # UTC 时间（aware）
print(f"当前时间:   {now}")
print(f"今天日期:   {today}")
print(f"UTC 时间:   {utc_now}")

# 指定时间
specific = datetime(2026, 5, 15, 10, 30, 0)
print(f"指定时间:   {specific}")

# 只创建时间对象（不带日期）
t = time(14, 30, 0)
print(f"时间对象:   {t}")

# Python 独有：combine 组合日期和时间
combined = datetime.combine(today, t)
print(f"组合后:     {combined}")

# 【C# 对比】
# C#: DateTime 是值类型（struct），默认创建时就是当地时区
# Python: datetime.now() 返回 naive（无时区），需要手动加 timezone


# ============================================================
# 2. 格式化 —— strftime / strptime
# ============================================================
# 【C# 等价】
#   now.ToString("yyyy年MM月dd日 HH:mm:ss")   → now.strftime("...")
#   DateTime.ParseExact("2026-05-15", "yyyy-MM-dd", null)
#                                                → datetime.strptime(...)
#
# 格式符差异：
#   Python %Y  →  C# yyyy
#   Python %m  →  C# MM
#   Python %d  →  C# dd
#   Python %H  →  C# HH
#   Python %M  →  C# mm
#   Python %S  →  C# ss
#   Python %A  →  C# dddd
# ============================================================
print("\n===== 2. 格式化 =====")

# strftime: datetime → 字符串
# 【C# 等价】string formatted = now.ToString("yyyy年MM月dd日 HH:mm:ss");
formatted = now.strftime("%Y年%m月%d日 %H:%M:%S")
print(f"strftime: {formatted}")

# strptime: 字符串 → datetime
# 【C# 等价】DateTime parsed = DateTime.ParseExact("2026-05-15", "yyyy-MM-dd", null);
parsed = datetime.strptime("2026-05-15", "%Y-%m-%d")
print(f"strptime: {parsed}")

# 常用格式符
print(f"  %Y-%m-%d:  {now.strftime('%Y-%m-%d')}")
print(f"  %H:%M:%S:  {now.strftime('%H:%M:%S')}")
print(f"  %A:        {now.strftime('%A')}")        # 星期几英文
print(f"  %a:        {now.strftime('%a')}")        # 星期几缩写
print(f"  %B:        {now.strftime('%B')}")        # 月份英文
print(f"  %I:%M %p:  {now.strftime('%I:%M %p')}")  # 12小时制

# 【C# vs Python】
# C# 的 ToString() 比 Python 的 strftime() 更灵活
# C#: now.ToString("yyyy-MM-dd") 直接在对象上调用
# Python: now.strftime("%Y-%m-%d") 需要调用方法


# ============================================================
# 3. isoformat / fromisoformat —— ISO 8601 标准格式
# ============================================================
# 【C# 等价】
#   now.ToString("o") 或 now.ToString("yyyy-MM-ddTHH:mm:ss.ffffff")
#   DateTimeOffset.Parse(str)
# ============================================================
print("\n===== 3. isoformat / fromisoformat =====")

# ISO 8601 格式（全球通用标准）
# 【C# 等价】string iso = now.ToString("o");
iso_str = now.isoformat()
print(f"isoformat:       {iso_str}")

utc_iso = utc_now.isoformat()
print(f"UTC isoformat:   {utc_iso}")

# 解析 ISO 格式
# 【C# 等价】DateTimeOffset parsed = DateTimeOffset.Parse(iso_str);
parsed_back = datetime.fromisoformat(iso_str)
print(f"fromisoformat:   {parsed_back}")

# Python 3.11+ 还支持 fromisoformat 解析更多格式
# C# 的 DateTimeOffset.Parse 更宽松，能解析各种格式

# 【Python vs C#】
# Python isoformat → C# ToString("o") (round-trip 格式)
# C# 的 "o" 格式和 Python 的 isoformat 几乎等价


# ============================================================
# 4. 时间运算 —— timedelta
# ============================================================
# 【C# 等价】
#   now.AddDays(1)     → now + timedelta(days=1)
#   now.AddHours(2)    → now + timedelta(hours=2)
#   TimeSpan diff = now - other   → timedelta 对象
#   diff.TotalDays     → diff.days / diff.total_seconds()
# ============================================================
print("\n===== 4. 时间运算 =====")

tomorrow = now + timedelta(days=1)
next_week = now + timedelta(weeks=1)
two_hours_later = now + timedelta(hours=2)
next_month = now + timedelta(days=30)

print(f"明天:      {tomorrow.strftime('%Y-%m-%d %H:%M')}")
print(f"下周:      {next_week.strftime('%Y-%m-%d %H:%M')}")
print(f"2小时后:   {two_hours_later.strftime('%Y-%m-%d %H:%M')}")

# 时间差
diff = tomorrow - now
print(f"\n差值:")
print(f"  .days 属性:        {diff.days} 天")
print(f"  .total_seconds():  {diff.total_seconds()} 秒")

# 计算年龄
birthday = datetime(1990, 5, 20)
age_days = (now - birthday).days
age_years = age_days // 365
print(f"\n从 1990-05-20 到今: {age_days} 天 ≈ {age_years} 岁")

# 【C# 对比】
# C#: DateTime.AddHours/AddDays 返回新 DateTime（方法调用方式）
# Python: 用 + timedelta() 运算符，更直观
# C#: TimeSpan 只能存储时间差，不能表示"某个时间点"


# ============================================================
# 5. replace —— 替换日期/时间部分
# ============================================================
# 【C# 等价】
#   now.AddYears(1)    → now.replace(year=now.year + 1)
#   C# 没有直接的 replace 方法，用 Add 系列方法
# ============================================================
print("\n===== 5. replace 替换日期部分 =====")

# 替换年份
same_day_next_year = now.replace(year=now.year + 1)
print(f"明年同日: {same_day_next_year.strftime('%Y-%m-%d %H:%M')}")

# 替换时间为午夜
midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
print(f"今天午夜: {midnight}")

# 替换日期为指定日期
same_time_different_day = now.replace(day=1)
print(f"本月1号:  {same_time_different_day}")

# 【C# vs Python】
# Python: replace() 返回新对象，可以同时替换多个部分
# C#: 没有 replace 方法，需要用 AddYears/AddMonths/AddDays 分别操作
# Python replace 更灵活，一次可以改多个字段


# ============================================================
# 6. 时区处理 —— zoneinfo (Python 3.9+) / TimeZoneInfo (C#)
# ============================================================
# 【C# 等价】
#   TimeZoneInfo beijingTz = TimeZoneInfo.FindSystemTimeZoneById("China Standard Time");
#   DateTime nowBj = TimeZoneInfo.ConvertTimeFromUtc(utcNow, beijingTz);
#
# Python zoneinfo 是 Python 3.9+ 新增的标准库
# 之前需要 dateutil 第三方库（类似 C# 的 NodaTime）
# ============================================================
print("\n===== 6. 时区处理 =====")

# 创建时区对象
# 【C# 等价】TimeZoneInfo beijingTz = TimeZoneInfo.FindSystemTimeZoneById("China Standard Time");
beijing_tz = ZoneInfo("Asia/Shanghai")
tokyo_tz = ZoneInfo("Asia/Tokyo")
utc_tz = timezone.utc

# 获取带时区的当前时间
now_bj = datetime.now(beijing_tz)
now_tokyo = now_bj.astimezone(tokyo_tz)
now_utc = now_bj.astimezone(utc_tz)

print(f"北京时间:  {now_bj.strftime('%Y-%m-%d %H:%M:%S %Z')}")
print(f"东京时间:  {now_tokyo.strftime('%Y-%m-%d %H:%M:%S %Z')}")
print(f"UTC 时间:  {now_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}")

# astimezone —— 转换时区
# 【C# 等价】DateTime tokyoTime = TimeZoneInfo.ConvertTime(nowBj, tokyoTz);
us_east = ZoneInfo("America/New_York")
now_us = now_bj.astimezone(us_east)
print(f"纽约时间:  {now_us.strftime('%Y-%m-%d %H:%M:%S %Z')}")


# ============================================================
# 7. naive vs aware —— 有无时区信息
# ============================================================
# 【C# 等价】
#   DateTime（无 Kind）= naive
#   DateTimeOffset = aware
#   UtcDateTime = UTC aware
# ============================================================
print("\n===== 7. naive vs aware =====")

naive = datetime.now()                   # 无时区信息（naive）
aware = datetime.now(timezone.utc)       # 有时区信息（aware）
print(f"naive:   {naive}  (无时区)")
print(f"aware:   {aware}  (有时区)")
print(f"naive.tzinfo is None: {naive.tzinfo is None}")
print(f"aware.tzinfo:         {aware.tzinfo}")

# 【C# 对比】
# C#: DateTime 默认是 Unspecified（类似 naive）
#      DateTimeOffset 自带偏移量（类似 aware）
#      不能混合比较 naive 和 aware
# Python: 同样不能混合比较 naive 和 aware datetime


# ============================================================
# 8. timezone 固定偏移量
# ============================================================
# 【C# 等价】
#   TimeZoneInfo.CreateCustomTimeZone("UTC+8", TimeSpan.FromHours(8), ...)
# ============================================================
print("\n===== 8. timezone 固定偏移量 =====")

# 创建固定偏移时区
utc8 = timezone(timedelta(hours=8))
utc5 = timezone(timedelta(hours=-5))

now_utc8 = datetime.now(utc8)
now_utc5 = datetime.now(utc5)

print(f"UTC+8:  {now_utc8.strftime('%H:%M:%S %Z')}")
print(f"UTC-5:  {now_utc5.strftime('%H:%M:%S %Z')}")

# 【C# 等价】
# var customTz = TimeZoneInfo.CreateCustomTimeZone(
#     "Custom", TimeSpan.FromHours(8), "Custom UTC+8");
# Python 的 timezone() 更简洁
# C# 的 CreateCustomTimeZone 更正式，支持名称和缩写


# ============================================================
# 9. Unix 时间戳
# ============================================================
# 【C# 等价】
#   long timestamp = ((DateTimeOffset)now).ToUnixTimeSeconds();
#   DateTime back = DateTimeOffset.FromUnixTimeSeconds(timestamp).DateTime;
# ============================================================
print("\n===== 9. Unix 时间戳 =====")

# datetime → timestamp
# 【C# 等价】((DateTimeOffset)now).ToUnixTimeSeconds()
timestamp = now.timestamp()
print(f"当前时间戳:   {timestamp:.0f}")
print(f"时间戳类型:   {type(timestamp)}")  # float（C# 是 long）

# timestamp → datetime
# 【C# 等价】DateTimeOffset.FromUnixTimeSeconds(timestamp).DateTime
back = datetime.fromtimestamp(timestamp)
print(f"转换回来:     {back}")

# 带时区的转换
back_utc = datetime.fromtimestamp(timestamp, tz=timezone.utc)
print(f"转换为 UTC:   {back_utc}")

# 【C# vs Python】
# Python: timestamp() 返回 float（含毫秒精度）
# C#: ToUnixTimeSeconds() 返回 long（只到秒）
#       ToUnixTimeMilliseconds() 返回 long（到毫秒）


# ============================================================
# 10. 实际场景
# ============================================================
print("\n===== 10. 实际场景 =====")

# 场景1：日志时间戳解析与计算
log_time = datetime.strptime("2026-05-15 10:30:45", "%Y-%m-%d %H:%M:%S")
elapsed = datetime.now() - log_time
print(f"日志时间: {log_time}")
print(f"距今: {elapsed.days}天 {elapsed.seconds // 3600}小时 {elapsed.seconds % 3600 // 60}分钟")

# 场景2：日期范围遍历
start = date(2026, 1, 1)
end = date(2026, 12, 31)
days_count = (end - start).days + 1
print(f"\n2026年共 {days_count} 天")

# 场景3：比较时间
future = datetime(2030, 1, 1)
past = datetime(2020, 1, 1)
print(f"2030 > 2020? {future > past}")    # True（直接比较）
print(f"2030 - 2020 = {(future - past).days} 天")

# 场景4：工作日计算（简单版）
# 【C# NodaTime 等价】NodaTime.Calendars.IsoCalendarSystem
next_monday = now + timedelta(days=(7 - now.weekday()) % 7)
print(f"下个周一: {next_monday.strftime('%Y-%m-%d %A')}")

# 场景5：时间戳格式化为 ISO 字符串（API 常用）
api_time = datetime.now(timezone.utc).isoformat()
print(f"API 时间戳: {api_time}")


# ============================================================
# 总结对比表
# ============================================================
print("\n" + "=" * 60)
print("总结：Python datetime vs C# DateTime")
print("=" * 60)
comparison = """
┌────────────────────────┬──────────────────────────┬───────────────────────────────┐
│      操作              │    Python datetime       │    C# DateTime               │
├────────────────────────┼──────────────────────────┼───────────────────────────────┤
│ 当前时间               │ datetime.now()           │ DateTime.Now                 │
│ 今天日期               │ date.today()             │ DateTime.Today               │
│ UTC 时间               │ datetime.now(timezone.utc)│ DateTime.UtcNow             │
│ 指定时间               │ datetime(2026,5,15,10,30)│ new DateTime(2026,5,15,10,30)│
│ 格式化                 │ p.strftime("%Y-%m-%d")   │ now.ToString("yyyy-MM-dd")   │
│ 解析字符串             │ datetime.strptime(s,f)   │ DateTime.ParseExact(s,f,null)│
│ ISO 格式               │ p.isoformat()            │ now.ToString("o")            │
│ 时间加减               │ p + timedelta(days=1)    │ now.AddDays(1)               │
│ 时间差                 │ now - other → timedelta  │ now - other → TimeSpan       │
│ 替换部分               │ p.replace(year=2030)     │ 无直接对应（用 Add 方法）     │
│ 时区转换               │ p.astimezone(tz)         │ TimeZoneInfo.ConvertTime()   │
│ 获取时区               │ ZoneInfo("Asia/Shanghai")│ TimeZoneInfo.FindSystem...() │
│ Unix 时间戳            │ p.timestamp()            │ ((DateTimeOffset)p)          │
│                        │                          │   .ToUnixTimeSeconds()       │
│ 带偏移量               │ timezone(timedelta(h=8)) │ DateTimeOffset               │
│ 不可变性               │ datetime 是不可变的       │ DateTime 是 struct（值类型）  │
│ Naive/Aware            │ 无 tzinfo / 有 tzinfo    │ Unspecified / DateTimeOffset │
└────────────────────────┴──────────────────────────┴───────────────────────────────┘
"""
print(comparison)
print("完成!")
