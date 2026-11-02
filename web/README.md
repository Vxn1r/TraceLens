# TraceLens Web

A lightweight static web interface for TraceLens. It is designed for desktop and mobile, with no framework, build step, external JavaScript dependency, account, or API key.

## Run locally

From the repository root:

```bash
python -m http.server 8000 --directory web
```

Open `http://localhost:8000` in a browser.

## Capabilities

- Queries a fixed set of public DNS record types (A, AAAA, CNAME, MX, NS, TXT, CAA, SOA) through DNS-over-HTTPS.
- Uses Cloudflare DNS-over-HTTPS with Google Public DNS as a fallback.
- Saves timestamped snapshots and sourced manual notes in browser local storage.
- Compares a selected snapshot with the previous saved snapshot for the same domain.
- Displays a relationship map built only from returned DNS answers.
- Exports the local vault as JSON and a per-domain evidence report as Markdown.

## Privacy and scope

DNS queries are sent to the configured public resolver. The resolver receives the domain being queried. Do not submit private or sensitive domains.

The browser vault is stored locally in the current browser profile. It is not uploaded to TraceLens or synchronized between devices. Clearing browser storage can remove the vault; use the JSON export to make a backup.

The web interface does not enumerate subdomains, scan ports, probe services, attempt authentication, scrape websites, identify people, or enrich addresses with geolocation. A DNS relationship is an observed answer—not proof of ownership, control, affiliation, or physical location.

## Deployment

The static assets are mirrored into the `tracelens/` directory of the already-published portfolio repository:

`https://vxn1r.github.io/tracelens/`

The source of truth remains this `web/` directory in the TraceLens repository. When making web app changes, copy the updated `index.html`, `styles.css`, `app.js`, and `favicon.svg` into the portfolio repository's `tracelens/` directory and commit them there.
