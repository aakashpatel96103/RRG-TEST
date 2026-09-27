# Employee Management System – CI/CD Pipeline

A full-stack Employee Management System with JWT authentication, CRUD operations, automated testing, Docker, Kubernetes, health checks, versioned artifacts, monitoring hooks and security scanning.

## 1. Local backend

Windows PowerShell:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:JWT_SECRET="local-development-secret"
uvicorn app.main:app --reload --port 8000
```

API: http://localhost:8000  
Swagger: http://localhost:8000/docs

Register a user in Swagger using POST `/auth/register`, then login using POST `/auth/login`.

## 2. Local frontend

Open another PowerShell:

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal.

## 3. Run tests

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest -q
```

## 4. Docker Compose

Install Docker Desktop, then from the project root:

```powershell
docker compose up --build
```

Frontend: http://localhost:3000  
Backend: http://localhost:8000/docs

## 5. Kubernetes

Build/push images first, then replace `YOUR_GITHUB_USERNAME` in `k8s/backend.yaml` and `k8s/frontend.yaml`.

```powershell
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml
kubectl apply -f k8s/monitoring.yaml
kubectl get pods -n employee-system
kubectl get services -n employee-system
```

Check rollout:

```powershell
kubectl rollout status deployment/employee-backend -n employee-system
kubectl rollout status deployment/employee-frontend -n employee-system
```

## 6. CI/CD

Push to GitHub:

```powershell
git init
git add .
git commit -m "Initial Employee Management CI/CD project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/employee-management-system.git
git push -u origin main
```

GitHub Actions runs:
1. Backend tests
2. Frontend build
3. Trivy security scan
4. Docker image build
5. GHCR image push
6. Versioned GitHub artifact creation

## 7. Versioning

Create a release tag:

```powershell
git tag v1.0.0
git push origin v1.0.0
```

Recommended versions:
- v1.0.0 – initial release
- v1.0.1 – bug fix
- v1.1.0 – new feature

## 8. Monitoring

The Kubernetes configuration includes a metrics service endpoint that can be connected to Prometheus/Grafana. For a production deployment, add Prometheus Operator or kube-prometheus-stack and expose application metrics using a dedicated `/metrics` endpoint.

## 9. Security

The CI workflow runs Trivy filesystem scanning. Docker image scanning can be added after image creation. Never commit real JWT secrets, database passwords or cloud credentials. Replace the example Kubernetes secret before production use.

## Practical mapping

P1 Git workflow – Git branches, commits and tags  
P2 Build automation – npm/Python build  
P3 CI pipeline – GitHub Actions  
P4 Automated testing – Pytest  
P5 Deployment pipeline – CI/CD workflow  
P6 Docker – backend/frontend images  
P7 Kubernetes – deployments/services  
P8 Container lifecycle – rollout/status/logs  
P9 Multi-container application – frontend + backend  
P10 Health checks – `/health`, `/ready`, probes  
P11 Monitoring – metrics service + Prometheus/Grafana integration  
P12 Security validation – Trivy and dependency checks
