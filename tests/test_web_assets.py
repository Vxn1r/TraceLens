from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_web_app_links_its_local_assets():
    html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    assert '<link rel="stylesheet" href="./styles.css">' in html
    assert '<script defer src="./app.js"></script>' in html
    assert 'href="./favicon.svg"' in html


def test_web_app_is_passive_and_keeps_vault_in_browser():
    app = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
    page = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    for record_type in ('name: "A"', 'name: "AAAA"', 'name: "CNAME"', 'name: "MX"', 'name: "NS"', 'name: "TXT"', 'name: "CAA"', 'name: "SOA"'):
        assert record_type in app
    assert "localStorage.setItem" in app
    assert "localStorage.removeItem" in app
    assert "subdomain" in page.lower()
    assert "port" in page.lower()
    assert "Noisy scans" in page


def test_web_app_does_not_load_remote_scripts_or_styles():
    html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")
    assert '<script src="https://' not in html
    assert '@import url("https://' not in css
