"""Task futures, concurrent submission, mapping, and explicit dependencies."""

import time

from prefect import flow, task
from prefect.futures import wait
from prefect.task_runners import ThreadPoolTaskRunner


@task
def square(value: int) -> int:
    time.sleep(0.05)
    return value * value


@task
def total(values: list[int]) -> int:
    return sum(values)


@task
def notify(answer: int) -> str:
    return f"합계={answer}"


@flow(task_runner=ThreadPoolTaskRunner(max_workers=4))
def mapping_flow(values: list[int] | None = None) -> str:
    values = values or [1, 2, 3, 4]

    # map은 각 입력에 대한 PrefectFutureList를 반환합니다.
    mapped = square.map(values)
    wait(mapped)
    results = [future.result() for future in mapped]

    # submit은 즉시 future를 반환하며 runner가 병렬 실행합니다.
    answer_future = total.submit(results)
    message_future = notify.submit(answer_future, wait_for=[*mapped])
    return message_future.result()


if __name__ == "__main__":
    print(mapping_flow())
