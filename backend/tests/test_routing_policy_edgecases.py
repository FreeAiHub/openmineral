# Edge-case tests for routing policy: empty/None task types and registry overrides.

from backend.routing_policy import ModelInfo, select_model_for_task

def test_empty_task_type_defaults():
    assert select_model_for_task("") == "gpt-4-turbo"

def test_none_task_type_defaults():
    assert select_model_for_task(None) == "gpt-4-turbo"

def test_spaces_and_case():
    assert select_model_for_task("   RiSk  ") == "gpt-4-turbo"

def test_registry_none_behaves_like_policy():
    reg = {}
    assert select_model_for_task("risk", registry=reg) == "gpt-4-turbo"

def test_registry_with_modelinfo_override():
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
