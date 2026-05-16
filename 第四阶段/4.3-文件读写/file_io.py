"""
Python 文件读写完整示例
对应文章：4.3 文件读写

C# 对比：
  Python open() + with     ≈  C# File.ReadAllText / using + StreamReader
  Python pathlib.Path      ≈  C# System.IO.Path + File
  Python io.StringIO       ≈  C# MemoryStream + StreamWriter
"""
import os
import io
import tempfile
import pathlib

# =============================================================
# 1. 文件打开模式 (open modes)
# =============================================================
# C# 对比：
#   "r"  ≈ File.OpenRead() / new StreamReader(path)
#   "w"  ≈ File.Create()   / new StreamWriter(path)
#   "a"  ≈ new StreamWriter(path, append: true)
#   "r+" ≈ new FileStream(path, FileMode.Open, FileAccess.ReadWrite)
#   "x"  ≈ new FileStream(path, FileMode.CreateNew)
#   "rb" ≈ File.ReadAllBytes(path)
#   "wb" ≈ File.WriteAllBytes(path, ...)
# =============================================================
print("=" * 60)
print("1. 文件打开模式 (open modes)")
print("=" * 60)

# 准备演示文件
test_dir = "_temp_fileio_demo"
os.makedirs(test_dir, exist_ok=True)
test_file = os.path.join(test_dir, "test.txt")

# --- "w" 模式：写入（覆盖） ---
# C# 等价：File.WriteAllText(path, content)
with open(test_file, "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")
    f.write("第三行\n")
print(f"['w' 模式] 写入完成: {test_file}")

# --- "r" 模式：只读 ---
# C# 等价：File.ReadAllText(path)
with open(test_file, "r", encoding="utf-8") as f:
    content = f.read()
    print(f"['r' 模式] 文件内容:\n{content}")

# --- "a" 模式：追加 ---
# C# 等价：new StreamWriter(path, append: true)
with open(test_file, "a", encoding="utf-8") as f:
    f.write("第四行(追加)\n")
print(f"['a' 模式] 追加完成")

with open(test_file, "r", encoding="utf-8") as f:
    print(f"['a' 模式] 追加后内容: {f.read()}")

# --- "x" 模式：排他创建（文件已存在则报错） ---
# C# 等价：new FileStream(path, FileMode.CreateNew)
new_file = os.path.join(test_dir, "new_only.txt")
try:
    with open(new_file, "x", encoding="utf-8") as f:
        f.write("新文件内容\n")
    print(f"['x' 模式] 创建成功: {new_file}")
    # 再次创建同一文件会报错
    with open(new_file, "x", encoding="utf-8") as f:
        f.write("这行不会执行")
except FileExistsError:
    print(f"['x' 模式] 文件已存在，创建失败 (FileExistsError)")

# --- "rb"/"wb" 二进制模式 ---
# C# 等价：File.ReadAllBytes / File.WriteAllBytes
binary_file = os.path.join(test_dir, "binary.bin")
data = bytes(range(256))  # 0x00 ~ 0xFF
with open(binary_file, "wb") as f:
    f.write(data)
print(f"['wb' 模式] 写入 {len(data)} 字节二进制数据")

with open(binary_file, "rb") as f:
    read_data = f.read()
print(f"['rb' 模式] 读取 {len(read_data)} 字节，内容匹配: {read_data == data}")

print()
print("=" * 60)
print("2. with 语句 — 自动资源管理")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   using (var reader = new StreamReader(path))
#   {
#       string line;
#       while ((line = reader.ReadLine()) != null)
#           Console.WriteLine(line);
#   }
#
# Python with ≈ C# using，都会在块结束时自动调用 close/Dispose
# -------------------------------------------------------
print("with 语句确保文件正确关闭，即使发生异常:")

with open(test_file, "r", encoding="utf-8") as f:
    for line in f:
        # f 本身是一个迭代器，逐行读取（内存友好）
        # C# 等价：reader.ReadLine() 逐行读取
        print(f"  {line.strip()}")

print()
print("=" * 60)
print("3. read / readlines / readline 方法")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   File.ReadAllText(path)       ≈  f.read()
#   File.ReadAllLines(path)      ≈  f.readlines()
#   reader.ReadLine()            ≈  f.readline()
# -------------------------------------------------------

# --- read() 读取全部内容 ---
with open(test_file, "r", encoding="utf-8") as f:
    full_content = f.read()  # 一次读入全部，适合小文件
print(f"read(): {full_content.strip()}")

# --- read(n) 读取指定字节数 ---
with open(test_file, "r", encoding="utf-8") as f:
    chunk = f.read(5)  # 读取前 5 个字符
print(f"read(5): '{chunk}'")

# --- readline() 逐行读取 ---
with open(test_file, "r", encoding="utf-8") as f:
    line1 = f.readline().strip()
    line2 = f.readline().strip()
print(f"readline(): '{line1}', '{line2}'")

# --- readlines() 读取所有行到列表 ---
with open(test_file, "r", encoding="utf-8") as f:
    lines = f.readlines()  # 返回 list[str]
print(f"readlines(): {lines}")

print()
print("=" * 60)
print("4. write / writelines 方法")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   File.WriteAllText(path, text)   ≈  f.write(text)
#   File.WriteAllLines(path, lines) ≈  f.writelines(lines)
# -------------------------------------------------------

output_file = os.path.join(test_dir, "output.txt")

# --- write() ---
# 注意：write() 不会自动添加换行符，需要手动添加
with open(output_file, "w", encoding="utf-8") as f:
    f.write("Hello, World!\n")
    f.write("你好，Python!\n")
    count = f.write("write() 返回写入的字符数\n")
    print(f"write() 返回: {count}")

# --- writelines() ---
# 注意：writelines() 也不会自动添加换行符
with open(output_file, "w", encoding="utf-8") as f:
    f.writelines(["line1\n", "line2\n", "line3\n"])

with open(output_file, "r", encoding="utf-8") as f:
    print(f"writelines() 写入结果: {f.read()}")

print()
print("=" * 60)
print("5. encoding 参数 — 指定编码")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   File.ReadAllText(path, Encoding.UTF8)
#   new StreamReader(path, Encoding.GetEncoding("gbk"))
# -------------------------------------------------------
encoding_file = os.path.join(test_dir, "encoding.txt")

# 写入不同编码
text = "编码测试: Hello 你好 [CELEBRATE]"

# UTF-8 (Python 默认)
with open(encoding_file, "w", encoding="utf-8") as f:
    f.write(text)

# 读取 UTF-8
with open(encoding_file, "r", encoding="utf-8") as f:
    print(f"UTF-8 读取: {f.read()}")

# GBK 编码
with open(encoding_file, "r", encoding="utf-8") as f:
    raw_bytes = f.read().encode("utf-8")
gbk_file = os.path.join(test_dir, "encoding_gbk.txt")
raw_bytes.decode("utf-8").encode("gbk", errors="replace")  # 不支持的字符会替换

with open(encoding_file, "rb") as f:
    binary = f.read()
print(f"文件大小 (UTF-8 编码): {len(binary)} 字节")

print()
print("=" * 60)
print("6. pathlib — 面向对象的路径操作 (推荐)")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   pathlib.Path  ≈  System.IO.Path + System.IO.File + System.IO.Directory
#   Python 3.4+ 引入，更 Pythonic 的文件操作方式
# -------------------------------------------------------
# 创建 Path 对象
p = pathlib.Path(test_dir) / "test.txt"
print(f"Path 对象: {p}")
print(f"  文件名: {p.name}")
print(f"  扩展名: {p.suffix}")
print(f"  父目录: {p.parent}")
print(f"  是否存在: {p.exists()}")
print(f"  文件大小: {p.stat().st_size} 字节")

# pathlib 读写文件（最简洁的方式）
content = p.read_text(encoding="utf-8")
print(f"  read_text(): {content.strip()}")

p.write_text("pathlib 写入的内容\n第二行\n", encoding="utf-8")
print(f"  write_text() 完成")

# 遍历目录
print(f"\n  目录 {test_dir} 下的文件:")
for item in pathlib.Path(test_dir).iterdir():
    print(f"    {'[DIR]' if item.is_dir() else '[FILE]'} {item.name}")

print()
print("=" * 60)
print("7. tempfile — 临时文件和临时目录")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   Path.GetTempFileName()     ≈  tempfile.NamedTemporaryFile()
#   Path.GetTempPath()         ≈  tempfile.gettempdir()
#   using var tmp = ...        ≈  with tempfile.NamedTemporaryFile() as tmp:
# -------------------------------------------------------
# 创建临时文件
with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                  delete=False, encoding="utf-8") as tmp:
    tmp.write("这是一个临时文件\n")
    tmp_name = tmp.name
    print(f"临时文件: {tmp_name}")

# 读取临时文件
with open(tmp_name, "r", encoding="utf-8") as f:
    print(f"读取: {f.read().strip()}")

# 创建临时目录
with tempfile.TemporaryDirectory() as tmp_dir:
    tmp_path = pathlib.Path(tmp_dir)
    tmp_file = tmp_path / "temp_data.txt"
    tmp_file.write_text("临时目录中的文件\n", encoding="utf-8")
    print(f"临时目录: {tmp_dir}")
    print(f"  目录内容: {list(tmp_path.iterdir())}")
# 离开 with 块后，临时目录和其中的文件自动删除

# 清理
os.unlink(tmp_name)

print()
print("=" * 60)
print("8. io.StringIO — 内存中的文件对象")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   StringIO ≈ MemoryStream + StreamWriter/StreamReader
#   用于在内存中模拟文件操作，常用于测试和字符串处理
# -------------------------------------------------------
# 创建 StringIO
buffer = io.StringIO()
buffer.write("第一行\n")
buffer.write("第二行\n")
buffer.write("第三行\n")

# seek 回到开头
buffer.seek(0)
content = buffer.read()
print(f"StringIO 内容:\n{content}")
buffer.close()

# 从字符串初始化
buffer2 = io.StringIO("Hello StringIO\n")
lines = buffer2.readlines()
print(f"从字符串初始化: {lines}")
buffer2.close()

print()
print("=" * 60)
print("9. 上下文管理器同时打开多个文件")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   using (var fin = new StreamReader(inPath))
#   using (var fout = new StreamWriter(outPath))
#   {
#       // ...
#   }
# -------------------------------------------------------
input_file = os.path.join(test_dir, "input.txt")
output_file = os.path.join(test_dir, "upper_output.txt")

with open(input_file, "w", encoding="utf-8") as f:
    f.write("hello world\n")
    f.write("python file io\n")

# Python 3.10+ 可以用括号包裹
with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file, "w", encoding="utf-8") as fout:
    for line in fin:
        fout.write(line.upper())

with open(output_file, "r", encoding="utf-8") as f:
    print(f"转换结果: {f.read().strip()}")

print()
print("=" * 60)
print("10. 文件操作速查表")
print("=" * 60)

# -------------------------------------------------------
# C# 对比：
#   File.Copy / File.Move / File.Delete / File.Exists
#   Directory.CreateDirectory / Directory.GetFiles
# -------------------------------------------------------
import shutil

# 文件操作
src_file = os.path.join(test_dir, "test.txt")
copy_file = os.path.join(test_dir, "test_copy.txt")
rename_file = os.path.join(test_dir, "test_renamed.txt")

shutil.copy(src_file, copy_file)
print(f"复制: {src_file} -> {copy_file}")

os.rename(copy_file, rename_file)
print(f"重命名: {copy_file} -> {rename_file}")

exists = os.path.exists(rename_file)
print(f"文件是否存在: {exists}")

size = os.path.getsize(rename_file)
print(f"文件大小: {size} 字节")

os.remove(rename_file)
print(f"删除: {rename_file}")

# 目录操作
new_dir = os.path.join(test_dir, "new_folder")
os.makedirs(new_dir, exist_ok=True)
print(f"创建目录: {new_dir}")

files = os.listdir(test_dir)
print(f"目录内容: {files}")

# 清理演示目录
shutil.rmtree(test_dir)
print(f"清理演示目录: {test_dir}")

print()
print("=" * 60)
print("11. 文件操作最佳实践总结")
print("=" * 60)
print("""
Python vs C# 文件操作对比:
  Python open() + with           ≈  C# File.ReadAllText / using StreamReader
  Python pathlib.Path             ≈  C# System.IO.Path + File
  Python io.StringIO              ≈  C# MemoryStream
  Python tempfile                 ≈  C# Path.GetTempFileName
  Python os.path / shutil         ≈  C# System.IO.File / Directory

最佳实践:
  1. 始终使用 with/using 确保资源释放
  2. 指定 encoding 参数，避免平台编码差异
  3. 小文件用 read()/write()，大文件用迭代逐行处理
  4. 路径操作优先使用 pathlib (Python) / Path (C#)
  5. 临时文件使用 tempfile 模块管理
""")

print("所有文件读写示例运行完毕！")
