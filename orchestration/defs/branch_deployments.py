from dagster_duckdb import DuckDBResource
from dagster import In, Nothing, graph, op, OpExecutionContext
import os

base_dbname: str = os.environ.get("MOTHERDUCK_DATABASE", "")
pr_id: str = os.environ.get("DAGSTER_CLOUD_PR_ID", "")


@op
def drop_database_clone(motherduck: DuckDBResource):
    with motherduck.get_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS 'md:{base_dbname}_clone_{pr_id}")


@op(ins={"start": In(Nothing)})
def clone_production_database(context: OpExecutionContext, motherduck: DuckDBResource):
    with motherduck.get_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"ATTACH 'md:prod_{base_dbname}' AS source")
        cur.execute(f"ATTACH 'md:{base_dbname}_clone{pr_id}' AS target")

        # Get table list
        tables = cur.execute("""
            SELECT table_name
            FROM source.information_schema.tables
            WHERE table_schema = 'main'
              AND table_type = 'BASE TABLE';
        """).fetchall()

        # Clone each table
        for (table_name,) in tables:
            context.log.info(f"Cloning table: {table_name}")
            cur.execute(f"""
                CREATE TABLE target.{table_name} AS
                SELECT * FROM source.{table_name};
            """)


@graph
def clone_prod():
    clone_production_database(start=drop_database_clone())


@graph
def drop_prod_clone():
    drop_database_clone()
