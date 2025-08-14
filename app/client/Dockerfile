# ./app/client/Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install client deps
# If your client deps are in a different file, adjust accordingly
COPY app/client/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app/ /app/app/

EXPOSE 5049
CMD ["python", "-m", "app.client.run"]
