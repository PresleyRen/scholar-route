# Project data contract and CLI

## Contents

- Project and history
- Evidence records
- Journal facts and constraints
- Updates and conflict resolution
- Search imports and reports
- Validation boundaries

## Project and history

`init` creates one UTF-8 `project.json` with schema_version 1, stable project_id, topic, language, domain IDs, region, stage, constraints, UTC timestamps, integer revision, eight record collections and history. Do not hand-edit identity/revision fields. Running init again with the same topic resumes the existing configuration; it does not reset records or apply new configuration silently. Another topic in the same directory is an error.

Collections are `sources`, `papers`, `journals`, `claims`, `hypotheses`, `experiments`, `decisions` and `searches`: eight collections. Singular CLI kinds map to those collections. Records use explicit IDs of 1–160 ASCII letters/digits plus dot, underscore, colon or hyphen. Use meaningful local IDs; observed provider URLs belong in URL/provider_record_id fields.

The current document is authoritative state; history retains previous changed records and conflict resolutions, with one consecutive history entry per revision. Writes use a single-writer lock and temporary-file replacement, rejecting symlinked project/report files. A live lock must not be removed merely because a command wants to proceed. Inspect the writer first; a crashed process can leave a stale lock.

Core JSON files are capped at 16 MiB. Archive a faithful copy before intentionally restructuring a very large project; never truncate history silently. The code does not promise concurrent distributed storage, database migrations, a tamper-proof ledger or automatic backup.

## Evidence records

| Kind | Required useful fields | Meaning |
|---|---|---|
| source | id, title, type, accessed_at; url or local path + sha256; optional verified boolean | type: publisher/index/registry/metadata/paper/community/other. verified records the host's actual source review; it is not a cryptographic fact. |
| paper | id, title; DOI, URL, authors, year, venue, venue_type, source_ids, read_status as known | Preserve original identifiers and versions. read_status is metadata/abstract/full_text. Source discovery does not imply the full paper was read. |
| journal | id, title, issns, source_ids, facts; optional metrics and fit | ISSN checksum confirms format only. Identity needs actual primary evidence. A missing ISSN remains unverified. |
| claim | id, text, status; source_ids/paper_ids | status: proposed/supported/contested/unsupported. Supported claims require a source; the host still checks scientific support. |
| hypothesis | id, text, status; claim_ids/paper_ids | status: proposed/planned/tested/rejected/inconclusive. Add predicted outcome, alternatives and falsification criteria in notes. |
| experiment | id, text, status; hypothesis_ids/claim_ids | status: planned/running/completed/failed/blocked. Completed needs artifact and outcome strings; actual execution is a host responsibility. |
| decision | id, text, status; linked entity IDs | status: proposed/accepted/superseded. Explain reasons, evidence and relevant conflict rule. |
| search | id, provider, query, retrieved_at; paper_ids/source_ids, exhaustive | Keep failures, bounded windows and literal syntax. A true exhaustive flag requires an explicit coverage_proof for the stated bounded scope. Native imports always set false. |

DOIs normalize observed prefix/case and ISSNs validate their checksum; neither validator looks up registration. Distinct preprint/publication versions remain separate even if an arXiv record contains a later journal DOI. Use shared study/relationship notes to link related reports. Title-only records do not silently merge.

A referenced ID must already exist. Add sources before papers, and evidence before claims or assessments. Free-form notes may contain domain-specific extraction fields, methods, reported numbers, locators, research questions, code commits or limitations. Do not put credentials in records. For a local manuscript, brief, dataset or archived source, record its actual path and SHA-256; do not invent a public URL. An optional origin_url can retain the original official location. Compute the hash from the actual file with the host tools; validation checks the recorded format, not file existence or content. Local notes support statements about those notes, not external scientific findings.

## Journal facts and constraints

See [record-examples.md](record-examples.md) for concrete JSON.

Each `facts.FIELD` is an evidence object with:

- `value`: typed fact; unknown is null or omitted.
- `verification`: verified, unverified or conflicted.
- `source_ids`: reviewed evidence record IDs.
- `checked_at`: ISO date/timestamp; verified facts require it.
- Optional notes describing exact source location, population/period or applicability.

Recognized fields are `venue_type`, `indexing`, `publisher`, `mandatory_fee`, `languages`, `first_decision_days`, `external_review_days`, `acceptance_days`, `publication_days`, `article_types`, `scope` and `oa_route`. Indexing/languages/article_types are string lists. Timelines and mandatory_fee are nonnegative finite numbers. Time facts require endpoint/statistic/period explanations in notes; code stores them without treating averages as deadline guarantees.

A mandatory_fee also needs currency, `includes_all_mandatory: true` to pass a total-fee filter, and a checked publication route. Set `conditional: true` while a waiver or eligibility condition remains unresolved. Optional OA is not a mandatory fee; document that choice and the supporting official route.

Metrics are a list of objects with `system` (JCR/SJR/CAS), integer `year`, `category`, `value`, verification, checked_at and source_ids. JCR/SJR values use Q1–Q4; CAS values use string 1–4. Keep different editions/categories. Contradictory current entries for the same triple become an unknown constraint.

Optional `fit` contains score 0–5, rationale, assessed_at, source_ids and paper_ids. It records an explicit qualitative judgment. For display ranking, both assessed_at and at least one verified linked source must be within max_fact_age_days, and a referenced paper must have been read at least at abstract level. Eligible unscored candidates remain visible. The score is not a forecast or readiness label.

Supported constraints:

```json
{
  "require_journal": true,
  "required_index": "SCIE",
  "max_mandatory_fee": {"amount": 0, "currency": "USD"},
  "excluded_publishers": [],
  "allowed_languages": ["English"],
  "max_fact_age_days": 180
}
```

An optional exact-rank constraint:

```json
{
  "quartile": {
    "system": "JCR",
    "year": 2025,
    "category": "EXPLICIT CATEGORY FROM THE INDEX",
    "allowed": ["Q2", "Q3", "Q4"]
  }
}
```

The category above is a placeholder, not a real index category; replace it with observed data. Do not use quartile requirements to grade the validity of evidence studies. The 180-day default is a screening cutoff, not proof that policies cannot change sooner.

## Updates and conflict resolution

`record --kind KIND --input FILE` adds or version-merges one record. A matching observed identity can return an existing canonical ID; use that returned ID in later references. Existing source links and old metric observations are preserved. Incompatible identities require explicit reconciliation. Repeated identical records do not add revisions.

A changed journal fact retains previous/incoming evidence and enters a conflict state. Changes to a fee currency, waiver condition or all-mandatory-charges flag also count as fact changes even if the amount is unchanged. A new convenient source does not automatically win. Read both sources and explain scope, time or identity differences.

```bash
python scripts/scholar_route.py resolve --project /path/to/project \
  --journal journal-a --field mandatory_fee \
  --reason "The current official publication route supersedes the dated policy." \
  --sources publisher-policy-current
```

This adopts the currently stored incoming value, not a value guessed from the reason. To choose an earlier value, explicitly record that evidence-backed value first. Missing/unreviewed sources will not satisfy the primary-evidence assessment even if a conflict is marked resolved.

`constraints --input FILE` merges supplied constraint fields and preserves the former constraints in history. It does not delete omitted fields. Set empty lists to clear list restrictions; for a materially different study create a separate project rather than silently reusing the wrong scope.

## Search imports and reports

`search --provider openalex --query "language agent memory" --limit 10` returns a JSON envelope. `--project` atomically imports the source, metadata papers and a bounded search log. `import-search` does the same for a saved envelope. Provider failure is logged explicitly and cannot import fabricated results.

`report` writes:

- `REPORT.md`: current route, counts, candidate pools/reasons, claim/experiment states, search boundaries and sources.
- `MAP.md`: Mermaid relationships and complete entity table; capped diagram edges are disclosed.
- `journals.csv`: comparable candidate rows with spreadsheet-formula escaping.
- `references.bib`: citation metadata with escaped fields; verify both bibliography style and claim support.
- `assessment.json`: machine-readable constraints, checks, pools and heuristic ordering.

MAP.md includes all eight record types in its entity table and the first 60 recorded relationships in its diagram, including source links and journal fact/metric/fit provenance. Venue records use a neutral candidate label so a conference is not relabeled as a journal.

Generated reports use Chinese discussion labels in v1; the host can compose English or bilingual deliverables from the same evidence. The stored language guides host writing and does not automatically translate journal metadata or scientific content.

The report records a project fingerprint and revision. It does not change the evidence merely by exporting it. Read all output files before a consequential decision.

## Validation boundaries

`validate` checks the project schema, record relationships, identities, dates, numeric types and history structure. `doctor` checks available packaged references, Python and optional local rendering commands; it does not test the internet. CLI exit codes: 0 success, 2 input/local validation error, 3 provider request failure.

Tests use fictional data and isolated temporary directories. Passing them establishes specific software behaviors. It does not establish recommendation accuracy, scientific novelty, ethical approval, correct statistics for an unseen dataset, or a manuscript's publication outcome.
