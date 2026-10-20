# Changelog

## 1.1.0 — 2026-10-20

- Re-audited the complete tracked inventory: 17 sources, 139 feature mappings, 41 capabilities and 33 integration rules.
- Added `coverage_audit.py` to validate mappings and locate repair paths by symptom, capability ID or source name.
- Added 29 regression tests; 118 total, including 288 domain/stage/region combinations.
- Linked 18 integration rules to executable behavior tests and documented 15 workflow conflict scenarios with applied outputs.
- Rebuilt Chinese and English READMEs around purpose, concrete outputs, text workflow diagrams, capability coverage and extension paths.
- Added a generated source/complementarity/module/test index and retained tested source plus logs in CI artifacts.
- Preserved the existing research and publication workflow contracts in the skill references.

## 1.0.0 — 2026-10-20

Initial public release of **ScholarRoute · 研途**.

- A single research-to-publication skill with 8 composable domain profiles and 41 workflow modules.
- 17 pinned upstream repositories, 139 capability mappings, original implementation and explicit license provenance.
- 33 conflict-resolution rules for evidence, journal facts, publication workflows and optional tools.
- Agent research guidance covering 14 capability families and 8 program/runtime layers.
- Standard-library Python tools for routing, local/online evidence records, history, fact conflicts, constraint-based venue pools and five report exports.
- Bounded OpenAlex, Crossref, DBLP and arXiv adapters with atomic import and explicit failures.
- 89 offline regressions and three fresh-agent usability cases. Local evidence and evidence-map omissions discovered in forward use were repaired before publication.
- Chinese README with complete capability details, English guide, source audit, data contracts and validation records.

Initial network-isolated API probes failed. Authorized follow-up probes retrieved one parsed record each from Crossref and arXiv; OpenAlex was rate-limited and DBLP returned a non-success response. The Python 3.11/3.12 GitHub CI matrix passed. Workflow coverage does not bundle upstream runtimes, guarantee acceptance, install the skill in every host or report unperformed research experiments.
