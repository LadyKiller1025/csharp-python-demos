// ============================================================
// C# 文件路径处理完全指南（对标 Python pathlib）
// 对应文章：4.6 pathlib —— 面向对象的文件路径处理
// Python 对比：pathlib.Path 对象
// ============================================================
//
// 【核心对比】
//   Python pathlib   →  用 Path 对象表示路径，支持 / 运算符拼接
//   C# System.IO     →  Path（静态工具类）+ Directory + FileInfo 组合使用
//
// C# 的 Path 类全是静态方法，不创建对象
// Python 的 Path 是实例对象，方法直接挂在对象上
// ============================================================

using System;
using System.IO;
using System.Linq;

public class PathlibDemo
{
    static void Main()
    {
        Console.WriteLine("============================================");
        Console.WriteLine("C# 文件路径处理 vs Python pathlib");
        Console.WriteLine("============================================");

        // ============================================================
        // 1. 创建路径 —— C# 直接用字符串，不创建 Path 对象
        // ============================================================
        // 【Python 等价】
        //   home = Path.home()
        //   current = Path.cwd()
        //   project = Path("e:/Code/csharp-python-learning-series")
        // ============================================================
        Console.WriteLine("\n===== 1. 特殊路径 =====");

        string home = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
        string cwd = Directory.GetCurrentDirectory();
        string project = @"e:\Code\csharp-python-learning-series";

        Console.WriteLine($"用户主目录: {home}");
        Console.WriteLine($"当前工作目录: {cwd}");
        Console.WriteLine($"项目路径: {project}");

        // 【C# vs Python】
        // C#:  没有 Path 对象，Path 只是静态工具类
        // Python: Path("...") 创建对象，然后调用对象方法


        // ============================================================
        // 2. Path.Combine 拼接路径 —— 没有 / 运算符
        // ============================================================
        // 【Python 等价】
        //   readme = project / "README.md"
        //   stage1 = project / "第一阶段" / "1.1-Hello-World"
        // ============================================================
        Console.WriteLine("\n===== 2. 路径拼接 =====");

        // C# 用 Path.Combine 静态方法
        string readme = Path.Combine(project, "README.md");
        string stage1 = Path.Combine(project, "第一阶段", "1.1-Hello-World与程序结构");

        Console.WriteLine($"README:  {readme}");
        Console.WriteLine($"阶段一:  {stage1}");

        // C# 不支持 path / "sub" 运算符重载
        // Python 的 / 运算符更直观优雅
        // 但 C# 的 Combine 可以一次拼接多个部分，也不差


        // ============================================================
        // 3. 路径组件分解 —— 用 Path 静态方法
        // ============================================================
        // 【Python 等价】
        //   p.name     → Path.GetFileName(p)
        //   p.stem     → Path.GetFileNameWithoutExtension(p)
        //   p.suffix   → Path.GetExtension(p)
        //   p.parent   → Path.GetDirectoryName(p)
        // ============================================================
        Console.WriteLine("\n===== 3. 路径组件分解 =====");

        string p = Path.Combine("/", "home", "user", "docs", "report.txt");
        Console.WriteLine($"完整路径:   {p}");
        Console.WriteLine($"name:       {Path.GetFileName(p)}");              // report.txt
        Console.WriteLine($"stem:       {Path.GetFileNameWithoutExtension(p)}"); // report
        Console.WriteLine($"suffix:     {Path.GetExtension(p)}");             // .txt
        Console.WriteLine($"parent:     {Path.GetDirectoryName(p)}");         // /home/user/docs

        // 多后缀
        string p2 = "archive.tar.gz";
        Console.WriteLine($"\narchive.tar.gz:");
        Console.WriteLine($"  GetExtension = {Path.GetExtension(p2)}");       // .gz（只有最后一个）
        Console.WriteLine($"  文件名 = {Path.GetFileName(p2)}");             // archive.tar.gz

        // 【Python 优势】Python 有 suffixes 属性返回所有后缀列表
        // C# 只能获取最后一个后缀，需要自己循环处理


        // ============================================================
        // 4. 路径判断
        // ============================================================
        // 【Python 等价】
        //   readme.exists()      → File.Exists(readme)
        //   readme.is_file()     → File.Exists(readme)
        //   project.is_dir()     → Directory.Exists(project)
        //   project.is_absolute()→ Path.IsPathRooted(project)
        // ============================================================
        Console.WriteLine("\n===== 4. 路径判断 =====");

        Console.WriteLine($"README 存在:     {File.Exists(readme)}");
        Console.WriteLine($"README 是文件:   {File.Exists(readme)}");
        Console.WriteLine($"项目 是目录:     {Directory.Exists(project)}");
        Console.WriteLine($"项目 是绝对路径: {Path.IsPathRooted(project)}");

        // 【C# vs Python】
        // C#: File.Exists 只判断文件，Directory.Exists 只判断目录
        // Python: exists() 通吃，is_file/is_dir 再细分


        // ============================================================
        // 5. Path.GetFullPath —— 解析绝对路径（对标 Python resolve()）
        // ============================================================
        // 【Python 等价】
        //   resolved = relative.resolve()
        // ============================================================
        Console.WriteLine("\n===== 5. GetFullPath 解析绝对路径 =====");

        string relativePath = "README.md";
        string resolvedPath = Path.GetFullPath(relativePath);
        Console.WriteLine($"相对路径:  {relativePath}");
        Console.WriteLine($"解析后:    {resolvedPath}");
        Console.WriteLine($"是否绝对:  {Path.IsPathRooted(resolvedPath)}");


        // ============================================================
        // 6. 读写文件 —— File.ReadAllText / File.WriteAllText
        // ============================================================
        // 【Python 等价】
        //   content = p.read_text(encoding="utf-8")
        //   p.write_text("text", encoding="utf-8")
        // ============================================================
        Console.WriteLine("\n===== 6. 读写文件 =====");

        string tempFile = Path.Combine(cwd, "temp_demo.txt");

        // 写入
        File.WriteAllText(tempFile, "Hello C# Path!\n第二行内容\n");
        Console.WriteLine($"写入文件: {tempFile}");

        // 读取
        string content = File.ReadAllText(tempFile);
        Console.WriteLine($"读取内容: {content.Trim()}");

        // 读取 README 前 80 字符
        if (File.Exists(readme))
        {
            string readmeContent = File.ReadAllText(readme);
            Console.WriteLine($"README 前 80 字: {readmeContent.Substring(0, Math.Min(80, readmeContent.Length))}...");
        }

        // 清理
        File.Delete(tempFile);
        Console.WriteLine("删除临时文件: 完成");

        // 【C# vs Python】
        // C#:  File.ReadAllText / WriteAllText 是静态方法
        // Python: p.read_text() 是实例方法，更符合 OOP


        // ============================================================
        // 7. 创建/删除目录
        // ============================================================
        // 【Python 等价】
        //   demo_dir.mkdir(parents=True, exist_ok=True)
        //   shutil.rmtree(demo_dir.parent)
        // ============================================================
        Console.WriteLine("\n===== 7. 创建/删除目录 =====");

        string demoDir = Path.Combine(cwd, "temp_dir_demo", "sub_dir");

        // 创建目录（等价于 Python mkdir(parents=True, exist_ok=True)）
        Directory.CreateDirectory(demoDir);
        Console.WriteLine($"创建目录: {demoDir}");
        Console.WriteLine($"目录存在: {Directory.Exists(demoDir)}");

        // 写入文件到临时目录
        string subFile = Path.Combine(demoDir, "test.txt");
        File.WriteAllText(subFile, "测试文件");

        // 遍历目录内容
        Console.WriteLine("目录内容:");
        foreach (string item in Directory.GetFileSystemEntries(demoDir))
        {
            string itemName = Path.GetFileName(item);
            string prefix = Directory.Exists(item) ? "[DIR] " : "      ";
            Console.WriteLine($"  {prefix}{itemName}");
        }

        // 删除整个目录树
        Directory.Delete(Path.Combine(cwd, "temp_dir_demo"), true);
        Console.WriteLine("删除目录树: 完成");

        // 【C# vs Python】
        // C#:  Directory.CreateDirectory 不存在就创建，存在也不报错（类似 exist_ok=True）
        // C#:  Directory.Delete(path, recursive: true) 类似 shutil.rmtree()


        // ============================================================
        // 8. 文件搜索 —— Directory.GetFiles + SearchOption
        // ============================================================
        // 【Python 等价】
        //   py_files = list(project.glob("*.md"))
        //   all_py = list(project.rglob("*.py"))
        // ============================================================
        Console.WriteLine("\n===== 8. 文件搜索 =====");

        // 当前目录匹配（等价于 glob("*.md")）
        string[] mdFiles = Directory.GetFiles(project, "*.md");
        Console.WriteLine($"项目根目录的 .md 文件 ({mdFiles.Length} 个):");
        foreach (string f in mdFiles.Take(5))
        {
            Console.WriteLine($"  {Path.GetFileName(f)}");
        }

        // 递归搜索（等价于 rglob("*.py")）
        string[] allPy = Directory.GetFiles(project, "*.py", SearchOption.AllDirectories);
        Console.WriteLine($"\n递归搜索所有 .py 文件 ({allPy.Length} 个):");
        foreach (string f in allPy.Take(5))
        {
            string relPath = Path.GetRelativePath(project, f);
            Console.WriteLine($"  {relPath}");
        }

        // 【C# vs Python】
        // C#:  需要传 SearchOption.AllDirectories 实现递归
        // Python: rglob("*.py") 更简洁，glob("*.py") 只当前目录


        // ============================================================
        // 9. FileInfo —— 获取文件元信息（对标 Python stat()）
        // ============================================================
        // 【Python 等价】
        //   st = readme.stat()
        //   st.st_size     → fileInfo.Length
        //   st.st_mtime    → fileInfo.LastWriteTime
        //   st.st_ctime    → fileInfo.CreationTime
        // ============================================================
        Console.WriteLine("\n===== 9. FileInfo 文件元信息 =====");

        if (File.Exists(readme))
        {
            FileInfo fi = new FileInfo(readme);
            Console.WriteLine($"文件: {fi.Name}");
            Console.WriteLine($"  大小: {fi.Length:N0} bytes ({fi.Length / 1024.0:F1} KB)");
            Console.WriteLine($"  修改时间: {fi.LastWriteTime}");
            Console.WriteLine($"  创建时间: {fi.CreationTime}");
            Console.WriteLine($"  最后访问: {fi.LastAccessTime}");
        }

        // 【C# vs Python】
        // C#:  FileInfo 是一个有状态的对象，可以多次访问属性
        // Python: stat() 返回一次性命名元组，轻量但不可变


        // ============================================================
        // 10. Path.ChangeExtension —— 修改后缀
        // ============================================================
        // 【Python 等价】
        //   txt_version = original.with_suffix(".txt")
        //   new_name = original.with_name("summary.pdf")
        // ============================================================
        Console.WriteLine("\n===== 10. 修改路径组件 =====");

        string original = "report.final.docx";
        Console.WriteLine($"原始路径:   {original}");

        // 修改后缀（等价于 with_suffix）
        string txtVersion = Path.ChangeExtension(original, ".txt");
        Console.WriteLine($"改后缀 .txt: {Path.GetFileName(txtVersion)}");  // report.final.txt

        // 修改文件名（C# 没有 with_name，需要手动拼接）
        string dirPart = Path.GetDirectoryName(original) ?? "";
        string newName = Path.Combine(dirPart, "summary.pdf");
        Console.WriteLine($"改文件名:    {Path.GetFileName(newName)}");

        // 【Python 优势】
        // Python: p.with_suffix(".txt"), p.with_name("x.pdf"), p.with_stem("x")
        // C#: 只有 ChangeExtension，修改文件名需要手动拼接


        // ============================================================
        // 11. Path.GetRelativePath —— 路径相对化
        // ============================================================
        // 【Python 等价】
        //   rel = full.relative_to(project)
        // ============================================================
        Console.WriteLine("\n===== 11. GetRelativePath =====");

        string fullPath = Path.Combine(project, "第二阶段", "2.1-函数定义", "README.md");
        string relPath = Path.GetRelativePath(project, fullPath);
        Console.WriteLine($"完整路径: {fullPath}");
        Console.WriteLine($"相对路径: {relPath}");


        // ============================================================
        // 12. Path 拆分 parts —— C# 手动实现
        // ============================================================
        // 【Python 等价】
        //   p.parts → ('/', 'home', 'user', 'docs', 'report.txt')
        // ============================================================
        Console.WriteLine("\n===== 12. 路径 parts 拆分 =====");

        string pathStr = Path.Combine("/", "home", "user", "docs", "report.txt");
        string[] parts = pathStr.Split(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
        Console.WriteLine($"parts: [{string.Join(", ", parts)}]");

        // 【C# vs Python】
        // Python: p.parts 是属性，直接返回元组
        // C#: 没有内置 parts，需要手动 Split


        // ============================================================
        // 总结对比表
        // ============================================================
        Console.WriteLine("\n============================================");
        Console.WriteLine("总结：C# System.IO vs Python pathlib");
        Console.WriteLine("============================================");
        Console.WriteLine(@"
┌──────────────────────┬──────────────────────────┬───────────────────────────────┐
│      操作            │    C# System.IO          │    Python pathlib             │
├──────────────────────┼──────────────────────────┼───────────────────────────────┤
│ 创建路径             │ 直接传字符串              │ Path("a/b/c") 创建对象        │
│ 路径拼接             │ Path.Combine(p, "sub")   │ p / "sub" / "file"           │
│ 判断存在             │ File/Directory.Exists()  │ p.exists()                   │
│ 创建目录             │ Directory.CreateDirectory│ p.mkdir(parents=True)        │
│ 删除目录树           │ Directory.Delete(p, true)│ shutil.rmtree(p)             │
│ 读取文本             │ File.ReadAllText(p)      │ p.read_text()                │
│ 写入文本             │ File.WriteAllText(p,txt) │ p.write_text(txt)            │
│ 文件搜索             │ Directory.GetFiles(p,**) │ p.glob("*.py") / p.rglob()   │
│ 文件信息             │ new FileInfo(p)          │ p.stat()                     │
│ 修改后缀             │ Path.ChangeExtension()   │ p.with_suffix(".txt")        │
│ 解析绝对路径         │ Path.GetFullPath(p)      │ p.resolve()                  │
│ 路径各部分           │ GetFileName/Extension()  │ p.name/stem/suffix/parent    │
│ parts 拆分           │ 需手动 Split             │ p.parts 属性直接获取          │
└──────────────────────┴──────────────────────────┴───────────────────────────────┘
");
        Console.WriteLine("完成!");
    }
}
