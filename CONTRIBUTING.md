# Contributing

Thanks for your interest in TraceLens.

## Scope

TraceLens is an evidence-first, passive DNS research tool. Contributions must preserve its bounded, non-intrusive scope. Do not add port scanning, credential testing, exploit execution, access-control bypass, or collection of private data.

## Development setup

```bash
git clone https://github.com/Vxn1r/TraceLens.git
cd TraceLens
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

On Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1`.

## Before opening a pull request

1. Add or update tests for behavior changes.
2. Run `python -m pytest -q`.
3. Keep DNS collection bounded and preserve source, method, timestamp, and confidence metadata.
4. Update the README or documentation when command behavior changes.
5. Never include local databases, private observations, credentials, or personal data.

GitHub Actions runs the test suite on supported Python versions for pushes and pull requests.

## Style

- Prefer small, focused changes.
- Use clear names and helpful error messages.
- Keep network-dependent behavior out of unit tests by injecting or mocking resolvers.
- Document limitations; do not describe observations as proof of ownership or vulnerability.
