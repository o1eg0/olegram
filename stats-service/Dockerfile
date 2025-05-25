FROM python:3.13-slim

WORKDIR /app

# Add system dependencies for building Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       build-essential \
       libpq-dev \
       libffi-dev \
       libssl-dev \
       wget \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY . .

EXPOSE 50051

CMD ["poetry", "run", "python3", "main.py"]
