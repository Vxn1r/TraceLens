import json

from tracelens.cli import main


def test_manual_note_round_trip_and_json_export(tmp_path, capsys):
    database = tmp_path / "tracelens.sqlite3"
    report = tmp_path / "example.json"

    assert main([
        "note", "example.com",
        "--text", "Sample observation for workflow testing",
        "--source", "https://example.com/about",
        "--category", "Contact page",
        "--confidence", "medium",
        "--db", str(database),
    ]) == 0
    assert "Saved one note" in capsys.readouterr().out

    assert main(["history", "example.com", "--db", str(database)]) == 0
    history = capsys.readouterr().out
    assert "Sample observation for workflow testing" in history
    assert "https://example.com/about" in history
    assert "Confidence: medium" in history

    assert main([
        "report", "example.com",
        "--format", "json",
        "--output", str(report),
        "--db", str(database),
    ]) == 0
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["observation_count"] == 1
    assert payload["observations"][0]["value"] == "Sample observation for workflow testing"


def test_empty_manual_note_returns_friendly_error(tmp_path, capsys):
    result = main([
        "note", "example.com",
        "--text", "   ",
        "--source", "https://example.com",
        "--db", str(tmp_path / "empty.sqlite3"),
    ])
    captured = capsys.readouterr()
    assert result == 2
    assert "cannot be empty" in captured.err


def test_history_for_unknown_domain_is_empty(tmp_path, capsys):
    result = main([
        "history", "example.com",
        "--db", str(tmp_path / "empty.sqlite3"),
    ])
    assert result == 0
    assert "No observations found." in capsys.readouterr().out
