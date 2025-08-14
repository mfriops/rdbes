# ./server/Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python deps (server + gateway)
# If your requirements file lives elsewhere, adjust the COPY path.
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Recommended: pyogrio simplifies GDAL deps for GeoPackage I/O
# Ensure it's listed in requirements.txt:
#   geopandas>=0.14
#   pyogrio>=0.9

# Copy server code
COPY . /app/server

# Default CMD is provided per-service in docker-stack.yml
