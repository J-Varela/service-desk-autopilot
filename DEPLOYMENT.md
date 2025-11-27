# Service Desk Autopilot - Deployment Guide

## Prerequisites

- Docker and Docker Compose installed
- Azure OpenAI or GitHub Models access
- Environment variables configured

## Quick Start

### 1. Configure Environment

```bash
# Copy the example environment file
cp .env.example backend/.env

# Edit backend/.env with your actual credentials
```

### 2. Local Development

```bash
# Activate virtual environment
.\serviceEnv\Scripts\Activate.ps1

# Run the server
uvicorn backend.orchestrator.main:app --reload
```

### 3. Docker Deployment

```bash
# Build the image
docker build -t service-desk-autopilot .

# Run with docker-compose
docker-compose up -d

# Check logs
docker-compose logs -f
```

## Deployment Options

### Option 1: Azure Container Instances

```bash
# Login to Azure
az login

# Create resource group
az group create --name service-desk-rg --location eastus

# Deploy container
az container create \
  --resource-group service-desk-rg \
  --name service-desk-autopilot \
  --image service-desk-autopilot:latest \
  --dns-name-label service-desk-app \
  --ports 8000 \
  --environment-variables \
    AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT \
    AZURE_OPENAI_API_KEY=$AZURE_OPENAI_API_KEY
```

### Option 2: Azure App Service

```bash
# Create App Service plan
az appservice plan create \
  --name service-desk-plan \
  --resource-group service-desk-rg \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --resource-group service-desk-rg \
  --plan service-desk-plan \
  --name service-desk-autopilot \
  --deployment-container-image-name service-desk-autopilot:latest
```

### Option 3: Kubernetes

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: service-desk-autopilot
spec:
  replicas: 2
  selector:
    matchLabels:
      app: service-desk
  template:
    metadata:
      labels:
        app: service-desk
    spec:
      containers:
      - name: service-desk
        image: service-desk-autopilot:latest
        ports:
        - containerPort: 8000
        env:
        - name: AZURE_OPENAI_ENDPOINT
          valueFrom:
            secretKeyRef:
              name: service-desk-secrets
              key: azure-endpoint
```

## Environment Variables

Required:
- `AZURE_OPENAI_ENDPOINT` - Your Azure OpenAI endpoint
- `AZURE_OPENAI_API_KEY` - Your Azure OpenAI API key

Optional:
- `GITHUB_TOKEN` - GitHub Models token
- `LOG_LEVEL` - Logging level (default: INFO)
- `ENVIRONMENT` - Environment name (development/production)

## Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "ok",
  "environment": "production",
  "azure_configured": true
}
```

## Monitoring

Check application logs:
```bash
# Docker
docker-compose logs -f

# Azure Container Instances
az container logs --resource-group service-desk-rg --name service-desk-autopilot

# Kubernetes
kubectl logs -f deployment/service-desk-autopilot
```

## Scaling

### Docker Compose
```bash
docker-compose up -d --scale service-desk=3
```

### Kubernetes
```bash
kubectl scale deployment service-desk-autopilot --replicas=5
```

## Security Checklist

- [ ] Never commit `.env` file
- [ ] Use Azure Key Vault for secrets in production
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS appropriately
- [ ] Set up authentication/authorization
- [ ] Enable audit logging
- [ ] Regular security updates

## Troubleshooting

### Container won't start
```bash
docker logs service-desk-autopilot
```

### Health check failing
- Verify environment variables are set
- Check Azure OpenAI endpoint is accessible
- Review application logs

### High latency
- Check AI model endpoint performance
- Consider caching strategies
- Scale horizontally if needed
