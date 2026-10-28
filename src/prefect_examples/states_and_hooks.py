"""States, return_state, failure handling, and lifecycle hooks."""

from typing import Any

from prefect import Flow, Task, flow, task
from prefect.client.schemas import FlowRun, TaskRun
from prefect.states import State


def flow_finished(flow: Flow[Any, Any], flow_run: FlowRun, state: State) -> None:
    print(f"flow hook: {flow.name} / {flow_run.name} -> {state.name}")


def task_failed(task: Task[Any, Any], task_run: TaskRun, state: State) -> None:
    print(f"task hook: {task.name} / {task_run.name} -> {state.message}")


@task(on_failure=[task_failed])
def divide(numerator: float, denominator: float) -> float:
    return numerator / denominator


@flow(on_completion=[flow_finished])
def state_flow(fail: bool = False) -> str:
    state = divide(10, 0 if fail else 2, return_state=True)
    if state.is_failed():
        return f"처리된 실패: {state.message}"
    return f"성공: {state.result()}"


if __name__ == "__main__":
    print(state_flow())
    print(state_flow(fail=True))
