CloudOps Hub
A containerized task-management application built to demonstrate practical Cloud and DevOps workflows, including Docker, Docker Compose, Kubernetes, PostgreSQL, automated testing, and CI/CD.

Architecture
<img width="998" height="1722" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/0fd37fb9-c79d-46d5-86dc-4937321e67fc" />

PostgreSQL Database
Technology Stack
- Frontend: React, Vite, Nginx
- Backend: Python, Flask
- Database: PostgreSQL
- Containerization: Docker
- Local orchestration: Docker Compose
- Container orchestration: Kubernetes, Minikube, kubectl
- CI/CD: GitHub Actions
- Testing: pytest
- Kubernetes manifest validation: Kubeconform
Features
- Task management through REST API endpoints
- PostgreSQL database integration
- Containerized frontend and backend
- Multi-container local deployment with Docker Compose
- Kubernetes deployments and services
- Persistent database storage
- Application health checks
- Automated testing and CI/CD workflow
Prerequisites
For the local Docker Compose setup:
- Git
- Docker Engine
- Docker Compose plugin
For Kubernetes deployment, you will also need:
- kubectl
- Minikube
Getting Started
1. Clone the repository
git clone https://github.com/Manoj-Sivanandharaja/cloudops-hub.git
cd cloudops-hub
2. Configure environment variables
Create your local environment file from the example:
cp .env.example .env
Open .env and set a strong local development password for POSTGRES_PASSWORD. Keep this file private and do not commit it.

Example .env format:
POSTGRES_DB=cloudops
POSTGRES_USER=cloudops_user
POSTGRES_PASSWORD=replace_with_a_local_password
Use your own local password in .env; the value above is only a placeholder.
3. Build and start the application
docker compose up --build -d
4. Check the container status
docker compose ps
5. Open the application
- Frontend: http://localhost:8081
- Backend health check: http://localhost:5000/api/health
- Tasks API: http://localhost:5000/api/tasks
The health endpoint should return a healthy status when the API and database connection are working.
6. Stop the application
docker compose down
To remove the Compose database volume as well:
docker compose down -v
Warning: docker compose down -v deletes the database volume and its stored data.

API Endpoints
Method	Endpoint	Purpose
GET	/	Root endpoint
GET	/api/health	Check API and database health
GET	/api/tasks	List tasks
POST	/api/tasks	Create a task
GET	/api/tasks/<task_id>	Retrieve a task
PUT	/api/tasks/<task_id>	Update a task
DELETE	/api/tasks/<task_id>	Delete a task


For POST and PUT requests, send the JSON fields expected by the backend implementation.
Run Tests
Install the backend dependencies and pytest:
python -m pip install -r backend/requirements.txt
python -m pip install pytest
Run the tests from the repository root:
PYTHONPATH=backend python -m pytest -v tests/
Kubernetes Deployment
The repository contains Kubernetes manifests in the k8s/ directory. Review the manifests before applying them to your cluster.
1. Start Minikube
minikube start
2. Create the local Kubernetes Secret
The Secret manifest containing credentials is intentionally not committed. Create k8s/secret.yaml locally, using the Secret name, keys, and namespace expected by k8s/app.yaml. Use your own credentials and do not commit the Secret file.
3. Apply the manifests
If the namespace manifest is named namespace.yaml, run:
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/app.yaml
If your manifest filenames differ, use the actual filenames in k8s/.
4. Check Kubernetes resources
kubectl get pods -n cloudops-hub
kubectl get services -n cloudops-hub
5. Access the frontend
minikube service frontend -n cloudops-hub --url
The frontend service is configured to use NodePort 30081 in this project. Use the URL printed by Minikube to open it.
Container Images
- Backend image: cloudops-hub-backend on Docker Hub
- Frontend image: cloudops-hub-frontend on Docker Hub
CI/CD
The GitHub Actions workflow is located in .github/workflows/.

Depending on the workflow configuration, it can run automated checks and build or publish container images. If the workflow publishes images to Docker Hub, configure the required repository secrets in GitHub Actions settings, using the exact names referenced by the workflow (for example, DOCKERHUB_USERNAME and DOCKERHUB_TOKEN if those are the names used in the file).

Never commit access tokens, passwords, or other secrets.
Security Notes
- Keep .env out of version control.
- Commit .env.example only with placeholder values.
- Keep Kubernetes Secret manifests containing credentials out of Git.
- Store CI/CD credentials in repository secrets.
- Do not publish real passwords or access tokens in screenshots, logs, or documentation.
Project Scope
CloudOps Hub demonstrates application containerization, database integration, health checks, local orchestration, Kubernetes deployment, and CI/CD practices. A public AWS deployment is not included unless you deploy and configure it separately.
Author
Manoj Sivanandharaja
- GitHub: Manoj-Sivanandharaja
- Repository: CloudOps Hub
