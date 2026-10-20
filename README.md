# ScholarRoute · 研途

**把研究领域、Agent 项目或论文初稿，推进到文献地图、可验证问题、实验方案和投稿路线。**

ScholarRoute 是一个可按领域组合的科研与选刊技能。它根据**领域、贡献类型和当前阶段**选择需要的流程，将文献探索、Agent 能力与程序研究、实验、写作、选刊、投稿和返修连接到同一项目记录。

重点适合 **LLM Agent 能力研究、Agent 程序/系统研究，以及优先考虑费用和实际适配度的期刊选择**。中文讨论和英文论文写作可以在同一项目中协作。

[English](README.en.md) · [技能入口](skills/scholar-route/SKILL.md) · [覆盖与修复索引](docs/COVERAGE.md) · [来源明细](docs/source-audit.md) · [本轮验收](docs/AUDIT-2026-10-20.md)

## 能解决什么问题

| 你的起点 | 技能完成的工作 | 获得的产物 |
|---|---|---|
| 只有一个领域，不知道研究哪个点 | 阅读综述与代表论文，整理问题、方法、证据和竞争者 | 领域地图、研究问题候选、下一轮检索路线 |
| 有一个 Agent 想法或程序 | 区分能力创新与系统贡献，比较替代设计和失败场景 | 可证伪假设、基线、消融、最小实验和实现计划 |
| 有实验结果，不知道怎么组织论文 | 建立问题—机制—结果—结论的论证链 | 论文结构、英文段落、图表与引文检查清单 |
| 有稿件，想找相对现实、费用合适的期刊 | 多来源发现候选，调查同刊先例、文种、索引、费用和审稿时间 | 单刊档案、三类候选池、主投/备选顺序和补强任务 |
| 已收到审稿意见 | 拆解每条意见，关联补实验、实际改动与稿件位置 | 返修任务表、逐条回复和修改定位 |
| 项目做了一半，需要继续 | 读取已有账本、历史和关系图 | 延续原有证据、实验与决策的下一步工作 |

## v1.1.0 概览

| 组成 | 内容 |
|---|---|
| 领域配置 | **8 个**，支持交叉领域组合 |
| 统一能力 | **41 项**，每项都有入口与工作流说明 |
| 来源覆盖 | **17 个来源仓库、139 条技能/子模式/领域变体映射** |
| 冲突整合 | **33 条规则**；18 条关联程序行为测试，15 条关联工作流场景审查 |
| 原生检索 | OpenAlex、Crossref、DBLP、arXiv |
| 本地工具 | 路由、证据账本、历史、约束筛选、报告、图和 BibTeX 导出 |
| 实测 | **118 项 Python 回归通过**；包含 288 种路由组合 |
| 运行环境 | Python 3.11+，核心使用标准库 |

**使用一个入口即可组合这些能力。**139 条记录是来源特点到统一模块的映射；具体功能在本项目中由三层协作完成：Python 工具处理确定性任务，使用本技能的 Agent 执行阅读、研究与写作流程，宿主提供浏览、代码运行、绘图及专业数据库访问。

## 全流程文本图

```text
输入：领域 / 研究笔记 / Agent 代码 / 论文初稿
  │
  ▼
目标与阶段识别 ─── 领域组合 + 贡献类型 + 语言/预算/数据条件
  │
  ├─ 领域探索
  │   多源检索 → 身份与版本 → 精读与证据提取 → 领域地图
  │                                            │
  ├─ 研究设计 ◀─────────────────────────────────┘
  │   竞争方法 → 创新差异 → 可证伪假设 → 最小验证实验
  │                                  │
  │           ┌──────────────────────┴────────────────────┐
  │           ▼                                           ▼
  │     Agent 能力研究                              Agent 程序研究
  │     规划 / 记忆 / 工具 / RAG / 协作             状态 / 调度 / 恢复 / 存储 / 部署
  │           └──────────────────────┬────────────────────┘
  │                                  ▼
  ├─ 实验与实现：基线 → 等预算对照 → 消融 → 故障注入 → 统计与复现
  │                                  │
  │                         新证据 ────┴──→ 更新问题与地图
  │                                  ▼
  ├─ 论文与选刊
  │   论证 / 写作 / 引文 / 图表 / 多视角审稿
  │   候选召回 → 单刊调查 → 索引/分区/费用/时间 → 适配比较
  │                         ├─ 符合条件 → 主投/备选顺序
  │                         ├─ 待核实   → 指定字段与来源
  │                         └─ 排除     → 保存明确原因
  │                                  ▼
  └─ 投稿与后续：模板 / 投稿信 / 预检 → 逐条返修 → 清样 / 传播 / 更正

贯穿所有阶段：project.json + 证据来源 + 历史版本 + 决策记录
交付：REPORT.md / MAP.md / journals.csv / references.bib / assessment.json
扩展：来源特点 → 能力 ID → 实现/工作流 → 冲突用例 → 回归验证
```

## 快速开始

### 安装和验证

```bash
git clone https://github.com/PresleyRen/scholar-route.git
cd scholar-route
python tests/run.py
python tools/validate_package.py
python tools/coverage_audit.py --check
```

技能目录是 `skills/scholar-route/`，入口是 `SKILL.md`。Codex 可将整个目录安装到项目的 `.agents/skills/scholar-route/`，或个人目录 `~/.agents/skills/scholar-route/`；调用方式见 [官方技能文档](https://learn.chatgpt.com/docs/build-skills)。其他支持本地技能的宿主可以加载相同入口。

```text
用 $scholar-route 探索 LLM Agent 的长期记忆和错误恢复。
先读取已有项目；整理领域地图、竞争方法与研究问题。
分别分析能力创新和程序/系统创新，设计等预算基线、消融和最小实验。
再根据稿件证据筛选 SCIE 期刊，优先无强制发表费用的路线。
中文讨论，论文段落用英文。
```

### 直接使用 Python 工具

```bash
python skills/scholar-route/scripts/scholar_route.py route \
  --topic "LLM Agent memory and recovery" \
  --domains agent-ai,computer-science --stage full

python skills/scholar-route/scripts/scholar_route.py init \
  --project ./work/agent-memory --topic "LLM Agent memory and recovery" \
  --domains agent-ai,computer-science --language zh-CN

python skills/scholar-route/scripts/scholar_route.py search \
  --provider crossref --query "language agent memory" \
  --limit 5 --project ./work/agent-memory

python skills/scholar-route/scripts/scholar_route.py report \
  --project ./work/agent-memory
```

运行离线示例查看完整产物：

```bash
python examples/run_demo.py --project ./work/demo
```

示例使用明确标记的合成期刊记录，展示候选筛选、证据保存、关系图与报告导出。真实研究时，将检索结果和核验后的期刊事实导入项目即可继续。

## 按领域组合能力

<!-- DOMAINS:START -->

| 配置 ID | 领域 | 首选来源路线（原生与宿主来源合并列示） |
|---|---|---|
| `agent-ai` | LLM Agent 能力与系统 | OpenAlex、DBLP、arXiv、Semantic Scholar、Crossref、Hugging Face Papers |
| `computer-science` | 计算机、软件工程与 NLP | DBLP、OpenAlex、arXiv、Semantic Scholar、Crossref、ACM Digital Library、IEEE Xplore |
| `engineering` | 工程、控制与应用 AI | OpenAlex、Crossref、IEEE Xplore、Scopus |
| `biomedicine` | 生物、医学与公共健康 | PubMed、PMC、Europe PMC、bioRxiv、medRxiv、OpenAlex、Crossref |
| `social-sciences` | 社会科学、心理、教育与 HCI | OpenAlex、Crossref、Semantic Scholar、Scopus、Web of Science、ERIC |
| `food-agriculture` | 食品、营养与农业 | PubMed、OpenAlex、Crossref、AGRICOLA |
| `humanities` | 人文、历史与哲学 | OpenAlex、Crossref、JSTOR、disciplinary bibliographies |
| `general` | 通用领域自适应 | OpenAlex、Crossref、Semantic Scholar、DOAJ |

<!-- DOMAINS:END -->

| 场景 | 推荐组合 | 重点增加的流程 |
|---|---|---|
| Agent 规划、记忆、工具能力 | `agent-ai,computer-science` | 能力拆解、竞争机制、等预算基线、任务评测 |
| Agent 框架、运行时、错误恢复 | `agent-ai,computer-science,engineering` | 架构取舍、故障注入、幂等性、延迟与成本 |
| 医疗文献 Agent | `agent-ai,computer-science,biomedicine` | 医学文献路线、研究设计评价、任务与临床证据分层 |
| 人机协作与 Agent 用户研究 | `agent-ai,social-sciences` | 人类监督、用户实验、测量与混杂控制 |
| 食品或农业 Agent 应用 | `agent-ai,food-agriculture` | 领域数据、专项数据库、应用评价与可复现分析 |
| 已有论文、只做选刊 | 对应领域 + `--stage journal` | 画像、召回、单刊、费用、索引与投稿顺序 |

其他阶段包括 `explore`、`review`、`design`、`experiment`、`dossier`、`write`、`audit`、`submit`、`revise`、`disseminate` 和 `full`。地区路线可选 `international`、`china`、`turkey`。

## 41 项能力详情

<!-- CAPABILITIES:START -->

| 能力 ID | 能力 | 具体产物 |
|---|---|---|
| `intake` | [目标、证据与限制](skills/scholar-route/references/data-contracts.md) | 研究目标、贡献类型、稿件阶段、语言、预算和已有证据清单。 |
| `field-map` | [领域结构与研究地图](skills/scholar-route/references/exploration.md) | 问题—方法—证据—研究缺口地图，以及下一轮探索入口。 |
| `search-protocol` | [检索协议与多语言查询](skills/scholar-route/references/exploration.md) | 中英文查询词、数据库路线、时间范围、筛选标准与查询日志。 |
| `paper-search` | [论文与开放科研资源检索](skills/scholar-route/references/sources-and-tools.md) | 多源论文记录、检索状态与来源信息；四个原生 API 统一导入。 |
| `identifier-check` | [DOI、ISSN、版本与元数据校验](skills/scholar-route/references/data-contracts.md) | DOI、ISSN、元数据、预印本和正式版本的身份与关联记录。 |
| `evidence-review` | [筛选、提取、质量与证据综合](skills/scholar-route/references/exploration.md) | 文献筛选表、证据提取表、质量评价和跨研究综合。 |
| `paper-notes` | [精读、笔记与主张关联](skills/scholar-route/references/exploration.md) | 问题、机制、数据、结果、代码和主张关联的精读笔记。 |
| `novelty-audit` | [新颖性、反证与研究空白](skills/scholar-route/references/exploration.md) | 最近竞争方法、相邻领域先例、创新差异和反证清单。 |
| `hypothesis-plan` | [可证伪假设与可行性](skills/scholar-route/references/exploration.md) | 可证伪假设、机制解释、可行性分析与最小验证实验。 |
| `agent-capabilities` | [Agent 能力拆解与评测](skills/scholar-route/references/agent-research.md) | 14 类 Agent 能力的机制拆解、比较基线和评价协议。 |
| `agent-systems` | [Agent 程序、架构与运行实验](skills/scholar-route/references/agent-research.md) | 8 个程序层的架构分析、故障模型、运行轨迹与系统实验。 |
| `experiment-plan` | [实验设计与效度](skills/scholar-route/references/exploration.md) | 变量、对照、消融、指标、样本、资源预算和停止条件。 |
| `statistics-robustness` | [统计、稳健性与不确定性](skills/scholar-route/references/publication.md) | 统计单位、置信区间、混杂、泄漏、多重比较与稳健性检查。 |
| `implementation` | [复现、代码实现与执行记录](skills/scholar-route/references/agent-research.md) | 基线复现、最小机制实现、等预算运行与命令和结果记录。 |
| `data-collection` | [数据计划、出处与再利用](skills/scholar-route/references/exploration.md) | 数据出处、许可、采样、版本、质量、拆分和再利用计划。 |
| `state-map` | [项目记录、关系图与断点恢复](skills/scholar-route/references/data-contracts.md) | 持久项目账本、关系图、版本历史、断点恢复与报告导出。 |
| `manuscript-profile` | [稿件画像与贡献类型](skills/scholar-route/references/journal-selection.md) | 研究问题、贡献、方法角色、证据、读者和文章类型画像。 |
| `venue-discovery` | [多来源期刊与候选召回](skills/scholar-route/references/journal-selection.md) | 由相似论文、专业刊、出版社匹配器及索引合并生成候选池。 |
| `venue-identity` | [期刊/会议身份与 ISSN](skills/scholar-route/references/journal-selection.md) | 刊名、ISSN、出版社、官方入口、改名记录与发表载体类型。 |
| `journal-dossier` | [单刊全景与作者指南](skills/scholar-route/references/journal-selection.md) | 单刊范围、同刊先例、文章类型、费用、时间和作者要求档案。 |
| `indexing-metrics` | [索引、分区、年份与类别](skills/scholar-route/references/journal-selection.md) | 按体系、年度和学科类别保存索引身份与分区事实。 |
| `costs-timelines` | [费用路径与审稿时间定义](skills/scholar-route/references/journal-selection.md) | 必缴费用、可选 OA、减免条件、货币与不同审稿时间端点。 |
| `journal-integrity` | [出版透明度与风险证据](skills/scholar-route/references/journal-selection.md) | 期刊身份、政策透明度、同行评审与出版风险的具体证据。 |
| `fit-comparison` | [适配、证据与三态筛选](skills/scholar-route/references/journal-selection.md) | 符合、待核实、排除三类候选，以及各项条件和适配比较理由。 |
| `submission-plan` | [可解释投稿顺序](skills/scholar-route/references/journal-selection.md) | 可解释的主投/备选顺序、补强任务和改投触发条件。 |
| `argument-audit` | [论证与实验叙事重构](skills/scholar-route/references/publication.md) | 问题—机制—实验—结论的论证链，以及缺少比较和逻辑跳步。 |
| `manuscript-writing` | [科学写作、润色与数值保真](skills/scholar-route/references/publication.md) | 中文或英文论文段落、润色与结构调整，保持数值、术语和引用一致。 |
| `citation-audit` | [引文、BibTeX 与引用支持](skills/scholar-route/references/publication.md) | 引用身份、版本、内容支持和位置检查，以及 BibTeX 整理。 |
| `figure-table-audit` | [图表、单位与可视化检查](skills/scholar-route/references/publication.md) | 图表数据、单位、样本数、标注、可读性与目标刊要求检查。 |
| `peer-review` | [分角色审稿与异议归并](skills/scholar-route/references/publication.md) | 多视角模拟审稿、关键异议、证据定位和可执行修改建议。 |
| `venue-formatting` | [期刊模板、改投与排版](skills/scholar-route/references/publication.md) | 当前作者指南、文章类型要求、模板适配和改投排版清单。 |
| `cover-letter` | [投稿信](skills/scholar-route/references/publication.md) | 围绕真实贡献与期刊范围撰写的投稿信。 |
| `presubmission-inquiry` | [投稿前询问信](skills/scholar-route/references/publication.md) | 具有明确适配问题和研究摘要的投稿前询问信。 |
| `reviewer-discovery` | [审稿人候选与利益冲突](skills/scholar-route/references/publication.md) | 按专长、论文和利益冲突条件组织的审稿人候选资料。 |
| `authorship-credit` | [署名、CRediT 与声明核实](skills/scholar-route/references/publication.md) | 作者实际贡献、CRediT 角色和声明的统一记录。 |
| `submission-preflight` | [Quick/Full 投稿预检](skills/scholar-route/references/publication.md) | Quick/Full 两级稿件、图表、声明、附件与数据代码预检。 |
| `revision-response` | [逐条返修与修改定位](skills/scholar-route/references/publication.md) | 逐条意见、回复、实际改动与稿件定位的返修对照表。 |
| `proof-check` | [清样核对](skills/scholar-route/references/publication.md) | 录用稿与清样的文字、数值、公式、署名、引用和排版差异。 |
| `dissemination` | [发表后传播与公开材料](skills/scholar-route/references/publication.md) | 基于发表结果的通俗摘要、海报、展示与公开材料草稿。 |
| `postpublication-correction` | [更正与发表后问题处理](skills/scholar-route/references/publication.md) | 错误影响分析、证据整理和更正沟通材料。 |
| `regional-indexing` | [中文/土耳其期刊与目录](skills/scholar-route/references/domains.md) | 中文和土耳其期刊的目录、身份与地区投稿路线。 |

<!-- CAPABILITIES:END -->

每项能力的来源特点、实现文件、冲突规则与测试入口集中在 [覆盖与修复索引](docs/COVERAGE.md)。

## Agent 专项：能力与程序都覆盖

**14 个能力族：** 意图与任务定义、路由与委派、规划与分解、工具使用、检索与依据、记忆与上下文、推理与验证、反馈与适应、多 Agent 协作、长任务执行、学习与优化、多模态与具身行为、人类监督、可靠性与误用抵抗。

**8 个程序层：** 控制器/状态、工具接口、执行隔离、调度、恢复、记忆/存储、可观测性、部署/复现。

例如，研究“多 Agent 更有效”时，比较强单 Agent、同总 token/调用预算和顺序集成；研究“记忆更可靠”时，测试过期、冲突和跨任务污染；研究“恢复更好”时，测中断、重试、幂等性、重复副作用和最终任务结果。协议在 [Agent 研究指南](skills/scholar-route/references/agent-research.md)。

## 这些来源如何互补

本轮逐项核对了原清单中的 17 个现行来源仓库。139 条来源映射均有对应能力 ID、固定版本和文件证据；41 项能力均有工作流入口。

| 参考来源 | 保留的特点 | 互补方式 |
|---|---|---|
| [zero565656/journal-recommender](https://github.com/zero565656/journal-recommender) | 摘要画像与投稿梯队 | 先形成投稿梯队，再用单刊档案与多源核验补齐证据。 |
| [kkunkunya/journal-research-agent-plugins](https://github.com/kkunkunya/journal-research-agent-plugins) | 中英文、多数据库发现与权威核验分工 | 广泛发现候选，再由本地索引和单刊调查提高深度。 |
| [keros68/xiaoyu-skill](https://github.com/keros68/xiaoyu-skill) | 相似论文反查期刊、本地索引及选刊模式切换 | 保留相似论文反查与可更新索引，缺失的关键字段转入核验队列。 |
| [huangwb8/ChineseResearchLaTeX](https://github.com/huangwb8/ChineseResearchLaTeX) | 从候选发现深入到单刊全景调查 | 保留发现与单刊调查，计算机研究补充 DBLP、arXiv 和系统评测路线。 |
| [hztopcu/journal-fit-finder](https://github.com/hztopcu/journal-fit-finder) | 主题、方法、读者、文种与出版商多样性比较 | 综合主题、方法、读者和文种，搭配投稿规划与结构化期刊档案。 |
| [yujie-jason-zhang/polish_skill](https://github.com/yujie-jason-zhang/polish_skill) | 精读、创新审计、论证重构、写作与回复衔接 | 论文修改衔接证据审查和投稿要求，统一记录引用、数字和修改。 |
| [yaotingsun/academic-publishing-skills](https://github.com/yaotingsun/academic-publishing-skills) | 投稿前询问至清样、更正的发表生命周期 | 将选刊接到询问、投稿、返修、清样和更正流程。 |
| [regisely/superpapers](https://github.com/regisely/superpapers) | 复现驱动的问题发现、实验计划与稳健性 | 把研究问题连到可复现实验，加入 Agent 能力和系统研究的比较协议。 |
| [sokolmarek/researcher](https://github.com/sokolmarek/researcher) | 研究流水线、代码分析、竞争方法与版本管理 | 用持续项目记录连接代码分析、竞争方法、实验与写作。 |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 论文身份、综述方法、证据批判与模板检查 | 用文献身份、综述和批判评价支持选刊及 ML/系统论证。 |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | 区分 ML 能力贡献与系统设计贡献 | 分清能力创新与程序贡献，再匹配对应实验和期刊要求。 |
| [Zaious/journal-atlas](https://github.com/Zaious/journal-atlas) | 结构化期刊档案与证据等级、档案更新 | 结构化保存单刊证据，配合多源召回持续更新档案。 |
| [alexishuang1901-hub/journal-finder](https://github.com/alexishuang1901-hub/journal-finder) | 由文献定位发表社区、本地索引维护 | 用参考文献发现发表社区，再补跨库发现与单刊核验。 |
| [yibeixiaobai/journal-selector](https://github.com/yibeixiaobai/journal-selector) | 中文期刊条件和国内目录路径 | 保留中文目录条件，并入统一身份、费用与投稿路线。 |
| [brycewang-stanford/Awesome-Journal-Skills](https://github.com/brycewang-stanford/Awesome-Journal-Skills) | 学科与具体发表场所的写作要求 | 把具体刊会要求接到范围识别、文种与投稿预检。 |
| [PangenomeAI/academic-skills-food-nutrition](https://github.com/PangenomeAI/academic-skills-food-nutrition) | 食品农业专项检索、研究计划和展示流程 | 食品农业专项路线与通用证据审查、实验设计互补。 |
| [HosungYou/LongTable](https://github.com/HosungYou/LongTable) | 项目访谈、互补审稿视角与持续证据包 | 项目访谈与互补审稿视角持续更新同一证据包。 |

完整模块级出处见 [来源审计](docs/source-audit.md)，提交与文件路径保存在 [upstreams.json](skills/scholar-route/assets/upstreams.json)。

## 冲突如何处理，保留了什么

| 冲突 | 整合后的行为 | 验证入口 |
|---|---|---|
| 学科不同，默认数据库和研究规则不同 | 按研究对象组合来源；医学 Agent 同时保留计算机与医学路线 | 288 种领域/阶段/地区组合与交叉领域测试 |
| 期刊字段缺失，却要做硬筛选 | 明确符合、待核实、排除三类，保留缺失字段 | 三态筛选、过时证据与冲突事实测试 |
| JCR、SJR、中科院分区被混用 | 按体系、年度、学科类别分别比较 | 精确分区与同版本矛盾测试 |
| 可选 OA 被当成强制费用 | 按实际发表路径保存必缴费、可选费和减免条件 | 零费用、货币、完整费用和 OA 测试 |
| 首次决定、外审、录用和发表时间混在一起 | 四个端点分别保留 | 时间字段保存与导出测试 |
| 数量模板要求固定候选数 | 按实际证据生成短名单，保留出版社多样性 | 不补空位、排序稳定性和出版社上限测试 |
| 新旧证据相互覆盖 | 保存冲突双方和历史，核验后显式解决 | 冲突重导入、解决与幂等测试 |
| 润色、审稿、格式检查相互越权 | 一个修改负责人，证据核查与格式核查分工 | 15 个工作流冲突场景及处理产物 |

33 条规则的逐项对应关系见 [冲突—测试索引](docs/COVERAGE.md)，工作流场景的输入、处理结果和取舍见 [场景审查](docs/WORKFLOW-REVIEW.md)。

## 实测结果

| 检查 | 本轮结果 |
|---|---|
| Python 自动化回归 | **118/118 通过**：原有 89 项 + 新增 29 项 |
| 路由组合 | **288/288 组合通过**，作为一项参数组合回归执行 |
| 来源与实现索引 | **17 个来源、139 条映射、41 项能力、33 条冲突**通过一致性检查 |
| 程序冲突 | **18 条**规则关联实际行为测试 |
| 工作流冲突 | **15 条**固定场景已应用规则并保存处理结果 |
| 合成端到端示例 | 初始化、证据导入、候选筛选、图与报告导出完成 |

自动化测试记录与工作流审查分别保存。详情、命令及验证范围见 [本轮验收](docs/AUDIT-2026-10-20.md)；每次提交的 Python 3.11/3.12 结果可在 [GitHub Actions](https://github.com/PresleyRen/scholar-route/actions) 查看，运行产物包含对应源码与测试日志。

## 怎样快速定位不足并扩展

先按**症状、能力 ID 或来源名**查找：

```bash
python tools/coverage_audit.py --find "费用"
python tools/coverage_audit.py --find agent-systems
python tools/coverage_audit.py --find journal-recommender
```

返回：能力、工作流文件、原生实现位置、来源、冲突 ID 和相关测试。

| 发现的问题 | 从哪里开始 | 修改与验证 |
|---|---|---|
| 某个领域没被正确识别 | `assets/domains.json`、`scripts/route_core.py` | 调整领域配置，运行路由与交叉领域测试 |
| 论文搜不到或响应解析不对 | `scripts/scholarly_sources.py`、`search_import.py` | 加入成功、空结果、错误响应、截断和身份保真用例 |
| 期刊费用、分区或状态判断不对 | `scripts/venue_audit.py`、`project_store.py` | 先添加失败样例，再改约束或事实规则 |
| Agent 实验不够有说服力 | `references/agent-research.md`、`exploration.md` | 加入竞争机制、对照/消融和新的场景处理结果 |
| 写作、审稿或返修出现缺口 | `references/publication.md` | 明确输入与产物，补充具体稿件/意见场景 |
| 新上游技能有值得吸收的特点 | `assets/upstreams.json`、`assets/modules.json` | 记录固定版本、特点、统一能力和冲突取舍 |
| 项目恢复、图或历史不正确 | `scripts/project_store.py`、`reports.py` | 增加状态、幂等、历史和导出回归 |

上表路径相对于 `skills/scholar-route/`。完整维护链路：

```text
症状 → 能力 ID → 来源特点 → 工作流/实现 → 最小失败样例
                                              │
                                              ▼
                    更新索引与 README ← 回归通过 ← 修复或补充
```

```bash
python tools/update_readme.py
python tools/coverage_audit.py --write
python tools/validate_package.py
python tools/update_readme.py --check
python tools/coverage_audit.py --check
python tests/run.py
```

注册表、README、来源映射和测试索引由这些检查保持同步。

## 项目文件与输出

```text
skills/scholar-route/
├── SKILL.md                  统一入口与自动触发描述
├── assets/
│   ├── domains.json          领域与检索来源配置
│   ├── modules.json          41 项能力注册表
│   └── upstreams.json        139 条来源特点与固定版本映射
├── references/               研究、选刊、Agent、发表与冲突工作流
└── scripts/                  路由、检索、状态、评估和导出

tools/coverage_audit.py       从问题定位能力、文件与测试
docs/COVERAGE.md              来源互补、模块和冲突索引
docs/WORKFLOW-REVIEW.md       15 个工作流场景与处理结果
tests/test_conflict_matrix.py 新增冲突与覆盖回归
```

| 项目产物 | 内容 |
|---|---|
| `project.json` | 八类证据实体、关联、修订号和历史 |
| `REPORT.md` | 研究条件、证据、主张、候选与下一步 |
| `MAP.md` | 当前实体关系图与清单 |
| `journals.csv` | 候选期刊与筛选状态 |
| `references.bib` | 引用记录 |
| `assessment.json` | 可由程序继续处理的条件评估 |

记录结构、事实字段和导入样例见 [数据契约](skills/scholar-route/references/data-contracts.md)与[记录示例](skills/scholar-route/references/record-examples.md)。

## 来源版本与许可

本项目原创实现采用 [MIT License](LICENSE)。参考来源及其许可证按固定提交记录，详见[来源审计](docs/source-audit.md)。

<details>
<summary>查看 17 个来源的版本与映射数量</summary>

<!-- SOURCES:START -->

| 来源仓库 | 映射条目 | 参考提交 | 许可证声明 |
|---|---:|---|---|
| [zero565656/journal-recommender](https://github.com/zero565656/journal-recommender) | 1 | [407aff1066](https://github.com/zero565656/journal-recommender/commit/407aff106677aac090bf2d177155db15e3593126) | 未发现许可证 |
| [kkunkunya/journal-research-agent-plugins](https://github.com/kkunkunya/journal-research-agent-plugins) | 17 | [d902e4cb07](https://github.com/kkunkunya/journal-research-agent-plugins/commit/d902e4cb07443f079cbb5085f2de2820a1a09f79) | MIT |
| [keros68/xiaoyu-skill](https://github.com/keros68/xiaoyu-skill) | 4 | [d8b26a741b](https://github.com/keros68/xiaoyu-skill/commit/d8b26a741beae6d474db08f9fe8bc857f0490a95) | MIT |
| [huangwb8/ChineseResearchLaTeX](https://github.com/huangwb8/ChineseResearchLaTeX) | 2 | [d288ea832e](https://github.com/huangwb8/ChineseResearchLaTeX/commit/d288ea832e4b2ffca5a0cca97576d3413391a342) | MIT |
| [hztopcu/journal-fit-finder](https://github.com/hztopcu/journal-fit-finder) | 1 | [2624d0b40a](https://github.com/hztopcu/journal-fit-finder/commit/2624d0b40a444951157c626c01bda73c65c60b23) | MIT |
| [yujie-jason-zhang/polish_skill](https://github.com/yujie-jason-zhang/polish_skill) | 9 | [9b2a86ca6a](https://github.com/yujie-jason-zhang/polish_skill/commit/9b2a86ca6ac88879a3d3490fecdb909673fd1562) | MIT |
| [yaotingsun/academic-publishing-skills](https://github.com/yaotingsun/academic-publishing-skills) | 18 | [3103f4d7d4](https://github.com/yaotingsun/academic-publishing-skills/commit/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e) | Apache-2.0 |
| [regisely/superpapers](https://github.com/regisely/superpapers) | 16 | [805a9a7369](https://github.com/regisely/superpapers/commit/805a9a7369d57f01b67732645175ad0b7a8a3f23) | MIT |
| [sokolmarek/researcher](https://github.com/sokolmarek/researcher) | 35 | [e4ddbf4eb8](https://github.com/sokolmarek/researcher/commit/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945) | MIT |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 7 | [593377bb04](https://github.com/K-Dense-AI/scientific-agent-skills/commit/593377bb048752abb0152deab9fbb1083a6087df) | MIT |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | 2 | [773a52944b](https://github.com/Orchestra-Research/AI-Research-SKILLs/commit/773a52944ba4747a18bd4ae9ade53fff041adcbc) | MIT |
| [Zaious/journal-atlas](https://github.com/Zaious/journal-atlas) | 2 | [574d27d84c](https://github.com/Zaious/journal-atlas/commit/574d27d84c270fc8da16df69d9bad929e5c341e0) | CC-BY-SA-4.0 content; MIT scripts |
| [alexishuang1901-hub/journal-finder](https://github.com/alexishuang1901-hub/journal-finder) | 2 | [b8fb764bc4](https://github.com/alexishuang1901-hub/journal-finder/commit/b8fb764bc4b60acb88538e579b165bf4745b3072) | MIT |
| [yibeixiaobai/journal-selector](https://github.com/yibeixiaobai/journal-selector) | 1 | [b5303f3531](https://github.com/yibeixiaobai/journal-selector/commit/b5303f35310500302e4f72381451dc6d2d433bc8) | 未发现许可证 |
| [brycewang-stanford/Awesome-Journal-Skills](https://github.com/brycewang-stanford/Awesome-Journal-Skills) | 7 | [932eb23331](https://github.com/brycewang-stanford/Awesome-Journal-Skills/commit/932eb23331721b16e967c59f093781be1928b498) | MIT |
| [PangenomeAI/academic-skills-food-nutrition](https://github.com/PangenomeAI/academic-skills-food-nutrition) | 10 | [01b2158a48](https://github.com/PangenomeAI/academic-skills-food-nutrition/commit/01b2158a48408a8d0e56238c04075080c793d53c) | MIT |
| [HosungYou/LongTable](https://github.com/HosungYou/LongTable) | 5 | [eed627a85f](https://github.com/HosungYou/LongTable/commit/eed627a85f0db7ea218beb56c61fde36c975a4e4) | MIT |

<!-- SOURCES:END -->

</details>
