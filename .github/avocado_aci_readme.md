# GitHub Actions Workflow: Deploy to Azure Kubernetes Services (AKS)
This branch contains a GitHub Actions workflow for deploying an application to Azure Kubernetes Services (AKS) using docker-compose.

### Workflow Overview
The deploy_on_k8s workflow is designed to run on an `ubuntu-latest` virtual environment and depends on the successful completion of the `buildImage` job.
It uses a series of GitHub Actions and shell scripts to deploy the application to AKS.

#### Main Steps
1. Checkout repository

2. Login to Azure

3. Set up kubelogin for non-interactive login

4. Get Kubernetes context

5. Install Kompose and kubectl

6. Convert Docker Compose to Kubernetes resources

7. Deploy Kubernetes resources

#### Permissions
The following permissions are required for this workflow:

  `contents`: read

  `id-token`: write

### How to Use
Make sure you have a valid Azure subscription.

1. Store your Azure credentials in the GitHub repository secrets as AZURE_CREDENTIALS.

2. Update the environment variables `CLUSTER_NAME`, `CLUSTER_RESOURCE_GROUP`, and `DOCKER_COMPOSE_FILE` in file to match your configuration.

3. Push the changes to your repository. The workflow will be triggered automatically when the `buildImage` job completes successfully.

### Dependencies
The workflow depends on the following GitHub Actions:
  - actions/checkout@v3

  - azure/login@v1.4.3

  - azure/use-kubelogin@v1

  - azure/aks-set-context@v3

In addition, the workflow requires the following tools to be installed:

  - Kompose

  - kubectl

The installation of these tools is handled within the workflow script.
