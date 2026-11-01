# TraceLens

TraceLens is a small Python command-line toolkit for **passive DNS research and evidence management**. It collects a bounded set of public DNS records, stores observations locally in SQLite, and exports evidence-focused Markdown or JSON reports.

> Use only with domains you own or are explicitly authorized to assess. TraceLens does not attempt authentication, exploit services, scan ports, or bypass access controls.

## Features

- Validates and normalizes domain names (including IDNA).
- Performs bounded DNS lookups for A, AAAA, MX, NS, TXT, and CNAME records.
- Stores timestamped observations in a local SQLite database.
- Adds sourced manual notes with an explicit confidence label.
- Displays observation history and exports Markdown/JSON reports.
- Includes automated tests with a fake DNS resolver; tests do not require network access.

## Requirements

- Python 3.10+
- Windows, macOS, or Linux

## Setup (Windows Command Prompt)

```cmd
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements-dev.txt
py main.py --help
```

## Setup (macOS/Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python main.py --help
```

## Usage

```bash
# Collect the supported public DNS record types
python main.py lookup example.com

# View stored observations
python main.py history example.com

# Add a sourced manual note (unverified by default)
python main.py note example.com --text "Observed contact page" --source "https://example.com/contact"

# Export a Markdown report
python main.py report example.com --format markdown --output reports/example-report.md

# Export JSON
python main.py report example.com --format json --output reports/example-report.json

# Run tests
python -m pytest
```

On Windows, replace `python` with `py` if that is your configured Python launcher.

## Data and privacy

The SQLite database is created locally at `data/tracelens.sqlite3`. Reports are written only when you request an output path. Do not commit private investigation notes, database files, tokens, or personal data.

## Project structure

```text
TraceLens/
├── main.py
├── pyproject.toml
├── requirements*.txt
├── src/tracelens/
│   ├── cli.py
│   ├── validation.py
│   ├── models.py
│   ├── collectors/dns.py
│   ├── storage/sqlite_store.py
│   └── reporting/reports.py
├── tests/
└── docs/
```

See [Architecture](docs/architecture.md) and [Responsible Use](docs/responsible-use.md).

## Current status

Version 0.1.0 — an educational, early-stage project. DNS results can vary by resolver and time; observations are evidence, not proof of ownership or security posture.

## License

MIT. See [LICENSE](LICENSE).
