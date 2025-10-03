"""Integration test placeholder verifying coverage.json linkage."""

from pathlib import Path

import pytest


@pytest.mark.integration
def test_cli_coverage_links_requirements_and_facts() -> None:
    """Integration should ensure bullets cite facts and coverage status is accurate."""
    spec_path = Path(__file__).resolve().parents[3] / "specs" / "001-build-a-local" / "spec.md"
    pytest.fail(
        "Contract T012 not yet implemented. Implement coverage linkage to satisfy"
        f" acceptance scenario 2 described in {spec_path} before enabling this test."
    )


