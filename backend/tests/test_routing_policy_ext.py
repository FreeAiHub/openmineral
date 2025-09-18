# Additional tests for routing policy: registry-based overrides and model info usage.

from backend.routing_policy import select_model_for_task, ModelInfo

def test_registry_override_direct():
    # Build a tiny registry mapping task key to a ModelInfo
    reg = {
        "risk": ModelInfo(
            name="custom-model",
            provider="test",
            latency_ms=5.0,
            cost_per_token=0.0,
            max_tokens=2048,
            active=True
        )
    }
    assert select_model_for_task("risk", registry=reg) == "custom-model"

def test_registry_fallback_when_missing():
    # If registry doesn't contain the task type, fallback to policy
    reg = {
        "local": ModelInfo(
            name="local-model",
            provider="test",
            latency_ms=3.0,
            cost_per_token=0.0,
            max_tokens=1024,
            active=True
        )
    }
    # Should fall back to policy since "risk" not in registry
    assert select_model_for_task("risk", registry=reg) == "gpt-4-turbo"
