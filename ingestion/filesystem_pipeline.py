# flake8: noqa
from typing import Iterator
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
            base_data = pd.read_excel(
                balance_xlsx_bytes,
                sheet_name="Dem. Result.",
                header=None,
            )
            # tricks based on the file structure
            company_name = base_data.iloc[0, 1].split("-")[1].strip()
            base_historical_earnings = base_data.iloc[-1, 1:].to_list()

            yield {
                "company_name": company_name,
                "values": [float(x) for x in base_historical_earnings if x is not None],
            }


if __name__ == "__main__":
    fundamentus_data = filesystem() | historical_earnings()
    # keep only one table at the destination
    fundamentus_data.max_table_nesting = 0

    pipeline = dlt.pipeline(
        pipeline_name="fundamentus_balance_sheets_pipeline",
        dataset_name="fundamentus",
    )
    # Execute the pipeline and load the extracted data into the "duckdb" destination.
    load_info = pipeline.run(
        fundamentus_data.apply_hints(write_disposition="replace"),
        destination="motherduck",
        refresh="drop_sources",
    )
    # Print the loading information.
    print(load_info)
