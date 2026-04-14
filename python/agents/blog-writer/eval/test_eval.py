import json
import os


def test_blogger_eval_fixture_schema() -> None:
    """Validates that the local eval fixture matches the expected old-format schema."""
    dataset_path = os.path.join(
        os.path.dirname(__file__), "data", "blog_eval.test.json"
    )
    with open(dataset_path, encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, list) and data, (
        "Eval dataset must be a non-empty list"
    )
    for invocation in data:
        assert isinstance(invocation, dict)
        assert invocation.get("query")
        assert "reference" in invocation
        assert "expected_tool_use" in invocation
        assert "expected_intermediate_agent_responses" in invocation
