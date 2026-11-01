"""Shared data models for TraceLens."""
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

@dataclass(slots=True)
class Observation:
    domain: str
    record_type: str
    value: str
    observed_at: str
    source: str = "DNS resolver"
    method: str = "passive DNS lookup"
    confidence: str = "observed"
    note: str = ""

    @classmethod
    def now(cls, domain: str, record_type: str, value: str, **kwargs: Any) -> "Observation":
        stamp = datetime.now(timezone.utc).isoformat()
        return cls(domain, record_type, value, stamp, **kwargs)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
