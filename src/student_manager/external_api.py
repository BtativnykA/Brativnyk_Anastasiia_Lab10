"""External API client demonstrating async features."""

import asyncio

import httpx


async def fetch_group_stat(
    group_id: int, client: httpx.AsyncClient, semaphore: asyncio.Semaphore
) -> dict:
    """Fetch stats for one group, with Semaphore limit and retry."""
    async with semaphore:
        for attempt in range(3):  # Retry logic
            try:
                url = f"http://127.0.0.1:8000/groups/{group_id}/statistics"
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
            except (httpx.RequestError, httpx.HTTPStatusError):
                if attempt == 2:
                    raise  # Остання спроба, піднімаємо помилку
                await asyncio.sleep(attempt + 1)  # Backoff


async def fetch_many_stats(group_ids: list[int]) -> list[dict]:
    """Fetch stats concurrently using Task, gather, and Semaphore."""
    semaphore = asyncio.Semaphore(3)  # Максимум 3 одночасних запити
    async with httpx.AsyncClient(timeout=5.0) as client:
        # Створюємо Task для кожної групи
        tasks = [
            asyncio.create_task(fetch_group_stat(gid, client, semaphore))
            for gid in group_ids
        ]
        # Запускаємо всі паралельно і чекаємо результати
        results = await asyncio.gather(*tasks)
        return list(results)
