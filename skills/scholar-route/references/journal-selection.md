# Journal discovery, dossier and evidence-based submission order

## Start from the manuscript

For a short request such as “给这篇稿选刊”, open the project's abstract, contribution statement and main results table. Reuse its saved budget, index, publication deadlines, language and region preferences. Give the current request precedence. If only a topic is available, make a provisional shortlist and identify the missing comparison or result that could change the ranking. Use the journal stage for this task.

Describe the measured contribution in one sentence: inputs, intervention, output, evaluation unit, primary metric and intended readers. Use the research question and main table to confirm the primary track, adding secondary tracks only where the manuscript supplies independent evidence. For AI manuscripts, run the router and then check its suggestions against the following distinctions.

| Evidence in the main experiment | Where to look for comparable work |
|---|---|
| Utterance → intent, multiple labels, slots or abstention. Intent F1, recall or false acceptance. | NLP, dialogue and classification. Look for the same label regime and test conditions. |
| Request → selected tool, arguments or next action. Tool-selection accuracy or invalid-call rate. | Agent tool use and routing. Service or component selection alone measures one step. |
| Task → sequence of actions → checked final state. Task success, recovery, cost or latency across trajectories. | End-to-end Agent capabilities or systems. Separate work on orchestration overhead from work on the model's decisions. |
| Natural language → SQL or database answer. Execution accuracy or result equivalence. | Database interfaces and semantic parsing (Text-to-SQL). A database that only stores Agent logs supplies infrastructure. |
| Workload → learned estimate, index or execution plan. Cardinality error, plan quality, throughput or query latency. | AI for database systems (AI4DB). For a broad “DBAI” request, investigate both this track and database interfaces until the manuscript resolves the distinction. |
| Class/relation or constraint model evaluated for coverage, validity or reuse; or document retrieval/answers evaluated for evidence and correctness. | Ontology resources or knowledge engineering for the former; retrieval/RAG for the latter. Combine when the paper measures the modeling contribution as well as downstream retrieval. |
| AI applied to an industry or scientific task. Results are validated against domain outcomes, stakeholders or field-specific baselines. | Domain or applied journals read by the people who would use that result. Keep general AI venues in view if the paper also validates a transferable method. |

## Discover and verify candidates

1. Search for the closest journal papers in the manuscript's primary and secondary tracks, using task, baseline and metric in the query. Add specialist venues and regional journals. For a fee-sensitive English SCI search, prioritize verified zero or low mandatory fees. Include journals sponsored in China, Türkiye, Malaysia, Jordan, Serbia or other regions relevant to the request, alongside affordable international specialist venues. Geography guides discovery. The manuscript and journal's evidence determine fit. Apply hard index or budget exclusions only when requested or saved in the project.
2. For the default fee-sensitive search, look for original Chinese author/blogger reports and identifiable editors’ public statements as leads, alongside database and journal searches. For example, search an exact journal title with “投稿经验 / 版面费 / 审稿周期”, then search the journal site for signed editorials, article-type criteria or calls. Use any screenshots or links already provided in the research project. Respect a narrower or offline-only request. For a claim such as “水刊”, “好发” or “沾边就收”, recover the original post or screenshot if available. Record platform, author, date, URL or supplied image location, exact journal title/ISSN and what was claimed. Search distinctive wording for an original when a post is a repost. Keep an unidentified title as an unresolved lead. Match the ISSN and official journal URL before assigning fees, ranks, turnaround or the statement to a journal.
3. Look for what the speaker can establish. A reviewer describes individual practice. A named editor's editorial can describe a particular article type. A guest editor's call covers its special issue and dates. Check the current official author instructions or editorial policy for journal-wide criteria. When someone says incremental research is welcome, identify the exact contribution the policy accepts (such as a replication or a reusable resource) and the validation, license or documentation that article type requires. Give the post and the primary source separately; preserve any discrepancy.
4. Open actual publications in the same journal. Record DOI or stable URL, year, article type, regular issue or special collection, and the specific shared task, method and evaluation. Include the most important difference. Read at least the abstract for a fit judgment and use the full paper when conclusions depend on experimental details. Record the search scope and unresolved fit if no comparable paper can be identified.
5. Apply the dossier checks below, classify each candidate, and recommend a submission order. A new deadline, policy, scope or charge can change the order; refresh decisive facts before submission. For an explicitly named journal, go directly to its dossier.

## Minimum dossier

| Dimension | Record |
|---|---|
| Identity and status | Exact title, ISSNs, sponsoring institution/editorial location, publisher, official submission URL, title changes and whether the relevant track is accepting submissions. Flag obsolete suspension notices and expired calls when current status is uncertain. |
| Scope and precedent | Target readers, article types, exclusions, primary source and comparable studies. For editorial statements record the speaker, role, date and scope of the statement. |
| Indexing and rank | Match ISSN to the current responsible index, e.g. Clarivate MJL for SCIE versus ESCI. For JCR give the JIF data year, release/edition, and JIF quartile for each relevant category. Label a dated institutional reproduction or an inaccessible current record explicitly. Keep CAS editions and SJR separate. |
| Costs to this author | Specify the article type and chosen route, payer (individual or institution), currency and effective date. Calculate the mandatory total for that case, including submission, APC, compulsory pages, length charges and applicable taxes. List elective OA/print color separately. Treat affiliation agreements or waivers as conditional until eligibility is verified. Zero APC alone establishes only the APC amount. |
| Time to a usable result | Separate submission → first decision, external-review decision, acceptance, first online and issue publication. State whether each figure is a journal statistic, an editor's scheduled milestone, a community report, or an observed article date. Record statistic type, period, population and endpoint where available. |
| Requirements and integrity | Current author instructions for the submission stage, scope, peer review, terms, article materials, data/code, declarations, publisher ownership and corrections. Retain contrary evidence and unresolved requirements. |

For a relevant timeline, inspect comparable published articles with visible histories. List DOI, manuscript type, original dates and calculated calendar days for each supported interval. Report how many papers had usable dates and that these are accepted papers. Preserve month-only issue dates, combined “accepted/published online” fields, and disagreements between PDF and platform records. Omit individual intervals whose endpoints cannot be established. When the journal gives only first decision or a final-manuscript deadline, mark the actual time to publication unknown. Retain these case histories in source-linked dossier notes, distinct from official statistics.

Keep the user's source posts, author-specific payment assumptions and unpublished work in the project. Keep the distributed skill reusable. Do not redistribute licensed metrics tables or proprietary templates.

## Interpret “relatively attainable”

Base the recommendation on the actual contribution, the journal's editorial threshold for that article type, comparable papers, practical costs and current submission status. State which limitation of the manuscript could lead to desk rejection. Report an official acceptance statistic only with its definition, time period and source. A person's chance of acceptance is unknown. Offer a stretch, primary or backup route where the evidence supports one; fixed quotas and a low quartile alone do not justify a candidate.

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

Lead with the primary track, the evidence in the manuscript and the best supported route. For a Chinese request, present a compact table with 方向与同刊先例、候选及状态、收录与逐学科分区、个人必付费用、投稿到录用/上线时间、依据与待核项. Name the best fit, the lowest confirmed out-of-pocket route and the time to budget for the author's actual deadline where available. Explain conflicts or missing facts that would change the order. Retain the full candidate pool, dates and sources in the project for later verification. Record each consequential recommendation as a project decision with its journal and source IDs, including why the runner-up ranks lower. Put the original timeline dates, article histories and scoped editorial quotations in source-linked dossier notes. The generated REPORT.md can be rebuilt from records; keep research notes and author decisions in the project rather than editing an export.

Use the live source routes in `sources-and-tools.md` and the relevant publication stages in `publication.md`. All source-specific tradeoffs and rejected shortcuts are recorded in `conflicts.md`.
