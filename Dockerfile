FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY .env .env

RUN mkdir -p /app/media
RUN mkdir -p /app/static

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# FROM python:3.12-slim
#
# WORKDIR /app
#
# RUN apt-get update \
#     && apt-get install -y gcc libpq-dev \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*
#
#
# COPY pyproject.toml poetry.lock ./
#
# RUN pip install poetry && poetry install --no-root
#
# COPY . .
#
# RUN mkdir -p /app/media
#
# EXPOSE 8000
#
# COPY .env .env
#
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
