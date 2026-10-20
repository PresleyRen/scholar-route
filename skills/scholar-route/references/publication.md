# Journal strategy and the publication lifecycle

## Contents

- Select the requested stage
- Build a manuscript and journal profile
- Discover and verify candidate journals
- Compare fit and create a submission order
- Investigate a named journal
- Complete the eighteen publication operations
- Preserve claims, declarations and manuscript structure
- Final checks, examples and sources

## Select the requested stage

Run the operations required by the user's task. A request for journal fees does not require rewriting a manuscript, and a proof check does not reopen the whole research plan. For full domain exploration, connect this workflow to `exploration.md` and, where relevant, `agent-research.md`.

Use three entry routes:

- **Discovery:** turn a topic, abstract or manuscript into a verified candidate pool and practical submission order.
- **Known journal:** investigate identity, scope, policies, fees and requirements; assess manuscript fit only when enough manuscript evidence is supplied.
- **Publication stage:** prepare or inspect the requested manuscript, submission, revision, proof or post-publication materials.

Use a quick pass for a narrow question and a fuller audit for consequential selection or submission decisions. State the pass depth and missing inputs. Reuse supplied preferences, target lists and prior verified facts, refreshing time-sensitive facts before relying on them.

## Build a manuscript and journal profile

Extract the research object, question, contribution, method's role, evidence available, article type, readers, language and excluded domains. Distinguish a new method from an engineering application, benchmark, replication, review or perspective.

Capture hard constraints separately from preferences: required index, ranking system/year/category, article type, language, fee ceiling/currency, timeline, publication model and institutional rules. A remembered quartile or the manuscript's LaTeX class does not establish an intended journal.

Use evidence fields with source and date. For journal identity, retain title, publisher/society, ISSN/eISSN or other reliable identifier, official site, submission entry and publication type. Track title changes and uncertain same-name matches explicitly.

| Fact family | Required distinctions |
|---|---|
| Indexing | SCIE, SSCI, AHCI, ESCI and other indexes; current inclusion versus historical coverage; source of verification. |
| Rankings and metrics | JCR quartile/JIF, SJR quartile, CiteScore, CAS edition and category are distinct fields, each with year and source. |
| Fees | Mandatory versus optional APC; subscription route; submission/page/color/other charges; currency, tax, conditions, waivers and source date. |
| Timing | Desk/first decision, externally reviewed decision, acceptance and online publication intervals; definition, period and source. |
| Acceptance | If an official aggregate is available, record its definition, population and period; never turn it into this manuscript's probability. |
| Eligibility | Article type, language, scope and any verified author or submission restrictions. |
| Evidence | Policy fact, comparable published paper, author experience, external dataset entry or model judgment; do not merge these categories. |

## Discover and verify candidate journals

1. Search several complementary routes: journals publishing verified similar papers, subject catalogs, publisher journal finders, established specialist venues and domain-specific indexes. Explain coverage rather than claiming every publisher was searched.
2. Include specialist journals that a large general index or title-keyword match might miss. A local journal index is an optional discovery aid; record its version, coverage and license.
   Optional embedding/vector retrieval can broaden candidate recall across wording or languages when an actual implementation is available. Treat its similarity score as discovery evidence, not identity verification, journal quality or acceptance likelihood.
3. Use similar-paper counts as exploratory evidence. Where useful, contextualize them by journal volume, date window and article type so very large journals do not dominate by size alone. Neither raw nor normalized counts establish acceptance ease.
4. For CS, use DBLP/OpenAlex/Semantic Scholar and original publisher records as appropriate. For biomedical work, add PubMed and the relevant clinical/life-science sources. Choose a justified recent window, extending it for slow-moving subjects; do not force a three-month PubMed rule onto every field.
5. For Chinese journals, combine catalog discovery and reverse discovery from relevant articles, then verify identity and current submission instructions. NPPA identity, core-journal lists and commercial aggregator rankings answer different questions.
6. For open-access discovery, use sources such as DOAJ or B!SON within their actual coverage. Verify current publisher fees independently. Absence from an OA directory does not establish misconduct, especially for subscription or hybrid journals.
7. Verify decisive fields using their competent primary sources: publisher for author policies/fees; index provider for index status; official ranking source for that ranking. A page calling itself official or showing a logo is insufficient identity evidence.
8. Label source access as succeeded, partial, attempted-but-failed or skipped, with the reason. A query being attempted does not mean its content was retrieved or verified.

Publisher-specific recommenders can contribute candidates. Their publisher coverage is a limitation, so avoid silently converting one recommender's list into a universal ranking. Prefer available lawful interfaces; do not bypass access controls or require a commercial platform without a user-selected reason.

## Compare fit and create a submission order

Apply hard constraints with three outcomes:

- **Eligible:** the necessary facts have supporting evidence and meet the constraint.
- **Excluded:** verified evidence contradicts at least one hard constraint; retain the reason and source.
- **Unverified:** a decisive fact is missing, stale, ambiguous or conflicting. Keep the candidate visible in a verification queue, outside the confirmed eligible shortlist.

Do not silently drop all journals because a local dataset lacks a requested field. Report the incomplete dataset and continue the appropriate verification. Do not treat missing fees as zero or unknown indexing as a failed/fulfilled requirement.

Evaluate eligible candidates using distinct lenses: topical fit, contribution/article-type fit, audience, evidence precedent, practical constraints and confidence in the supporting facts. If a scoring heuristic is used, expose weights, handling of unknowns and sensitivity to different priorities. Do not display the score as an acceptance probability or an objective manuscript-quality rating.

Create a flexible submission order instead of forcing a fixed 2+2+1 or four-tier list. Use primary/backup/conditional/excluded labels as appropriate. A "challenge" label is a strategy label only, with a reason tied to scope or demands; it cannot encode a predicted rejection rate. Never call a backup a guaranteed acceptance.

For "相对好投", interpret the goal as reducing avoidable mismatch while meeting the user's constraints. Explain the observable evidence: same contribution type recently published, suitable scope, realistic evidence requirements, manageable costs and preparation burden. A lower quartile, faster desk decision, high publication volume or broad scope alone does not prove easier acceptance.

Return a comparison table with the journal's verified identity, type, scope fit, recent comparable articles, relevant index/rank facts, mandatory cost, timing definition, unresolved fields, source date and recommended next action. Offer publisher variety when candidates are comparably suitable; do not discard the best fit just to enforce a cosmetic diversity quota.

## Investigate a named journal

1. Confirm identity and official submission route. Resolve materially ambiguous titles before asserting target-specific facts; continue other independent checks where possible.
2. Read current aims/scope, article types, author instructions, peer-review policy, fees, ethical/data/code/AI policies and submission-system requirements.
3. Record article-type-specific limits: main text and abstract, structured headings, keywords, figures/tables, references, supplements and required forms. Separate initial submission, revision and accepted-production rules.
4. Distinguish format-free submission from obligations that still apply, such as anonymization, declarations and file completeness. Do not impose camera-ready formatting on a format-free initial submission.
5. Inspect two or three accessible recent examples of the same article type when useful. Use them to understand audience and presentation conventions; do not treat observed examples as mandatory official rules.
6. Separate published aggregate timing from dated, self-selected author experiences on SciRev, LetPub, Muchong or forums. Summarize contradictory experiences without fabricating an average or assuming they represent all submissions.
7. Produce a journal dossier: identity, fit, policies, fees, timings, article-type checklist, comparable articles, experience signals, sources and open questions.

Screen concrete identity and policy concerns: conflicting publisher/ISSN, impersonated domain, unverifiable editorial claims, misleading fees or disputed index claims. Investigate and report the evidence. Avoid blanket misconduct labels based only on low fees, rapid publication, high volume, geography or a missing directory entry.

## Complete the eighteen publication operations

These operations are integrated instructions for the host agent. They do not imply that a script performs editorial judgment, image forensics, statistical modeling or remote submission automatically.

| Operation | Carry it out | Deliverable and boundary |
|---|---|---|
| 1. Journal selection | Apply the profile, discovery, identity, constraint and fit workflow above. | Verified shortlist/submission order, plus excluded and unverified candidates. |
| 2. Presubmission inquiry | Check whether an inquiry is appropriate for the article type; identify the editor/contact from the journal's current site; draft a concise fit argument. | Reviewable inquiry draft; missing author facts stay marked. Send only with explicit authorization already in the session or newly obtained. |
| 3. Journal reformatting | Apply current stage-specific rules to headings, file structure, references and layout while preserving scientific wording unless editing was also requested. | Reformatted files and a rule/change checklist; obtain official templates lawfully rather than bundling proprietary forms. |
| 4. Manuscript copyediting | Improve grammar, clarity, terminology and typography at the requested edit depth; preserve results, claim strength and technical meaning. | Edited text with material changes explained; a verification-only request produces findings rather than a competing rewrite. |
| 5. Citation audit | Verify identity, metadata, duplicates, accessible corrections/retractions and actual support; look for omitted counterevidence or misleading citation use. | Traceable citation/claim audit and corrected bibliography; unverified references stay unresolved. |
| 6. Reviewer suggestions | Derive expertise from relevant papers and verify current professional identity; check applicable conflicts such as recent collaboration, shared institution or other journal-defined exclusions. | Evidence-backed candidates and unresolved conflicts; never invent contact details or imply consent. |
| 7. Authorship and contribution | Collect actual contributions and the applicable discipline/journal criteria; map to CRediT where requested; surface unresolved author-order or approval decisions. | Contribution statement and decision questions; people and the relevant policy determine authorship, not an automatic universal formula. |
| 8. Cover letter | Link the bounded contribution to scope and include only verified required declarations and author-approved reviewer preferences. | Initial-submission cover-letter draft; never assert all-author approval, originality or absence of conflicts without supporting input. |
| 9. Submission screening | Check internal consistency, complete files, results versus claims, applicable ethics/consent, declarations, data/code availability and required deposition. | Issue list with evidence, severity and concrete repair; missing input is not a finding of misconduct. |
| 10. Statistical rigor | Assess design, analysis unit, assumptions, confounding, leakage, dependence, missing data and multiple testing; use domain-appropriate methods. | Analysis plan or audit; calculations run only with actual data/tools, and recommendations are not fabricated analyses. |
| 11. Figure checks | Compare plotted values with source data when supplied; inspect dimensions, resolution, labels, legends, colors, panel identity and journal rules. | Figure issue list and reproducible changes; visual inspection or duplicate-file checks do not prove image authenticity. |
| 12. Table checks | Check source values, units, denominators, precision, abbreviations, footnotes, cross-references and main/supplement placement. | Table corrections and unresolved source-data questions. |
| 13. Simulated review | Use clearly labeled editor and complementary reviewer perspectives to challenge scope, methods, evidence and presentation; synthesize agreements and unresolved disagreements. | Internal simulation with actionable priorities; no claim to predict real reviewers, review decisions or acceptance. |
| 14. Submission checklist | Select current publisher/venue and study-design reporting requirements, verifying applicability before use. | Requirement-by-requirement status with manuscript location and unresolved items; do not mark requirements satisfied without evidence. |
| 15. Revision response or appeal | Parse each editor/reviewer request, link the response to evidence and an actual manuscript change, or explain a respectful disagreement. | Point-by-point response, change map and revised files; appeal drafts use the real decision and defensible grounds. |
| 16. Proof check | Compare the typeset proof with the accepted version; prioritize changed numbers, equations, figures, author details, references and unanswered production queries. | Localized correction list; avoid introducing new research claims or unapproved changes at proof stage. |
| 17. Dissemination | Adapt the published findings to a plain-language summary, visual concept or requested channel while preserving magnitude, uncertainty and limitations. | Channel-appropriate drafts; actual posting requires authorization. |
| 18. Post-publication correction | Document the discovered error, affected claims/data, evidence and likely remedy under the journal's current correction policy; distinguish author and production errors where established. | Correction dossier and draft communication; the editor/publisher determines the formal notice category. Never autonomously declare or issue a retraction. |

## Preserve claims, declarations and manuscript structure

Keep one verified fact record for each declaration shared across documents. Drafting, presence checking, substantive auditing and proof comparison are different operations on that same fact; they must not invent mutually inconsistent statements.

For writing work, build a claim–evidence–section map. Explain the problem, gap, mechanism, result and limitation in a connected argument. Do not improve perceived novelty by strengthening an unsupported claim. For Agent/system papers, preserve the distinction between architecture, implementation and observed performance.

Preserve LaTeX commands, labels, citations, math, numerical values and cross-references when editing prose. Use the actual file-format toolchain when available. Compile/render after meaningful format changes, inspect the output and report compilation/rendering limits. A Markdown draft is not a verified DOCX/PDF export.

Apply PRISMA, CONSORT, STROBE, ARRIVE or other reporting guidance only when the study design and current journal policy warrant it. Check current official guidance; do not extrapolate a biomedical evidence cap or authorship rule to unrelated CS, engineering or humanities papers.

When an upstream optional skill is installed and helpful, invoke only the relevant operation, preserve this workflow's evidence and authorization rules, and map the result into the same project state. Do not load every upstream workflow or let a helper replace the user's selected language, constraints or scope.

## Final checks, examples and sources

Before delivery, verify identities and links, reconcile critical facts across output files, check current sources for decisive policies, distinguish official facts from anecdotes, and expose unknowns. Check that publication-stage claims match the work actually performed.

Submit manuscripts, send correspondence, recommend people to an external system or publish dissemination materials only when explicitly authorized. Existing authorization remains valid; do not ask the user to reconfirm routine reversible edits or an action already requested.

- `用 $scholar-route 根据这份 Agent 系统论文选 SCI 期刊：无强制 APC，区分已确认、待核实和排除项。`
- `用 $scholar-route 完整调查这本期刊的 Original Research 投稿要求，附费用来源和逐项清单。`
- `用 $scholar-route 审查我的返修信，逐条对应审稿意见和实际修改，不代发邮件。`

Original integration informed by [Academic Publishing Agent Skills](https://github.com/yaotingsun/academic-publishing-skills), [Journal Research Agent Plugins](https://github.com/kkunkunya/journal-research-agent-plugins), [xiaoyu-skill sci-select](https://github.com/keros68/xiaoyu-skill/tree/main/skills/sci-select), [paper-know-journal](https://github.com/huangwb8/ChineseResearchLaTeX/tree/main/skills/paper-know-journal), [journal-fit-finder](https://github.com/hztopcu/journal-fit-finder), [polish_skill](https://github.com/yujie-jason-zhang/polish_skill), [Superpapers](https://github.com/regisely/superpapers), [Researcher](https://github.com/sokolmarek/researcher), and [Journal Atlas](https://github.com/Zaious/journal-atlas). Verify actual journal facts against the competent current source, not a skill's example table.
