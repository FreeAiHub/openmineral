# 🚀 Быстрый старт с OpenMineral

## Демо-версия за 5 минут

*"От идеи до работающего AI-powered trading приложения за считанные минуты"*

---

## 🎯 Что вы получите через 5 минут

- ✅ **Работающий backend** с FastAPI и AI интеграцией
- ✅ **Современный frontend** с React 18 и real-time обновлениями
- ✅ **Базу данных** с тестовыми данными о сделках
- ✅ **AI-ассистента** для анализа торговых решений
- ✅ **Полную инфраструктуру** для локальной разработки

## 📋 Предварительные требования

### Обязательные компоненты
- **Python 3.11+** - основной язык разработки
- **Node.js 20+** - для frontend разработки
- **Docker 24+** - для контейнеризации
- **Git** - система контроля версий

### Рекомендуемые инструменты
- **VS Code** с расширениями Python и TypeScript
- **Cursor IDE** - для AI-assisted разработки
- **Postman** или **Insomnia** - для тестирования API

---

## ⚡ Экспресс-установка (Docker)

### Шаг 1: Клонирование репозитория
```bash
git clone https://github.com/openmineral/platform.git
cd openmineral
```

### Шаг 2: Запуск с Docker Compose
```bash
# Запуск всех сервисов
docker compose up -d

# Проверка статуса
docker compose ps
```

### Шаг 3: Открытие приложения
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432 (PostgreSQL)

### Шаг 4: Тестирование AI функций
```bash
# Тест AI анализа сделки
curl -X POST "http://localhost:8000/api/deals/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "commodity": "Copper",
    "quantity": 1000,
    "price": 8500,
    "counterparty": "Global Mining Corp"
  }'
```

---

## 🛠️ Ручная установка (для разработчиков)

### Backend установка

```bash
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r backend/requirements.txt

# Настройка переменных окружения
cp backend/.env.example backend/.env
# Отредактируйте .env файл с вашими API ключами

# Запуск базы данных (если не используете Docker)
docker run -d --name postgres -p 5432:5432 \
  -e POSTGRES_PASSWORD=devpassword \
  postgres:16

# Миграции базы данных
cd backend
alembic upgrade head

# Запуск сервера
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend установка

```bash
# Установка зависимостей
cd frontend
npm install
# или
pnpm install

# Запуск в режиме разработки
npm run dev
# или
pnpm dev
```

---

## 🎮 Интерактивная демонстрация

### Создание первой сделки

```bash
# 1. Создание пользователя
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "trader@openmineral.dev",
    "password": "demo123",
    "full_name": "Demo Trader"
  }'

# 2. Авторизация
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "trader@openmineral.dev",
    "password": "demo123"
  }'

# 3. Создание сделки
curl -X POST "http://localhost:8000/api/deals/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Copper Purchase Agreement",
    "description": "Strategic copper purchase for Q1 2026",
    "commodity": "Copper",
    "quantity": 5000,
    "price": 8500.0,
    "counterparty": "Chilean Mining Corp"
  }'

# 4. AI анализ сделки
curl -X POST "http://localhost:8000/api/analysis/deal/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Работа с рынком в реальном времени

```python
# Python клиент для real-time данных
import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    print(f"Market Update: {data['symbol']} @ ${data['price']}")

ws = websocket.WebSocketApp(
    "ws://localhost:8000/api/market/stream",
    on_message=on_message
)
ws.run_forever()
```

---

## 🤖 AI Features демонстрация

### LangGraph Workflow пример

```python
from openmineral import TradingWorkflow

# Создание AI-powered workflow
workflow = TradingWorkflow()

# Анализ сделки с AI
result = await workflow.analyze_deal({
    "commodity": "Lithium",
    "quantity": 10000,
    "price": 25000,
    "market_conditions": "Bullish due to EV demand"
})

print(f"AI Decision: {result['decision']}")
print(f"Confidence: {result['confidence']}%")
print(f"Risk Assessment: {result['risk_level']}")
```

### Vector Search для документов

```python
from openmineral import DocumentSearch

# Поиск релевантных торговых документов
search = DocumentSearch()
results = await search.semantic_search(
    "copper supply chain disruptions China"
)

for doc in results:
    print(f"Document: {doc['title']}")
    print(f"Relevance: {doc['score']}")
    print(f"Summary: {doc['ai_summary']}\n")
```

---

## 📊 Мониторинг и отладка

### Логи приложения
```bash
# Просмотр логов всех сервисов
docker compose logs -f

# Логи конкретного сервиса
docker compose logs -f backend

# Логи с фильтром по уровню
docker compose logs | grep ERROR
```

### API тестирование
```bash
# Health check
curl http://localhost:8000/api/health

# API schema
curl http://localhost:8000/openapi.json

# Database connection test
curl http://localhost:8000/api/debug/db-status
```

### Performance monitoring
```bash
# Prometheus metrics
curl http://localhost:9090/metrics

# Application metrics
curl http://localhost:8000/metrics

# System resources
docker stats
```

---

## 🔧 Расширение функционала

### Добавление нового AI агента

```python
# backend/services/ai/agents/custom_agent.py
from langchain.agents import Tool
from openmineral.ai import BaseAgent

class CommodityAnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Commodity Analyst",
            role="Analyze commodity market trends and predict price movements"
        )

        self.tools = [
            Tool(
                name="MarketData",
                func=self.get_market_data,
                description="Get real-time market data for commodities"
            ),
            Tool(
                name="SentimentAnalysis",
                func=self.analyze_sentiment,
                description="Analyze market sentiment from news and social media"
            )
        ]

    async def analyze(self, commodity: str) -> dict:
        """Main analysis method"""
        market_data = await self.get_market_data(commodity)
        sentiment = await self.analyze_sentiment(commodity)

        return {
            "commodity": commodity,
            "trend": self.predict_trend(market_data, sentiment),
            "confidence": self.calculate_confidence(market_data, sentiment),
            "recommendations": self.generate_recommendations()
        }
```

### Кастомный React компонент

```typescript
// frontend/components/TradingChart.tsx
import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';

interface TradingChartProps {
  symbol: string;
  timeframe?: '1D' | '1W' | '1M';
}

export function TradingChart({ symbol, timeframe = '1D' }: TradingChartProps) {
  const { data: chartData, isLoading } = useQuery({
    queryKey: ['chart', symbol, timeframe],
    queryFn: () => api.getChartData(symbol, timeframe),
    refetchInterval: 5000, // Real-time updates
  });

  if (isLoading) return <div>Loading chart...</div>;

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={chartData}>
        <XAxis dataKey="time" />
        <YAxis domain={['dataMin - 5', 'dataMax + 5']} />
        <Tooltip />
        <Line
          type="monotone"
          dataKey="price"
          stroke="#1890ff"
          strokeWidth={2}
          dot={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

---

## 🚀 Production развертывание

### AWS EKS развертывание

```bash
# Инициализация Terraform
cd infrastructure/aws
terraform init
terraform workspace select prod
terraform plan
terraform apply

# Деплой приложения
kubectl apply -f k8s/
kubectl rollout status deployment/openmineral-backend
```

### Azure AKS развертывание

```bash
# Azure CLI
az aks create --resource-group openmineral-prod \
  --name openmineral-cluster \
  --node-count 3 \
  --enable-addons monitoring

# Деплой
kubectl apply -f k8s/
```

---

## 📚 Следующие шаги

### Для новичков
1. **Изучите API документацию** - http://localhost:8000/docs
2. **Попробуйте демо-скрипты** из папки `scripts/demo/`
3. **Почитайте портфолио проектов** - `portfolio-projects/`
4. **Присоединяйтесь к сообществу** - Discord/Github Discussions

### Для разработчиков
1. **Изучите архитектуру** - `ARCHITECTURE.md`
2. **Посмотрите на тесты** - `backend/tests/`
3. **Прочитайте roadmap** - `ROADMAP.md`
4. **Внесите свой вклад** - `CONTRIBUTING.md`

### Для бизнеса
1. **Оцените возможности** - `PORTFOLIO.md`
2. **Посмотрите на конкурентов** - `competitive-intelligence/`
3. **Свяжитесь с командой** - team@openmineral.dev

---

*"OpenMineral - это не просто код. Это будущее commodity trading в ваших руках."* 🚀
