# Flask API Test GitHub Action Workflow
GitHub Actions workflow for testing a Flask API using a MongoDB backend.

The workflow is triggered on `push` and `pull_request` events for the `main` branch.

## Workflow Overview
The workflow includes the following steps:
1. Checkout code
2. Set up Python environment
3. Cache pip packages
4. Install dependencies
5. Install coverage dependencies
6. Start Flask API
7. Wait for API to start up
8. Test if API is running
9. Print directory structure
10. Run tests with coverage
11. Upload coverage to Codecov

### Prerequisites
- A GitHub repository with a Flask API
- MongoDB server configuration
- GitHub Secrets for the following variables:
  - MONGO_DATABASE
  - MONGO_USERNAME
  - MONGO_PASSWORD
  - CODECOV_TOKEN

## Workflow Details
The workflow first sets up the Python environment and caches the pip packages.

It then installs the dependencies for the Flask API and the coverage tool.

The workflow starts the Flask API and waits for it to be fully operational before running a simple health check using `curl`.

t then prints the directory structure and runs the tests with coverage using `pytest`.

Finally, the workflow uploads the coverage report to Codecov using the `codecov-action` and fails the CI if there is an error in the process.
