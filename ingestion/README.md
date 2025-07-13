# dlt ingestion pipelines

Outlines the required credentials for the dlt pipelines.

## config.toml

```toml
[runtime]
log_level="WARNING"  # the system log level of dlt
# use the dlthub_telemetry setting to enable/disable anonymous usage data reporting, see https://dlthub.com/docs/reference/telemetry
dlthub_telemetry = true

[sources.filesystem]
bucket_url = "s3://fundamentus-data/" # please set me up!

[sources.scraping]
start_urls = ["https://www.fundamentus.com.br/detalhes.php?papel=ITUB3"] # please set me up!
start_urls_file = ""
```

## secrets.toml

```toml
[sources.filesystem.credentials]
aws_access_key_id = "xxx"
aws_secret_access_key = "xxxx"
region_name="sa-east-1"
```
