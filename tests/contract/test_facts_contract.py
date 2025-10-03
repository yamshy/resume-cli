"""Contract tests for the `resumecli facts` command suite."""

from pathlib import Path

import pytest


CONTRACT_PATH = Path(__file__).resolve().parents[3] / "specs" / "001-build-a-local" / "contracts" / "cli" / "facts.contract.md"


@pytest.mark.contract
def test_facts_contract_list_confirm_doctor_flows() -> None:
    """`facts` command must mirror contract scenarios including doctor mode."""
    pytest.fail(
        "Contract T005 not yet implemented. Flesh out facts workflows to satisfy"
        f" {CONTRACT_PATH} acceptance criteria before enabling this test."
    )


