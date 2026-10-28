"""Flow, task, parameters, subflows, and native Python branching."""

from prefect import flow, get_run_logger, task


@task(name="normalize-name", description="문자열을 정규화합니다", tags={"cpu"})
def normalize(name: str) -> str:
    return name.strip().title()


@task
def greeting(name: str, excited: bool = False) -> str:
    suffix = "!" if excited else "."
    return f"안녕하세요, {name}{suffix}"


@flow(name="audit-subflow")
def audit(message: str) -> None:
    get_run_logger().info("감사 로그: %s", message)


@flow(name="hello-prefect", log_prints=True)
def hello_flow(names: list[str] | None = None, excited: bool = True) -> list[str]:
    """Task를 일반 함수처럼 호출하고 서브플로우를 조합합니다."""
    names = names or ["  kim  ", "lee"]
    messages: list[str] = []
    for raw_name in names:  # DAG DSL 대신 네이티브 Python 제어 흐름을 사용합니다.
        name = normalize(raw_name)
        message = greeting(name, excited=excited)
        audit(message)
        messages.append(message)
    print(messages)
    return messages


if __name__ == "__main__":
    hello_flow()
