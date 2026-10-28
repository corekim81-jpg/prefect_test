"""Global concurrency slots and rate limits (requires a persistent API server)."""

import time

from prefect import flow, task
from prefect.concurrency.sync import concurrency, rate_limit


@task
def limited_database_write(value: int) -> int:
    # 먼저 실행: prefect gcl create database-writes --limit 2
    with concurrency("database-writes", occupy=1):
        time.sleep(0.1)
        return value


@task
def rate_limited_request(value: int) -> int:
    # 먼저 실행: prefect gcl create external-api --limit 5 --slot-decay-per-second 1
    rate_limit("external-api", occupy=1)
    return value


@flow
def limits_flow() -> list[int]:
    writes = limited_database_write.map(range(4))
    requests = rate_limited_request.map(range(4, 8))
    return [future.result() for future in [*writes, *requests]]


if __name__ == "__main__":
    print(limits_flow())
