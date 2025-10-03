from pathlib import Path

import pytest

CONTRACT_PATH = Path(__file__).resolve().parents[3] / "specs" / "001-build-a-local" / "contracts" / "agents" / "validation_reviewer.prompt.md"


@pytest.mark.contract
def test_validation_reviewer_prompt_contract() -> None:
    """Validation reviewer prompt must enforce guardrails and coverage checks."""
    pytest.fail(
        "Contract T010 not yet implemented. Align validation reviewer prompt with"
        f" {CONTRACT_PATH} before enabling this test."
    )
