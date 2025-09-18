# 📡 OpenMineral API - Примеры использования

## 🎯 Обзор API

OpenMineral предоставляет RESTful API для управления commodity trading операциями, включая парсинг документов, управление сделками, анализ рисков и AI-powered аналитику.

**Base URL**: `http://localhost:8000` (локальная разработка)
**Production URL**: `https://api.openmineral.com`

## 🔐 Аутентификация

```bash
# Получение токена доступа
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo@openmineral.com",
    "password": "demo123"
  }'

# Использование токена в запросах
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  "http://localhost:8000/api/deals"
```

## 📄 Business Confirmation Parser API

### 1. Информация о парсере
```bash
curl "http://localhost:8000/api/bc-parser/parser-info"
```

**Ответ:**
```json
{
  "parser_name": "OpenMineral BC Parser",
  "version": "1.0.0",
  "supported_formats": [".txt", ".docx", ".doc"],
  "extracted_fields": [
    "date", "seller", "buyer", "material", "quantity",
    "delivery_terms", "shipment_period", "tc_rate", "rc_rate",
    "pricing_basis", "quotational_period", "assay_data",
    "payment_terms", "wsmd_terms"
  ],
  "description": "Парсер для извлечения структурированных данных из Business Confirmation документов"
}
```

### 2. Парсинг примера документа
```bash
curl "http://localhost:8000/api/bc-parser/parse-example"
```

**Ответ:**
```json
{
  "success": true,
  "message": "Пример Business Confirmation распарсен",
  "data": {
    "document_type": "business_confirmation",
    "parsed_at": "2025-09-18T14:19:58.123176",
    "data": {
      "basic_info": {
        "date": "December 14th, 2021",
        "seller": "Open Mineral",
        "buyer": "Company A, John Materials",
        "material": "Lead concentrate of Akzhal mine, Kazakhstan"
      },
      "commercial_terms": {
        "quantity": "1500 dmt +/- 10% in seller's option",
        "delivery_terms": "DAP ALASHANKOU In big bags or in open railcars",
        "shipment_period": "To be shipped evenly from Dec 2023 to Mar 2024",
        "tc_rate": "320.00",
        "rc_rate": "5.00",
        "pricing_basis": "At LME Lead Cash Seller Settlement Price",
        "quotational_period": "M+3, basis RWB shipped date"
      },
      "quality_specs": {
        "assay_data": [
          {"element": "Zn", "value": "9%", "unit": "%"},
          {"element": "Pb", "value": "65%", "unit": "%"},
          {"element": "Cu", "value": "0.2%", "unit": "%"},
          {"element": "Au", "value": "0.1", "unit": "g/t"},
          {"element": "Ag", "value": "815", "unit": "g/t"}
        ]
      },
      "payment_terms": {
        "prepayment": "30% of the provisional value",
        "provisional": "95% of the provisional value",
        "final": "100% of Final Value"
      }
    }
  }
}
```

### 3. Парсинг текста
```bash
curl -X POST "http://localhost:8000/api/bc-parser/parse-text" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Business Confirmation\nDate: January 15th, 2024\nSeller: OpenMineral Trading Ltd\nBuyer: Global Metals Corp\nMaterial: Copper concentrate\nQuantity: 2000 dmt +/- 5%\nTC: USD 85.00/dmt\nRC Cu: USD 0.085/lb"
  }'
```

### 4. Парсинг файла
```bash
curl -X POST "http://localhost:8000/api/bc-parser/parse-file" \
  -F "file=@/path/to/your/bc_document.txt"
```

## 🏢 Deal Management API

### 1. Получение списка сделок
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/deals?limit=10&offset=0"
```

### 2. Создание новой сделки
```bash
curl -X POST "http://localhost:8000/api/deals" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "seller": "OpenMineral Trading",
    "buyer": "Global Metals Corp",
    "material": "Copper Concentrate",
    "quantity": 5000,
    "unit": "dmt",
    "price": 85.50,
    "currency": "USD",
    "delivery_terms": "CIF Shanghai",
    "shipment_period": "Q1 2024"
  }'
```

### 3. Получение деталей сделки
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/deals/12345"
```

### 4. Обновление сделки
```bash
curl -X PUT "http://localhost:8000/api/deals/12345" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "confirmed",
    "notes": "Final terms agreed"
  }'
```

## 📊 Market Analysis API

### 1. Получение рыночных данных
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/market/prices?commodity=copper&period=30d"
```

**Ответ:**
```json
{
  "commodity": "copper",
  "period": "30d",
  "data": [
    {
      "date": "2024-01-15",
      "price": 8450.50,
      "currency": "USD",
      "unit": "tonne",
      "exchange": "LME"
    }
  ],
  "statistics": {
    "avg_price": 8425.75,
    "min_price": 8200.00,
    "max_price": 8650.00,
    "volatility": 2.3
  }
}
```

### 2. AI-анализ рынка
```bash
curl -X POST "http://localhost:8000/api/market/ai-analysis" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "commodity": "copper",
    "analysis_type": "price_forecast",
    "timeframe": "30d"
  }'
```

## ⚠️ Risk Management API

### 1. Расчет VaR (Value at Risk)
```bash
curl -X POST "http://localhost:8000/api/risk/var" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio_id": "PORT_001",
    "confidence_level": 0.95,
    "time_horizon": 1
  }'
```

**Ответ:**
```json
{
  "portfolio_id": "PORT_001",
  "var_95": 125000.50,
  "currency": "USD",
  "confidence_level": 0.95,
  "time_horizon_days": 1,
  "calculation_method": "historical_simulation",
  "calculated_at": "2024-01-15T10:30:00Z"
}
```

### 2. Анализ рисков сделки
```bash
curl -X POST "http://localhost:8000/api/risk/deal-analysis" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "deal_id": "DEAL_12345",
    "risk_factors": ["price", "credit", "operational"]
  }'
```

## 🔍 KYC & Compliance API

### 1. Проверка контрагента
```bash
curl -X POST "http://localhost:8000/api/kyc/check-counterparty" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Global Metals Corp",
    "country": "Singapore",
    "registration_number": "SG123456789"
  }'
```

**Ответ:**
```json
{
  "company_name": "Global Metals Corp",
  "kyc_status": "approved",
  "risk_rating": "low",
  "sanctions_check": "clear",
  "last_updated": "2024-01-10T15:20:00Z",
  "compliance_notes": "All documentation verified",
  "next_review_date": "2024-07-10"
}
```

### 2. Проверка санкций
```bash
curl -X POST "http://localhost:8000/api/kyc/sanctions-screening" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_name": "Test Company Ltd",
    "entity_type": "company",
    "country": "UK"
  }'
```

## 🤖 AI Workflow API

### 1. Запуск AI workflow
```bash
curl -X POST "http://localhost:8000/api/workflow/start" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_type": "deal_analysis",
    "input_data": {
      "deal_id": "DEAL_12345",
      "analysis_depth": "comprehensive"
    }
  }'
```

**Ответ:**
```json
{
  "workflow_id": "WF_789012",
  "status": "running",
  "estimated_completion": "2024-01-15T10:35:00Z",
  "progress": 0,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 2. Проверка статуса workflow
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/workflow/WF_789012/status"
```

### 3. Получение результатов workflow
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/workflow/WF_789012/results"
```

## 📈 Analytics API

### 1. Получение аналитики портфеля
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/analytics/portfolio?period=ytd"
```

### 2. Отчет по производительности
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/analytics/performance?start_date=2024-01-01&end_date=2024-01-31"
```

## 🔧 System API

### 1. Проверка здоровья системы
```bash
curl "http://localhost:8000/api/health"
```

**Ответ:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production",
  "chroma_status": "healthy",
  "chroma_vectors": 15420,
  "uptime_seconds": 86400,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 2. Тест ChromaDB подключения
```bash
curl "http://localhost:8000/api/chroma/test"
```

## 📝 WebSocket API

### Real-time обновления
```javascript
// JavaScript пример подключения к WebSocket
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = function(event) {
    console.log('Connected to WebSocket');
    
    // Подписка на обновления сделок
    ws.send(JSON.stringify({
        type: 'subscribe',
        channel: 'deals',
        filters: {
            status: 'active'
        }
    }));
};

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received update:', data);
};
```

## 🚨 Обработка ошибок

### Стандартные коды ошибок
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "quantity",
      "issue": "must be greater than 0"
    },
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req_123456789"
  }
}
```

### Коды состояния HTTP
- `200` - Успешный запрос
- `201` - Ресурс создан
- `400` - Неверный запрос
- `401` - Не авторизован
- `403` - Доступ запрещен
- `404` - Ресурс не найден
- `422` - Ошибка валидации
- `429` - Превышен лимит запросов
- `500` - Внутренняя ошибка сервера

## 📊 Rate Limiting

```bash
# Заголовки ответа с информацией о лимитах
HTTP/1.1 200 OK
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642248600
```

## 🔄 Pagination

```bash
# Пример запроса с пагинацией
curl "http://localhost:8000/api/deals?page=2&per_page=50"
```

**Ответ:**
```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "per_page": 50,
    "total": 1250,
    "pages": 25,
    "has_next": true,
    "has_prev": true
  }
}
```

## 📚 SDK и библиотеки

### Python SDK
```python
from openmineral_sdk import OpenMineralClient

client = OpenMineralClient(
    base_url="http://localhost:8000",
    api_key="your_api_key"
)

# Парсинг BC документа
result = client.bc_parser.parse_file("path/to/document.txt")
print(result.data)

# Создание сделки
deal = client.deals.create({
    "seller": "OpenMineral",
    "buyer": "Global Metals",
    "material": "Copper Concentrate",
    "quantity": 5000
})
```

### JavaScript SDK
```javascript
import { OpenMineralClient } from '@openmineral/sdk';

const client = new OpenMineralClient({
    baseUrl: 'http://localhost:8000',
    apiKey: 'your_api_key'
});

// Получение рыночных данных
const marketData = await client.market.getPrices({
    commodity: 'copper',
    period: '30d'
});
```

---

**Версия API**: v1.0.0 | **Последнее обновление**: 2025-09-18

Для получения актуальной документации API посетите: `http://localhost:8000/docs`
