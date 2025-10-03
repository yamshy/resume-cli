"""Integration test placeholder for quickstart Step 4 diagnostics."""

from pathlib import Path

import pytest


@pytest.mark.integration
def test_cli_doctor_quickstart_diagnostics() -> None:
    """`resumecli doctor` should validate environment and emit JSON diagnostics."""
    quickstart_path = Path(__file__).resolve().parents[3] / "specs" / "001-build-a-local" / "quickstart.md"
    pytest.fail(
        "Contract T013 not yet implemented. Implement doctor diagnostics to satisfy"
        f" quickstart step 4 guidance in {quickstart_path} before enabling this test."
    )


