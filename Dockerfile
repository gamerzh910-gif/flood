FROM python:3.12-slim

# Install system dependencies including aria2c and ffmpeg
RUN apt-get update && apt-get install -y \
    aria2 \
    ffmpeg \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Create downloads directory
RUN mkdir -p downloads

# Run the bot
CMD ["python3", "main.py"]
