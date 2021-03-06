#!/bin/bash

FROM python:3.8-alpine
RUN rm -rf /var/cache/apk/* && \
    apk update && \
    apk add make && \
    apk add build-base && \
    apk add gcc && \
    apk add python3-dev && \
    apk add libffi-dev && \
    apk add musl-dev && \
    apk add openssl-dev && \
    apk del build-base && \
    rm -rf /var/cache/apk/*

ENV HOME=/home/api FLASK_APP=application.py FLASK_ENV=development PORT=5000
RUN adduser -D api
USER api
WORKDIR $HOME
COPY --chown=api:api . $HOME

RUN python -m venv venv && \
    venv/bin/pip install --upgrade pip && \
    venv/bin/pip install wheel && \
    venv/bin/pip install -r requirements/develop.txt

EXPOSE 5000
COPY . $HOME
ENTRYPOINT [ "./boot.sh" ]
