FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.7.1

WORKDIR /app/

# Install system requirements
RUN apt update && apt upgrade -y && apt install -y gcc pkg-config wget && rm -rf /var/lib/apt/lists/*

# Install gphoto2 stable from source
RUN wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh
RUN wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/.env
RUN bash gphoto2-updater.sh -s

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Disable virtualenv inside container
RUN poetry config virtualenvs.create false

# Copy Python requirements
COPY poetry.lock pyproject.toml ./

# Install requirements
RUN poetry install --only main --no-interaction --no-ansi --no-root

