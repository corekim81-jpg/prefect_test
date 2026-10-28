import prefect_examples.resilience as example


def test_resilient_flow() -> None:
    example.attempts = 0
    assert example.resilient_flow(3) == {"service": "recovered", "computed": 27}
