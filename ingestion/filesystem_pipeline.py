# flake8: noqa
from typing import Iterator
from destination import duckdb_destination
import dlt
from dlt.sources import TDataItems
from dlt.sources.filesystem import FileItemDict, filesystem
import pandas as pd
from zipfile import ZipFile


def extract_zip(input_bytes):
    input_zip = ZipFile(input_bytes)
    return {name: input_zip.read(name) for name in input_zip.namelist()}


# Define a standalone transformer to read data historical balance sheets.
@dlt.transformer(standalone=True)
def historical_earnings(items: Iterator[FileItemDict]) -> Iterator[TDataItems]:

    # Iterate through each file item.
    for file_obj in items:
        # Open the file object.
        with file_obj.open() as file:
            balance_xlsx_bytes = extract_zip(file)["balanco.xls"]
            quarter_column_headers = list(map(lambda x: f"Q-{60-x}", range(0, 60)))
            base_data = pd.read_excel(
                balance_xlsx_bytes,
                sheet_name="Dem. Result.",
                header=None,
                names=["metric"] + quarter_column_headers,
                usecols="A:BI",
            )
            # trick based on the file structure
            company_name = base_data["Q-60"].values[0].split("-")[1].strip()

            base_historical_earnings = (
                base_data[quarter_column_headers].iloc[-1, :].to_list()
            )
            return {
                "company_name": company_name,
                "values": list(
                    filter(lambda x: x is not None, base_historical_earnings)
                ),
            }


if __name__ == "__main__":
    fundamentus_data = filesystem() | historical_earnings()
    # keep only one table at the destination
    fundamentus_data.max_table_nesting = 0

    pipeline = dlt.pipeline(
        pipeline_name="fundamentus_balance_sheets_pipeline",
        destination=duckdb_destination,
        dataset_name="fundamentus",
    )
    # Execute the pipeline and load the extracted data into the "duckdb" destination.
    load_info = pipeline.run(
        fundamentus_data.apply_hints(write_disposition="replace"),
    )
    # Print the loading information.
    print(load_info)
