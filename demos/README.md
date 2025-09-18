# 🎯 OpenMineral Demo Versions

Данная папка содержит 4 различных демо версии OpenMineral платформы, каждая с разным уровнем функциональности и интеграции.

## 📁 Структура демо версий

### Version 1: Full AI Demo 🤖
**Путь**: `demos/v1-full-ai/`
**Время разработки**: 8-10 часов
**Онлайн URL**: `https://openmineral-ai.vercel.app`

**Функции**:
- ✅ Реальная интеграция с OpenAI GPT-4 Turbo
- ✅ Claude 3.5 Sonnet для market analysis
- ✅ LangChain workflows для deal analysis
- ✅ PostgreSQL база данных
- ✅ Real-time WebSocket connections
- ✅ AI-powered price prediction
- ✅ Intelligent risk assessment
- ✅ Automated compliance checking

### Version 2: Enhanced Mock Demo 🎭
**Путь**: `demos/v2-enhanced-mock/`
**Время разработки**: 4-5 часов
**Онлайн URL**: `https://openmineral-mock.vercel.app`

**Функции**:
- ✅ Реальная frontend-backend интеграция
- ✅ JWT Authentication + защищенные routes
- ✅ SQLite база данных для персистентности
- ✅ Улучшенные mock AI responses (реалистичные задержки)
- ✅ CRUD операции с deals
- ✅ Real-time price updates (mock)
- ✅ Professional UI/UX

### Version 3: Hybrid Demo 🔄
**Путь**: `demos/v3-hybrid/`
**Время разработки**: 6-7 часов
**Онлайн URL**: `https://openmineral-hybrid.vercel.app`

**Функции**:
- ✅ PostgreSQL для реальной персистентности
- ✅ Переключаемый AI режим (Mock ↔ Real AI)
- ✅ Environment-based конфигурация
- ✅ Fallback mechanisms для AI сервисов
- ✅ Advanced caching с Redis
- ✅ Configuration dashboard для AI settings

### Version 4: Minimal Working Demo ⚡
**Путь**: `demos/v4-minimal/`
**Время разработки**: 2-3 часа
**Онлайн URL**: `https://openmineral-minimal.vercel.app`

**Функции**:
- ✅ Основная frontend-backend связь
- ✅ Простая авторизация
- ✅ In-memory данные (без БД)
- ✅ Базовые CRUD операции
- ✅ Статичные mock данные
- ✅ Минимальный UI для демонстрации концепции

## 🚀 Deployment Strategy

Каждая версия имеет свою независимую конфигурацию развертывания:

### Автоматическое развертывание:
```bash
# Развернуть все версии одновременно
./deploy-all-demos.sh

# Развернуть конкретную версию
cd demos/v1-full-ai && ./deploy.sh
cd demos/v2-enhanced-mock && ./deploy.sh
cd demos/v3-hybrid && ./deploy.sh
cd demos/v4-minimal && ./deploy.sh
```

### Мониторинг:
- Status dashboard: `https://status.openmineral.demo/`
- All demos health check: `https://health.openmineral.demo/`

## 🎯 Recommended Demo Flow for Clients

1. **Начать с Version 4 (Minimal)** - показать базовую концепцию
2. **Перейти к Version 2 (Enhanced Mock)** - продемонстрировать UI/UX
3. **Показать Version 3 (Hybrid)** - объяснить гибкость архитектуры
4. **Завершить Version 1 (Full AI)** - впечатлить реальным AI функционалом

## 📊 Features Comparison Matrix

| Feature | V4 Minimal | V2 Enhanced | V3 Hybrid | V1 Full AI |
|---------|------------|-------------|-----------|------------|
| Frontend-Backend API | ✅ | ✅ | ✅ | ✅ |
| Authentication | Basic | JWT | JWT | JWT + OAuth |
| Database | Memory | SQLite | PostgreSQL | PostgreSQL |
| AI Integration | ❌ | Mock | Switchable | Real LLM |
| Real-time Updates | ❌ | Polling | WebSocket | WebSocket |
| Deal Management | Basic | Advanced | Advanced | AI-Enhanced |
| Risk Assessment | Static | Calculator | Hybrid | AI-Powered |
| Market Analysis | Static | Mock | Enhanced | AI-Driven |
| Deployment Time | 15 min | 30 min | 45 min | 60 min |
| Development Time | 2-3h | 4-5h | 6-7h | 8-10h |

## 🔧 Development Setup

### Prerequisites:
```bash
# Required tools
node >= 18.0.0
python >= 3.11
docker >= 24.0.0
git >= 2.40.0
```

### Environment Variables:
```bash
# For Full AI Demo (v1)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
PINECONE_API_KEY=...

# For all versions
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
JWT_SECRET_KEY=...
```

## 📞 Support & Maintenance

- **Production Issues**: Create issue in main repo
- **Demo Updates**: Auto-deployed from main branch
- **Client Feedback**: Collected via embedded analytics

---

**Last Updated**: 2025-09-16  
**Next Review**: 2025-10-16  
**Maintainer**: OpenMineral Development Team