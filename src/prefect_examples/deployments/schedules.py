"""Cron, interval, and RRule schedules on one served deployment."""

from prefect.schedules import Cron, Interval, RRule

from prefect_examples.deployments.flows import scheduled_report

if __name__ == "__main__":
    scheduled_report.serve(
        name="multiple-schedules",
        schedules=[
            Cron(
                "0 9 * * 1-5",
                timezone="Asia/Seoul",
                parameters={"report_date": "weekday-cron"},
                slug="weekday-cron",
            ),
            Interval(
                3600,
                parameters={"report_date": "hourly"},
                slug="hourly-interval",
            ),
            RRule(
                "FREQ=MONTHLY;BYMONTHDAY=1;BYHOUR=9",
                timezone="Asia/Seoul",
                parameters={"report_date": "monthly-rrule"},
                slug="monthly-rrule",
            ),
        ],
        tags=["demo", "schedules"],
    )
