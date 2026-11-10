"""Analytics, baseline Python loops, and NumPy vectorization."""

from __future__ import annotations

import math
import random

import numpy as np


def generate_students(count: int) -> list[dict]:
    """Generate a large list of student dictionaries."""
    random.seed(42)
    groups = ["PI-21", "PI-22", "PI-23", "PI-24"]
    return [
        {"id": i, "group": random.choice(groups), "grade": random.uniform(60.0, 100.0)}
        for i in range(count)
    ]


def grade_score(grade: float) -> float:
    """Heavy CPU-bound operation to demonstrate multiprocessing benefits."""
    value = grade
    for _ in range(50):  # Штучне навантаження
        value = math.sin(value) ** 2 + math.cos(value) ** 2 + math.sqrt(abs(value) + 1)
    return value


def calculate_scores_sequential(grades: list[float]) -> list[float]:
    """Baseline: Sequential Python loop."""
    return [grade_score(g) for g in grades]


def statistics_python(grades: list[float]) -> dict[str, float]:
    """Baseline: Pure Python statistics with standard deviation loop."""
    count = len(grades)
    total = sum(grades)
    average = total / count
    minimum = min(grades)
    maximum = max(grades)

    variance = sum((x - average) ** 2 for x in grades) / count
    std_dev = math.sqrt(variance)

    return {"average": average, "minimum": minimum, "maximum": maximum, "std": std_dev}


def statistics_numpy(grades: list[float]) -> dict[str, float]:
    """Optimized: NumPy vectorization."""
    arr = np.asarray(grades, dtype=np.float64)
    return {
        "average": float(arr.mean()),
        "minimum": float(arr.min()),
        "maximum": float(arr.max()),
        "std": float(arr.std()),
    }
