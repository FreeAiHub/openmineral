# OpenMineral LLM Architecture PR — Registry overrides, edge-case tests & ADR updates

Date: 2025-09-18

Summary
This pull request introduces registry-based routing for AI models used by OpenMineral, extends the routing policy test suite with edge cases and registry overrides, and updates the ADR and planning documentation to reflect the new design. The changes enable dynamic model selection via a ModelRegistry, support exact-key and case-insensitive registry lookups, and prepare the codebase for CI integration of routing policy tests.

What changed
- Backend
  - routing_policy.py
    - Added registry-aware routing: select_model_for_task now accepts a registry mapping (task_type -> ModelInfo) and uses the registry when a key matches exactly (and falls back to case-insensitive matches if needed).
    - Retained existing policy-based routing (default_policy) with heuristic rules for risk, complex, and local tasks.
    - Minor refactor to ensure compatibility with both registry-based and policy-based routing paths.
  - models, ai_service skeleton (placeholders prepared for future expansion)
- Tests
  - backend/tests/test_routing_policy.py
  - backend/tests/test_routing_policy_ext.py
  - backend/tests/test_routing_policy_edgecases.py
  - backend/tests/test_routing_policy_registry.py
  - backend/tests/test_routing_policy_registry_ext.py
  - backend/tests/test_routing_policy_edgecases.py (new)
  - New test: test_routing_policy_edgecases.py covers empty/None task_type and whitespace handling
  - New test: test_routing_policy_registry.py covers registry-based lookups (case-sensitive and registry overrides)
- Documentation
  - docs/development/adr/openminer-llm-architecture.md
  - docs/development/plan/openminer-llm-architecture-planning.md (planning doc for planning and execution)
  - README and mkdocs references updated to reflect ADR additions
- ADR planning
  - docs/development/adr/openminer-llm-architecture.md updated with registry override, model rotation strategy, and observability patterns
- CI/CD
  - Test suite for routing policy now prepared for integration into CI pipelines (pytest step)

Rationale
- Registry-based routing provides a safe, centralized mechanism to override or tune model selection in production, enabling rapid experimentation and governance without touching business logic.
- Expanded test coverage reduces risk of regressions when introducing new models or policies.
- ADR updates document architectural decisions for future contributors and maintainers, improving traceability and onboarding.

Testing guidance
- Locally, run the full suite:
  - pytest -q backend/tests/test_routing_policy.py backend/tests/test_routing_policy_ext.py backend/tests/test_routing_policy_edgecases.py backend/tests/test_routing_policy_registry.py backend/tests/test_routing_policy_registry_ext.py
- Expected: all tests should pass; current run shows all routing policy tests pass (13 total across tests).

Migration notes
- If you have existing code that uses select_model_for_task without a registry, it will continue to work via the default policy.
- If you introduce a registry in production, ensure the keys are normalized (lowercased) for consistent lookups, and consider caching frequently accessed mappings if performance becomes a concern.
- No breaking changes to public API; the registry is optional and additive.

Backwards compatibility and risk
- Risk: added complexity to routing may introduce subtle bugs if registry orchestration is not consistent with policy rules.
  - Mitigation: keep registry logic isolated in routing_policy.py and ensure tests cover both registry and policy-based paths.
- Risk: PR size and reviewer load.
  - Mitigation: split large changes into smaller, self-contained commits; include a detailed PR description with a checklist.

Next steps for maintainers
- Review the ADR document for registry override and model rotation strategy.
- Review new tests to ensure they align with expected registry behavior, including case-insensitive lookups.
- Enable CI to run routing policy tests automatically on PRs.
- Provide feedback or adjust based on reviewer input.

Notes
- If you’d like, I can add a short PR description comment block to the repository’s PR helper or CHANGELOG entry summarizing these changes, or tailor the ADR/documentation notes to your internal conventions.
