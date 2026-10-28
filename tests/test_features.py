import asyncio

from prefect_examples.assets import asset_flow
from prefect_examples.async_workflows import async_flow
from prefect_examples.automations import build_demo_automation
from prefect_examples.observability import observable_flow
from prefect_examples.states_and_hooks import state_flow
from prefect_examples.transactions import transactional_flow


def test_async_flow() -> None:
    assert asyncio.run(async_flow([1, 2])) == [
        {"id": 1, "value": 10},
        {"id": 2, "value": 20},
    ]


def test_automation_model() -> None:
    automation = build_demo_automation()
    assert automation.name == "demo-order-processed"


def test_asset_flow() -> None:
    assert asset_flow() == [{"id": 1, "amount": 100}]


def test_observability_flow() -> None:
    assert observable_flow() is None


def test_state_flow_handles_failure() -> None:
    assert state_flow() == "성공: 5.0"
    assert state_flow(fail=True).startswith("처리된 실패:")


def test_transactional_flow() -> None:
    assert transactional_flow("row-test") == "row-test"
