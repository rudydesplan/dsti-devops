# Avocado API - Kubernetes Manifest
This README.md file provides an overview of the Kubernetes manifests used to deploy the Avocado API application in a Kubernetes cluster. 

#### Overview

The Kubernetes manifests include the following resources:
1. Namespace
2. Deployment
3. Service

### 1. Namespace
The `Namespace` resource named "avocado" isolates the Avocado API resources within the Kubernetes cluster.

### 2. Deployment
The `Deployment` resource named "avocado-api" creates a deployment for the Avocado API application.
It consists of the following configurations:
  - Replicas: 1 replica for the application pod.
  - Labels: Uses the label `app: avocado-api` to identify the pods managed by this deployment.
  - Template: Defines the pod's specifications, which include:
    - Annotations: Configures Istio sidecar injection and provides optional Prometheus monitoring configurations.
    - Labels: Assigns the `app: avocado-api` label to the pod.
    - Containers: Specifies the "avocado-k8s-container" to be used, along with its container image and port configuration.
    - Environment Variables: Sets the MongoDB connection string.

### 3. Service
The `Service` resource named "avocado-api" exposes the Avocado API application to be accessed by other services or external clients.
It uses the following configurations:
  - Selector: Maps the service to the pods with the label `app: avocado-api`.
  - Ports: Defines the port mapping from port 80 to the target container port 5000.
  - Type: Configures the service as a `LoadBalancer` to handle traffic and expose it externally.

## NB : If you want to enable ISTIO , uncomment the lines.
