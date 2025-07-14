from dlt.destinations import motherduck, duckdb
import os
from pathlib import Path

deployment: str = os.environ.get("DAGSTER_CLOUD_DEPLOYMENT_NAME", "")
repo_root: Path = Path(__file__).parent.parent.resolve()

if not deployment:
    destination = duckdb(
        credentials=(
            repo_root / f"{os.environ.get('MOTHERDUCK_DATABASE')}.duckdb"
        ).as_posix()
    )
elif deployment == "prod":
    destination = motherduck(
        credentials=f"md:prod_{os.environ.get('MOTHERDUCK_DATABASE')}?motherduck_token={os.environ.get('MOTHERDUCK_TOKEN', '')}"
    )
else:  # branch deployment
    destination = motherduck(
        credentials=f"md:{os.environ.get('MOTHERDUCK_DATABASE')}_clone_{os.environ.get('DAGSTER_CLOUD_PULL_REQUEST_ID')}?motherduck_token={os.environ.get('MOTHERDUCK_TOKEN', '')}"
    )
