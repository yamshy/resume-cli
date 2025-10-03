"""Contract tests for the `resumecli templates` command suite."""

from pathlib import Path

import pytest


CONTRACT_PATH = Path(__file__).resolve().parents[3] / "specs" / "001-build-a-local" / "contracts" / "cli" / "templates.contract.md"


@pytest.mark.contract
def test_templates_contract_list_render_expectations() -> None:
    """`templates` command must expose metadata and rendering per contract."""
    pytest.fail(
        "Contract T006 not yet implemented. Complete templates workflows to satisfy"
        f" {CONTRACT_PATH} acceptance criteria before enabling this test."
    )


