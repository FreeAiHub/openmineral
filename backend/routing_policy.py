from typing import Dict, Optional

class ModelInfo:
    def __init__(
        self,
        name: str,
        provider: str,
        latency_ms: float,
        cost_per_token: float,
        max_tokens: int,
        active: bool = True,
        fallback_order: Optional[int] = None,
    ):
        self.name = name
        self.provider = provider
        self.latency_ms = latency_ms
        self.cost_per_token = cost_per_token
        self.max_tokens = max_tokens
        self.active = active
        self.fallback_order = fallback_order

class ModelRegistry:
    def __init__(self, models: Optional[Dict[str, ModelInfo]] = None):
        self.models: Dict[str, ModelInfo] = models or {}

    def register(self, name: str, info: ModelInfo) -> None:
        self.models[name] = info

    def get(self, name: str) -> Optional[ModelInfo]:
        return self.models.get(name)

def default_policy() -> Dict[str, str]:
    """
    Returns a default task_type -> model_name policy.
    """
    return {
        "risk": "gpt-4-turbo",
        "rapid": "gpt-4-turbo",
        "complex": "claude-3.5-sonnet",
        "local": "llama-3.1",
        "default": "gpt-4-turbo",
    }

def select_model_for_task(
    task_type: str,
    registry: Optional[Dict[str, ModelInfo]] = None,
    policy: Optional[Dict[str, str]] = None,
) -> str:
    """
    Simple task-based routing to pick a model name from a registry using a policy.

    - If a registry is provided and contains the exact task_type key, return that model name.
    - If a registry is provided but does not contain the exact key, try a case-insensitive match.
    - If a policy is provided, use it; otherwise, fall back to the default policy.
    - A few heuristic checks based on keywords in the task_type are used
      to choose a model.
    """
    t_key = (task_type or "").lower()
    if registry:
        if t_key in registry:
            info = registry[t_key]
            return info.name
        # Case-insensitive fallback for registry keys
        lower_map = {k.lower(): v for k, v in registry.items()}
        if t_key in lower_map:
            info = lower_map[t_key]
            return info.name

    if policy is None:
        policy = default_policy()

    t = t_key

    # Heuristic routing
    if any(k in t for k in ("risk", "rapid", "alert")):
        return policy.get("risk", policy.get("default", "gpt-4-turbo"))

    if any(k in t for k in ("complex", "reasoning", "planning")):
        return policy.get("complex", policy.get("default", "gpt-4-turbo"))

    if any(k in t for k in ("local", "offline", "on-premise")):
        return policy.get("local", policy.get("default", "gpt-4-turbo"))

    return policy.get("default", "gpt-4-turbo")
