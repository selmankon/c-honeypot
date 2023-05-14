FROM python:3.11.3-alpine

# RUN apk update && apk add bash python3-dev
RUN apk update && apk add bash

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./honeypot/ ./honeypot/
COPY ./run.sh ./

RUN chmod +x ./run.sh

ENTRYPOINT ["./run.sh"]
