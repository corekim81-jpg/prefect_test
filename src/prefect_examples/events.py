"""Emit custom events with resources and related resources."""

from prefect import flow
from prefect.events import RelatedResource, emit_event


@flow
def event_flow(order_id: str = "order-42") -> None:
    emit_event(
        event="demo.order.processed",
        resource={
            "prefect.resource.id": f"demo.order.{order_id}",
            "prefect.resource.name": order_id,
            "demo.status": "processed",
        },
        related=[
            RelatedResource(
                {
                    "prefect.resource.id": "demo.service.orders",
                    "prefect.resource.role": "processor",
                }
            )
        ],
        payload={"order_id": order_id, "items": 3},
    )


if __name__ == "__main__":
    event_flow()
