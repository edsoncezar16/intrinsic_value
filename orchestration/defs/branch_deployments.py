from dagster_duckdb import DuckDBResource
from dagster import In, Nothing, graph, op, OpExecutionContext
import os

base_dbname: str = os.environ.get("MOTHERDUCK_DATABASE", "")
pr_id: str = os.environ.get("DAGSTER_CLOUD_PULL_REQUEST_ID", "")


@op
def drop_database_clone(motherduck: DuckDBResource):
    with motherduck.get_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {base_dbname}_clone_{pr_id}")


@op(ins={"start": In(Nothing)})
def clone_production_database(context: OpExecutionContext, motherduck: DuckDBResource):
    with motherduck.get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            f"CREATE DATABASE {base_dbname}_clone_{pr_id} FROM CURRENT_DATABASE()"
        )


@graph
def clone_prod():
    clone_production_database(start=drop_database_clone())


@graph
def drop_prod_clone():
    drop_database_clone()
