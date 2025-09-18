# OpenMineral AI Architecture Decision (ADR): LLM Orchestration, Model Rotation & Vector Search

Date: 2025-09-18
Status: Proposed

Context
OpenMineralHub aims to power commodity trading with AI-assisted workflows. The current README highlights:
- Multi-model AI stack (GPT-4 Turbo, Claude 3.5 Sonnet, Local Llama 3.1)
- LangGraph/LangChain for orchestration
- Vector storage and search via Pinecone/Weaviate
- Real-time data channels (Kafka, Redis)
- Observability and security considerations exist but lack a formal, codified ADR

Problem
1) How should the platform architecturally support multi-model AI usage, model rotation, and task-specific routing in production?
2) How to structure data flows for embeddings, vector search, and context retrieval while ensuring performance and cost-effectiveness?
3) How to ensure observability, security, and maintainability across AI workflows?

Decision
1) Establish an AI Orchestration service
   - Implement a dedicated AI Service within the backend (e.g., ai_service) that exposes a unified interface for AI tasks.
   - Use LangGraph for stateful AI workflows and LangChain agents for model-specific interactions.
   - Maintain a registry of models with per-model metadata (name, provider, latency, cost, max token limits, fallback flags).

2) Model routing policy (Task-based routing)
   - Define a mapping from task type to preferred model families, with a default fallback chain:
     - Risk analysis, rapid replies: GPT-4 Turbo
     - Complex reasoning with cost considerations: Claude 3.5 Sonnet
     - Local/offline or data-sensitive tasks: Local Llama 3.1
   - Implement a rotation/config mechanism to switch models based on:
     - Latency targets
     - Error rates or degraded performance
     - Cost budgets
   - Include a fallback policy: if primary model fails or times out, move to the next model in the chain and log the incident.

3) Vector search and context management
   - Primary vector DB: Pinecone for production; maintain the ability to switch to Weaviate if needed.
   - Embedding provider: use OpenAI embeddings or alternative models depending on cost/performance.
   - Context batching: chunk inputs, store embeddings, and fetch top-k contexts for RAG-style responses.

4) Data flow and service boundaries
   - Ingest data via existing data processing stack (Polars/Numpy/Pandas, etc.).
   - Generate embeddings and store in vector DB; retrieve relevant contexts for LLM prompts.
   - Ensure context length remains within model limits; implement summarization or pruning strategies when needed.

5) Observability, security & compliance
   - Propagate a correlation_id through requests and AI invocations for traceability.
   - Instrument with OpenTelemetry, Prometheus metrics, and structured logs (structlog).
   - Secrets management via environment variables and Kubernetes Secrets; avoid hard-coded keys.
   - Align with SOC2-like controls for auditability of AI workflows.

6) Deployment considerations
   - AI Orchestration service runs as a container in the same cluster as other services to reduce cross-service latency.
   - Feature flags for enabling/disabling specific models.
   - Testing: unit tests for routing logic, integration tests for model calls, and E2E tests for end-to-end AI workflows.

Rationale
- A dedicated AI Orchestration layer decouples AI decision-making from business logic, enabling easier rotation of models, clearer monitoring, and safer rollout strategies.
- Task-based routing allows cost/performance optimization and better governance over model usage.
- A consistent vector-search and context-management approach ensures robust RAG capabilities and scalable retrieval.
- Observability and security practices are essential for a production AI platform handling sensitive trading data.

Consequences
- Additional code paths for AI routing and model registry; requires tests and monitoring.
- Possible refactoring of current ai/chroma_service.py and related modules to align with the new orchestration service.
- Documentation updates and ADR traceability for future changes.

Status & Next Steps
- Create an AI Orchestration module with:
  - ai_service.py (unified interface)
  - routing_policy.py (task-to-model mapping with rotation logic)
  - vector_store_adapter.py (Pinecone/Weaviate abstraction)
  - integration with LangGraph workflows
- Update README/docs to reflect the new ADR and usage patterns.
- Add initial unit tests for routing logic and a basic integration test for a sample AI task.

References
- README.md describes multi-model and vector-search orientation.
- docs/mkdocs.yml for site generation and documentation layout.
