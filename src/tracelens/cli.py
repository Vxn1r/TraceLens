"""Command-line interface for TraceLens."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tracelens import __version__
from tracelens.collectors.dns import DNSCollector
from tracelens.models import Observation
from tracelens.reporting.reports import render_json, render_markdown
from tracelens.storage.sqlite_store import SQLiteStore
from tracelens.validation import ValidationError, normalize_domain


def _add_database_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--db", default="data/tracelens.sqlite3", help="SQLite database path (default: data/tracelens.sqlite3)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tracelens", description="Evidence-first passive domain research.", epilog="Use only for systems you own or are authorized to assess.")
    parser.add_argument("--version", action="version", version=f"TraceLens {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    lookup = commands.add_parser("lookup", help="Collect common public DNS records for one domain")
    lookup.add_argument("domain", help="Domain name, for example example.com")
    lookup.add_argument("--timeout", type=float, default=3.0, help="Per-query timeout in seconds (max 10)")
    _add_database_option(lookup)

    note = commands.add_parser("note", help="Save a sourced manual observation")
    note.add_argument("domain")
    note.add_argument("--text", required=True)
    note.add_argument("--source", required=True)
    note.add_argument("--category", default="Manual note")
    note.add_argument("--confidence", choices=("unverified", "low", "medium", "high"), default="unverified")
    _add_database_option(note)

    history = commands.add_parser("history", help="List saved observations")
    history.add_argument("domain", nargs="?")
    _add_database_option(history)

    report = commands.add_parser("report", help="Generate a Markdown or JSON report")
    report.add_argument("domain")
    report.add_argument("--format", choices=("markdown", "json"), default="markdown")
    report.add_argument("--output")
    _add_database_option(report)
    return parser


def _print_observations(observations: list[Observation]) -> None:
    if not observations:
        print("No DNS records were returned. This does not prove that records do not exist.")
        return
    print(f"{'TYPE':<12} VALUE")
    print("-" * 72)
    for item in observations:
        print(f"{item.category:<12} {item.value}")


def run(args: argparse.Namespace) -> int:
    if args.command == "lookup":
        target = normalize_domain(args.domain)
        observations = DNSCollector(timeout=args.timeout).collect(target)
        with SQLiteStore(args.db) as store:
            saved = store.add_many(observations)
            total = store.count(target)
        print(f"TraceLens lookup complete: {target}")
        print(f"New observations saved: {saved} | Total saved for target: {total}")
        print("Collection: passive DNS only; no port scanning or login attempts.")
        _print_observations(observations)
        return 0
    if args.command == "note":
        target = normalize_domain(args.domain)
        text = args.text.strip()
        source = args.source.strip()
        category = args.category.strip()
        if not text or not source or not category:
            raise ValidationError("Note text, source, and category cannot be empty.")
        observation = Observation(target=target, category=category, value=text, source=source, method="User-supplied note", confidence=args.confidence, note="Manually entered; verify the source and context independently.")
        with SQLiteStore(args.db) as store:
            store.add_many([observation])
            total = store.count(target)
        print(f"Saved one note for {target}. Total observations: {total}")
        return 0
    if args.command == "history":
        target = normalize_domain(args.domain) if args.domain else None
        with SQLiteStore(args.db) as store:
            observations = store.list_observations(target)
        if not observations:
            print("No observations found.")
            return 0
        for item in observations:
            print(f"[{item.observed_at}] {item.target} | {item.category} | {item.value}")
            print(f"  Source: {item.source} | Method: {item.method} | Confidence: {item.confidence}")
        print(f"\nTotal: {len(observations)} observation(s)")
        return 0
    if args.command == "report":
        target = normalize_domain(args.domain)
        with SQLiteStore(args.db) as store:
            observations = store.list_observations(target)
        content = render_json(target, observations) if args.format == "json" else render_markdown(target, observations)
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(content, encoding="utf-8")
            print(f"Report written to: {output_path}")
        else:
            print(content, end="")
        return 0
    return 2


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args)
    except (ValidationError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"File or network error: {exc}", file=sys.stderr)
        return 1
