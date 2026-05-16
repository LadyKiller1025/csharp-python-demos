"""
Python 单元测试完整示例
对应文章：4.5 单元测试

C# 对比：
  Python unittest.TestCase   ≈  C# [TestClass] + [TestMethod] (MSTest)
  Python assertEqual          ≈  C# Assert.AreEqual (MSTest/NUnit)
  Python setUp/tearDown      ≈  C# [TestInitialize]/[TestCleanup] (MSTest)
  Python @patch              ≈  C# Moq / NSubstitute
  Python @skipIf             ≈  C# [Conditional("DEBUG")] / Assert.Inconclusive
  Python pytest              ≈  C# xUnit / NUnit (第三方框架)
"""
import unittest
import sys
import os
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime

# =============================================================
# 被测试的类（生产代码）
# =============================================================
class Calculator:
    """计算器类 — 用于演示单元测试"""
    def __init__(self):
        self.history = []

    def add(self, a: float, b: float) -> float:
        result = a + b
        self.history.append(("add", a, b, result))
        return result

    def subtract(self, a: float, b: float) -> float:
        result = a - b
        self.history.append(("subtract", a, b, result))
        return result

    def multiply(self, a: float, b: float) -> float:
        result = a * b
        self.history.append(("multiply", a, b, result))
        return result

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("除数不能为零")
        result = a / b
        self.history.append(("divide", a, b, result))
        return result

    @staticmethod
    def is_positive(n: float) -> bool:
        return n > 0

    def get_history(self) -> list:
        return self.history.copy()


class UserService:
    """用户服务 — 用于演示 mock"""
    def __init__(self, db=None):
        self.db = db

    def get_user(self, user_id: int) -> dict:
        user = self.db.find_user(user_id)
        if user is None:
            raise ValueError(f"用户 {user_id} 不存在")
        return user

    def create_user(self, name: str, email: str) -> dict:
        if not name or not email:
            raise ValueError("名字和邮箱不能为空")
        user = {"name": name, "email": email}
        self.db.save_user(user)
        return user

    def get_user_count(self) -> int:
        return self.db.count_users()

    def send_welcome_email(self, user: dict) -> bool:
        """发送欢迎邮件（需要外部服务）"""
        # 模拟发送邮件
        print(f"  [发送邮件] 向 {user['email']} 发送欢迎邮件...")
        return True


# =============================================================
# 1. unittest — 基础 TestCase (Python 内置测试框架)
# =============================================================
# C# 对比：
#   [TestClass]
#   public class CalculatorTests
#   {
#       [TestMethod]
#       public void Add_ReturnsSum() { ... }
#   }
# =============================================================
print("=" * 60)
print("1. unittest — 基础 TestCase")
print("=" * 60)


class TestCalculatorBasic(unittest.TestCase):
    """基础测试用例 — 演示常用的 assert 方法"""

    # -------------------------------------------------------
    # C# 对比：
    #   [TestInitialize]
    #   public void Setup() { ... }
    # -------------------------------------------------------
    def setUp(self):
        """每个测试方法执行前调用（≈ C# [TestInitialize] / xUnit 构造函数）"""
        self.calc = Calculator()

    def tearDown(self):
        """每个测试方法执行后调用（≈ C# [TestCleanup] / xUnit IDisposable.Dispose）"""
        pass  # 清理资源

    # --- assertEqual / assertNotEqual ---
    # C# 等价：Assert.AreEqual / Assert.AreNotEqual
    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(4, 3), 12)

    # --- assertRaises ---
    # C# 等价：Assert.ThrowsException<DivideByZeroException>(() => ...)
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError) as ctx:
            self.calc.divide(10, 0)
        self.assertIn("除数不能为零", str(ctx.exception))

    # --- assertAlmostEqual (浮点数比较) ---
    # C# 等价：Assert.AreEqual(expected, actual, delta)
    def test_divide_float(self):
        result = self.calc.divide(10, 3)
        self.assertAlmostEqual(result, 3.333, places=2)

    # --- assertTrue / assertFalse ---
    # C# 等价：Assert.IsTrue / Assert.IsFalse
    def test_is_positive(self):
        self.assertTrue(Calculator.is_positive(5))
        self.assertFalse(Calculator.is_positive(-5))
        self.assertFalse(Calculator.is_positive(0))

    # --- assertIn / assertNotIn ---
    # C# 等价：CollectionAssert.Contains / CollectionAssert.DoesNotContain
    def test_history_recorded(self):
        self.calc.add(1, 2)
        history = self.calc.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0], ("add", 1, 2, 3))


# 运行基础测试
print("运行基础测试...")
loader = unittest.TestLoader()
suite = loader.loadTestsFromTestCase(TestCalculatorBasic)
runner = unittest.TextTestRunner(verbosity=0)
result = runner.run(suite)
print(f"结果: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun} 通过")

# =============================================================
# 2. 参数化测试
# =============================================================
# C# 对比：
#   [Theory]
#   [InlineData(2, 3, 5)]
#   [InlineData(-1, 1, 0)]
#   public void Add_MultipleCases(int a, int b, int expected) { ... }
# =============================================================
print()
print("=" * 60)
print("2. 参数化测试")
print("=" * 60)

# unittest 没有内置参数化，用 subTest 模拟
class TestCalculatorParametrized(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add_parametrized(self):
        """使用 subTest 实现参数化"""
        test_cases = [
            (2, 3, 5),
            (-1, 1, 0),
            (0, 0, 0),
            (100, -100, 0),
            (0.1, 0.2, 0.3),  # 浮点数精度
        ]
        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                self.assertAlmostEqual(self.calc.add(a, b), expected, places=7)


suite2 = loader.loadTestsFromTestCase(TestCalculatorParametrized)
result2 = runner.run(suite2)
print(f"参数化测试: {result2.testsRun - len(result2.failures) - len(result2.errors)}/{result2.testsRun} 通过")

# =============================================================
# 3. setUp / tearDown — 测试装置
# =============================================================
# C# 对比：
#   [ClassInitialize]  →  类级别 setUpClass
#   [TestInitialize]   →  方法级别 setUp
#   [TestCleanup]      →  方法级别 tearDown
#   [ClassCleanup]     →  类级别 tearDownClass
# =============================================================
print()
print("=" * 60)
print("3. setUp / tearDown — 测试装置")
print("=" * 60)


class TestCalculatorSetup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """整个测试类只执行一次（≈ C# [ClassInitialize] / xUnit IClassFixture）"""
        print("  [setUpClass] 一次性设置: 创建数据库连接、加载配置等")

    @classmethod
    def tearDownClass(cls):
        """整个测试类结束时执行一次（≈ C# [ClassCleanup]）"""
        print("  [tearDownClass] 一次性清理: 关闭连接、删除临时文件等")

    def setUp(self):
        """每个测试方法前执行（≈ C# [TestInitialize] / xUnit 构造函数）"""
        self.calc = Calculator()
        self.calc.add(1, 1)  # 预置数据

    def tearDown(self):
        """每个测试方法后执行（≈ C# [TestCleanup] / xUnit IDisposable.Dispose）"""
        self.calc = None  # 释放引用

    def test_preset_data(self):
        """验证 setUp 创建的预置数据"""
        self.assertEqual(len(self.calc.history), 1)

    def test_fresh_after_setup(self):
        """每次 setUp 都会创建全新的 Calculator"""
        self.assertEqual(len(self.calc.history), 1)  # 只有 setUp 添加的 1 条


# =============================================================
# 4. 异常测试
# =============================================================
# C# 对比：
#   [TestMethod]
#   [ExpectedException(typeof(InvalidOperationException))]
#   或 Assert.ThrowsException<T>(() => ...)
# =============================================================
print()
print("=" * 60)
print("4. 异常测试")
print("=" * 60)


class TestCalculatorExceptions(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_divide_by_zero_raises_value_error(self):
        """验证抛出特定异常"""
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

    def test_divide_by_zero_error_message(self):
        """验证异常消息内容"""
        with self.assertRaisesRegex(ValueError, "除数不能为零"):
            self.calc.divide(10, 0)

    def test_exception_context(self):
        """验证异常上下文"""
        try:
            self.calc.divide(10, 0)
        except ValueError as e:
            self.assertEqual(str(e), "除数不能为零")
            self.assertEqual(type(e), ValueError)


suite4 = loader.loadTestsFromTestCase(TestCalculatorExceptions)
result4 = runner.run(suite4)
print(f"异常测试: {result4.testsRun - len(result4.failures) - len(result4.errors)}/{result4.testsRun} 通过")

# =============================================================
# 5. Mock 和 Patch — 模拟外部依赖
# =============================================================
# C# 对比：
#   var mockDb = new Mock<IDatabase>();
#   mockDb.Setup(x => x.FindUser(It.IsAny<int>()))
#         .Returns(new User { Name = "Alice" });
# =============================================================
print()
print("=" * 60)
print("5. Mock 和 Patch — 模拟外部依赖")
print("=" * 60)


class TestUserServiceMock(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.service = UserService(db=self.mock_db)

    def test_get_user(self):
        """使用 MagicMock 模拟数据库"""
        # 设置 mock 返回值
        self.mock_db.find_user.return_value = {"name": "Alice", "email": "alice@example.com"}

        user = self.service.get_user(1)
        self.assertEqual(user["name"], "Alice")

        # 验证 mock 被调用（≈ C# mock.Verify()）
        self.mock_db.find_user.assert_called_once_with(1)

    def test_get_user_not_found(self):
        """测试用户不存在的情况"""
        self.mock_db.find_user.return_value = None

        with self.assertRaises(ValueError) as ctx:
            self.service.get_user(999)
        self.assertIn("不存在", str(ctx.exception))

    def test_create_user(self):
        """测试创建用户"""
        self.mock_db.save_user.return_value = None

        user = self.service.create_user("Bob", "bob@example.com")
        self.assertEqual(user["name"], "Bob")
        self.mock_db.save_user.assert_called_once_with(user)

    def test_create_user_validation(self):
        """测试参数验证"""
        with self.assertRaises(ValueError):
            self.service.create_user("", "bob@example.com")
        with self.assertRaises(ValueError):
            self.service.create_user("Bob", "")

    def test_get_user_count(self):
        """测试获取用户数"""
        self.mock_db.count_users.return_value = 42
        self.assertEqual(self.service.get_user_count(), 42)


suite5 = loader.loadTestsFromTestCase(TestUserServiceMock)
result5 = runner.run(suite5)
print(f"Mock 测试: {result5.testsRun - len(result5.failures) - len(result5.errors)}/{result5.testsRun} 通过")

# =============================================================
# 6. @patch — 装饰器方式的 Mock
# =============================================================
# C# 对比：
#   using (MockRepository.Create())
#   {
#       // 临时替换
#   }
# =============================================================
print()
print("=" * 60)
print("6. @patch — 装饰器方式的 Mock")
print("=" * 60)


class TestWithPatch(unittest.TestCase):
    @patch('builtins.print')  # 模拟 print 函数
    def test_send_welcome_email(self, mock_print):
        """使用 @patch 装饰器替换外部依赖"""
        service = UserService()
        user = {"name": "Alice", "email": "alice@example.com"}

        result = service.send_welcome_email(user)
        self.assertTrue(result)

        # 验证 print 被调用
        mock_print.assert_called_once_with("  [发送邮件] 向 alice@example.com 发送欢迎邮件...")

    @patch('datetime.datetime')
    def test_with_datetime_mock(self, mock_datetime):
        """模拟 datetime.now()"""
        mock_datetime.now.return_value = datetime(2024, 1, 15, 12, 0, 0)

        now = datetime.now()
        self.assertEqual(now.year, 2024)
        self.assertEqual(now.month, 1)


suite6 = loader.loadTestsFromTestCase(TestWithPatch)
result6 = runner.run(suite6)
print(f"@patch 测试: {result6.testsRun - len(result6.failures) - len(result6.errors)}/{result6.testsRun} 通过")

# =============================================================
# 7. skipIf / skipUnless — 条件跳过
# =============================================================
# C# 对比：
#   [Conditional("DEBUG")]           → 条件编译
#   Assert.Inconclusive("reason")    → 标记为跳过
#   [Skip] (NUnit)                   → 跳过测试
# =============================================================
print()
print("=" * 60)
print("7. skipIf / skipUnless — 条件跳过")
print("=" * 60)


class TestConditionalSkip(unittest.TestCase):
    @unittest.skip("演示: 跳过此测试 (≈ C# [Skip])")
    def test_skipped(self):
        """此测试始终被跳过"""
        self.fail("不应执行到这里")

    @unittest.skipIf(sys.platform == "win32", "在 Windows 上跳过 (≈ C# #if !WINDOWS)")
    def test_not_on_windows(self):
        """非 Windows 平台才运行"""
        self.assertTrue(True)

    @unittest.skipUnless(sys.platform == "win32", "仅在 Windows 上运行")
    def test_windows_only(self):
        """仅 Windows 平台运行"""
        self.assertTrue(sys.platform == "win32")


suite7 = loader.loadTestsFromTestCase(TestConditionalSkip)
result7 = runner.run(suite7)
print(f"条件跳过: {result7.testsRun} 个测试执行, "
      f"{len(result7.skipped)} 个跳过")

# =============================================================
# 8. 测试发现与运行
# =============================================================
# C# 对比：
#   dotnet test                      ≈  python -m pytest
#   dotnet test --filter "Category"  ≈  python -m pytest -k "test_add"
# =============================================================
print()
print("=" * 60)
print("8. 测试发现与运行")
print("=" * 60)
print("""
Python 测试发现命令:
  python -m unittest discover         # 自动发现并运行所有 test_*.py
  python -m pytest                    # pytest 自动发现（推荐）
  python -m pytest -v                 # 详细输出
  python -m pytest -k "add"          # 运行名称包含 "add" 的测试
  python -m pytest test_file.py      # 指定文件
  python -m unittest TestClass       # 运行指定测试类

C# 对比:
  dotnet test                        # 运行所有测试
  dotnet test --filter "FullyQualifiedName~Add"   # 过滤测试
  dotnet test --logger "console;verbosity=detailed"  # 详细输出
  vstest.console.exe /TestCaseFilter:Category=Fast   # 按分类过滤

Python 测试文件命名约定:
  test_*.py 或 *_test.py  (pytest 自动发现)

C# 测试项目命名约定:
  Project.Tests (如 Calculator.Tests)
  [TestClass] 标记测试类
  [TestMethod] 标记测试方法
""")

# =============================================================
# 9. pytest vs unittest
# =============================================================
print("=" * 60)
print("9. pytest vs unittest")
print("=" * 60)
print("""
pytest (第三方框架，推荐):
  - 语法更简洁: assert x == y (不需要 self.assertEqual)
  - 内置参数化: @pytest.mark.parametrize
  - fixture 系统更强大
  - 更好的错误信息
  - 丰富的插件生态
  pip install pytest

unittest (Python 内置):
  - 无需额外安装
  - 面向对象风格 (继承 TestCase)
  - 与 C# MSTest 风格接近
  - 适合学习测试基础概念

C# 对比:
  pytest        ≈  xUnit / NUnit (简洁，第三方)
  unittest      ≈  MSTest (内置框架，面向对象)

推荐:
  - 新项目: pytest (Python) / xUnit (C#)
  - 遗留项目: 保持与现有框架一致
""")

# =============================================================
# 10. 单元测试最佳实践总结
# =============================================================
print("=" * 60)
print("10. 单元测试最佳实践总结")
print("=" * 60)
print("""
Python vs C# 单元测试对比:
  Python TestCase               ≈  C# [TestClass] (MSTest)
  Python @test_method            ≈  C# [TestMethod] (MSTest)
  Python assertEqual             ≈  C# Assert.AreEqual
  Python assertRaises            ≈  C# Assert.ThrowsException<T>
  Python setUp / tearDown        ≈  C# [TestInitialize] / [TestCleanup]
  Python unittest.skipIf         ≈  C# [Conditional] / [Skip]
  Python unittest.mock           ≈  C# Moq / NSubstitute
  Python @patch                  ≈  C# mock.Setup(x => x.Method(...))
  Python pytest                  ≈  C# xUnit / NUnit

最佳实践:
  1. AAA 模式: Arrange → Act → Assert
  2. 每个测试方法只测试一个行为
  3. 测试名称要清晰: test_<行为>_<条件>_<期望>
  4. 使用 Mock 隔离外部依赖 (数据库、网络、文件系统)
  5. 测试正常路径和异常路径
  6. 保持测试独立性，测试之间不要有依赖
  7. 使用 setUp/tearDown 管理共享资源
  8. 测试覆盖率目标: 核心业务逻辑 > 80%
""")

# 运行所有测试
print("=" * 60)
print("运行所有测试 (最终汇总)")
print("=" * 60)
all_suite = unittest.TestSuite()
all_suite.addTests(loader.loadTestsFromTestCase(TestCalculatorBasic))
all_suite.addTests(loader.loadTestsFromTestCase(TestCalculatorParametrized))
all_suite.addTests(loader.loadTestsFromTestCase(TestCalculatorSetup))
all_suite.addTests(loader.loadTestsFromTestCase(TestCalculatorExceptions))
all_suite.addTests(loader.loadTestsFromTestCase(TestUserServiceMock))
all_suite.addTests(loader.loadTestsFromTestCase(TestWithPatch))
all_suite.addTests(loader.loadTestsFromTestCase(TestConditionalSkip))

final_runner = unittest.TextTestRunner(verbosity=0)
final_result = final_runner.run(all_suite)
print()
print(f"总计: {final_result.testsRun} 个测试, "
      f"{final_result.testsRun - len(final_result.failures) - len(final_result.errors) - len(final_result.skipped)} 通过, "
      f"{len(final_result.failures)} 失败, "
      f"{len(final_result.errors)} 错误, "
      f"{len(final_result.skipped)} 跳过")

print()
print("所有单元测试示例运行完毕！")
