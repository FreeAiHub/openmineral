# OpenMineral Frontend

This directory contains the ReactJS frontend application for the OpenMineral trading platform.

## Structure

- `src/` - Main source code directory
  - `components/` - Reusable UI components
    - `common/` - Common UI elements (buttons, forms, etc.)
    - `layout/` - Layout components (header, sidebar, etc.)
    - `modules/` - Module-specific components
  - `pages/` - Page components for different routes
    - `dashboard/` - Trading dashboard components
    - `deals/` - Deal management pages
    - `analytics/` - Analytics and reporting pages
    - `workflows/` - Workflow management pages
  - `services/` - API service integrations
    - `api/` - API client implementations
    - `auth/` - Authentication services
  - `utils/` - Utility functions and helpers
  - `assets/` - Static assets (images, styles, etc.)
    - `images/` - Image assets
    - `styles/` - CSS/SCSS stylesheets
  - `config/` - Frontend configuration files
  - `tests/` - Frontend tests

## Setup & Development

To install dependencies and run the development server:
```bash
npm install
npm run dev
```

## Features & Architecture

- **TypeScript & Strong Types**: All components and hooks use TypeScript for type safety.
- **Multi-Step BC Flow Wizard**: Step-by-step UI for Business Confirmation, powered by React Context API.
- **AI Suggestions**: Real-time validation warnings and recommendations from mock AI modules.
- **State Management**: Uses Context API (BCFlowContext) and React Query for server state.
- **Styling**: Tailwind CSS for utility classes and responsive design.
- **Testing**: Jest + React Testing Library for unit tests, Playwright for end-to-end tests.

## Running Tests

### Unit & Integration Tests
```bash
npm run test
```

### End-to-End Tests
```bash
npm run test:e2e
```
