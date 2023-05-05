# Use the official Python 3.10 slim image as the base
FROM python:3.10-slim-bullseye

# Set the working directory
WORKDIR /app

# Update packages and install necessary packages
RUN apt-get update \
    && apt-get install -y telnet \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

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

# docker tag 97261b7e36f27c4bdb5785568fd14d68022166149b907c0b470ea900785a2e0d  suleymanozkeskin/auth:latest

# docker push suleymanozkeskin/auth:latest

# docker pull suleymanozkeskin/auth:latest

# cd manifests ==> kubectl apply -f ./

# kubectl port-forward pod/auth-6b4c657556-4mwdp 5000:5000 ==>  by using this command we can access the pod from our local machine as well. Otherwise we can not access the pod from our local machine.


