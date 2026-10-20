# Sources and tool capabilities

## Contents

- Native executable adapters
- Scholarly source coverage
- Journal discovery and authority
- Optional host capabilities
- Evidence, privacy and failure handling

## Native executable adapters

`scripts/scholarly_sources.py` and `scholar_route.py search` implement exactly four providers: OpenAlex, Crossref, DBLP and arXiv. Read [sources-api.md](sources-api.md) for the verified API documentation, response contract and query differences. Basic metadata queries need no configured key in the bundled path; an optional `OPENALEX_API_KEY` comes from the environment. Check the service's current contract if access behavior changes.

Each call requests a bounded first page, at most 100 records and 2 MiB, with a configurable timeout. It reports the literal query, retrieval date, source URL, warnings and incomplete coverage. It has no automatic cursor-pagination or universal full-text reader. A provider failure returns an error and no invented records; CLI exit code 3 signals that failure.

`search --project PATH` imports the search record and metadata transactionally into an existing project. It preserves publication/preprint versions and starts imported papers at `read_status: metadata`. Mark actual abstract/full-text reading after doing it. `import-search` accepts a previously saved native search envelope. A failed search can be logged; it cannot become evidence of zero relevant research.

## Scholarly source coverage

The following source routes preserve the capability coverage of the original paper-lookup workflow. Only the four adapters above are bundled execution. Other rows require an available host connector/API/browser or a supplied export.

| Source | Role | Runtime |
|---|---|---|
| [PubMed](https://pubmed.ncbi.nlm.nih.gov/) | Biomedical citations and study discovery | Host |
| [PMC](https://pmc.ncbi.nlm.nih.gov/) | Available biomedical full text | Host |
| [Europe PMC](https://europepmc.org/) | Life-science citations, full text and links | Host |
| [bioRxiv](https://www.biorxiv.org/) | Biology preprints and versions | Host |
| [medRxiv](https://www.medrxiv.org/) | Health preprints; preserve non-peer-reviewed status | Host |
| [arXiv](https://arxiv.org/) | CS/physics/mathematics and other preprints | Bundled metadata search |
| [OpenAlex](https://openalex.org/) | Cross-disciplinary works, sources and citation links | Bundled works search; other endpoints host |
| [Crossref](https://www.crossref.org/) | Registered DOI metadata and bibliographic checks | Bundled works search; direct DOI verification host |
| [Semantic Scholar](https://www.semanticscholar.org/) | Paper discovery and citation neighborhoods | Host |
| [CORE](https://core.ac.uk/) | Repository and open-access discovery | Host |
| [Unpaywall](https://unpaywall.org/) | Available lawful open-access locations | Host |
| [OpenCitations](https://opencitations.net/) | Citation relationships | Host |
| [PubTator 3](https://www.ncbi.nlm.nih.gov/research/pubtator3/) | Biomedical entity enrichment | Host |
| [Zenodo](https://zenodo.org/) | Datasets, software and archival releases | Host |
| [Figshare](https://figshare.com/) | Research outputs and data | Host |
| [ROR](https://ror.org/) | Research-organization identity | Host |
| [BioStudies](https://www.ebi.ac.uk/biostudies/) | Biological study data and links | Host |
| [DOAJ](https://doaj.org/) | Open-access journal information | Host |
| [DBLP](https://dblp.org/) | Computer-science publications and exact venue identity | Bundled metadata search |
| [Hugging Face Papers](https://huggingface.co/papers) | ML paper pages and linked models/data | Available host skill/connector |
| Google Scholar / field bibliographies | Complementary recall and citation tracing | Host access or user export; no scraper bundled |

OpenAlex source statistics, DOAJ status, database search hits and DOI existence answer different questions. None establishes a manuscript's acceptance probability. Bibliographic discovery does not establish full-text access, scientific validity or SCIE coverage.

## Journal discovery and authority

| Route | Appropriate use | Boundary |
|---|---|---|
| [Elsevier JournalFinder](https://journalfinder.elsevier.com/) | Publisher-specific content matches | Publisher coverage; check current language/input requirements; no automatic manuscript upload. |
| [Springer Nature journal finder](https://link.springer.com/journals) | Publisher scope discovery | Verify actual scope and journal instructions. |
| [Wiley Journal Finder](https://www.wiley.com/journal-finder/) | Publisher candidates and comparison | Preserve metric definitions and dates. |
| [IEEE Publishing Portal](https://publishingportal.ieee.org/) | IEEE venue discovery and publication tools | Separate journals and conferences. |
| [B!SON](https://service.tib.eu/bison/) | Open-access journal similarity leads | OA-focused coverage; verify any decisive fact. |
| [Clarivate Master Journal List](https://mjl.clarivate.com/home) | Exact Web of Science collection membership | Record SCIE/SSCI/AHCI/ESCI explicitly. |
| JCR / CAS / SJR / Scopus | The named metric or index in its proper edition and category | Licensed exports may be needed; do not redistribute proprietary tables. |
| [JANE](https://jane.biosemantics.org/) | Biomedical journal/author/paper leads | Biomedical scope, not a general CS recommender. |
| LetPub / SciRev / Muchong | Supporting discovery and dated author experience | No authoritative personal acceptance forecast or guaranteed timeline. |
| NPPA / CSSCI / CSCD / TR Dizin | Regional publication identity or specific catalog coverage | Use each responsible authority for its actual fact. |
| Local CSV/JSON/Excel or optional embeddings | Additional recall, custom catalogs and query expansion | Record provenance and coverage; do not silently fill absent columns. No vector-search engine is bundled. |

For explicit single-journal tasks, skip broad candidate generation and build the dossier from the actual official identity. For broad discovery, use complementary publishers/societies and specialist recall; do not let one publisher's matcher define the entire pool.

## Optional host capabilities

Use these only when the host actually exposes them and the task benefits:

- Paper reading, search and evidence synthesis skills for additional sources or full text.
- Hugging Face papers/datasets/evaluations/training/jobs/Trackio/Gradio skills for actual ML data, evaluation, training, logging and demos. An Agent project does not automatically require model fine-tuning or a paid job.
- Code execution, package environments, plotting and reproducible experiment tools. Inspect the user's code/data and budget before a run.
- Document, PDF, spreadsheet, LaTeX and presentation tools for manuscript edits, reports and editable figures/decks. Inspect rendered outputs; Markdown alone is not a verified PDF/DOCX.
- Optional specialized upstream skills from the provenance inventory, loaded individually after reading their current instructions and license. Do not recursively install every package or assume provider-specific commands exist.
- Browser interaction for an authorized publisher portal if an appropriate connector does not cover the requested operation. Never bypass access restrictions.
- Git/project persistence for code and skill updates when authorized. Researcher drafts, credentials and unpublished papers must not be included in a public skill release by default.

The orchestration reference can direct these tasks, but it is not itself a training engine, meta-analysis implementation, figure editor, PDF parser, external-model reviewer service or submission robot.

## Evidence, privacy and failure handling

Before asserting a changing journal fact, inspect the competent current source, record the supported statement/location, and link it to its field. A project source's `verified: true` records the host's review; Python cannot prove that the linked page says what the record claims. For ranking and SCI requirements, a bibliography API is insufficient.

Use a metadata/abstract query sufficient for discovery. Upload full unpublished manuscripts to matching/LLM services only within the user's explicit or clearly applicable prior authorization. Credentials belong in the host environment, never in repository content, project evidence, URL query parameters or logs. Respect service terms, authentication and rate limits.

Distinguish successful retrieval, bounded partial retrieval, access failure, no results, unavailable full text and unreviewed content. On a blocked service, continue complementary searches or work from supplied evidence and log the gap. Do not claim real-time connectivity because parser tests passed.

At this release's test run, the sandbox blocked socket creation. Four native adapters passed deterministic parser/error tests; direct live probes failed. See the repository validation report for exact execution evidence. Refresh that validation statement when a later release actually runs live checks.
