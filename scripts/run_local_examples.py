"""Run examples that need no preconfigured persistent API objects."""

import asyncio

from prefect_examples.async_workflows import async_flow
from prefect_examples.basics import hello_flow
from prefect_examples.concurrency_mapping import mapping_flow
from prefect_examples.observability import observable_flow
from prefect_examples.resilience import resilient_flow
from prefect_examples.states_and_hooks import state_flow
from prefect_examples.transactions import transactional_flow


def main() -> None:
    print("basics:", hello_flow())
    print("mapping:", mapping_flow())
    print("async:", asyncio.run(async_flow()))
    print("resilience:", resilient_flow())
    print("states:", state_flow())
    observable_flow()
    print("transactions:", transactional_flow())


if __name__ == "__main__":
    main()
