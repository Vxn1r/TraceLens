"""Bounded passive DNS collection using a system-configured resolver."""
from __future__ import annotations

import dns.exception
import dns.resolver

from tracelens.models import Observation

RECORD_TYPES = ("A", "AAAA", "MX", "NS", "TXT", "CNAME")


class DNSCollector:
    """Collect a fixed set of public DNS records; never scans hosts or ports."""

    def __init__(self, timeout: float = 3.0, resolver=None) -> None:
        if timeout <= 0 or timeout > 10:
            raise ValueError("timeout must be greater than 0 and no more than 10 seconds")
        self.timeout = float(timeout)
        self.resolver = resolver or dns.resolver.Resolver()
        self.resolver.timeout = self.timeout
        self.resolver.lifetime = min(self.timeout * 3, 10.0)

    def collect(self, domain: str) -> list[Observation]:
        observations: list[Observation] = []
        for record_type in RECORD_TYPES:
            try:
                answer = self.resolver.resolve(
                    domain,
                    record_type,
                    lifetime=self.resolver.lifetime,
                    raise_on_no_answer=False,
                )
                if answer.rrset is None:
                    continue
                for record in answer:
                    observations.append(
                        Observation.now(
                            target=domain,
                            category=f"DNS {record_type}",
                            value=record.to_text(),
                            source="System-configured DNS resolver",
                            method=f"DNS query: {record_type}",
                            confidence="observed",
                            note="Public DNS response; point-in-time observation.",
                        )
                    )
            except (
                dns.resolver.NXDOMAIN,
                dns.resolver.NoAnswer,
                dns.resolver.NoNameservers,
                dns.exception.Timeout,
            ):
                continue
        return observations
