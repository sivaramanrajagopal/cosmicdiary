# Cosmic Diary Flask API - Python Only
# This service runs only the Flask API backend, ignoring Next.js frontend

FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy only Python files (ignore Node.js files)
COPY requirements.txt .
COPY *.py ./
COPY prompts/ ./prompts/
# Note: Individual files already copied by *.py, but explicit for clarity

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (Railway sets PORT env var)
EXPOSE 8000

# Start Flask API server
CMD ["python", "api_server.py"]

