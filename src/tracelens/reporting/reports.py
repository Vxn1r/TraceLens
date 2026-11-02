"""Human-readable and machine-readable report rendering."""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from typing import Iterable

from tracelens import __version__
from tracelens.models import Observation

SCOPE_NOTE = (
    "TraceLens performs bounded, passive DNS lookups and records supplied notes. "
    "It does not establish ownership, prove a vulnerability, or guarantee that "
    "an observation is complete or current."
)


def render_json(target: str, observations: Iterable[Observation]) -> str:
    items = list(observations)
    payload = {
        "tool": "TraceLens",
        "version": __version__,
        "target": target,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "scope": SCOPE_NOTE,
        "observation_count": len(items),
        "observations": [item.to_dict() for item in items],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def render_markdown(target: str, observations: Iterable[Observation]) -> str:
    items = list(observations)
    grouped: dict[str, list[Observation]] = defaultdict(list)
    for item in items:
        grouped[item.category].append(item)
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    lines = [
        f"# TraceLens report: `{target}`", "",
        f"- Generated: `{generated}`",
        f"- Version: **{__version__}**",
        f"- Observations: **{len(items)}**",
        "- Collection mode: **passive DNS + manually supplied notes**", "",
        "> **Scope note:** " + SCOPE_NOTE, "", "## Observations", "",
    ]
    if not items:
        lines.extend(["No observations are stored for this target yet.", ""])
    else:
        for category in sorted(grouped):
            lines.extend([f"### {category}", ""])
            for item in grouped[category]:
                safe_value = item.value.replace("`", "\\`")
                lines.extend([
                    f"- **Value:** `{safe_value}`",
                    f"  - **Observed at:** `{item.observed_at}`",
                    f"  - **Source:** {item.source}",
                    f"  - **Method:** {item.method}",
                    f"  - **Confidence:** `{item.confidence}`",
                ])
                if item.note:
                    lines.append(f"  - **Note:** {item.note}")
            lines.append("")
    lines.extend([
        "## Interpretation guidance", "",
        "- A returned DNS record is an observation at a point in time, not proof of ownership.",
        "- Missing records in this report do not prove that a record does not exist.",
        "- Correlate observations only when the source, timestamp, and context support the connection.",
        "- Verify important findings independently before relying on them.", "",
        "---", "[TraceLens](https://github.com/Vxn1r/TraceLens) · MIT License", "",
    ])
    return "\n".join(lines)
