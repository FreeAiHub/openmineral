# Version 3: Hybrid Demo 🔄

**Цель**: Гибкая архитектура с переключаемым AI режимом и production-ready базой данных  
**Время разработки**: 6-7 часов  
**Online URL**: https://openmineral-hybrid.vercel.app  

## 🎯 Hybrid Features

**Best of Both Worlds:**
- 🔄 **Switchable AI Mode** - Mock ↔ Real AI через environment variables
- 🐘 **PostgreSQL Database** - Production-ready persistence
- ⚡ **Redis Caching** - High-performance data caching
- 📊 **Advanced Analytics** - Enhanced reporting capabilities
- 🛠️ **Configuration Dashboard** - Admin panel для AI settings
- 🔧 **Fallback Mechanisms** - Graceful degradation если AI недоступен

## 🚀 Quick Start

```bash
# 1. Infrastructure setup
docker-compose up -d postgres redis

# 2. Environment configuration
cp .env.hybrid.example .env
# Configure AI mode:
# AI_MODE=mock          # For demo without API keys
# AI_MODE=real          # For full AI functionality
# AI_MODE=hybrid        # Automatic fallback

# 3. Database migration
cd backend
pip install -r requirements-hybrid.txt
alembic upgrade head

# 4. Backend with hybrid capabilities
uvicorn main:app --reload --port 8000

# 5. Frontend with mode switching
cd ../frontend
npm install
npm run dev

# 6. Access hybrid demo
# Frontend: http://localhost:3000
# Admin Panel: http://localhost:3000/admin
# API Docs: http://localhost:8000/docs
```

## 🛠 Hybrid Architecture

**Smart AI System:**
```python
class HybridAI:
    def __init__(self, mode: str = "hybrid"):
        self.mode = mode
        self.real_ai = RealAI() if self._has_api_keys() else None
        self.mock_ai = EnhancedMockAI()
        self.fallback_count = 0
    
    async def analyze_deal(self, deal_data):
        if self.mode == "real" and self.real_ai:
            try:
                return await self.real_ai.analyze(deal_data)
            except Exception as e:
                logger.warning(f"Real AI failed: {e}")
                if self.mode == "hybrid":
                    return await self._fallback_to_mock(deal_data)
                raise
        
        elif self.mode == "hybrid":
            # Try real AI first, fallback to mock
            if self.real_ai and self.fallback_count < 3:
                try:
                    result = await self.real_ai.analyze(deal_data)
                    self.fallback_count = 0  # Reset on success
                    return result
                except Exception:
                    self.fallback_count += 1
                    return await self._fallback_to_mock(deal_data)
            else:
                return await self.mock_ai.analyze(deal_data)
        
        else:  # mode == "mock"
            return await self.mock_ai.analyze(deal_data)
```

## 🎛️ Configuration Dashboard

**Admin Panel Features:**
- 🔧 **AI Mode Switching** - Real-time toggle между mock/real AI
- 📊 **Usage Analytics** - API calls, response times, error rates
- 🔑 **API Key Management** - Secure storage и rotation
- 📈 **Performance Monitoring** - AI service health checks
- 🚨 **Alert Configuration** - Notifications для failures
- 💾 **Cache Management** - Redis cache controls

```python
@router.get("/admin/ai-config")
async def get_ai_configuration():
    return {
        "current_mode": settings.ai_mode,
        "available_modes": ["mock", "real", "hybrid"],
        "api_keys_configured": {
            "openai": bool(settings.openai_api_key),
            "anthropic": bool(settings.anthropic_api_key)
        },
        "fallback_count": ai_service.fallback_count,
        "cache_stats": await get_redis_stats(),
        "last_24h_usage": await get_usage_stats()
    }

@router.post("/admin/switch-ai-mode")
async def switch_ai_mode(new_mode: str):
    if new_mode not in ["mock", "real", "hybrid"]:
        raise HTTPException(400, "Invalid AI mode")
    
    settings.ai_mode = new_mode
    await ai_service.reinitialize(new_mode)
    
    return {
        "message": f"AI mode switched to {new_mode}",
        "effective_immediately": True,
        "fallback_available": new_mode == "hybrid"
    }
```

## 💾 Production Database Schema

**Enhanced PostgreSQL Structure:**
```sql
-- Enhanced Users with roles
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    hashed_password VARCHAR(255),
    role user_role DEFAULT 'trader',
    is_active BOOLEAN DEFAULT true,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Deals with comprehensive tracking
CREATE TABLE deals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(200) NOT NULL,
    commodity VARCHAR(50),
    quantity DECIMAL(15,2),
    price DECIMAL(12,2),
    counterparty VARCHAR(100),
    status deal_status DEFAULT 'draft',
    user_id UUID REFERENCES users(id),
    ai_analysis_id UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI Analysis results
CREATE TABLE ai_analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deal_id UUID REFERENCES deals(id),
    ai_mode VARCHAR(20) NOT NULL,  -- mock/real/hybrid
    model_used VARCHAR(50),         -- gpt-4-turbo/claude/mock
    analysis_data JSONB,
    confidence DECIMAL(3,2),
    processing_time_ms INTEGER,
    api_cost DECIMAL(10,4),         -- API costs tracking
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- System configuration
CREATE TABLE system_config (
    key VARCHAR(100) PRIMARY KEY,
    value JSONB,
    updated_by UUID REFERENCES users(id),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Usage analytics
CREATE TABLE api_usage_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    endpoint VARCHAR(100),
    ai_mode VARCHAR(20),
    success BOOLEAN,
    response_time_ms INTEGER,
    error_message TEXT,
    user_id UUID REFERENCES users(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 Smart Fallback System

**Graceful Degradation:**
```python
@router.post("/ai/analyze-deal")
async def hybrid_deal_analysis(deal_data: DealRequest):
    analysis_start = time.time()
    
    try:
        # Attempt analysis with current mode
        result = await ai_service.analyze_deal(deal_data)
        
        # Log successful analysis
        await log_api_usage(
            endpoint="/ai/analyze-deal",
            ai_mode=ai_service.current_mode,
            success=True,
            response_time=int((time.time() - analysis_start) * 1000)
        )
        
        return {
            **result,
            "meta": {
                "ai_mode_used": ai_service.current_mode,
                "fallback_triggered": ai_service.fallback_count > 0,
                "processing_time": f"{time.time() - analysis_start:.2f}s"
            }
        }
        
    except Exception as e:
        # Log failed analysis
        await log_api_usage(
            endpoint="/ai/analyze-deal", 
            ai_mode=ai_service.current_mode,
            success=False,
            error_message=str(e)
        )
        
        # Return fallback response
        return {
            "analysis": "Fallback analysis due to AI service unavailability",
            "confidence": 0.5,
            "recommendations": ["Manual review required"],
            "meta": {
                "ai_mode_used": "fallback",
                "error": "AI service temporarily unavailable"
            }
        }
```

## 📊 Enhanced Analytics

**Performance Monitoring:**
```python
@router.get("/analytics/ai-performance")
async def ai_performance_analytics(days: int = 7):
    """
    Comprehensive AI usage analytics
    """
    return {
        "time_period": f"Last {days} days",
        "total_requests": await count_ai_requests(days),
        "success_rate": await calculate_success_rate(days),
        "avg_response_time": await avg_response_time(days),
        "mode_distribution": {
            "real_ai": await count_by_mode("real", days),
            "mock_ai": await count_by_mode("mock", days), 
            "fallback": await count_by_mode("fallback", days)
        },
        "cost_tracking": {
            "openai_cost": await calculate_openai_cost(days),
            "total_api_cost": await calculate_total_api_cost(days)
        },
        "error_analysis": await get_error_breakdown(days)
    }
```

## 🛠 Configuration Management

**Dynamic Settings:**
```python
class HybridSettings(BaseSettings):
    ai_mode: Literal["mock", "real", "hybrid"] = "hybrid"
    
    # Real AI Configuration
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    ai_timeout_seconds: int = 30
    max_fallback_attempts: int = 3
    
    # Database Configuration
    postgresql_url: str
    redis_url: str
    
    # Caching Configuration
    cache_ttl_seconds: int = 300
    cache_ai_responses: bool = True
    
    # Monitoring Configuration
    enable_usage_logging: bool = True
    enable_performance_monitoring: bool = True
    alert_on_ai_failures: bool = True
    
    class Config:
        env_file = ".env"
```

## 🚢 Deployment Strategies

**Multi-Environment Setup:**
```bash
# Development (Mock AI)
export AI_MODE=mock
./deploy.sh --env development

# Staging (Hybrid AI) 
export AI_MODE=hybrid
export OPENAI_API_KEY=sk-staging-...
./deploy.sh --env staging

# Production (Real AI with fallback)
export AI_MODE=hybrid
export OPENAI_API_KEY=sk-prod-...
export ANTHROPIC_API_KEY=sk-ant-prod-...
./deploy.sh --env production
```

**Infrastructure:**
- **Frontend**: Vercel с environment-specific configs
- **Backend**: Railway с auto-scaling
- **Database**: Railway PostgreSQL с connection pooling
- **Cache**: Upstash Redis с persistence
- **Monitoring**: DataDog + custom metrics

## 🎯 Client Demo Scenarios

### **Scenario 1: Cost-Conscious Client**
- Start в mock mode - "Полная функциональность без AI costs"
- Demonstrate switching to hybrid - "Можем включить AI когда needed"
- Show analytics - "Мониторим usage и контролируем costs"

### **Scenario 2: Enterprise Security Client**
- Show fallback mechanisms - "System никогда не падает"  
- Demonstrate admin controls - "Full control над AI settings"
- Analytics dashboard - "Complete visibility в system performance"

### **Scenario 3: Scalability-Focused Client**
- PostgreSQL performance - "Production-ready database"
- Redis caching - "Sub-second response times"
- Configuration flexibility - "Easy scaling по мере роста"

## 💡 Business Advantages

- **💰 Cost Optimization** - Pay for AI только when needed
- **🛡️ Risk Mitigation** - Fallback mechanisms ensure uptime
- **📊 Full Visibility** - Complete analytics и monitoring
- **🔧 Operational Flexibility** - Switch modes без downtime
- **🚀 Scalable Architecture** - Ready для enterprise deployment
- **⚡ Performance** - Redis caching + PostgreSQL optimization

## 🔄 Migration Paths

**From Other Versions:**
```bash
# Migrate from v4-minimal
./migrate.sh --from minimal --to hybrid

# Migrate from v2-enhanced-mock  
./migrate.sh --from enhanced-mock --to hybrid

# Upgrade to v1-full-ai
./migrate.sh --from hybrid --to full-ai
```

---

**Perfect solution для clients who want flexibility и enterprise-readiness!** 🔄