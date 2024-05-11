# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY auth.py /app
COPY auth2.py /app

RUN pip install flask flask-httpauth

# Make port 9090 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "auth.py"]
