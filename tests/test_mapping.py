from prefect_examples.concurrency_mapping import mapping_flow


def test_mapping_flow() -> None:
    assert mapping_flow([1, 2, 3]) == "합계=14"
