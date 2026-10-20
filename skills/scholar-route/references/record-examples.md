# Record examples

All identities, journals, identifiers and numerical facts in this page are fictional fixtures. They demonstrate the schema only; do not retrieve or recommend them as real venues. Dates reflect the demonstration run, not a publisher check.

## Source

```json
{
  "id": "fixture-publisher",
  "title": "Fictional test evidence — publisher",
  "url": "https://example.org/fixtures/publisher",
  "type": "publisher",
  "accessed_at": "2026-10-20",
  "verified": true,
  "note": "SYNTHETIC FIXTURE: not an observed publisher, index or paper."
}
```

Set verified to true only after actually reviewing a source in a real project. Primary-source type and URL alone do not prove support.

## Paper

```json
{
  "id": "paper-one",
  "title": "Fictional equal-budget Agent recovery study",
  "doi": "10.5555/scholarroute-fixture-1",
  "year": 2025,
  "venue": "Fictional Journal A",
  "venue_type": "journal",
  "read_status": "abstract",
  "authors": [
    "Fixture Author"
  ],
  "source_ids": [
    "fixture-paper"
  ]
}
```

Record the real reading depth. An API search starts at metadata; do not mark an abstract or full text read without reading it.

## Journal

```json
{
  "id": "journal-a",
  "title": "Fictional Journal A",
  "issns": [
    "1234-5679"
  ],
  "source_ids": [
    "fixture-publisher"
  ],
  "facts": {
    "venue_type": {
      "value": "journal",
      "verification": "verified",
      "source_ids": [
        "fixture-publisher"
      ],
      "checked_at": "2026-10-20"
    },
    "publisher": {
      "value": "Fictional Publisher A",
      "verification": "verified",
      "source_ids": [
        "fixture-publisher"
      ],
      "checked_at": "2026-10-20"
    },
    "indexing": {
      "value": [
        "SCIE"
      ],
      "verification": "verified",
      "source_ids": [
        "fixture-index"
      ],
      "checked_at": "2026-10-20"
    },
    "mandatory_fee": {
      "value": 0,
      "verification": "verified",
      "source_ids": [
        "fixture-publisher"
      ],
      "checked_at": "2026-10-20",
      "currency": "USD",
      "includes_all_mandatory": true
    }
  },
  "fit": {
    "score": 4,
    "rationale": "Fixture only: mechanism and readership align.",
    "assessed_at": "2026-10-20",
    "source_ids": [
      "fixture-paper"
    ],
    "paper_ids": [
      "paper-one"
    ]
  }
}
```

This schema requires source records and the referenced paper to exist before adding the journal. The fit score is a qualitative assessment, not an acceptance percentage.

## Completed experiment record

A completed experiment must reference a real artifact and summarize an actually measured outcome. A command string or a planned run is insufficient evidence of completion. Use planned or blocked until the run occurs.

## Reproducible repository demo

From the repository root:

```bash
python examples/run_demo.py --project /tmp/scholar-route-demo
```

Use a fresh directory. The demo deliberately includes one eligible journal, one unknown-fee candidate and one conference excluded from a journal-only pool. Its report is illustrative, not a recommendation accuracy test.

## Local evidence

For a manuscript or brief stored locally, supply path and the SHA-256 computed from its actual bytes instead of inventing a URL. Keep type other for a user brief and distinguish its observations from published evidence. An archived official source can also retain origin_url.
