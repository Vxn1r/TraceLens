import dns.resolver

from tracelens.collectors.dns import DNSCollector


class FakeRecord:
    def to_text(self):
        return "192.0.2.10"


class FakeAnswer:
    rrset = object()

    def __iter__(self):
        return iter([FakeRecord()])


class FakeResolver:
    timeout = None
    lifetime = None
    nameservers = None

    def __init__(self):
        self.calls = []

    def resolve(self, domain, record_type, **kwargs):
        self.calls.append((domain, record_type, kwargs))
        if record_type == "A":
            return FakeAnswer()
        raise dns.resolver.NoAnswer


def test_collector_uses_injected_resolver_and_records_observation():
    resolver = FakeResolver()
    observations = DNSCollector(timeout=2, resolver=resolver).collect("example.com")

    assert len(observations) == 1
    assert observations[0].category == "DNS A"
    assert observations[0].value == "192.0.2.10"
    assert observations[0].source == "Injected DNS resolver"
    assert len(resolver.calls) == 6


def test_termux_fallback_is_used_without_system_resolver(monkeypatch):
    fallback = FakeResolver()

    def resolver_factory(configure=True):
        if configure:
            raise dns.resolver.NoResolverConfiguration("missing resolv.conf")
        return fallback

    monkeypatch.setattr(dns.resolver, "Resolver", resolver_factory)
    collector = DNSCollector()

    assert collector.resolver is fallback
    assert fallback.nameservers == ["1.1.1.1", "8.8.8.8"]
    assert "fallback" in collector.resolver_source.lower()
