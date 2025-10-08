
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./notification_service /app/notification_service
COPY run_consumer.py /app/run_consumer.py

# Expose the port FastAPI runs on
EXPOSE 8000

CMD ["uvicorn", "notification_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
