"""Flows referenced by serve, Python deployments, and prefect.yaml."""

from prefect import flow, get_run_logger


@flow(name="scheduled-report")
def scheduled_report(report_date: str = "today") -> str:
    get_run_logger().info("report_date=%s", report_date)
    return f"report:{report_date}"
