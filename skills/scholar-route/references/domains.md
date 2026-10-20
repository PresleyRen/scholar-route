# Domain routing

## Select the research object

Use the explicit domain IDs below with the CLI. Automatic keywords suggest profiles; the host must determine the actual research object, method and intended contribution. A bare "agent" is deliberately insufficient: a chemical agent, economic agent and LLM Agent need different workflows. Select several profiles when justified, designate the primary audience, and combine the relevant methods rather than running every specialist checklist.

| ID | Main coverage | Evidence emphasis |
|---|---|---|
| `agent-ai` | LLM Agent intent, routing, planning, retrieval, memory, tool use, verification, collaboration and recovery | Controlled budgets, task distribution, strongest simple baselines, contamination and evaluator validity. Adds the CS profile. |
| `computer-science` | NLP, ML, software, retrieval, knowledge graphs and systems | Algorithms and software artifacts, reproducible configurations, benchmark versions and end-to-end evidence. |
| `engineering` | Control, robotics, manufacturing, energy and applied AI | Realistic domain outcomes, simulation-to-deployment limits, classical engineering baselines, applicable standards. |
| `biomedicine` | Biomedical, clinical and public-health work | Study-design-specific validity, population, intervention/exposure, registry and reporting requirements when applicable. |
| `social-sciences` | Psychology, education, economics, HCI and behavioral work | Sampling, constructs, identification/confounding, instruments, qualitative interpretation and human interaction. |
| `food-agriculture` | Food science, nutrition, agriculture and crop research | Distinguish chemistry, nutrition interventions, animal studies and engineering; choose each method's evidence standards. |
| `humanities` | History, philosophy, linguistics and related work | Primary texts, interpretations, context, provenance, counterarguments and disciplinary methods. |
| `general` | Unrecognized or emerging fields | Establish an explicit vocabulary, primary sources, methods and evaluation unit; do not substitute a CS rubric automatically. |

## Cross-domain cases

- Clinical LLM decision-support Agent: Agent + CS + biomedicine. Software benchmark results do not establish clinical efficacy.
- Agent in teaching: Agent + CS + social sciences. Distinguish task accuracy from learning outcomes; use an appropriate study if claiming student benefit.
- Multi-agent economic simulation: social sciences; add CS only for an actual software/method contribution. Do not assume language-model tool calling.
- Agentic industrial inspection: Agent + engineering + CS. Separate model behavior from factory outcomes and domain constraints.
- Ontology-guided knowledge-graph construction: usually CS; add the knowledge domain when making claims about its data or outcomes. Compare schema/constraint checking, rule-based and non-Agent alternatives where relevant.

## Region, language and publication type

Use `--region international`, `china` or `turkey`. Region is a journal/index overlay, not the author's nationality. English discussion does not require an English-only search, and a Chinese request does not imply only Chinese journals.

For China, distinguish NPPA publication identity from index inclusion. Verify current CSSCI, CSCD and other requested catalog editions with the responsible source; a CN number or hosting platform is not proof of core-index status. CNKI/Wanfang/VIP are useful discovery routes; respect access limits. LetPub/Muchong reports are supporting or anecdotal sources, not official acceptance statistics. Easyscholar can enrich rankings only with its returned system/year/source and independent checks where decisive.

For Turkey, distinguish TR Dizin coverage, DergiPark hosting and journal scope. Verify language and current journal rules. Do not interpret a hosting platform as an index.

Keep relevant conference evidence in a CS literature map. Exclude conferences only from a journal-only target pool. A venue-specific package called Computer-Science-Journal-Skills may describe the single journal 《计算机科学》; read exact identity before using it.

## Full exploration and stopping

The full route exposes every applicable module. It does not mean that an early idea can immediately complete a paper, clinical study and publication. Deliver the completed evidence map, candidate questions, minimum informative experiment, preliminary audience fit and remaining dependencies. Resume later from recorded evidence.

For an update, keep the original coverage contract, state what changed, and expand subfields deliberately. A sparse map is an invitation to search, not proof of a research gap. Finish when the agreed scope and feasible outputs are covered, or when the next result requires unavailable evidence/resources; report that boundary precisely.
