
# Use a lightweight base image
FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /app
WORKDIR $APP_HOME

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project requirements and install them
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./app $APP_HOME/app

# Create a directory for exports and ensure appropriate permissions
RUN mkdir -p /app/exports && chmod -R 777 /app/exports

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application using uvicorn
# For production, consider using a process manager like Gunicorn with Uvicorn workers
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
