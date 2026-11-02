"""Input validation and normalization."""
from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlsplit


class ValidationError(ValueError):
    """Raised when a target is not a valid fully qualified domain name."""


_LABEL = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$", re.I)


def normalize_domain(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError("A domain name is required.")

    candidate = value.strip()
    if "://" in candidate:
        try:
            parsed = urlsplit(candidate)
            if parsed.scheme.lower() not in ("http", "https") or not parsed.hostname:
                raise ValidationError("Only a valid HTTP or HTTPS URL can be converted to a domain.")
            candidate = parsed.hostname
        except ValueError as exc:
            raise ValidationError("The supplied URL is invalid.") from exc
    elif any(char in candidate for char in "/@?#"):
        raise ValidationError("Enter a domain name or an HTTP(S) URL.")

    candidate = candidate.rstrip(".")
    if candidate.startswith("[") and candidate.endswith("]"):
        candidate = candidate[1:-1]
    try:
        ipaddress.ip_address(candidate)
    except ValueError:
        pass
    else:
        raise ValidationError("IP addresses are not accepted; enter a domain name.")

    try:
        domain = candidate.encode("idna").decode("ascii").lower()
    except UnicodeError as exc:
        raise ValidationError("The domain name is not valid IDNA.") from exc

    if len(domain) > 253 or "." not in domain:
        raise ValidationError("Enter a fully qualified domain name, such as example.com.")
    labels = domain.split(".")
    if any(not _LABEL.fullmatch(label) for label in labels):
        raise ValidationError("The domain name contains an invalid label.")
    return domain
