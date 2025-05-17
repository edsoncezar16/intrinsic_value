import dlt
from scrapy import Spider, Request
from scrapy.http import Response
from destination import duckdb_destination
from scraping import run_pipeline


def get_relevant_info(all_info: list[str], relevant_info: str) -> str:
    """Helper function to extract desired info from Fundamentus pages."""
    index = all_info.index(relevant_info)
    return all_info[index + 1]


class FundamentusSpider(Spider):
    name = "fundamentus"

    start_urls = [
        "https://www.fundamentus.com.br/detalhes.php?papel=ITUB3",
    ]

    def start_requests(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0"
        }
        for url in self.start_urls:
            yield Request(url, headers=headers)

    def parse(self, response: Response):
        ticker = response.url.split("=")[-1]
        all_info = response.css("span.txt::text").getall()
        company_name = get_relevant_info(all_info, "Empresa").split("ON")[0].strip()
        n_stocks = int(get_relevant_info(all_info, "Nro. Ações").replace(".", ""))
        market_price = float(get_relevant_info(all_info, "Cotação").replace(",", "."))
        market_price_date = get_relevant_info(all_info, "Data últ cot")
        yield {
            "ticker": ticker,
            "company_name": company_name,
            "n_stocks": n_stocks,
            "market_price": market_price,
            "market_price_date": market_price_date,
        }


def scrape_fundamentus() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="fundamentus_scraping_pipeline",
        destination=duckdb_destination,
        dataset_name="fundamentus",
    )

    run_pipeline(
        pipeline,
        FundamentusSpider,
        table_name="market_data",
    )


if __name__ == "__main__":
    scrape_fundamentus()
