> **输出来源说明：** 下方正文是主 Agent 在图谱修复后于 2026-10-20 04:40:58 UTC 对同一项目重新运行 report 得到的主报告，不是首次前向试用的原始导出。首次导出于 04:36:38 UTC，文件在独立保存前被覆盖；首次命令、检查及发现的问题见 [local-evidence-case.md](local-evidence-case.md)。此页不作为修复后独立回归通过的证据。

# ScholarRoute 研究与投稿记录

**主题：** Long-term memory and failure recovery in an LLM Agent for public biomedical article question answering

**生成时间：** 2026-10-20T04:40:58+00:00  
**项目版本：** 6

**数据指纹：** 3acc179b3a92149718f84762603756ba656a10e3ae8ad84b244c40ab9a180727

这是基于项目记录生成的工作报告。结构检查不能证明源网页支持某个事实，也不预测录用率。

## 路由与当前工作

- 领域：agent-ai、computer-science
- 阶段：explore
- 适用模块：12
- 模块清单：intake、field-map、search-protocol、paper-search、identifier-check、evidence-review、paper-notes、novelty-audit、hypothesis-plan、agent-capabilities、agent-systems、state-map

## 记录统计

| 记录 | 数量 |
|---|---|
| sources | 1 |
| papers | 0 |
| journals | 0 |
| claims | 1 |
| hypotheses | 1 |
| experiments | 1 |
| decisions | 2 |
| searches | 0 |

## 期刊筛选

以下分组只检查已记录的硬约束。适配分是 0–5 的主观、有依据评估；空值不补分。

### 符合已记录约束

| 投稿候选 | ID | 适配分 | 检查结果 |
|---|---|---|---|
| — | — | — | 尚无记录 |

### 待核实

| 投稿候选 | ID | 适配分 | 检查结果 |
|---|---|---|---|
| — | — | — | 尚无记录 |

### 已知不符合

| 投稿候选 | ID | 适配分 | 检查结果 |
|---|---|---|---|
| — | — | — | 尚无记录 |

### 待人工复核的建议顺序

暂无同时具备完整硬约束证据和适配评估的候选。

同出版社展示上限：2；被延后或未评分的期刊仍保留在完整候选池。

## 主张、假设与实验

| 类型 | ID | 内容 | 状态 |
|---|---|---|---|
| claims | claim-note-motivation | 仅关于这份虚构规划笔记的可核对陈述：笔记记载长对话摘要可能丢失版本信息，超时重试可能重复执行；作者明确说明这些只是没有次数、运行轨迹或受控研究的开发观察，且未运行基准。此来源支持将版本一致性列为待研究问题，不支持已经存在可量化缺陷、改进有效、优于缓存或具有文献新颖性的结论。 | supported |
| hypotheses | rq1-version-aware-memory | RQ1：在公开文章或合成文档的版本更新与长对话任务中，固定模型、检索快照、提示、上下文及总调用预算时，带来源标识和版本感知失效的记忆机制，能否比固定摘要记忆和简单版本检查缓存更少地产生过期回答，同时不降低正确完成率？候选假设是可以；目前尚未测量。 | proposed |
| experiments | experiment-rq1-pilot | 待执行最小试验：先建立可本地审计的合成文档版本变化任务与正确答案，再在相同任务上比较固定摘要、简单版本检查缓存、完整来源与版本感知失效三种条件；测量过期回答与正确完成率。本轮仅记录计划，未编写或执行该实验，未产生结果。 | planned |
| decisions | decision-local-scope | 接受本轮范围：仅审阅并归档提供的本地虚构规划笔记，建立可续用证据记录并导出报告。主研究领域采用 agent-ai 与 computer-science；生物医学是语料背景，本轮无患者数据、临床部署或患者获益主张。明确不联网，未检索论文，未检查控制器代码，未运行基准；不据此选刊或宣称新颖性。 | accepted |
| decisions | decision-update-protocol | 继续更新规则：同主题在此目录 init 以恢复项目；新增证据先保存原始字节和实际 SHA-256，再 record source，之后更新引用它的 claim、hypothesis 或 experiment。保留本次快照和尚未解决的替代解释。只有实际运行并保存产物与测量结果后才能将试验设为 completed。每次实质更新后 validate 并重新 report。 | accepted |

## 检索边界

尚未记录检索。不能据此声称已覆盖某个领域。

## 证据来源

| ID | 来源 | 类型 | 访问日期 | 记录核实状态 |
|---|---|---|---|---|
| local-agent-brief-v1 | Research brief — fictional planning case — local: /tmp/scholar-route-local-evidence-case/evidence/agent-brief.md (sha256: be531057e0af472d00da91a2b3201fa996c1af33c70cbecc54130fa64332685a) | other | 2026-10-20 | 已记录核实 |

## 当前边界

- 报告保留事实来源和缺失项；科学主张是否成立、期刊是否真实适配仍需阅读原始证据。
- first_decision、external_review、acceptance、publication 时间不得混用；历史统计不是截止时间保证。
- 任何尚未实际执行的实验、提交、发表或通信均不能由本报告自动变成已完成。
- 研究关系见 MAP.md；规范化记录及历史见 project.json；引文元数据见 references.bib。
