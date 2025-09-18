# OpenMineral LLM Architecture - Planning & Implementation Plan

Date: 2025-09-18

1) Goals
- Implement an AI Orchestration service (ai_service) in the backend.
- Introduce a Model Registry and registry-driven model overrides for task-based routing.
- Use LangGraph for AI workflows and LangChain for model-specific interactions.
- Abstract vector store access (Pinecone/Weaviate) with a adapter layer.
- Enhance Observability, Security, and Monitoring across AI workflows.

2) Scope
- Backend
  - Create ai_service module skeleton to expose a unified AI task interface.
  - Extend routing_policy with registry-aware routing using a ModelRegistry.
  - Ensure select_model_for_task can consume a registry map with exact-key and case-insensitive fallbacks.
- Tests
  - Extend test coverage to include registry-based overrides, edge cases, and case-insensitive lookups.
  - Ensure all routing-related tests pass locally.
- ADR & Documentation
  - Update ADR (openminer-llm-architecture.md) to include registry override, model rotation, and observability patterns.
  - Document usage patterns in README/docs for developers.
- CI/CD
  - Integrate routing policy tests into CI workflow (pytest step with caching).
  - Ensure tests run on PRs and main merges.

3) Planned Tasks (high-level)
- [x] Create ai_service skeleton in backend (e.g., backend/ai_service.py or similar)
- [x] Integrate registry support into routing_policy.py (registry-based override)
- [x] Add tests: test_routing_policy_ext.py, test_routing_policy_edgecases.py, test_routing_policy_registry.py
- [x] Update ADR documentation with registry override details
- [ ] Extend tests to cover more edge-cases (empty/None task_type, whitespace, unknown keys)
- [ ] Add CI workflow steps for routing policy tests
- [ ] Add documentation for developers on using ModelRegistry

4) Acceptance Criteria
- All routing tests pass (including extended registry tests)
- Registry override works for exact key and case-insensitive match
- ADR updated to reflect new architectural decisions
- CI includes routing policy test execution

5) Risks & Mitigations
- Risk: Increased complexity of AI routing logic
  - Mitigation: Use clear separation between policy-based routing and registry overrides; add feature flags for registry usage.
- Risk: Performance impact from registry lookups
  - Mitigation: keep registry lookups O(1) with small caches; profile in CI.

6) Milestones
- M1: Architecture skeleton + registry integration
- M2: Testing coverage extension
- M3: ADR/documentation updates
- M4: CI integration

7) Next Steps
- Confirm and publish the plan as part of the PR description.
- Create/adjust PR to include changes and tests.
- Update ADR and documentation accordingly.

Notes
- This plan assumes existing routing_policy.py and test suite structure as of now.
- If you’d like, I can implement the plan step-by-step: add AI service skeleton, finalize registry integration, extend tests, update ADR, and wire CI.
