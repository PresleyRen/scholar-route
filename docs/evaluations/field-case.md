# Field-case：首次离线研究探索试跑

## 准确任务提示

以下为本次独立代理收到并据以执行的任务提示，保留原文：

> 请使用 $scholar-route，技能在 /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/SKILL.md，完成 /workspace/scratch/00d3cea7c405/scholar-route/examples/fixtures/agent-brief.md 中请求的研究探索方案。先基于现有初步笔记工作，本轮不联网也不调用模型 API。请在 /tmp/scholar-route-field-case/ 建立可以继续更新的研究项目、领域和证据关系图、中英文检索计划、两个可研究问题及最小实验方案，最后用中文交付。请直接推进合理的可逆工作，不需要先问用户。不要修改技能文件。

输入是本仓库原创合成 fixture：examples/fixtures/agent-brief.md。首次运行日期为 2026-10-20。输入 SHA-256：be531057e0af472d00da91a2b3201fa996c1af33c70cbecc54130fa64332685a。

本评估记录首次工作流体验；不因为随后可能进行的实现修改而追改首次结论。没有修改技能代码、技能说明或 README。

## 实际执行范围

读取 SKILL.md，以及 data-contracts.md、domains.md、exploration.md、agent-research.md、journal-selection.md、record-examples.md。为准确使用 CLI，阅读其帮助与相关源代码的参数/校验片段。使用 Python 标准库与原生 CLI 创建项目、登记记录、导出报告。没有联网，没有调用模型 API，没有阅读科研论文或原控制器源码，没有执行研究基准。

自动路由返回 agent-ai、biomedicine、computer-science；随后显式采用 agent-ai、computer-science、biomedicine，并在研究解释中把 Agent/软件可靠性设为主要贡献、生物医学限定为文章证据语境。full 的模块列表被视为后续路线，而非已完成清单。

## 实际输出

完整可续写项目位于 /tmp/scholar-route-field-case/。项目通过 CLI 创建与更新，保留 project_id/revision/history。

| 输出 | 实际内容 |
|---|---|
| RESEARCH_PLAN_ZH.md | 中文边界、开发观察、八种竞争解释、两个问题、优先顺序和后续决策 |
| FIELD_EVIDENCE_MAP.md | 领域图、记忆证据图、恢复证据图及主张—证据—实验表 |
| SEARCH_PLAN_ZH_EN.md | 17 条中英文查询草案、概念组、四层反新颖性检索、筛选/去重/阅读深度与记录规则 |
| EXPERIMENT_PROTOCOL.md | RQ1/RQ2、强基线、合成数据、故障/版本设计、预算、评分与分析、停止规则 |
| JOURNAL_ROUTE.md | 基于真实结果的后续稿件定位、候选发现、官方事实核查与三池路径；没有虚构候选 |
| project.json | 5 claims、2 hypotheses、3 planned experiments、5 decisions；sources/papers/journals/searches 均为 0 |
| LOCAL_EVIDENCE.json / evidence/agent-brief.md | 本地输入快照、原路径、SHA-256、阅读状态与定位 |
| protocol/ | 机器可读试点预算与 planned 搜索清单 |
| templates/ | 后续检索/证据提取/运行清单/调用账本/事件记录/期刊核查模板 |
| REPORT.md / MAP.md / assessment.json / journals.csv / references.bib | 原生 report 导出，明确未检索、未测量、无期刊候选 |
| logs/ | 路由、逐条 record、validate/assess/report 与 33 项一致性检查的真实输出 |

供仓库评审的主研究方案保留于 [field-case-output.md](field-case-output.md)。没有把完整临时项目、运行账本、用户私有文件或凭据复制进仓库。

### 两个研究问题

1. 在相同模型、版本目录、语料与预算下，来源依赖的选择性失效能否比完整来源版本清单规则缓存提高正确且版本可追溯的完成率？摘要记忆与每次新检索为额外对照，完整版本清单缓存为主要危险基线。
2. 在相同幂等键、状态核查与尝试预算下，按可观测错误类型恢复能否减少无效重试且保持有效完成率？通用重试和移除幂等的消融用于归因，不能把幂等带来的收益归于错误分类。

### 最小实验与预算

- E0：20 个独立合成家族 × 6 类故障 × 4 策略 = 480 个计划本地运行，外部模型调用 0；未执行。
- E1：4 家族 × 4 组开发 = 16 调用；16 测试家族 × 2 上下文 × 4 组 = 128 调用；未执行。
- E2：8 新家族 × 3 恢复策略 × 一次最终回答 = 24 调用；未执行。
- 加 4 次接口烟雾检查，基础计划 172；明示保留 28；未来硬上限 200。失败、超时和重试均计入，本轮实际调用 0。

明确使用固定本地摘要/可控丢失注入，不把这项设计声称为自然生成摘要的端到端分布研究。E2 使用程序化恢复，不声称测试了模型自主选择恢复动作。评分优先采用可确定的版本、来源与提交语义，保留拒答和失败，按家族配对分析，不把重复运行当作新独立样本。

## 验证命令与首次实际结果

运行下列原生 CLI 命令均返回退出码 0：

    python skills/scholar-route/scripts/scholar_route.py route --topic "Long-term memory and failure recovery in an LLM Agent for public biomedical articles" --stage full

    python skills/scholar-route/scripts/scholar_route.py route --topic "Long-term memory and failure recovery in an LLM Agent for public biomedical articles" --domains agent-ai,computer-science,biomedicine --stage full

    python skills/scholar-route/scripts/scholar_route.py init --project /tmp/scholar-route-field-case --topic "Long-term memory and failure recovery in an LLM Agent for public biomedical articles" --domains agent-ai,computer-science,biomedicine --stage full --language zh-CN

每条记录经由原生 record 命令写入，顺序为 claim → hypothesis → experiment → decision，全部 15 条写入成功。没有直接编辑主项目身份/修订字段。

    python skills/scholar-route/scripts/scholar_route.py validate --project /tmp/scholar-route-field-case
    python skills/scholar-route/scripts/scholar_route.py assess --project /tmp/scholar-route-field-case
    python skills/scholar-route/scripts/scholar_route.py report --project /tmp/scholar-route-field-case

首次 validate 实际结果为 valid=true、revision=15、warnings=[]；计数为 sources=0、papers=0、journals=0、claims=5、hypotheses=2、experiments=3、decisions=5、searches=0。assess 的三个期刊池均为空；不把这一结果当作期刊不存在或不可发表。

额外运行：

    PYTHONDONTWRITEBYTECODE=1 python /tmp/scholar-route-field-case/verify_artifacts.py

实际结果：33 项检查通过，包含 200 次上限算术、E0 分组乘积、未执行状态、17 条未执行查询、来源哈希一致、sidecar 引用、文档存在与生成报告修订一致。它们是项目/方案一致性检查，不是科研实验或科学新颖性验证。

已阅读导出的 REPORT.md、MAP.md、assessment.json、journals.csv 与 references.bib。手写地图采用精简 Mermaid 补足本地证据关系；没有运行图像渲染器，故没有声称完成图像级视觉检查。

## 最初遇到的问题与实际降级方式

### 1. 本地初步笔记不能作为原生 source 记录

首次阅读数据契约及 project_store.py 的 URL 校验时确认 source.url 只接受有 hostname 的 HTTP(S)，拒绝 file/local 路径。此次唯一本地 brief 没有已知正式 URL。

这项限制是在调用 record source 之前识别的，**不是一次实际 record 命令报错**。没有先造假 URL 再修复，也没有用 example.org 冒充来源。

实际降级：原文副本与 SHA-256 放入 evidence/ 和 LOCAL_EVIDENCE.json；claim/decision 的 notes.local_evidence_ids 关联 sidecar；sources 保持 0；手写 FIELD_EVIDENCE_MAP.md 显示本地证据节点。开发者观察的研究主张保持 unsupported；候选机制保持 proposed，未写成 supported。

影响：项目仍能续写、结构验证与导出，但原生 REPORT/MAP 的 source 关系不能直接展示该本地输入。完整证据链需要同时阅读 sidecar 和手写地图。单独传阅原生报告的可读性较弱；README 与主方案明确解释这一点。

### 2. 原控制器只有文字描述，没有实际代码或日志

brief 说存在 Python 控制器与两个工具，但没有提供程序入口、工具定义、摘要样本或失败 trace。本轮没有从文字推断实际实现，也没有为了凑实验结果搭建一个替身并宣称验证原系统。

实际降级：实验保留 planned；先给出需要核对的接口、工具副作用、operation_id、提交前/提交后超时区别、可重放场景与评分/预算门槛。没有因缺代码阻断独立的计划、图谱、检索协议与项目建设。

### 3. 离线约束使搜索与新颖性只能处于计划状态

没有任何科研论文输入。实际降级：17 条查询保存在 planned 协议 sidecar，executed_at/counts 为 null；原生 searches 为空，避免把“未运行”误记成“零结果”。新颖性主张未支持、研究缺口标为“尚未检索”。

### 4. 原生 full 报告信息较泛

full 路由展示 40 个适用模块与空期刊池。它能保存状态，但不能替代有内容的研究探索。实际处理：保留原生输出供复核，另交付针对本任务的中文研究报告、地图与实验协议。没有把模块枚举视作完成工作，也没有修改技能或报告生成器。

## 未完成项及原因

- 未执行文献检索/精读/引用追踪：本轮明确禁止联网，输入中没有论文。
- 未证实创新性或任何机制增益：缺少文献与实测结果。
- 未审查/运行真实 Agent：未提供原控制器源码与日志。
- 未执行 E0/E1/E2：本次目标为探索计划；原控制器/评分器未就绪，模型调用被明确禁止。
- 未核验真实公开文章的授权、版本/更正、训练污染和域内语义：尚未获取任务语料。
- 未核验/排序真实期刊、费用、收录或周期：没有当前官方证据，也没有已形成的稿件结果。
- 未部署、购买、临床研究、通信或投稿：没有相应授权，也不属于当前任务。
- 未做 Mermaid 图像渲染：交付为 Markdown/Mermaid，进行了文本/关系与结构审查。

## 评价边界

本次试跑证明该入口在离线、只有初步笔记的条件下能组织出具体研究方案并维持主张/实验状态，但它不能证明检索召回、科研新颖性、模型机制、统计功效、真实运行可靠性或投稿建议准确性。最明显的工作流限制是本地证据来源需要原生结构之外的 sidecar；该首次观察保留，不因未来实现修订而消除。
