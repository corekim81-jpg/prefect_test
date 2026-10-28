"""Register a deployment for a Process work pool."""

from prefect_examples.deployments.flows import scheduled_report

if __name__ == "__main__":
    deployment_id = scheduled_report.from_source(
        source=".",
        entrypoint="src/prefect_examples/deployments/flows.py:scheduled_report",
    ).deploy(
        name="process-worker",
        work_pool_name="local-process",
        cron="0 9 * * 1-5",
        tags=["demo", "worker"],
        parameters={"report_date": "weekday"},
        version="0.1.0",
    )
    print(deployment_id)
