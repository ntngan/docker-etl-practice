FROM rapidfort/python-chromedriver:latest

WORKDIR /opt/airflow

RUN apt-get update && \
    apt-get install -y wget ca-certificates unzip curl gnupg jq --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./

RUN pip install -r requirements.txt --no-cache-dir 

CMD ["airflow", "standalone"]
