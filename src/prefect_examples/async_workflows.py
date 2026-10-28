"""Native async/await workflows."""

import asyncio

from prefect import flow, task


@task
async def fetch_item(item_id: int) -> dict[str, int]:
    await asyncio.sleep(0.05)
    return {"id": item_id, "value": item_id * 10}


@flow
async def async_flow(item_ids: list[int] | None = None) -> list[dict[str, int]]:
    item_ids = item_ids or [1, 2, 3]
    futures = [fetch_item.submit(item_id) for item_id in item_ids]
    # submit된 PrefectFuture의 result()는 완료 시점까지 기다린 뒤 값을 반환합니다.
    return [future.result() for future in futures]


if __name__ == "__main__":
    print(asyncio.run(async_flow()))
