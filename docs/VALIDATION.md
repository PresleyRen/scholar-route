# ScholarRoute v1.0.0 验证记录

日期：2026-10-20。这里区分程序回归、包结构、全新 Agent 前向试用、真实 API 试探与科研实验。它们回答不同问题。

## 已取得的结果

| 验证 | 实际结果 | 能说明什么 |
|---|---|---|
| 本地自动化回归 | **89 项通过**；Python 3.12.14 | 在合成输入和受控响应下，核心实现与预期契约一致 |
| 组成 | 49 核心 + 24 接口 + 10 CLI/导入 + 6 本地证据/关系图 | 见下面测试范围 |
| 全新 Agent 前向试用 | 3 个独立任务；保留首次产物与问题 | 验证真实使用路径和文档可操作性，不是推荐准确率评测 |
| 官方技能结构检查 | `quick_validate.py` 返回 `Skill is valid!` | 技能元数据与基本结构符合检查器规则 |
| 本地包完整性 | 用 `tools/validate_package.py` 验证 | 名称、入口、参考链接、Python 语法、41 项映射及来源提交完整 |
| 文档同步 | `tools/update_readme.py --check` | README 三张注册表与 JSON 配置相符 |
| 真实论文 API | 首轮网络隔离失败；获准联网补测后 Crossref/arXiv 各解析 1 条记录，OpenAlex 为 429，DBLP 为非成功状态 | 两个成功的元数据烟雾测试；另外两个未验证成功检索，不代表全量检索或全文验证 |
| 科研实验、训练与投稿 | **未执行** | 本项目测试不会产生研究结论、录用率或真实投稿状态 |

最后一次本地回归输出：

```text
Ran 89 tests in 0.648s

OK
```

完整测试名与结果保存在 [test-output.txt](test-output.txt)。Python 3.11+ 是声明的最低运行范围；本地实际解释器为 3.12.14。GitHub Actions 的 **Python 3.11 与 3.12 两个任务均已成功**，包检查、文档同步、89 项回归和合成端到端示例全部通过。实际记录为 [run 39378341894](https://github.com/PresleyRen/scholar-route/actions/runs/39378341894)，对应 [源码提交 16d199d](https://github.com/PresleyRen/scholar-route/commit/16d199d261caf56a1feec9db0bbb20c00604044c)。后续文档补充不改变受测程序。

## 如何复现

在仓库根目录执行：

```bash
python tests/run.py
python tools/validate_package.py
python tools/update_readme.py --check
python skills/scholar-route/scripts/scholar_route.py doctor
python examples/run_demo.py --project ./work/validation-demo
python skills/scholar-route/scripts/scholar_route.py validate --project ./work/validation-demo
```

官方 `quick_validate.py` 来自创建环境的 `work-skill-creator`，不复制到本仓库，也不是使用者运行本项目的依赖。调用形式是：

```text
python <skill-creator>/scripts/quick_validate.py skills/scholar-route
```

可移植包检查器覆盖本项目需要的元数据、入口长度、文件与来源映射规则，不声称完全替代宿主安装器。

## 自动化回归范围

### 49 项核心测试

覆盖初始化与同主题恢复、限制合并、原子写入与锁、无变化重导入、修订历史、失效输入不改变项目、来源关系、DOI 规范化与别名、期刊 ISSN 身份、预印本/正式论文/版本区分、数值与日期、未知与冲突、费用条件变更、分区体系/年度/类别、出版社筛选及展示多样性、来源和适配评估新鲜度、报告一致性、CSV/BibTeX/Mermaid 输出和符号链接保护。

实际发现并修复的缺陷包括：异常输入泄漏类型错误、记录别名导致身份覆盖、费用金额不变时丢失条件冲突、历史结构校验不足、未知载体误判、过期适配来源仍参与排名，以及未核实出版社用于分组。测试只验证保存的证据属性，不判断网页是否真的支持科学事实。

### 24 项接口测试

OpenAlex、Crossref、DBLP、arXiv 的正常、空值、缺失字段、单条/多条形状、错误内容、HTTP 200 错误体、超时/网络错误、响应上限、服务忽略条数、DOI/版本、预印本身份、URL 编码、arXiv 明示查询语义、重定向和凭据处理。通过注入受控传输完成，不调用外部服务。

### 10 项 CLI / 导入测试

成功结果与失败结果的导入、整批原子性、无重复修订、保留阅读深度、预印本与期刊版本分开、拒绝带伪结果的错误包、批次上限、跨工作目录运行、缺文件的可读错误与 exit code。有效空查询与失败查询不混淆。

### 6 项本地证据 / 图谱测试

本地 `path + sha256` 来源可以支持范围明确的 claim；无须伪造 URL。检查错误路径/哈希、可选原始网址、报告中的本地版本标识、来源到主张的关联、检索记录和嵌套期刊事实的来源边，以及会议候选不被图表标签误写为期刊。

关系图扩展后，原有只计论文关联的测试出现预期不一致。已将断言改为准确核对全部六条已记录证据边，同时继续拒绝凭空添加关系；没有通过删除语义检查让测试变绿。

## 三次前向试用

每个任务交给没有创建过程上下文的全新 Agent，只提供技能入口、用户任务和原始案例文件。未传入理想答案、预先诊断或通过条件。案例均为本项目原创合成输入。前向试用是定性可用性检查，样本量不足以估计普遍成功率。

| 任务 | 首次实际表现 | 发现与后续处理 |
|---|---|---|
| [选刊案例](evaluations/venue-case.md) | A 满足记录条件；B 因费用未知待核实；C 是会议而排除。不会为满足“3 本”要求凑数；保留原始研究状态和历史 | 发现 MAP 使用集合标签“期刊”可能误标会议；实现改为中性“投稿候选”，并回归验证 |
| [领域探索案例](evaluations/field-case.md) | Agent/CS 与生物医学语境组合，17 条待执行中英查询、2 个研究问题、3 项 planned 实验、200 次未来模型调用预算；没有捏造检索或实证结果 | 首次 source 只接受网页，因此用本地快照与哈希保留证据。随后增加原生本地来源契约，保持首次报告不改写 |
| [本地证据案例](evaluations/local-evidence-case.md) | 新 Agent 成功将本地笔记作为 source 登记，区分笔记内容与已证明机制，导出五份文件并验证同主题恢复 | 发现图谱未显示来源/检索实体、stage 帮助未列可用值；随后补齐图谱与帮助文本，增加回归测试 |

这些首次试用文件保留当时的实现边界；其中描述的旧限制不表示发布实现仍有同样问题。新增修复由对应回归和导出检查验证，没有重写原始试用以制造“首次全部完美”的记录。

## 真实 API 试探

[live-smoke.json](live-smoke.json) 保留 provider、公开请求 URL、时间、计数、错误与警告。四个 provider 都在当前网络沙箱返回 `network_error`。记录中的 `count: 0` 是没有取得有效响应后的结构字段，不是科学意义上的零相关论文。

随后经自动审批允许访问公开网络，执行各 provider 一条 keyless 查询（limit 1、timeout 10）。Crossref 与 arXiv 成功解析响应；OpenAlex 返回 `http_429`，DBLP 返回 `http_error`。没有重试限流或失败来源。首次诊断包装仅保存了错误状态而遗漏记录数，因此又对两个成功来源各查询一次，保存规范化记录和 `completeness`，如实分开记录在 [live-smoke-authorized.json](live-smoke-authorized.json)。

最终 Crossref 和 arXiv 均保存了 1 条有效元数据记录，保留其预印本身份；该结果不证明相关性、科学结论或正式期刊收录。OpenAlex/DBLP 成功检索、全部提供方的鉴权访问、稳定可用性和全量分页仍未验证。使用时检查 `error`、`records` 与 `completeness`；需要认证时使用提供方允许的凭据和接口。

## 发布与安装边界

本任务获得了上传和发布 GitHub 的明确授权。原生技能保存路径位于创建环境的受保护 `/root/.codex` 目录；自动审批审查拒绝向该目录写入。因此实现改在可写项目中完成，并通过用户 GitHub 仓库持久发布。

这不影响公开仓库源码、文档、测试和版本交付。**没有声称已自动装入创建环境的个人技能列表**，也没有验证平台的隐式触发、插件目录上架或外部训练工具。安装说明见 [README](../README.md)。

## 仍需实际研究验证的内容

期刊官网与索引的实时事实、各候选的真实语义匹配、文献综述的覆盖程度、新颖性、科学主张、Agent 程序的实证性能，以及 Word/PDF/图表的实际渲染，都需要具体研究数据和相应工具。当前测试不对这些内容给出通过结论。
