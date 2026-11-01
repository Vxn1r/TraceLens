# TraceLens architecture (v0.1)

TraceLens is intentionally split into small layers:

1. **Validation** (`validation.py`) normalizes user-supplied domain names and rejects malformed input and IP literals.
2. **Collection** (`collectors/dns.py`) makes a short, bounded set of DNS requests through the machine's configured resolver.
3. **Data model** (`models.py`) represents a single observation with a timestamp, source, method, confidence, and note.
4. **Storage** (`storage/sqlite_store.py`) persists observations in SQLite using parameterized SQL statements.
5. **Reporting** (`reporting/reports.py`) exports the same evidence as Markdown or JSON.
6. **CLI** (`cli.py`) connects the components without mixing collection, persistence, and report formatting.

## Data flow

```text
User domain
   |
   v
Validation / IDNA normalization
   |
   v
Bounded DNS collector -----> DNS resolver
   |
   v
Observation records
   |
   +-----> SQLite evidence store
   |
   +-----> Terminal summary
                 |
                 v
          Markdown / JSON report
```

## Observation fields

- `target`: normalized domain name.
- `category`: for example `DNS A` or `Manual note`.
- `value`: the returned record value or operator-entered note.
- `source`: resolver description or supplied source reference.
- `method`: how the observation was obtained.
- `confidence`: a review label, not a statistical probability.
- `observed_at`: timezone-aware ISO-8601 timestamp.
- `note`: limitations or interpretation notes.

The current schema stores each record as a separate observation. Later versions can add explicit source entities and relationship edges without treating correlation as proof.
