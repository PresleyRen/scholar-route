# Research brief — fictional planning case

Topic: Long-term memory and failure recovery in an LLM Agent that answers
questions about public biomedical research articles.

Current artifact: a small Python controller with retrieval, a summary memory
store, two tools and a retry loop. No benchmark has been run. No patient data
is used. There is no clinical deployment or claim of patient benefit.

Working observation: after a long conversation, a summary may lose version
information. A tool timeout sometimes causes the same action to run twice.
These are developer observations without counts, traces or a controlled study.

Candidate idea: attach provenance and version-aware invalidation to memory,
then choose recovery actions from typed errors. It might reduce stale answers
and duplicate work, but we do not know whether existing methods already solve
the problem or whether a simple rule-based cache is sufficient.

Resources: one laptop, Python experience, public articles or synthetic workloads,
and a hard limit of 200 external model calls for a later pilot. No paid service
purchase, deployment, clinical study or external communication is authorized.

Desired outputs: an English/Chinese query strategy, a domain/evidence map,
competing explanations, two tractable research questions, a minimum experiment
plan and a route to later journal selection. All results are still unmeasured.
Keep hypotheses distinct from established literature claims.
