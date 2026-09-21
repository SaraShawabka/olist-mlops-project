FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --default-timeout=600 -r requirements.txt

COPY app/ app/
COPY src/ src/
COPY config/ config/
COPY great_expectations/ great_expectations/
COPY artifacts/feature_list.json artifacts/feature_list.json
COPY artifacts/models/ artifacts/models/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
