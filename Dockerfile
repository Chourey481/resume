# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install spacy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application
COPY . .

# Install gunicorn
RUN pip install gunicorn

# Expose port
EXPOSE 10000

# Set environment variables
ENV FLASK_APP=app/main.py
ENV FLASK_ENV=production
ENV PORT=10000

# Run the application with gunicorn
CMD ["gunicorn", "app.main:app", "--bind", "0.0.0.0:10000"]