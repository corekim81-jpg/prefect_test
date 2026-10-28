"""Read orchestration data with Prefect's asynchronous client."""

import asyncio

from prefect.client.orchestration import get_client


async def list_recent_flow_runs(limit: int = 10) -> None:
    async with get_client() as client:
        flows = await client.read_flows(limit=limit)
        runs = await client.read_flow_runs(limit=limit)
        print("flows:", [(flow.name, str(flow.id)) for flow in flows])
        print("runs:", [(run.name, run.state_name) for run in runs])


if __name__ == "__main__":
    asyncio.run(list_recent_flow_runs())
