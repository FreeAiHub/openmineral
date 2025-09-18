# 🚀 Руководство по развертыванию OpenMineral

## 📋 Обзор

Данное руководство описывает процесс развертывания платформы OpenMineral в различных окружениях: от локальной разработки до production deployment.

## 🛠️ Предварительные требования

### Минимальные системные требования
- **CPU**: 4 cores (8 рекомендуется)
- **RAM**: 8GB (16GB рекомендуется)
- **Диск**: 50GB свободного места
- **ОС**: Linux/macOS/Windows с WSL2

### Необходимое ПО
- **Docker**: 24.0+
- **Docker Compose**: 2.20+
- **Node.js**: 20+ (для локальной разработки)
- **Python**: 3.11+ (для локальной разработки)
- **Git**: 2.40+

## 🏠 Локальное развертывание

### 1. Клонирование репозитория
```bash
git clone https://github.com/FreeAiHub/openmineral.git
cd openmineral
```

### 2. Настройка переменных окружения
```bash
# Копирование примера конфигурации
cp .env.example .env

# Редактирование конфигурации
nano .env
```

### 3. Запуск через Docker Compose
```bash
# Сборка и запуск всех сервисов
docker compose up -d --build

# Проверка статуса сервисов
docker compose ps

# Просмотр логов
docker compose logs -f
```

### 4. Проверка работоспособности
```bash
# Backend API
curl http://localhost:8000/api/health

# Frontend
open http://localhost:3000

# BC Flow приложение
open http://localhost:3001

# API документация
open http://localhost:8000/docs
```

## ☁️ Cloud развертывание

### AWS EKS
```bash
# 1. Создание кластера через Terraform
cd infrastructure/aws
terraform init
terraform plan -var-file="prod.tfvars"
terraform apply

# 2. Настройка kubectl
aws eks update-kubeconfig --region us-west-2 --name openmineral-prod

# 3. Развертывание приложения
kubectl apply -f kubernetes/manifests/

# 4. Проверка статуса
kubectl get pods -n openmineral
kubectl get services -n openmineral
```

### Azure AKS
```bash
# 1. Создание кластера
cd infrastructure/azure
terraform init
terraform apply

# 2. Настройка kubectl
az aks get-credentials --resource-group openmineral-rg --name openmineral-aks

# 3. Развертывание
kubectl apply -f kubernetes/manifests/
```

## 🔧 Конфигурация сервисов

### Backend (FastAPI)
```yaml
# docker-compose.yml
backend:
  environment:
    - DATABASE_URL=postgresql://user:pass@db:5432/openmineral
    - REDIS_URL=redis://redis:6379
    - CHROMA_HOST=chromadb
    - OPENAI_API_KEY=${OPENAI_API_KEY}
    - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
```

### Frontend (React)
```yaml
frontend:
  environment:
    - NEXT_PUBLIC_API_URL=http://localhost:8000
    - NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### База данных
```yaml
postgres:
  environment:
    - POSTGRES_DB=openmineral
    - POSTGRES_USER=openmineral
    - POSTGRES_PASSWORD=${DB_PASSWORD}
  volumes:
    - postgres_data:/var/lib/postgresql/data
```

## 🔐 Безопасность

### SSL/TLS сертификаты
```bash
# Генерация самоподписанных сертификатов для разработки
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Production: использование Let's Encrypt
certbot certonly --webroot -w /var/www/html -d api.openmineral.com
```

### Секреты в Kubernetes
```bash
# Создание секретов
kubectl create secret generic openmineral-secrets \
  --from-literal=database-password=${DB_PASSWORD} \
  --from-literal=openai-api-key=${OPENAI_API_KEY} \
  --from-literal=anthropic-api-key=${ANTHROPIC_API_KEY}
```

## 📊 Мониторинг и логирование

### Prometheus + Grafana
```bash
# Установка через Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack

# Доступ к Grafana
kubectl port-forward svc/prometheus-grafana 3000:80
```

### Централизованное логирование
```bash
# ELK Stack
helm repo add elastic https://helm.elastic.co
helm install elasticsearch elastic/elasticsearch
helm install kibana elastic/kibana
helm install filebeat elastic/filebeat
```

## 🔄 CI/CD Pipeline

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/backend backend=${{ env.IMAGE_TAG }}
          kubectl rollout status deployment/backend
```

## 🧪 Тестирование развертывания

### Smoke тесты
```bash
#!/bin/bash
# scripts/smoke-test.sh

echo "🧪 Запуск smoke тестов..."

# Проверка backend
if curl -f http://localhost:8000/api/health; then
  echo "✅ Backend работает"
else
  echo "❌ Backend недоступен"
  exit 1
fi

# Проверка frontend
if curl -f http://localhost:3000; then
  echo "✅ Frontend работает"
else
  echo "❌ Frontend недоступен"
  exit 1
fi

# Проверка парсера
if curl -f http://localhost:8000/api/bc-parser/parser-info; then
  echo "✅ BC Parser работает"
else
  echo "❌ BC Parser недоступен"
  exit 1
fi

echo "🎉 Все тесты прошли успешно!"
```

### Load тесты
```bash
# Установка k6
brew install k6

# Запуск нагрузочного тестирования
k6 run scripts/load-test.js
```

## 🔧 Troubleshooting

### Частые проблемы

#### 1. Проблемы с базой данных
```bash
# Проверка подключения
docker compose exec backend python -c "
from sqlalchemy import create_engine
engine = create_engine('postgresql://user:pass@db:5432/openmineral')
print('DB connection:', engine.execute('SELECT 1').scalar())
"
```

#### 2. Проблемы с ChromaDB
```bash
# Перезапуск ChromaDB
docker compose restart chromadb

# Проверка логов
docker compose logs chromadb
```

#### 3. Проблемы с памятью
```bash
# Увеличение лимитов в docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
```

### Полезные команды
```bash
# Просмотр использования ресурсов
docker stats

# Очистка неиспользуемых образов
docker system prune -a

# Бэкап базы данных
docker compose exec postgres pg_dump -U openmineral openmineral > backup.sql

# Восстановление базы данных
docker compose exec -T postgres psql -U openmineral openmineral < backup.sql
```

## 📈 Масштабирование

### Горизонтальное масштабирование
```yaml
# kubernetes/manifests/backend-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Вертикальное масштабирование
```yaml
# Увеличение ресурсов для подов
resources:
  requests:
    memory: "1Gi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "1000m"
```

## 🔄 Обновления

### Rolling Updates
```bash
# Обновление образа
kubectl set image deployment/backend backend=openmineral/backend:v1.1.0

# Откат к предыдущей версии
kubectl rollout undo deployment/backend

# Проверка статуса обновления
kubectl rollout status deployment/backend
```

### Blue-Green Deployment
```bash
# Создание green окружения
kubectl apply -f kubernetes/manifests/green/

# Переключение трафика
kubectl patch service backend -p '{"spec":{"selector":{"version":"green"}}}'

# Удаление blue окружения
kubectl delete -f kubernetes/manifests/blue/
```

---

**Версия**: v1.0.0 | **Последнее обновление**: 2025-09-18
