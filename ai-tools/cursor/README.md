# Cursor IDE Configuration for OpenMineral

This directory contains custom configurations and commands for Cursor IDE to accelerate development of the OpenMineral platform.

## Configuration Overview

The `config.json` file contains:

1. **Project Settings** - Basic project information and AI model preferences
2. **Custom Commands** - Predefined prompts for common development tasks
3. **Code Templates** - Boilerplate code snippets for quick generation
4. **Project Structure** - References to backend and frontend directories

## Custom Commands

### Generate API Endpoint
```
/generate_api_endpoint endpoint_name:"user management"
```
Creates a new FastAPI endpoint with proper error handling and documentation.

### Generate React Component
```
/generate_react_component component_name:"DealCard"
```
Creates a new React component using Ant Design with proper state management.

### Generate Database Model
```
/generate_database_model model_name:"Deal"
```
Creates a SQLAlchemy model with proper relationships and constraints.

### Generate Test Case
```
/generate_test_case function_name:"calculate_risk_score"
```
Creates a Pytest test case covering normal operation, edge cases, and error conditions.

## Code Templates

Templates are available for:
- Python FastAPI endpoints
- React components with Ant Design
- SQLAlchemy models

## Usage

1. Open the OpenMineral project in Cursor IDE
2. Use the custom commands in the AI chat panel
3. Modify the generated code as needed
4. The AI will learn from your modifications for future generations

## Best Practices

1. **Be Specific** - Provide detailed descriptions when using custom commands
2. **Review Generated Code** - Always review and test AI-generated code
3. **Update Templates** - Modify templates as the project evolves
4. **Share Knowledge** - Add new useful commands to the configuration