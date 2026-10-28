"""Transactional task groups with commit and rollback hooks."""

from prefect import flow, task
from prefect.transactions import transaction


@task
def write_record(record_id: str) -> str:
    return record_id


@write_record.on_rollback
def rollback_record(transaction) -> None:  # type: ignore[no-untyped-def]
    print("rollback:", transaction.get("record_id", default="unknown"))


@write_record.on_commit
def commit_record(transaction) -> None:  # type: ignore[no-untyped-def]
    print("commit:", transaction.get("record_id", default="unknown"))


@flow
def transactional_flow(record_id: str = "row-1", fail: bool = False) -> str:
    with transaction(key=f"record-{record_id}") as txn:
        txn.set("record_id", record_id)
        result = write_record(record_id)
        if fail:
            raise RuntimeError("후속 작업 실패: 트랜잭션을 롤백합니다")
    return result


if __name__ == "__main__":
    print(transactional_flow())
