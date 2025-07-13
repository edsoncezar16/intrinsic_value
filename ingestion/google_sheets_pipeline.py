from typing import Sequence
import dlt
from ingestion.google_sheets import google_spreadsheet
from .destination import destination


def load_pipeline_with_ranges(
    spreadsheet_url_or_id: str, range_names: Sequence[str]
) -> None:
    """
    Loads explicitly passed ranges
    """
    pipeline = dlt.pipeline(
        pipeline_name="google_sheets_pipeline",
        destination=destination,
    )
    data = google_spreadsheet(
        spreadsheet_url_or_id=spreadsheet_url_or_id,
        range_names=range_names,
        get_sheets=False,
        get_named_ranges=False,
    )
    info = pipeline.run(data, dataset_name="trading_view", table_name="financial_info")
    print(info)


url_or_id = "16PKHlBo1WxiH5FqaY2OHQpb7KLR8AH4FVxT9K23kG3o"
range_names = ["Sheet 1!A4:E300"]

financial_source = google_spreadsheet(
    spreadsheet_url_or_id=url_or_id,
    range_names=range_names,
    get_sheets=False,
    get_named_ranges=False,
)

financial_pipeline = dlt.pipeline(
    pipeline_name="google_sheets_pipeline", destination="motherduck", progress="log"
)

if __name__ == "__main__":
    load_pipeline_with_ranges(url_or_id, range_names)
