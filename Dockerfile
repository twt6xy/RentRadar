FROM python:3.10-slim

WORKDIR /rentradar
COPY . /rentradar

RUN pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

CMD uvicorn rentradar.api.deploy:app --host 0.0.0.0 --port 8000 --reload
