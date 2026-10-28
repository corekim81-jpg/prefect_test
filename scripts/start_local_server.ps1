$ErrorActionPreference = "Stop"

# 저장소 전용 SQLite를 사용합니다. 사용자 Prefect 프로필에 PostgreSQL이 설정되어
# 있어도 이 프로세스에서만 덮어쓰며, 전역 설정은 변경하지 않습니다.
$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path.Replace("\", "/")
$env:PREFECT_API_DATABASE_CONNECTION_URL = "sqlite+aiosqlite:///$repositoryRoot/prefect.db"
$env:PREFECT_API_URL = "http://127.0.0.1:4200/api"

uv run prefect server start
