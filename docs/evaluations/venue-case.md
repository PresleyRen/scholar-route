# 合成选刊案例试用记录

## 试用范围与准确任务提示

- 试用日期：2026-10-20。
- 技能：仓库内 `skills/scholar-route/SKILL.md`。
- 输入：仓库内 `examples/fixtures/journal-case.json`。
- 本次执行目录：`/tmp/scholar-route-venue-case/`。
- 数据性质：合成教学 fixture；仅使用给定本地材料，不联网。

本次子任务实际收到的提示原文如下：

> 请使用 $scholar-route，技能在 /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/SKILL.md，处理 /workspace/scratch/00d3cea7c405/scholar-route/examples/fixtures/journal-case.json 这份合成选刊教学案例。用户希望这篇 Agent 系统稿件投 SCIE、没有强制费用，尽量给出三本候选，并说明哪个更值得先投、还有什么需要核实。只使用给定材料，不联网。请完成可用的分析和项目报告，把输出保存到 /tmp/scholar-route-venue-case/，最后用中文交付。不要修改技能文件。

本次原始中文分析保存为同目录的 `venue-case-output.md`，内容来自本次输出 `CASE_ANALYSIS_ZH.md`，未改写结论。公开归档把未分发的临时文件链接改为文件名，并把原始输入引用指向仓库 fixture；完整试用项目未纳入本仓库。

## 主要结果

结论为：**A 优先考虑；B 的强制费用待核实；C 为会议并排除。现有材料支持 1 本记录内合格期刊，不能提供 3 本合格期刊。**

| 记录 | 出版类型 | SCIE 字段 | 全部强制费用 | 结果 | 解释 |
|---|---|---|---|---|---|
| `journal-a` / Fictional Journal A | `journal` | 记录为 SCIE | 0 USD，`includes_all_mandatory: true` | `eligible` | 唯一通过所有记录内硬约束的对象 |
| `journal-b` / Fictional Journal B | `journal` | 记录为 SCIE | 缺少 `mandatory_fee` | `unverified` | 未知费用不能填为零，也不能当作已知收费 |
| `venue-c` / Fictional Conference C | `conference` | 记录为 SCIE | 0 USD，`includes_all_mandatory: true` | `excluded` | 违反必须是期刊的约束，其他字段通过不能抵消 |

显式执行 `assess --limit 3` 后，shortlist 仅含 `journal-a`。没有虚构第三本期刊，没有把会议改为期刊，也没有降低用户的 SCIE 或零强制费用要求。

A 的优先级来自硬约束证据完整性。三个对象的原始 fit 都是 4/5，且共同链接 `fixture-paper` 与唯一的 `paper-one`；不能用这些相同且未独立复核的分数预测录用率、稿件准备度或逐刊真实适配。

### 待核实事项

- A 的具体零费用出版路线、文章类型与全部适用收费。输入虽有“0 + 包含全部强制费用”标记，但没有具体 `oa_route`、费用分项与适用条件原文。
- B 的全部强制费用。完整、无未确认条件且适用于本稿的总额为零，才可升入合格池；明确大于零则排除；仍未知则继续待核实。
- 实际期刊身份、正式 ISSN/eISSN、当前 SCIE 集合、各刊 scope、文章类型与各自的可比论文。
- 稿件全文、实现、数据、固定调用预算的核算规则、对照、消融及留出测试证据。
- 新的期刊材料，以补充第三本合格候选。当前三条记录无法满足该数量。

## 项目恢复与执行过程

从 fixture 的 `project_records` 恢复原项目，没有重新创建身份或覆盖原历史。保留了原始 10 条历史以及来源、论文、候选、fit、主张、假设和实验状态，通过技能 CLI 追加 8 条有证据链接的分析决策，最终 revision 为 18。

领域显式选择 `agent-ai,computer-science`，本次工作阶段为 `journal`。原项目 `stage: full` 保留不变；它是项目配置，不代表全部适用模块已完成。`claim-one` 仍为 `proposed`，`hypothesis-one` 与 `experiment-one` 仍为 `planned`。

生成了项目 JSON、三池评估、记录报告、CSV、关系图、书目、待核实队列和完整中文分析。完整项目、命令日志及合成压缩包仍留在本次本地输出目录；本仓库此次只保存本记录和原始中文分析两份 Markdown。

## 实际验证命令及结果

实际运行的本地构建入口为：

```bash
python -B /tmp/scholar-route-venue-case/build_case_report.py
```

该脚本顺序调用技能 CLI 完成路由、结构校验、决策记录、评估及导出。为避免写入技能目录的 Python 缓存，本次 Python 命令使用 `-B`，脚本子进程同时设置 `PYTHONDONTWRITEBYTECODE=1`。

下列是关键子命令的可读形式；本次子进程实际解释器路径为 `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python`，此处用 `python` 表示同一个解释器：

```bash
python -B /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py route --topic "LLM Agent recovery under a fixed tool-call budget" --domains agent-ai,computer-science --stage journal --region international

python -B /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py validate --project /tmp/scholar-route-venue-case

python -B /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py assess --project /tmp/scholar-route-venue-case --limit 3

python -B /workspace/scratch/00d3cea7c405/scholar-route/skills/scholar-route/scripts/scholar_route.py report --project /tmp/scholar-route-venue-case
```

8 条决策分别使用 `record --project /tmp/scholar-route-venue-case --kind decision --input <本次决策JSON路径>` 顺序写入。构建入口先执行了一次，再为增加导出文件中的合成数据说明及可读图重新运行一次；重复记录没有增加 revision。原始证据和历史保留检查均通过。

| 检查 | 实际结果 |
|---|---|
| CLI 路由、记录、评估、校验、导出 | 全部相关命令退出码 0 |
| 最终项目结构校验 | `valid: true`，revision 18，`warnings: []` |
| 记录数量 | sources 3；papers 1；journals 3；claims 1；hypotheses 1；experiments 1；decisions 8；searches 0 |
| 三池结果 | eligible `[journal-a]`；unverified `[journal-b]`；excluded `[venue-c]` |
| 显式最多 3 项 shortlist | `[journal-a]` |
| 原项目 ID、前 10 条历史、原证据及科研状态 | 保留检查通过 |
| 原 fixture 与本次副本 | SHA-256 相同 |
| 本次运行前后技能文件内容 | 哈希对比未变 |
| 输出 JSON 解析 | 43 个 JSON 全部解析成功 |
| 中文报告中的本地 sandbox 文件链接 | 检查时无缺失目标 |
| 本地交付压缩包 | 65 个文件、66,089 字节，`ZipFile.testzip()` 检查通过；没有纳入仓库 |

本次 fixture SHA-256：

```text
a72fa184d9322c5a8892565862c70b8faf6e347acab3cc2fc36fbf3a1ec74a4c
```

最终报告记录的项目 fingerprint：

```text
9616ef7fb30b4fb62995fecfc58802e88632a86a47a57750891ae0793816e3a6
```

## 发现的显示标签问题

技能 CLI 原始 `MAP.md` 对 `journals` 集合的节点和实体表统一使用“期刊”显示标签，因此出现了：

```text
J3["期刊: Fictional Conference C"]
```

实体表中 `venue-c` 的类型显示也为“期刊”。这是集合的通用展示标签与记录的实际 `venue_type: conference` 不一致；它没有改变本次约束判断，`assess` 仍将 C 排除。

本次仅在输出层处理可读性：保留 CLI 原始图为 `logs/map-generated-original.md`，把用户阅读的 `MAP.md` 整理为三池筛选图，并在实体表中按记录类型将 C 显示为“会议”。项目事实、技能代码与原始测试结论都未修改。

同时在输出 `REPORT.md` 和 `references.bib` 增加了合成数据说明。CLI 原始记录报告保留于 `logs/report-generated-original.md`，便于区分程序原始输出与交付展示层说明。

## 证据与结论的限制

1. **这是教学 fixture，不是真实期刊推荐试验。** 输入明确 `fictional: true`，三条来源都注明是 synthetic fixture；本次实际核实的真实期刊数为 0。
2. **没有联网。** 示例网址均未访问；没有尝试实时索引、费用、周期或官方政策核验。
3. **未实际阅读论文摘要或全文。** `paper-one` 的 `read_status: abstract` 是继承的输入状态，fixture 没有摘要正文；原 `verified: true` 同样不代表本次完成外部核查。
4. **程序检查不能替代语义核验。** A 的费用标记足以通过当前 CLI，但具体出版路线仍缺；三个 fit 都能被结构接受，却不能形成三个独立、当前且逐刊成立的适配论证。
5. **结构警告为空不代表证据完整。** `warnings: []` 说明规定的结构检查未报错，不能证明身份、政策、文献主张或实验结果真实。
6. **没有执行科研实验。** 本次验证是本地项目及报告验证；未执行 Agent 恢复实验、训练、基准评估或投稿。
7. **覆盖范围很小且明示有限。** 只审查 3 条合成投稿对象和 1 条合成论文记录；未做市场级期刊发现、穷尽检索、接收概率估计或第三本真实候选补充。

本次试用支持的判断是：三态硬约束筛选对这组输入得到预期结果，历史与未知状态被保留，人工报告明确处理了凑数、会议类型、费用未知、共享 fit 证据和合成来源边界。它不证明现实选刊准确率或稿件发表结果。
