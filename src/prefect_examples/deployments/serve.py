"""Serve a flow from static, long-running infrastructure."""

from prefect_examples.deployments.flows import scheduled_report

if __name__ == "__main__":
    scheduled_report.serve(
        name="static-every-minute",
        interval=60,
        tags=["demo", "serve"],
        parameters={"report_date": "scheduled"},
        global_limit=1,
    )
