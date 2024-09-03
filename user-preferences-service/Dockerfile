# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables to avoid Python buffering and specify the Flask app
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Expose port 5001 for the Flask app to run on
EXPOSE 5001

# Run the command to start the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
