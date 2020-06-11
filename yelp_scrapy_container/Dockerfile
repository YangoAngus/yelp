FROM python:3.7-alpine
WORKDIR /yelp_scrapy
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk add --no-cache \
        libressl-dev \
        musl-dev \
        libffi-dev
RUN apk add libxml2-dev libxslt-dev
RUN apk add musl-dev mariadb-dev gcc
RUN pip install mysqlclient
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD scrapy crawl yelp





