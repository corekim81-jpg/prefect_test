"""Structured run logging and UI artifacts."""

from prefect import flow, get_run_logger, task
from prefect.artifacts import create_link_artifact, create_markdown_artifact, create_table_artifact


@task(log_prints=True)
def analyze() -> list[dict[str, object]]:
    print("print도 Prefect 로그로 캡처됩니다")
    return [
        {"metric": "rows", "value": 1200},
        {"metric": "invalid", "value": 3},
    ]


@flow(name="observable-report")
def observable_flow() -> None:
    logger = get_run_logger()
    rows = analyze()
    logger.info("분석 완료", extra={"row_count": len(rows)})
    create_markdown_artifact(
        key="quality-report",
        markdown="# 품질 보고서\n\n검증이 **완료**되었습니다.",
        description="실행별 Markdown 요약",
    )
    create_table_artifact(key="quality-metrics", table=rows, description="품질 지표")
    create_link_artifact(
        key="prefect-docs",
        link="https://docs.prefect.io/v3/get-started",
        description="Prefect 공식 문서",
    )


if __name__ == "__main__":
    observable_flow()
