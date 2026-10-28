"""Create an event-driven automation in the active Prefect API."""

from prefect.automations import Automation, DoNothing, EventTrigger


def build_demo_automation() -> Automation:
    """Build an automation that reacts to the custom event emitted by events.py.

    DoNothing makes this example safe. Replace it with RunDeployment,
    SendNotification, CallWebhook, PauseWorkPool, etc. for production use.
    """
    return Automation(
        name="demo-order-processed",
        description="demo.order.processed 이벤트를 감지하는 안전한 자동화 예제",
        tags=["demo"],
        trigger=EventTrigger(
            expect={"demo.order.processed"},
            match={"prefect.resource.id": "demo.order.*"},
            threshold=1,
        ),
        actions=[DoNothing()],
    )


def create_demo_automation() -> Automation:
    automation = build_demo_automation()
    automation.create()
    return automation


if __name__ == "__main__":
    print(create_demo_automation().id)
