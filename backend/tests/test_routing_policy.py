# Tests for the routing policy that selects AI models based on task types.

from backend.routing_policy import select_model_for_task

def test_default_policy_risk():
    assert select_model_for_task("risk") == "gpt-4-turbo"

def test_default_policy_complex():
    assert select_model_for_task("complex") == "claude-3.5-sonnet"

def test_default_policy_local():
    assert select_model_for_task("local") == "llama-3.1"

def test_default_policy_unknown():
    # Any task not matching specific heuristics should fall back to default
    assert select_model_for_task("unknown task") == "gpt-4-turbo"

def test_policy_override():
    custom = {"risk": "custom-model"}
    assert select_model_for_task("risk", policy=custom) == "custom-model"
