# OpenMineral LLM Architecture PR — Description Template

Date: 2025-09-18

Purpose
- Provide a ready-to-paste PR description for the feature:
  - Registry-based routing overrides for routing_policy
  - Expanded test coverage (edge cases, registry overrides)
  - ADR updates documenting registry-driven decisions
  - Preparation for CI integration of routing policy tests

What changed (high level)
- Backend
  - routing_policy.py: registry-aware routing; exact-key matching with registry, plus case-insensitive fallback
  - Added/updated tests:
    - test_routing_policy.py
    - test_routing_policy_ext.py
    - test_routing_policy_edgecases.py
    - test_routing_policy_registry.py
    - test_routing_policy_registry_ext.py
- Documentation
  - docs/development/adr/openminer-llm-architecture.md: registry override and model rotation patterns
  - docs/development/plan/openminer-llm-architecture-planning.md: planning and milestones
- ADR planning
  - Registry override, model rotation strategy, observability alignment
- CI/CD
  - Prepared routing policy test suite for CI integration (pytest steps)

Rationale
- Registry-based routing enables governance, experimentation, and safe overrides without changing business logic.
- Expanded test coverage reduces risk of regressions when introducing models or policies.
- ADR updates ensure long-term traceability and onboarding.

How to test locally
- Run full routing policy test suite:
  - pytest -q backend/tests/test_routing_policy.py backend/tests/test_routing_policy_ext.py backend/tests/test_routing_policy_edgecases.py backend/tests/test_routing_policy_registry.py backend/tests/test_routing_policy_registry_ext.py

Validation steps for reviewers
- Confirm registry override behavior:
  - Exact-key match overrides policy
  - Case-insensitive lookup works when registry key is present but capitalisation differs
- Confirm no regressions for non-registry paths (policy-based routing remains intact)
- Validate ADR updates reflect the intended architecture
- Ensure tests execute and pass locally

Review guidance
- Look for:
  - Clarity of the registry override rationale
  - Completeness and correctness of test coverage
  - Alignment with ADR and planning docs
  - Any necessary follow-up tasks (flagging, experimental toggles, etc.)

Acceptance criteria
- All routing tests pass
- Registry override paths behave as described (exact-key and case-insensitive)
- ADR updated to document the changes
- CI pipeline includes routing policy tests

Notes for maintainers
- The registry is optional and additive; existing code paths must remain backwards compatible.
- If needed, consider introducing a feature flag to enable/disable registry usage in production.

Files touched (summary)
- backend/routing_policy.py
- backend/tests/test_routing_policy.py
- backend/tests/test_routing_policy_ext.py
- backend/tests/test_routing_policy_edgecases.py
- backend/tests/test_routing_policy_registry.py
- docs/development/adr/openminer-llm-architecture.md
- docs/development/plan/openminer-llm-architecture-planning.md
- docs/development/plan/openminer-llm-architecture-pr.md (template)
