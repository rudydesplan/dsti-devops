# GitHub Actions Workflow: Deploy to Azure Kubernetes Services (AKS)
This branch contains a GitHub Actions workflow for deploying an application to Azure Kubernetes Services (AKS) using docker-compose.

### Workflow Overview
The `avocado_aci` workflow is designed to run on an `ubuntu-latest` virtual environment and is triggered on `push` and `pull_request` events to the `deploy/aci` branch. 
It consists of two jobs: `buildImage` and `deploy_aci`.

## BuildImage Job
The buildImage job is responsible for building and pushing a Docker image to Azure Container Registry (ACR).

Main steps involved are:

1. Checkout repository: Using the `actions/checkout@v3` action, the repository contents are checked out to the runner.

2. Azure Login: The `azure/login@v1.4.3` action is used for logging into Azure using the credentials stored in the repository secrets.

3. Login to ACR: A shell command (`az acr login`) is run to login to the Azure Container Registry.

4. Set up Docker Buildx: The `docker/setup-buildx-action@v2.5.0` action sets up Docker Buildx, an extension of Docker that enables full support of its features in CI.

5. Cache Docker layers: The `actions/cache@v2.1.8 action is used to cache Docker layers. This helps to speed up subsequent Docker builds by reusing the cached layers.

6. Build and push Docker image: The `docker/build-push-action@v4.0.0` action is used to build the Docker image from the Dockerfile located in the `./flask-api` directory and push it to the Azure Container Registry.

## Deploy_aci Job
The `deploy_aci` job is responsible for deploying the Docker image to Azure Container Instances (ACI).

Main steps involved are:

1.  Checkout repository: The repository contents are checked out to the runner using actions/checkout@v3 action.

2.  Azure Login: The azure/login@v1.4.3 action is used for logging into Azure using the credentials stored in the repository secrets.

3.  Login to ACR: A shell command (az acr login) is run to login to the Azure Container Registry.

4.  Deploy to ACI: A series of Docker commands are run to create a Docker context, set it to the newly created context, and use Docker Compose to deploy the application to ACI.

5.  Check ACI deployment status: The status of the ACI deployment is checked by running docker compose ps.


This workflow utilizes environment variables and GitHub secrets to securely manage sensitive information such as Azure credentials and Azure Container Registry details.
