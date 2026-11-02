# TraceLens

**TraceLens** is an evidence-first, passive DNS research and evidence-management CLI. It collects a fixed set of public DNS record types, stores timestamped observations in SQLite, accepts sourced manual notes, and exports Markdown or JSON reports.

[![Tests](https://github.com/Vxn1r/TraceLens/actions/workflows/tests.yml/badge.svg)](https://github.com/Vxn1r/TraceLens/actions/workflows/tests.yml)
[![Latest release](https://img.shields.io/github/v/release/Vxn1r/TraceLens?display_name=tag)](https://github.com/Vxn1r/TraceLens/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> **Responsible use:** Use only with domains you own or are explicitly authorized to assess. TraceLens performs passive DNS queries only. It does not scan ports, attempt logins, exploit services, bypass access controls, or establish domain ownership.

## Features

- Domain normalization with IDNA support and URL-hostname extraction.
- Bounded DNS lookups for A, AAAA, MX, NS, TXT, and CNAME records.
- Android/Termux compatibility: uses the system resolver when available and falls back to public recursive resolvers when the system has no resolver configuration.
- Timestamped observations with source, method, confidence, and notes.
- Local SQLite storage and domain-filtered history.
- Sourced manual observations with explicit confidence labels.
- Markdown and JSON evidence reports.
- Automated tests and a GitHub Actions Python-version matrix (3.10–3.14).

## Requirements

- Python 3.10 or newer
- Internet access for live DNS lookups
- Windows, macOS, Linux, or Android with Termux

## Installation

### Android / Termux

Install Python and Git in Termux, then clone and install the project:

```bash
pkg update
pkg install python git
git clone https://github.com/Vxn1r/TraceLens.git
cd TraceLens
python -m pip install -r requirements-dev.txt
python main.py --help
```

If you already cloned the repository, update it with:

```bash
git pull --ff-only
python -m pip install -r requirements-dev.txt
```

### Windows

```powershell
py -m venv .venv
.venv\\Scripts\\Activate.ps1
py -m pip install -r requirements-dev.txt
py main.py --help
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python main.py --help
```

## Usage

### Collect public DNS records

```bash
python main.py lookup example.com
```

The collector queries a fixed set of DNS record types. It does not enumerate subdomains or scan hosts and ports.

### View saved observations

```bash
python main.py history example.com
```

### Add a sourced manual note

```bash
python main.py note example.com \\
  --text "Sample observation: contact page is published" \\
  --source "https://example.com/contact" \\
  --category "Public website" \\
  --confidence unverified
```

Manual notes are user-supplied and are not independently verified by TraceLens. Keep the source and context accurate.

### Export reports

```bash
python main.py report example.com --format markdown --output reports/example-report.md
python main.py report example.com --format json --output reports/example-report.json
```

### Run tests

```bash
python -m pytest -q
```

## Data and privacy

- The default local database is `data/tracelens.sqlite3`.
- Reports are created only when an output path is supplied.
- Do not commit databases, private notes, tokens, personal data, or sensitive investigation material.
- When the system resolver configuration is unavailable (as can happen in Termux), the collector uses public recursive DNS resolvers at Cloudflare and Google. DNS queries are therefore visible to the selected resolver.

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

See [Architecture](docs/architecture.md), [Responsible Use](docs/responsible-use.md), and [Contributing](CONTRIBUTING.md).

## Status

**Version 0.2.0** — an educational, early-stage project. DNS responses vary by resolver and time. Observations are point-in-time evidence, not proof of ownership, vulnerability, or security posture. Review the automated test workflow and release notes before relying on a release.

## License

MIT. See [LICENSE](LICENSE).
