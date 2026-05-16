# =============================================================================
# Python 多线程与 GIL 示例 — C# 老兵的 Python 修炼手册 5.2
# 对应文章：5.2 多线程与GIL
# 关键概念：threading, GIL限制, multiprocessing, concurrent.futures,
#           asyncio vs threading vs multiprocessing
# =============================================================================
# 【C# vs Python 对比 — 最大的差异之一】
#
# C# 没有 GIL（全局解释器锁），线程可以真正并行执行 CPU 密集型任务
# Python 有 GIL，同一时刻只有一个线程执行 Python 字节码
#
# C# 多线程: Task.Run(() => { ... }) -> 线程池中的真实并行
# Python 多线程: threading.Thread(target=fn) -> 受 GIL 限制的并发
#
# 结论: Python CPU 密集型任务用 multiprocessing，I/O 密集型用 asyncio
# =============================================================================

import threading
import multiprocessing
import concurrent.futures
import time
import sys
from typing import List


# =============================================================================
# 1. GIL 是什么？—— 全局解释器锁
# =============================================================================
# GIL (Global Interpreter Lock) 是 CPython 解释器中的一个互斥锁，
# 保证同一时刻只有一个线程执行 Python 字节码。
#
# 【C# 对比】C# CLR 没有 GIL，每个线程可以独立执行 JIT 编译的机器码
# 这意味着 C# 的多线程可以真正利用多核 CPU 进行并行计算
#
# 为什么 Python 需要 GIL？
# - CPython 使用引用计数进行内存管理
# - GIL 简化了内存管理，避免了竞态条件
# - 但也意味着 CPU 密集型任务无法通过多线程加速


def demo_what_is_gil():
    """解释 GIL 的概念"""
    print("\n=== 1. 什么是 GIL ===")
    print(f"  Python 实现: {sys.implementation.name}")
    print(f"  Python 版本: {sys.version}")
    print(f"  GIL 存在: 是 (仅 CPython，PyPy 有 GIL-free 模式)")
    print(f"  【C# 对比】C# CLR 没有 GIL，线程可以真正并行")
    print(f"  Python 3.12+ 有 PEP 684 子解释器独立 GIL (实验性)")
    print(f"  Python 3.13+ 支持 free-threaded 模式 (实验性)")


# =============================================================================
# 2. threading 模块 —— I/O 密集型任务
# =============================================================================
# 【C# 对比】
# C#: Task.Run(() => DoWork()) 或 new Thread(() => DoWork()).Start()
# Python: threading.Thread(target=func).start()
#
# 两者都能用于 I/O 密集型任务（网络请求、文件读写、数据库查询）
# 因为 I/O 等待期间线程会释放 GIL（Python）或让出 CPU（C#）

shared_counter = 0
counter_lock = threading.Lock()


def increment_shared(n: int) -> None:
    """线程安全的递增操作"""
    global shared_counter
    for _ in range(n):
        # 不加锁会出问题（GIL 不能保证原子操作）
        with counter_lock:
            shared_counter += 1


def demo_threading_basics():
    """演示 threading 基础"""
    print("\n=== 2. threading 模块（I/O 密集型） ===")

    # 【C# 对比】
    # var t1 = new Thread(() => IncrementShared(1000000));
    # var t2 = new Thread(() => IncrementShared(1000000));
    # t1.Start(); t2.Start();
    # t1.Join(); t2.Join();

    n = 1_000_000
    t1 = threading.Thread(target=increment_shared, args=(n,))
    t2 = threading.Thread(target=increment_shared, args=(n,))

    start = time.perf_counter()
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    elapsed = time.perf_counter() - start

    print(f"  两个线程各递增 {n:,} 次")
    print(f"  结果: {shared_counter:,} (期望: {2 * n:,})")
    print(f"  耗时: {elapsed:.3f}s")


# =============================================================================
# 3. GIL 的影响 —— CPU 密集型任务不会加速
# =============================================================================
# 这是 C# 开发者最容易踩的坑！
# 在 C# 中，Parallel.For 会让 CPU 密集型任务加速
# 在 Python 中，threading 反而可能更慢（线程切换开销 + GIL）

def cpu_bound_work(n: int) -> float:
    """CPU 密集型计算"""
    total = 0.0
    for i in range(n):
        total += i ** 0.5
    return total


def demo_gil_limitation():
    """演示 GIL 对 CPU 密集型任务的限制"""
    print("\n=== 3. GIL 限制 — CPU 密集型任务 ===")

    n = 2_000_000

    # 单线程
    start = time.perf_counter()
    r1 = cpu_bound_work(n)
    r2 = cpu_bound_work(n)
    single_time = time.perf_counter() - start
    print(f"  单线程: {single_time:.3f}s (结果: {r1 + r2:.0f})")

    # 多线程（受 GIL 限制，可能不会更快甚至更慢）
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(cpu_bound_work, n) for _ in range(2)]
        results = [f.result() for f in futures]
    threaded_time = time.perf_counter() - start
    print(f"  多线程: {threaded_time:.3f}s (结果: {sum(results):.0f})")

    ratio = single_time / threaded_time if threaded_time > 0 else 0
    if ratio < 1.0:
        print(f"  [GIL 限制] 多线程反而慢了 {1/ratio:.2f}x — GIL 导致!")
    else:
        print(f"  多线程略快 {ratio:.2f}x (I/O 开销可能被 GIL 掩盖)")

    print("  【C# 对比】C# Parallel.For 可以真正加速，因为没有 GIL")


# =============================================================================
# 4. multiprocessing —— 绕过 GIL，真正并行
# =============================================================================
# 【C# 对比】
# C#: Parallel.For(0, 4, i => { results[i] = CpuBound(i); });
#      或 Task.Run(() => CpuBound(i))
#
# Python multiprocessing: 每个子进程有独立的 Python 解释器和 GIL
#                         真正的并行，但进程间通信有开销

def cpu_bound_process(n: int) -> float:
    """在子进程中执行的 CPU 密集型计算"""
    return sum(i ** 0.5 for i in range(n))


def demo_multiprocessing():
    """演示 multiprocessing 绕过 GIL"""
    print("\n=== 4. multiprocessing（绕过 GIL，真正并行） ===")

    n = 2_000_000
    num_workers = 4

    # 单进程
    start = time.perf_counter()
    single_result = sum(cpu_bound_process(n) for _ in range(num_workers))
    single_time = time.perf_counter() - start
    print(f"  单进程 ({num_workers}次串行): {single_time:.3f}s")

    # 多进程
    start = time.perf_counter()
    with multiprocessing.Pool(num_workers) as pool:
        results = pool.map(cpu_bound_process, [n] * num_workers)
    multi_time = time.perf_counter() - start
    print(f"  多进程 ({num_workers}核并行): {multi_time:.3f}s")
    print(f"  加速比: {single_time / multi_time:.2f}x")
    print(f"  【C# 对比】C# 的 Parallel.For 天然支持并行，不需要额外模块")


# =============================================================================
# 5. concurrent.futures —— 统一的并发接口
# =============================================================================
# 【C# 对比】
# C# 的 Task + Task.WhenAll 是统一的异步模型
# Python 的 concurrent.futures 提供 ThreadPoolExecutor 和 ProcessPoolExecutor
#
# ThreadPoolExecutor  → 用于 I/O 密集型（类似 C# Task.Run）
# ProcessPoolExecutor → 用于 CPU 密集型（类似 C# Parallel.For）

def demo_concurrent_futures():
    """演示 concurrent.futures 模块"""
    print("\n=== 5. concurrent.futures（统一并发接口） ===")

    # ThreadPoolExecutor —— I/O 密集型
    # 【C# 对比】Task.WhenAll
    def io_task(task_id: int) -> str:
        time.sleep(0.3)  # 模拟 I/O
        return f"任务{task_id}完成"

    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # 提交多个任务
        futures = {executor.submit(io_task, i): i for i in range(5)}
        for future in concurrent.futures.as_completed(futures):
            task_id = futures[future]
            result = future.result()
            print(f"  {result}")
    io_time = time.perf_counter() - start
    print(f"  I/O 任务总耗时: {io_time:.3f}s (并发执行)")

    # ProcessPoolExecutor —— CPU 密集型
    # 【C# 对比】Parallel.For
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(cpu_bound_process, [500_000] * 2))
    print(f"  CPU 任务结果: [{len(results)} 个子进程完成]")


# =============================================================================
# 6. asyncio vs threading vs multiprocessing —— 选择指南
# =============================================================================

def demo_comparison():
    """对比三种并发模型"""
    print("\n=== 6. asyncio vs threading vs multiprocessing 选择指南 ===")
    print("  ┌─────────────────┬──────────────┬──────────────┬──────────────┐")
    print("  │ 特性            │ asyncio      │ threading    │ multiprocessing │")
    print("  ├─────────────────┼──────────────┼──────────────┼──────────────┤")
    print("  │ GIL 影响        │ 不受影响     │ 受限         │ 不受限       │")
    print("  │ 适用场景        │ I/O 密集     │ I/O 密集     │ CPU 密集     │")
    print("  │ 内存共享        │ 是           │ 是(需加锁)   │ 否(需IPC)    │")
    print("  │ 创建开销        │ 最小         │ 中等         │ 最大         │")
    print("  │ 切换开销        │ 最小         │ 中等         │ 最大         │")
    print("  │ C# 对应         │ async/await  │ Task.Run     │ Parallel.For │")
    print("  └─────────────────┴──────────────┴──────────────┴──────────────┘")


# =============================================================================
# 7. 实际案例：I/O 密集型并发下载
# =============================================================================

def demo_io_concurrent():
    """实际案例：模拟并发下载"""
    print("\n=== 7. 实际案例：I/O 密集型并发 ===")

    def download_page(url: str) -> dict:
        """模拟下载网页"""
        time.sleep(0.2)  # 模拟网络延迟
        return {"url": url, "size": len(url) * 100}

    urls = [f"https://example.com/page{i}" for i in range(10)]

    # 串行
    start = time.perf_counter()
    serial_results = [download_page(url) for url in urls]
    serial_time = time.perf_counter() - start
    print(f"  串行: {serial_time:.3f}s")

    # 并发（threading + futures）
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        parallel_results = list(executor.map(download_page, urls))
    parallel_time = time.perf_counter() - start
    print(f"  并发: {parallel_time:.3f}s (5个线程)")
    print(f"  加速比: {serial_time / parallel_time:.1f}x")


# =============================================================================
# 主程序入口
# =============================================================================

def main():
    """运行所有演示
    
    【C# 对比】
    C#: static void Main() { DemoAll(); }
    Python: main() + if __name__ == "__main__"
    """
    print("=" * 60)
    print("  C# 老兵的 Python 修炼手册 — 5.2 多线程与 GIL")
    print("=" * 60)

    demo_what_is_gil()
    demo_threading_basics()
    demo_gil_limitation()
    demo_multiprocessing()
    demo_concurrent_futures()
    demo_comparison()
    demo_io_concurrent()

    print("\n" + "=" * 60)
    print("  核心结论：")
    print("  1. Python 有 GIL，多线程不能加速 CPU 密集型任务")
    print("  2. CPU 密集型用 multiprocessing，I/O 密集型用 asyncio")
    print("  3. C# 没有 GIL，Task.Run + Parallel.For 可以真正并行")
    print("  4. asyncio 是 Python 处理高并发 I/O 的最佳选择")
    print("=" * 60)


if __name__ == "__main__":
    main()
