"""Retries, retry delay, caching, cache keys, and persisted results."""

from datetime import timedelta

from prefect import flow, task
from prefect.cache_policies import INPUTS, TASK_SOURCE
from prefect.tasks import exponential_backoff

attempts = 0


@task(
    retries=3,
    retry_delay_seconds=exponential_backoff(backoff_factor=0.1),
    retry_jitter_factor=0.1,
)
def flaky_service() -> str:
    global attempts
    attempts += 1
    if attempts < 2:
        raise RuntimeError("일시적인 오류")
    return "recovered"


@task(
    cache_policy=INPUTS + TASK_SOURCE,
    cache_expiration=timedelta(minutes=10),
    persist_result=True,
)
def expensive(value: int) -> int:
    return value**3


@flow(persist_result=True)
def resilient_flow(value: int = 4) -> dict[str, object]:
    return {"service": flaky_service(), "computed": expensive(value)}


if __name__ == "__main__":
    print(resilient_flow())
