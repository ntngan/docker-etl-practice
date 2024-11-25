## Dockerized ETL Project with Airflow and Python Tools

This project aims to create a single Docker container equipped with Apache Airflow, Selenium, Requests, BeautifulSoup, Pandas, and AWS CLI to build a simple ETL pipeline. The pipeline extracts data from Wikipedia, transforms it using Python tools, and saves it as a CSV file. 

### ETL pipeline:
  1. **Extract**: Scrap data from a Wikipedia page using Selenium and BeautifulSoup (https://en.wikipedia.org/wiki/List_of_countries_with_KFC_franchises)
  2. **Transform**: Clean and process the extracted data using Pandas.
  3. **Load**: Save the processed data into a CSV file.

### Apache Airflow:
Create a DAG for orchestrating the ETL process.