# OpenMineral Database Schema Design

## Overview

This document outlines the database schema design for the OpenMineral trading platform. The platform uses a hybrid database approach:

1. **PostgreSQL** - For structured relational data (users, deals, compliance records)
2. **MongoDB** - For unstructured data (documents, reports, market analysis)
3. **Redis** - For caching and session management

## PostgreSQL Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    role VARCHAR(20) NOT NULL, -- trader, analyst, compliance, admin
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Deals Table
```sql
CREATE TABLE deals (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    commodity VARCHAR(50) NOT NULL,
    quantity DECIMAL(15,2) NOT NULL,
    price DECIMAL(15,2) NOT NULL,
    counterparty VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL, -- draft, pending, active, completed, cancelled
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### KYC Records Table
```sql
CREATE TABLE kyc_records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    full_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    nationality VARCHAR(50) NOT NULL,
    address TEXT NOT NULL,
    id_type VARCHAR(20) NOT NULL, -- passport, id_card, driver_license
    id_number VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL, -- pending, approved, rejected
    risk_level VARCHAR(10) NOT NULL, -- low, medium, high
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP,
    reviewed_by INTEGER REFERENCES users(id)
);
```

### Compliance Checks Table
```sql
CREATE TABLE compliance_checks (
    id SERIAL PRIMARY KEY,
    deal_id INTEGER REFERENCES deals(id),
    regulations TEXT[], -- Array of regulation names
    status VARCHAR(20) NOT NULL, -- compliant, non_compliant, pending
    violations TEXT[], -- Array of violation descriptions
    checked_by INTEGER REFERENCES users(id),
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Risk Assessments Table
```sql
CREATE TABLE risk_assessments (
    id SERIAL PRIMARY KEY,
    deal_id INTEGER REFERENCES deals(id),
    overall_score DECIMAL(3,1) NOT NULL, -- 0.0 to 10.0
    risk_factors JSONB, -- Detailed risk factors in JSON format
    recommendations TEXT[], -- Array of recommendation strings
    assessed_by INTEGER REFERENCES users(id),
    assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Workflow Definitions Table
```sql
CREATE TABLE workflow_definitions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    steps JSONB, -- Workflow steps in JSON format
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Workflow Executions Table
```sql
CREATE TABLE workflow_executions (
    id SERIAL PRIMARY KEY,
    workflow_id INTEGER REFERENCES workflow_definitions(id),
    deal_id INTEGER REFERENCES deals(id),
    current_step INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL, -- active, paused, completed, failed
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);
```

## MongoDB Collections

### Market Analysis Collection
```javascript
// market_analysis collection
{
  "_id": ObjectId,
  "commodity": "Iron Ore",
  "timestamp": ISODate,
  "price_data": {
    "current_price": 85.50,
    "historical_prices": [...],
    "volume": 150000
  },
  "forecasts": {
    "short_term": {...},
    "medium_term": {...},
    "long_term": {...}
  },
  "analysis": {
    "trends": [...],
    "factors": [...],
    "recommendations": [...]
  }
}
```

### Documents Collection
```javascript
// documents collection
{
  "_id": ObjectId,
  "deal_id": 1,
  "filename": "contract_iron_ore_purchase.pdf",
  "file_type": "contract",
  "uploaded_by": 1,
  "uploaded_at": ISODate,
  "content": "...", // Extracted text content for search
  "metadata": {
    "parties": [...],
    "effective_date": ISODate,
    "expiration_date": ISODate
  }
}
```

## Redis Usage

### Session Storage
- User session data with expiration
- Format: `session:{session_id} -> {user_data}`

### Caching
- Frequently accessed deal data
- Market price data
- User permissions
- Format: `cache:{key} -> {value}`

## Relationships

1. **Users** can create and manage **Deals**
2. Each **Deal** has one **KYC Record** per counterparty
3. Each **Deal** can have multiple **Compliance Checks**
4. Each **Deal** can have one **Risk Assessment**
5. **Workflow Definitions** can be executed for **Deals**
6. **Workflow Executions** track the progress of workflows for specific deals

## Indexes

### PostgreSQL Indexes
```sql
-- Performance indexes
CREATE INDEX idx_deals_status ON deals(status);
CREATE INDEX idx_deals_commodity ON deals(commodity);
CREATE INDEX idx_deals_created_by ON deals(created_by);
CREATE INDEX idx_kyc_user_id ON kyc_records(user_id);
CREATE INDEX idx_compliance_deal_id ON compliance_checks(deal_id);
CREATE INDEX idx_risk_deal_id ON risk_assessments(deal_id);
```

### MongoDB Indexes
```javascript
// Market analysis indexes
db.market_analysis.createIndex({"commodity": 1, "timestamp": -1})

// Documents indexes
db.documents.createIndex({"deal_id": 1})
db.documents.createIndex({"file_type": 1})
db.documents.createIndex({"content": "text"})
```

## Data Migration Strategy

1. **Version Control**: All schema changes are tracked with migration scripts
2. **Backward Compatibility**: New columns/fields are added with default values
3. **Rollback Plans**: Each migration includes rollback procedures
4. **Testing**: Migrations are tested in staging before production deployment

## Security Considerations

1. **Data Encryption**: Sensitive data is encrypted at rest
2. **Access Control**: Role-based access to database objects
3. **Audit Logging**: All data modifications are logged
4. **Connection Security**: SSL/TLS for database connections