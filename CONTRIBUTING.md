# Contributing to OpenMineral

We welcome contributions to the OpenMineral platform! This document provides guidelines for contributing to our AI-driven commodity trading platform.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. We are committed to providing a welcoming and inspiring community for all.

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker 24+
- Git 2.40+

### Local Development Environment
```bash
# Clone the repository
git clone https://github.com/openmineral/platform.git
cd openmineral

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup frontend
cd ../frontend
npm install

# Setup pre-commit hooks
pip install pre-commit
pre-commit install
```

### Environment Variables
Create a `.env` file in the backend directory:
```bash
# Database
POSTGRESQL_URL=postgresql://user:password@localhost:5432/openmineral
MONGODB_URL=mongodb://localhost:27017/openmineral
REDIS_URL=redis://localhost:6379/0

# AI Services
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
PINECONE_API_KEY=your_pinecone_key

# Security
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Development Guidelines

### Python Code Style
We use the following tools for code quality:
- **Black**: Code formatting
- **isort**: Import sorting
- **mypy**: Type checking
- **flake8**: Linting
- **pytest**: Testing

```bash
# Format code
black backend/
isort backend/

# Type checking
mypy backend/

# Run tests
pytest backend/tests/ -v --cov=backend/
```

### TypeScript/React Code Style
- **ESLint**: Linting configuration
- **Prettier**: Code formatting
- **Vitest**: Unit testing
- **Playwright**: End-to-end testing

```bash
# Lint and format
npm run lint
npm run format

# Run tests
npm run test
npm run test:e2e
```

### Git Workflow

1. **Fork the repository** and create your feature branch
```bash
git checkout -b feature/amazing-feature
```

2. **Make your changes** following our coding standards

3. **Commit your changes** using conventional commits
```bash
git commit -m "feat(api): add metal price prediction endpoint"
```

4. **Push to your fork** and create a Pull Request
```bash
git push origin feature/amazing-feature
```

### Commit Message Convention
We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(trading): implement real-time position monitoring
fix(auth): resolve JWT token expiration issue
docs(api): update FastAPI endpoint documentation
```

## Testing Guidelines

### Backend Testing
```python
# Example test structure
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

@pytest.fixture
def auth_headers():
    # Login and get auth token
    response = client.post("/api/auth/token", data={
        "username": "testuser",
        "password": "testpass"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_deal(auth_headers):
    deal_data = {
        "title": "Test Copper Deal",
        "commodity": "Copper",
        "quantity": 1000,
        "price": 9200,
        "counterparty": "Test Company"
    }
    
    response = client.post("/api/deals/", json=deal_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == deal_data["title"]
```

### Frontend Testing
```javascript
// Example component test
import { render, screen, fireEvent } from '@testing-library/react';
import { vi } from 'vitest';
import DealCard from '../components/DealCard';

describe('DealCard', () => {
  const mockDeal = {
    id: 1,
    title: 'Test Deal',
    commodity: 'Copper',
    status: 'Active'
  };

  it('renders deal information correctly', () => {
    render(<DealCard deal={mockDeal} />);
    
    expect(screen.getByText('Test Deal')).toBeInTheDocument();
    expect(screen.getByText('Copper')).toBeInTheDocument();
    expect(screen.getByText('Active')).toBeInTheDocument();
  });

  it('handles edit action', () => {
    const onEdit = vi.fn();
    render(<DealCard deal={mockDeal} onEdit={onEdit} />);
    
    fireEvent.click(screen.getByText('Edit'));
    expect(onEdit).toHaveBeenCalledWith(mockDeal.id);
  });
});
```

## Documentation

### API Documentation
- All FastAPI endpoints are automatically documented with OpenAPI/Swagger
- Access docs at `http://localhost:8000/docs` when running locally
- Add comprehensive docstrings to all functions and classes

### Component Documentation
- Use Storybook for React component documentation
- Add JSDoc comments for TypeScript functions
- Include usage examples in component stories

```javascript
/**
 * DealCard component for displaying trading deal information
 * @param {Object} deal - Deal object containing deal details
 * @param {Function} onEdit - Callback function when edit is clicked
 * @param {Function} onDelete - Callback function when delete is clicked
 */
export const DealCard = ({ deal, onEdit, onDelete }) => {
  // Component implementation
};
```

## AI/ML Contributions

### Model Development
- Follow MLOps best practices with MLflow for experiment tracking
- Use DVC for data version control
- Include model evaluation metrics and benchmarks
- Document model architecture and training procedures

### LangChain Integration
```python
# Example LangChain contribution
from langchain.agents import Tool, AgentExecutor
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema import SystemMessage

def create_trading_agent():
    """Create a trading-specific LangChain agent"""
    
    tools = [
        Tool(
            name="get_market_data",
            description="Get current market data for a commodity",
            func=get_market_data
        ),
        Tool(
            name="calculate_risk",
            description="Calculate risk metrics for a trading position", 
            func=calculate_position_risk
        )
    ]
    
    system_message = SystemMessage(content="""
    You are an expert commodity trading assistant. You help traders analyze 
    market conditions, assess risks, and make informed trading decisions.
    Always consider market volatility, counterparty risk, and regulatory requirements.
    """)
    
    agent = OpenAIFunctionsAgent.from_llm_and_tools(
        llm=ChatOpenAI(model="gpt-4-turbo", temperature=0.1),
        tools=tools,
        system_message=system_message
    )
    
    return AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)
```

## Security Guidelines

### Security Best Practices
- Never commit API keys, passwords, or sensitive data
- Use environment variables for configuration
- Follow OWASP security guidelines for web applications
- Implement proper input validation and sanitization

### Reporting Security Issues
If you discover a security vulnerability, please send an email to security@openmineral.com. Do not create a public issue.

## Performance Guidelines

### Backend Performance
- Use async/await for I/O operations
- Implement proper database indexing
- Use Redis for caching frequently accessed data
- Profile code with `cProfile` for performance bottlenecks

### Frontend Performance
- Use React.memo() for expensive components
- Implement proper code splitting with lazy loading
- Optimize bundle size with tree shaking
- Use Web Workers for heavy computations

## Release Process

### Version Numbering
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist
- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in relevant files
- [ ] Security scan completed
- [ ] Performance benchmarks verified

## Community

### Getting Help
- **GitHub Discussions**: For questions and general discussion
- **GitHub Issues**: For bug reports and feature requests
- **Discord**: Real-time chat and community support
- **Stack Overflow**: Tag questions with `openmineral`

### Contribution Recognition
We recognize contributors through:
- GitHub contributor graphs
- Quarterly community highlights
- Special mention in release notes
- Invitation to contributor-only events

## Pull Request Process

1. **Update Documentation**: Ensure any new features are documented
2. **Add Tests**: Include tests for new functionality
3. **Follow Code Style**: Run linting and formatting tools
4. **Update CHANGELOG**: Add entry describing your changes
5. **Request Review**: Assign relevant maintainers for review

### Pull Request Template
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] All new and existing tests pass locally

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
```

Thank you for contributing to OpenMineral! 🚀