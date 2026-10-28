"""Blocks, encrypted secrets, and Variables (requires a persistent API server)."""

from prefect import flow
from prefect.blocks.core import Block
from prefect.blocks.system import Secret
from prefect.variables import Variable


class DemoSettings(Block):
    """사용자 정의 typed block 예제."""

    region: str
    retries: int = 3
    environment: str = "development"


def create_demo_configuration() -> None:
    """Create or overwrite demo configuration in the active Prefect API."""
    Secret(value="replace-me").save("demo-api-key", overwrite=True)
    DemoSettings(region="ap-northeast-2").save("demo-settings", overwrite=True)
    Variable.set("demo-feature-flag", True, overwrite=True)


@flow
def read_configuration() -> dict[str, object]:
    secret = Secret.load("demo-api-key")
    settings = DemoSettings.load("demo-settings")
    return {
        "secret_length": len(secret.get()),  # 비밀 자체는 로그에 남기지 않습니다.
        "settings": settings.model_dump(),
        "environment": settings.environment,
        "feature_flag": Variable.get("demo-feature-flag", default=False),
    }


if __name__ == "__main__":
    create_demo_configuration()
    print(read_configuration())
