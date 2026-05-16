using System;
using System.IO;
using System.Text;

/// <summary>
/// C# 文件读写完整示例
/// 对应文章：4.3 文件读写
///
/// Python 对比：
///   C# File.ReadAllText / using StreamReader  ≈  Python open() + with
///   C# System.IO.Path + File                  ≈  Python pathlib.Path
///   C# MemoryStream                           ≈  Python io.StringIO
/// </summary>
class FileIO
{
    static void Main()
    {
        // =============================================================
        // 1. 文件读取方式
        // =============================================================
        // Python 对比：
        //   with open("file.txt", "r") as f:
        //       content = f.read()        # ≈ File.ReadAllText
        //       lines = f.readlines()     # ≈ File.ReadAllLines
        //       for line in f: ...        # ≈ reader.ReadLine() 循环
        // =============================================================
        Console.WriteLine("============================================================");
        Console.WriteLine("1. 文件读取方式");
        Console.WriteLine("============================================================");

        // 准备演示文件
        string testDir = "_temp_fileio_demo_cs";
        Directory.CreateDirectory(testDir);
        string testFile = Path.Combine(testDir, "test.txt");
        File.WriteAllText(testFile, "第一行\n第二行\n第三行\n", Encoding.UTF8);

        // --- File.ReadAllText: 一次读取全部 (Python: f.read()) ---
        string content = File.ReadAllText(testFile, Encoding.UTF8);
        Console.WriteLine($"File.ReadAllText():\n{content}");

        // --- File.ReadAllLines: 读取所有行到数组 (Python: f.readlines()) ---
        string[] lines = File.ReadAllLines(testFile, Encoding.UTF8);
        Console.WriteLine("File.ReadAllLines():");
        foreach (var line in lines)
            Console.WriteLine($"  {line}");

        // --- StreamReader 逐行读取 (Python: for line in f) ---
        Console.WriteLine("StreamReader 逐行读取:");
        using (var reader = new StreamReader(testFile, Encoding.UTF8))
        {
            string? line;
            while ((line = reader.ReadLine()) != null)
                Console.WriteLine($"  {line}");
        }
        // 离开 using 块，reader 自动 Dispose（等同 Python 的 with）

        // --- File.ReadAllBytes: 二进制读取 (Python: open("rb").read()) ---
        byte[] bytes = File.ReadAllBytes(testFile);
        Console.WriteLine($"File.ReadAllBytes(): {bytes.Length} 字节");

        // =============================================================
        // 2. 文件写入方式
        // =============================================================
        // Python 对比：
        //   with open("output.txt", "w") as f:
        //       f.write("text")          # ≈ File.WriteAllText / writer.Write
        //       f.writelines([...])      # ≈ File.WriteAllLines
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("2. 文件写入方式");
        Console.WriteLine("============================================================");

        string outputFile = Path.Combine(testDir, "output.txt");

        // --- File.WriteAllText: 一次性写入 (Python: f.write(text)) ---
        File.WriteAllText(outputFile, "Hello, World!\n", Encoding.UTF8);
        Console.WriteLine("File.WriteAllText() 完成");

        // --- File.WriteAllLines: 写入多行 (Python: f.writelines([...])) ---
        File.WriteAllLines(outputFile, new[] { "line1", "line2", "line3" }, Encoding.UTF8);
        Console.WriteLine("File.WriteAllLines() 完成");

        // --- StreamWriter 写入 (Python: f.write()) ---
        string streamFile = Path.Combine(testDir, "stream_output.txt");
        using (var writer = new StreamWriter(streamFile, false, Encoding.UTF8))
        {
            writer.Write("StreamWriter 写入: ");
            writer.WriteLine("Hello");
            writer.WriteLine("StreamWriter 写入第二行");
        }
        Console.WriteLine("StreamWriter 写入完成");

        // --- 追加写入 (Python: open("file", "a")) ---
        using (var writer = new StreamWriter(outputFile, append: true, Encoding.UTF8))
        {
            writer.WriteLine("追加的内容");
        }
        Console.WriteLine("追加写入完成");

        // =============================================================
        // 3. using 语句 — 资源管理 (Python with 的等价物)
        // =============================================================
        // Python 对比：
        //   with open("file.txt") as f:
        //       content = f.read()
        //   # 离开 with 块自动关闭，不需要 finally
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("3. using 语句 — 资源管理");
        Console.WriteLine("============================================================");

        // 传统 using 语句（等同 Python 的 with 语句）
        Console.WriteLine("传统 using 语句:");
        using (var reader = new StreamReader(testFile))
        using (var writer = new StreamWriter(Path.Combine(testDir, "copy.txt")))
        {
            string? line;
            int lineNum = 1;
            while ((line = reader.ReadLine()) != null)
            {
                Console.WriteLine($"  {lineNum++}: {line}");
                writer.WriteLine(line);
            }
        }

        // C# 8+ using 声明（更简洁）
        Console.WriteLine("C# 8+ using 声明:");
        using var reader2 = new StreamReader(testFile);
        Console.WriteLine($"  第一行: {reader2.ReadLine()}");

        // =============================================================
        // 4. 文件模式和 FileOptions
        // =============================================================
        // Python 对比：
        //   open("file", "r")   → FileMode.Open
        //   open("file", "w")   → FileMode.Create (覆盖)
        //   open("file", "a")   → FileMode.Append
        //   open("file", "x")   → FileMode.CreateNew (不存在才创建)
        //   open("file", "r+")  → FileMode.Open, FileAccess.ReadWrite
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("4. 文件模式和 FileOptions");
        Console.WriteLine("============================================================");

        // FileMode.CreateNew (Python: "x" 模式)
        string newOnlyFile = Path.Combine(testDir, "new_only.txt");
        try
        {
            using var fs = new FileStream(newOnlyFile, FileMode.CreateNew);
            byte[] data = Encoding.UTF8.GetBytes("新文件内容");
            fs.Write(data, 0, data.Length);
            Console.WriteLine($"CreateNew: 创建成功 {newOnlyFile}");

            // 再次创建会报错
            using var fs2 = new FileStream(newOnlyFile, FileMode.CreateNew);
        }
        catch (IOException ex)
        {
            Console.WriteLine($"CreateNew: 文件已存在 — {ex.Message}");
        }

        // FileMode.OpenOrCreate (Python: open("file", "a") 的变体)
        string openOrCreate = Path.Combine(testDir, "open_or_create.txt");
        using (var fs = new FileStream(openOrCreate, FileMode.OpenOrCreate))
        {
            byte[] data = Encoding.UTF8.GetBytes("OpenOrCreate 写入");
            fs.Write(data, 0, data.Length);
        }
        Console.WriteLine("OpenOrCreate 完成");

        // =============================================================
        // 5. 编码 — Encoding 参数
        // =============================================================
        // Python 对比：
        //   open("file", "r", encoding="utf-8")
        //   open("file", "r", encoding="gbk")
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("5. 编码 — Encoding 参数");
        Console.WriteLine("============================================================");

        string encodingFile = Path.Combine(testDir, "encoding.txt");
        string text = "编码测试: Hello 你好";

        // UTF-8 编码
        File.WriteAllText(encodingFile, text, Encoding.UTF8);
        string readBack = File.ReadAllText(encodingFile, Encoding.UTF8);
        Console.WriteLine($"UTF-8 读取: {readBack}");

        // 编码信息
        byte[] utf8Bytes = Encoding.UTF8.GetBytes(text);
        byte[] gbkBytes = Encoding.GetEncoding("gbk").GetBytes(text);
        Console.WriteLine($"UTF-8 字节数: {utf8Bytes.Length}");
        Console.WriteLine($"GBK 字节数: {gbkBytes.Length}");

        // =============================================================
        // 6. Path 类 — 路径操作 (Python pathlib 的等价物)
        // =============================================================
        // Python 对比：
        //   p = pathlib.Path("dir") / "file.txt"
        //   p.name, p.suffix, p.parent, p.stem
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("6. Path 类 — 路径操作");
        Console.WriteLine("============================================================");

        string fullPath = Path.GetFullPath(testFile);
        Console.WriteLine($"完整路径: {fullPath}");
        Console.WriteLine($"  文件名 (Name): {Path.GetFileName(fullPath)}");
        Console.WriteLine($"  无扩展名 (Stem): {Path.GetFileNameWithoutExtension(fullPath)}");
        Console.WriteLine($"  扩展名 (Extension): {Path.GetExtension(fullPath)}");
        Console.WriteLine($"  父目录 (DirectoryName): {Path.GetDirectoryName(fullPath)}");
        Console.WriteLine($"  是否绝对路径: {Path.IsPathRooted(fullPath)}");

        // 路径组合 (Python: p1 / p2)
        string combined = Path.Combine("C:", "Users", "test", "file.txt");
        Console.WriteLine($"  Path.Combine: {combined}");

        // 临时路径
        Console.WriteLine($"  临时目录: {Path.GetTempPath()}");
        Console.WriteLine($"  临时文件: {Path.GetTempFileName()}");

        // =============================================================
        // 7. MemoryStream — 内存中的文件 (Python io.StringIO 的等价物)
        // =============================================================
        // Python 对比：
        //   import io
        //   buffer = io.StringIO()
        //   buffer.write("text")
        //   buffer.seek(0)
        //   content = buffer.read()
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("7. MemoryStream — 内存中的文件");
        Console.WriteLine("============================================================");

        // 写入 MemoryStream
        using var memoryStream = new MemoryStream();
        using (var writer = new StreamWriter(memoryStream, Encoding.UTF8, leaveOpen: true))
        {
            writer.WriteLine("第一行");
            writer.WriteLine("第二行");
            writer.Flush();
        }

        // 读取 MemoryStream
        memoryStream.Seek(0, SeekOrigin.Begin);
        using var reader3 = new StreamReader(memoryStream);
        string memoryContent = reader3.ReadToEnd();
        Console.WriteLine($"MemoryStream 内容:\n{memoryContent}");

        // =============================================================
        // 8. 临时文件和临时目录
        // =============================================================
        // Python 对比：
        //   import tempfile
        //   with tempfile.NamedTemporaryFile() as tmp:
        //       tmp.write(b"data")
        //   with tempfile.TemporaryDirectory() as tmp_dir:
        //       ...
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("8. 临时文件和临时目录");
        Console.WriteLine("============================================================");

        // 临时文件
        string tempFile = Path.GetTempFileName();
        File.WriteAllText(tempFile, "临时文件内容", Encoding.UTF8);
        Console.WriteLine($"临时文件: {tempFile}");
        Console.WriteLine($"  内容: {File.ReadAllText(tempFile)}");

        // 临时目录
        string tempDir = Path.Combine(Path.GetTempPath(), $"demo_{Guid.NewGuid():N}");
        Directory.CreateDirectory(tempDir);
        File.WriteAllText(Path.Combine(tempDir, "temp.txt"), "临时数据", Encoding.UTF8);
        Console.WriteLine($"临时目录: {tempDir}");
        Console.WriteLine($"  文件: {string.Join(", ", Directory.GetFiles(tempDir).Select(Path.GetFileName))}");

        // 清理
        File.Delete(tempFile);
        Directory.Delete(tempDir, true);
        Console.WriteLine("临时文件和目录已清理");

        // =============================================================
        // 9. 文件异步读写 (Python asyncio 的对比)
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("9. 文件异步读写");
        Console.WriteLine("============================================================");
        Console.WriteLine("C# 支持原生异步文件 I/O，Python 也可以用 aiofiles 库");
        Console.WriteLine("C# 优势: File.ReadAllTextAsync / File.WriteAllTextAsync");
        Console.WriteLine("Python: 默认是同步的，需要 aiofiles 或 asyncio.to_thread");

        // 注意：async Main 需要 C# 7.1+
        // string asyncContent = await File.ReadAllTextAsync(testFile);
        // await File.WriteAllTextAsync("async.txt", "Hello");
        Console.WriteLine("  (异步方法示例，需要 async Main 声明)");

        // =============================================================
        // 10. 文件操作速查表
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("10. 文件操作速查表");
        Console.WriteLine("============================================================");

        string copyFile = Path.Combine(testDir, "test_copy.txt");
        string renameFile = Path.Combine(testDir, "test_renamed.txt");

        // 复制
        File.Copy(testFile, copyFile);
        Console.WriteLine($"复制: {testFile} -> {copyFile}");

        // 重命名
        File.Move(copyFile, renameFile);
        Console.WriteLine($"重命名: {copyFile} -> {renameFile}");

        // 检查存在
        bool exists = File.Exists(renameFile);
        Console.WriteLine($"文件是否存在: {exists}");

        // 获取大小
        var fileInfo = new FileInfo(renameFile);
        Console.WriteLine($"文件大小: {fileInfo.Length} 字节");

        // 删除
        File.Delete(renameFile);
        Console.WriteLine($"删除: {renameFile}");

        // 目录操作
        string newDir = Path.Combine(testDir, "new_folder");
        Directory.CreateDirectory(newDir);
        Console.WriteLine($"创建目录: {newDir}");

        string[] files = Directory.GetFiles(testDir);
        Console.WriteLine($"目录内容: {string.Join(", ", files.Select(Path.GetFileName))}");

        // 清理
        Directory.Delete(testDir, true);
        Console.WriteLine($"清理演示目录: {testDir}");

        // =============================================================
        // 11. 文件操作最佳实践总结
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("11. 文件操作最佳实践总结");
        Console.WriteLine("============================================================");
        Console.WriteLine();
        Console.WriteLine("C# vs Python 文件操作对比:");
        Console.WriteLine("  C# File.ReadAllText           ≈  Python open().read()");
        Console.WriteLine("  C# using StreamReader          ≈  Python with open() as f");
        Console.WriteLine("  C# Path                       ≈  Python pathlib.Path");
        Console.WriteLine("  C# MemoryStream               ≈  Python io.StringIO");
        Console.WriteLine("  C# Path.GetTempFileName       ≈  Python tempfile.NamedTemporaryFile");
        Console.WriteLine("  C# File.Copy/Move/Delete      ≈  Python shutil.copy/move + os.remove");
        Console.WriteLine("  C# Directory.GetFiles         ≈  Python os.listdir / pathlib.iterdir");
        Console.WriteLine();
        Console.WriteLine("最佳实践:");
        Console.WriteLine("  1. 始终使用 using/with 确保资源释放");
        Console.WriteLine("  2. 指定 Encoding 参数，避免平台编码差异");
        Console.WriteLine("  3. 小文件用 ReadAllText/WriteAllText，大文件用 StreamReader");
        Console.WriteLine("  4. 路径操作优先使用 Path (C#) / pathlib (Python)");
        Console.WriteLine("  5. 临时文件使用 Path.GetTempFileName / tempfile 模块");

        Console.WriteLine();
        Console.WriteLine("所有文件读写示例运行完毕！");
    }
}
