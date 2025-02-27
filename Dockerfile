# Use an official Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first (for caching)
COPY requirements.txt .

# Install system dependencies for Selenium & Chromium
RUN apt-get update && apt-get install -y \
    curl unzip wget xvfb libxi6 libgconf-2-4 gnupg chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Use environment variables from .env file
ENV PYTHONUNBUFFERED=1

# Command to run the script
CMD ["python", "main.py"]
