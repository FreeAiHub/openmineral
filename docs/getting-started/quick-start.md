# Quick Start Guide

Get OpenMineral up and running in minutes with our streamlined setup process.

## Prerequisites

- **Docker Desktop** 24.0+ with BuildKit enabled
- **Git** 2.40+ for version control
- **Modern Browser** (Chrome 120+, Firefox 121+, Safari 17+)

## 🚀 1-Minute Setup

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/openmineral/platform.git
cd openmineral

# Start all services
docker compose up -d

# Wait for services to be ready (30-60 seconds)
docker compose logs -f
```

### Option 2: Quick Development Setup

```bash
# Backend (Terminal 1)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (Terminal 2) 
cd frontend
npm install && npm run dev
```

## 🎯 First Steps

### 1. Access the Platform

Once running, navigate to:

- **Frontend Application**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Interactive API**: http://localhost:8000/redoc

### 2. Login with Demo Account

Use these demo credentials to explore the platform:

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| Trader | `trader` | `trader123` | Trading operations, deal management |
| Analyst | `analyst` | `analyst123` | Market analysis, reporting |
| Compliance | `compliance` | `compliance123` | KYC, regulatory, compliance |

### 3. Explore Key Features

#### Trading Dashboard
Navigate to the dashboard to see:
- Real-time market data for major commodities
- Active deals and portfolio overview
- AI-generated market insights
- Risk metrics and alerts

#### Create Your First Deal
1. Click **"Deals"** in the sidebar
2. Click **"Create New Deal"** 
3. Fill in deal details:
   ```
   Title: My First Copper Deal
   Commodity: Copper
   Quantity: 1000 (MT)
   Price: 9200 (USD/MT)
   Counterparty: Demo Trading Corp
   ```
4. Click **"Save"** to create the deal

#### AI-Powered Market Analysis
1. Go to **"Analytics"** page
2. View real-time price charts and forecasts
3. Explore AI-generated market insights
4. Check alternative data signals

## 🤖 AI Features Demo

### LangChain Workflow Execution

Test the AI workflow system:

```bash
# Using the API directly
curl -X POST "http://localhost:8000/api/workflow/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": 1,
    "deal_data": {
      "commodity": "copper",
      "quantity": 1000,
      "counterparty": "Demo Corp"
    }
  }'
```

### AI-Powered Deal Intelligence

Try the AI assistant:

1. Navigate to any deal in the **Deals** page
2. Click **"AI Analysis"** button
3. Ask questions like:
   - "What are the risks for this copper deal?"
   - "Should we hedge this position?"
   - "What's the market outlook for this commodity?"

## 📊 Sample Data

The platform comes with pre-loaded sample data:

- **10 sample deals** across different commodities
- **Historical price data** for major metals
- **Mock compliance records** for testing workflows
- **Sample risk assessments** with AI-generated insights

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# Core Configuration
DEBUG=true
SECRET_KEY=your-secret-key-here

# Database URLs (using Docker Compose defaults)
POSTGRESQL_URL=postgresql://openmineral:openmineral123@postgres:5432/openmineral
MONGODB_URL=mongodb://openmineral:openmineral123@mongodb:27017/openmineral
REDIS_URL=redis://redis:6379/0

# AI Service APIs (optional for demo)
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
PINECONE_API_KEY=your-pinecone-key
```

### AI Model Configuration

Enable different AI models by setting environment variables:

```bash
# OpenAI Models
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_EMBEDDING_MODEL=text-embedding-3-large

# Anthropic Models  
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Local Models (if available)
ENABLE_LOCAL_LLAMA=true
LLAMA_MODEL_PATH=/models/llama-3.1-405b
```

## 🧪 Testing the Platform

### Backend API Testing

```bash
# Run backend tests
cd backend
pytest tests/ -v

# Test specific components
pytest tests/test_deals.py -v
pytest tests/test_ai_integration.py -v
```

### Frontend Testing

```bash
# Run frontend tests
cd frontend
npm test

# End-to-end testing
npm run test:e2e
```

### AI Integration Testing

```bash
# Test LangChain workflows
python -m pytest tests/ai/ -v -k "test_langchain"

# Test model integrations
python scripts/test_ai_models.py
```

## 📚 Next Steps

Now that you have OpenMineral running:

1. **[Read the User Guide](../user-guide/trading.md)** - Learn about trading operations
2. **[Explore AI Integration](../ai/overview.md)** - Understand AI capabilities  
3. **[Check API Reference](../api/authentication.md)** - Integrate with external systems
4. **[Join the Community](../community/contributing.md)** - Contribute to the project

## 🆘 Troubleshooting

### Common Issues

#### Services Not Starting
```bash
# Check service status
docker compose ps

# View logs for specific service
docker compose logs backend
docker compose logs frontend
```

#### Database Connection Issues
```bash
# Reset database
docker compose down -v
docker compose up -d

# Check database connectivity
docker compose exec postgres psql -U openmineral -d openmineral -c "\dt"
```

#### AI Models Not Responding
1. Verify API keys are set correctly in `.env`
2. Check network connectivity to AI services
3. Review rate limits and quotas

### Getting Help

- **GitHub Issues**: [Report bugs or request features](https://github.com/openmineral/platform/issues)
- **Discussions**: [Ask questions and share ideas](https://github.com/openmineral/platform/discussions)
- **Discord**: [Real-time community support](https://discord.gg/openmineral)
- **Email**: support@openmineral.com

Welcome to the future of commodity trading! 🌟