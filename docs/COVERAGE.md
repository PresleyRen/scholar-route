# 覆盖、互补与扩展定位索引

由 `python tools/coverage_audit.py --write` 从注册表生成。

## 覆盖摘要

17 个来源、139 条特点映射、41 个能力、8 个领域。
33 条冲突中，18 条链接程序行为测试；其余 15 条使用工作流审查。
程序测试验证结构化输入的行为；工作流审查检查实际研究/写作产物。两者分别记录。

## 来源特点如何互补

| 来源 ID | 保留的特点 | 互补来源 |
|---|---|---|
| `zero-journal-recommender` | 摘要画像与投稿梯队 | chinese-research-latex, journal-research-plugins |
| `journal-research-plugins` | 中英文、多数据库发现与权威核验分工 | sci-select, journal-fit-finder |
| `sci-select` | 相似论文反查期刊、本地索引及选刊模式切换 | journal-research-plugins, chinese-research-latex |
| `chinese-research-latex` | 从候选发现深入到单刊全景调查 | journal-research-plugins, ai-research-skills |
| `journal-fit-finder` | 主题、方法、读者、文种与出版商多样性比较 | zero-journal-recommender, journal-atlas |
| `polish-skill` | 精读、创新审计、论证重构、写作与回复衔接 | scientific-agent-skills, academic-publishing-skills |
| `academic-publishing-skills` | 投稿前询问至清样、更正的发表生命周期 | polish-skill, superpapers |
| `superpapers` | 复现驱动的问题发现、实验计划与稳健性 | ai-research-skills, scientific-agent-skills |
| `researcher` | 研究流水线、代码分析、竞争方法与版本管理 | superpapers, longtable |
| `scientific-agent-skills` | 论文身份、综述方法、证据批判与模板检查 | ai-research-skills, journal-research-plugins |
| `ai-research-skills` | 区分 ML 能力贡献与系统设计贡献 | superpapers, academic-publishing-skills |
| `journal-atlas` | 结构化期刊档案与证据等级、档案更新 | journal-research-plugins, journal-fit-finder |
| `journal-finder-local` | 由文献定位发表社区、本地索引维护 | journal-research-plugins, chinese-research-latex |
| `cn-journal-selector` | 中文期刊条件和国内目录路径 | journal-research-plugins, journal-fit-finder |
| `awesome-journal-skills` | 学科与具体发表场所的写作要求 | journal-research-plugins, academic-publishing-skills |
| `food-nutrition-skills` | 食品农业专项检索、研究计划和展示流程 | scientific-agent-skills, superpapers |
| `longtable` | 项目访谈、互补审稿视角与持续证据包 | researcher, polish-skill |

## 能力到实现的定位

每项能力的完整上游子技能映射见 [来源审计](source-audit.md)。

| 能力 ID | 工作流文件 | 原生支撑代码 | 冲突/验收入口 |
|---|---|---|---|
| `intake` | [references/data-contracts.md](../skills/scholar-route/references/data-contracts.md) | route_core.py, project_store.py | CF01, CF16, CF25 |
| `field-map` | [references/exploration.md](../skills/scholar-route/references/exploration.md) | Agent 按工作流执行 | CF01, CF08 |
| `search-protocol` | [references/exploration.md](../skills/scholar-route/references/exploration.md) | Agent 按工作流执行 | CF19 |
| `paper-search` | [references/sources-and-tools.md](../skills/scholar-route/references/sources-and-tools.md) | scholarly_sources.py, search_import.py | CF20, CF27 |
| `identifier-check` | [references/data-contracts.md](../skills/scholar-route/references/data-contracts.md) | project_store.py, scholarly_sources.py | CF09, CF17, CF18 |
| `evidence-review` | [references/exploration.md](../skills/scholar-route/references/exploration.md) | Agent 按工作流执行 | CF08, CF17, CF33 |
| `paper-notes` | [references/exploration.md](../skills/scholar-route/references/exploration.md) | Agent 按工作流执行 | 按该模块具体产物验收 |
| `novelty-audit` | [references/exploration.md](../skills/scholar-route/references/exploration.md) | Agent 按工作流执行 | 按该模块具体产物验收 |
| `hypothesis-plan` | [references/exploration.md](../skills/scholar-route/references/exploration.md) | Agent 按工作流执行 | 按该模块具体产物验收 |
| `agent-capabilities` | [references/agent-research.md](../skills/scholar-route/references/agent-research.md) | Agent 按工作流执行 | 按该模块具体产物验收 |
| `agent-systems` | [references/agent-research.md](../skills/scholar-route/references/agent-research.md) | Agent 按工作流执行 | 按该模块具体产物验收 |
| `experiment-plan` | [references/exploration.md](../skills/scholar-route/references/exploration.md) | Agent 按工作流执行 | 按该模块具体产物验收 |
| `statistics-robustness` | [references/publication.md](../skills/scholar-route/references/publication.md) | Agent 按工作流执行 | 按该模块具体产物验收 |
| `implementation` | [references/agent-research.md](../skills/scholar-route/references/agent-research.md) | Agent 按工作流执行 | CF27 |
| `data-collection` | [references/exploration.md](../skills/scholar-route/references/exploration.md) | Agent 按工作流执行 | 按该模块具体产物验收 |
| `state-map` | [references/data-contracts.md](../skills/scholar-route/references/data-contracts.md) | project_store.py, reports.py | CF18, CF25, CF26, CF28 |
| `manuscript-profile` | [references/journal-selection.md](../skills/scholar-route/references/journal-selection.md) | Agent 按工作流执行 | 按该模块具体产物验收 |
| `venue-discovery` | [references/journal-selection.md](../skills/scholar-route/references/journal-selection.md) | Agent 按工作流执行 | CF10 |
| `venue-identity` | [references/journal-selection.md](../skills/scholar-route/references/journal-selection.md) | project_store.py, venue_audit.py | CF09 |
| `journal-dossier` | [references/journal-selection.md](../skills/scholar-route/references/journal-selection.md) | Agent 按工作流执行 | 按该模块具体产物验收 |
| `indexing-metrics` | [references/journal-selection.md](../skills/scholar-route/references/journal-selection.md) | project_store.py, venue_audit.py | CF04, CF05, CF06, CF33 |
| `costs-timelines` | [references/journal-selection.md](../skills/scholar-route/references/journal-selection.md) | project_store.py, venue_audit.py | CF06, CF12, CF13 |
| `journal-integrity` | [references/journal-selection.md](../skills/scholar-route/references/journal-selection.md) | Agent 按工作流执行 | CF14 |
| `fit-comparison` | [references/journal-selection.md](../skills/scholar-route/references/journal-selection.md) | venue_audit.py | CF02, CF04, CF10, CF11, CF30 |
| `submission-plan` | [references/journal-selection.md](../skills/scholar-route/references/journal-selection.md) | venue_audit.py | CF02, CF03, CF07 |
| `argument-audit` | [references/publication.md](../skills/scholar-route/references/publication.md) | Agent 按工作流执行 | CF21 |
| `manuscript-writing` | [references/publication.md](../skills/scholar-route/references/publication.md) | Agent 按工作流执行 | CF16, CF21 |
| `citation-audit` | [references/publication.md](../skills/scholar-route/references/publication.md) | Agent 按工作流执行 | 按该模块具体产物验收 |
| `figure-table-audit` | [references/publication.md](../skills/scholar-route/references/publication.md) | Agent 按工作流执行 | 按该模块具体产物验收 |
| `peer-review` | [references/publication.md](../skills/scholar-route/references/publication.md) | Agent 按工作流执行 | CF02, CF23, CF29 |
| `venue-formatting` | [references/publication.md](../skills/scholar-route/references/publication.md) | Agent 按工作流执行 | CF31 |
| `cover-letter` | [references/publication.md](../skills/scholar-route/references/publication.md) | Agent 按工作流执行 | CF24 |
| `presubmission-inquiry` | [references/publication.md](../skills/scholar-route/references/publication.md) | Agent 按工作流执行 | 按该模块具体产物验收 |
| `reviewer-discovery` | [references/publication.md](../skills/scholar-route/references/publication.md) | Agent 按工作流执行 | 按该模块具体产物验收 |
| `authorship-credit` | [references/publication.md](../skills/scholar-route/references/publication.md) | Agent 按工作流执行 | CF22 |
| `submission-preflight` | [references/publication.md](../skills/scholar-route/references/publication.md) | Agent 按工作流执行 | CF24, CF29 |
| `revision-response` | [references/publication.md](../skills/scholar-route/references/publication.md) | Agent 按工作流执行 | 按该模块具体产物验收 |
| `proof-check` | [references/publication.md](../skills/scholar-route/references/publication.md) | Agent 按工作流执行 | 按该模块具体产物验收 |
| `dissemination` | [references/publication.md](../skills/scholar-route/references/publication.md) | Agent 按工作流执行 | 按该模块具体产物验收 |
| `postpublication-correction` | [references/publication.md](../skills/scholar-route/references/publication.md) | Agent 按工作流执行 | CF32 |
| `regional-indexing` | [references/domains.md](../skills/scholar-route/references/domains.md) | route_core.py | CF15 |

## 冲突测试与审查清单

CF 编号对应 [冲突规则](../skills/scholar-route/references/conflicts.md)。

| ID | 保留的组合方案 | 验证类型 | 定位 |
|---|---|---|---|
| CF01 | 按任务按需加载 | 程序行为测试 | [test_core.RoutingTests.test_stage_alias_and_region_filter_modules_and_sources](../tests/test_core.py#L631) |
| CF02 | 稿件批评、适配与梯队分工 | 工作流审查 | [工作流验收场景](WORKFLOW-REVIEW.md#cf02) |
| CF03 | 刊级统计与个人机会分开 | 程序行为测试 | [test_core.VenueAuditTests.test_primary_evidence_passes_constraints_without_predicting_acceptance](../tests/test_core.py#L468) |
| CF04 | 缺值进入待核实池 | 程序行为测试 | [test_core.VenueAuditTests.test_confirmed_violation_excludes_even_when_another_fact_is_unknown](../tests/test_core.py#L479) |
| CF05 | 分区精确到体系年度类别 | 程序行为测试 | [test_core.VenueAuditTests.test_quartiles_require_exact_system_year_category_and_consistent_values](../tests/test_core.py#L540) |
| CF06 | 动态事实刷新后使用 | 程序行为测试 | [test_core.VenueAuditTests.test_stale_or_unverified_evidence_does_not_satisfy_hard_constraints](../tests/test_core.py#L511) |
| CF07 | 候选数量随证据变化 | 程序行为测试 | [test_conflict_matrix.ConflictMatrixTests.test_shortlist_does_not_pad_to_requested_size](../tests/test_conflict_matrix.py#L101) |
| CF08 | 研究对象决定检索与评价路线 | 程序行为测试 | [test_conflict_matrix.ConflictMatrixTests.test_agent_medical_and_food_routes_keep_complementary_sources](../tests/test_conflict_matrix.py#L59) |
| CF09 | 文献证据与投稿载体分开 | 程序行为测试 | [test_core.VenueAuditTests.test_unknown_venue_type_is_unverified_and_known_conference_is_excluded](../tests/test_core.py#L488) |
| CF10 | 多源召回与出版社多样性 | 程序行为测试 | [test_core.VenueAuditTests.test_shortlist_retains_pools_and_applies_fit_order_and_publisher_cap](../tests/test_core.py#L584) |
| CF11 | 实际可比论文优于粗略数量 | 工作流审查 | [工作流验收场景](WORKFLOW-REVIEW.md#cf11) |
| CF12 | 必缴费用、可选 OA 与减免分开 | 程序行为测试 | [test_core.VenueAuditTests.test_fee_caps_distinguish_zero_cost_waivers_completeness_and_currency](../tests/test_core.py#L525) |
| CF13 | 四种审稿时间端点分别保存 | 程序行为测试 | [test_conflict_matrix.ConflictMatrixTests.test_turnaround_endpoints_remain_separate](../tests/test_conflict_matrix.py#L90) |
| CF14 | 出版风险按具体证据判断 | 工作流审查 | [工作流验收场景](WORKFLOW-REVIEW.md#cf14) |
| CF15 | 中文目录和商业平台分开 | 工作流审查 | [工作流验收场景](WORKFLOW-REVIEW.md#cf15) |
| CF16 | 复用语言与已知偏好 | 程序行为测试 | [test_conflict_matrix.ConflictMatrixTests.test_resume_preserves_language_and_constraints](../tests/test_conflict_matrix.py#L78) |
| CF17 | 论文身份与阅读深度分开 | 程序行为测试 | [test_core.VenueAuditTests.test_fit_requires_read_paper_current_assessment_and_current_verified_source](../tests/test_core.py#L554) |
| CF18 | 去重同时保留版本 | 程序行为测试 | [test_cli_import.ImportTests.test_preprint_and_publication_with_same_doi_stay_separate](../tests/test_cli_import.py#L78) |
| CF19 | 保留检索覆盖记录 | 程序行为测试 | [test_core.MalformedInputTests.test_search_exhaustiveness_requires_explicit_coverage_record](../tests/test_core.py#L414) |
| CF20 | 接口失败、空结果与成功分开 | 程序行为测试 | [test_scholarly_sources.SearchTests.test_http_200_error_bodies_do_not_create_papers](../tests/test_scholarly_sources.py#L127) |
| CF21 | 一个改写负责人、多个核查视角 | 工作流审查 | [工作流验收场景](WORKFLOW-REVIEW.md#cf21) |
| CF22 | 作者贡献与声明统一登记 | 工作流审查 | [工作流验收场景](WORKFLOW-REVIEW.md#cf22) |
| CF23 | 模拟审稿归并异议 | 工作流审查 | [工作流验收场景](WORKFLOW-REVIEW.md#cf23) |
| CF24 | 准备文件与外部发送分开执行 | 工作流审查 | [工作流验收场景](WORKFLOW-REVIEW.md#cf24) |
| CF25 | 统一项目状态和操作决策 | 工作流审查 | [工作流验收场景](WORKFLOW-REVIEW.md#cf25) |
| CF26 | 续做项目保留历史 | 程序行为测试 | [test_core.ProjectLifecycleTests.test_create_resume_and_wrong_topic_preserve_project](../tests/test_core.py#L126) |
| CF27 | 原生工具、Agent 工作流及外部服务分别标注 | 工作流审查 | [工作流验收场景](WORKFLOW-REVIEW.md#cf27) |
| CF28 | 源码、文档和数据的来源分别登记 | 工作流审查 | [工作流验收场景](WORKFLOW-REVIEW.md#cf28) |
| CF29 | 格式合规与科学审查分工 | 工作流审查 | [工作流验收场景](WORKFLOW-REVIEW.md#cf29) |
| CF30 | 适配分与证据完整度分开 | 程序行为测试 | [test_core.VenueAuditTests.test_fit_requires_read_paper_current_assessment_and_current_verified_source](../tests/test_core.py#L554) |
| CF31 | 当前作者指南优先于排版样本 | 工作流审查 | [工作流验收场景](WORKFLOW-REVIEW.md#cf31) |
| CF32 | 更正材料与编辑决定分开 | 工作流审查 | [工作流验收场景](WORKFLOW-REVIEW.md#cf32) |
| CF33 | 文献纳入标准与投稿分区分开 | 工作流审查 | [工作流验收场景](WORKFLOW-REVIEW.md#cf33) |

## 从症状到修改

```text
症状/能力ID/源技能名称
  -> coverage_audit.py --find QUERY
  -> 工作流文件 + 支撑代码 + CF编号 + 测试入口
  -> 增加失败用例 -> 修改 -> 回归 -> 同步README/索引
```

```bash
python tools/coverage_audit.py --find "费用"
python tools/coverage_audit.py --find agent-systems
python tools/coverage_audit.py --find journal-recommender
python tools/coverage_audit.py --write
python tools/coverage_audit.py --check
python tests/run.py
```

新增领域：更新 `assets/domains.json` 和 `references/domains.md`，再做领域×阶段路由回归。
新增能力：更新 `assets/modules.json`、工作流正文、`assets/upstreams.json` 和本工具的测试/互补映射。
新增来源：记录完整提交、具体文件和特点，将其映射到现有或新增能力。
新增冲突：在 `conflicts.md` 登记稳定编号；程序行为增加回归，模型工作流增加输入、实际输出和审查记录。
新增接口：补正常、空值、错误、限流、版本、导入回滚和敏感字段检查。
