FROM python:3.12-slim

# Set environment variables
ARG OPENWEATHERMAP_API_KEY
ENV OPENWEATHERMAP_API_KEY=$OPENWEATHERMAP_API_KEY

WORKDIR /app

# Copy the application code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
