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

# Ensure the correct ChromeDriver version is installed
RUN CHROMIUM_VERSION=$(chromium --version | awk '{print $2}') && \
    CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMIUM_VERSION) && \
    wget -q "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver

# Use environment variables from .env file
ENV PYTHONUNBUFFERED=1

# Command to run the script
CMD ["python", "main.py"]
