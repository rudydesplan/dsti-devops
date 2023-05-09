# Project

## Deadline

08/05/2023

## Opportunities

1. This DevOps project is based on all of the labs passed during the course.

2. Work on the project has be carried out by 2 students.


## Instructions

### 1. Web application

We Create a a Flask web application exposing REST API that uses a custom Python module, to transform a CSV file or a Dataframe from raw avocados data to prepared and accurate JSON output.

Prepared data are also stored in MongoDB Database on the cloud.

Look at the readme.md file in the flask-api directory for more information about the configuration and use

**Are proposed:**

- a little user API application
- storage in MongoDB database on cloud storage
- tests: unit, API, configuration, connection.
- health check endpoint ensuring an application is functional

### 2. CI/CD pipeline 

CI/CD (including deployment) pipeline using GitHub Actions.

2 Workflows :

Flask Api Test
Avocado ( with build Image and Deployment on Azure)

NB : EACH WORKFLOW HAS A README.MD AND GRAPH FILE.

### 3. Configure and provision a virtual environment and run your application using the IaC approach

1. Configure with Vagrant: 1 VM running on any Linux distribution 

Look at the `readme.md` in the Iac Directory for instructions

2. Provision the VM with Ansible, which includes installing and running:
  - language runtime
  - database
  - your application
  - health check of your application

Look at the `readme.md` in the Iac/playbooks directory

### 4. Build Docker image of your application

1. Docker image of the application created via GitHubActions
2. Image pushed to Azure Container Registry


### 5. Make container orchestration using Docker Compose

Branch : `compose_on_k8s`

`docker-compose.yml`: file for the Avocado API running on Kubernetes, using MongoDB as its database.

Look at the `docker-compose_readme.md` in the Iac/flask-api directory for more information.

Graph of the docker-compose file : `docker-compose.svg`

On this branch we convert the Docker Compose to Kubernetes resources to deploy the application on a Azure Kubernetes Service.

### 6. Make docker orchestration using Kubernetes

Branch : `main`

`avocado-api.yaml` Kubernetes Manifest YAML file :
  - deployments
  - services
  - namespaces

Look at the `avocado-api_readme.md` for more information about the manifest file.

Graphes of the manifest file present in the root directory. 

On this branch we use a Kubernetes Manifest YAML file to deploy the application on a Azure Kubernetes Service with Prometeus , Grafana and the possibility to also install Istio - by uncommenting lines .

The docker image is pushed to Azure Container Registry but it's also possible to push it to DockerHub - by uncommenting lines .

### 7. Make a service mesh using Istio

1. Deploy your application using Istio

In this project , we didn't use Istio even if it was possible but we setup the possibility to install it during the deploy phase. 

We used Azure Solution: Open Service Mesh.

2. Create configuration:
  - route requests between 2 different versions of your app
  - traffic shifting between 2 different versions of your app

  WE DIDN'T COMPLETE THIS PART OF THE EXERCICE
  
### 8. Implement Monitoring to your containerized application

1. Install Prometheus and Grafana to your K8s cluster

It was done in the deployment phase of the workflow

2. Set up monitoring with Prometheus:

  - Prometheus should contact the application (eg. health check endpoint) and pull its status
  - You should be able to see the status of the application on Prometheus

  WE DIDN'T COMPLETE THIS PART OF THE EXERCICE but to
  make Prometheus contact our application's health check endpoint and pull its status, we needed to expose the health check status as a Prometheus metric in our application and configure Prometheus to scrape that metric.


3. Set up monitoring with Grafana:

  - Link it to the Prometheus server and display the monitored applications

  We linked Graphana to Prometheus server and also Azure Monitor ( so we had 2 Data Sources)

  We also setup a Graphana Cloud Monitoring ( for that it was also necessary to expose Prometheus servia via a Load Balancer)

  - Create alerts and trigger them by shutting down your applications.

  We created a NoData Alert which was triggered by stopping the application ( or cluster ). # a vérifier
  Plus de détails sur l'alerte et photo


## Structure

Here is an example structure of oour project repository:

```
.github/
flask-api/
  modules/
  tests/
  service/
  README.md
  package.json
  Dockerfile
  requirements.txt
  setup.py
  ...
iac/
  Vagrantfile
  playbooks/
k8s/
istio/
image/
.gitignore
.whitesource
README.md
avocado-api.yaml
avocado-api-readme.md
manifest.svg
renovate.json
...
```