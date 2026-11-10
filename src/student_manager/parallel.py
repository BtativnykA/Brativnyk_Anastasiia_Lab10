"""Threading and multiprocessing implementations."""

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path
from threading import Lock

from student_manager.analytics import grade_score

# --- Threading (корисно для I/O-bound) ---


def calculate_scores_threads(grades: list[float], workers: int = 4) -> list[float]:
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(grade_score, grades))


def load_files_parallel(paths: list[Path]) -> list[str]:
    """I/O-bound task: read multiple files in parallel."""

    def read_file(p: Path) -> str:
        return p.read_text(encoding="utf-8")

    with ThreadPoolExecutor(max_workers=8) as executor:
        return list(executor.map(read_file, paths))


# --- Multiprocessing (корисно для CPU-bound) ---


def calculate_scores_processes(grades: list[float], workers: int = 4) -> list[float]:
    with ProcessPoolExecutor(max_workers=workers) as executor:
        # chunksize зменшує overhead передачі даних між процесами
        return list(executor.map(grade_score, grades, chunksize=100))


# --- Synchronization ---

_counter = 0
_counter_lock = Lock()


def increment_counter_safe():
    """Safely increment global counter using Lock."""
    global _counter
    with _counter_lock:
        _counter += 1
