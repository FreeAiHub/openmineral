# Version 4: Minimal Working Demo ⚡

**Цель**: Самая быстрая демонстрация работающей связи frontend-backend  
**Время разработки**: 2-3 часа  
**Online URL**: https://openmineral-minimal.vercel.app  

## 🎯 Scope

**Минимальный функционал для proof-of-concept:**
- ✅ React frontend подключен к FastAPI backend
- ✅ Базовая авторизация (простая проверка)  
- ✅ CRUD операции с deals (в памяти)
- ✅ Статичные mock данные для market prices
- ✅ Простой UI без лишних наворотов

## 🚀 Quick Start

```bash
# 1. Backend setup
cd backend
pip install fastapi uvicorn python-jose passlib
uvicorn main:app --reload --port 8000

# 2. Frontend setup  
cd ../frontend
npm install --legacy-peer-deps
npm start

# 3. Access demo
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
```

## 🛠 Tech Stack

**Backend**: FastAPI + In-Memory Storage  
**Frontend**: React + Axios + Ant Design  
**Auth**: Simple JWT tokens  
**Database**: None (все в памяти)  
**Deployment**: Vercel (frontend) + Railway (backend)

## 📋 Demo Flow

1. **Login page** → Enter credentials (demo/demo123)
2. **Dashboard** → View static stats and charts  
3. **Deals page** → Create/Edit/Delete deals (in memory)
4. **Market page** → View mock price data
5. **Settings** → Basic user profile

**Demo credentials**:
- Username: `demo`  
- Password: `demo123`

## 🔄 API Endpoints

```python
# Minimal API structure
GET /api/health          # Health check
POST /api/auth/login     # Simple login
GET /api/deals          # List deals (in memory)
POST /api/deals         # Create deal
GET /api/market/prices  # Mock market data
```

## 📦 Dependencies

**Backend** (`requirements-minimal.txt`):
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-jose==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
```

**Frontend** (`package.json` - minimal):
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "antd": "^5.12.8", 
    "axios": "^1.6.2",
    "react-router-dom": "^6.20.1"
  }
}
```

## 🎨 Features

- 📱 **Responsive design**: Works on mobile/desktop
- 🔐 **Simple auth**: Login/logout functionality  
- 📊 **Basic charts**: Simple data visualization
- 💾 **In-memory storage**: No database setup needed
- ⚡ **Fast load**: Minimal dependencies

## ⚠ Limitations

- ❌ Data не сохраняется после перезапуска
- ❌ Нет реального AI функционала
- ❌ Упрощенная авторизация
- ❌ Ограниченная валидация данных

## 🚢 Deployment

**Auto-deploy**:
```bash
./deploy.sh
```

**Manual deploy**:
```bash
# Frontend to Vercel
vercel --prod

# Backend to Railway
railway login && railway deploy
```

**Environment variables**:
```env
# Minimal config
JWT_SECRET_KEY=minimal-demo-secret
ENVIRONMENT=demo
```

## 🎯 Client Presentation Points

1. **"Это базовая архитектура платформы"**
2. **"Frontend полностью подключен к API"** 
3. **"Можем масштабировать функционал"**
4. **"Готово к интеграции с real data sources"**

**Next step**: "Теперь покажем версию с базой данных и улучшенным AI..." → v2-enhanced-mock