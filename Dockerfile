FROM python:3.12

WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml .

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . .

EXPOSE 80

ENTRYPOINT ["uvicorn", "chat.app:app", "--host", "0.0.0.0", "--port", "80"]
