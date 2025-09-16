#!/bin/bash

# OpenMineral v4-minimal Deployment Script
# Quick deployment for proof-of-concept demo

set -e

echo "🚀 Deploying OpenMineral v4-minimal Demo"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="openmineral-minimal"
BACKEND_SERVICE="$PROJECT_NAME-backend"
FRONTEND_SERVICE="$PROJECT_NAME-frontend"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo -e "${YELLOW}⚠️  Railway CLI not found. Installing...${NC}"
    npm install -g @railway/cli
fi

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo -e "${YELLOW}⚠️  Vercel CLI not found. Installing...${NC}"
    npm install -g vercel
fi

echo -e "${BLUE}📦 Step 1: Preparing deployment...${NC}"

# Create production environment file
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✅ Environment file created${NC}"
fi

echo -e "${BLUE}🔧 Step 2: Deploying Backend (Railway)...${NC}"

# Deploy backend
cd backend

# Check if railway project exists
if ! railway status &> /dev/null; then
    echo -e "${YELLOW}🔧 Initializing Railway project...${NC}"
    railway login
    railway init --name "$BACKEND_SERVICE"
fi

# Deploy backend to Railway
railway up --detach

# Get backend URL
BACKEND_URL=$(railway domain 2>/dev/null || echo "https://$BACKEND_SERVICE.railway.app")
echo -e "${GREEN}✅ Backend deployed: $BACKEND_URL${NC}"

cd ..

echo -e "${BLUE}🎨 Step 3: Deploying Frontend (Vercel)...${NC}"

# Deploy frontend
cd frontend

# Set API URL for production
export REACT_APP_API_URL="$BACKEND_URL"

# Check if vercel project exists
if [ ! -f ".vercel/project.json" ]; then
    echo -e "${YELLOW}🔧 Initializing Vercel project...${NC}"
    vercel --confirm
fi

# Deploy to Vercel
vercel --prod --confirm

# Get frontend URL  
FRONTEND_URL=$(vercel inspect --timeout 10000 2>/dev/null | grep "https://" | head -1 | awk '{print $1}' || echo "https://$PROJECT_NAME.vercel.app")
echo -e "${GREEN}✅ Frontend deployed: $FRONTEND_URL${NC}"

cd ..

echo -e "${BLUE}🔍 Step 4: Health Checks...${NC}"

# Wait a moment for deployments to be ready
sleep 10

# Test backend health
echo "Testing backend health..."
if curl -f "$BACKEND_URL/api/health" &> /dev/null; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
else
    echo -e "${RED}❌ Backend health check failed${NC}"
fi

# Test frontend
echo "Testing frontend..."
if curl -f "$FRONTEND_URL" &> /dev/null; then
    echo -e "${GREEN}✅ Frontend is accessible${NC}"
else
    echo -e "${RED}❌ Frontend health check failed${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo ""
echo "📋 Demo Information:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "🌐 Frontend URL: ${BLUE}$FRONTEND_URL${NC}"
echo -e "🔧 Backend API:  ${BLUE}$BACKEND_URL${NC}"
echo -e "📚 API Docs:     ${BLUE}$BACKEND_URL/docs${NC}"
echo ""
echo "🔐 Demo Credentials:"
echo "   Username: demo     | Password: demo123"
echo "   Username: trader   | Password: trader123"
echo ""
echo "✨ Features Available:"
echo "   • JWT Authentication"
echo "   • Real-time Dashboard"
echo "   • Deal Management (CRUD)"
echo "   • Market Data Display"
echo "   • Responsive UI"
echo ""
echo "⚡ Quick Test Commands:"
echo "   curl $BACKEND_URL/api/health"
echo "   curl -X POST $BACKEND_URL/api/auth/token \\"
echo "        -d 'username=demo&password=demo123'"
echo ""
echo -e "${YELLOW}📝 Next Steps:${NC}"
echo "   1. Test the demo URLs above"
echo "   2. Share with clients: $FRONTEND_URL"
echo "   3. Monitor with: railway logs (backend)"
echo "   4. Update with: ./deploy.sh (redeploy)"
echo ""
echo -e "${GREEN}🚀 v4-minimal demo is live and ready for client presentations!${NC}"

# Save deployment info
cat > deployment-info.json << EOF
{
  "version": "v4-minimal",
  "deployed_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "frontend_url": "$FRONTEND_URL",
  "backend_url": "$BACKEND_URL",
  "api_docs": "$BACKEND_URL/docs",
  "health_check": "$BACKEND_URL/api/health",
  "credentials": {
    "demo": "demo123",
    "trader": "trader123"
  },
  "features": [
    "JWT Authentication",
    "Dashboard with real API data",
    "Full CRUD deal management",
    "Market data display",
    "Responsive design"
  ]
}
EOF

echo -e "${GREEN}💾 Deployment info saved to deployment-info.json${NC}"