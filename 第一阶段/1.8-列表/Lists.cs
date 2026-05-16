// C# 列表操作示例
// 对应文章：1.8 列表与数组

using System;
using System.Collections.Generic;
using System.Linq;

// ==================== 数组（固定大小）====================
Console.WriteLine("=== 数组 vs List ===");
int[] arr1 = { 1, 2, 3 };              // 数组（固定大小）
int[] arr2 = new int[5];               // 默认值为 0
Console.WriteLine($"数组: [{string.Join(", ", arr1)}]");

// List（动态大小，类似 Python 的 list）
List<int> list1 = new() { 1, 2, 3 };
List<int> list2 = new List<int>();     // 空列表
Console.WriteLine($"List: [{string.Join(", ", list1)}]");

// ==================== 添加元素 ====================
Console.WriteLine("\n=== 添加元素 ===");
list1.Add(6);                          // 添加到末尾
list1.Insert(0, 0);                    // 插入到指定位置
list1.AddRange(new[] { 7, 8 });        // 添加多个
Console.WriteLine($"操作后: [{string.Join(", ", list1)}]");

// ==================== 删除元素 ====================
Console.WriteLine("\n=== 删除元素 ===");
list1.Remove(6);                       // 删除第一个匹配项
list1.RemoveAt(0);                     // 删除指定索引
list1.RemoveAll(x => x > 7);          // 删除所有匹配项
Console.WriteLine($"操作后: [{string.Join(", ", list1)}]");

// ==================== 查找 ====================
Console.WriteLine("\n=== 查找 ===");
var nums = new List<int> { 10, 20, 30, 40, 50 };
int index = nums.IndexOf(30);          // 查找索引: 2
bool exists = nums.Contains(30);       // 是否包含: true
Console.WriteLine($"IndexOf(30) = {index}");
Console.WriteLine($"Contains(30) = {exists}");

// ==================== 排序和反转 ====================
Console.WriteLine("\n=== 排序和反转 ===");
var sortList = new List<int> { 3, 1, 4, 1, 5, 9, 2, 6 };
sortList.Sort();                       // 排序（原地）
Console.WriteLine($"Sort(): [{string.Join(", ", sortList)}]");
sortList.Reverse();                    // 反转（原地）
Console.WriteLine($"Reverse(): [{string.Join(", ", sortList)}]");

// 带比较器排序
var words = new List<string> { "banana", "apple", "cherry" };
words.Sort((a, b) => a.Length.CompareTo(b.Length));
Console.WriteLine($"按长度排序: [{string.Join(", ", words)}]");

// ==================== 切片 ====================
Console.WriteLine("\n=== 切片（C# 8.0+ Range）===");
var sliceList = Enumerable.Range(0, 10).ToList();
var sub = sliceList.GetRange(1, 3);     // 传统方式：从索引1开始取3个
var rangeSub = sliceList[1..4];          // C# 8.0+ 方式
Console.WriteLine($"GetRange(1,3): [{string.Join(", ", sub)}]");
Console.WriteLine($"[1..4]:        [{string.Join(", ", rangeSub)}]");

// ==================== LINQ（等价于 Python 列表推导式）====================
Console.WriteLine("\n=== LINQ ===");
var numbers = new List<int> { 1, 2, 3, 4, 5 };
var squares = numbers.Select(x => x * x).ToList();           // 平方
var even = numbers.Where(x => x % 2 == 0).ToList();          // 偶数
int sum = numbers.Sum();
double avg = numbers.Average();
Console.WriteLine($"平方: [{string.Join(", ", squares)}]");
Console.WriteLine($"偶数: [{string.Join(", ", even)}]");
Console.WriteLine($"求和: {sum}, 平均: {avg}");

// ==================== 浅拷贝 vs 深拷贝 ====================
Console.WriteLine("\n=== 浅拷贝 vs 深拷贝 ===");
var original = new List<List<int>> { new() { 1, 2 }, new() { 3, 4 } };
var shallow = new List<List<int>>(original);  // 浅拷贝
shallow[0][0] = 999;
Console.WriteLine($"浅拷贝修改后 original[0][0] = {original[0][0]}");  // 999（被影响！）

var deep = original.Select(x => new List<int>(x)).ToList();  // 深拷贝
deep[0][0] = 1;
Console.WriteLine($"深拷贝修改后 original[0][0] = {original[0][0]}");  // 999（不受影响）
