# 1. Base Image: Use a lightweight Python version to keep the image small and secure
FROM python:3.9-slim

# 2. Environment Variables for Python Optimization
# Prevents Python from writing .pyc files (useless in containers)
ENV PYTHONDONTWRITEBYTECODE=1
# Ensures logs are flushed directly to the terminal (crucial for debugging)
ENV PYTHONUNBUFFERED=1

# 3. Set Working Directory inside the container
WORKDIR /app

# 4. System Dependencies
# Install basic build tools required for some Python libraries (like Pandas/Numpy)
# Clean up apt cache afterwards to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Python Dependencies
# Strategy: Copy requirements first to leverage Docker Layer Caching.
# If code changes but requirements don't, this step is skipped (faster builds).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy Application Code
# Copy the rest of the project files into the container
COPY . .

# 7. Create Directory Structure for Data (Idempotency)
# Ensures raw data folders exist before execution to prevent "Path Not Found" errors
RUN mkdir -p data/raw/flow data/raw/rainfall

# 8. Entry Point
# The command that runs when the container starts
CMD ["python", "src/main.py"]