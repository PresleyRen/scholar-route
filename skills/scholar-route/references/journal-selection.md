# Journal discovery, dossier and evidence-based submission order

## Workflow

1. Build a manuscript profile: object/question, mechanism, contribution type, method role, evidence level, intended readers, language, article type, keywords and known constraints. Derive terms from the content, not the LaTeX template.
2. Route discovery by field. Combine similar papers, specialist venues, official journal lists and publisher matchers when useful. Use English/Chinese query variants and adjacent terminology where appropriate.
3. Retrieve comparable publications, preferably including recent work under a justified window and seminal methodological precedents. Distinguish journal articles, conferences and preprints. Raw matching-paper volume is not a fit score; account for large-journal volume and inspect actual examples.
4. Establish exact title, publisher, canonical URL and ISSN/eISSN/ISSN-L where supported. Preserve renamed titles and related editions. Similar names alone must not merge identities.
5. Build the dossier and verify hard requirements with current competent sources. Use a known-journal route when the user already named a target.
6. Put candidates into eligible, unverified or excluded pools. A source lookup failure creates a verification task, not a false numerical value or silent exclusion.
7. Assess topic, methods, article type, readership and comparable-paper fit with reasons. Keep this judgment separate from fact coverage, reputation and practical constraints.
8. Give an evidence-based submission order. Explain why a candidate comes first, which changes improve fit, what must be verified and when a different target makes sense. Do not describe any venue as a guaranteed acceptance.
9. Refresh decisive facts before preparing the actual submission package, then use the publication workflow and Quick/Full preflight.

## Minimum dossier

| Dimension | Record |
|---|---|
| Identity | Exact title, ISSNs, publisher, official URL, title history and journal/conference distinction. |
| Scope | Official scope, intended readers, accepted contribution/article types, explicit exclusions and exact supporting source. |
| Comparable papers | Identified articles with DOI/URL, year, relevant mechanism/method, real similarity and mismatch. Read beyond metadata for fit judgments. |
| Indexing | Responsible index authority, collection, checked date and identity match. Verify SCIE separately from ESCI or generic WoS. |
| Metrics | Named system, edition/year, category and value. Distinguish JCR, SJR and CAS; do not infer unavailable JCR fields from CAS or a local title index. |
| Charges | Chosen publication route, mandatory APC/page/color/submission charges, optional OA, currency, taxes if applicable, waivers/conditions and total basis. |
| Timelines | Desk-inclusive first decision, external review decision, acceptance and publication endpoints; statistic type, population/period and source. |
| Requirements | Initial/revision/final stage, article type, word/figure/table/reference rules, file format, data/code, AI use and relevant reporting/declaration policies. |
| Publication integrity | Verifiable ownership/contact/policies, peer-review transparency, corrections, indexing claims and concrete discrepancies. Lack of DOAJ or high volume alone is insufficient for accusations. |
| Confidence | Primary sources checked, supporting secondary/anecdotal material, missing facts, contradictions and next verification. |

Use current official instructions as requirements. Recent articles show conventions, not binding submission limits. Never copy proprietary templates, a licensed journal metrics table, personal reviewer lists or a skill's example IF/acceptance data into a reusable public skill.

## What “relatively attainable” means

Explain attainable fit through actual evidence: the journal publishes this contribution type, recent comparable studies have relevant methods/evidence, the manuscript meets its scope and basic requirements, and practical costs/resources are acceptable. Assess repairable weaknesses honestly. A lower quartile cannot establish acceptance likelihood; strong topical fit cannot compensate for false or insufficient results.

Official journal-level acceptance statistics can be reported descriptively if the definition, period and source are available. They are not personal predictions. A simulated review may prioritize revisions but cannot calibrate a manuscript's chance of acceptance.

If the user requests “冲刺 / 主投 / 备选”, use these as strategy labels and explain the assumed scope/evidence differences. Do not invent percentages. Never invent candidates to fill a fixed 2+2+1 template. For a fee-sensitive first paper, prioritize confirmed publication routes and avoid treating optional OA as mandatory or unknown cost as zero.

## Bundled constraint checks

`assess` checks recorded identity and requested constraints, requiring appropriate recorded primary evidence and a configurable freshness cutoff (default 180 days). That cutoff is a screening aid; re-check mutable facts for the actual decision even within it.

Supported constraints:

- Journal-only target.
- Exact requested index label.
- Maximum total mandatory charge and currency.
- Excluded publishers.
- Acceptable manuscript languages.
- Exact quartile system, edition year, category and allowed values.

Different currencies stay unresolved unless zero cost is confirmed or a corresponding budget is provided. Conditional waivers stay unresolved. First-decision statistics are retained as facts, not used as guaranteed-deadline filters.

A confirmed violation wins over unknowns for the excluded pool, while all check results remain visible. In the absence of a violation, any decisive unknown makes the candidate unverified. Pure structural compliance cannot prove the evidence is true.

A host-assessed 0–5 fit score needs a rationale, assessed date, linked source and at least one relevant paper actually read at abstract/full-text level. It is optional, separate from eligibility and not a publication-readiness score. Unscored eligible candidates remain visible. The display shortlist uses only current primary-supported publisher facts and groups unknown/unverified/conflicted publisher identities as unknown. It caps a publisher at two by default for diversity; it may be shorter than requested and never discards the other candidates.

Conflicting updates are preserved. The `resolve` command adopts the currently recorded incoming fact after the host reviews evidence and records a reason and source IDs. To retain an earlier value, record it explicitly before resolving; never resolve merely to satisfy a desired filter.

## Outputs

Give a manuscript profile, complete candidate table with pool and reasons, detailed dossiers for useful targets, a practical submission order, unknown verification tasks and a current source ledger. Include only relevant fields and state actual coverage. Use Chinese for discussion when requested and the intended manuscript language for manuscript-ready text.

Use the live source routes in `sources-and-tools.md` and the relevant publication stages in `publication.md`. All source-specific tradeoffs and rejected shortcuts are recorded in `conflicts.md`.
