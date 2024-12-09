# Use an official Python image as the base
FROM python:3.9-slim

# Set environment variables to avoid buffering in logs
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose the Streamlit default port
EXPOSE 8504

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
