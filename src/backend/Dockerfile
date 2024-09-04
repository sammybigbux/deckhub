# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy website_backend and chat_backend directories into the container
COPY website_backend/ /app/website_backend/
COPY chat_backend/ /app/chat_backend/

# Copy data directories used by term_manager.py
COPY chat_backend/apply_data /app/chat_backend/apply_data
COPY chat_backend/learn_data /app/chat_backend/learn_data
COPY chat_backend/understand_data /app/chat_backend/understand_data

# Expose port 5000 for Flask
EXPOSE 5000

# Start the Flask app (adjust command based on your setup)
CMD ["python", "website_backend/app.py"]
