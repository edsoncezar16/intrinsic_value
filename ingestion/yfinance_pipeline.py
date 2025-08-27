import dlt
from typing import Iterator, Any
from datetime import datetime
import yfinance as yf
from .destination import destination
from .google_sheets_pipeline import financial_source


@dlt.transformer(
    data_from=financial_source.resources["financial_info"],
    max_table_nesting=0,
    write_disposition="replace",
    name="market_info",
)
def market_info(financial_item) -> Iterator[dict[str, Any]]:
    try:
        ticker: str = financial_item["Stock"]
        info: dict = yf.Ticker(f"{ticker}.SA").info
        market_price: float = info.get("regularMarketPreviousClose", -1.0)
        market_price_date: str = datetime.fromtimestamp(
            info.get("regularMarketTime", 0.0)
        ).strftime("%Y-%m-%d")
        industry: str = info.get("industry", "")
        company_name: str = info.get("longName", "")
        yield {
            "ticker": ticker,
            "company_name": company_name,
            "industry": industry,
            "market_price": market_price,
            "market_price_date": market_price_date,
        }
    except ValueError as e:
        print(f"Failed to extract data for ticker {ticker}: {e}")
        raise e


market_pipeline = dlt.pipeline(
    pipeline_name="yfinance_pipeline",
    destination=destination,
    dataset_name="yfinance",
    refresh="drop_sources",
)


@dlt.source(name="yfinance")
def market_source():
    yield market_info()


def ingest_yfinance() -> None:
    load_info = market_pipeline.run(market_info())

    print(load_info)


if __name__ == "__main__":
    ingest_yfinance()
