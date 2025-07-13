from orchestration.defs.ingestion import (
    dagster_market_assets,
    dagster_financial_assets,
    data_ingestion_job,
    data_ingestion_schedule,
    dlt_resource,
)
from orchestration.defs.transformation import intrinsic_dbt_assets, intrinsic_project
from dagster import Definitions
from dagster_dbt import DbtCliResource

defs = Definitions(
    assets=[dagster_financial_assets, dagster_market_assets, intrinsic_dbt_assets],
    jobs=[data_ingestion_job],
    schedules=[data_ingestion_schedule],
    resources={
        "dlt": dlt_resource,
        "dbt": DbtCliResource(project_dir=intrinsic_project),
    },
)
