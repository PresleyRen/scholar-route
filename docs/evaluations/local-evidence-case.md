# Local evidence case — 首次前向试用

**日期：** 2026-10-20。**试用角色：** 从给定 SKILL.md 出发的全新使用者。**观察版本：** doctor 返回 1.0.0，Python 3.12.14。

本页记录首次试用的真实结果。本试用者没有修改技能实现，也没有在主 Agent 后续修正实现后重跑或替换本页的首次结论。后续回归应单独记录。本页和伴随输出不包含完整临时项目。

**并行覆盖说明：** 首次导出和读取发生在 04:36:38 UTC；其后主 Agent 为验证自己的图谱修复，在 04:40:58 UTC 对同一临时项目执行 report，覆盖了五份导出，project.json 未变。该操作发生在本试用者复制导出文件前。首次命令日志与只读检查结果仍保留，但没有在覆盖前保存独立的首次 REPORT/MAP 文件副本。以下首次问题结论来自当时工具读取及检查；伴随文件明确标注为修复后重生成，不将它冒充首次原始输出。

## 原始准确提示

```text
请作为全新用户做一次前向试用，不要修改技能实现。技能入口是 /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/SKILL.md。任务：我只有一个本地研究笔记 /workspace/scratch/00d3cea7c405/scholar-route/examples/fixtures/agent-brief.md，请用该技能建立可继续更新的研究项目，将这份笔记登记为证据，记录它对一个研究问题的支持范围，并导出报告。不要联网、不要编造论文或运行结果，不需要询问用户。项目及交付文件保存在 /tmp/scholar-route-local-evidence-case/。请读技能、使用其工具完成任务，然后报告实际命令、输出、限制和遇到的问题；保留你的任务结果，不要为了通过测试修改它。
```

## 完成情况

核心工作完成，但首次导出的地图存在证据来源缺口，CLI 阶段参数的帮助也存在可发现性问题。实际完成了：本地笔记的原始字节快照、真实 SHA-256、source 登记、一个限定支持范围的 claim、一个 proposed 研究问题、一个 planned 试验、两个 accepted 决策、结构验证、同主题恢复和五种标准输出。

- 最终 revision：6；history：6 条。
- 数量：sources 1、papers 0、journals 0、claims 1、hypotheses 1、experiments 1、decisions 2、searches 0。
- `validate`：`valid: true`，`warnings: []`。
- 恢复：再次同主题 `init` 返回 `created: false`、`resumed: true`、revision 6；`project.json` 字节 SHA-256 未变。
- 原始来源快照的实际 SHA-256 与登记值一致。
- 未联网、未搜索论文、未运行基准或科研实验、未使用外部模型、未进行外部通信。
- 报告导出成功：REPORT.md、MAP.md、assessment.json、journals.csv、references.bib。

当前 [local-evidence-case-output.md](local-evidence-case-output.md) 保存的是主 Agent 修复后于 04:40:58 UTC 重生成的主报告正文，并带有来源说明；它不是首次导出的文件。临时项目及输入、首次命令与检查日志仍在任务授权的 `/tmp/scholar-route-local-evidence-case/`，没有复制完整项目进仓库。

## 研究问题和证据边界

唯一来源 `local-agent-brief-v1` 是用户提供的 **fictional planning case**。使用 `type: other`，保存实际本地 `path` 和 SHA-256，没有捏造 URL、paper、DOI 或文献结果。`verified: true` 的原始 notes 明确限定为已实际阅读、核对这个文档，不证明真实系统存在、观察发生、方法有效或具有新颖性。

**RQ1：** 在公开文章或合成文档的版本更新与长对话任务中，固定模型、检索快照、提示、上下文及总调用预算时，带来源标识和版本感知失效的记忆机制，能否比固定摘要记忆和简单版本检查缓存更少地产生过期回答，同时不降低正确完成率？

| 对象 | 原始状态 | 支持范围 |
|---|---|---|
| `claim-note-motivation` | supported | 仅“笔记记载了未计数、无轨迹、未经受控研究的开发观察，且尚未跑基准”。支持把版本一致性列为待研究问题，不支持效果量、优越性、新颖性或临床效益。 |
| `rq1-version-aware-memory` | proposed | 候选问题/假设，未测量。简单缓存足够、检索返回旧版本、额外上下文或调用、观察不能复现，都是未排除的解释。 |
| `experiment-rq1-pilot` | planned | 三种记忆条件、版本变化与不变对照、任务级成对比较；不存在运行产物或实验结果。本轮没有执行它。 |

原始 notes 保存了未来 200 次外部模型调用硬上限、应包含失败/重试/开发/评价调用、判否条件和实现依赖。本轮实际外部调用为 0。笔记中的未来期望没有被当作覆盖本轮离线任务的指令。

主领域显式采用 `agent-ai,computer-science`。路由原本因 biomedical 关键词建议加入 biomedicine；本轮依据笔记将其限定为文档语料背景，没有临床干预或患者效益研究。

## 首次发现的问题和限制

1. **阶段帮助没有枚举允许值。** `route --help`、`init --help` 只显示 `--stage STAGE`，第一次根据文档用词输入 `--stage exploration` 返回退出码 2；错误消息才列出可用的 `explore` 等值。使用错误消息给出的合法值后成功。没有修改解析器。
2. **MAP.md 缺少 source 节点、source→claim 关系和 source 实体表行。** 原始项目中 `claim-note-motivation.source_ids` 正确指向 `local-agent-brief-v1`，但首次 MAP.md 从 claim 节点开始。首次工具读取与只读检查保留了这一观察。首次 MAP 没有在主 Agent 覆盖前保存独立副本，因此本页不重建或补写所谓首次完整输出。REPORT.md 的来源表正常含本地路径及 SHA-256。
3. **主报告未展示详细 notes。** 原始 REPORT.md/MAP.md 只展示主要 text 与状态，因此替代解释、判否条件、预算及依赖仍需阅读项目记录。重要的支持边界事先写入 claim.text，所以它在导出主报告内可见。另写人工伴随说明不等于修改工具输出。
4. **探索输出仍以期刊筛选为主要固定段落。** 本轮没有期刊，三个池为空，CSV 只有表头、BibTeX 只有注释。这些是没有记录的真实输出，不意味着搜索没有找到论文或期刊。

这些观察只来自首次前向试用。结构验证证明记录结构通过，不证明来源所述科学事实；恢复检查只证明此次本地同主题恢复保持文件字节，不证明长期存储或分布式并发能力。

## 前置调用与最早错误

日期：2026-10-20。以下为自动命令日志建立前的实际调用及关键输出摘录；不是补跑或模拟结果。完整工具响应已在试用会话中返回。

## 读取技能和输入

实际阅读了以下本地文件：

- `/workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/SKILL.md`
- `/workspace/scratch/00d3cea7c405/scholar-route/examples/fixtures/agent-brief.md`
- `references/data-contracts.md`
- `references/record-examples.md`
- `references/domains.md`
- `references/exploration.md`
- `references/agent-research.md`

引用文件均从 SKILL.md 所在目录解析。没有调用文献搜索工具、联网工具或安装依赖。

## CLI 帮助与 doctor

以下命令均退出 0：

```bash
python /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py --help
python /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py init --help
python /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py route --help
python /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py record --help
python /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py doctor
```

`doctor` 关键原始值：`version=1.0.0`、`python=3.12.14`、`python_supported=true`、`module_count=41`、`domain_count=8`、`missing_references=[]`、`provenance_manifest_present=true`、`live_network_tested=false`、`ok=true`。发现 pandoc、pdflatex、xelatex，但本轮没有调用它们。

## 首次路由失败及恢复

实际失败命令：

```bash
python /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py route --topic 'Long-term memory and failure recovery in an LLM Agent for public biomedical article question answering' --stage exploration
```

退出码 2，原始输出：

```json
{
  "error": {
    "type": "ValueError",
    "message": "Unknown stage. Choose: explore, review, design, experiment, journal, dossier, write, audit, submit, revise, disseminate, full"
  }
}
```

依据错误消息调整输入后，实际执行：

```bash
python /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py route --topic 'Long-term memory and failure recovery in an LLM Agent for public biomedical article question answering' --stage explore
```

退出码 0，输出中 `selection` 为 `keyword_suggestion`，domains 为 `agent-ai,biomedicine,computer-science`，stage 为 `explore`，给出 12 个模块。根据已读笔记的真实研究对象，初始化项目时显式采用 `agent-ai,computer-science`，原因记录在 `decision-local-scope` 中。

## 执行侧问题，非 ScholarRoute CLI 缺陷

第一次寻找可能适用的 AGENTS.md 使用：

```bash
rg --files -g AGENTS.md /workspace/scratch/00d3cea7c405 /tmp
```

退出码 2，输出 `rg: /tmp/codex-daemon-0: Permission denied (os error 13)`。这是搜索范围包含无关受限目录造成的环境权限提示；没有尝试绕过权限，也没有影响指定路径中的任务。

一次自编的只读检查错误地假设来源集合直接位于项目顶层，访问 `p['sources']` 后得到 `KeyError: 'sources'`、退出 1。随后通过 `head -n 90 project.json` 观察实际格式，改用 `p['records']['sources']` 完成只读检查。此错误没有修改项目文件。正确检查结果保存在 `logs/artifact-inspection.json`。项目数据合同没有展示完整顶层 JSON 示例，但该自编检查错误不等同于 CLI 存储错误。

本试用者没有更改 ScholarRoute 源代码、技能文档或生成报告来让检查通过。首次输入和日志仍保留；之后主 Agent 重生成导出的并行操作另见本页说明。


## 从初始化开始的完整实际 CLI 命令与输出

以下内容来自本轮自动保留的 commands.jsonl；run_cli.py 只是标准库 subprocess 日志包装器，实际调用的是下列未经本试用者修改的脚本。无 stdout/stderr 时不填造输出。

### 命令 1：init

```bash
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py init --project /tmp/scholar-route-local-evidence-case --topic 'Long-term memory and failure recovery in an LLM Agent for public biomedical article question answering' --domains agent-ai,computer-science --stage explore --language zh-CN
```

退出码：0

```text
{
  "created": true,
  "resumed": false,
  "project": "/tmp/scholar-route-local-evidence-case",
  "revision": 0
}
```

### 命令 2：record

```bash
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py record --project /tmp/scholar-route-local-evidence-case --kind source --input /tmp/scholar-route-local-evidence-case/inputs/source-v1.json
```

退出码：0

```text
{
  "changed": true,
  "id": "local-agent-brief-v1",
  "revision": 1
}
```

### 命令 3：record

```bash
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py record --project /tmp/scholar-route-local-evidence-case --kind claim --input /tmp/scholar-route-local-evidence-case/inputs/claim-note-support.json
```

退出码：0

```text
{
  "changed": true,
  "id": "claim-note-motivation",
  "revision": 2
}
```

### 命令 4：record

```bash
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py record --project /tmp/scholar-route-local-evidence-case --kind hypothesis --input /tmp/scholar-route-local-evidence-case/inputs/hypothesis-rq1.json
```

退出码：0

```text
{
  "changed": true,
  "id": "rq1-version-aware-memory",
  "revision": 3
}
```

### 命令 5：record

```bash
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py record --project /tmp/scholar-route-local-evidence-case --kind experiment --input /tmp/scholar-route-local-evidence-case/inputs/experiment-rq1.json
```

退出码：0

```text
{
  "changed": true,
  "id": "experiment-rq1-pilot",
  "revision": 4
}
```

### 命令 6：record

```bash
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py record --project /tmp/scholar-route-local-evidence-case --kind decision --input /tmp/scholar-route-local-evidence-case/inputs/decision-scope.json
```

退出码：0

```text
{
  "changed": true,
  "id": "decision-local-scope",
  "revision": 5
}
```

### 命令 7：record

```bash
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py record --project /tmp/scholar-route-local-evidence-case --kind decision --input /tmp/scholar-route-local-evidence-case/inputs/decision-update.json
```

退出码：0

```text
{
  "changed": true,
  "id": "decision-update-protocol",
  "revision": 6
}
```

### 命令 8：assess

```bash
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py assess --project /tmp/scholar-route-local-evidence-case
```

退出码：0

```text
{
  "project_revision": 6,
  "constraints": {
    "require_journal": true
  },
  "pools": {
    "eligible": [],
    "unverified": [],
    "excluded": []
  },
  "shortlist": {
    "ids": [],
    "publisher_cap": 2,
    "deferred_for_diversity": [],
    "unranked_eligible": [],
    "note": "A heuristic fit ordering with a soft display diversity cap; all candidates remain in their pools."
  },
  "assessed_count": 0,
  "acceptance_probability": null,
  "notice": "No acceptance probability is calculated. Missing evidence remains visible."
}
```

### 命令 9：validate

```bash
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py validate --project /tmp/scholar-route-local-evidence-case
```

退出码：0

```text
{
  "valid": true,
  "revision": 6,
  "counts": {
    "sources": 1,
    "papers": 0,
    "journals": 0,
    "claims": 1,
    "hypotheses": 1,
    "experiments": 1,
    "decisions": 2,
    "searches": 0
  },
  "warnings": []
}
```

### 命令 10：init

```bash
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py init --project /tmp/scholar-route-local-evidence-case --topic 'Long-term memory and failure recovery in an LLM Agent for public biomedical article question answering' --domains agent-ai,computer-science --stage explore --language zh-CN
```

退出码：0

```text
{
  "created": false,
  "resumed": true,
  "project": "/tmp/scholar-route-local-evidence-case",
  "revision": 6
}
```

### 命令 11：report

```bash
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py report --project /tmp/scholar-route-local-evidence-case
```

退出码：0

```text
{
  "project_revision": 6,
  "fingerprint": "3acc179b3a92149718f84762603756ba656a10e3ae8ad84b244c40ab9a180727",
  "files": [
    "/tmp/scholar-route-local-evidence-case/REPORT.md",
    "/tmp/scholar-route-local-evidence-case/MAP.md",
    "/tmp/scholar-route-local-evidence-case/journals.csv",
    "/tmp/scholar-route-local-evidence-case/references.bib",
    "/tmp/scholar-route-local-evidence-case/assessment.json"
  ]
}
```

## 主机端最终只读检查结果

```json
{
  "revision": 6,
  "counts": {
    "sources": 1,
    "papers": 0,
    "journals": 0,
    "claims": 1,
    "hypotheses": 1,
    "experiments": 1,
    "decisions": 2,
    "searches": 0
  },
  "history_entries": 6,
  "source_bytes_match": true,
  "claim_source_ids": [
    "local-agent-brief-v1"
  ],
  "hypothesis_status": "proposed",
  "experiment_status": "planned",
  "project_sha256_after_report": "1ff57368c1482abc4b7319e17c1aa1fbf284aa91ab08c767390703b0dbf0bb0a",
  "exported_map_contains_source_id": false,
  "exported_map_contains_source_node": false,
  "exported_report_contains_source_id": true,
  "exported_report_contains_alternative_explanation": false
}
```

该检查针对首次结果。原始 project.json 的集合实际位于 `records` 下；最初自编检查误用顶层 sources 导致的 KeyError 已在上方列为执行侧问题，未归咎于 CLI。

## 并行覆盖后的文件来源

主 Agent 说明其为验证图谱修复，直接对本轮临时目录运行了 `report --project /tmp/scholar-route-local-evidence-case`。这不是本试用者的首次流程，也没有进入本轮 run_cli.py 的命令日志。原始日志中的 report 及 artifact-inspection.json 因此仍反映首次行为。

事后只读核对发现，复制出的 REPORT 生成时间为 `2026-10-20T04:40:58+00:00`，当前 MAP 已包含 `S1["来源: Research brief — fictional planning case"]`。这两份文件来自主 Agent 修复后的重新生成；本页不把这些新内容当作首次运行结果或独立回归通过结论。先前误复制进此页并标为首次 MAP 的完整区块已经移除，以免污染首次试用记录。

伴随输出页加了明确来源说明，正文保持所复制的修复后 REPORT 内容。没有重建或补写首次 REPORT/MAP，没有改动 project.json，没有开启新的实验或重新执行 CLI。首次问题及实际命令观察保持原结论。
