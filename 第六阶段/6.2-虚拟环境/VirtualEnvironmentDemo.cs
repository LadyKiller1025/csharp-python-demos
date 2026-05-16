/*
=================================================================
6.2 虚拟环境 —— C#/.NET 项目隔离机制
对应文章：6.2 虚拟环境
=================================================================

C# 的项目隔离 vs Python 的虚拟环境：
  C# 天然项目隔离 —— 每个 .csproj 独立引用 NuGet 包，
  即使不同项目引用同一包的不同版本也不会冲突。

  Python 需要虚拟环境来实现类似效果。

本文件展示 C# 侧的对应概念和实际代码。
*/

using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.InteropServices;

public class VirtualEnvironmentDemo
{
    static void Main()
    {
        Console.WriteLine("===========================================================");
        Console.WriteLine("  C#/.NET 项目隔离机制 —— 对标 Python 虚拟环境");
        Console.WriteLine("===========================================================\n");

        // =====================================================================
        // 第一部分：.NET 天然的项目隔离
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第一部分：.NET 天然的项目隔离");
        Console.WriteLine("===========================================================\n");

        Console.WriteLine("C#/.NET 的项目隔离是\"开箱即用\"的：");
        Console.WriteLine();
        Console.WriteLine("  每个 .csproj 文件独立声明依赖 → 自然隔离");
        Console.WriteLine("  NuGet 全局缓存 → 多个项目共享下载，但版本独立");
        Console.WriteLine();
        Console.WriteLine("  这相当于 Python 的：");
        Console.WriteLine("  - requirements.txt（依赖声明）");
        Console.WriteLine("  - 虚拟环境（隔离安装）");
        Console.WriteLine("  - 但 C# 不需要手动创建\"虚拟环境\"，因为 .csproj 天然隔离");
        Console.WriteLine();

        // 演示 .csproj 项目结构
        Console.WriteLine("--- .csproj 依赖声明（类似 Python pyproject.toml）---");
        Console.WriteLine("""
            <!-- MyApp.csproj -->
            <Project Sdk="Microsoft.NET.Sdk">
              <PropertyGroup>
                <TargetFramework>net8.0</TargetFramework>
              </PropertyGroup>
              <ItemGroup>
                <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
                <PackageReference Include="Serilog" Version="3.1.1" />
              </ItemGroup>
              <ItemGroup Condition="'$(Configuration)'=='Debug'">
                <PackageReference Include="xUnit" Version="2.6.0" />
              </ItemGroup>
            </Project>
            """);
        Console.WriteLine("对比 Python pyproject.toml:");
        Console.WriteLine("  [project]");
        Console.WriteLine("  dependencies = [\"requests>=2.28\", \"flask>=3.0\"]");
        Console.WriteLine("  [project.optional-dependencies]");
        Console.WriteLine("  dev = [\"pytest>=7.0\"]\n");


        // =====================================================================
        // 第二部分：global.json —— Python .python-version 的 C# 对应
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第二部分：global.json —— SDK 版本锁定");
        Console.WriteLine("===========================================================\n");

        Console.WriteLine("┌──────────────────────────────────────────────────────────┐");
        Console.WriteLine("│  概念对照                                                 │");
        Console.WriteLine("│                                                           │");
        Console.WriteLine("│  C# global.json          Python .python-version          │");
        Console.WriteLine("│  ──────────────          ────────────────────            │");
        Console.WriteLine("│  锁定 .NET SDK 版本      锁定 Python 解释器版本          │");
        Console.WriteLine("│  {                       3.12.0                           │");
        Console.WriteLine("│    \"sdk\": {                                                │");
        Console.WriteLine("│      \"version\": \"8.0\"                                     │");
        Console.WriteLine("│    }                                                      │");
        Console.WriteLine("│  }                                                        │");
        Console.WriteLine("└──────────────────────────────────────────────────────────┘");
        Console.WriteLine();

        Console.WriteLine("--- global.json 示例 ---");
        Console.WriteLine("""
            {
              "sdk": {
                "version": "8.0.100",
                "rollForward": "latestFeature",
                "allowPrerelease": false
              }
            }
            """);

        Console.WriteLine("Python .python-version:");
        Console.WriteLine("  3.12.0");
        Console.WriteLine();

        // 读取当前 .NET SDK 版本
        Console.WriteLine("--- 当前 .NET SDK 信息 ---");
        Console.WriteLine($"  运行时框架: {RuntimeInformation.FrameworkDescription}");
        Console.WriteLine($"  操作系统:   {RuntimeInformation.OSDescription}");
        Console.WriteLine($"  处理器架构: {RuntimeInformation.ProcessArchitecture}");
        Console.WriteLine();


        // =====================================================================
        // 第三部分：.NET 工具隔离 —— 全局 vs 本地
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第三部分：.NET 工具管理 —— 全局 vs 本地");
        Console.WriteLine("===========================================================\n");

        Console.WriteLine("┌──────────────────────────────────────────────────────────┐");
        Console.WriteLine("│  .NET 工具 vs Python 工具                                │");
        Console.WriteLine("│                                                           │");
        Console.WriteLine("│  C#                          Python                      │");
        Console.WriteLine("│  ────                        ──────                      │");
        Console.WriteLine("│  dotnet tool install --global pip install --user <pkg>   │");
        Console.WriteLine("│  (全局，所有项目可用)      (用户级，所有项目可用)         │");
        Console.WriteLine("│                                                           │");
        Console.WriteLine("│  dotnet tool install --local pip install <pkg>           │");
        Console.WriteLine("│  (项目级，仅当前项目)      (虚拟环境中，仅当前项目)      │");
        Console.WriteLine("│                                                           │");
        Console.WriteLine("│  .config/dotnet-tools.json  pyproject.toml [tool]        │");
        Console.WriteLine("│  (工具版本锁定)             (工具版本锁定)                │");
        Console.WriteLine("└──────────────────────────────────────────────────────────┘");
        Console.WriteLine();

        var toolComparisons = new List<(string DotnetCmd, string PythonCmd, string Description)>
        {
            ("dotnet tool install --global dotnet-ef",    "pip install --user black",       "全局安装工具"),
            ("dotnet tool install --local dotnet-format",  "pip install pytest",             "项目级安装"),
            ("dotnet tool restore",                        "pip install -r requirements.txt","从配置文件恢复"),
            ("dotnet tool list --global",                  "pip list --user",                "列出已安装工具"),
            ("dotnet tool list --local",                   "pip list",                       "列出当前环境工具"),
        };

        Console.WriteLine("--- 工具管理命令对照 ---");
        Console.WriteLine($"  {"C# dotnet tool":45s} {"Python pip":35s} {"说明"}");
        Console.WriteLine("  " + new string('-', 100));
        foreach (var (dotnetCmd, pythonCmd, desc) in toolComparisons)
        {
            Console.WriteLine($"  {dotnetCmd:45s} {pythonCmd:35s} {desc}");
        }
        Console.WriteLine();


        // =====================================================================
        // 第四部分：NuGet 包缓存机制
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第四部分：NuGet 包缓存 vs Python pip 缓存");
        Console.WriteLine("===========================================================\n");

        Console.WriteLine("NuGet 包缓存路径：");
        string nugetCache = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
        Console.WriteLine($"  Windows: %USERPROFILE%\\.nuget\\packages");
        Console.WriteLine($"  macOS/Linux: ~/.nuget/packages");
        Console.WriteLine();

        Console.WriteLine("缓存策略对比：");
        var cacheComparisons = new (string Aspect, string DotNet, string Python)[]
        {
            ("缓存位置",     "~/.nuget/packages",           "~/.cache/pip"),
            ("缓存粒度",     按包名+版本，硬链接到项目",     "按包名+版本，解压到项目"),
            ("磁盘占用",     共享缓存，节省空间",             "各虚拟环境独立，可能重复"),
            ("离线安装",     "支持（缓存中有即可）",          "支持（pip install --no-index）"),
            ("清理缓存",     "dotnet nuget locals --clear",  "pip cache purge"),
        };

        foreach (var (aspect, dotnet, python) in cacheComparisons)
        {
            Console.WriteLine($"  {aspect:12s}:");
            Console.WriteLine($"    C#:     {dotnet}");
            Console.WriteLine($"    Python: {python}");
            Console.WriteLine();
        }


        // =====================================================================
        // 第五部分：Docker 中的项目隔离
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第五部分：Docker 中的项目隔离");
        Console.WriteLine("===========================================================\n");

        Console.WriteLine("Docker 是终极隔离方案 —— 完整的操作系统级隔离");
        Console.WriteLine();

        Console.WriteLine("C# Dockerfile 示例：");
        Console.WriteLine("""
            # 多阶段构建
            FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
            WORKDIR /src
            COPY *.csproj .
            RUN dotnet restore                    # 类似 pip install -r requirements.txt
            COPY . .
            RUN dotnet publish -c Release -o /app

            FROM mcr.microsoft.com/dotnet/aspnet:8.0
            WORKDIR /app
            COPY --from=build /app .
            ENTRYPOINT ["dotnet", "MyApp.dll"]
            """);
        Console.WriteLine();

        Console.WriteLine("Python Dockerfile 示例：");
        Console.WriteLine("""
            FROM python:3.12-slim
            WORKDIR /app
            COPY requirements.txt .
            RUN python -m venv /opt/venv && \\
                /opt/venv/bin/pip install -r requirements.txt
            ENV PATH="/opt/venv/bin:$PATH"
            COPY . .
            CMD ["python", "main.py"]
            """);
        Console.WriteLine();

        Console.WriteLine("隔离方案选择指南：");
        var isolationMethods = new (string Method, string Scope, string Speed, string UseCase)[]
        {
            (".csproj + NuGet",    "项目级",     "快",     "C# 默认方式"),
            ("venv + pip",         "项目级",     "快",     "Python 默认方式"),
            ("Docker",             "容器级",     "较慢",   "生产部署 / 复杂依赖"),
            ("WSL2 / VM",          "系统级",     "慢",     "跨平台开发测试"),
        };

        Console.WriteLine($"  {"方案":20s} {"隔离粒度":10s} {"创建速度":8s} {"适用场景"}");
        Console.WriteLine("  " + new string('-', 60));
        foreach (var (method, scope, speed, useCase) in isolationMethods)
        {
            Console.WriteLine($"  {method:20s} {scope:10s} {speed:8s} {useCase}");
        }
        Console.WriteLine();


        // =====================================================================
        // 第六部分：实际代码 —— 模拟项目依赖解析
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  第六部分：模拟 NuGet 依赖解析过程");
        Console.WriteLine("===========================================================\n");

        // 模拟 NuGet 依赖解析
        var projectDependencies = new Dictionary<string, List<(string Package, string Version)>>
        {
            ["MyWebApp"] = new()
            {
                ("Newtonsoft.Json", "13.0.3"),
                ("Serilog", "3.1.1"),
                ("Microsoft.AspNetCore", "8.0.0"),
            },
            ["MyLibrary"] = new()
            {
                ("Newtonsoft.Json", "13.0.3"),  // 同版本，复用
            },
            ["MyTests"] = new()
            {
                ("xUnit", "2.6.0"),
                ("Moq", "4.20.0"),
            },
        };

        Console.WriteLine("模拟 NuGet 依赖解析：");
        var resolvedPackages = new Dictionary<string, string>();

        foreach (var (project, deps) in projectDependencies)
        {
            Console.WriteLine($"\n  [{project}]");
            foreach (var (package, version) in deps)
            {
                string status;
                if (resolvedPackages.TryGetValue(package, out string? existingVersion))
                {
                    if (existingVersion == version)
                    {
                        status = $"(复用全局缓存: {existingVersion})";
                    }
                    else
                    {
                        status = $"(⚠ 版本冲突! 期望 {version}, 已有 {existingVersion})";
                    }
                }
                else
                {
                    resolvedPackages[package] = version;
                    status = "(新安装到全局缓存)";
                }
                Console.WriteLine($"    {package} {version} {status}");
            }
        }

        Console.WriteLine($"\n  全局缓存中的包: {resolvedPackages.Count} 个");
        foreach (var (pkg, ver) in resolvedPackages)
        {
            Console.WriteLine($"    - {pkg} {ver}");
        }

        Console.WriteLine("\n  → C# 的 NuGet 天然处理了版本解析和冲突");
        Console.WriteLine("  → Python 需要 pip/Poetry/uv 来做类似的事情");
        Console.WriteLine();


        // =====================================================================
        // 总结
        // =====================================================================
        Console.WriteLine("===========================================================");
        Console.WriteLine("  总结：Python 虚拟环境 vs .NET 项目隔离");
        Console.WriteLine("===========================================================");
        Console.WriteLine();
        Console.WriteLine("  本质区别：");
        Console.WriteLine("    C#:    .csproj 文件天然隔离 → 不需要\"虚拟环境\"概念");
        Console.WriteLine("    Python: 全局 site-packages 共享 → 必须虚拟环境隔离");
        Console.WriteLine();
        Console.WriteLine("  等价概念：");
        Console.WriteLine("    Python venv        ≈  C# .csproj（项目级依赖隔离）");
        Console.WriteLine("    Python .python-version  ≈  C# global.json（版本锁定）");
        Console.WriteLine("    Python pyproject.toml    ≈  C# .csproj + Directory.Build.props");
        Console.WriteLine("    Python poetry.lock       ≈  C# packages.lock.json");
        Console.WriteLine("    Python venv + Docker     ≈  C# Docker + NuGet");
        Console.WriteLine();
        Console.WriteLine("  对 C# 开发者的建议：");
        Console.WriteLine("    1. 用 venv 是 Python 的\"正确姿势\"，不是可选的");
        Console.WriteLine("    2. uv 是目前最接近 dotnet CLI 体验的工具");
        Console.WriteLine("    3. 生产环境用 Docker，和 C# 一样");
        Console.WriteLine("    4. .python-version 文件要提交到版本控制");
    }
}
