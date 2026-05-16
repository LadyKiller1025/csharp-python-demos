using System;
using System.Collections.Generic;
using System.Linq;

/// <summary>
/// C# 单元测试完整示例
/// 对应文章：4.5 单元测试
///
/// Python 对比：
///   C# [TestMethod] (MSTest)       ≈  Python def test_xxx (unittest)
///   C# [Fact] (xUnit)              ≈  Python def test_xxx (pytest)
///   C# Assert.AreEqual             ≈  Python self.assertEqual
///   C# [TestInitialize]            ≈  Python setUp
///   C# [TestCleanup]               ≈  Python tearDown
///   C# Moq / NSubstitute           ≈  Python unittest.mock
///   C# [DataRow] (MSTest)          ≈  Python @pytest.mark.parametrize
/// </summary>
class UnitTesting
{
    static void Main()
    {
        Console.WriteLine("============================================================");
        Console.WriteLine("C# 单元测试示例 — Main 方法模拟测试执行");
        Console.WriteLine("============================================================");
        Console.WriteLine();
        Console.WriteLine("注意: 以下示例模拟了 MSTest/xUnit 风格的测试");
        Console.WriteLine("实际项目中，请在测试项目中使用 [TestClass] 和 [TestMethod]");
        Console.WriteLine();

        // =============================================================
        // 1. MSTest 风格测试
        // =============================================================
        Console.WriteLine("============================================================");
        Console.WriteLine("1. MSTest 风格测试 — [TestClass] + [TestMethod]");
        Console.WriteLine("============================================================");
        Console.WriteLine();
        Console.WriteLine("Python 对比:");
        Console.WriteLine("  [TestClass]          ≈  class TestXxx(unittest.TestCase):");
        Console.WriteLine("  [TestMethod]         ≈  def test_xxx(self):");
        Console.WriteLine("  [TestInitialize]     ≈  def setUp(self):");
        Console.WriteLine("  [TestCleanup]        ≈  def tearDown(self):");
        Console.WriteLine();
        Console.WriteLine("MSTest 示例代码:");
        Console.WriteLine("  [TestClass]");
        Console.WriteLine("  public class CalculatorTests");
        Console.WriteLine("  {");
        Console.WriteLine("      private Calculator _calc;");
        Console.WriteLine("");
        Console.WriteLine("      [TestInitialize]");
        Console.WriteLine("      public void Setup() { _calc = new Calculator(); }");
        Console.WriteLine("");
        Console.WriteLine("      [TestMethod]");
        Console.WriteLine("      public void Add_TwoNumbers_ReturnsSum()");
        Console.WriteLine("      {");
        Console.WriteLine("          Assert.AreEqual(5, _calc.Add(2, 3));");
        Console.WriteLine("      }");
        Console.WriteLine("  }");
        Console.WriteLine();

        // 实际执行演示
        var calc = new Calculator();

        // 模拟: Assert.AreEqual(5, calc.Add(2, 3))
        AssertEqual("Add(2, 3) == 5", 5, calc.Add(2, 3));

        // 模拟: Assert.AreEqual(2, calc.Subtract(5, 3))
        AssertEqual("Subtract(5, 3) == 2", 2, calc.Subtract(5, 3));

        // 模拟: Assert.AreEqual(12, calc.Multiply(4, 3))
        AssertEqual("Multiply(4, 3) == 12", 12, calc.Multiply(4, 3));

        // =============================================================
        // 2. Assert 方法大全
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("2. Assert 方法大全");
        Console.WriteLine("============================================================");
        Console.WriteLine();
        Console.WriteLine("C# Assert 方法             Python assert 方法");
        Console.WriteLine("---------------------------|-------------------------------");
        Console.WriteLine("Assert.AreEqual(a, b)     | self.assertEqual(a, b)");
        Console.WriteLine("Assert.AreNotEqual(a, b)  | self.assertNotEqual(a, b)");
        Console.WriteLine("Assert.IsTrue(x)          | self.assertTrue(x)");
        Console.WriteLine("Assert.IsFalse(x)         | self.assertFalse(x)");
        Console.WriteLine("Assert.IsNull(x)          | self.assertIsNone(x)");
        Console.WriteLine("Assert.IsNotNull(x)       | self.assertIsNotNone(x)");
        Console.WriteLine("Assert.Contains(a, b)     | self.assertIn(a, b)");
        Console.WriteLine("Assert.Empty(collection)  | self.assertEqual(len(c), 0)");
        Console.WriteLine("Assert.Throws<T>(() =>)   | with self.assertRaises(T):");
        Console.WriteLine("Assert.Equal(a, b, delta) | self.assertAlmostEqual(a, b, places=2)");
        Console.WriteLine();

        // 实际执行
        AssertTrue("5 > 3", 5 > 3);
        AssertFalse("5 < 3", 5 < 3);
        AssertNotNull("new object()", new object());

        var list = new List<int> { 1, 2, 3 };
        AssertContains("list contains 2", list, 2);

        // =============================================================
        // 3. xUnit 风格测试
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("3. xUnit 风格测试 — [Fact] + [Theory]");
        Console.WriteLine("============================================================");
        Console.WriteLine();
        Console.WriteLine("Python 对比:");
        Console.WriteLine("  [Fact]              ≈  def test_xxx(): (pytest)");
        Console.WriteLine("  [Theory]            ≈  @pytest.mark.parametrize");
        Console.WriteLine("  [InlineData(1,2,3)]  ≈  @pytest.mark.parametrize('a,b', [(1,2)])");
        Console.WriteLine("  构造函数             ≈  @pytest.fixture");
        Console.WriteLine("  IDisposable.Dispose ≈  fixture teardown");
        Console.WriteLine();
        Console.WriteLine("xUnit 示例代码:");
        Console.WriteLine("  public class CalculatorTests");
        Console.WriteLine("  {");
        Console.WriteLine("      private readonly Calculator _calc;");
        Console.WriteLine("");
        Console.WriteLine("      public CalculatorTests()  // 构造函数 = fixture");
        Console.WriteLine("      {");
        Console.WriteLine("          _calc = new Calculator();");
        Console.WriteLine("      }");
        Console.WriteLine("");
        Console.WriteLine("      [Fact]");
        Console.WriteLine("      public void Add_ReturnsSum()");
        Console.WriteLine("      {");
        Console.WriteLine("          Assert.Equal(5, _calc.Add(2, 3));");
        Console.WriteLine("      }");
        Console.WriteLine("");
        Console.WriteLine("      [Theory]");
        Console.WriteLine("      [InlineData(2, 3, 5)]");
        Console.WriteLine("      [InlineData(-1, 1, 0)]");
        Console.WriteLine("      [InlineData(0, 0, 0)]");
        Console.WriteLine("      public void Add_MultipleCases(int a, int b, int expected)");
        Console.WriteLine("      {");
        Console.WriteLine("          Assert.Equal(expected, _calc.Add(a, b));");
        Console.WriteLine("      }");
        Console.WriteLine("  }");
        Console.WriteLine();

        // 模拟 [Theory] + [InlineData]
        Console.WriteLine("模拟 [Theory] + [InlineData] 参数化测试:");
        var testCases = new (int a, int b, int expected)[]
        {
            (2, 3, 5),
            (-1, 1, 0),
            (0, 0, 0),
            (100, -100, 0),
        };

        foreach (var (a, b, expected) in testCases)
        {
            int result = calc.Add(a, b);
            AssertEqual($"Add({a}, {b}) == {expected}", expected, result);
        }

        // =============================================================
        // 4. 异常测试
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("4. 异常测试");
        Console.WriteLine("============================================================");
        Console.WriteLine();
        Console.WriteLine("Python 对比:");
        Console.WriteLine("  with self.assertRaises(ValueError):");
        Console.WriteLine("      calc.divide(10, 0)");
        Console.WriteLine("  // 或 pytest:");
        Console.WriteLine("  with pytest.raises(ValueError, match='除数不能为零'):");
        Console.WriteLine("      calc.divide(10, 0)");
        Console.WriteLine();
        Console.WriteLine("C# 方式:");
        Console.WriteLine("  // MSTest:");
        Console.WriteLine("  Assert.ThrowsException<DivideByZeroException>(() => calc.Divide(10, 0));");
        Console.WriteLine("  // xUnit:");
        Console.WriteLine("  Assert.Throws<DivideByZeroException>(() => calc.Divide(10, 0));");
        Console.WriteLine();

        // 实际执行
        try
        {
            calc.Divide(10, 0);
            Console.WriteLine("  [FAIL] 应该抛出 DivideByZeroException");
        }
        catch (DivideByZeroException)
        {
            Console.WriteLine("  [PASS] DivideByZeroException 被正确抛出");
        }

        try
        {
            calc.Divide(10, 0);
        }
        catch (DivideByZeroException ex)
        {
            Console.WriteLine($"  [PASS] 异常消息: {ex.Message}");
        }

        // =============================================================
        // 5. Mock 和依赖注入
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("5. Mock 和依赖注入");
        Console.WriteLine("============================================================");
        Console.WriteLine();
        Console.WriteLine("Python 对比:");
        Console.WriteLine("  from unittest.mock import MagicMock, patch");
        Console.WriteLine("  mock_db = MagicMock()");
        Console.WriteLine("  mock_db.find_user.return_value = {'name': 'Alice'}");
        Console.WriteLine("  service = UserService(db=mock_db)");
        Console.WriteLine();
        Console.WriteLine("C# 方式 (需要 Moq 库):");
        Console.WriteLine("  var mockDb = new Mock<IDatabase>();");
        Console.WriteLine("  mockDb.Setup(x => x.FindUser(It.IsAny<int>()))");
        Console.WriteLine("        .Returns(new User { Name = \"Alice\" });");
        Console.WriteLine("  var service = new UserService(mockDb.Object);");
        Console.WriteLine();

        // 模拟 Mock 行为
        var mockDb = new MockDatabase();
        mockDb.Users[1] = new User { Name = "Alice", Email = "alice@example.com" };

        var userService = new UserService(mockDb);

        // 测试 GetUser
        var user = userService.GetUser(1);
        Console.WriteLine($"  [PASS] GetUser(1): {user.Name}");

        // 测试 Mock 验证 (≈ Python mock.assert_called_once_with())
        Console.WriteLine($"  [PASS] Mock 调用验证: FindUser(1) 被调用 {mockDb.FindUserCallCount} 次");

        // 测试异常
        try
        {
            userService.GetUser(999);
            Console.WriteLine("  [FAIL] 应该抛出异常");
        }
        catch (ArgumentException)
        {
            Console.WriteLine("  [PASS] GetUser(999) 正确抛出异常");
        }

        // =============================================================
        // 6. 条件编译 — 跳过测试
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("6. 条件编译 — 跳过测试");
        Console.WriteLine("============================================================");
        Console.WriteLine();
        Console.WriteLine("Python 对比:");
        Console.WriteLine("  @unittest.skip(\"reason\")");
        Console.WriteLine("  @unittest.skipIf(sys.platform == 'win32', 'Windows 跳过')");
        Console.WriteLine("  @unittest.skipUnless(sys.platform == 'linux', '仅 Linux')");
        Console.WriteLine();
        Console.WriteLine("C# 方式:");
        Console.WriteLine("  // MSTest:");
        Console.WriteLine("  [TestCategory(\"SkipThisTest\")]  // 用 filter 排除");
        Console.WriteLine("  // xUnit:");
        Console.WriteLine("  [Fact(Skip = \"reason\")]");
        Console.WriteLine("  // NUnit:");
        Console.WriteLine("  [Ignore(\"reason\")]");
        Console.WriteLine("  // 条件编译:");
        Console.WriteLine("  #if DEBUG");
        Console.WriteLine("  [TestMethod] public void DebugOnlyTest() { ... }");
        Console.WriteLine("  #endif");
        Console.WriteLine("  // 或");
        Console.WriteLine("  [TestMethod]");
        Console.WriteLine("  [Conditional(\"DEBUG\")]");
        Console.WriteLine("  public void DebugOnlyTest() { ... }");
        Console.WriteLine();

        // 条件执行演示
#if DEBUG
        Console.WriteLine("  [PASS] DEBUG 模式下的测试正在运行");
#else
        Console.WriteLine("  [SKIP] 非 DEBUG 模式，条件编译测试已跳过");
#endif

        // =============================================================
        // 7. 测试发现与运行
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("7. 测试发现与运行");
        Console.WriteLine("============================================================");
        Console.WriteLine();
        Console.WriteLine("Python 测试命令:");
        Console.WriteLine("  python -m unittest discover         # unittest 自动发现");
        Console.WriteLine("  python -m pytest -v                 # pytest 运行 (推荐)");
        Console.WriteLine("  python -m pytest -k \"test_add\"      # 按名称过滤");
        Console.WriteLine();
        Console.WriteLine("C# 测试命令:");
        Console.WriteLine("  dotnet test                         # 运行所有测试");
        Console.WriteLine("  dotnet test --filter \"ClassName~CalculatorTests\"");
        Console.WriteLine("  dotnet test --filter \"FullyQualifiedName~Add\"");
        Console.WriteLine("  dotnet test --logger \"console;verbosity=detailed\"");
        Console.WriteLine();
        Console.WriteLine("测试框架选择:");
        Console.WriteLine("  框架      风格          Python 等价");
        Console.WriteLine("  --------|-------------|-------------");
        Console.WriteLine("  MSTest   属性+面向对象  unittest");
        Console.WriteLine("  xUnit    约定+简洁     pytest");
        Console.WriteLine("  NUnit    属性+灵活     pytest + 插件");

        // =============================================================
        // 8. MSTest vs xUnit vs NUnit
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("8. MSTest vs xUnit vs NUnit");
        Console.WriteLine("============================================================");
        Console.WriteLine();
        Console.WriteLine("特性          MSTest           xUnit             NUnit");
        Console.WriteLine("------------|----------------|-----------------|----------------");
        Console.WriteLine("测试标记     [TestMethod]    [Fact]            [Test]");
        Console.WriteLine("参数化       [DataRow]       [Theory]+[Inline]  [TestCase]");
        Console.WriteLine("初始化       [TestInitialize] 构造函数          [SetUp]");
        Console.WriteLine("清理         [TestCleanup]    Dispose           [TearDown]");
        Console.WriteLine("类初始化     [ClassInitialize] IClassFixture    [OneTimeSetUp]");
        Console.WriteLine("跳过         [Ignore]        [Fact(Skip=...)]  [Ignore]");
        Console.WriteLine("异常测试     Assert.Throws    Assert.Throws     Assert.Throws");
        Console.WriteLine("并行执行     需配置          默认并行          需配置");
        Console.WriteLine();
        Console.WriteLine("Python 对比:");
        Console.WriteLine("  pytest    ≈  xUnit (简洁，默认并行)");
        Console.WriteLine("  unittest  ≈  MSTest (面向对象，内置)");

        // =============================================================
        // 9. 单元测试最佳实践总结
        // =============================================================
        Console.WriteLine();
        Console.WriteLine("============================================================");
        Console.WriteLine("9. 单元测试最佳实践总结");
        Console.WriteLine("============================================================");
        Console.WriteLine();
        Console.WriteLine("C# vs Python 单元测试对比:");
        Console.WriteLine("  C# [TestMethod]              ≈  Python def test_xxx");
        Console.WriteLine("  C# Assert.AreEqual            ≈  Python self.assertEqual");
        Console.WriteLine("  C# Assert.Throws<T>           ≈  Python self.assertRaises(T)");
        Console.WriteLine("  C# [TestInitialize]           ≈  Python setUp");
        Console.WriteLine("  C# [TestCleanup]              ≈  Python tearDown");
        Console.WriteLine("  C# [DataRow]                  ≈  Python @pytest.mark.parametrize");
        Console.WriteLine("  C# Moq                       ≈  Python unittest.mock");
        Console.WriteLine("  C# [Conditional(\"DEBUG\")]    ≈  Python @unittest.skipIf");
        Console.WriteLine("  C# xUnit                     ≈  Python pytest");
        Console.WriteLine();
        Console.WriteLine("最佳实践 (C# 和 Python 通用):");
        Console.WriteLine("  1. AAA 模式: Arrange → Act → Assert");
        Console.WriteLine("  2. 每个测试方法只测试一个行为");
        Console.WriteLine("  3. 测试名称清晰: Method_Scenario_Expected");
        Console.WriteLine("     Python: test_add_positive_numbers_returns_sum");
        Console.WriteLine("     C#:     Add_PositiveNumbers_ReturnsSum");
        Console.WriteLine("  4. 使用 Mock 隔离外部依赖");
        Console.WriteLine("  5. 测试正常路径和异常路径");
        Console.WriteLine("  6. 保持测试独立性");
        Console.WriteLine("  7. 核心逻辑测试覆盖率 > 80%");
        Console.WriteLine("  8. 避免测试实现细节，测试行为");

        Console.WriteLine();
        Console.WriteLine("所有单元测试示例运行完毕！");
    }

    // =============================================================
    // 辅助方法 — 模拟 Assert
    // =============================================================
    static void AssertEqual(string testName, object expected, object actual)
    {
        bool pass = expected?.ToString() == actual?.ToString();
        Console.WriteLine($"  {(pass ? "[PASS]" : "[FAIL]")} {testName}: 期望={expected}, 实际={actual}");
    }

    static void AssertTrue(string testName, bool condition)
    {
        Console.WriteLine($"  {(condition ? "[PASS]" : "[FAIL]")} {testName}: 期望=True, 实际={condition}");
    }

    static void AssertFalse(string testName, bool condition)
    {
        Console.WriteLine($"  {!condition ? "[PASS]" : "[FAIL]"} {testName}: 期望=False, 实际={condition}");
    }

    static void AssertNotNull(string testName, object? obj)
    {
        Console.WriteLine($"  {obj != null ? "[PASS]" : "[FAIL]"} {testName}: 不应为 null");
    }

    static void AssertContains<T>(string testName, IEnumerable<T> collection, T item)
    {
        bool found = collection.Contains(item);
        Console.WriteLine($"  {found ? "[PASS]" : "[FAIL]"} {testName}: 集合中包含 {item}");
    }
}

// =============================================================
// 被测试的类
// =============================================================

/// <summary>
/// 计算器类
/// Python 等价：
///   class Calculator:
///       def add(self, a, b): return a + b
/// </summary>
public class Calculator
{
    public List<(string Op, double A, double B, double Result)> History { get; } = new();

    public double Add(double a, double b)
    {
        double result = a + b;
        History.Add(("add", a, b, result));
        return result;
    }

    public double Subtract(double a, double b)
    {
        double result = a - b;
        History.Add(("subtract", a, b, result));
        return result;
    }

    public double Multiply(double a, double b)
    {
        double result = a * b;
        History.Add(("multiply", a, b, result));
        return result;
    }

    public double Divide(double a, double b)
    {
        if (b == 0) throw new DivideByZeroException("除数不能为零");
        double result = a / b;
        History.Add(("divide", a, b, result));
        return result;
    }

    public static bool IsPositive(double n) => n > 0;
}

// =============================================================
// 用于演示 Mock 的类
// =============================================================

/// <summary>
/// 用户类
/// </summary>
public class User
{
    public string Name { get; set; } = "";
    public string Email { get; set; } = "";
}

/// <summary>
/// 简化的 Mock 数据库（实际项目中使用 Moq / NSubstitute）
/// Python 等价：
///   mock_db = MagicMock()
///   mock_db.find_user.return_value = {"name": "Alice"}
/// </summary>
public class MockDatabase
{
    public Dictionary<int, User> Users { get; } = new();
    public int FindUserCallCount { get; private set; }

    public User? FindUser(int userId)
    {
        FindUserCallCount++;
        Users.TryGetValue(userId, out var user);
        return user;
    }

    public void SaveUser(User user) { /* 模拟保存 */ }
    public int CountUsers() => Users.Count;
}

/// <summary>
/// 用户服务
/// Python 等价：
///   class UserService:
///       def __init__(self, db=None):
///           self.db = db
///       def get_user(self, user_id):
///           return self.db.find_user(user_id)
/// </summary>
public class UserService
{
    private readonly MockDatabase _db;

    public UserService(MockDatabase db)
    {
        _db = db;
    }

    public User GetUser(int userId)
    {
        var user = _db.FindUser(userId);
        if (user == null)
            throw new ArgumentException($"用户 {userId} 不存在");
        return user;
    }

    public User CreateUser(string name, string email)
    {
        if (string.IsNullOrEmpty(name) || string.IsNullOrEmpty(email))
            throw new ArgumentException("名字和邮箱不能为空");
        var user = new User { Name = name, Email = email };
        _db.SaveUser(user);
        return user;
    }

    public int GetUserCount() => _db.CountUsers();
}
