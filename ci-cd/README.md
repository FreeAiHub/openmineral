# OpenMineral CI/CD Pipeline

This directory contains CI/CD pipeline configurations for automated testing and deployment of the OpenMineral platform.

## Structure

- `.github/workflows/` - GitHub Actions workflows
  - `test.yml` - Automated testing workflow
  - `build.yml` - Build and packaging workflow
  - `deploy.yml` - Deployment workflow
- `docker/` - Docker configuration files
  - `Dockerfile` - Main Docker configuration
  - `docker-compose.yml` - Multi-container Docker setup
- `kubernetes/` - Kubernetes deployment configurations
  - `manifests/` - Kubernetes manifests
  - `helm/` - Helm charts for deployment
- `scripts/` - Deployment and automation scripts
  - `deploy.sh` - Deployment scripts
  - `test.sh` - Testing scripts