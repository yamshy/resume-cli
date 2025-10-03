from pathlib import Path

import pytest

CONTRACT_PATH = Path(__file__).resolve().parents[3] / "specs" / "001-build-a-local" / "contracts" / "agents" / "bullet_composer.prompt.md"


@pytest.mark.contract
def test_bullet_composer_prompt_contract() -> None:
    """Bullet composer prompt must enforce provenance guardrails."""
    pytest.fail(
        "Contract T009 not yet implemented. Align bullet composer prompt with"
        f" {CONTRACT_PATH} before enabling this test."
    )
