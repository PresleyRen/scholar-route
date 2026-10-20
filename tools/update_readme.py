"""Regenerate the three README registry tables; --check is read-only for CI."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "skills" / "scholar-route" / "assets"

# Public outcomes; technical execution contracts remain in module references.
OUTCOMES = {'intake': '研究目标、贡献类型、稿件阶段、语言、预算和已有证据清单。',
 'field-map': '问题—方法—证据—研究缺口地图，以及下一轮探索入口。',
 'search-protocol': '中英文查询词、数据库路线、时间范围、筛选标准与查询日志。',
 'paper-search': '多源论文记录、检索状态与来源信息；四个原生 API 统一导入。',
 'identifier-check': 'DOI、ISSN、元数据、预印本和正式版本的身份与关联记录。',
 'evidence-review': '文献筛选表、证据提取表、质量评价和跨研究综合。',
 'paper-notes': '问题、机制、数据、结果、代码和主张关联的精读笔记。',
 'novelty-audit': '最近竞争方法、相邻领域先例、创新差异和反证清单。',
 'hypothesis-plan': '可证伪假设、机制解释、可行性分析与最小验证实验。',
 'agent-capabilities': '14 类 Agent 能力的机制拆解、比较基线和评价协议。',
 'agent-systems': '8 个程序层的架构分析、故障模型、运行轨迹与系统实验。',
 'experiment-plan': '变量、对照、消融、指标、样本、资源预算和停止条件。',
 'statistics-robustness': '统计单位、置信区间、混杂、泄漏、多重比较与稳健性检查。',
 'implementation': '基线复现、最小机制实现、等预算运行与命令和结果记录。',
 'data-collection': '数据出处、许可、采样、版本、质量、拆分和再利用计划。',
 'state-map': '持久项目账本、关系图、版本历史、断点恢复与报告导出。',
 'manuscript-profile': '研究问题、贡献、方法角色、证据、读者和文章类型画像。',
 'venue-discovery': '由相似论文、专业刊、出版社匹配器及索引合并生成候选池。',
 'venue-identity': '刊名、ISSN、出版社、官方入口、改名记录与发表载体类型。',
 'journal-dossier': '单刊范围、同刊先例、文章类型、费用、时间和作者要求档案。',
 'indexing-metrics': '按体系、年度和学科类别保存索引身份与分区事实。',
 'costs-timelines': '必缴费用、可选 OA、减免条件、货币与不同审稿时间端点。',
 'journal-integrity': '期刊身份、政策透明度、同行评审与出版风险的具体证据。',
 'fit-comparison': '符合、待核实、排除三类候选，以及各项条件和适配比较理由。',
 'submission-plan': '可解释的主投/备选顺序、补强任务和改投触发条件。',
 'argument-audit': '问题—机制—实验—结论的论证链，以及缺少比较和逻辑跳步。',
 'manuscript-writing': '中文或英文论文段落、润色与结构调整，保持数值、术语和引用一致。',
 'citation-audit': '引用身份、版本、内容支持和位置检查，以及 BibTeX 整理。',
 'figure-table-audit': '图表数据、单位、样本数、标注、可读性与目标刊要求检查。',
 'peer-review': '多视角模拟审稿、关键异议、证据定位和可执行修改建议。',
 'venue-formatting': '当前作者指南、文章类型要求、模板适配和改投排版清单。',
 'cover-letter': '围绕真实贡献与期刊范围撰写的投稿信。',
 'presubmission-inquiry': '具有明确适配问题和研究摘要的投稿前询问信。',
 'reviewer-discovery': '按专长、论文和利益冲突条件组织的审稿人候选资料。',
 'authorship-credit': '作者实际贡献、CRediT 角色和声明的统一记录。',
 'submission-preflight': 'Quick/Full 两级稿件、图表、声明、附件与数据代码预检。',
 'revision-response': '逐条意见、回复、实际改动与稿件定位的返修对照表。',
 'proof-check': '录用稿与清样的文字、数值、公式、署名、引用和排版差异。',
 'dissemination': '基于发表结果的通俗摘要、海报、展示与公开材料草稿。',
 'postpublication-correction': '错误影响分析、证据整理和更正沟通材料。',
 'regional-indexing': '中文和土耳其期刊的目录、身份与地区投稿路线。'}


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def render(text):
    modules = json.loads((ASSETS / "modules.json").read_text(encoding="utf-8"))
    domains = json.loads((ASSETS / "domains.json").read_text(encoding="utf-8"))
    sources = json.loads((ASSETS / "upstreams.json").read_text(encoding="utf-8"))["sources"]
    blocks = {
        "DOMAINS": ["| 配置 ID | 领域 | 首选来源路线（原生与宿主来源合并列示） |",
                    "|---|---|---|"],
        "CAPABILITIES": ["| 能力 ID | 能力 | 具体产物 |", "|---|---|---|"],
        "SOURCES": ["| 来源仓库 | 映射条目 | 参考提交 | 许可证声明 |", "|---|---:|---|---|"],
    }
    for domain in domains:
        blocks["DOMAINS"].append("| `" + domain["id"] + "` | " + cell(domain["title"]) +
                                 " | " + cell("、".join(domain["sources"])) + " |")
    for module in modules:
        if module["id"] not in OUTCOMES:
            raise ValueError("Missing README outcome: " + module["id"])
        blocks["CAPABILITIES"].append("| `" + module["id"] + "` | [" + cell(module["title"]) +
                                      "](skills/scholar-route/" + module["reference"] + ") | " +
                                      cell(OUTCOMES[module["id"]]) + " |")
    for source in sources:
        sha = source["reference_commit"]
        license_text = source["license"]["declaration"]
        if license_text == "not found":
            license_text = "未发现许可证"
        blocks["SOURCES"].append("| [" + source["repository"] + "](" + source["url"] + ") | " +
                                  str(len(source["modules"])) + " | [" + sha[:10] + "](" +
                                  source["url"].rstrip("/") + "/commit/" + sha + ") | " + cell(license_text) + " |")
    for name, lines in blocks.items():
        start, end = "<!-- " + name + ":START -->", "<!-- " + name + ":END -->"
        if text.count(start) != 1 or text.count(end) != 1:
            raise ValueError("README needs exactly one marker pair for " + name)
        before, rest = text.split(start, 1)
        _, after = rest.split(end, 1)
        text = before + start + "\n\n" + "\n".join(lines) + "\n\n" + end + after
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    readme = ROOT / "README.md"
    current = readme.read_text(encoding="utf-8")
    updated = render(current)
    if args.check:
        print("README registry tables are current." if updated == current else
              "README tables need regeneration: python tools/update_readme.py")
        return 0 if updated == current else 1
    readme.write_text(updated, encoding="utf-8")
    print("Updated domain, capability and provenance tables.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
