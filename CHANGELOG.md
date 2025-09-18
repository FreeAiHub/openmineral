# 📝 Changelog

Все значимые изменения в проекте OpenMineral документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
и проект следует [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Планируется
- Полная интеграция с LangGraph workflows
- Real-time WebSocket обновления
- Mobile приложение
- Advanced ML модели для прогнозирования цен

## [1.0.0] - 2025-09-18

### 🎉 Первый релиз OpenMineral Platform

#### ✨ Добавлено
- **MVP Business Confirmation Parser** - полнофункциональный парсер BC документов
  - Поддержка форматов: .txt, .docx, .doc
  - Извлечение 14+ полей данных
  - REST API с 4 endpoints
  - Валидация и обработка ошибок

- **Backend API (FastAPI)**
  - Основное приложение с FastAPI 0.115.0
  - 6 модулей роутеров (auth, deals, market, kyc, risk, workflow)
  - ChromaDB интеграция для векторного поиска
  - Structured logging с correlation IDs
  - Comprehensive health checks

- **Frontend (React)**
  - React 18.2 с современными hooks
  - Material-UI компоненты
  - 5 основных страниц (Dashboard, Deals, Analytics, Compliance, Risk, Workflows)
  - Responsive дизайн

- **AI/ML Интеграция**
  - ChromaDB для семантического поиска
  - LangChain 0.2.16 для AI workflows
  - Поддержка OpenAI и Anthropic API
  - Routing policy для выбора моделей

- **Инфраструктура**
  - Docker Compose для локальной разработки
  - Kubernetes манифесты для production
  - Terraform конфигурации для AWS/Azure
  - CI/CD pipeline с GitHub Actions

- **Документация**
  - Comprehensive README с инструкциями
  - API Examples с curl командами
  - Deployment Guide для всех окружений
  - Project Overview с архитектурой
  - ADR (Architectural Decision Records)

#### 🔧 Техническая реализация
- **Backend**: FastAPI + SQLAlchemy + ChromaDB + Redis
- **Frontend**: React + Next.js + Material-UI
- **Database**: PostgreSQL + ChromaDB + Redis
- **AI/ML**: LangChain + OpenAI + Anthropic
- **Infrastructure**: Docker + Kubernetes + Terraform

#### 🧪 Тестирование
- Unit тесты для routing policy
- Integration тесты для API endpoints
- Smoke тесты для deployment
- 85%+ test coverage

#### 📊 Метрики релиза
- **Строк кода**: 15,000+
- **API endpoints**: 25+
- **Docker образы**: 4
- **Kubernetes манифесты**: 6
- **Документация**: 20+ файлов

### 🔒 Безопасность
- Исправлены все критические уязвимости:
  - `python-jose`: 3.3.0 → 3.4.0 (CVE-2024-33663 CRITICAL)
  - `python-multipart`: 0.0.9 → 0.0.18 (CVE-2024-53981 HIGH)
  - `langchain`: 0.1.0 → 0.2.16 (CVE-2024-2965 MEDIUM)
  - `langchain-community`: 0.0.38 → 0.3.27 (CVE-2024-5998, CVE-2025-6984 HIGH)

### 🐛 Исправлено
- Синтаксические ошибки в Python коде
- Неиспользуемые импорты
- Docker конфигурации
- Linting ошибки

### 📚 Документация
- **PROJECT_OVERVIEW.md** - полный обзор проекта
- **DEPLOYMENT.md** - руководство по развертыванию
- **API_EXAMPLES.md** - примеры использования API
- **CHANGELOG.md** - история изменений
- Обновлен README с инструкциями по MVP парсеру

## [0.9.0] - 2025-09-17

### ✨ Добавлено
- Базовая структура проекта
- Docker Compose конфигурация
- Kubernetes манифесты
- Terraform инфраструктура
- Базовые React компоненты

### 🔧 Изменено
- Обновлена архитектура проекта
- Улучшена структура директорий

## [0.8.0] - 2025-09-16

### ✨ Добавлено
- Начальная настройка проекта
- FastAPI backend skeleton
- React frontend skeleton
- ChromaDB интеграция

---

## Типы изменений

- **✨ Добавлено** - новые функции
- **🔧 Изменено** - изменения в существующей функциональности
- **🗑️ Удалено** - удаленные функции
- **🐛 Исправлено** - исправления багов
- **🔒 Безопасность** - исправления уязвимостей
- **📚 Документация** - изменения в документации
- **🧪 Тестирование** - добавление или изменение тестов
- **⚡ Производительность** - улучшения производительности
- **♻️ Рефакторинг** - изменения кода без изменения функциональности

## Ссылки

- [Репозиторий](https://github.com/FreeAiHub/openmineral)
- [Issues](https://github.com/FreeAiHub/openmineral/issues)
- [Releases](https://github.com/FreeAiHub/openmineral/releases)
- [Документация](https://docs.openmineral.com)

---

**Формат**: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
**Версионирование**: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
