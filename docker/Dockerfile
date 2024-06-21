FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TZ=Europe/Amsterdam

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_NO_CACHE_DIR=1

RUN pip install "poetry==1.8.3" && pip install --upgrade setuptools
RUN --mount=type=cache,target=/var/cache/apk

RUN python -m venv /venv
ENV PATH=/venv/bin:$PATH VIRTUAL_ENV=/venv

COPY ./ /app
RUN poetry install --only main

RUN mkdir -p /var/opt/db