# Python Hello World（带入口保护）
# 对应文章：1.1 Hello World 与程序结构

# if __name__ == "__main__" 是 Python 的"入口保护"
# 作用：当文件被直接运行时执行，被 import 时不执行
# 类似 C# 的 if (args.Length > 0) 但更常见
#
# C# 对比：
# C# 的入口点是 Main 方法，编译器自动识别
# Python 没有固定的入口点，靠 __name__ 变量判断
#   - 直接运行：__name__ == "__main__"
#   - 被导入：__name__ == 模块名（如 "hello_with_main"）

def greet(name: str) -> str:
    """向指定用户打招呼"""
    return f"Hello, {name}!"

def main():
    print(greet("World"))
    print(greet("Python"))

if __name__ == "__main__":
    main()
