# OpenMineral LLM Architecture PR Publishing Guide

Date: 2025-09-18

Purpose
- Provide a robust, safe, and auditable process for publishing PRs related to OpenMineral LLM architecture changes (registry overrides, ADR updates, test expansions).

Supported publishing strategies
1) GitHub CLI (gh)
- Ideal when gh CLI is available in the environment (local or CI runners).
- Requires a valid GitHub authentication context (gh auth login) or a repository secret (GITHUB_TOKEN) configured in CI.
- PR creation command (example):
  - gh pr create --base main --head feature/full-stack-bc-flow --title "feat: routing policy registry overrides tests; edge cases & ADR updates" --body "$(cat docs/development/plan/openminer-llm-architecture-pr-template.md)"
- Security notes:
  - Do not expose tokens in public channels or logs.
  - Store tokens in CI secrets (e.g., GitHub Secrets) and reference them in CI builds, not in chat transcripts.

2) GitHub REST API (PAT)
- Use when gh CLI is not available or desired.
- Requires a GitHub Personal Access Token (PAT) with repo permissions, stored securely as a CI secret (e.g., GITHUB_PAT).
- PR creation example (curl):
  - curl -X POST -H "Authorization: token $GITHUB_PAT" -H "Accept: application/vnd.github+json" \
    -d '{"title":"feat: routing policy registry overrides tests; edge cases & ADR updates","head":"feature/full-stack-bc-flow","base":"main","body":"OpenMineral routing policy updates: registry overrides, edge-case tests, ADR updates."}' \
    https://api.github.com/repos/FreeAiHub/openmineral/pulls
- Security notes:
  - Never expose PATs in logs or messages. Use CI secrets.

3) Manual publishing (UI)
- If automated methods are unavailable, create the PR manually on GitHub:
  - Copy body from docs/development/plan/openminer-llm-architecture-pr-template.md
  - Create PR from feature/full-stack-bc-flow to main with title and body
  - Attach ADR references and planning documents in the PR description

What to include in the PR body
- Summary of changes
- Rationale and architectural decisions
- Test coverage and results
- ADR references (docs/development/adr/openminer-llm-architecture.md)
- CI/CD plan or test steps (if applicable)
- Links to related planning documents (openminer-llm-architecture-planning.md)

Recommended pre-publish checks
- Confirm all routing policy tests pass locally:
  - pytest -q backend/tests/test_routing_policy.py backend/tests/test_routing_policy_ext.py backend/tests/test_routing_policy_edgecases.py backend/tests/test_routing_policy_registry.py backend/tests/test_routing_policy_registry_ext.py
- Ensure ADR and planning docs are up-to-date and referenced in the PR body.
- Validate that secrets (GH_TOKEN or PAT) are stored in CI secrets and not echoed in logs.
- Ensure the PR includes a concise checklist for reviewers (tests run, ADR reference, architectural changes).

Next steps (when you’re ready)
- Let me know which publishing method you want to use (gh CLI, REST API with PAT, or manual).
- If you want, I can generate the exact PR body content from docs/development/plan/openminer-llm-architecture-pr-template.md and draft the PR description for you to paste into the platform you choose.
- I can also prepare a minimal CI workflow snippet (GitHub Actions) to run the routing_policy tests on PRs.
