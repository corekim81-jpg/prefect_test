import pytest
from prefect.testing.utilities import prefect_test_harness


@pytest.fixture(scope="session", autouse=True)
def isolated_prefect_api():  # type: ignore[no-untyped-def]
    """Run every test against a temporary Prefect API and database."""
    with prefect_test_harness():
        yield
