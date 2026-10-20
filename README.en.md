# ScholarRoute

**Turn a research field, Agent project or manuscript into an evidence map, testable questions, experiment plans and a submission route.**

ScholarRoute combines literature exploration, Agent research, experiments, writing, journal selection and publication workflows through one skill entry point. It routes by **domain, contribution type and project stage**, keeping evidence and decisions in a durable project record.

[中文](README.md) · [Skill](skills/scholar-route/SKILL.md) · [Coverage and repair index](docs/COVERAGE.md) · [Source audit](docs/source-audit.md) · [Validation](docs/AUDIT-2026-10-20.md)

## What you get

| Starting point | Work performed | Deliverables |
|---|---|---|
| A research field | Map reviews, methods, evidence, competitors and open questions | Field map, candidate questions and search protocol |
| An Agent idea or program | Separate capability contributions from systems contributions; compare alternatives | Falsifiable hypothesis, baselines, ablations and minimal experiment |
| Experiment results | Connect problem, mechanism, results and conclusions | Paper outline, scientific prose, citation and figure checks |
| A manuscript | Discover venues and investigate comparable papers, scope, indexing, costs and timelines | Journal dossiers, candidate pools and submission order |
| Reviewer comments | Link each concern to evidence, changes and manuscript locations | Revision plan and point-by-point response |
| An existing project | Resume the evidence ledger and history | Updated map, decisions and next actions |

## Version 1.1.0

- **8 composable domain profiles and 41 unified capabilities.**
- **17 reference repositories and 139 source-feature mappings**, covering skills, submodes and domain variants.
- **33 integration rules:** 18 linked to executable behavior tests and 15 to documented workflow scenarios.
- **118 Python regressions passing**, including 288 domain/stage/region routing combinations.
- Four native scholarly adapters: OpenAlex, Crossref, DBLP and arXiv.
- Standard-library Python utilities for routing, durable evidence, fact conflicts, venue constraints and exports.

The implementation has three cooperating layers: native Python utilities handle deterministic work; the host Agent follows the reading, research and writing workflows; host tools provide browsing, execution, graphics and specialist database access. The source-feature inventory explains how the 139 mapped upstream features contribute to the 41 modules.

## Text workflow map

```text
Field / notes / Agent code / manuscript
  -> domain + contribution + stage + practical constraints
  -> search -> identity/version checks -> reading -> evidence map
  -> competitors -> novelty audit -> hypothesis -> minimal experiment
       |                                      |
       +-- Agent capabilities                 +-- Agent systems
           planning, memory, tools, RAG            state, scheduling, recovery
       +------------------+-----------------------+
                          v
       implementation -> matched-budget baselines -> ablations -> robustness
                          |                 |
                          |                 +-> update questions and map
                          v
       argument + writing + citations + figures + simulated peer review
       venue discovery -> dossier -> indexing/cost/time -> fit comparison
                             | eligible / unverified / excluded
                             v
       submission package -> revision -> proofs -> dissemination/correction

All stages share project.json, provenance, history and decision records.
Repair loop: symptom -> capability -> source trait -> implementation -> test.
```

## Quick start

```bash
git clone https://github.com/PresleyRen/scholar-route.git
cd scholar-route
python tests/run.py
python tools/validate_package.py
python tools/coverage_audit.py --check
python examples/run_demo.py --project ./work/demo
```

Requires Python 3.11+. Install the entire `skills/scholar-route/` directory in the host's skill directory. For Codex, project and personal locations are `.agents/skills/scholar-route/` and `~/.agents/skills/scholar-route/`; see the [official skill documentation](https://learn.chatgpt.com/docs/build-skills).

```text
Use $scholar-route to investigate long-term memory and failure recovery
in LLM Agents. Resume the existing project, map the literature and competing
mechanisms, then design equal-budget baselines, ablations and a minimal test.
Distinguish capability and systems contributions. Build an SCIE submission
route from the manuscript evidence, prioritizing no-mandatory-fee options.
```

Direct CLI example:

```bash
python skills/scholar-route/scripts/scholar_route.py route \
  --topic "LLM Agent memory and recovery" \
  --domains agent-ai,computer-science --stage full
python skills/scholar-route/scripts/scholar_route.py init \
  --project ./work/agent-memory --topic "LLM Agent memory and recovery" \
  --domains agent-ai,computer-science --language en
python skills/scholar-route/scripts/scholar_route.py search \
  --provider crossref --query "language agent memory" \
  --limit 5 --project ./work/agent-memory
python skills/scholar-route/scripts/scholar_route.py report \
  --project ./work/agent-memory
```

The offline demo uses labeled synthetic journals and produces all five exports. Real projects use imported search records and investigated venue facts.

## Domain and stage routing

| Domain ID | Emphasis |
|---|---|
| `agent-ai` | Agent capabilities, mechanisms and systems |
| `computer-science` | Computer science, NLP and software engineering |
| `engineering` | Engineering, control and applied AI |
| `biomedicine` | Biomedical literature and study-design appraisal |
| `social-sciences` | Social science, psychology, education and HCI |
| `food-agriculture` | Food, nutrition and agriculture |
| `humanities` | Humanities, history and philosophy |
| `general` | Adaptable cross-domain exploration |

Combine profiles: a medical-literature Agent uses `agent-ai,computer-science,biomedicine`; a runtime-recovery project can add `engineering`. Stages are `explore`, `review`, `design`, `experiment`, `journal`, `dossier`, `write`, `audit`, `submit`, `revise`, `disseminate` and `full`. Regional routes are `international`, `china` and `turkey`.

## All 41 capabilities

| Capability IDs | Output |
|---|---|
| `intake` | Research goals, contribution type, language, budget and evidence inventory |
| `field-map` | Problem–method–evidence map and unexplored connections |
| `search-protocol` | Queries, sources, windows, screening and reproducible search log |
| `paper-search` | Multi-source scholarly records and retrieval status |
| `identifier-check` | DOI/ISSN identity, metadata and report-version relationships |
| `evidence-review` | Screening, extraction, quality appraisal and synthesis |
| `paper-notes` | Structured reading notes connected to claims |
| `novelty-audit` | Competitors, prior mechanisms, differentiators and counterexamples |
| `hypothesis-plan` | Falsifiable hypotheses, feasibility and minimal tests |
| `agent-capabilities` | Mechanism analysis and evaluation for 14 capability families |
| `agent-systems` | Architecture, workload and failure analysis across 8 runtime layers |
| `experiment-plan` | Controls, ablations, metrics, samples, budgets and stopping conditions |
| `statistics-robustness` | Statistical units, uncertainty, leakage and robustness checks |
| `implementation` | Reproduction, implementation and recorded execution |
| `data-collection` | Provenance, licensing, sampling, versions and splits |
| `state-map` | Persistent ledger, relationship map, history and resume |
| `manuscript-profile` | Problem, contribution, methods, evidence, audience and article type |
| `venue-discovery` | Candidate pool from similar papers, specialist venues and indexes |
| `venue-identity` | Exact venue identity, ISSN, publisher and publication type |
| `journal-dossier` | Scope, precedents, requirements, costs and timeline dossier |
| `indexing-metrics` | Index and quartile facts by system, edition and category |
| `costs-timelines` | Mandatory/optional fees, waivers, currency and time endpoints |
| `journal-integrity` | Concrete identity, transparency and publication-risk evidence |
| `fit-comparison` | Eligible, unverified and excluded pools with reasons |
| `submission-plan` | Justified submission order, improvements and switching criteria |
| `argument-audit` | Claim–evidence structure and missing comparisons |
| `manuscript-writing` | Scientific drafting and editing with consistent values and citations |
| `citation-audit` | Identity, version, claim support and bibliography |
| `figure-table-audit` | Values, units, sample counts, readability and venue requirements |
| `peer-review` | Complementary simulated reviews and actionable repairs |
| `venue-formatting` | Current author instructions and template adaptation |
| `cover-letter` | Contribution- and scope-specific cover letter |
| `presubmission-inquiry` | Focused editorial inquiry draft |
| `reviewer-discovery` | Expertise and conflict-of-interest candidate records |
| `authorship-credit` | Actual contributions, CRediT roles and declarations |
| `submission-preflight` | Quick/Full package checks |
| `revision-response` | Comment–response–change–location mapping |
| `proof-check` | Accepted-manuscript and proof comparison |
| `dissemination` | Summaries, presentation and public-material drafts |
| `postpublication-correction` | Error impact, evidence and correction communication |
| `regional-indexing` | Chinese and Turkish directory and submission routes |

The [coverage index](docs/COVERAGE.md) links each module to its workflow, implementation, source features and conflict checks. The [source audit](docs/source-audit.md) records the complete 17-source, 139-feature inventory.

## Agent-specific depth

**14 capability families:** task definition, routing, planning, tool use, retrieval, memory, reasoning/verification, feedback/adaptation, multi-Agent cooperation, long-horizon execution, learning, multimodal/embodied behavior, human oversight, reliability and misuse resistance.

**8 program layers:** controller/state, tool interfaces, isolation, scheduling, recovery, memory/storage, observability and deployment/reproduction.

Examples include equal-token and equal-call comparisons for multi-Agent claims; stale, conflicting and cross-task records for memory; and interruption, retries, idempotency and duplicate effects for recovery. See [Agent research protocols](skills/scholar-route/references/agent-research.md).

## Integration choices and tests

The integration preserves useful workflow contributions while selecting explicit rules for conflicting behavior: field-aware retrieval, three-state candidate eligibility, exact quartile identities, mandatory versus optional fees, separate review-time endpoints, provenance-preserving updates and complementary review roles.

**118 automated tests** comprise the existing 89 plus 29 new routing, conflict and coverage checks. One parameter-combination test covers **288 routes**. **18 conflict rules** link executable tests; **15 workflow conflicts** have saved inputs, applied outputs and review decisions. Workflow scenarios and Python test results are recorded separately in the [audit report](docs/AUDIT-2026-10-20.md).

GitHub Actions runs Python 3.11 and 3.12, retaining exact tested source and logs as artifacts. The [workflow scenario review](docs/WORKFLOW-REVIEW.md) records qualitative decisions; the original release's API probes and usability cases remain in [historical validation](docs/VALIDATION.md).

## Locate a weakness and extend the skill

```bash
python tools/coverage_audit.py --find "APC"
python tools/coverage_audit.py --find agent-systems
python tools/coverage_audit.py --find journal-recommender
```

Results identify capability IDs, workflow files, native support code, sources, conflict IDs and tests.

```text
symptom -> capability -> source trait -> workflow/code -> failing example
                                                   |
                                                   v
                  regenerate docs <- tests pass <- improve implementation
```

| Improvement | Starting point under `skills/scholar-route/` |
|---|---|
| New domain | `assets/domains.json`, `references/domains.md`, `scripts/route_core.py` |
| New upstream feature | `assets/upstreams.json`, `assets/modules.json`, corresponding reference |
| Retrieval/parser issue | `scripts/scholarly_sources.py`, `scripts/search_import.py` |
| Fee/index/eligibility issue | `scripts/venue_audit.py`, `scripts/project_store.py` |
| Agent experiments | `references/agent-research.md`, `references/exploration.md` |
| Writing/review/revision | `references/publication.md` |
| Resume/history/export issue | `scripts/project_store.py`, `scripts/reports.py` |

After a change:

```bash
python tools/update_readme.py
python tools/coverage_audit.py --write
python tools/validate_package.py
python tools/update_readme.py --check
python tools/coverage_audit.py --check
python tests/run.py
```

Add an executable regression for deterministic behavior, or a saved input/output review scenario for host-Agent workflows. Update the source-feature and conflict index together.

## Project outputs

`project.json` stores eight entity types, links, revisions and history. Exports are `REPORT.md`, `MAP.md`, `journals.csv`, `references.bib` and `assessment.json`. The v1 CLI emits Chinese report labels; the project language guides the host's research and manuscript writing.

See [data contracts](skills/scholar-route/references/data-contracts.md) and [record examples](skills/scholar-route/references/record-examples.md) for import formats. Original implementation is published under the [MIT License](LICENSE); source versions and license declarations are recorded in the [source audit](docs/source-audit.md).
