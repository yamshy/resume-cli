from pathlib import Path

import pytest

CONTRACT_PATH = Path(__file__).resolve().parents[3] / "specs" / "001-build-a-local" / "contracts" / "agents" / "jobreq_extractor.prompt.md"


@pytest.mark.contract
def test_jobreq_extractor_prompt_contract() -> None:
    """Prompt must match JobReq extractor schema and guardrails."""
    pytest.fail(
        "Contract T008 not yet implemented. Align jobreq extractor prompt with"
        f" {CONTRACT_PATH} before enabling this test."
    )
