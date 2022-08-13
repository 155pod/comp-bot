ARG PYTHON_VERSION=3.10.4

FROM python:${PYTHON_VERSION}

RUN apt-get update && apt-get install -y \
    python3-pip \
    ffmpeg

RUN mkdir -p /app
WORKDIR /app

COPY pyproject.toml .

RUN pip install poetry
RUN poetry install

COPY . .

CMD poetry run python main.py
