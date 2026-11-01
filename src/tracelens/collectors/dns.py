"""Bounded passive DNS collector."""
from __future__ import annotations
import dns.exception
import dns.resolver
from tracelens.models import Observation

RECORD_TYPES = ("A", "AAAA", "MX", "NS", "TXT", "CNAME")

def collect_dns(domain: str, timeout: float = 3.0, lifetime: float = 10.0, resolver=None) -> list[Observation]:
    """Collect a small fixed set of public DNS records using a bounded resolver."""
    if timeout <= 0 or lifetime <= 0 or timeout > lifetime:
        raise ValueError("Use positive timeouts with timeout no greater than lifetime.")
    dns_resolver = resolver or dns.resolver.Resolver()
    results: list[Observation] = []
    for record_type in RECORD_TYPES:
        try:
            answers = dns_resolver.resolve(domain, record_type, lifetime=lifetime, raise_on_no_answer=False)
            if answers.rrset is None:
                continue
            for answer in answers:
                results.append(Observation.now(domain, record_type, answer.to_text()))
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.exception.Timeout):
            continue
    return results
