# Prefect 3 기능별 실행 예제

Prefect 3의 공개 사용자 기능을 작은 실행 예제로 익히기 위한 저장소입니다. 각 파일은 한 가지 주제에 집중하며, `uv`만 있으면 로컬 임시 Prefect API로 바로 실행할 수 있습니다.

> 기준: Prefect `3.9.x`, Python 3.11 이상. "모든 기능"은 내부 구현용 API가 아닌 공식 문서의 사용자 기능군을 뜻합니다. 클라우드 공급자별 인프라는 계정과 자격 증명이 필요하므로 재현 가능한 설정 예제로 제공합니다.

## 1분 시작

의존성을 설치한 다음 터미널 두 개를 엽니다. 로컬 프로필의 API 주소가
`http://127.0.0.1:4200/api`라면 서버를 먼저 실행해야 합니다.

```powershell
# 터미널 1
uv sync --extra dev
.\scripts\start_local_server.ps1

# 터미널 2
$env:PREFECT_API_URL = "http://127.0.0.1:4200/api"
uv run python -m prefect_examples.basics
uv run pytest
```

UI: <http://127.0.0.1:4200>

### `Failed to reach API` / `WinError 10061`

이 오류는 `PREFECT_API_URL`은 설정되어 있지만 해당 주소에서 Prefect 서버가
실행되지 않을 때 발생합니다. 첫 번째 터미널에서 `.\scripts\start_local_server.ps1`을
실행하고 `http://127.0.0.1:4200`이 열리는지 확인한 뒤 예제를 다시 실행하세요.
Docker를 사용한다면 `docker compose up prefect-server`로 서버만 시작할 수도 있습니다.

### 서버 시작 중 PostgreSQL `ConnectionRefusedError`

Prefect 프로필에 `PREFECT_API_DATABASE_CONNECTION_URL`이 PostgreSQL로 설정되어 있지만
PostgreSQL이 실행되지 않을 때 발생합니다. 위의 `start_local_server.ps1`은 사용자
프로필을 수정하지 않고 이 저장소의 `prefect.db` SQLite 파일을 사용하므로 학습용
실행에 적합합니다. PostgreSQL 구성을 시험하려면 해당 서버를 먼저 시작하세요.

## 기능 지도

| 기능군 | 예제 | 실행 조건 |
|---|---|---|
| Flow, Task, 파라미터, 서브플로우, 동적 분기 | `basics.py` | 로컬 |
| Future, 동시 실행, `submit`, `map`, 의존성 | `concurrency_mapping.py` | 로컬 |
| 비동기 Flow/Task | `async_workflows.py` | 로컬 |
| 재시도, 지수 백오프, 캐시, 결과 영속화 | `resilience.py` | 로컬 |
| 상태, 실패 처리, 완료/실패 훅 | `states_and_hooks.py` | 로컬 |
| 로그, Markdown/Table/Link 아티팩트 | `observability.py` | 로컬/서버 권장 |
| 태그 기반 전역 동시성 및 rate limit | `global_concurrency.py` | 서버 필요 |
| Blocks, Secret, Variables | `configuration.py` | 서버 필요 |
| 커스텀 이벤트, 이벤트 리소스 | `events.py` | 서버 필요 |
| 이벤트 자동화, trigger/action | `automations.py` | 서버 필요 |
| 사람 입력, pause/suspend | `interactive.py` | 서버와 UI 필요 |
| 동기/비동기 API 클라이언트 | `api_client.py` | 서버 필요 |
| 트랜잭션, rollback/commit 훅 | `transactions.py` | 로컬 |
| Asset/lineage 메타데이터 | `assets.py` | 로컬/서버 권장 |
| `serve`, cron/interval/rrule 스케줄 | `deployments/serve.py` | 서버 필요 |
| 여러 cron/interval/rrule 스케줄 | `deployments/schedules.py` | 서버 필요 |
| Process work pool, worker, 원격 배포 | `deployments/work_pool.py` | 서버 필요 |
| `prefect.yaml` 배포 레시피 | `prefect.yaml` | 서버 필요 |
| Docker 실행 | `Dockerfile`, `compose.yaml` | Docker |
| 단위/통합 테스트 | `tests/` | 로컬 |
| CI | `.github/workflows/ci.yml` | GitHub Actions |

## 자주 쓰는 실행 명령

```powershell
# 모든 로컬 예제를 차례로 실행
uv run python scripts/run_local_examples.py

# 배포 생성 (서버가 실행 중이어야 함)
uv run prefect work-pool create --type process local-process
uv run python -m prefect_examples.deployments.work_pool
uv run prefect worker start --pool local-process

# YAML 기반 배포
uv run prefect deploy --all
uv run prefect deployment run "scheduled-report/yaml-cron"

# 정적 인프라에서 serve
uv run python -m prefect_examples.deployments.serve
```

## Prefect Cloud 연결

```powershell
uv run prefect cloud login
# 또는 CI에서 PREFECT_API_URL, PREFECT_API_KEY를 secret으로 설정
uv run prefect config view
```

비밀 값은 저장소나 `prefect.yaml`에 넣지 마세요. `Secret` block, 환경 변수 또는 CI secret을 사용하세요.

## Docker

```powershell
docker compose up --build
```

이 구성은 학습용 SQLite 서버와 예제 컨테이너를 시작합니다. 운영 환경에서는 PostgreSQL, 인증, TLS, 백업 및 별도 worker를 구성하세요.

## 통합 패키지

Prefect 통합은 필요한 것만 추가합니다. 예: `prefect-aws`, `prefect-azure`, `prefect-gcp`, `prefect-docker`, `prefect-kubernetes`, `prefect-dask`, `prefect-ray`, `prefect-sqlalchemy`, `prefect-github`, `prefect-slack`. 각 통합은 별도 서비스와 자격 증명이 필요하므로 이 저장소의 기본 설치에는 포함하지 않았습니다.

## 공식 문서

- [Prefect 시작하기](https://docs.prefect.io/v3/get-started)
- [Flows](https://docs.prefect.io/v3/concepts/flows)
- [Tasks](https://docs.prefect.io/v3/concepts/tasks)
- [Deployments](https://docs.prefect.io/v3/concepts/deployments)
- [공식 통합 목록](https://docs.prefect.io/integrations)
