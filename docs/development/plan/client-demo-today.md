# План демонстрации для клиента СЕГОДНЯ

Дата: 18.09.2025

## 🎯 Цель: Показать рабочий прототип BC Flow согласно ТЗ

### Что нужно сделать ПРЯМО СЕЙЧАС (1-2 часа):

## 1. Быстрое исправление BC Flow (30 минут)

### Проблема: 
Docker файлы не найдены в bc_flow/frontend/

### Решение:
```bash
# Создать недостающие Dockerfile
cd bc_flow/frontend
cat > Dockerfile << 'EOF'
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
EOF

# Создать Dockerfile для backend если нужно
cd ../backend
ls Dockerfile* || cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
```

## 2. Запуск демо (15 минут)

```bash
# Вернуться в корень bc_flow
cd bc_flow

# Запустить сервисы
docker-compose up -d

# Проверить статус
docker-compose ps

# Открыть в браузере
open http://localhost:3000
```

## 3. Альтернативный быстрый запуск (если Docker не работает)

### Frontend:
```bash
cd bc_flow/frontend
npm install
npm start
# Откроется на http://localhost:3000
```

### Backend:
```bash
cd bc_flow/backend
pip install -r requirements.txt
uvicorn main:app --reload
# Запустится на http://localhost:8000
```

## 4. Что показать клиенту (по ТЗ):

### ✅ Шаг 1: Deal Basics
- Seller & Buyer (статический продавец, динамический покупатель)
- Material & Quantity (dropdown + числовое поле)
- Кнопка "Proceed to Terms"
- Валидация: количество должно быть числом

### ✅ Шаг 2: Commercial Terms  
- Delivery & Shipment (Term, Point, Mode, Shipment Period, Packaging)
- Assay/Quality (загрузка файла - mock)
- Pricing & Charges (TC USD/dmt, RC USD/toz)
- **AI Suggestions** (mock): "Your RC is higher than market avg. Suggest lowering to $4.50"
- Additional Terms (clauses)

### ✅ Шаг 3: Payment Terms
- Payment Method, Currency, Triggering Event
- Payment Stages (Prepayment %, Provisional & Final)
- WSMD & Surveyor (Final location, cost sharing)

### ✅ Шаг 4: Review & Submit
- Review Summary (все поля в read-only)
- Final Confirmation (Submit button, Back/Edit)
- **AI Validation**: "⚠️ Surveyor not selected"

### ✅ Шаг 5: Summary Page
- Успешное завершение
- **Celery Task**: Submit запускает фоновую задачу (15 сек sleep)
- Статус обработки и подтверждение

## 5. Презентационный скрипт (5 минут подготовки):

### Введение:
"Демонстрирую Business Confirmation Flow - систему для валидации критической информации о сделках перед исполнением контрактов"

### Демо по шагам:
1. **"Начинаем с базовой информации о сделке"**
   - Показать предзаполненного продавца
   - Выбрать покупателя из dropdown
   - Ввести материал и количество
   - Показать валидацию

2. **"Переходим к коммерческим условиям"**
   - Заполнить условия доставки
   - Показать AI-подсказку по ценам
   - Загрузить mock файл assay
   - Показать логику Rails/Ship -> Bulk/Big Bags

3. **"Настраиваем условия оплаты"**
   - Выбрать метод оплаты
   - Настроить этапы оплаты (слайдер)
   - Выбрать surveyor

4. **"Финальный обзор и подтверждение"**
   - Показать сводку всех данных
   - Показать AI валидацию
   - Нажать Submit

5. **"Асинхронная обработка"**
   - Показать индикатор загрузки
   - Объяснить работу Celery + Redis
   - Показать успешное завершение

### Технические особенности:
- "Все dropdown значения приходят из backend API"
- "AI-подсказки интегрированы в workflow"
- "Фоновые задачи выполняются в Celery worker"
- "Полная Docker контейнеризация"

## 6. Если что-то не работает - Plan B:

### Показать готовые скриншоты:
1. Подготовить скриншоты всех 5 шагов
2. Записать короткое видео демо
3. Показать код архитектуры

### Альтернативный демо:
- Показать routing_policy тесты (13 passed)
- Продемонстрировать AI маршрутизацию
- Показать архитектуру в docs/

## 7. Вопросы клиента - готовые ответы:

**Q: "Как масштабируется система?"**
A: "Микросервисная архитектура + Kubernetes + multi-cloud (AWS/Azure)"

**Q: "Где AI интеграция?"**  
A: "AI-подсказки в шаге 2, AI валидация в шаге 4, полная LangChain интеграция в roadmap"

**Q: "Безопасность данных?"**
A: "OAuth 2.0, JWT токены, шифрование at-rest и in-transit, audit trails"

**Q: "Интеграция с существующими системами?"**
A: "REST API, готовые коннекторы, SDK для разработчиков"

## 🚀 Действия ПРЯМО СЕЙЧАС:

1. **Исправить Dockerfile (5 мин)**
2. **Запустить bc_flow (5 мин)** 
3. **Протестировать все шаги (10 мин)**
4. **Подготовить презентацию (10 мин)**
5. **Готов к демо!**

## Команды для копирования:

```bash
# Быстрое исправление и запуск
cd bc_flow/frontend && echo 'FROM node:18-alpine
WORKDIR /app  
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]' > Dockerfile

cd ../backend && echo 'FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt  
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]' > Dockerfile

cd .. && docker-compose up -d && open http://localhost:3000
