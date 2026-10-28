"""Pause for typed human input and suspend a run (server/UI required)."""

from prefect import flow, get_run_logger
from prefect.flow_runs import pause_flow_run, suspend_flow_run
from pydantic import BaseModel, Field


class Approval(BaseModel):
    approved: bool = Field(description="계속 진행할지 선택")
    reviewer: str = Field(description="검토자 이름")
    comment: str = ""


@flow
def approval_flow(suspend_first: bool = False) -> str:
    if suspend_first:
        # suspend는 현재 프로세스를 종료하고 배포 인프라에서 재개합니다.
        suspend_flow_run(timeout=3600)
    approval = pause_flow_run(wait_for_input=Approval, timeout=3600)
    get_run_logger().info("reviewer=%s, comment=%s", approval.reviewer, approval.comment)
    return "approved" if approval.approved else "rejected"


if __name__ == "__main__":
    print(approval_flow())
