from orchestration.defs.ingestion import (
    dagster_market_assets,
    dagster_financial_assets,
    data_ingestion_job,
    data_ingestion_schedule,
    dlt_resource,
)
from orchestration.defs.transformation import intrinsic_dbt_assets, intrinsic_project
from orchestration.defs.branch_deployments import (
    clone_prod,
    drop_prod_clone,
)
from dagster import Definitions
from dagster_dbt import DbtCliResource
from dagster_duckdb import DuckDBResource
import os

is_branch_deployment: bool = (
    os.environ.get("DAGSTER_CLOUD_IS_BRANCH_DEPLOYMENT", "") == "1"
)

base_jobs = [data_ingestion_job]

base_resources = {
    "dlt": dlt_resource,
    "dbt": DbtCliResource(project_dir=intrinsic_project),
}

branch_deployment_jobs = [clone_prod.to_job(), drop_prod_clone.to_job()]

motherduck_resource = DuckDBResource(
    database=f"md:{os.environ.get('DAGSTER_CLOUD_DEPLOYMENT_NAME', '')}_{os.environ.get('BASE_DB_NAME', '')}?motherduck_token={os.environ.get('MOTHERDUCK_TOKEN')}"
)


jobs = base_jobs + branch_deployment_jobs if is_branch_deployment else base_jobs

resources = (
    base_resources.update({"motherduck": motherduck_resource})
    if is_branch_deployment
    else base_resources
)

defs = Definitions(
    assets=[dagster_financial_assets, dagster_market_assets, intrinsic_dbt_assets],
    jobs=jobs,
    schedules=[data_ingestion_schedule],
    resources=resources,
)
