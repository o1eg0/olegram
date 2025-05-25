FROM python:3.13-slim

WORKDIR /app

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8080"]
