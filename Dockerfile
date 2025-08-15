# Dockerfile for Cognitive SOAR System
# Use Python 3.11, the latest version officially supported by PyCaret
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Set environment variables for better Python performance
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# 1. Install system-level build dependencies
# This is a critical step to install compilers (like gcc, g++) needed by
# some of PyCaret's underlying packages (e.g., shap, wordcloud, scikit-learn).
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        libblas-dev \
        liblapack-dev \
        libatlas-base-dev \
        gfortran \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 2. Copy only the requirements file to leverage Docker's layer caching.
# This layer only gets rebuilt if requirements.txt changes.
COPY requirements.txt .

# 3. Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4. Create necessary directories
RUN mkdir -p models data .streamlit

# 5. Copy application code
COPY . .

# 6. Set proper permissions
RUN chmod +x /app/train_model.py

# Expose the port that Streamlit runs on
EXPOSE 8501

# Health check to ensure the application is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# The CMD to start the application is located in the docker-compose.yml file
# for better development/production flexibility.

