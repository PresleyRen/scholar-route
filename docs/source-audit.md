# 来源、能力映射与许可证核验

核验日期：**2026-10-20**。本文记录 ScholarRoute 参考了哪些公开技能、保留了什么能力，以及哪些做法经过调整或未采用。精确提交、来源文件和模块映射见技能内的 `assets/upstreams.json`。

## 目录

- [范围与证据强度](#范围与证据强度)
- [来源版本和许可证](#来源版本和许可证)
- [逐项能力映射](#逐项能力映射)
- [冲突处理摘要](#冲突处理摘要)
- [外部服务的能力边界](#外部服务的能力边界)
- [可复核性与后续更新](#可复核性与后续更新)

## 范围与证据强度

这里覆盖上一轮调研的 **17 个现行公开仓库**，并将其中相关模块展开为 **139 条来源映射**。映射条目包括真实技能、子模式和成对的领域版本，因此 **139 不是独立可执行功能的数量**，也不表示安装了这些上游包。大型仓库中与本次研究—选刊—发表流程无关的全部技能不在逐文件审计范围内。

本项目采用独立编写的工作流、路由、数据约束与支撑代码。此审计没有复制上游技能正文、实现代码、期刊数据库、出版社模板或文章全文。引用上游，是为了让设计依据和差异可检查；上游并未因此成为本项目运行时依赖，也没有表示认可本项目。

已直接核验 GitHub 仓库元数据及默认分支提交，并读取许可证声明和相关文件。对于核心选刊文件，读取了原始说明中的相关章节；对于较大套件的附属模块，核验了仓库树、模块前言/开头或官方 README/marketplace 声明。每条记录标明检查层级；**未运行上游软件，也未检验上游声称的推荐准确率**。

## 来源版本和许可证

许可证列记录相应提交的可见声明，不把公开可读等同于可随意复制。对没有许可证的来源，只参考通用问题与能力，独立实现并保留出处。Journal Atlas 的内容和代码采用不同许可证，本项目没有引入其内容或脚本。后续若实际导入上游文件，必须重新检查该文件适用条款、保留所需声明，并更新来源清单。

| 来源 ID | 仓库 | 核验提交 | 许可证声明 | 本次检查 |
|---|---|---|---|---|
| `zero-journal-recommender` | [zero565656/journal-recommender](https://github.com/zero565656/journal-recommender) | [407aff1066](https://github.com/zero565656/journal-recommender/commit/407aff106677aac090bf2d177155db15e3593126) | not found | 仓库、相关 SKILL/模块开头及许可证声明 |
| `journal-research-plugins` | [kkunkunya/journal-research-agent-plugins](https://github.com/kkunkunya/journal-research-agent-plugins) | [d902e4cb07](https://github.com/kkunkunya/journal-research-agent-plugins/commit/d902e4cb07443f079cbb5085f2de2820a1a09f79) | MIT | 仓库、相关 SKILL/模块开头及许可证声明 |
| `sci-select` | [keros68/xiaoyu-skill](https://github.com/keros68/xiaoyu-skill) | [d8b26a741b](https://github.com/keros68/xiaoyu-skill/commit/d8b26a741beae6d474db08f9fe8bc857f0490a95) | MIT | 仓库、相关 SKILL/模块开头及许可证声明 |
| `chinese-research-latex` | [huangwb8/ChineseResearchLaTeX](https://github.com/huangwb8/ChineseResearchLaTeX) | [d288ea832e](https://github.com/huangwb8/ChineseResearchLaTeX/commit/d288ea832e4b2ffca5a0cca97576d3413391a342) | MIT | 仓库、相关 SKILL/模块开头及许可证声明 |
| `journal-fit-finder` | [hztopcu/journal-fit-finder](https://github.com/hztopcu/journal-fit-finder) | [2624d0b40a](https://github.com/hztopcu/journal-fit-finder/commit/2624d0b40a444951157c626c01bda73c65c60b23) | MIT | 仓库、相关 SKILL/模块开头及许可证声明 |
| `polish-skill` | [yujie-jason-zhang/polish_skill](https://github.com/yujie-jason-zhang/polish_skill) | [9b2a86ca6a](https://github.com/yujie-jason-zhang/polish_skill/commit/9b2a86ca6ac88879a3d3490fecdb909673fd1562) | MIT | 仓库、相关 SKILL/模块开头及许可证声明 |
| `academic-publishing-skills` | [yaotingsun/academic-publishing-skills](https://github.com/yaotingsun/academic-publishing-skills) | [3103f4d7d4](https://github.com/yaotingsun/academic-publishing-skills/commit/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e) | Apache-2.0 | 仓库、相关 SKILL/模块开头及许可证声明 |
| `superpapers` | [regisely/superpapers](https://github.com/regisely/superpapers) | [805a9a7369](https://github.com/regisely/superpapers/commit/805a9a7369d57f01b67732645175ad0b7a8a3f23) | MIT | 仓库、相关 SKILL/模块开头及许可证声明 |
| `researcher` | [sokolmarek/researcher](https://github.com/sokolmarek/researcher) | [e4ddbf4eb8](https://github.com/sokolmarek/researcher/commit/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945) | MIT | 仓库、相关 SKILL/模块开头及许可证声明 |
| `scientific-agent-skills` | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | [593377bb04](https://github.com/K-Dense-AI/scientific-agent-skills/commit/593377bb048752abb0152deab9fbb1083a6087df) | MIT | 仓库、相关 SKILL/模块开头及许可证声明 |
| `ai-research-skills` | [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | [773a52944b](https://github.com/Orchestra-Research/AI-Research-SKILLs/commit/773a52944ba4747a18bd4ae9ade53fff041adcbc) | MIT | 仓库、相关 SKILL/模块开头及许可证声明 |
| `journal-atlas` | [Zaious/journal-atlas](https://github.com/Zaious/journal-atlas) | [574d27d84c](https://github.com/Zaious/journal-atlas/commit/574d27d84c270fc8da16df69d9bad929e5c341e0) | CC-BY-SA-4.0 content; MIT scripts | 仓库、混合许可证、README 相关章节 |
| `journal-finder-local` | [alexishuang1901-hub/journal-finder](https://github.com/alexishuang1901-hub/journal-finder) | [b8fb764bc4](https://github.com/alexishuang1901-hub/journal-finder/commit/b8fb764bc4b60acb88538e579b165bf4745b3072) | MIT | 仓库、相关 SKILL/模块开头及许可证声明 |
| `cn-journal-selector` | [yibeixiaobai/journal-selector](https://github.com/yibeixiaobai/journal-selector) | [b5303f3531](https://github.com/yibeixiaobai/journal-selector/commit/b5303f35310500302e4f72381451dc6d2d433bc8) | not found | 仓库、相关 SKILL/模块开头及许可证声明 |
| `awesome-journal-skills` | [brycewang-stanford/Awesome-Journal-Skills](https://github.com/brycewang-stanford/Awesome-Journal-Skills) | [932eb23331](https://github.com/brycewang-stanford/Awesome-Journal-Skills/commit/932eb23331721b16e967c59f093781be1928b498) | MIT | 仓库、许可证、marketplace 包声明；未逐刊审计 |
| `food-nutrition-skills` | [PangenomeAI/academic-skills-food-nutrition](https://github.com/PangenomeAI/academic-skills-food-nutrition) | [01b2158a48](https://github.com/PangenomeAI/academic-skills-food-nutrition/commit/01b2158a48408a8d0e56238c04075080c793d53c) | MIT | 仓库、相关 SKILL/模块开头及许可证声明 |
| `longtable` | [HosungYou/LongTable](https://github.com/HosungYou/LongTable) | [eed627a85f](https://github.com/HosungYou/LongTable/commit/eed627a85f0db7ea218beb56c61fde36c975a4e4) | MIT | 仓库、许可证、README 相关章节 |

旧仓库 [keros68/sci-select](https://github.com/keros68/sci-select) 是历史参考；本次实现映射到上表的 `keros68/xiaoyu-skill/skills/sci-select`。其旧 README 中的测试数量、数据覆盖和准确率准备条件均不转写成本项目成绩。

## 逐项能力映射

“宿主工作流”表示由使用本技能的 Agent 按步骤完成；需要实际检索、阅读、分析或运行工具。“依赖外部工具”表示还需要可访问的服务、库或格式处理能力。二者都不表示把上游实现复制到 ScholarRoute。能力 ID 对应本项目统一注册表；多个上游模块可以汇入同一能力，而同一上游模块也可以跨多个阶段。

### zero-journal-recommender

摘要画像、投稿偏好、带证据的候选筛选和多档提交顺序。 [源仓库](https://github.com/zero565656/journal-recommender/tree/407aff106677aac090bf2d177155db15e3593126)。

| 上游模块或子模式 | 统一能力 ID | 整合方式与能力边界 |
|---|---|---|
| [journal-recommender](https://github.com/zero565656/journal-recommender/blob/407aff106677aac090bf2d177155db15e3593126/SKILL.md) | `venue-discovery`、`manuscript-profile`、`submission-plan` | **宿主工作流**：用范围、同刊先例、已核验约束生成可比较候选；提交顺序不是录用概率。 |

未采用或调整：

- 从摘要估算 CAS 基线并自动映射保底录用倾向。
- 强制 2+2+1 数量及反复询问已经给出的偏好。

### journal-research-plugins

按学科和中英文投稿路线组合候选发现、身份核验、指标调查和社区证据。 [源仓库](https://github.com/kkunkunya/journal-research-agent-plugins/tree/d902e4cb07443f079cbb5085f2de2820a1a09f79)。

| 上游模块或子模式 | 统一能力 ID | 整合方式与能力边界 |
|---|---|---|
| [journal-research-orchestrator](https://github.com/kkunkunya/journal-research-agent-plugins/blob/d902e4cb07443f079cbb5085f2de2820a1a09f79/plugins/journal-research-en/skills/journal-research-orchestrator/SKILL.md) | `intake`、`field-map`、`state-map` | **宿主工作流**：合并中英文路线，候选发现、核验和风险分析保持独立。 |
| [ai-journal-match](https://github.com/kkunkunya/journal-research-agent-plugins/blob/d902e4cb07443f079cbb5085f2de2820a1a09f79/plugins/journal-research-en/skills/ai-journal-match/SKILL.md) | `venue-discovery` | **依赖外部工具**：生医可选 JANE；出版社 Finder 按当前可用接口人工或工具辅助核验。 |
| [openalex-explore](https://github.com/kkunkunya/journal-research-agent-plugins/blob/d902e4cb07443f079cbb5085f2de2820a1a09f79/plugins/journal-research-en/skills/openalex-explore/SKILL.md) | `paper-search` | **依赖外部工具**：检索论文后聚合期刊；OpenAlex 记录不等于 SCIE 证明。 |
| [crossref-validator](https://github.com/kkunkunya/journal-research-agent-plugins/blob/d902e4cb07443f079cbb5085f2de2820a1a09f79/plugins/journal-research-en/skills/crossref-validator/SKILL.md) | `identifier-check`、`venue-identity` | **依赖外部工具**：用 DOI/ISSN 与标题交叉核验注册元数据。 |
| [dblp-cs-explore](https://github.com/kkunkunya/journal-research-agent-plugins/blob/d902e4cb07443f079cbb5085f2de2820a1a09f79/plugins/journal-research-en/skills/dblp-cs-explore/SKILL.md) | `paper-search`、`venue-discovery` | **依赖外部工具**：对 CS 论文和 venue 补召回，明确期刊与会议类别。 |
| [bison-oa-explore](https://github.com/kkunkunya/journal-research-agent-plugins/blob/d902e4cb07443f079cbb5085f2de2820a1a09f79/plugins/journal-research-en/skills/bison-oa-explore/SKILL.md) | `venue-discovery`、`costs-timelines` | **依赖外部工具**：OA 候选建议仍需逐刊核实费用、范围与投稿渠道。 |
| [arxiv-preprint-explore](https://github.com/kkunkunya/journal-research-agent-plugins/blob/d902e4cb07443f079cbb5085f2de2820a1a09f79/plugins/journal-research-en/skills/arxiv-preprint-explore/SKILL.md) | `identifier-check`、`paper-search` | **依赖外部工具**：追踪预印本到正式出版物；arXiv 本身不是期刊。 |
| [google-scholar-explore](https://github.com/kkunkunya/journal-research-agent-plugins/blob/d902e4cb07443f079cbb5085f2de2820a1a09f79/plugins/journal-research-en/skills/google-scholar-explore/SKILL.md) | `paper-search` | **依赖外部工具**：作为合法可访问时的补充召回；不宣称穷尽。 |
| [letpub-sci-journal-review](https://github.com/kkunkunya/journal-research-agent-plugins/blob/d902e4cb07443f079cbb5085f2de2820a1a09f79/plugins/journal-research-en/skills/letpub-sci-journal-review/SKILL.md) | `journal-dossier`、`costs-timelines` | **依赖外部工具**：经验时间与录用比例标明社区样本和日期，官方字段另核。 |
| [journal-authority-check](https://github.com/kkunkunya/journal-research-agent-plugins/blob/d902e4cb07443f079cbb5085f2de2820a1a09f79/plugins/journal-research-en/skills/journal-authority-check/SKILL.md) | `indexing-metrics` | **宿主工作流**：按字段向其权威来源核查，并保留未核验状态。 |
| [predatory-risk-check](https://github.com/kkunkunya/journal-research-agent-plugins/blob/d902e4cb07443f079cbb5085f2de2820a1a09f79/plugins/journal-research-en/skills/predatory-risk-check/SKILL.md) | `journal-integrity` | **宿主工作流**：检查身份、透明度、撤销收录和明确警示；输出有依据的风险线索。 |
| [cn-orchestrator](https://github.com/kkunkunya/journal-research-agent-plugins/blob/d902e4cb07443f079cbb5085f2de2820a1a09f79/plugins/journal-research-cn/skills/cn-orchestrator/SKILL.md) | `regional-indexing`、`venue-discovery` | **宿主工作流**：根据语言、机构目录、学科与文章类型选中文路线。 |
| [cn-discover-by-catalog](https://github.com/kkunkunya/journal-research-agent-plugins/blob/d902e4cb07443f079cbb5085f2de2820a1a09f79/plugins/journal-research-cn/skills/cn-discover-by-catalog/SKILL.md) | `regional-indexing`、`indexing-metrics` | **依赖外部工具**：读取用户可合法使用的当前目录并保留版本。 |
| [cn-discover-by-paper](https://github.com/kkunkunya/journal-research-agent-plugins/blob/d902e4cb07443f079cbb5085f2de2820a1a09f79/plugins/journal-research-cn/skills/cn-discover-by-paper/SKILL.md) | `regional-indexing`、`paper-search` | **依赖外部工具**：中文论文反推候选期刊，频次不等于录用率。 |
| [easyscholar-rank](https://github.com/kkunkunya/journal-research-agent-plugins/blob/d902e4cb07443f079cbb5085f2de2820a1a09f79/plugins/journal-research-cn/skills/easyscholar-rank/SKILL.md) | `indexing-metrics` | **依赖外部工具**：聚合标签仅作线索，官方目录和年份优先。 |
| [muchong-cn-journal-review](https://github.com/kkunkunya/journal-research-agent-plugins/blob/d902e4cb07443f079cbb5085f2de2820a1a09f79/plugins/journal-research-cn/skills/muchong-cn-journal-review/SKILL.md) | `regional-indexing`、`costs-timelines` | **依赖外部工具**：社区评价与官方规则分栏。 |
| [nppa-validator](https://github.com/kkunkunya/journal-research-agent-plugins/blob/d902e4cb07443f079cbb5085f2de2820a1a09f79/plugins/journal-research-cn/skills/nppa-validator/SKILL.md) | `regional-indexing`、`venue-identity` | **依赖外部工具**：按需核验 CN 号及主办信息；验证码或权限阻塞时给人工核验入口。 |

未采用或调整：

- 把 LetPub 或 easyScholar 转述当成当前官方收录证明。
- 因不在 DOAJ、APC 高低或年发文量直接判定掠夺性。
- 固化某年度目录、CAS 停更说法、抓取层级、密钥位置或必填 2+2+1。
- 把 JANE 之外尚未实现的 publisher adapter 当成已完成能力。

### sci-select

独立的相似论文与专科期刊召回、稿件画像、已知期刊查询及 Quick/Full 投稿要求核对。 [源仓库](https://github.com/keros68/xiaoyu-skill/tree/d8b26a741beae6d474db08f9fe8bc857f0490a95)。

| 上游模块或子模式 | 统一能力 ID | 整合方式与能力边界 |
|---|---|---|
| [sci-select](https://github.com/keros68/xiaoyu-skill/blob/d8b26a741beae6d474db08f9fe8bc857f0490a95/skills/sci-select/SKILL.md) | `venue-discovery`、`manuscript-profile`、`submission-plan` | **宿主工作流**：保留稿件指纹、独立召回、按发文量校正的先例解释及来源状态。 |
| [sci-select:known-journal-lookup](https://github.com/keros68/xiaoyu-skill/blob/d8b26a741beae6d474db08f9fe8bc857f0490a95/skills/sci-select/SKILL.md) | `journal-dossier` | **宿主工作流**：只查已知期刊所需字段，不强迫重新推荐。 |
| [sci-select:presubmission-check](https://github.com/keros68/xiaoyu-skill/blob/d8b26a741beae6d474db08f9fe8bc857f0490a95/skills/sci-select/SKILL.md) | `submission-preflight` | **宿主工作流**：分轻量硬性检查与用户要求的完整同刊分析；未读取规则不声称已满足。 |
| [sci-select:index-and-benchmark-maintenance](https://github.com/keros68/xiaoyu-skill/blob/d8b26a741beae6d474db08f9fe8bc857f0490a95/skills/sci-select/SKILL.md) | `state-map`、`indexing-metrics` | **宿主工作流**：数据需授权、记录版本与缺失；人工独立标签完成前不报告推荐准确率。 |

未采用或调整：

- 继承旧索引中的时间敏感值或受限制数据。
- 因关键字段缺失而静默删除候选。
- 把客观分区或适配度改写为投稿安全性。

### chinese-research-latex

单刊官方要求及社区调查，以及分阶段候选筛选。 [源仓库](https://github.com/huangwb8/ChineseResearchLaTeX/tree/d288ea832e4b2ffca5a0cca97576d3413391a342)。

| 上游模块或子模式 | 统一能力 ID | 整合方式与能力边界 |
|---|---|---|
| [paper-know-journal](https://github.com/huangwb8/ChineseResearchLaTeX/blob/d288ea832e4b2ffca5a0cca97576d3413391a342/skills/paper-know-journal/SKILL.md) | `journal-dossier` | **宿主工作流**：调查文章类型、作者指南、费用路径、周转定义、图表和数据代码政策。 |
| [paper-select-journal](https://github.com/huangwb8/ChineseResearchLaTeX/blob/d288ea832e4b2ffca5a0cca97576d3413391a342/skills/paper-select-journal/SKILL.md) | `venue-discovery`、`manuscript-profile`、`submission-plan` | **宿主工作流**：保留画像→候选→核验的分阶段收敛，使用领域数据库和可配置时间窗口。 |

未采用或调整：

- 固定 2023IF.xlsx、IF 小于 3 的通用排除规则。
- 把 PubMed 近三个月作为所有学科必经检索。
- 强制隐藏目录、特定作者 bug 上报流程及模板默认值。

### journal-fit-finder

全文或摘要适配度、语言/地区/索引路由、出版社多样性及改写定位建议。 [源仓库](https://github.com/hztopcu/journal-fit-finder/tree/2624d0b40a444951157c626c01bda73c65c60b23)。

| 上游模块或子模式 | 统一能力 ID | 整合方式与能力边界 |
|---|---|---|
| [journal-fit-finder](https://github.com/hztopcu/journal-fit-finder/blob/2624d0b40a444951157c626c01bda73c65c60b23/journal-fit-finder/SKILL.md) | `fit-comparison`、`submission-plan` | **宿主工作流**：用户语言优先；土耳其、拉美、亚洲等地区资源仅在相关时加载；所有评分注明推断。 |

未采用或调整：

- 从地区或指标推断个人录用率。
- 把第三方网站存在等同官方索引或期刊合法性。

### polish-skill

从文献笔记、问题驱动综述和新意审计，到论证、实验审计、选刊、润色及回复。 [源仓库](https://github.com/yujie-jason-zhang/polish_skill/tree/9b2a86ca6ac88879a3d3490fecdb909673fd1562)。

| 上游模块或子模式 | 统一能力 ID | 整合方式与能力边界 |
|---|---|---|
| [read-paper-to-notes](https://github.com/yujie-jason-zhang/polish_skill/blob/9b2a86ca6ac88879a3d3490fecdb909673fd1562/read-paper-to-notes/SKILL.md) | `paper-notes` | **宿主工作流**：区分作者报告、证据位置、阅读者推断与未知。 |
| [idea-novelty-auditor](https://github.com/yujie-jason-zhang/polish_skill/blob/9b2a86ca6ac88879a3d3490fecdb909673fd1562/idea-novelty-auditor/SKILL.md) | `novelty-audit` | **宿主工作流**：新意相对已检索文献，保留检索范围与最接近工作。 |
| [problem-driven-literature-review](https://github.com/yujie-jason-zhang/polish_skill/blob/9b2a86ca6ac88879a3d3490fecdb909673fd1562/problem-driven-literature-review/SKILL.md) | `evidence-review` | **宿主工作流**：围绕问题、方法类别、证据与争议组织综述。 |
| [paper-argument-reconstructor](https://github.com/yujie-jason-zhang/polish_skill/blob/9b2a86ca6ac88879a3d3490fecdb909673fd1562/paper-argument-reconstructor/SKILL.md) | `argument-audit`、`manuscript-writing` | **宿主工作流**：把贡献、论据、实验和段落目的连成可追溯论证。 |
| [experiment-section-auditor](https://github.com/yujie-jason-zhang/polish_skill/blob/9b2a86ca6ac88879a3d3490fecdb909673fd1562/experiment-section-auditor/SKILL.md) | `argument-audit`、`experiment-plan` | **宿主工作流**：对已有计划提最小必要补证，不捏造实验或可用资源。 |
| [journal-recommender](https://github.com/yujie-jason-zhang/polish_skill/blob/9b2a86ca6ac88879a3d3490fecdb909673fd1562/journal-recommender/SKILL.md) | `venue-discovery`、`manuscript-profile`、`submission-plan` | **宿主工作流**：新生成和仅核验模式分开，保留原候选及差异记录。 |
| [paper-polisher](https://github.com/yujie-jason-zhang/polish_skill/blob/9b2a86ca6ac88879a3d3490fecdb909673fd1562/paper-polisher/SKILL.md) | `manuscript-writing` | **宿主工作流**：保护数字、引用、术语和 TeX 结构，报告未确定含义。 |
| [paper-cover-letter](https://github.com/yujie-jason-zhang/polish_skill/blob/9b2a86ca6ac88879a3d3490fecdb909673fd1562/paper-cover-letter/SKILL.md) | `cover-letter` | **宿主工作流**：用真实贡献、期刊匹配与已确认声明写初投稿信。 |
| [paper-response-to-reviewers](https://github.com/yujie-jason-zhang/polish_skill/blob/9b2a86ca6ac88879a3d3490fecdb909673fd1562/paper-response-to-reviewers/SKILL.md) | `revision-response` | **宿主工作流**：逐条回复并关联修订位置；不同意时说明证据。 |

未采用或调整：

- 四组各约十本的强制膨胀、任何主张更易录用的安全档保证。
- 将 LetPub 简体中文特定站点作为所有学科完成工作的前提。
- 正文语言修改时扩写未经证实的科学结论。

### academic-publishing-skills

覆盖选刊、初投稿、修订、校样和发表后材料的 18 个模块。 [源仓库](https://github.com/yaotingsun/academic-publishing-skills/tree/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e)。

| 上游模块或子模式 | 统一能力 ID | 整合方式与能力边界 |
|---|---|---|
| [journal-selector](https://github.com/yaotingsun/academic-publishing-skills/blob/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e/plugins/journal-selector/skills/journal-selector/SKILL.md) | `fit-comparison`、`submission-plan` | **宿主工作流**：适配、客观指标、成本和证据完整性分开。 |
| [presubmission-inquiry](https://github.com/yaotingsun/academic-publishing-skills/blob/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e/plugins/presubmission-inquiry/skills/presubmission-inquiry/SKILL.md) | `presubmission-inquiry` | **宿主工作流**：先核实是否接受预询问及正确渠道，仅生成可审阅草稿。 |
| [journal-reformatter](https://github.com/yaotingsun/academic-publishing-skills/blob/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e/plugins/journal-reformatter/skills/journal-reformatter/SKILL.md) | `venue-formatting` | **宿主工作流**：遵循目标当前阶段指南；不改动科学含义。 |
| [manuscript-copyeditor](https://github.com/yaotingsun/academic-publishing-skills/blob/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e/plugins/manuscript-copyeditor/skills/manuscript-copyeditor/SKILL.md) | `manuscript-writing` | **宿主工作流**：语言与排版修订独立于方法和结构评议。 |
| [citation-auditor](https://github.com/yaotingsun/academic-publishing-skills/blob/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e/plugins/citation-auditor/skills/citation-auditor/SKILL.md) | `citation-audit` | **宿主工作流**：分别找支持文献和核验已有引用；纳入相反证据与撤稿状态。 |
| [reviewer-recommender](https://github.com/yaotingsun/academic-publishing-skills/blob/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e/plugins/reviewer-recommender/skills/reviewer-recommender/SKILL.md) | `reviewer-discovery` | **宿主工作流**：从相关论文定位专家并查利益冲突；身份与联系方式必须核验。 |
| [authorship-credit](https://github.com/yaotingsun/academic-publishing-skills/blob/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e/plugins/authorship-credit/skills/authorship-credit/SKILL.md) | `authorship-credit` | **宿主工作流**：整理贡献与适用规范，实际署名顺序和批准由作者决定。 |
| [cover-letter-writer](https://github.com/yaotingsun/academic-publishing-skills/blob/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e/plugins/cover-letter-writer/skills/cover-letter-writer/SKILL.md) | `cover-letter` | **宿主工作流**：不伪造伦理、原创性、全体作者批准或数据链接。 |
| [submission-screener](https://github.com/yaotingsun/academic-publishing-skills/blob/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e/plugins/submission-screener/skills/submission-screener/SKILL.md) | `submission-preflight` | **宿主工作流**：核对数字、文件、声明与目标指南；按证据指出缺项。 |
| [statistical-rigor-helper](https://github.com/yaotingsun/academic-publishing-skills/blob/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e/plugins/statistical-rigor-helper/skills/statistical-rigor-helper/SKILL.md) | `statistics-robustness`、`experiment-plan` | **宿主工作流**：按实际设计选择统计框架并检查泄漏、混杂和伪重复。 |
| [figure-checker](https://github.com/yaotingsun/academic-publishing-skills/blob/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e/plugins/figure-checker/skills/figure-checker/SKILL.md) | `figure-table-audit` | **宿主工作流**：需要原图和源数据才可核验图值，不做无依据不端指控。 |
| [table-checker](https://github.com/yaotingsun/academic-publishing-skills/blob/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e/plugins/table-checker/skills/table-checker/SKILL.md) | `figure-table-audit` | **宿主工作流**：检查单位、精度、合计、注释及报告一致性。 |
| [review-simulator](https://github.com/yaotingsun/academic-publishing-skills/blob/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e/plugins/review-simulator/skills/review-simulator/SKILL.md) | `peer-review` | **宿主工作流**：模拟不同角色的建设性意见，显式标注非独立人类评审。 |
| [journal-submission-checklist](https://github.com/yaotingsun/academic-publishing-skills/blob/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e/plugins/journal-submission-checklist/skills/journal-submission-checklist/SKILL.md) | `submission-preflight` | **宿主工作流**：按研究设计和目标要求选 PRISMA/CONSORT/STROBE/ARRIVE 等适用清单。 |
| [revision-responder](https://github.com/yaotingsun/academic-publishing-skills/blob/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e/plugins/revision-responder/skills/revision-responder/SKILL.md) | `revision-response` | **宿主工作流**：草拟、审计或有证据的申诉三种模式，记录每条修订。 |
| [proof-checker](https://github.com/yaotingsun/academic-publishing-skills/blob/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e/plugins/proof-checker/skills/proof-checker/SKILL.md) | `proof-check` | **宿主工作流**：以已接收版本为基线核对校样、作者查询、图表和补充件。 |
| [research-disseminator](https://github.com/yaotingsun/academic-publishing-skills/blob/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e/plugins/research-disseminator/skills/research-disseminator/SKILL.md) | `dissemination` | **宿主工作流**：写忠于论文的公众摘要、图形摘要方案及平台草稿。 |
| [post-publication-corrector](https://github.com/yaotingsun/academic-publishing-skills/blob/3103f4d7d4a97fc3bf80a61ce4cb04dd21d4d88e/plugins/post-publication-corrector/skills/post-publication-corrector/SKILL.md) | `postpublication-correction` | **宿主工作流**：对已确认错误整理更正材料；通知类别与最终处理依期刊政策和编辑决定。 |

未采用或调整：

- 无论用户语言都强制英文。
- 以生物医学证据规则作为所有研究领域的硬门槛。
- 把历史录用比例分桶后当作稿件被录用机会。
- 模拟评审中的录用结论被误写为真实编辑决定。

### superpapers

可复现研究到论文编译的阶段流程，配合选刊和作者指南模块。 [源仓库](https://github.com/regisely/superpapers/tree/805a9a7369d57f01b67732645175ad0b7a8a3f23)。

| 上游模块或子模式 | 统一能力 ID | 整合方式与能力边界 |
|---|---|---|
| [academic-baseline](https://github.com/regisely/superpapers/blob/805a9a7369d57f01b67732645175ad0b7a8a3f23/skills/academic-baseline/SKILL.md) | `intake`、`field-map` | **宿主工作流**：记录问题、材料、假设和可用资源。 |
| [replication-driven-research](https://github.com/regisely/superpapers/blob/805a9a7369d57f01b67732645175ad0b7a8a3f23/skills/replication-driven-research/SKILL.md) | `hypothesis-plan`、`experiment-plan` | **宿主工作流**：先复现最近工作，再确定可检验差异。 |
| [brainstorm](https://github.com/regisely/superpapers/blob/805a9a7369d57f01b67732645175ad0b7a8a3f23/skills/brainstorm/SKILL.md) | `hypothesis-plan` | **宿主工作流**：列候选问题、否证方法和可行性，不声称已证明新颖。 |
| [write-plan](https://github.com/regisely/superpapers/blob/805a9a7369d57f01b67732645175ad0b7a8a3f23/skills/write-plan/SKILL.md) | `hypothesis-plan`、`experiment-plan` | **宿主工作流**：安排依赖、实验、交付物和停止条件。 |
| [execute-plan](https://github.com/regisely/superpapers/blob/805a9a7369d57f01b67732645175ad0b7a8a3f23/skills/execute-plan/SKILL.md) | `implementation` | **宿主工作流**：按已有授权执行可逆步骤，保存实际运行记录。 |
| [literature-search](https://github.com/regisely/superpapers/blob/805a9a7369d57f01b67732645175ad0b7a8a3f23/skills/literature-search/SKILL.md) | `paper-search`、`search-protocol` | **宿主工作流**：多来源检索、筛选、去重和检索式记录。 |
| [citation-management](https://github.com/regisely/superpapers/blob/805a9a7369d57f01b67732645175ad0b7a8a3f23/skills/citation-management/SKILL.md) | `identifier-check`、`citation-audit` | **宿主工作流**：规范 DOI、BibTeX、版本关系与引用位置。 |
| [data-collection](https://github.com/regisely/superpapers/blob/805a9a7369d57f01b67732645175ad0b7a8a3f23/skills/data-collection/SKILL.md) | `data-collection` | **宿主工作流**：记录数据许可、抽样、清洗、版本和排除条件。 |
| [statistical-modeling](https://github.com/regisely/superpapers/blob/805a9a7369d57f01b67732645175ad0b7a8a3f23/skills/statistical-modeling/SKILL.md) | `statistics-robustness` | **宿主工作流**：分析代码和结果需实际运行；不能通过文字模拟。 |
| [robustness-checks](https://github.com/regisely/superpapers/blob/805a9a7369d57f01b67732645175ad0b7a8a3f23/skills/robustness-checks/SKILL.md) | `statistics-robustness` | **宿主工作流**：检查敏感性、替代解释、规格变化和负向结果。 |
| [paper-writing](https://github.com/regisely/superpapers/blob/805a9a7369d57f01b67732645175ad0b7a8a3f23/skills/paper-writing/SKILL.md) | `argument-audit`、`manuscript-writing` | **宿主工作流**：以已完成证据撰写方法、结果和讨论。 |
| [paper-review](https://github.com/regisely/superpapers/blob/805a9a7369d57f01b67732645175ad0b7a8a3f23/skills/paper-review/SKILL.md) | `peer-review` | **宿主工作流**：按主张与证据给修改建议。 |
| [tables-and-figures](https://github.com/regisely/superpapers/blob/805a9a7369d57f01b67732645175ad0b7a8a3f23/skills/tables-and-figures/SKILL.md) | `figure-table-audit`、`manuscript-writing` | **宿主工作流**：精确图表来自真实数据或确定性绘图工具。 |
| [compile-latex](https://github.com/regisely/superpapers/blob/805a9a7369d57f01b67732645175ad0b7a8a3f23/skills/compile-latex/SKILL.md) | `venue-formatting` | **依赖外部工具**：依赖本机 LaTeX/Pandoc 等实际安装并检查编译输出。 |
| [journal-selection](https://github.com/regisely/superpapers/blob/805a9a7369d57f01b67732645175ad0b7a8a3f23/skills/journal-selection/SKILL.md) | `venue-discovery`、`manuscript-profile`、`submission-plan` | **宿主工作流**：按学科选择候选，保持顺序为策略而非概率。 |
| [journal-guidelines](https://github.com/regisely/superpapers/blob/805a9a7369d57f01b67732645175ad0b7a8a3f23/skills/journal-guidelines/SKILL.md) | `journal-dossier` | **宿主工作流**：记录目标文章类型和提交阶段的当前官方规则。 |

未采用或调整：

- 每个可逆阶段结束都强制等待批准。
- 把经济学或实证研究模板施加到所有领域。
- 将固定目标期刊格式绑定研究问题。

### researcher

细分的研究检索、证据收敛、实验实现、论文产出与长期更新工作流。 [源仓库](https://github.com/sokolmarek/researcher/tree/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945)。

| 上游模块或子模式 | 统一能力 ID | 整合方式与能力边界 |
|---|---|---|
| [brainstorming](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/brainstorming/SKILL.md) | `hypothesis-plan` | **宿主工作流**：候选想法与查证后的研究空白分开。 |
| [citation-audit](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/citation-audit/SKILL.md) | `citation-audit` | **宿主工作流**：检查出处、位置、版本、支持力度和遗漏。 |
| [citation-context](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/citation-context/SKILL.md) | `paper-notes`、`citation-audit` | **宿主工作流**：区分引用是支持、反驳还是背景，并读取上下文。 |
| [citation-management](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/citation-management/SKILL.md) | `identifier-check`、`citation-audit` | **宿主工作流**：管理引用元数据和稳定引用键。 |
| [code-analysis](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/code-analysis/SKILL.md) | `implementation`、`agent-systems` | **宿主工作流**：审阅已有代码与论文主张、数据流程和依赖一致性。 |
| [conference-finder](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/conference-finder/SKILL.md) | `venue-discovery` | **宿主工作流**：仅在允许会议时启用，并明确非 SCI 期刊。 |
| [contradiction-detection](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/contradiction-detection/SKILL.md) | `evidence-review` | **宿主工作流**：保留定义、设定和证据冲突，不强迫综合为共识。 |
| [cover-letter](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/cover-letter/SKILL.md) | `cover-letter` | **宿主工作流**：写初投引介信，和修回逐条回复分开。 |
| [experiment-design](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/experiment-design/SKILL.md) | `experiment-plan` | **宿主工作流**：定义变量、比较组、单位、评价和否证条件。 |
| [extraction-tables](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/extraction-tables/SKILL.md) | `paper-notes`、`evidence-review` | **宿主工作流**：每个抽取单元带来源位置和无法评估状态。 |
| [fact-checking](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/fact-checking/SKILL.md) | `citation-audit`、`argument-audit` | **宿主工作流**：寻找支持和反驳单个具体主张的证据。 |
| [figure-suggestions](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/figure-suggestions/SKILL.md) | `figure-table-audit` | **宿主工作流**：按论证目标设计图表类型、分面和图注。 |
| [image-prompt-crafting](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/image-prompt-crafting/SKILL.md) | `dissemination` | **依赖外部工具**：仅用于概念说明和封面；不可生成测量结果图。 |
| [implementation](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/implementation/SKILL.md) | `implementation` | **宿主工作流**：使用可用编程工具构建与运行基线、训练或评估；资源不足写阻塞。 |
| [journal-finder](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/journal-finder/SKILL.md) | `venue-discovery`、`manuscript-profile`、`submission-plan` | **宿主工作流**：保留范围、费用和证据匹配，删除模板假指标。 |
| [journal-formatting](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/journal-formatting/SKILL.md) | `venue-formatting` | **宿主工作流**：格式和期刊选择分开，当前官方指南覆盖旧配置。 |
| [latex-tables](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/latex-tables/SKILL.md) | `figure-table-audit`、`manuscript-writing` | **依赖外部工具**：从给定或已核实数据生成 LaTeX 表格。 |
| [literature-monitoring](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/literature-monitoring/SKILL.md) | `state-map`、`search-protocol` | **宿主工作流**：复用保存检索式、游标和见过的记录；定时执行需真实调度器。 |
| [literature-search](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/literature-search/SKILL.md) | `paper-search`、`search-protocol` | **宿主工作流**：按领域数据库组合检索。 |
| [manuscript-setup](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/manuscript-setup/SKILL.md) | `state-map` | **宿主工作流**：初始化后非破坏性恢复项目、证据和决策。 |
| [paper-drafting](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/paper-drafting/SKILL.md) | `argument-audit`、`manuscript-writing` | **宿主工作流**：缺失数据留空或标记，不生成虚构结果。 |
| [peer-review](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/peer-review/SKILL.md) | `peer-review` | **宿主工作流**：分角色审稿建议是模拟，无法证明专家一致同意。 |
| [plotneuralnet](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/plotneuralnet/SKILL.md) | `agent-systems`、`figure-table-audit` | **依赖外部工具**：按真实模型结构绘图，绘图库需独立安装。 |
| [research-convergence](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/research-convergence/SKILL.md) | `evidence-review`、`field-map` | **宿主工作流**：把一致、分歧与结论适用范围做成可追溯地图。 |
| [research-gaps](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/research-gaps/SKILL.md) | `novelty-audit`、`hypothesis-plan` | **宿主工作流**：区分未检索到、缺少证据、未解决以及可实施。 |
| [research-pipeline](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/research-pipeline/SKILL.md) | `intake`、`field-map`、`state-map` | **宿主工作流**：保存阶段状态，复用已有授权，不强迫全部阶段运行。 |
| [response-to-reviewers](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/response-to-reviewers/SKILL.md) | `revision-response` | **宿主工作流**：逐条关联评审意见、修改与理由。 |
| [revision-management](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/revision-management/SKILL.md) | `revision-response`、`state-map` | **宿主工作流**：保存版本、变更位置及已解决/待解决状态。 |
| [sota-finder](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/sota-finder/SKILL.md) | `agent-capabilities`、`agent-systems`、`evidence-review` | **宿主工作流**：指标带数据集版本、拆分、预算、日期和来源。 |
| [statistical-analysis](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/statistical-analysis/SKILL.md) | `statistics-robustness` | **宿主工作流**：方法选择、效应量、区间及元分析需要实际数据和工具。 |
| [systematic-review](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/systematic-review/SKILL.md) | `search-protocol`、`evidence-review` | **宿主工作流**：保存协议与筛选账本；人类独立双筛需真实参与，模型分身不冒充。 |
| [tikz-diagrams](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/tikz-diagrams/SKILL.md) | `agent-systems`、`figure-table-audit` | **依赖外部工具**：用代码表达流程和系统结构；必要时编译核验。 |
| [visualization](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/visualization/SKILL.md) | `figure-table-audit`、`manuscript-writing` | **依赖外部工具**：从真实表格生成可复现数据图。 |
| [word-output](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/word-output/SKILL.md) | `venue-formatting` | **依赖外部工具**：按宿主可用文档能力导出并核验，不继承未实现的格式能力。 |
| [writing-style-analysis](https://github.com/sokolmarek/researcher/blob/e4ddbf4eb8a93565a222c48797ed3e0dc6cf0945/skills/writing-style-analysis/SKILL.md) | `manuscript-writing` | **宿主工作流**：只迁移风格，保留新稿事实和科学结论。 |

未采用或调整：

- 模板中的具体期刊 IF、出版商、录用率数值作为真实数据。
- 把未实现的 Word 富内容或外部多模型评审写成现成能力。
- 固定模型供应商、自动人类共识、每阶段停等或个人能力评分。

### scientific-agent-skills

科研信息检索、综述、审稿、模板、引用、方法批判与发展性反馈。 [源仓库](https://github.com/K-Dense-AI/scientific-agent-skills/tree/593377bb048752abb0152deab9fbb1083a6087df)。

| 上游模块或子模式 | 统一能力 ID | 整合方式与能力边界 |
|---|---|---|
| [paper-lookup](https://github.com/K-Dense-AI/scientific-agent-skills/blob/593377bb048752abb0152deab9fbb1083a6087df/skills/paper-lookup/SKILL.md) | `paper-search` | **依赖外部工具**：保留 18 类来源用途与来源记录；按宿主可用 API、连接器或合法检索实际调用。 |
| [literature-review](https://github.com/K-Dense-AI/scientific-agent-skills/blob/593377bb048752abb0152deab9fbb1083a6087df/skills/literature-review/SKILL.md) | `search-protocol`、`evidence-review` | **宿主工作流**：区分系统性/范围/叙述综述、记录与研究；元分析另需数据与运行环境。 |
| [peer-review](https://github.com/K-Dense-AI/scientific-agent-skills/blob/593377bb048752abb0152deab9fbb1083a6087df/skills/peer-review/SKILL.md) | `peer-review` | **宿主工作流**：建立受证据约束的评审草稿，尊重已存在的访问授权和适用保密规则。 |
| [venue-templates](https://github.com/K-Dense-AI/scientific-agent-skills/blob/593377bb048752abb0152deab9fbb1083a6087df/skills/venue-templates/SKILL.md) | `venue-formatting` | **宿主工作流**：当前作者指南与提交阶段优先于模板默认。 |
| [citation-management](https://github.com/K-Dense-AI/scientific-agent-skills/blob/593377bb048752abb0152deab9fbb1083a6087df/skills/citation-management/SKILL.md) | `identifier-check`、`citation-audit` | **宿主工作流**：检索并核验参考文献元数据、DOI 和引用格式。 |
| [scientific-critical-thinking](https://github.com/K-Dense-AI/scientific-agent-skills/blob/593377bb048752abb0152deab9fbb1083a6087df/skills/scientific-critical-thinking/SKILL.md) | `peer-review`、`statistics-robustness` | **宿主工作流**：按实验单位、混杂、偏差、因果范围与效应不确定性审查。 |
| [scholar-evaluation](https://github.com/K-Dense-AI/scientific-agent-skills/blob/593377bb048752abb0152deab9fbb1083a6087df/skills/scholar-evaluation/SKILL.md) | `peer-review` | **宿主工作流**：定性且可追溯的作品反馈；不评价人员或预测录用。 |

未采用或调整：

- 把 18 个检索 API 列表描述为 ScholarRoute 内置且全部已联通。
- 强迫所有领域使用生物医学证据分级。
- 把反馈评分转为录用、顶刊或人员能力判断。

### ai-research-skills

ML/AI 与系统论文的不同论证结构和评估要求。 [源仓库](https://github.com/Orchestra-Research/AI-Research-SKILLs/tree/773a52944ba4747a18bd4ae9ade53fff041adcbc)。

| 上游模块或子模式 | 统一能力 ID | 整合方式与能力边界 |
|---|---|---|
| [ml-paper-writing](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/20-ml-paper-writing/ml-paper-writing/SKILL.md) | `agent-capabilities`、`argument-audit`、`manuscript-writing` | **宿主工作流**：从仓库证据、最近工作和可核实结果形成 ML 论文论证。 |
| [systems-paper-writing](https://github.com/Orchestra-Research/AI-Research-SKILLs/blob/773a52944ba4747a18bd4ae9ade53fff041adcbc/20-ml-paper-writing/systems-paper-writing/SKILL.md) | `agent-systems`、`argument-audit`、`manuscript-writing` | **宿主工作流**：说明系统设计权衡、端到端性能、微基准、扩展性和替代方案。 |

未采用或调整：

- 把会议名单标记为 SCI 期刊。
- 固化提交年度、页数和会议时间。
- 宣称写作工具能替代真实实验。

### journal-atlas

把期刊编辑范围、方法倾向和实际要求作为有出处的知识，而非只看指标。 [源仓库](https://github.com/Zaious/journal-atlas/tree/574d27d84c270fc8da16df69d9bad929e5c341e0)。

| 上游模块或子模式 | 统一能力 ID | 整合方式与能力边界 |
|---|---|---|
| [journal-atlas](https://github.com/Zaious/journal-atlas/blob/574d27d84c270fc8da16df69d9bad929e5c341e0/README.md) | `journal-dossier` | **宿主工作流**：独立设计有出处的期刊画像与缺失项。 |
| [journal-atlas-contribute](https://github.com/Zaious/journal-atlas/blob/574d27d84c270fc8da16df69d9bad929e5c341e0/README.md) | `journal-dossier`、`state-map` | **宿主工作流**：按字段补充有来源的期刊知识或用户授权的经历，保留修订与核验状态；不向上游自动发布。 |

未采用或调整：

- 复制或嵌入 CC BY-SA 的期刊条目、模板、文档。
- 将不完整语义档案扩张为广泛领域覆盖或把缺失当中性值。

### journal-finder-local

人文社科与环境健康交叉期刊的本地关键词/语义索引路径。 [源仓库](https://github.com/alexishuang1901-hub/journal-finder/tree/b8fb764bc4b60acb88538e579b165bf4745b3072)。

| 上游模块或子模式 | 统一能力 ID | 整合方式与能力边界 |
|---|---|---|
| [find-journal](https://github.com/alexishuang1901-hub/journal-finder/blob/b8fb764bc4b60acb88538e579b165bf4745b3072/codex-skills/find-journal/SKILL.md) | `venue-discovery`、`paper-search` | **依赖外部工具**：可连接有权限的本地索引；没有语义模型时写明词法回退。 |
| [local-index-refresh](https://github.com/alexishuang1901-hub/journal-finder/blob/b8fb764bc4b60acb88538e579b165bf4745b3072/README.md) | `state-map`、`indexing-metrics` | **宿主工作流**：记录合法来源、版本、缺失字段和查询模型；当前值必须复核。 |

未采用或调整：

- 复制当前 JCR 白名单、JIF/CAS 受限表格或固化期刊数量。
- 以国籍或机构占比估计个人录用率。
- 把 SPECTER2/FAISS 当作无依赖内置功能。
- 硬编码原作者电脑路径。

### cn-journal-selector

中文出版身份、机构认可、费用和时间约束的组合检查。 [源仓库](https://github.com/yibeixiaobai/journal-selector/tree/b5303f35310500302e4f72381451dc6d2d433bc8)。

| 上游模块或子模式 | 统一能力 ID | 整合方式与能力边界 |
|---|---|---|
| [journal-selector](https://github.com/yibeixiaobai/journal-selector/blob/b5303f35310500302e4f72381451dc6d2d433bc8/SKILL.md) | `regional-indexing`、`venue-discovery` | **宿主工作流**：重写为机构认可与官方身份核验流程；只提供已核实官方投稿入口。 |

未采用或调整：

- 指定商业平台优先、强制导流按钮和直接采信平台报价。
- 低价、发文量或单一数据库未收录即定为不正规。
- 未验证录用率、个人身份资历推断和承诺见刊时间。

### awesome-journal-skills

按具体期刊/会议和研究领域选择作者规则与稿件定位包。 [源仓库](https://github.com/brycewang-stanford/Awesome-Journal-Skills/tree/932eb23331721b16e967c59f093781be1928b498)。

| 上游模块或子模式 | 统一能力 ID | 整合方式与能力边界 |
|---|---|---|
| [aamas-skills](https://github.com/brycewang-stanford/Awesome-Journal-Skills/blob/932eb23331721b16e967c59f093781be1928b498/.claude-plugin/marketplace.json) | `agent-capabilities`、`venue-discovery` | **宿主工作流**：Agent 与多智能体会议侧的内容和规则核验；会议路径按需。 |
| [acl-skills](https://github.com/brycewang-stanford/Awesome-Journal-Skills/blob/932eb23331721b16e967c59f093781be1928b498/.claude-plugin/marketplace.json) | `agent-capabilities`、`venue-discovery` | **宿主工作流**：NLP 评审、ARR 和提交规则需核实当前周期。 |
| [icse-skills](https://github.com/brycewang-stanford/Awesome-Journal-Skills/blob/932eb23331721b16e967c59f093781be1928b498/.claude-plugin/marketplace.json) | `agent-systems`、`venue-discovery` | **宿主工作流**：软件工程贡献与实证/工件要求，会议不满足仅期刊约束。 |
| [csj-skills](https://github.com/brycewang-stanford/Awesome-Journal-Skills/blob/932eb23331721b16e967c59f093781be1928b498/.claude-plugin/marketplace.json) | `regional-indexing`、`journal-dossier` | **宿主工作流**：仅指《计算机科学》(JSJKX)，不要扩张包的范围。 |
| [computer-science-conference-skills](https://github.com/brycewang-stanford/Awesome-Journal-Skills/blob/932eb23331721b16e967c59f093781be1928b498/.claude-plugin/marketplace.json) | `venue-discovery` | **宿主工作流**：使用领域路由思路，所有具体 venue 按当前官方规则核查。 |
| [engineering-technology-journal-skills](https://github.com/brycewang-stanford/Awesome-Journal-Skills/blob/932eb23331721b16e967c59f093781be1928b498/.claude-plugin/marketplace.json) | `journal-dossier` | **宿主工作流**：工程期刊范围、应用证据和作者要求分开核验。 |
| [discipline-breadth-and-per-journal-packs](https://github.com/brycewang-stanford/Awesome-Journal-Skills/blob/932eb23331721b16e967c59f093781be1928b498/.claude-plugin/marketplace.json) | `intake`、`field-map`、`state-map` | **宿主工作流**：按实际学科装载所需规则；不宣称整个市场包已被安装或逐文件审计。 |

未采用或调整：

- 复制庞大 venue 配置、过期年度规则或出版社模板。
- 把《计算机科学》单刊包误认为国际 CS 期刊总包。
- 把 AAMAS、ACL、ICSE 等会议算进 SCI 期刊。

### food-nutrition-skills

食品、营养与农业的领域研究流程和目标期刊作者规则路由。 [源仓库](https://github.com/PangenomeAI/academic-skills-food-nutrition/tree/01b2158a48408a8d0e56238c04075080c793d53c)。

| 上游模块或子模式 | 统一能力 ID | 整合方式与能力边界 |
|---|---|---|
| [journal-selector](https://github.com/PangenomeAI/academic-skills-food-nutrition/blob/01b2158a48408a8d0e56238c04075080c793d53c/journal-selector/SKILL.md) | `journal-dossier` | **宿主工作流**：选定食品/营养/农业期刊后映射作者要求；它在上游是共享过程。 |
| [food-research / agri-research](https://github.com/PangenomeAI/academic-skills-food-nutrition/blob/01b2158a48408a8d0e56238c04075080c793d53c/food-research/SKILL.md) | `field-map` | **宿主工作流**：在相应领域建立问题、文献与方法图谱。 |
| [food-deep-research / agri-deep-research](https://github.com/PangenomeAI/academic-skills-food-nutrition/blob/01b2158a48408a8d0e56238c04075080c793d53c/food-deep-research/SKILL.md) | `search-protocol`、`evidence-review` | **宿主工作流**：按研究设计与纳入范围组织深入综述。 |
| [food-paper / agri-paper](https://github.com/PangenomeAI/academic-skills-food-nutrition/blob/01b2158a48408a8d0e56238c04075080c793d53c/food-paper/SKILL.md) | `manuscript-writing` | **宿主工作流**：依据真实食品/农业研究证据和期刊规范写作。 |
| [food-review / agri-review](https://github.com/PangenomeAI/academic-skills-food-nutrition/blob/01b2158a48408a8d0e56238c04075080c793d53c/food-review/SKILL.md) | `peer-review`、`statistics-robustness` | **宿主工作流**：应用相应的实验、样本和报告检查。 |
| [food-pipeline / agri-pipeline](https://github.com/PangenomeAI/academic-skills-food-nutrition/blob/01b2158a48408a8d0e56238c04075080c793d53c/food-pipeline/SKILL.md) | `intake`、`field-map`、`state-map` | **宿主工作流**：共享状态和阶段编排。 |
| [food-fetch](https://github.com/PangenomeAI/academic-skills-food-nutrition/blob/01b2158a48408a8d0e56238c04075080c793d53c/food-fetch/SKILL.md) | `paper-search` | **依赖外部工具**：只读取有权访问的文献和数据。 |
| [food-figure](https://github.com/PangenomeAI/academic-skills-food-nutrition/blob/01b2158a48408a8d0e56238c04075080c793d53c/food-figure/SKILL.md) | `figure-table-audit`、`manuscript-writing` | **依赖外部工具**：真实数据图和概念插图分开。 |
| [food-proposal](https://github.com/PangenomeAI/academic-skills-food-nutrition/blob/01b2158a48408a8d0e56238c04075080c793d53c/food-proposal/SKILL.md) | `hypothesis-plan`、`manuscript-writing` | **宿主工作流**：写问题、设计、资源和里程碑，不生成不存在的初步结果。 |
| [food-ppt / agri-ppt](https://github.com/PangenomeAI/academic-skills-food-nutrition/blob/01b2158a48408a8d0e56238c04075080c793d53c/food-ppt/SKILL.md) | `dissemination`、`manuscript-writing` | **依赖外部工具**：需要宿主幻灯片生成和渲染工具。 |

未采用或调整：

- 复制期刊规则数据库或把旧覆盖数量当当前有效规则。
- 让食品领域模板决定 Agent/软件论文的研究设计。
- 把编排说明称为内置训练、实验或图像生成引擎。
- 按期刊分区机械排除 Q4 文献；证据综述按研究本身和协议纳入，不能把期刊声望当研究质量。

### longtable

跨会话研究状态、证据谱系、明确分歧、同行讨论和可验证研究包。 [源仓库](https://github.com/HosungYou/LongTable/tree/eed627a85f0db7ea218beb56c61fde36c975a4e4)。

| 上游模块或子模式 | 统一能力 ID | 整合方式与能力边界 |
|---|---|---|
| [longtable-start](https://github.com/HosungYou/LongTable/blob/eed627a85f0db7ea218beb56c61fde36c975a4e4/README.md) | `state-map` | **宿主工作流**：保存研究问题、决策依据、未决项和当前状态。 |
| [longtable-interview](https://github.com/HosungYou/LongTable/blob/eed627a85f0db7ea218beb56c61fde36c975a4e4/README.md) | `hypothesis-plan` | **宿主工作流**：将张力转换为需要证据回答的具体问题，已清晰输入无需重复访谈。 |
| [longtable-reviewer / panel](https://github.com/HosungYou/LongTable/blob/eed627a85f0db7ea218beb56c61fde36c975a4e4/README.md) | `peer-review` | **宿主工作流**：保留各角色分歧与合成依据；真实上游 panel 工具未嵌入。 |
| [venue-search-and-journal-profiles](https://github.com/HosungYou/LongTable/blob/eed627a85f0db7ea218beb56c61fde36c975a4e4/README.md) | `journal-dossier` | **宿主工作流**：把范围、指南与同刊文章形式构成可审计的目标档案。 |
| [durable-checkpoints-and-evidence-package](https://github.com/HosungYou/LongTable/blob/eed627a85f0db7ea218beb56c61fde36c975a4e4/README.md) | `state-map` | **宿主工作流**：独立实现本项目的日志和引用关系，外部传输需另行连接。 |

未采用或调整：

- 复制 Node/TypeScript CLI、provider hooks 或 MCP 并宣称内嵌。
- 强制单问题访谈节奏和所有阶段人工阻断。
- 把模型角色分工当作独立人类评审。

## 冲突处理摘要

完整执行规则由技能的冲突说明维护。这里保留与来源直接相关的主要决定。

| 冲突 | ScholarRoute 的统一处理 |
|---|---|
| 摘要估算“档次”并自动推荐“保底” vs. sci-select 不评科研质量、不预测录用 | 分开呈现适配证据、稿件缺口、客观分区、实践成本；可建议投稿顺序，但不能生成个人录用概率。 |
| 多个模块都叫 journal-selector/recommender，任务不同 | 用能力 ID 与领域/阶段路由；分清候选发现、单刊查询、作者规则加载和已有名单核验。 |
| 先选刊再研究 vs. 从问题和文献出发 | 早期检查潜在出版要求，问题和方法由研究目标决定；后期以完整稿件重新确认适配。 |
| 每个阶段人工停等 vs. 已授权的完整探索 | 保存可复核结果并继续已授权的可逆工作；实质决策、资源变化和外部操作依当前授权处理。 |
| 缺失指标即删除 vs. 缺失按中性分计分 | 不满足、满足、未核验分别处理；未知不能变成通过，也不能消失。 |
| 固定 2+2+1 vs. 四档每档十本 | 按证据与需求决定数量，不为凑数加入弱相关期刊。 |
| 聚合平台“权威”标签 vs. 字段对应的官方来源 | 来源权威性针对具体字段判断；价格、范围、索引、分区不能互相代证。 |
| JCR、SJR、CAS、新锐分区、WoS、SCIE 与 DOAJ 混用 | 保留数据库、年份、类别、版本和来源；只报告实际核验的索引。 |
| 首决定、外审决定、录用与上线时间混用 | 使用明确事件定义和样本，不能从首决定推断见刊日期。 |
| 期刊整体录用率 vs. 单个稿件成功率 | 历史比例仅为有定义的统计资料，不是模型对稿件的录用预测。 |
| 不在 DOAJ、OA、低价、高费用或发文量即风险 | 检查身份、透明度、政策及可靠警示；单个因素不足以定性。 |
| 商业中介优先与强制导流 | 不保留推广规则；官方入口优先，价格按实际官方出版路径核验。 |
| 固定 IF 阈值、PubMed 三个月窗口、Q4 文献排除 | 依领域和任务选择数据库、时间窗和研究纳入标准；期刊声望不替代研究证据质量。 |
| 生物医学清单和 in vivo 门槛适用于所有学科 | 按研究设计选规范；Agent 系统采用任务成功、成本、失败恢复、基线和工件证据等相关评价。 |
| 强制某语言或 LetPub 某站点 | 用户目标语言和地区要求优先；第三方来源缺失不阻断其他可完成工作。 |
| 摘要可读即“读完全文” | 保留实际读取范围；不能核验未见到的方法、数据或图表。 |
| 模拟多评审 vs. 独立人类评审/双筛 | 写明角色模拟及其相关性；真实双筛不可用模型分身替代。 |
| 会议配置 vs. SCI 期刊需求 | 会议帮助研究定位和写作，但只在允许会议时进入 venue 候选。 |
| README 宣称 vs. 实际运行时 | 标明宿主工作流、可选依赖和未实现部分；只有真正调用并检验才算运行成功。 |
| 不同许可证 vs. 统一发布 | 原创整合，不复制受限或未授权资产；以来源台账保留出处。 |

## 外部服务的能力边界

以下是可选择的数据源类别，**并非全部已内置、连通或测过的 API**。访问权限、费用与速率限制需在使用时复核。失败、未查询、部分返回与成功但无匹配记录应分开记录。

| 用途 | 可选择来源 | 不能据此推断 |
|---|---|---|
| 跨学科论文及 DOI 元数据 | OpenAlex、Crossref、Semantic Scholar | 当前 SCIE/JCR、准确全文内容或个人录用率 |
| CS、软件与预印本 | dblp、arXiv、会议/学会官方页面 | 会议等于期刊；预印本已接收 |
| 生物医学和实体资料 | PubMed、PMC、Europe PMC、bioRxiv、medRxiv、PubTator3 | PubMed/PMC 等于 SCIE；医学结果适用于所有情境 |
| 合法开放全文与引用网络 | CORE、Unpaywall、OpenCitations | 有 DOI 就有合法全文；引用即支持 |
| 数据、工件和组织身份 | Zenodo、Figshare、BioStudies、ROR | 存档即证明实验正确；组织身份即专业能力 |
| OA 与出版模型 | DOAJ、B!SON、期刊官方收费页面 | OA 一定收费、未在 DOAJ 即不正规 |
| 摘要辅助选刊 | JANE、Elsevier/Springer/Wiley/IEEE 官方 Finder | 匹配分数等于录用概率；单出版商召回覆盖全部期刊 |
| 索引和机构目录 | Clarivate MJL/JCR、Scopus/SJR、对应官方中文目录、NPPA | 聚合标签代替当前目录；不同数据库 Q 值可互换 |
| 国内检索与地区适配 | CNKI、万方、维普、NCPSSD、Baidu Scholar、TR Dizin/DergiPark 等 | 平台收录等于所有机构认可或国际索引收录 |
| 投稿经历与聚合查询 | LetPub、SciRev、小木虫、easyScholar、Google Scholar | 社区经历是期刊承诺；未找到就是不存在 |

上游 `paper-lookup` 的 18 类 API 名称已逐项记录在机器清单；dblp、B!SON、JANE 是领域扩充。某个服务不可用时，应给已完成结果、具体缺失字段和下一步核验路径。

## 可复核性与后续更新

1. 用清单中的提交 SHA 查看当时来源，避免上游更新后无法解释差异。
2. 区分来源说明核验、静态代码检查、离线程序测试、在线接口测试和真实投稿结果；五者不能互相替代。
3. 引入真实外部适配器时，补充许可证、版本、实际输入输出、失败方式和测试证据。
4. 新增学科时，更新路由与适用数据库，并用该领域真实或明确标注的合成任务验证；不要只增加触发关键词。
5. 维护“已覆盖、可选依赖、未采用及原因”台账。能力提升结论应由本项目测试或实际结果支持，而非上游 README 宣传措辞。
