# Avocado API Deployment on Azure Kubernetes Services (AKS) using a manifest file

This GitHub Actions workflow is named "avocado" and is used to build, push, and deploy a Flask API in a Kubernetes cluster.

The workflow is triggered when you push to the `main` branch or manually via the GitHub Actions UI.

### Prerequisites
You need to have an Azure account and set up the following resources:
  - Azure Container Registry (ACR)
  - Kubernetes cluster (AKS)
  - Set up the required secrets in your GitHub repository: 
    - `AZURE_CREDENTIALS`

## Workflow overview
The workflow is composed of two main jobs: `buildImage` and `deploy`.

### buildImage job
This job is responsible for building and pushing the Docker image for the Flask API to the Azure Container Registry (ACR).

The following steps are executed:
  1. Check out the repository
  2. Log in to Azure
  3. Log in to ACR
  4. Set up Docker Buildx
  5. Cache Docker layers
  6. Build and push the Docker image

### deploy job
This job is responsible for deploying the Flask API to a Kubernetes cluster.

The following steps are executed:
  1. Check out the repository
  2. Log in to Azure
  3. Set up kubelogin for non-interactive login
  4. Get the Kubernetes context
  5. Install Helm
  6. Define public Kubernetes chart repository in the Helm configuration
  7. Install Prometheus and Grafana using Helm
  8. Log in to Azure Container Registry
  9. Deploy the application

## Environment Variables
The following environment variables are used throughout the workflow:

  -`ACR_RESOURCE_GROUP`: The Azure Resource Group for the Azure Container Registry
  
  -`AZURE_CONTAINER_REGISTRY`: The name of the Azure Container Registry
  
  -`CLUSTER_RESOURCE_GROUP`: The Azure Resource Group for the Kubernetes cluster
  
  -`CLUSTER_NAME`: The name of the Kubernetes cluster
  
  -`CONTAINER_NAME`: The name of the container to be used in the deployment
  
  -`DEPLOYMENT_MANIFEST_PATH`: The path to the Kubernetes deployment manifest file (e.g., ./avocado-api.yaml)
