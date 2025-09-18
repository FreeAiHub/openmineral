# 🚀 OpenMineral Demo Deployment Guide

Complete deployment guide for all 4 demo versions with online access capabilities.

## 📋 Prerequisites

### Required Tools:
```bash
# Core tools
node >= 18.0.0
python >= 3.11
git >= 2.40.0

# Deployment tools
npm install -g vercel      # Frontend deployment
npm install -g @railway/cli # Backend deployment
docker >= 24.0.0          # For local development
```

### Required Accounts:
- **Vercel Account** (free tier) - для frontend hosting
- **Railway Account** (free tier) - для backend hosting  
- **Upstash Account** (free tier) - для Redis caching
- **PlanetScale/Supabase** (free tier) - для production databases

## 🎯 Deployment Strategy Overview

| Demo Version | Frontend | Backend | Database | AI Services | Deployment Time |
|--------------|----------|---------|----------|-------------|----------------|
| **v4-minimal** | Vercel | Railway | None (memory) | Mock only | 15 minutes |
| **v2-enhanced-mock** | Vercel | Railway | SQLite | Enhanced Mock | 30 minutes |
| **v3-hybrid** | Vercel | Railway | PostgreSQL | Switchable | 45 minutes |
| **v1-full-ai** | Vercel | Railway | PostgreSQL + Redis | Real AI | 60 minutes |

## 🚀 Quick Deploy All Versions

### One-Command Deployment Script:
```bash
# Create deployment script
cat > deploy-all-demos.sh << 'EOF'
#!/bin/bash
set -e

echo "🚀 OpenMineral - Deploying All Demo Versions"
echo "============================================"

# Set common environment variables
export OPENMINERAL_PROJECT="openmineral-demos"
export TIMESTAMP=$(date +%Y%m%d-%H%M%S)

# Deploy v4-minimal (fastest)
echo "📦 Deploying v4-minimal..."
cd demos/v4-minimal
./deploy.sh
echo "✅ v4-minimal deployed: https://openmineral-minimal.vercel.app"

# Deploy v2-enhanced-mock
echo "📦 Deploying v2-enhanced-mock..."
cd ../v2-enhanced-mock  
./deploy.sh
echo "✅ v2-enhanced-mock deployed: https://openmineral-mock.vercel.app"

# Deploy v3-hybrid
echo "📦 Deploying v3-hybrid..."
cd ../v3-hybrid
./deploy.sh  
echo "✅ v3-hybrid deployed: https://openmineral-hybrid.vercel.app"

# Deploy v1-full-ai (requires API keys)
if [[ -n "$OPENAI_API_KEY" ]]; then
    echo "📦 Deploying v1-full-ai..."
    cd ../v1-full-ai
    ./deploy.sh
    echo "✅ v1-full-ai deployed: https://openmineral-ai.vercel.app"
else
    echo "⚠️  Skipping v1-full-ai (OPENAI_API_KEY not provided)"
fi

echo ""
echo "🎉 All deployments completed!"
echo "📋 Demo URLs:"
echo "   • v4-minimal:      https://openmineral-minimal.vercel.app"
echo "   • v2-enhanced:     https://openmineral-mock.vercel.app" 
echo "   • v3-hybrid:       https://openmineral-hybrid.vercel.app"
echo "   • v1-full-ai:      https://openmineral-ai.vercel.app"
echo ""
echo "📊 Status dashboard: https://status.openmineral.demo"
EOF

chmod +x deploy-all-demos.sh
```

## 📱 Individual Demo Deployment

### Version 4: Minimal Working Demo

**Time**: 15 minutes  
**Complexity**: Beginner  

```bash
# 1. Setup
cd demos/v4-minimal
cp .env.example .env

# 2. Frontend deployment
cd frontend
vercel --prod
# URL: https://openmineral-minimal.vercel.app

# 3. Backend deployment  
cd ../backend
railway login
railway init
railway add --database postgresql
railway deploy
# URL: https://openmineral-minimal-api.railway.app

# 4. Connect frontend to backend
vercel env add NEXT_PUBLIC_API_URL https://openmineral-minimal-api.railway.app
vercel --prod
```

### Version 2: Enhanced Mock Demo

**Time**: 30 minutes  
**Complexity**: Intermediate  

```bash
# 1. Setup
cd demos/v2-enhanced-mock
cp .env.example .env

# 2. Database setup (SQLite → PostgreSQL for production)
railway login
railway init
railway add --database postgresql

# 3. Backend deployment
cd backend
# Update DATABASE_URL from Railway
railway deploy

# 4. Database migration
railway run alembic upgrade head

# 5. Frontend deployment
cd ../frontend
vercel --prod
vercel env add NEXT_PUBLIC_API_URL https://openmineral-mock-api.railway.app
vercel --prod

# Demo URL: https://openmineral-mock.vercel.app
```

### Version 3: Hybrid Demo  

**Time**: 45 minutes  
**Complexity**: Advanced  

```bash
# 1. Infrastructure setup
cd demos/v3-hybrid

# 2. Database setup (PostgreSQL)
railway login
railway init  
railway add --database postgresql

# 3. Redis setup (Upstash)
# Visit https://console.upstash.com
# Create Redis database
# Get REDIS_URL

# 4. Environment configuration
cat > .env << EOF
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=rediss://default:pass@host:port
AI_MODE=hybrid
OPENAI_API_KEY=sk-optional-...
ANTHROPIC_API_KEY=sk-ant-optional-...
EOF

# 5. Backend deployment
cd backend
railway deploy

# 6. Database migration
railway run alembic upgrade head

# 7. Frontend deployment
cd ../frontend
vercel --prod
vercel env add NEXT_PUBLIC_API_URL https://openmineral-hybrid-api.railway.app
vercel env add NEXT_PUBLIC_AI_MODE hybrid
vercel --prod

# Demo URL: https://openmineral-hybrid.vercel.app
```

### Version 1: Full AI Demo

**Time**: 60 minutes  
**Complexity**: Expert  

```bash
# 1. AI Services setup
cd demos/v1-full-ai

# 2. Required API Keys
echo "Required API keys for full AI demo:"
echo "- OPENAI_API_KEY (required)"
echo "- ANTHROPIC_API_KEY (required)"  
echo "- PINECONE_API_KEY (recommended)"

# 3. Infrastructure setup
railway login
railway init
railway add --database postgresql
# Setup Upstash Redis
# Setup Pinecone vector database

# 4. Environment configuration  
cat > .env << EOF
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=rediss://default:pass@host:port
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=...
AI_MODE=real
EOF

# 5. Vector database setup
railway run python scripts/setup_vector_db.py

# 6. Backend deployment with AI services
cd backend  
railway deploy

# 7. Database and vector DB migration
railway run alembic upgrade head
railway run python scripts/populate_ai_data.py

# 8. Frontend deployment with AI features
cd ../frontend
vercel --prod
vercel env add NEXT_PUBLIC_API_URL https://openmineral-ai-api.railway.app
vercel env add NEXT_PUBLIC_AI_ENABLED true
vercel env add NEXT_PUBLIC_WEBSOCKET_URL wss://openmineral-ai-api.railway.app/ws
vercel --prod

# Demo URL: https://openmineral-ai.vercel.app
```

## 🔧 Environment Variables Reference

### Common Variables (All Versions):
```env
# Application
NODE_ENV=production
PYTHON_ENV=production
DEBUG=false

# JWT Authentication
JWT_SECRET_KEY=your-super-secure-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration  
ALLOWED_ORIGINS=["https://your-frontend-domain.vercel.app"]
```

### Version-Specific Variables:

#### v4-minimal:
```env
# Minimal config
DEMO_MODE=true
STORAGE_TYPE=memory
```

#### v2-enhanced-mock:
```env
# Enhanced mock
DATABASE_URL=postgresql://user:pass@host:port/db
AI_MODE=mock
ENABLE_ANALYTICS=true
```

#### v3-hybrid:
```env
# Hybrid configuration
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=rediss://default:pass@host:port
AI_MODE=hybrid
OPENAI_API_KEY=sk-optional-...
ANTHROPIC_API_KEY=sk-ant-optional-...
FALLBACK_TO_MOCK=true
MAX_FALLBACK_ATTEMPTS=3
```

#### v1-full-ai:
```env
# Full AI configuration
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=rediss://default:pass@host:port
AI_MODE=real
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=...
ENABLE_WEBSOCKETS=true
ENABLE_AI_STREAMING=true
```

## 🌐 Custom Domain Setup

### Frontend Domains (Vercel):
```bash
# Add custom domains
vercel domains add openmineral-minimal.your-domain.com
vercel domains add openmineral-mock.your-domain.com  
vercel domains add openmineral-hybrid.your-domain.com
vercel domains add openmineral-ai.your-domain.com

# Configure SSL (automatic with Vercel)
vercel certs ls
```

### Backend Domains (Railway):
```bash
# Custom domains for APIs
railway domain
# Follow Railway docs for custom domain setup
```

## 📊 Monitoring & Analytics Setup

### Health Check Endpoints:
```bash
# Add to each backend
GET /health              # Basic health check
GET /health/detailed     # Detailed system status
GET /metrics            # Prometheus metrics
GET /admin/status       # Admin dashboard
```

### Status Dashboard Creation:
```bash
# Create status dashboard
mkdir status-dashboard
cd status-dashboard

# Simple status page
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>OpenMineral Demo Status</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .online { background: #d4edda; border: 1px solid #c3e6cb; }
        .offline { background: #f8d7da; border: 1px solid #f5c6cb; }
        .demo-link { text-decoration: none; color: #007bff; }
        .demo-link:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>🚀 OpenMineral Demo Status</h1>
    <div id="demo-status">
        <!-- Status будет загружен через JavaScript -->
    </div>
    
    <script>
        async function checkStatus() {
            const demos = [
                {name: 'v4-minimal', url: 'https://openmineral-minimal.vercel.app'},
                {name: 'v2-enhanced-mock', url: 'https://openmineral-mock.vercel.app'},
                {name: 'v3-hybrid', url: 'https://openmineral-hybrid.vercel.app'},
                {name: 'v1-full-ai', url: 'https://openmineral-ai.vercel.app'}
            ];
            
            const container = document.getElementById('demo-status');
            container.innerHTML = '';
            
            for (const demo of demos) {
                const statusDiv = document.createElement('div');
                statusDiv.className = 'status';
                
                try {
                    const response = await fetch(`${demo.url}/api/health`);
                    const isOnline = response.ok;
                    
                    statusDiv.className += isOnline ? ' online' : ' offline';
                    statusDiv.innerHTML = `
                        <strong>${demo.name}</strong> - 
                        <span style="color: ${isOnline ? 'green' : 'red'}">
                            ${isOnline ? '🟢 Online' : '🔴 Offline'}
                        </span>
                        <a href="${demo.url}" class="demo-link" target="_blank">→ Open Demo</a>
                    `;
                } catch (error) {
                    statusDiv.className += ' offline';
                    statusDiv.innerHTML = `
                        <strong>${demo.name}</strong> - 
                        <span style="color: red">🔴 Offline</span>
                        <a href="${demo.url}" class="demo-link" target="_blank">→ Try Anyway</a>
                    `;
                }
                
                container.appendChild(statusDiv);
            }
        }
        
        // Check status on load and every 30 seconds
        checkStatus();
        setInterval(checkStatus, 30000);
    </script>
</body>
</html>
EOF

# Deploy status page
vercel --prod
# Status URL: https://openmineral-status.vercel.app
```

## 🚨 Troubleshooting Guide

### Common Issues:

#### 1. Frontend не подключается к Backend
```bash
# Check CORS configuration
curl -H "Origin: https://your-frontend.vercel.app" \
     -H "Access-Control-Request-Method: GET" \
     https://your-backend.railway.app/api/health

# Fix: Update ALLOWED_ORIGINS in backend settings
```

#### 2. Database Connection Failed
```bash
# Test database connection
railway run python -c "
import psycopg2
import os
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
print('Database connection successful!')
"
```

#### 3. AI API Limits Exceeded
```bash
# Monitor API usage
curl https://your-backend.railway.app/admin/api-usage

# Switch to hybrid/mock mode temporarily
railway env set AI_MODE=mock
railway deploy
```

#### 4. Redis Connection Issues
```bash
# Test Redis connection
railway run python -c "
import redis
import os
r = redis.from_url(os.getenv('REDIS_URL'))
r.ping()
print('Redis connection successful!')
"
```

## 📈 Performance Optimization

### Frontend Optimization:
```bash
# Enable Vercel analytics
vercel analytics enable

# Optimize build
npm run build -- --analyze
```

### Backend Optimization:
```bash
# Database connection pooling
railway env set DATABASE_POOL_SIZE=10
railway env set DATABASE_POOL_OVERFLOW=20

# Redis configuration
railway env set REDIS_MAX_CONNECTIONS=50
```

## 🎯 Client Presentation Setup

### Pre-Demo Checklist:
```markdown
- [ ] All 4 demos deployed and accessible
- [ ] Status dashboard showing all green
- [ ] Demo credentials documented
- [ ] Presentation slides updated with live URLs
- [ ] Backup plans готовы (local versions)
- [ ] Performance metrics собраны
```

### Demo URLs для Client Presentation:
```
🎯 Client Demo Links:
├── 📱 Status Dashboard: https://status.openmineral.demo
├── ⚡ v4-minimal: https://openmineral-minimal.vercel.app
├── 🎭 v2-enhanced: https://openmineral-mock.vercel.app
├── 🔄 v3-hybrid: https://openmineral-hybrid.vercel.app
└── 🤖 v1-full-ai: https://openmineral-ai.vercel.app
```

---

**🚀 Ready to impress clients with professional online demos!**