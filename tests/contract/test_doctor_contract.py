"""Contract tests for the `resumecli doctor` command."""

from pathlib import Path

import pytest


CONTRACT_PATH = Path(__file__).resolve().parents[3] / "specs" / "001-build-a-local" / "contracts" / "cli" / "doctor.contract.md"


@pytest.mark.contract
def test_doctor_contract_diagnostics_and_json_output() -> None:
    """`doctor` command must emit diagnostics and JSON per contract."""
    pytest.fail(
        "Contract T007 not yet implemented. Implement doctor diagnostics to satisfy"
        f" {CONTRACT_PATH} acceptance criteria before enabling this test."
    )


