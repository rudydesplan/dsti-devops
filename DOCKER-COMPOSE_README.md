# Avocado API - Docker Compose 
This docker-compose.yaml file is used to define and configure the services required to deploy the Avocado API with a MongoDB backend.

Docker Compose allows for easily managing multi-container Docker applications, and this file outlines the necessary components and settings.

Here is a breakdown of the main sections of the docker-compose.yaml file:

## Version
The version field specifies the version of the Docker Compose file format being used:

```ruby
version: '3.8'
```

## Services
The services section contains the definitions of the individual components of the application:

### MongoDB Database
The MongoDB container is based on the official MongoDB 4.4 image:
```ruby
mongo:
  image: "mongo:4.4"
  container_name: "mongo"
```
It maps the host port 27017 to the container port 27017, which is the default MongoDB port:
```ruby
ports:
  - "27017:27017"
```
Environment variables are used to configure the MongoDB instance:
```ruby
environment:
  MONGO_INITDB_DATABASE: avocado_db
  MONGO_INITDB_ROOT_USERNAME: ${MONGODB_ROOT_USERNAME}
  MONGO_INITDB_ROOT_PASSWORD: ${MONGODB_ROOT_PASSWORD}
  MONGO_INITDB_USERNAME: ${MONGODB_USERNAME}
  MONGO_INITDB_PASSWORD: ${MONGODB_PASSWORD}
  MONGO_INITDB_EXTRA_ARGS: --authenticationDatabase admin
```
A volume is mounted for initialization scripts, allowing you to customize the MongoDB instance:
```ruby
volumes:
  - ./mongo-init-scripts:/docker-entrypoint-initdb.d/
```
The MongoDB service is connected to the backend network:
```ruby
networks:
  - backend
```

### Flask API
The Flask API container is built using a custom Dockerfile located in the flask-api folder:
```ruby
app:
  build: ./flask-api
  container_name: avocado_api
  ...
```
The host port 5000 is mapped to the container port 5000, which is the default Flask API port:
```ruby
ports:
  - "5000:5000"
```
The MONGODB_URI environment variable is set to connect to the MongoDB service:
```ruby
environment:
  MONGODB_URI: "mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongo:27017/avocado_db?retryWrites=true&w=majority"
```
The Flask API service depends on the MongoDB service, ensuring that the database is started before the API:
```ruby
depends_on:
  - mongo
```
A volume is mounted to the datasets folder, allowing you to manage the dataset files:
```ruby
volumes:
  - ./datasets:/app/datasets
```
The Flask API service is connected to the backend network:
```ruby
networks:
  - backend
```

## Networks
The backend network is used to connect the Flask API and MongoDB services, facilitating communication between them:
```ruby
networks:
  backend:
    driver: bridge
```
