# ScholarRoute · 研途

**From a research field to evidence-linked questions, reproducible experiments, and a publication route.**

ScholarRoute is a unified skill for research agents. It organizes literature, claims, hypotheses, experiments, journal facts, and decisions around the actual contribution and research stage. Its emphasis is LLM Agent capability research, Agent software and systems, and cost-sensitive journal selection.

[中文](README.md) · [Skill entry](skills/scholar-route/SKILL.md) · [Capability registry](skills/scholar-route/references/capabilities.md) · [Source audit](docs/source-audit.md)

## Coverage

Version 1.0.0 includes **8 domain profiles, 41 workflow modules, 17 consulted repositories, 139 provenance mappings, 33 conflict rules, and 4 native search adapters**.

The mappings include upstream skills, submodes, and domain variants. They are attribution and integration records, not 139 executable plugins. Upstream packages need not be installed. Full commit references, inspection depth, adopted capabilities, and exclusions are recorded in the [provenance manifest](skills/scholar-route/assets/upstreams.json).

The workflow covers field exploration, multilingual search, evidence synthesis, novelty assessment, experiments, manuscript positioning, journal dossiers, writing and citation audits, submission preparation, revisions, proofs, and post-publication work. “Full” means planning every applicable stage and completing what available evidence and resources permit. It does not imply exhaustive literature coverage or completed experiments.

## Install and start

The core requires **Python 3.11+ and the standard library**.

```bash
git clone https://github.com/PresleyRen/scholar-route.git
cd scholar-route
python tests/run.py
python tools/validate_package.py
python skills/scholar-route/scripts/scholar_route.py doctor
```

The installable skill directory is [skills/scholar-route](skills/scholar-route), with SKILL.md as its single entry point. Use the host's skill installer or local skill support. For Codex CLI/IDE, place the directory under a project's `.agents/skills/scholar-route/` or your personal `~/.agents/skills/scholar-route/`; compare existing versions before replacing anything. Other hosts may use different locations or selectors.

A repository download or release does not automatically install the skill or establish marketplace availability. Once the host has loaded it, a request can be:

```text
Use $scholar-route to explore LLM Agent memory and recovery.
Separate capability and systems contributions. Build an evidence map,
identify strong simple alternatives, and propose falsifiable questions
with equal-budget comparisons and a minimum experiment.
Keep unknowns explicit and continue the existing research project.
```

## Run the CLI

From the repository root:

```bash
python skills/scholar-route/scripts/scholar_route.py route \
  --topic "LLM Agent memory and recovery" \
  --domains agent-ai,computer-science --stage full

python skills/scholar-route/scripts/scholar_route.py init \
  --project ./work/agent-memory \
  --topic "LLM Agent memory and recovery" \
  --domains agent-ai,computer-science --language en

python skills/scholar-route/scripts/scholar_route.py validate \
  --project ./work/agent-memory

python skills/scholar-route/scripts/scholar_route.py report \
  --project ./work/agent-memory
```

For an offline demonstration using explicitly fictional evidence:

```bash
python examples/run_demo.py --project ./work/demo
```

With suitable network access, this command searches and imports a bounded result into an existing project:

```bash
python skills/scholar-route/scripts/scholar_route.py search \
  --provider openalex --query "language agent memory" \
  --limit 5 --project ./work/agent-memory
```

The other provider values are `crossref`, `dblp`, and `arxiv`. Each native request fetches a bounded first page: at most 100 records, a 2 MiB response, and a 1–60 second timeout. It does not exhaust pagination or read full papers. Invalid payloads, failed requests, and successful empty results remain distinct. See the [API contract](skills/scholar-route/references/sources-api.md).

| Command | Purpose |
|---|---|
| route / capabilities / doctor | Inspect routing, modules, and local dependencies |
| init | Create or resume a project for the same topic |
| record | Add or version-merge an evidence record |
| constraints / resolve | Update constraints or resolve an evidenced fact conflict |
| search / import-search | Query a provider or import a saved native envelope |
| assess / validate / report | Screen candidates, check structure, and export state |

Prepare record JSON using the [data contract](skills/scholar-route/references/data-contracts.md) and [examples](skills/scholar-route/references/record-examples.md), then use `record --project PATH --kind source --input source.json`. Add sources before papers and dependent claims. Do not edit project identity or revision fields manually.

## Route by the research object

| Domain ID | Focus |
|---|---|
| agent-ai | LLM Agent capabilities and systems |
| computer-science | Software, NLP, retrieval, and computing |
| engineering | Engineering, control, robotics, and applied AI |
| biomedicine | Biology, medicine, and public health |
| social-sciences | Psychology, education, economics, and HCI |
| food-agriculture | Food science, nutrition, and agriculture |
| humanities | History, philosophy, linguistics, and interpretation |
| general | Emerging or unclassified research |

Keyword routing is a suggestion; `--domains` supplies explicit choices. Combine profiles when the question warrants it. A biomedical literature Agent needs relevant provenance checks, while clinical requirements depend on the actual study design. Region overlays are `international`, `china`, and `turkey`. Regional databases and catalogs are source routes, not additional bundled APIs.

## Agent research

The [Agent research guide](skills/scholar-route/references/agent-research.md) covers **14 capability families**:

1. Intent and task formulation.
2. Routing and delegation.
3. Planning and decomposition.
4. Tool use.
5. Retrieval and grounding.
6. Memory and context.
7. Reasoning and verification.
8. Reflection and adaptation.
9. Multi-agent coordination.
10. Long-horizon execution.
11. Learning and optimization.
12. Multimodal or embodied action.
13. Human oversight.
14. Reliability and misuse resistance.

Its **8 system layers** are controller/state, tool boundaries, execution isolation, scheduling, recovery, memory/storage, observability, and deployment/reproducibility.

Research plans connect mechanisms to workloads, strong simple baselines, ablations, held-out tasks, contamination controls, resource accounting, uncertainty, and failure traces. Systems claims require actual code inspection and end-to-end measurements. Extra agents, retries, or tokens must not silently explain an apparent mechanism gain. A planned benchmark, mocked service check, and live experiment establish different things.

## Journal selection and unknown costs

[Journal selection](skills/scholar-route/references/journal-selection.md) evaluates scope, article type, comparable publications, evidence completeness, practical constraints, and repairable rejection risks. It does not predict personal acceptance probabilities.

| Pool | Meaning |
|---|---|
| eligible | Recorded evidence satisfies the requested hard constraints |
| unverified | No verified violation, but a decisive fact is missing, stale, conflicted, or insufficiently evidenced |
| excluded | At least one verified fact violates a hard constraint |

Eligibility is a rule-based assessment of records, not proof of scientific fit. Optional 0–5 fit scores are explicit qualitative judgments. Keep fit, evidence coverage, ranking systems, and submission strategy separate.

Unknown fees remain unknown. Optional open access is not a mandatory APC; a conditional waiver is not confirmed free publication. Include all mandatory page, color, submission, and publication charges for the chosen route, with currency and date. Nonzero currencies are not silently converted.

Verify SCIE/SSCI/ESCI separately, and preserve JCR/SJR/CAS year and category. Distinguish first decision, external review, acceptance, and publication times. Refresh changing facts before decisions. Conference literature remains useful research evidence while conferences stay outside journal-only candidate pools.

## Execution boundaries and project state

| Layer | What it provides |
|---|---|
| Native Python | Routing, evidence/history, identifiers, conflicts, constraint checks, four search adapters, and exports |
| Host workflow | Reading, scientific judgment, coding, experiments, statistics, writing, review, and preparation |
| Optional external tools | Additional databases, journal indexes, training/evaluation services, and document/rendering tools when actually available |

PubMed/PMC, Semantic Scholar, WoS/Scopus, Hugging Face, and Word/PDF/LaTeX tools are host-managed routes; listing them does not provide an integration.

No full-text subscription, GPU runtime, universal journal database, or automatic submission service is bundled. The [33 conflict rules](skills/scholar-route/references/conflicts.md) reconcile incompatible assumptions while preserving user scope, evidence, uncertainty, and authorization. Preparing a draft does not authorize sending, paying, or publishing.

`project.json` stores eight collections: sources, papers, journals, claims, hypotheses, experiments, decisions, and searches. Updates preserve history with locking and atomic replacement. Local evidence can retain its real path and SHA-256; format validation neither archives the file nor proves its scientific content.

Exports are `REPORT.md`, `MAP.md`, `journals.csv`, `references.bib`, and `assessment.json`. Version 1 report labels are Chinese; the project language guides host writing without automatically translating evidence. Keep private research projects outside this public skill repository.

## Validation, provenance, and license

The [tests](tests/run.py) use fictional data, temporary projects, and controlled provider responses. They check storage, validation, identities, conflicts, screening, exports, parsers, imports, and local evidence. The [field evaluation](docs/evaluations/field-case.md) preserves actual first-run findings and limitations.

Initial probes returned `network_error` in the restricted environment; see [first results](docs/live-smoke.json). With authorized network access, Crossref and arXiv each subsequently returned one parsed record. OpenAlex returned HTTP 429 and DBLP a non-success response, so successful retrieval for those two remains unverified. [Follow-up evidence](docs/live-smoke-authorized.json) preserves both attempts and limits. The Python 3.11/3.12 CI matrix also passed; see the [validation report](docs/VALIDATION.md). These checks do not establish scientific novelty, empirical results, or recommendation accuracy.

ScholarRoute's original instructions, schemas, code, and documentation use the [MIT License](LICENSE). The [source audit](docs/source-audit.md) links the 17 consulted repositories, pinned commits, licensing observations, and 139 mappings. Upstream licenses remain their own; upstream code, prompt text, datasets, publisher templates, and article full text are not bundled. No-license sources informed independently written general workflows without importing their protected materials.
