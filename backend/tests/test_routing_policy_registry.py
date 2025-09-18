from backend.routing_policy import select_model_for_task, ModelInfo

def test_registry_case_insensitive_lookup():
    reg = {"RiSk": ModelInfo(name="case-model", provider="test", latency_ms=1.0, cost_per_token=0.0, max_tokens=1000, active=True)}
    assert select_model_for_task("RISK", registry=reg) == "case-model"
