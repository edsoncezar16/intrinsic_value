from pathlib import Path
from dagster_dbt import (
    DbtCliResource,
    DbtProject,
    dbt_assets,
    DagsterDbtTranslator,
    DagsterDbtTranslatorSettings,
)
import dagster as dg
from typing import Mapping, Any, Optional


class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    def get_automation_condition(
        self, dbt_resource_props: Mapping[str, Any]
    ) -> Optional[dg.AutomationCondition]:
        return dg.AutomationCondition.eager()


RELATIVE_PATH_TO_MY_DBT_PROJECT = "../../transformation"

intrinsic_project = DbtProject(
    project_dir=Path(__file__)
    .joinpath("..", RELATIVE_PATH_TO_MY_DBT_PROJECT)
    .resolve(),
)
intrinsic_project.prepare_if_dev()


@dbt_assets(
    manifest=intrinsic_project.manifest_path,
    dagster_dbt_translator=CustomDagsterDbtTranslator(
        settings=DagsterDbtTranslatorSettings(enable_source_tests_as_checks=True)
    ),
)
def intrinsic_dbt_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
