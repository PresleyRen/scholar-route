# Domain exploration and evidence synthesis

## Contents

- Establish the research boundary
- Route sources by the research object
- Build a reproducible search
- Turn records into an evidence map
- Audit novelty and choose a tractable question
- Plan and assess research
- Maintain and deliver the exploration
- Worked prompts and consulted workflows

## Establish the research boundary

1. Reuse the user's existing project, research question, manuscript, constraints and decisions. Read the project's current state before starting another survey. Do not ask for information already supplied.
2. Extract the research object, target population or workload, problem, proposed mechanism, contribution type, audience, language, date range, resources and desired deliverable. Separate a topic ("agent memory") from an answerable question ("does selective retention improve task success under a fixed context budget?").
3. Mark the task as exploratory landscape, narrative review, scoping review, systematic review, novelty audit, experiment planning or update. A quick landscape is useful without calling it a systematic review.
4. Choose one primary domain and any justified secondary domain. Let explicit context override keyword matches. "Agent" may mean an LLM controller, a simulated economic actor or a chemical agent; the word alone cannot determine the route.
5. For "explore the entire field", establish an explicit coverage contract: subareas, timespan, languages, artifact types, source families and exclusions. Explain that coverage is bounded by this contract and accessible evidence. Do not claim that all research or all relevant skills have been exhausted.
6. Make a provisional plan immediately. Ask only when a missing decision would materially change the research or block a dependent action. Continue the independent work while recording unknowns.

Represent the research question with a domain-appropriate structure. Use task–mechanism–setting–outcome for Agent and systems work; use a suitable population/intervention/comparator/outcome or exposure formulation when it fits a biomedical question. Do not force one discipline's question format onto every field.

## Route sources by the research object

These are discovery routes, not a claim that every service has a bundled API adapter. Use an available connector, documented API, lawful web access or supplied export; record which route actually ran.

| Domain or layer | Complementary discovery routes | Additional checks |
|---|---|---|
| Agent capabilities, ML, NLP | OpenAlex, Semantic Scholar, DBLP, arXiv, publisher proceedings and journal sites | Link preprint and published versions; retain relevant conference evidence while keeping a journal-only venue pool separate. |
| Agent programs, software and systems | The CS routes plus official artifact repositories, archival releases and benchmark documentation | Read executable code/configuration and original evaluation methods where accessible; repository popularity does not establish correctness. |
| Medicine and life sciences | PubMed, PMC, Europe PMC, relevant preprint servers, study registries and field databases | Check study design, human/animal requirements when applicable, corrections, cohort overlap and reporting guidance. |
| Engineering and physical sciences | OpenAlex, Crossref, discipline repositories, society/publisher portals and relevant standards | Distinguish laboratory, simulation and deployment evidence; verify any applicable standard and version. |
| Social sciences, HCI and humanities | OpenAlex, field indexes, institutional repositories, cited primary works and suitable regional databases | Preserve context, sampling, construct validity, qualitative evidence and language coverage. Do not rank all designs by a clinical hierarchy. |
| Food, nutrition and agriculture | Biomedical routes where relevant plus agricultural/food databases and original journal sites | Distinguish food chemistry, clinical nutrition, animal work and agricultural engineering; use the corresponding methods and reporting rules. |
| Chinese-language scholarship | Relevant CNKI/Wanfang/VIP records, official catalogs, journal sites and supplied exports | Use catalog labels with edition/year. Verify publication identity through the competent official source; do not bypass access restrictions. |
| Turkish-language scholarship | Relevant TR Dizin records, DergiPark journal pages and official publisher/institution sources | Check the intended language, current scope, publication identity and actual index requirements rather than treating a hosting platform as an index. |
| Cross-domain and lawful full text | Crossref, CORE, Unpaywall, Zenodo, Figshare and institutional repositories | Registration, repository deposit and open access are different facts; none proves peer review or journal index coverage. |

For entity-centric biomedical searches, databases such as PubTator or BioStudies can enrich background or link data. For institution identity, ROR can disambiguate organizations. These functions do not replace a literature search. Use DOAJ for its actual open-access journal information, and OpenCitations for citation links; neither is a universal quality score.

## Build a reproducible search

1. Start with concept groups: task/object, mechanism, setting, outcomes and synonyms. Include Chinese/English variants when the question warrants them. Retain negative or contradictory results and established non-fashionable terminology.
2. Construct several source-specific queries. Translate Boolean syntax, field tags and date filters rather than assuming one query language works everywhere. Keep the literal executed query, not just a paraphrase.
3. Pilot against known relevant papers supplied by the user or verified during scoping. Explain known misses and revise the strategy. A hand-picked seed set is a diagnostic, not ground truth for global recall.
4. Combine keyword search with backward/forward citation chaining, surveys, classic work, adjacent fields, direct competitors and counterexamples. For emerging Agent work, record the retrieval date and update important claims near delivery.
5. Log source, interface, query, filters, timestamp, pagination/cursor, returned count, retained count, access failure and truncation. Record whether counts describe all results or only the fetched window.
6. Respect documented rate limits and credentials requirements. Check current contracts when an API changes. Do not treat an HTTP 200 error payload as valid data, retry indefinitely, or log secrets in URLs.
7. Distinguish unavailable service, unavailable full text, no results, rejected query and exhausted pagination. These outcomes support different conclusions.
8. Preserve source records before normalization. Normalize DOI/identifiers for matching; flag uncertain title matches instead of merging them automatically.

For a systematic or scoping review, write eligibility and extraction rules before the main screening pass. Track records, reports and studies separately, including reports not retrieved and full-text exclusion reasons. Reconcile flow counts. Use independent eligibility assessment as required by the chosen protocol; disclose a single-reviewer process or model-assisted screening. Multiple model roles are not automatically equivalent to independent human reviewers.

## Turn records into an evidence map

Extract from the actual source, not only its search snippet. For each relevant report, retain:

| Evidence unit | Minimum useful content |
|---|---|
| Identity | Title, authors, date, persistent identifiers, version, venue and artifact type. |
| Research setting | Task/population/workload, inclusion criteria, scale, datasets, environment and evaluation unit. |
| Method and comparison | Mechanism, assumptions, strongest relevant baselines, interventions/ablations and resource conditions. |
| Results | Reported outcomes, units, uncertainty, subgroup/failure findings and location in the source. Mark values transcribed from the source. |
| Limitations | Threats to validity, unavailable details, conflicts of evidence and restrictions on generalization. |
| Reproduction | Code/data location, license, release/commit, dependencies and what was actually rerun. |
| Provenance | Source URL, access date, evidence locator and whether the full report was read. |

1. Deduplicate repeated records, then link related reports without erasing their identities. A preprint, later journal paper and follow-up analysis may describe one underlying study.
2. Separate author claims, observations reported in the paper, your interpretation and results you reproduced. Label a secondary summary as such.
3. Verify that a citation identifies the intended work and supports the nearby claim. DOI registration alone cannot verify claim support, correction status or scientific truth.
4. Organize synthesis by questions, mechanisms, assumptions and disagreements. Use paper-by-paper notes as evidence backing a comparative synthesis, not as the final analysis by default.
5. Connect question → method → evidence → limitation → candidate next experiment. Add venue links only after the research fit is understood.
6. Mark each gap as evidence-supported, tentative or not yet searched. An empty cell in your map can mean missing search coverage rather than a genuine research gap.

Use a table for exact comparisons. Use a compact Mermaid map when dependencies or competing explanations matter. Keep exact numerical plots deterministic and traceable to data. Never generate study counts or effect estimates in an image prompt.

## Audit novelty and choose a tractable question

1. Restate the idea without application-specific branding. Identify the underlying algorithmic or methodological paradigm.
2. Search four comparison layers: closest task competitors, adjacent-domain solutions, classic methods and simple baselines that could explain the gain.
3. Build a distinction table: what already exists, what changes, why that change could matter, evidence required and conditions where the distinction disappears.
4. Test alternative explanations: extra compute/data, a stronger model, prompt tuning, favorable task selection, leakage, extra tools or additional human intervention.
5. Define bounded claims and prohibited overclaims. "No papers found in these queries" is not "first ever". Novelty and usefulness require different evidence.
6. For a drafted claim, default to verification: preserve its wording while reporting unsupported scope or missing comparisons. Rewrite only when requested or necessary to correct an overclaim.
7. Choose a minimum informative experiment with an explicit success measure, failure interpretation, resource estimate and stop rule. A negative result can still answer the question; do not reframe it as a positive result.

Assess candidate directions using separate dimensions: scientific value, novelty risk, feasibility, data access, evaluation credibility and audience fit. Use an explicit heuristic only if it helps a decision, name its assumptions, and avoid presenting a composite score as objective scientific quality or acceptance probability.

## Plan and assess research

- Separate hypotheses, planned analyses, exploratory analyses and completed results. Freeze important evaluation choices before observing test outcomes; document later changes.
- Inspect available data/code before promising feasibility. Build a reproducible environment and a small valid pilot before launching an expensive run.
- Match the statistical unit to the data-generating process. Address dependence, leakage, confounding, missing data, multiple comparisons and uncertainty using appropriate methods.
- For clinical or intervention reviews, choose study-design-specific appraisal and reporting guidance. For qualitative work, assess sampling, interpretation and reflexivity as applicable. For CS, inspect tasks, comparators, budgets, implementation and evaluation validity.
- Judge evidence eligibility using the question, design and protocol rather than journal quartile. If the user explicitly restricts a source set by quartile, record the restriction and resulting selection bias instead of presenting it as a scientific-quality guarantee.
- Plan quantitative synthesis only when outcomes, populations and designs support it. The skill does not supply a universal meta-analysis engine or automatically justify pooling.
- Carry out code, data and experiment work with the host's actual tools and the user's authorized resources. Report separately what was planned, implemented, executed and independently checked.
- Consult `agent-research.md` for Agent capability and program experiments; consult `publication.md` once journal positioning or manuscript preparation becomes relevant.

For a research proposal, turn the evidence map into the question, rationale, bounded contribution, work packages, methods, milestones, resources, alternatives and evaluation/stop criteria. Distinguish expected outcomes from measured findings. Check an actual funder/institution call when one is named; do not invent eligibility, budget rules or endorsements.

For a requested seminar, poster or editable slide deck, derive the narrative from the same claim/evidence map. Use the host's actual document/presentation tools, retain editable source where requested and inspect rendered output. Export capability depends on those tools; the research workflow itself is not a PPT/PDF rendering engine.

## Maintain and deliver the exploration

Produce the subset requested by the user, using one project state: scope, search log, verified bibliography, evidence matrix, field map, gap/claim audit, prioritized directions and next experiment. Include source links near substantive facts and state the last search date.

When updating, retain earlier evidence and decisions, annotate superseded facts, link versions and add a dated delta. Explain which conclusions changed and why. Do not silently rebuild a different project or erase unsuccessful searches.

At delivery, check:

- Are the coverage boundary and incomplete sources explicit?
- Can important claims be traced to evidence rather than just plausible citations?
- Are records, reports and underlying studies distinguished where relevant?
- Are contradictory findings and dangerous baselines represented?
- Does each recommended next step resolve a concrete uncertainty within available resources?
- Are unexecuted experiments and inaccessible materials clearly labeled?

## Worked prompts and consulted workflows

- `用 $scholar-route 探索低成本 Agent 长期记忆：先画问题和证据地图，再提出两条可在单卡上验证的方向。`
- `用 $scholar-route 更新这份食品营养综述，保留原筛选记录，列出新增研究和结论变化。`
- `用 $scholar-route 审核这个多 Agent 创新点，给出最危险的经典基线和最小验证实验。`

This reference is an original synthesis. Consulted workflow sources include [K-Dense literature-review](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/literature-review), [paper-lookup](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/paper-lookup), [polish_skill novelty and literature workflows](https://github.com/yujie-jason-zhang/polish_skill), [Superpapers](https://github.com/regisely/superpapers), and [Researcher](https://github.com/sokolmarek/researcher). Current scientific findings must come from the actual literature retrieved for the user's task, not these workflow repositories.
