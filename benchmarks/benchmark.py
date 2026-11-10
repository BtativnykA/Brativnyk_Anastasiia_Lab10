"""Main benchmarking script comparing all implementations."""

import time
from statistics import mean

from student_manager.analytics import (
    calculate_scores_sequential,
    generate_students,
    statistics_numpy,
    statistics_python,
)
from student_manager.parallel import (
    calculate_scores_processes,
    calculate_scores_threads,
)


def measure_time(func, *args) -> float:
    start = time.perf_counter()
    func(*args)
    return time.perf_counter() - start


def run_benchmark(data_size: int, repeats: int = 3):
    print(f"\n{'=' * 60}")
    print(f" BENCHMARK: {data_size:,} students")
    print(f"{'=' * 60}")

    # 1. Підготовка даних
    students = generate_students(data_size)
    grades = [s["grade"] for s in students]

    # 2. Python Baseline (Статистика)
    times = [measure_time(statistics_python, grades) for _ in range(repeats)]
    base_time = mean(times)
    print(f"1. Python Baseline (Stats):  {base_time:8.4f} s | Speedup: 1.00x")

    # 3. NumPy (Статистика)
    times = [measure_time(statistics_numpy, grades) for _ in range(repeats)]
    np_time = mean(times)
    print(
        f"2. NumPy Vectorization:      {np_time:8.4f} s | Speedup: {base_time / np_time:5.2f}x"
    )

    # Перевірка правильності
    res_py = statistics_python(grades)
    res_np = statistics_numpy(grades)
    assert abs(res_py["average"] - res_np["average"]) < 1e-9, "Results mismatch!"
    print("   [Validation] NumPy results match Python baseline. OK.")

    # 4. Тестування CPU-bound (Threading vs Multiprocessing)
    print("\n--- CPU-bound Task (Heavy Loop) ---")

    # Sequential
    times = [measure_time(calculate_scores_sequential, grades) for _ in range(repeats)]
    seq_time = mean(times)
    print(f"3. Sequential (Baseline):    {seq_time:8.4f} s | Speedup: 1.00x")

    # Threads (GIL limitation)
    times = [measure_time(calculate_scores_threads, grades, 4) for _ in range(repeats)]
    thread_time = mean(times)
    print(
        f"4. ThreadPoolExecutor (4w):  {thread_time:8.4f} s | Speedup: {seq_time / thread_time:5.2f}x"
    )

    # Processes (True parallelism)
    times = [
        measure_time(calculate_scores_processes, grades, 4) for _ in range(repeats)
    ]
    proc_time = mean(times)
    print(
        f"5. ProcessPoolExecutor (4w): {proc_time:8.4f} s | Speedup: {seq_time / proc_time:5.2f}x"
    )


if __name__ == "__main__":
    # Досліджуємо різні розміри даних
    run_benchmark(10_000)
    run_benchmark(100_000)
