#! /bin/bash

set -euxo pipefail

cd ingestion || exit

python filesystem_pipeline.py

python scraping_pipeline.py

cd ../transformation

dbt build
