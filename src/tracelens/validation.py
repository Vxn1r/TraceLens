"""Input validation and normalization."""
import ipaddress
import re

_LABEL = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$", re.I)

def normalize_domain(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("A domain name is required.")
    candidate = value.strip().rstrip(".")
    if "://" in candidate or "/" in candidate or "@" in candidate:
        raise ValueError("Enter a domain name only, without a URL, path, or email address.")
    try:
        ipaddress.ip_address(candidate.strip("[]"))
    except ValueError:
        pass
    else:
        raise ValueError("IP addresses are not accepted; enter a domain name.")
    try:
        domain = candidate.encode("idna").decode("ascii").lower()
    except UnicodeError as exc:
        raise ValueError("The domain name is not valid IDNA.") from exc
    if len(domain) > 253 or "." not in domain:
        raise ValueError("Enter a fully qualified domain name, such as example.com.")
    labels = domain.split(".")
    if any(not _LABEL.fullmatch(label) for label in labels):
        raise ValueError("The domain name contains an invalid label.")
    return domain
