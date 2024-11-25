FROM debian:bookworm-slim

WORKDIR /opt/airflow

RUN apt-get update && \
    apt-get install -y wget ca-certificates unzip curl gnupg jq python3 python3-pip chromium chromium-driver --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER=/usr/bin/chromedriver

COPY ./requirements.txt ./

RUN pip3 install --break-system-packages -r requirements.txt --no-cache-dir
