# CloudOps Hub

A containerized task-management application built to demonstrate practical Cloud and DevOps workflows using Docker, Docker Compose, Kubernetes, PostgreSQL, automated testing, and CI/CD.

## Architecture

<img width="998" height="1722" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/1e02fa9d-414b-444e-ac5e-c3c19406b8b9" />


## Application Flow

1. **Frontend:** React application served through Nginx.
2. **Backend:** Flask REST API handles application requests.
3. **Database:** PostgreSQL stores task data.
4. **Containerization:** Docker packages the application services.
5. **Orchestration:** Docker Compose and Kubernetes manage deployment environments.
6. **CI/CD:** GitHub Actions automates configured testing and build workflows.

## Application Screenshot

<img width="3200" height="1800" alt="cloudops-frontend" src="https://github.com/user-attachments/assets/5c6f5680-2ee6-4f75-b075-5b53e5e3569b" />


## Technology Stack

| Category | Technologies |
|---|---|
| Frontend | React, Vite, Nginx |
| Backend | Python, Flask |
| Database | PostgreSQL |
| Containerization | Docker |
| Local orchestration | Docker Compose |
| Container orchestration | Kubernetes, Minikube, kubectl |
| CI/CD | GitHub Actions |
| Testing | pytest |
| Manifest validation | Kubeconform |

## Features

- Task management through REST API endpoints
- PostgreSQL database integration
- Containerized frontend and backend
- Multi-container deployment using Docker Compose
- Kubernetes deployments and services
- Persistent database storage
- Application health checks
- Automated testing and CI/CD workflow

## Prerequisites

For local deployment:

- Git
- Docker Engine
- Docker Compose plugin

For Kubernetes deployment, you will also need:

- kubectl
- Minikube

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Manoj-Sivanandharaja/cloudops-hub.git
cd cloudops-hub
```

### 2. Configure Environment Variables

Create your local environment file:

```bash
cp .env.example .env
```

Edit `.env` and set your local PostgreSQL password.

Example configuration:

```dotenv
POSTGRES_DB=cloudops
POSTGRES_USER=cloudops_user
POSTGRES_PASSWORD=replace_with_a_local_password
```

Replace the example password with your own local development password.

**Security:** Never commit `.env` or real credentials to GitHub.

### 3. Build and Start the Application

```bash
docker compose up --build -d
```

### 4. Verify Container Status

```bash
docker compose ps
```

### 5. Access the Application

| Component | URL |
|---|---|
| Frontend | http://localhost:8081 |
| Backend health check | http://localhost:5000/api/health |
| Tasks API | http://localhost:5000/api/tasks |

The health endpoint should report a healthy status when the API and database connection are working.

### 6. Stop the Application

```bash
docker compose down
```

To remove the database volume and its stored data as well:

```bash
docker compose down -v
```

> **Warning:** The `-v` option deletes the database volume and its stored data.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/api/health` | Check API and database health |
| GET | `/api/tasks` | List tasks |
| POST | `/api/tasks` | Create a task |
| GET | `/api/tasks/<task_id>` | Retrieve a task |
| PUT | `/api/tasks/<task_id>` | Update a task |
| DELETE | `/api/tasks/<task_id>` | Delete a task |

For POST and PUT requests, provide the JSON fields expected by the backend implementation.

## Run Tests

Install the backend dependencies and pytest:

```bash
python -m pip install -r backend/requirements.txt
python -m pip install pytest
```

Run the tests from the repository root:

```bash
PYTHONPATH=backend python -m pytest -v tests/
```

## Kubernetes Deployment

The Kubernetes manifests are located in the `k8s/` directory.

### 1. Start Minikube

```bash
minikube start
```

### 2. Configure the Kubernetes Secret

Create the local `k8s/secret.yaml` file using the Secret name, keys, and namespace expected by `k8s/app.yaml`.

Use your own credentials. Do not commit the Secret file.

### 3. Apply the Manifests

If these filenames exist in your repository, run:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/app.yaml
```

### 4. Verify Kubernetes Resources

```bash
kubectl get pods -n cloudops-hub
kubectl get services -n cloudops-hub
```

### 5. Access the Frontend

```bash
minikube service frontend -n cloudops-hub --url
```

The frontend is configured to use NodePort `30081`. Open the URL returned by Minikube.

## Container Images

- **Backend:** [cloudops-hub-backend on Docker Hub](https://hub.docker.com/r/manoj03092005/cloudops-hub-backend)
- **Frontend:** [cloudops-hub-frontend on Docker Hub](https://hub.docker.com/r/manoj03092005/cloudops-hub-frontend)

## CI/CD

The GitHub Actions workflows are located in `.github/workflows/`.

The configured workflows may run automated tests, validate Kubernetes manifests, build container images, or publish images to Docker Hub.

If image publishing is enabled, configure the repository secrets required by the workflow, such as `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` if those are the names used in the workflow file.

Never commit passwords, tokens, or other secrets.

## Security Notes

- Keep `.env` out of version control.
- Commit `.env.example` with placeholder values only.
- Keep Kubernetes Secret manifests containing credentials out of Git.
- Store CI/CD credentials in GitHub repository secrets.
- Do not expose passwords or access tokens in screenshots or logs.

## Project Scope

CloudOps Hub demonstrates containerization, database integration, application health checks, local orchestration, Kubernetes deployment, and CI/CD practices.

A public AWS deployment is not included unless deployed and configured separately.

## Author

**Manoj Sivanandharaja**

- **GitHub:** [Manoj-Sivanandharaja](https://github.com/Manoj-Sivanandharaja)
- **Repository:** [CloudOps Hub](https://github.com/Manoj-Sivanandharaja/cloudops-hub)
