import dlt
from bs4 import BeautifulSoup
from typing import Iterator, Any
import dlt.extract
import dlt.extract.exceptions
from dlt.sources.helpers import requests

FUNDAMENTUS_BASE_URL: str = "https://www.fundamentus.com.br/detalhes.php?papel="


def get_relevant_info(all_info: list[str], relevant_info: str) -> str:
    """Helper function to extract desired info from Fundamentus pages."""
    index = all_info.index(relevant_info)
    return all_info[index + 1]


@dlt.resource(standalone=True, max_table_nesting=0, write_disposition="replace")
def market_data(tickers: list[str] = dlt.config.value) -> Iterator[dict[str, Any]]:
    for ticker in tickers:
        try:
            response = requests.get(FUNDAMENTUS_BASE_URL + ticker)
            soup = BeautifulSoup(response.text, "html.parser")
            all_info = list(
                map(lambda x: x.text, soup.find_all("span", {"txt": "txt"}))
            )
            company_name = get_relevant_info(all_info, "Empresa").split("ON")[0].strip()
            n_stocks = int(get_relevant_info(all_info, "Nro. Ações").replace(".", ""))
            market_price = float(
                get_relevant_info(all_info, "Cotação").replace(",", ".")
            )
            market_price_date = get_relevant_info(all_info, "Data últ cot")
            industry = get_relevant_info(all_info, "Subsetor")
            yield {
                "ticker": ticker,
                "company_name": company_name,
                "industry": industry,
                "n_stocks": n_stocks,
                "market_price": market_price,
                "market_price_date": market_price_date,
            }
        except dlt.extract.exceptions.ResourceExtractionError as e:
            print(f"Failed to extract data for ticker {ticker}: {e}")
            raise e


def scrape_fundamentus() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="fundamentus_scraping_pipeline",
        destination="motherduck",
        dataset_name="fundamentus",
        refresh="drop_sources",
    )

    load_info = pipeline.run(market_data())

    print(load_info)


if __name__ == "__main__":
    scrape_fundamentus()
