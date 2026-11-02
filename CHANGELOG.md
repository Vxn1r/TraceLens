# Changelog

## 0.2.0

- Added Android/Termux DNS resolver fallback for environments without `/etc/resolv.conf`.
- Added CLI workflow tests for sourced notes, history, and JSON report export.
- Added DNS collector tests, including the Termux fallback behavior.
- Expanded GitHub Actions testing to Python 3.10–3.14.
- Added Termux installation instructions and contribution guidance.
- Made report version metadata follow the installed package version.

## 0.1.0

- Initial release of the passive DNS and evidence-management CLI.
- Added domain validation, bounded DNS collection, SQLite storage, history, sourced notes, and Markdown/JSON reports.
- Added unit tests and CI workflow.
