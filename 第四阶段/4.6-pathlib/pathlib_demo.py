# ============================================================
# Python pathlib 模块完全指南
# 对应文章：4.6 pathlib —— 面向对象的文件路径处理
# C# 对比：System.IO.Path / Directory / FileInfo
# ============================================================
#
# 【核心对比】
#   Python pathlib   →  用 Path 对象表示路径，支持 / 运算符拼接
#   C# System.IO     →  Path（静态工具类）+ Directory + FileInfo 组合使用
#
# pathlib 优势：把路径当作对象，链式调用，比 os.path 更 Pythonic
# C# 类似思路：System.IO.Path.Combine() 但不够优雅，C# 10+ 可用新 API
# ============================================================

from pathlib import Path
import os

print("=" * 60)
print("pathlib 模块 vs C# System.IO")
print("=" * 60)


# ============================================================
# 1. Path 创建方式 —— 对比 C# 的 Path 类
# ============================================================
# 【C# 等价】
#   string home = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
#   string cwd  = Directory.GetCurrentDirectory();
#   string project = @"e:\Code\csharp-python-learning-series";
# ============================================================
print("\n===== 1. Path 创建方式 =====")

home = Path.home()           # 用户主目录
current = Path.cwd()         # 当前工作目录
project = Path("e:/Code/csharp-python-learning-series")  # 字符串转 Path
from_str = Path("/tmp/test.txt")   # 从字符串构造

print(f"home:   {home}")
print(f"cwd:    {current}")
print(f"项目:   {project}")
print(f"从字符串: {from_str}")

# 【C# 对比】C# 的 Path 类全是静态方法，不创建对象
# Python 的 Path 是实例对象，可以调用方法
# Python:  p = Path("/tmp")    → p.exists()   (对象调用)
# C#:      File.Exists(path)                       (静态方法)


# ============================================================
# 2. / 运算符拼接路径 —— pathlib 独有优势
# ============================================================
# 【C# 等价】
#   string readme = Path.Combine(project, "README.md");
#   string stage1 = Path.Combine(project, "第一阶段", "1.1-Hello-World");
#   C# 没有运算符重载，只能用 Combine() 方法
# ============================================================
print("\n===== 2. / 运算符拼接路径 =====")

readme = project / "README.md"
stage1 = project / "第一阶段" / "1.1-Hello-World与程序结构"
deep_path = project / "第一阶段" / "1.1-Hello-World与程序结构" / "hello.py"

print(f"README:  {readme}")
print(f"阶段一:  {stage1}")
print(f"深层路径: {deep_path}")

# 【Python 魔法】Path 重载了 __truediv__ 运算符 (/)
# C# 12 可以定义运算符重载，但路径拼接没有这样做
# 这是 Python pathlib 最直观的优势之一


# ============================================================
# 3. 路径组件分解 —— name / stem / suffix / parent / parts
# ============================================================
# 【C# 等价】
#   Path.GetFileName(p)      → p.name
#   Path.GetFileNameWithoutExtension(p) → p.stem
#   Path.GetExtension(p)     → p.suffix
#   Path.GetDirectoryName(p) → p.parent
#   C# 没有 parts 属性，需要自己 Split
# ============================================================
print("\n===== 3. 路径组件分解 =====")

p = Path("/home/user/docs/report.txt")
print(f"完整文件名:   p.name      = {p.name}")        # report.txt
print(f"不含后缀名:   p.stem      = {p.stem}")        # report
print(f"后缀:         p.suffix    = {p.suffix}")       # .txt
print(f"父目录:       p.parent    = {p.parent}")       # /home/user/docs
print(f"全部 parts:   p.parts     = {p.parts}")        # ('/', 'home', 'user', 'docs', 'report.txt')
print(f"祖父目录:     p.parent.parent = {p.parent.parent}")  # /home/user

# 多后缀的情况
p2 = Path("archive.tar.gz")
print(f"\narchive.tar.gz:")
print(f"  suffixes = {p2.suffixes}")   # ['.tar', '.gz'] —— Python 独有！
print(f"  stem     = {p2.stem}")       # archive
print(f"  suffix   = {p2.suffix}")     # .gz (最后一个后缀)

# 【Python vs C# 差异】
# C# 的 GetExtension 只返回最后一个后缀
# Python 的 suffixes 返回所有后缀列表，更灵活


# ============================================================
# 4. 路径判断 —— exists / is_file / is_dir / is_absolute
# ============================================================
# 【C# 等价】
#   File.Exists(path)       → path.is_file() + path.exists()
#   Directory.Exists(path)  → path.is_dir()
#   Path.IsPathRooted(path) → path.is_absolute()
# ============================================================
print("\n===== 4. 路径判断 =====")

print(f"README 存在:     {readme.exists()}")      # True
print(f"README 是文件:   {readme.is_file()}")      # True
print(f"项目 是目录:     {project.is_dir()}")      # True
print(f"项目 是绝对路径: {project.is_absolute()}")  # True

# 判断符号链接
p_link = Path("/tmp/link")
if p_link.exists():
    print(f"是符号链接: {p_link.is_symlink()}")

# 【C# 对比】C# 需要分别调用 File.Exists 和 Directory.Exists
# Python 用一个 exists() 搞定，然后用 is_file/is_dir 区分


# ============================================================
# 5. resolve() —— 解析为绝对路径（解析符号链接）
# ============================================================
# 【C# 等价】
#   Path.GetFullPath(path)   → path.resolve()
#   C# 没有内置的符号链接解析，需要 P/Invoke
# ============================================================
print("\n===== 5. resolve() 解析绝对路径 =====")

relative = Path("README.md")
resolved = relative.resolve()
print(f"相对路径:  {relative}")
print(f"解析后:    {resolved}")          # /绝对路径/README.md
print(f"是否绝对:  {resolved.is_absolute()}")  # True


# ============================================================
# 6. home() / cwd() —— 特殊路径
# ============================================================
# 【C# 等价】
#   Environment.GetFolderPath(SpecialFolder.UserProfile) → Path.home()
#   Directory.GetCurrentDirectory()                      → Path.cwd()
# ============================================================
print("\n===== 6. home() / cwd() =====")

print(f"用户主目录: {Path.home()}")
print(f"当前工作目录: {Path.cwd()}")

# 跨平台差异：Python pathlib 自动处理 / vs \ 分隔符
# C# 在 Windows 上用 \，在 Linux 上用 /
# Python pathlib 在所有平台上用 / 构造路径，内部自动转换


# ============================================================
# 7. read_text / write_text —— 读写文件一步到位
# ============================================================
# 【C# 等价】
#   File.ReadAllText(path)    → path.read_text()
#   File.WriteAllText(path, text) → path.write_text(text)
#   C# 需要 System.IO.File 静态类，Python 用 Path 实例方法
# ============================================================
print("\n===== 7. read_text / write_text =====")

# 写入临时文件
temp_file = Path.cwd() / "temp_demo.txt"
temp_file.write_text("Hello pathlib!\n第二行内容\n", encoding="utf-8")
print(f"写入文件: {temp_file}")

# 读取文件
content = temp_file.read_text(encoding="utf-8")
print(f"读取内容: {content.strip()}")

# 读取 README 前 100 字符
if readme.exists():
    readme_content = readme.read_text(encoding="utf-8")
    print(f"README 前 80 字: {readme_content[:80]}...")

# 清理临时文件
temp_file.unlink()   # 删除文件
print(f"删除临时文件: 完成")


# ============================================================
# 8. exists / mkdir / rmtree —— 目录操作
# ============================================================
# 【C# 等价】
#   Directory.CreateDirectory(path)  → path.mkdir()
#   Directory.Delete(path, true)     → path.rmtree()  (Python 3.12+)
#   C# 需要 Directory 类，Python 全在 Path 对象上操作
# ============================================================
print("\n===== 8. mkdir / rmtree 目录操作 =====")

# 创建临时目录（parents=True 递归创建，exist_ok=True 不报错）
demo_dir = Path.cwd() / "temp_dir_demo" / "sub_dir"
demo_dir.mkdir(parents=True, exist_ok=True)
print(f"创建目录: {demo_dir}")
print(f"目录存在: {demo_dir.exists()}")

# 写入文件到临时目录
sub_file = demo_dir / "test.txt"
sub_file.write_text("测试文件", encoding="utf-8")

# 遍历目录内容
print(f"目录内容:")
for item in demo_dir.iterdir():
    print(f"  {'[DIR] ' if item.is_dir() else '      '}{item.name}")

# 删除整个目录树（Python 3.12+）
# 如果是旧版本，需要 import shutil; shutil.rmtree(demo_dir.parent)
try:
    import shutil
    shutil.rmtree(demo_dir.parent)
    print(f"删除目录树: {demo_dir.parent} — 完成")
except ImportError:
    # Python 3.12+ 可直接用 Path.rmtree()
    demo_dir.parent.rmdir()  # rmdir 只能删空目录
    print(f"删除空目录: 完成")

# 【Python 3.12 新特性】Path.rmtree() 替代 shutil.rmtree()
# 这让 pathlib 更加自包含，不需要额外导入 shutil


# ============================================================
# 9. glob / rglob —— 文件搜索（通配符匹配）
# ============================================================
# 【C# 等价】
#   Directory.GetFiles(dir, "*.py", SearchOption.AllDirectories)
#   Python 的 glob 功能更强大，支持 ** 递归匹配
# ============================================================
print("\n===== 9. glob / rglob 文件搜索 =====")

# glob: 当前目录匹配
py_files = list(project.glob("*.md"))
print(f"项目根目录的 .md 文件 ({len(py_files)} 个):")
for f in py_files[:5]:
    print(f"  {f.name}")

# rglob: 递归匹配所有子目录
all_py = list(project.rglob("*.py"))
print(f"\n递归搜索所有 .py 文件 ({len(all_py)} 个):")
for f in all_py[:5]:
    # 显示相对路径，更易读
    try:
        rel = f.relative_to(project)
        print(f"  {rel}")
    except ValueError:
        print(f"  {f.name}")

# 【Python 高级用法】glob 支持多种模式
# project.glob("**/*.py")   等价于 rglob("*.py")
# project.glob("*.py,*.js") 不直接支持，需分开搜索


# ============================================================
# 10. stat() —— 获取文件元信息
# ============================================================
# 【C# 等价】
#   FileInfo fi = new FileInfo(path);
#   fi.Length        → stat.st_size
#   fi.LastWriteTime → stat.st_mtime
#   fi.CreationTime  → stat.st_ctime (Windows) / stat.st_birthtime (Unix)
# ============================================================
print("\n===== 10. stat() 文件元信息 =====")

if readme.exists():
    st = readme.stat()
    print(f"文件: {readme.name}")
    print(f"  大小: {st.st_size:,} bytes ({st.st_size / 1024:.1f} KB)")
    print(f"  修改时间: {st.st_mtime}")
    print(f"  创建时间: {st.st_ctime}")

    # Python 3.10+ 有更清晰的属性名
    # st.st_birthtime  → 文件创建时间 (跨平台)
    # st.st_atime      → 最后访问时间
    # st.st_mtime      → 最后修改时间
    print(f"  最后访问: {st.st_atime}")

# 【C# 对比】C# 的 FileInfo 对象更重量级
# Python 的 stat() 返回轻量级命名元组，用起来更简洁


# ============================================================
# 11. suffix / name / stem / with_suffix / with_name
# ============================================================
# 【C# 等价】
#   Path.ChangeExtension(path, ".txt")  → path.with_suffix(".txt")
#   没有 with_name 等价物
# ============================================================
print("\n===== 11. 修改路径组件 =====")

original = Path("report.final.docx")
print(f"原始路径:   {original}")
print(f"  name:     {original.name}")
print(f"  stem:     {original.stem}")
print(f"  suffix:   {original.suffix}")
print(f"  suffixes: {original.suffixes}")

# 替换后缀
txt_version = original.with_suffix(".txt")
print(f"改后缀 .txt: {txt_version.name}")      # report.final.txt

# 替换文件名
new_name = original.with_name("summary.pdf")
print(f"改文件名:    {new_name.name}")          # summary.pdf

# 替换 stem
new_stem = original.with_stem("analysis")
print(f"改 stem:     {new_stem.name}")          # analysis.docx

# 【Python 3.12 新特性】with_stem() 是 Python 3.12 新增
# C# 没有直接对应，需要手动拼接 Path.ChangeExtension + 文件名操作


# ============================================================
# 12. relative_to / parts —— 路径相对化
# ============================================================
# 【C# 等价】
#   Path.GetRelativePath(basePath, fullPath) → path.relative_to(base)
# ============================================================
print("\n===== 12. relative_to 路径相对化 =====")

full = project / "第二阶段" / "2.1-函数定义" / "README.md"
try:
    rel = full.relative_to(project)
    print(f"完整路径: {full}")
    print(f"相对路径: {rel}")
    print(f"parts:    {rel.parts}")  # ('第二阶段', '2.1-函数定义', 'README.md')
except ValueError as e:
    print(f"无法计算相对路径: {e}")


# ============================================================
# 总结对比表
# ============================================================
print("\n" + "=" * 60)
print("总结：pathlib vs C# System.IO")
print("=" * 60)
comparison = """
┌──────────────────────┬──────────────────────────┬───────────────────────────────┐
│      操作            │    Python pathlib        │    C# System.IO               │
├──────────────────────┼──────────────────────────┼───────────────────────────────┤
│ 创建路径对象         │ Path("a/b/c")            │ 不用创建，直接传字符串          │
│ 路径拼接             │ p / "sub" / "file"       │ Path.Combine(p, "sub", "file")│
│ 判断存在             │ p.exists()               │ File.Exists(p) + Dir.Exists() │
│ 创建目录             │ p.mkdir(parents=True)    │ Directory.CreateDirectory(p)  │
│ 删除目录树           │ shutil.rmtree(p)         │ Directory.Delete(p, true)     │
│ 读取文本             │ p.read_text()            │ File.ReadAllText(p)           │
│ 写入文本             │ p.write_text(text)       │ File.WriteAllText(p, text)    │
│ 文件搜索             │ p.glob("**/*.py")        │ Directory.GetFiles(p,"*.py",R)│
│ 文件信息             │ p.stat()                 │ new FileInfo(p)               │
│ 修改后缀             │ p.with_suffix(".txt")    │ Path.ChangeExtension(p,".txt")│
│ 解析绝对路径         │ p.resolve()              │ Path.GetFullPath(p)           │
└──────────────────────┴──────────────────────────┴───────────────────────────────┘
"""
print(comparison)
print("完成!")
