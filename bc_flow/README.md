# OpenMineral BC Flow

Business Confirmation Flow - AI-powered multi-step form application for commodity trading deals.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Run with Docker Compose (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   cd bc_flow
   ```

2. **Start all services:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development Setup

#### Backend Setup
```bash
cd bc_flow/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn bc_flow.backend.main:app --reload
```

#### Frontend Setup
```bash
cd bc_flow/frontend
npm install
npm start
```

## 📋 Features

### Multi-Step Business Confirmation Form
1. **Deal Basics** - Seller, buyer, material, quantity
2. **Commercial Terms** - Delivery, assay data, pricing
3. **Payment Terms** - Methods, stages, surveyor
4. **Review & Submit** - Validation and confirmation
5. **Summary** - Processing results

### AI-Powered Validation
- Real-time form validation
- Smart suggestions based on market data
- Risk assessment and warnings
- Industry standard recommendations

### Background Processing
- Celery task queue for form submission
- Redis for message brokering
- 15-second processing simulation
- Real-time status updates

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  FastAPI Backend │    │   PostgreSQL    │
│                 │◄──►│                 │◄──►│                 │
│ - Multi-step    │    │ - REST API      │    │ - BC Forms      │
│   wizard        │    │ - AI Validation │    │ - Tasks         │
│ - Real-time     │    │ - Celery tasks  │    │ - Dropdown data │
│   updates       │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                    ┌─────────────────┐
                    │     Redis       │
                    │                 │
                    │ - Task queue    │
                    │ - Cache         │
                    │ - Sessions      │
                    └─────────────────┘
```

## 🔧 API Endpoints

### BC Flow Endpoints
- `POST /bc-flow/validate/step{1-3}` - Validate individual steps
- `POST /bc-flow/validate/all` - Validate complete form
- `POST /bc-flow/submit` - Submit form for processing
- `GET /bc-flow/task/{task_id}` - Check processing status
- `GET /bc-flow/dropdown-data` - Get form dropdown options

### Counterparty Management
- `GET /counterparties/` - List counterparties
- `POST /counterparties/` - Create counterparty
- `GET /counterparties/{id}` - Get counterparty details
- `PUT /counterparties/{id}` - Update counterparty
- `DELETE /counterparties/{id}` - Delete counterparty

## 🗄️ Database Schema

### Main Tables
- **counterparties** - Trading partners
- **commodities** - Available materials
- **trades** - Trade records
- **tasks** - Background processing tasks

### Key Constraints
- Quantity >= 0
- Price > 0
- KYC status validation
- Foreign key relationships

## 🐳 Docker Services

- **bc-flow-backend** - FastAPI application (port 8000)
- **bc-flow-frontend** - React application (port 3000)
- **db** - PostgreSQL database (port 5432)
- **redis** - Redis cache/message broker (port 6379)
- **celery-worker** - Background task processor

## 🔒 Security Features

- CORS protection
- Input validation with Pydantic
- SQL injection prevention
- Secure headers in nginx
- Non-root container execution

## 📊 AI Features

### Smart Validation
- Market price comparisons
- Risk factor analysis
- Industry standard recommendations
- Dynamic packaging suggestions

### Processing Simulation
- 15-second background processing
- Real-time status polling
- Confirmation number generation
- Processing result storage

## 🧪 Testing

```bash
# Backend tests
cd bc_flow/backend
pytest

# Frontend tests
cd bc_flow/frontend
npm test

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Architecture**: See `docs/` directory
- **Database Schema**: See `database/schema_design.md`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**Port conflicts:**
```bash
# Check what's using ports
lsof -i :3000
lsof -i :8000
lsof -i :5432
lsof -i :6379
```

**Database connection issues:**
```bash
# Reset database
docker-compose down -v
docker-compose up --build
```

**Frontend build issues:**
```bash
cd bc_flow/frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

## 📞 Support

For questions or issues:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation
