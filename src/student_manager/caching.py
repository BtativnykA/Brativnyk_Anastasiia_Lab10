"""Caching implementation with invalidation strategy."""

from functools import lru_cache

# Глобальний лічильник версії даних для інвалідації кешу
DATA_VERSION = 1


@lru_cache(maxsize=128)
def get_group_statistics_cached(group_id: int, version: int) -> float:
    """
    Cached group average.
    `version` parameter ensures invalidation when data changes.
    """
    # Тут у реальному проєкті був би запит до БД
    # Імітуємо важке обчислення:
    import time

    time.sleep(0.5)  # Штучна затримка (I/O)
    return 85.0 + (group_id % 10) + version


def invalidate_cache():
    """Clear cache when data changes."""
    global DATA_VERSION
    DATA_VERSION += 1
    get_group_statistics_cached.cache_clear()
    return DATA_VERSION
