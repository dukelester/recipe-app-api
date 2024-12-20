FROM python:3.12-alpine3.20

LABEL maintainer="lesterlabs, dukelester"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts

ARG DEV=false

RUN pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; then pip install -r /tmp/requirements.dev.txt; fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        dukelester && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R dukelester:dukelester /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts


COPY ./app /app
WORKDIR /app
EXPOSE 8000

ENV PATH="/scripts:/py/bin:$PATH"
USER dukelester

CMD [ "run.sh" ]
