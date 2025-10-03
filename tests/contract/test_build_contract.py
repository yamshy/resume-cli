"""Contract tests for the `resumecli build` command."""

from pathlib import Path

import pytest


CONTRACT_PATH = Path(__file__).resolve().parents[3] / "specs" / "001-build-a-local" / "contracts" / "cli" / "build.contract.md"


@pytest.mark.contract
def test_build_contract_offline_artifact_generation() -> None:
    """`build` command must satisfy offline artifact guarantees (FR-001, FR-004)."""
    pytest.fail(
        "Contract T004 not yet implemented. Implement CLI build flow to satisfy"
        f" {CONTRACT_PATH} requirements before enabling this test."
    )


