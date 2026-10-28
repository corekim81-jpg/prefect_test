from prefect_examples.basics import hello_flow


def test_hello_flow() -> None:
    assert hello_flow([" kim "], excited=True) == ["안녕하세요, Kim!"]
