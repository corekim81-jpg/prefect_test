from prefect import flow


def test_isolated_prefect_api() -> None:
    @flow
    def answer() -> int:
        return 42

    # conftest.py의 harness가 실제 환경의 실행 기록을 오염시키지 않도록 격리합니다.
    assert answer() == 42
