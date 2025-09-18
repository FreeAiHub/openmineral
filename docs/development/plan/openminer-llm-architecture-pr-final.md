# OpenMineral LLM Architecture PR – Final Draft

Date: 2025-09-18

Overview
This document provides a concise, professional summary for publishing a PR that introduces:
- Registry-based routing overrides for the routing_policy module
- Expanded test coverage (edge cases, registry overrides)
- ADR updates covering registry-driven decisions
- Preparation for CI integration of routing policy tests

What changed (high level)
- Backend
  - routing_policy.py
    - Added registry-aware routing: select_model_for_task(task_type, registry, policy)
    - Supports exact-key lookups from a registry, plus case-insensitive fallback
    - Maintains existing policy-based routing (default_policy) with heuristic rules
- Tests
  - Added/expanded tests to cover registry overrides and edge cases:
    - test_routing_policy.py
    - test_routing_policy_ext.py
    - test_routing_policy_edgecases.py
    - test_routing_policy_registry.py
    - test_routing_policy_registry_ext.py
- Documentation
  - ADR: docs/development/adr/openminer-llm-architecture.md (registry override, model rotation, observability)
  - Planning: docs/development/plan/openminer-llm-architecture-planning.md
  - PR template reference: docs/development/plan/openminer-llm-architecture-pr-template.md
- CI/CD
  - Routing policy test suite prepared for CI (pytest steps)

Rationale
- Registry-based routing provides governance and agility for model selection without touching business logic.
- Expanded test coverage reduces risk of regressions with new models or policies.
- ADR updates ensure traceability and onboarding for new contributors.

Acceptance Criteria
- All routing tests pass, including registry override cases
- Registry lookups work with exact keys and are robust to case insensitivity
- ADR and planning docs reflect the changes
- CI workflow can run routing policy tests

How to publish (recommended approaches)
- GitHub CLI (gh)
  - Prerequisites: gh installed and authenticated (via gh auth login or repository secrets)
  - Command (example):
    - gh pr create --base main --head feature/full-stack-bc-flow --title "feat: routing policy registry overrides tests; edge cases & ADR updates" --body "$(cat docs/development/plan/openminer-llm-architecture-pr-template.md)"
- GitHub REST API (PAT)
  - Prerequisites: PAT with repo scope, stored securely in CI secrets (e.g., GITHUB_PAT)
  - Request example:
    - curl -X POST -H "Authorization: token $GITHUB_PAT" -H "Accept: application/vnd.github+json" \
      -d '{"title":"feat: routing policy registry overrides tests; edge cases & ADR updates","head":"feature/full-stack-bc-flow","base":"main","body":"OpenMineral routing policy updates: registry overrides, edge-case tests, ADR updates."}' \
      https://api.github.com/repos/FreeAiHub/openmineral/pulls
- Manual publishing
  - Create PR via GitHub UI, using the PR template body from docs/development/plan/openminer-llm-architecture-pr-template.md
  - Attach ADR/docs references in the PR description

What to include in the PR body
- Summary of changes
- Rationale and architectural decisions
- Test coverage and results
- ADR references (docs/development/adr/openminer-llm-architecture.md)
- CI/CD plan or test steps
- Links to related planning documents (openminer-llm-architecture-planning.md)

Pre-publish checks
- Run full routing policy tests locally:
  - pytest -q backend/tests/test_routing_policy.py backend/tests/test_routing_policy_ext.py backend/tests/test_routing_policy_edgecases.py backend/tests/test_routing_policy_registry.py backend/tests/test_routing_policy_registry_ext.py
- Ensure ADR/planning docs are up-to-date and referenced in PR body
- Verify that tokens/keys are not exposed in logs (use CI secrets)

Next steps
- Confirm preferred publishing method (gh CLI, REST API with PAT, or manual)
- If you want, I can generate the exact PR body content from the PR-template and draft the PR body for you
- I can also prepare a minimal GitHub Actions workflow snippet for routing policy tests

Notes
- All changes are designed to be additive and non-breaking for existing code paths.
- The registry is optional and can be toggled via code/config in the future.
