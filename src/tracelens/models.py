"""Shared evidence model used by collectors, storage, and reports."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class Observation:
    target: str
    category: str
    value: str
    source: str = "Unknown"
    method: str = "Unknown"
    confidence: str = "unverified"
    observed_at: str = ""
    note: str = ""
    id: int | None = None

    def __post_init__(self) -> None:
        if not self.observed_at:
            self.observed_at = datetime.now(timezone.utc).isoformat()

    @classmethod
    def now(cls, target: str, category: str, value: str, **kwargs: Any) -> "Observation":
        return cls(
            target=target,
            category=category,
            value=value,
            observed_at=datetime.now(timezone.utc).isoformat(),
            **kwargs,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
