# Agent capability and program research

## Contents

- Classify the contribution
- Explore the capability space
- Investigate the program and runtime
- Define a convincing evaluation
- Reproduce, implement and test
- Connect evidence to a paper and venue
- Failure conditions, worked prompts and sources

## Classify the contribution

Extract the task, controller/model, environment, tools, data, evaluation budget and proposed contribution. Use one or more of these routes:

| Route | Research question | Evidence emphasis |
|---|---|---|
| Capability/method | Does a mechanism improve planning, memory, tool use or another capability under specified conditions? | Strong comparators, controlled budgets, ablations, task generalization and failure analysis. |
| System/program | Does an architecture improve reliable or efficient execution? | Implemented artifact, design alternatives, end-to-end workloads, component measurements and recovery behavior. |
| Benchmark/evaluation | Does a task suite or metric measure the intended capability? | Construct validity, coverage, contamination controls, evaluator calibration and reproducible scoring. |
| Application | Does using an Agent improve a meaningful domain outcome? | Domain baseline, operational constraints, deployment or realistic simulation evidence and domain-specific validation. |
| Human interaction | How does Agent behavior affect users and collaborative work? | Appropriate study design, user/task sampling, instruments, qualitative/quantitative interpretation and applicable human-subject requirements. |

Treat combinations as a union of relevant checks. A clinical Agent remains an Agent system but also needs the applicable medical evidence. A multi-agent wrapper is an implementation choice until a research claim and comparison establish its contribution.

## Explore the capability space

For each requested capability, map established paradigms, current direct competitors, datasets, strongest simple alternatives, reported limitations and open questions. Verify current benchmark/model facts through primary sources; do not freeze a remembered leaderboard into the skill.

| Capability | Questions to explore | Useful controlled comparisons |
|---|---|---|
| Intent and task formulation | How are ambiguous goals resolved, constraints retained and success recognized? | Direct prompting, structured specification, clarification policy; vary ambiguity and conflicting constraints. |
| Routing and delegation | What determines model/tool/role selection, rejection or escalation? | Fixed routing, rules, learned routing and an oracle where definable; measure selection errors and overhead. |
| Planning and decomposition | What is planned, revised or executed reactively? | No planner, simple decomposition, search/classic planning and replanning; vary horizon and environment changes. |
| Tool use | Are tool selection, arguments, sequencing and result interpretation correct? | Tool-free and fixed-tool baselines; malformed inputs, partial results and changing schemas. |
| Retrieval and grounding | What information is fetched, ranked, cited and actually used? | No retrieval, lexical retrieval, dense/hybrid retrieval and reranking where appropriate; keep corpus/snapshot equal. |
| Memory and context | What is stored, retrieved, updated, forgotten and isolated? | No memory, full recent history, fixed summaries, simple stores; vary context limits, stale/conflicting facts and session boundaries. |
| Reasoning and verification | Which decisions require checking, and does verification catch real errors? | Equal-budget direct solving, self-checking, independent checks and external validators; count false confidence and false rejection. |
| Reflection and adaptation | What changes after feedback, and is improvement persistent? | Fixed policy and simple retry; separate online feedback from test leakage and learning from extra attempts. |
| Multi-agent coordination | When do additional roles improve outcome, and how are conflicts resolved? | Strong single agent, same total budget, sequential ensemble and centralized controller; vary communication structure and role count. |
| Long-horizon execution | Does the Agent maintain state, dependencies and stopping behavior over time? | Short/long horizons, interrupted tasks and environmental drift; measure compounding failure and successful recovery. |
| Learning and optimization | Which parameters, policies or prompts are optimized with what feedback? | Untuned and equally tuned baselines, held-out tasks, stable training/evaluation split and total tuning cost. |
| Multimodal or embodied action | How does perception uncertainty affect actions and feedback? | Appropriate perceptual/action baselines, sensor changes and real/simulated setting distinctions. |
| Human oversight | When is assistance requested, accepted or ignored? | Explicit interaction budgets and task difficulty; measure human time and intervention quality as well as success. |
| Reliability and misuse resistance | Which unwanted actions or false conclusions are possible in the intended setting? | Authorized sandbox evaluations for untrusted content, permission boundaries, data isolation and safe failure. |

Do not require every row for every task. Record the selected rows and why excluded ones are outside the question. Broaden the search when a supposedly new mechanism resembles search, caching, scheduling, program analysis, control, active learning or another established field.

## Investigate the program and runtime

Read the repository's instructions, entry points, dependency manifests, configuration, interfaces, tests and representative traces before redesigning it. Confirm what is implemented rather than inferring functionality from diagrams or README claims.

| Program layer | Inspect | Evaluation or artifact |
|---|---|---|
| Controller and state | State transitions, termination, task dependencies and cancellation | State-transition specification, dead-end/loop cases and traceable decisions. |
| Tool boundary | Schemas, validation, adapters, errors and returned evidence | Contract checks; real success distinguished from transport success. |
| Execution isolation | File/network permissions, secrets, untrusted outputs and side effects | Authorized sandbox scenarios and least-required permission inventory. |
| Scheduling | Concurrency, queues, backpressure, shared budgets and fairness | Throughput/latency under load, saturation and resource contention. |
| Recovery | Retries, timeouts, checkpoints, idempotency and compensation | Interrupted runs, partial failures, restart/resume and duplicate side-effect prevention. |
| Memory/storage | Provenance, indexing, updates, retention and user/task separation | Retrieval quality, stale data behavior, storage cost and cross-task isolation. |
| Observability | Structured events, correlation IDs, outcomes and redaction | Reconstructable runs with useful failure categories and no exposed credentials. |
| Deployment/reproducibility | Versions, environment, configuration and service contracts | Reproducible manifest, configuration example and explicit unavailable components. |

For each proposed architecture choice, state the workload observation or requirement that motivates it, alternatives considered, expected tradeoff and an experiment that could refute the choice. Avoid a feature inventory that never answers why the design matters.

## Define a convincing evaluation

### Claim-to-experiment contract

Create one row per substantive claim:

| Claim | Required comparison | Unit and outcome | Evidence and limitation |
|---|---|---|---|
| Capability gain | Mechanism removed/replaced under comparable resources | Task-level success or a justified capability measure | Repeated outcomes, uncertainty, stratification and failed cases. |
| Efficiency gain | Comparable quality at measured resource use, or comparable resources at measured quality | Latency, calls, tokens, memory, compute or total cost | Quality–resource curve and accounting assumptions. |
| Reliability gain | Controlled failures and realistic workload variation | Failure/recovery rates and correctly completed tasks | Failure taxonomy, retry/timeout accounting and side-effect checks. |
| Generality | Held-out tasks, domains, models or environments relevant to the claim | Defined transfer unit | Changes in assumptions and domains where the conclusion stops applying. |

Do not claim all forms of efficiency from one token count, or reliability from a few successful demonstrations. Report tradeoffs that weaken the headline.

### Comparators and budget fairness

1. Include a credible non-Agent/simple workflow when it could solve the task, the strongest relevant single Agent and the most dangerous direct competitor. Justify exclusions using access or task compatibility, not convenience.
2. Compare model versions, prompts, available tools, retrieved corpus, training/tuning data, retry policy and stopping rules. State every material difference.
3. When the contribution is orchestration, include equal total compute/call/token or monetary-budget comparisons as appropriate. Where exact equality is impossible, report budget curves and limitations.
4. Separate component ablations from replacements with sensible alternatives. Removing a component can also remove compute or information; account for that change.
5. Measure end-to-end outcomes as well as microbenchmarks. Add scale/load/horizon studies for systems claims and cross-task robustness for capability claims.

### Data and evaluator validity

- Define the sampling frame, task split, exclusion criteria and evaluation unit. Keep development/tuning cases separate from the test set, including generated variations of the same underlying task.
- Identify potential contamination from public benchmark answers, retrieval corpora, cached traces, demonstrations and feedback. Document uncertainty when training exposure cannot be established.
- Prefer objective task validators where valid. Verify the validator itself against representative successful and unsuccessful cases.
- For LLM judges, record model/version, rubric and prompt; test agreement against a justified independently assessed subset, report disagreement and control answer-order/style effects where relevant.
- Keep test outcomes out of iterative prompt tuning. If the test set informed changes, label it development evidence and obtain a fresh held-out evaluation for the revised claim.
- Treat tasks, users or environments as the statistical unit when that matches the design. Repeated runs of the same task are not automatically independent samples from the task population.
- Report uncertainty and effect magnitude using methods appropriate to the design. Explain missing runs, crashes, truncation and multiple comparisons rather than selectively omitting them.

### Cost, latency and operational metrics

Record the model/provider snapshot, token categories, cache policy, tool calls, retries, failed calls, timeouts, human interventions, execution hardware and workload. Retrieve current prices when estimating monetary cost; preserve currency/date and include relevant external-service costs. Do not infer billed cost from output tokens alone.

Measure latency boundaries explicitly: request-to-completion, model time, tool time, queue time and recovery time. Report distributions when tail behavior matters. Distinguish warm/cold starts and concurrency. State whether failed tasks are included in cost and latency summaries.

Use failure categories that explain action: misunderstanding, planning, retrieval, tool selection, argument construction, environment failure, state corruption, unsupported answer, premature termination and nontermination. Link representative traces with sensitive data removed.

## Reproduce, implement and test

1. Pin accessible source commits, dataset versions, model IDs and configuration. Preserve licenses and cite reused artifacts. Check upstream interfaces before selecting a framework version.
2. Reproduce a small, representative baseline run and compare expected data shapes and metrics before changing the architecture. State deviations from the original setup.
3. Implement the minimum mechanism necessary to test the claim. Keep evaluation code distinct from training/tuning where practical and protect reference results from accidental overwrite.
4. Use meaningful tests at fragile boundaries: tool response validation, termination, budget exhaustion, interrupted state, duplicate work and permission enforcement. Add task-level tests that can fail even if helper functions individually pass.
5. Run within the user's authorized local resources. Prepare expensive experiments concretely before requesting any genuinely missing resource/budget decision. Do not silently start paid sweeps or external deployments.
6. Store configuration, command, seed when relevant, dataset split, timestamps, raw outcomes, exclusions and environment. Preserve failures and partial runs instead of replacing them with expected values.
7. Derive plots/tables from recorded data. Verify units, sample counts, aggregation and captions; distinguish measured, estimated and illustrative numbers.
8. Describe what ran and what remains planned. Static inspection, mocked service tests, live API smoke tests and benchmark evaluations establish different things.

The host performs code inspection, implementation, experiments and scientific judgment using available tools. A routing or evidence-ledger script does not itself train models, run remote benchmarks or prove an Agent research claim.

## Connect evidence to a paper and venue

- For a methods paper, organize the argument around a bounded problem, mechanism, evidence and limitations. For a systems paper, connect workload constraints to design choices, implementation and end-to-end evaluation.
- Separate design description from observations and results. Do not invent production experience, user feedback, deployment scale or a favorable comparison.
- Use current primary literature for related work. Preserve conference research in the literature review when relevant. A user's SCI-journal requirement applies to submission candidates; it does not erase important conference evidence.
- Consult journal aims/scope, accepted article types and recent comparable journal papers. Match the contribution: Agent theory/methods, software engineering/system design, engineering application, HCI or domain science.
- Keep journal and conference identities explicit. AAMAS, ACL, ICSE, NeurIPS, OSDI and similar conferences do not become SCI journals because they are relevant or prestigious. A plugin named after one Chinese journal is not a catalog of all CS journals.
- Evaluate submission fit in `publication.md`. Scientific limitations and venue fit may inform a practical submission order, but they do not justify an individual acceptance probability.

## Failure conditions, worked prompts and sources

Stop the dependent claim when the evidence fails: an unverified metric stays unknown; an unavailable artifact stays unreproduced; a failed baseline becomes a documented limitation. Continue useful independent work, such as design inspection or an executable experiment plan. Do not replace a missing experiment with a plausible narrative.

- `用 $scholar-route 研究多 Agent 路由，重点判断收益是不是来自多花 token，并给出可执行的对照实验。`
- `用 $scholar-route 检查这个 Agent 程序的断点恢复和工具调用，提出能写成系统论文的可验证问题。`
- `用 $scholar-route 为 Agent 记忆机制做文献地图、创新性审查、消融设计和无强制 APC 的 SCI 选刊。`

Original synthesis informed by [Orchestra ML and systems writing workflows](https://github.com/Orchestra-Research/AI-Research-SKILLs/tree/main/20-ml-paper-writing), [polish_skill novelty and experiment audits](https://github.com/yujie-jason-zhang/polish_skill), [Researcher](https://github.com/sokolmarek/researcher), [Superpapers](https://github.com/regisely/superpapers), and [LongTable](https://github.com/HosungYou/LongTable). These workflow repositories are not empirical evidence that a proposed Agent mechanism works.
