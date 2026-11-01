import pytest

from tracelens.collectors.dns import DNSCollector


@pytest.mark.parametrize("timeout", [0, -1, 11])
def test_timeout_must_be_within_supported_range(timeout):
    with pytest.raises(ValueError):
        DNSCollector(timeout=timeout)
