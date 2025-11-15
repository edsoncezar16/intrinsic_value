from orchestration.defs.ingestion import (
    dagster_market_assets,
    dagster_financial_assets,
    dlt_resource,
)
from orchestration.defs.transformation import intrinsic_dbt_assets, intrinsic_project
from orchestration.defs.branch_deployments import (
    clone_prod,
    drop_prod_clone,
)
from dagster import Definitions, define_asset_job
from dagster_dbt import DbtCliResource
from dagster_duckdb import DuckDBResource
import os

jobs = [define_asset_job(name="all_assets_job")]

resources = {
    "dlt": dlt_resource,
    "dbt": DbtCliResource(project_dir=intrinsic_project),
}

branch_deployment_jobs = [clone_prod.to_job(), drop_prod_clone.to_job()]

motherduck_resource = DuckDBResource(
    database=f"md:prod_{os.environ.get('MOTHERDUCK_DATABASE', '')}?motherduck_token={os.environ.get('MOTHERDUCK_TOKEN')}"
)

if os.environ.get("DAGSTER_CLOUD_IS_BRANCH_DEPLOYMENT", "") == "1":
    jobs = jobs + branch_deployment_jobs
    resources.update({"motherduck": motherduck_resource})

defs = Definitions(
    assets=[dagster_financial_assets, dagster_market_assets, intrinsic_dbt_assets],
    jobs=jobs,
    resources=resources,
)
