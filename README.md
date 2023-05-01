# Microservice Flask Project

This project consists of a Flask-based microservice, deployed using Kubernetes. The microservice is responsible for authentication.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Environment Variables](#environment-variables)
- [Generating RSA Keys](#generating-rsa-keys)
- [Usage](#usage)
- [Contributing](#contributing)

## Prerequisites

Before getting started, ensure you have the following installed on your system:

1. Docker
2. Kubernetes (Minikube for local development)
3. Python 3.8+
4. Virtualenv
5. Postgres

## Installation

Follow these steps to set up the project:

1. Clone the repository:

    ```bash
   git clone <https://github.com/suleymanozkeskin/Microservice_Flask.git>
   cd Microservice_Flask/src/auth/
    ```

2. Create a virtual environment and install the dependencies:

    ```bash
   virtualenv venv
   source venv/bin/activate
   pip install -r requirements.txt
    ```

3. Build the Docker image:

    ```bash
   docker build -t your-user-name/auth:latest .
    ```

4. Start the Kubernetes cluster (if using Minikube):

    ```bash
    minikube start
    ```

5. Apply the Kubernetes manifests:

    ```bash
    cd manifests/
    kubectl apply -f .
    ```

6. Check the status of the pods:

    ```bash
    kubectl get pods
    ```

## Configuration

The configuration of the microservice is stored in the auth-configmap.yaml file. Update this file to change the database settings and other configuration options.
Additionally, the auth-secret.yaml file contains the private and public keys used for signing and verifying JWT tokens. You can generate new keys using the instructions in the [Generating RSA Keys](#generating-rsa-keys) section.

## Environment Variables

The following environment variables are used to configure the microservice:

- DATABASE_HOSTNAME: The hostname of the PostgreSQL database server.
- DATABASE_PORT: The port number of the PostgreSQL database server.
- DATABASE_USERNAME: The username to access the PostgreSQL database.
- DATABASE_PASSWORD: The password to access the PostgreSQL database.
- DATABASE_NAME: The name of the PostgreSQL database.
- PRIVATE_KEY: The private key used for signing JWT tokens.
- PUBLIC_KEY: The public key used for verifying JWT tokens.

## Generating RSA Keys

You need to generate a public-private key pair for JWT token signing and verification. Run the following commands to generate the keys:

    openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
    openssl rsa -pubout -in private_key.pem -out public_key.pem

Save the generated private_key.pem and public_key.pem files, and set the PRIVATE_KEY and PUBLIC_KEY environment variables in the auth-secret.yaml file with the contents of the respective files.

## Contributing

To contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch with a descriptive name.
3. Make your changes and commit them with clear and concise commit messages.
4. Push your changes to the forked repository.
5. Create a pull request to the original repository.
