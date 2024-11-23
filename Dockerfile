FROM python:3.12-alpine3.20

LABEL maintainer="lesterlabs, dukelester"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

ARG DEV=false

RUN pip install --upgrade pip
RUN if [ $DEV = "true" ]; then pip install -r /tmp/requirements.dev.txt; fi
RUN pip install -r /tmp/requirements.txt

COPY ./app /app
WORKDIR /app
EXPOSE 8000

# USER dukelester
