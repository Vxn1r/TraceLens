"""Convenience entry point for running TraceLens from a source checkout."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from tracelens.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
