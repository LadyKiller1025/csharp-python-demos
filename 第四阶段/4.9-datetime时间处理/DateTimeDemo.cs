// ============================================================
// C# 时间处理完全指南（对标 Python datetime 模块）
// 对应文章：4.9 datetime —— 时间日期处理
// Python 对比：datetime / timedelta / timezone / zoneinfo
// ============================================================
//
// 【核心对比】
//   Python datetime   →  内置模块，datetime/date/time 三个核心类
//   C# 时间处理      →  DateTime（值类型 struct）
//                       DateTimeOffset（带偏移量）
//                       TimeZoneInfo（时区转换）
//                       NodaTime（第三方，功能最强）
//
// 【最大差异】
//   Python datetime 不可变，用 + timedelta 运算符
//   C# DateTime 是 struct，用 AddDays/AddHours 方法
//   C# 推荐用 DateTimeOffset 处理带时区的时间
// ============================================================

using System;
using System.TimeZoneInfo;

public class DateTimeDemo
{
    static void Main()
    {
        Console.WriteLine("============================================");
        Console.WriteLine("C# 时间处理 vs Python datetime 模块");
        Console.WriteLine("============================================");

        // ============================================================
        // 1. 创建时间对象
        // ============================================================
        // 【Python 等价】
        //   now = datetime.now()
        //   today = date.today()
        //   utc_now = datetime.now(timezone.utc)
        //   specific = datetime(2026, 5, 15, 10, 30, 0)
        // ============================================================
        Console.WriteLine("\n===== 1. 创建时间对象 =====");

        DateTime now = DateTime.Now;                       // 当前本地时间
        DateTime today = DateTime.Today;                   // 今天日期（时分秒为 0）
        DateTime utcNow = DateTime.UtcNow;                 // UTC 时间
        DateTime specific = new DateTime(2026, 5, 15, 10, 30, 0);  // 指定时间

        Console.WriteLine($"当前时间:   {now}");
        Console.WriteLine($"今天日期:   {today}");
        Console.WriteLine($"UTC 时间:   {utcNow}");
        Console.WriteLine($"指定时间:   {specific}");

        // C# 8+ / .NET 6+: DateOnly / TimeOnly（对标 Python date / time）
        DateOnly dateOnly = DateOnly.FromDateTime(now);
        TimeOnly timeOnly = TimeOnly.FromDateTime(now);
        Console.WriteLine($"DateOnly:   {dateOnly}");
        Console.WriteLine($"TimeOnly:   {timeOnly}");

        // 【C# vs Python】
        // C#: DateTime 是值类型（struct），默认创建就是当地时区
        // Python: datetime.now() 返回 naive（无时区），需手动加 timezone
        // C#: .NET 6+ 的 DateOnly/TimeOnly 对标 Python 的 date/time


        // ============================================================
        // 2. 格式化 —— ToString / ParseExact
        // ============================================================
        // 【Python 等价】
        //   now.strftime("%Y年%m月%d日 %H:%M:%S")
        //   datetime.strptime("2026-05-15", "%Y-%m-%d")
        //
        // 格式符差异：
        //   C# yyyy  →  Python %Y
        //   C# MM    →  Python %m
        //   C# dd    →  Python %d
        //   C# HH    →  Python %H
        //   C# mm    →  Python %M
        //   C# ss    →  Python %S
        //   C# dddd  →  Python %A
        // ============================================================
        Console.WriteLine("\n===== 2. 格式化 =====");

        // ToString: DateTime → 字符串
        // 【Python 等价】now.strftime("%Y年%m月%d日 %H:%M:%S")
        string formatted = now.ToString("yyyy年MM月dd日 HH:mm:ss");
        Console.WriteLine($"ToString: {formatted}");

        // ParseExact: 字符串 → DateTime
        // 【Python 等价】datetime.strptime("2026-05-15", "%Y-%m-%d")
        DateTime parsed = DateTime.ParseExact("2026-05-15", "yyyy-MM-dd", null);
        Console.WriteLine($"ParseExact: {parsed}");

        // 常用格式
        Console.WriteLine($"  yyyy-MM-dd:  {now:yyyy-MM-dd}");
        Console.WriteLine($"  HH:mm:ss:    {now:HH:mm:ss}");
        Console.WriteLine($"  dddd:         {now:dddd}");         // 星期几
        Console.WriteLine($"  yyyy/MM/dd HH:mm:ss: {now:yyyy/MM/dd HH:mm:ss}");
        Console.WriteLine($"  hh:mm tt:    {now:hh:mm tt}");     // 12小时制

        // 【C# vs Python】
        // C#: now.ToString("format") 直接在对象上调用
        // Python: now.strftime("%format") 需要调用方法
        // C# 的 ToString 更灵活，支持自定义格式提供者（本地化）


        // ============================================================
        // 3. ISO 8601 格式 —— isoformat 对应 ToString("o")
        // ============================================================
        // 【Python 等价】
        //   now.isoformat()   → "2026-05-15T10:30:00"
        //   datetime.fromisoformat(s)
        // ============================================================
        Console.WriteLine("\n===== 3. ISO 8601 格式 =====");

        // ToString("o") 是 round-trip 格式（保留完整精度）
        // 【Python 等价】now.isoformat()
        string isoStr = now.ToString("o");
        Console.WriteLine($"ToString(\"o\"): {isoStr}");

        // 带时区的 ISO 格式
        DateTimeOffset dtoNow = DateTimeOffset.Now;
        string dtoIso = dtoNow.ToString("o");
        Console.WriteLine($"DateTimeOffset: {dtoIso}");

        // 解析 ISO 格式
        // 【Python 等价】datetime.fromisoformat(s)
        DateTime parsedBack = DateTime.Parse(isoStr);
        Console.WriteLine($"Parse: {parsedBack}");

        // 【C# vs Python】
        // C# ToString("o") ≈ Python isoformat()
        // 两者输出的 ISO 格式几乎等价


        // ============================================================
        // 4. 时间运算 —— Add 方法 / TimeSpan
        // ============================================================
        // 【Python 等价】
        //   now + timedelta(days=1)    → now.AddDays(1)
        //   now + timedelta(hours=2)   → now.AddHours(2)
        //   diff = now - other         → TimeSpan
        //   diff.days / diff.total_seconds()
        // ============================================================
        Console.WriteLine("\n===== 4. 时间运算 (TimeSpan) =====");

        // C# 用方法调用（Add 系列），Python 用运算符（+ timedelta）
        DateTime tomorrow = now.AddDays(1);
        DateTime nextWeek = now.AddDays(7);
        DateTime twoHoursLater = now.AddHours(2);

        Console.WriteLine($"明天:     {tomorrow:yyyy-MM-dd HH:mm}");
        Console.WriteLine($"下周:     {nextWeek:yyyy-MM-dd HH:mm}");
        Console.WriteLine($"2小时后:  {twoHoursLater:yyyy-MM-dd HH:mm}");

        // 时间差
        TimeSpan diff = tomorrow - now;
        Console.WriteLine($"\n差值:");
        Console.WriteLine($"  .TotalDays:     {diff.TotalDays} 天");
        Console.WriteLine($"  .TotalSeconds:  {diff.TotalSeconds} 秒");

        // 计算年龄
        DateTime birthday = new DateTime(1990, 5, 20);
        int ageDays = (now - birthday).Days;
        int ageYears = (int)(ageDays / 365.25);
        Console.WriteLine($"\n从 1990-05-20 到今: {ageDays} 天 ≈ {ageYears} 岁");

        // 【C# vs Python】
        // C#: now.AddDays(1) 返回新 DateTime（方法调用）
        // Python: now + timedelta(days=1) 用运算符，更直观
        // C# TimeSpan ≈ Python timedelta


        // ============================================================
        // 5. 日期部分操作 —— AddYears / AddMonths
        // ============================================================
        // 【Python 等价】
        //   now.replace(year=now.year + 1)   → now.AddYears(1)
        //   now.replace(hour=0, minute=0)    → 无直接对应
        // ============================================================
        Console.WriteLine("\n===== 5. 日期部分操作 =====");

        // C# 没有 Python 的 replace() 方法
        // C# 用 Add 系列方法逐个修改
        DateTime sameDayNextYear = now.AddYears(1);
        Console.WriteLine($"明年同日: {sameDayNextYear:yyyy-MM-dd HH:mm}");

        DateTime nextMonth = now.AddMonths(1);
        Console.WriteLine($"下月同日: {nextMonth:yyyy-MM-dd HH:mm}");

        // 设置时间为午夜（C# 没有 replace，需要手动构建）
        DateTime midnight = new DateTime(now.Year, now.Month, now.Day);
        Console.WriteLine($"今天午夜: {midnight}");

        // 【Python 优势】Python replace 可以一次替换多个字段
        // now.replace(hour=0, minute=0, second=0)
        // C# 需要 new DateTime(...) 重新构建


        // ============================================================
        // 6. 时区处理 —— TimeZoneInfo
        // ============================================================
        // 【Python 等价】
        //   beijing_tz = ZoneInfo("Asia/Shanghai")
        //   now_bj = datetime.now(beijing_tz)
        //   now_tokyo = now_bj.astimezone(tokyo_tz)
        // ============================================================
        Console.WriteLine("\n===== 6. 时区处理 =====");

        // 获取时区（C# 用 ID 字符串，Python 用 IANA 名称）
        // 【Python 等价】ZoneInfo("Asia/Shanghai")
        TimeZoneInfo beijingTz = TimeZoneInfo.FindSystemTimeZoneById("China Standard Time");
        TimeZoneInfo tokyoTz = TimeZoneInfo.FindSystemTimeZoneById("Tokyo Standard Time");
        TimeZoneInfo usEastTz = TimeZoneInfo.FindSystemTimeZoneById("Eastern Standard Time");

        // UTC 转北京时间
        // 【Python 等价】datetime.now(beijing_tz)
        DateTime nowBj = TimeZoneInfo.ConvertTimeFromUtc(utcNow, beijingTz);
        DateTime nowTokyo = TimeZoneInfo.ConvertTimeFromUtc(utcNow, tokyoTz);
        DateTime nowUsEast = TimeZoneInfo.ConvertTimeFromUtc(utcNow, usEastTz);

        Console.WriteLine($"北京时间:  {nowBj:HH:mm:ss} {beijingTz.StandardName}");
        Console.WriteLine($"东京时间:  {nowTokyo:HH:mm:ss} {tokyoTz.StandardName}");
        Console.WriteLine($"纽约时间:  {nowUsEast:HH:mm:ss} {usEastTz.StandardName}");
        Console.WriteLine($"UTC 时间:  {utcNow:HH:mm:ss} UTC");

        // 【C# vs Python 时区 ID 差异 —— 最容易踩的坑！】
        // Python (IANA): "Asia/Shanghai"
        // C# (Windows): "China Standard Time"
        // Linux 上 C# 也支持 IANA: TimeZoneInfo.FindSystemTimeZoneById("Asia/Shanghai")


        // ============================================================
        // 7. DateTimeOffset —— 带偏移量的时间（推荐用于时区敏感场景）
        // ============================================================
        // 【Python 等价】
        //   utc_now = datetime.now(timezone.utc)  → DateTimeOffset.Now
        //   now_bj.astimezone(tokyo_tz)           → dto.ToOffset(offset)
        // ============================================================
        Console.WriteLine("\n===== 7. DateTimeOffset =====");

        // DateTimeOffset 包含时间和 UTC 偏移量（类似 Python aware datetime）
        DateTimeOffset dto = DateTimeOffset.Now;
        Console.WriteLine($"DateTimeOffset:    {dto:yyyy-MM-dd HH:mm:ss zzz}");
        Console.WriteLine($"  UTC 偏移量:      {dto.Offset}");

        // 创建指定偏移量的时间
        DateTimeOffset dtoWithOffset = new DateTimeOffset(
            new DateTime(2026, 5, 15, 10, 30, 0),
            TimeSpan.FromHours(8));  // UTC+8
        Console.WriteLine($"指定偏移量:        {dtoWithOffset:yyyy-MM-dd HH:mm:ss zzz}");

        // 转换偏移量
        DateTimeOffset toUtc = dtoWithOffset.ToOffset(TimeSpan.Zero);
        Console.WriteLine($"转为 UTC:          {toUtc:yyyy-MM-dd HH:mm:ss zzz}");

        // 【C# vs Python】
        // C#: DateTimeOffset 天然带偏移量，是 struct（值类型）
        // Python: 需要手动用 timezone(timedelta(hours=8)) 创建 aware datetime
        // C# 的 DateTimeOffset 更安全，不容易混淆 naive/aware


        // ============================================================
        // 8. 固定偏移时区
        // ============================================================
        // 【Python 等价】
        //   utc8 = timezone(timedelta(hours=8))
        //   now_utc8 = datetime.now(utc8)
        // ============================================================
        Console.WriteLine("\n===== 8. 固定偏移时区 =====");

        // C# 用 TimeSpan 表示偏移
        // 【Python 等价】timezone(timedelta(hours=8))
        TimeSpan utc8Offset = TimeSpan.FromHours(8);
        TimeSpan utc5Offset = TimeSpan.FromHours(-5);

        Console.WriteLine($"UTC+8:  {now:HH:mm:ss} +{utc8Offset}");
        Console.WriteLine($"UTC-5:  {now:HH:mm:ss} {utc5Offset}");

        // 【C# vs Python】
        // Python: timezone(timedelta(hours=8)) 创建偏移时区对象
        // C#: TimeSpan.FromHours(8) 只是时间跨度
        //       配合 DateTimeOffset.ToOffset() 使用
        // C# 的方式更底层但更灵活


        // ============================================================
        // 9. Unix 时间戳
        // ============================================================
        // 【Python 等价】
        //   timestamp = now.timestamp()        → ((DateTimeOffset)now).ToUnixTimeSeconds()
        //   back = datetime.fromtimestamp(ts)  → DateTimeOffset.FromUnixTimeSeconds(ts)
        // ============================================================
        Console.WriteLine("\n===== 9. Unix 时间戳 =====");

        // datetime → timestamp
        // 【Python 等价】now.timestamp()
        long timestamp = dto.ToUnixTimeSeconds();
        Console.WriteLine($"当前时间戳(秒):   {timestamp}");

        // 毫秒精度
        long timestampMs = dto.ToUnixTimeMilliseconds();
        Console.WriteLine($"当前时间戳(毫秒): {timestampMs}");

        // timestamp → datetime
        // 【Python 等价】datetime.fromtimestamp(timestamp)
        DateTime back = DateTimeOffset.FromUnixTimeSeconds(timestamp).DateTime;
        Console.WriteLine($"转换回来:         {back}");

        // 【C# vs Python】
        // Python: timestamp() 返回 float（含微秒）
        // C#: ToUnixTimeSeconds() 返回 long（只到秒）
        //       ToUnixTimeMilliseconds() 返回 long（到毫秒）


        // ============================================================
        // 10. 实际场景
        // ============================================================
        Console.WriteLine("\n===== 10. 实际场景 =====");

        // 场景1：日志时间戳解析
        DateTime logTime = DateTime.ParseExact(
            "2026-05-15 10:30:45", "yyyy-MM-dd HH:mm:ss", null);
        TimeSpan logElapsed = DateTime.Now - logTime;
        Console.WriteLine($"日志时间: {logTime}");
        Console.WriteLine($"距今: {logElapsed.Days}天 {logElapsed.Hours}小时 {logElapsed.Minutes}分钟");

        // 场景2：日期范围
        DateTime yearStart = new DateTime(2026, 1, 1);
        DateTime yearEnd = new DateTime(2026, 12, 31);
        int daysInYear = (yearEnd - yearStart).Days + 1;
        Console.WriteLine($"2026年共 {daysInYear} 天");

        // 场景3：比较时间
        DateTime future = new DateTime(2030, 1, 1);
        DateTime past = new DateTime(2020, 1, 1);
        Console.WriteLine($"2030 > 2020? {future > past}");
        Console.WriteLine($"2030 - 2020 = {(future - past).Days} 天");

        // 场景4：下个周一
        int daysUntilMonday = ((int)DayOfWeek.Monday - (int)now.DayOfWeek + 7) % 7;
        DateTime nextMonday = now.AddDays(daysUntilMonday);
        Console.WriteLine($"下个周一: {nextMonday:yyyy-MM-dd dddd}");

        // 场景5：API 时间戳（ISO 格式）
        string apiTime = DateTimeOffset.UtcNow.ToString("o");
        Console.WriteLine($"API 时间戳: {apiTime}");

        // 场景6：DateTime vs DateTimeOffset 对比
        Console.WriteLine($"\nDateTime:       {now}  (无偏移量信息)");
        Console.WriteLine($"DateTimeOffset: {dto:yyyy-MM-dd HH:mm:ss zzz}  (带偏移量)");

        // 【C# 建议】
        // 存储和传输时间：用 DateTimeOffset（带偏移量，不容易混淆）
        // 内部计算时间：用 DateTime（性能更好，值类型）
        // 需要日历功能：用 NodaTime（第三方库，功能最强）


        // ============================================================
        // 总结对比表
        // ============================================================
        Console.WriteLine("\n============================================");
        Console.WriteLine("总结：C# DateTime vs Python datetime");
        Console.WriteLine("============================================");
        Console.WriteLine(@"
┌────────────────────────┬──────────────────────────┬───────────────────────────────┐
│      操作              │    C# DateTime           │    Python datetime            │
├────────────────────────┼──────────────────────────┼───────────────────────────────┤
│ 当前时间               │ DateTime.Now             │ datetime.now()                │
│ 今天日期               │ DateTime.Today           │ date.today()                  │
│ UTC 时间               │ DateTime.UtcNow          │ datetime.now(timezone.utc)    │
│ 指定时间               │ new DateTime(y,m,d,h,m,s)│ datetime(y,m,d,h,m,s)         │
│ 格式化                 │ now.ToString("yyyy-MM-dd")│ p.strftime("%Y-%m-%d")       │
│ 解析字符串             │ DateTime.ParseExact()    │ datetime.strptime()           │
│ ISO 格式               │ now.ToString("o")        │ p.isoformat()                 │
│ 时间加减               │ now.AddDays(1)           │ p + timedelta(days=1)         │
│ 时间差                 │ TimeSpan diff = a - b    │ timedelta diff = a - b        │
│ 替换部分               │ new DateTime(...)重建    │ p.replace(year=2030)          │
│ 时区转换               │ TimeZoneInfo.ConvertTime │ p.astimezone(tz)              │
│ 时区 ID                │ "China Standard Time"    │ "Asia/Shanghai"               │
│ 带偏移量               │ DateTimeOffset           │ timezone(timedelta(h=8))      │
│ Unix 时间戳            │ ToUnixTimeSeconds()      │ p.timestamp()                 │
│ 不可变性               │ struct 值类型（可赋值）   │ 不可变对象                    │
│ Naive/Aware            │ DateTime vs DateTimeOffset│ naive vs aware datetime       │
│ Date 类型              │ DateOnly (.NET 6+)       │ date                          │
│ Time 类型              │ TimeOnly (.NET 6+)       │ time                          │
└────────────────────────┴──────────────────────────┴───────────────────────────────┘

关键差异：
1. Python 用 + timedelta 运算符，C# 用 AddDays/AddHours 方法
2. Python replace() 更灵活，C# 需要 new DateTime() 重建
3. 时区 ID 不同：Python 用 IANA (Asia/Shanghai)，C# Windows 用 (China Standard Time)
4. C# 推荐 DateTimeOffset 处理时区场景，Python 推荐 zoneinfo (3.9+)
5. C# DateTime 是值类型，Python datetime 是不可变对象
");
        Console.WriteLine("完成!");
    }
}
