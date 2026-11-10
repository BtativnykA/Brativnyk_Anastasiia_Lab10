"""Profiling tools: cProfile and tracemalloc."""

import cProfile
import pstats
import tracemalloc

from student_manager.analytics import generate_students, statistics_python


def profile_memory():
    """Analyze peak memory usage."""
    tracemalloc.start()

    students = generate_students(100_000)
    grades = [s["grade"] for s in students]
    statistics_python(grades)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"[Memory] Current: {current / 1024 / 1024:.2f} MB")
    print(f"[Memory] Peak:    {peak / 1024 / 1024:.2f} MB")


def profile_time():
    """Run cProfile to find bottlenecks."""
    students = generate_students(100_000)
    grades = [s["grade"] for s in students]

    profiler = cProfile.Profile()
    profiler.enable()

    statistics_python(grades)

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats("cumulative").print_stats(10)


if __name__ == "__main__":
    profile_memory()
    profile_time()
