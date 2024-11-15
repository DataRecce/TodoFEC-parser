# TodoFEC-parser

This project aligns with the [**TodoFEC**](https://github.com/DataRecce/TodoFEC) initiative to create a standardized set of data tasks for comparing data processing frameworks. We parse and store the data in Parquet files, then upload to a public S3 bucket, so everyone access the data easily

## Query FEC Data on S3 with DuckDB

The [FEC data](https://www.fec.gov/data/browse-data/?tab=bulk-data) for this project is available as Parquet files in an [**S3 bucket**](https://us-east-1.console.aws.amazon.com/s3/buckets/datarecce-todofec?bucketType=general&region=us-east-1&tab=objects#), allowing direct querying without downloading. You can use DuckDB to query the data directly.

1. Install duckdb

``` bash
   pip install duckdb
```

2. Open duckdb

``` bash
   duckdb
```

3. Run a Query: Use the following command to query the Parquet file directly from S3

``` bash
  select count(*) from read_parquet('s3://datarecce-todofec/pac_summary_2024.parquet');
```

Here are the S3 URIs of available dataset:

```
s3://datarecce-todofec/all_candidates_2024.parquet
s3://datarecce-todofec/candidate_master_2024.parquet
s3://datarecce-todofec/candidate_committee_linkage_2024.parquet
s3://datarecce-todofec/house_senate_2024.parquet
s3://datarecce-todofec/committee_master_2024.parquet
s3://datarecce-todofec/pac_summary_2024.parquet
s3://datarecce-todofec/contributions_from_committees_to_candidates_2024.parquet
s3://datarecce-todofec/operating_expenditures_2024.parquet
```

## System Prequisites

Before you begin you'll need the following on your system:

- Python >=3.12 (see [here](https://www.python.org/downloads/))
- Python Poetry >= 1.8 (see [here](https://pypi.org/project/poetry/))

### Setup dependencies

Install the python dependencies

``` bash
poetry install
```

### Run the script

Once installation has completed you can start parsing data.

```bash
poetry run python main.py
```

### The result

```bash
tree --du -h datarecce-todofec/
[804M]  datarecce-todofec/
├── [354M]  parquet
│   ├── [173K]  all_candidates_2020.parquet
│   ├── [164K]  all_candidates_2024.parquet
│   ├── [ 86K]  candidate_committee_linkage_2024.parquet
│   ├── [330K]  candidate_master_2024.parquet
│   ├── [885K]  committee_master_2024.parquet
│   ├── [ 21M]  contributions_from_committees_to_candidates_2020.parquet
│   ├── [ 14M]  contributions_from_committees_to_candidates_2024.parquet
│   ├── [118K]  house_senate_2024.parquet
│   ├── [ 36M]  operating_expenditures_2024.parquet
│   ├── [449K]  pac_summary_2024.parquet
│   └── [281M]  transactions_between_committees_2024.parquet
└── [450M]  raw
    └── [450M]  bulk-downloads
        ├── [ 28M]  2020
        │   ├── [ 28M]  pas220.zip
        │   └── [179K]  weball20.zip
        └── [422M]  2024
            ├── [ 91K]  ccl24.zip
            ├── [855K]  cm24.zip
            ├── [343K]  cn24.zip
            ├── [ 45M]  oppexp24.zip
            ├── [356M]  oth24.zip
            ├── [ 19M]  pas224.zip
            ├── [169K]  weball24.zip
            ├── [448K]  webk24.zip
            └── [119K]  webl24.zip
```
