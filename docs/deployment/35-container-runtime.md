# Container Runtime

## Backend

The backend is packaged as a Python 3.11 container exposing FastAPI on port 8000.

## Frontend

The frontend is built with Vite and served from Nginx as static assets.

## Production flow

GitHub Actions -> build -> security scan -> ECR -> ECS/Fargate -> smoke tests.

## Security

No credentials are copied into either image. Runtime configuration is injected by the deployment environment. Production releases should pin images by digest.
