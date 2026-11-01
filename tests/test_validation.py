import pytest

from tracelens.validation import ValidationError, normalize_domain


def test_normalizes_case_and_trailing_dot():
    assert normalize_domain("  EXAMPLE.COM. ") == "example.com"


def test_accepts_url_and_uses_only_hostname():
    assert normalize_domain("https://Example.com/path?q=1") == "example.com"


def test_idna_domain_is_normalized():
    assert normalize_domain("bücher.de") == "xn--bcher-kva.de"


@pytest.mark.parametrize("value", ["", "localhost", "127.0.0.1", "example", "-bad.example", "bad_.example", "example.com/path"])
def test_rejects_invalid_inputs(value):
    with pytest.raises(ValidationError):
        normalize_domain(value)
