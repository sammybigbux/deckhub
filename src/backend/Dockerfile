# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary system dependencies and upgrade pip
RUN apt-get update && apt-get install -y \
    python3-venv \
    gcc \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

# Create a virtual environment
RUN python -m venv /app/venv

# Ensure the virtual environment is used for subsequent commands
ENV PATH="/app/venv/bin:$PATH"

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary dependencies within the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app will run on
EXPOSE 8080

# Set environment variables for Flask (if you're using Flask)
ENV PORT 8080

# Run the application
CMD ["python", "app.py"]
