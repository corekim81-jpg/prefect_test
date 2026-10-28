"""Asset dependencies and materialization metadata."""

from prefect import flow, task
from prefect.assets import Asset, AssetProperties, materialize

raw_orders = Asset(key="demo://raw-orders")
clean_orders = Asset(
    key="demo://clean-orders",
    properties=AssetProperties(description="정제된 주문 데이터", owners=["demo-team"]),
)


@task
def extract() -> list[dict[str, int]]:
    return [{"id": 1, "amount": 100}, {"id": 2, "amount": -1}]


@materialize(raw_orders)
def materialize_raw() -> list[dict[str, int]]:
    return extract()


@materialize(clean_orders)
def materialize_clean(rows: list[dict[str, int]]) -> list[dict[str, int]]:
    return [row for row in rows if row["amount"] >= 0]


@flow
def asset_flow() -> list[dict[str, int]]:
    return materialize_clean(materialize_raw())


if __name__ == "__main__":
    print(asset_flow())
