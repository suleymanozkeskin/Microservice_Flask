# Use the official Python 3.10 slim image as the base
FROM python:3.10-slim-bullseye

# Set the working directory
WORKDIR /app

# Update packages and install necessary packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*


# Copy the private key and public key files
COPY private_key.pem /app/
COPY public_key.pem /app/


# Copy requirements.txt and install the dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


# Copy the application files and .env file
COPY . /app/



# Expose the port your app runs on
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=server.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

## Build the image
# docker build -t flask-app:latest .

## Run the container

# docker run -d -p 5000:5000 flask-app:latest

# docker tag 10dacc26d9f7bd0490eddee4c9c915f82f22e03d575e089a601c931866e5d5d4 suleymanozkeskin/auth:latest
