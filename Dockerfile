FROM python:3.6

COPY pyproject.toml .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
RUN pip3 install flask

COPY app.py .
COPY /app /app
