import dlt
from typing import Iterator, Any
from datetime import datetime
import yfinance as yf
from .destination import destination


@dlt.resource(
    standalone=True,
    max_table_nesting=0,
    write_disposition="replace",
    name="market_info",
)
def market_info(tickers: list[str] = dlt.config.value) -> Iterator[dict[str, Any]]:
    for ticker in tickers:
        try:
            info: dict = yf.Ticker(f"{ticker}.SA").info
            try:
                short_name: str = info.get("shortName", "")
                company_name: str = short_name.split(" ")[0]
            except IndexError:
                company_name: str = ticker
            market_price: float = info.get("regularMarketPrice", -1.0)
            market_price_date: str = datetime.fromtimestamp(
                info.get("regularMarketTime", 0.0)
            ).strftime("%Y-%m-%d")
            industry = info.get("industry", "")
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
