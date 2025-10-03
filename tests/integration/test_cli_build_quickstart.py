"""Integration test placeholder for quickstart Step 5 build flow."""

from pathlib import Path

import pytest


@pytest.mark.integration
def test_cli_build_quickstart_flow() -> None:
    """`resumecli build` should produce PDF, coverage, and run logs within 60s."""
    fixtures_root = Path(__file__).resolve().parents[3] / "specs" / "001-build-a-local"
    pytest.fail(
        "Contract T011 not yet implemented. Implement build pipeline to satisfy"
        f" quickstart step 5 expectations in {fixtures_root / 'quickstart.md'} before enabling this test."
    )


