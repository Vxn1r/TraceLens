import json

from tracelens.models import Observation
from tracelens.reporting.reports import render_json, render_markdown


def sample_observation():
    return Observation(
        target="example.com",
        category="DNS A",
        value="192.0.2.10",
        source="System-configured DNS resolver",
        method="DNS query: A",
        confidence="high",
        observed_at="2026-01-01T00:00:00+00:00",
        note="Test observation",
    )


def test_json_report_is_valid_and_contains_evidence():
    report = json.loads(render_json("example.com", [sample_observation()]))
    assert report["target"] == "example.com"
    assert report["observation_count"] == 1
    assert report["observations"][0]["source"] == "System-configured DNS resolver"


def test_markdown_report_contains_caveats_and_evidence():
    report = render_markdown("example.com", [sample_observation()])
    assert "# TraceLens report: `example.com`" in report
    assert "DNS A" in report
    assert "System-configured DNS resolver" in report
    assert "Missing records" in report
