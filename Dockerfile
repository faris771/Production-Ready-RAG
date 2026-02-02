# Python application
FROM python:3.13-slim

# Add metadata labels for GitHub Container Registry
LABEL org.opencontainers.image.source="https://github.com/faris771/Production-Ready-RAG"
LABEL org.opencontainers.image.description="Production-Ready RAG System with FastAPI, Inngest, Qdrant, and Google Gemini"
LABEL org.opencontainers.image.licenses="MIT"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

