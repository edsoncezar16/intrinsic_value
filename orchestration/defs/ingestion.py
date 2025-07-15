from dagster import (
    AssetExecutionContext,
    define_asset_job,
    AssetSelection,
    ScheduleDefinition,
)
from dagster_dlt import DagsterDltResource, dlt_assets
from ingestion.google_sheets_pipeline import (
    financial_source,
    financial_pipeline,
    table_names,
)
from ingestion.yfinance_pipeline import market_source, market_pipeline
from dagster_dlt import DagsterDltTranslator
from dagster_dlt.translator import DltResourceTranslatorData
from dagster import AssetSpec, AssetKey


class CustomDagsterDltTranslator(DagsterDltTranslator):
    def get_asset_spec(self, data: DltResourceTranslatorData) -> AssetSpec:
        """Overrides asset spec to override asset deps to be none and improve asset keys."""
        default_spec = super().get_asset_spec(data)
        return default_spec.replace_attributes(
            deps=[], key=AssetKey(["google_sheets", data.resource.name])
        )


@dlt_assets(
    dlt_source=financial_source.with_resources(*table_names),
    dlt_pipeline=financial_pipeline,
    name="financial_ingestion",
    group_name="bronze",
    dagster_dlt_translator=CustomDagsterDltTranslator(),
)
def dagster_financial_assets(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context, dataset_name="google_sheets")


@dlt_assets(
    dlt_source=market_source(),
    dlt_pipeline=market_pipeline,
    name="market_ingestion",
    group_name="bronze",
    dagster_dlt_translator=CustomDagsterDltTranslator(),
)
def dagster_market_assets(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)


data_ingestion_job = define_asset_job(
    "bronze_ingestion_job", selection=AssetSelection.groups("bronze")
)

data_ingestion_schedule = ScheduleDefinition(
    job=data_ingestion_job,
    cron_schedule="0 9 * * 1-5",
    execution_timezone="America/Belem",
)

dlt_resource = DagsterDltResource()
