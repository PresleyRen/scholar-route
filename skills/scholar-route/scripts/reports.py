"""Readable, traceable exports from a validated ScholarRoute project."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import re
import tempfile
from pathlib import Path

from project_store import fingerprint, load_project, locked, now
from route_core import route
from venue_audit import assess


def md(value) -> str:
    text = str(value if value is not None else "未核实")
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace("\n", " ").replace("<", "&lt;").replace(">", "&gt;")


def graph_label(value) -> str:
    return re.sub(r'[\x00-\x1f\x7f\x60"\\<>;{}\[\]|]', " ", str(value))[:100].replace("&", " and ")


def _write(path: Path, text: str):
    if path.is_symlink():
        raise ValueError("Refusing to overwrite a symlinked report.")
    fd, tmp = tempfile.mkstemp(prefix=".scholar-route-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def map_markdown(state: dict) -> str:
    records = state["records"]
    lines = ["# 研究证据关系图", "", "项目：" + md(state["topic"]), "",
             "本图只显示已经记录的关系；箭头表示记录关联，不代表因果证明或实验成功。", ""]
    kinds = {"sources": ("S", "来源"), "searches": ("Q", "检索"),
             "papers": ("P", "论文"), "claims": ("C", "主张"),
             "hypotheses": ("H", "假设"), "experiments": ("E", "实验"),
             "decisions": ("D", "决策"), "journals": ("J", "投稿候选")}
    nodes, edges, all_records = {}, [], []
    for pool, (prefix, title) in kinds.items():
        for index, record in enumerate(records[pool]):
            key = (pool, record["id"])
            nodes[key] = prefix + str(index + 1)
            all_records.append((pool, title, record))
    links = {"source_ids": "sources", "paper_ids": "papers", "claim_ids": "claims",
             "hypothesis_ids": "hypotheses", "experiment_ids": "experiments",
             "journal_ids": "journals"}
    for pool, _, record in all_records:
        for field, target_pool in links.items():
            for source in record.get(field, []):
                if (target_pool, source) in nodes:
                    edges.append((nodes[(target_pool, source)], nodes[(pool, record["id"])]))
        if pool == "journals":
            evidence = [record.get("fit", {}), *record.get("facts", {}).values(),
                        *record.get("metrics", [])]
            for item in evidence:
                for field, target_pool in (("source_ids", "sources"), ("paper_ids", "papers")):
                    for source in item.get(field, []):
                        if (target_pool, source) in nodes:
                            edges.append((nodes[(target_pool, source)], nodes[(pool, record["id"])]))
    edges = list(dict.fromkeys(edges))
    shown = edges[:60]
    connected = {n for e in shown for n in e}
    if shown:
        lines += ["\x60\x60\x60mermaid", "flowchart TD"]
        for pool, title, record in all_records:
            node = nodes[(pool, record["id"])]
            if node in connected:
                content = record.get("title", record.get("text", record.get("query", record["id"])))
                label = graph_label(title + ": " + content)
                lines.append('    ' + node + '["' + label + '"]')
        lines += ["    " + a + " --> " + b for a, b in shown]
        lines += ["\x60\x60\x60", ""]
        if len(edges) > len(shown):
            lines += ["图中仅显示前 60 条关系；完整关系保存在 project.json。", ""]
    else:
        lines += ["尚未记录实体间关系。先关联来源、论文、主张、假设和实验，再生成关系图。", ""]
    lines += ["| 类型 | ID | 内容 | 状态 |", "|---|---|---|---|"]
    for pool, title, record in all_records:
        lines.append("| " + " | ".join(md(x) for x in (
            title, record["id"], record.get("title", record.get("text", record.get("query", record["id"]))),
            record.get("status", record.get("read_status", "记录")))) + " |")
    return "\n".join(lines) + "\n"


def bibtex(state: dict) -> str:
    def escape(value):
        chars = {"\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "&": r"\&",
                 "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
                 "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
        return "".join(chars.get(c, c) for c in str(value)).replace("\n", " ")
    chunks = ["% Generated from recorded metadata; verify citation support and venue style.\n"]
    for paper in state["records"]["papers"]:
        kind = {"journal": "article", "conference": "inproceedings"}.get(paper.get("venue_type"), "misc")
        key = re.sub(r"[^A-Za-z0-9_-]", "-", paper["id"])[:60]
        key += "-" + hashlib.sha256(paper["id"].encode()).hexdigest()[:8]
        values = {"title": paper["title"]}
        if paper.get("authors"):
            values["author"] = " and ".join(paper["authors"])
        if paper.get("year"):
            values["year"] = paper["year"]
        if paper.get("venue"):
            values["booktitle" if kind == "inproceedings" else ("journal" if kind == "article" else "howpublished")] = paper["venue"]
        if paper.get("doi"):
            values["doi"] = paper["doi"]
        if paper.get("url"):
            values["url"] = paper["url"]
        fields = ["  " + field + " = {" + escape(value) + "}" for field, value in values.items()]
        chunks.append("@" + kind + "{" + key + ",\n" + ",\n".join(fields) + "\n}\n")
    return "\n".join(chunks)


def report_markdown(state: dict, audit: dict) -> str:
    routing = route(state["topic"], state["domains"], state["stage"], state["region"])
    lines = [
        "# ScholarRoute 研究与投稿记录", "", "**主题：** " + md(state["topic"]), "",
        "**生成时间：** " + now() + "  \n**项目版本：** " + str(state["revision"]),
        "", "**数据指纹：** " + fingerprint(state), "",
        "这是基于项目记录生成的工作报告。结构检查不能证明源网页支持某个事实，也不预测录用率。", "",
        "## 路由与当前工作", "",
        "- 领域：" + "、".join(state["domains"]),
        "- 阶段：" + state["stage"],
        "- 适用模块：" + str(len(routing["modules"])),
        "- 模块清单：" + "、".join(routing["modules"]), "",
        "## 记录统计", "",
        "| 记录 | 数量 |", "|---|---|",
    ]
    lines += ["| " + pool + " | " + str(len(items)) + " |" for pool, items in state["records"].items()]
    lines += ["", "## 期刊筛选", "", "以下分组只检查已记录的硬约束。适配分是 0–5 的主观、有依据评估；空值不补分。", ""]
    for pool, title in (("eligible", "符合已记录约束"), ("unverified", "待核实"), ("excluded", "已知不符合")):
        lines += ["### " + title, "", "| 投稿候选 | ID | 适配分 | 检查结果 |", "|---|---|---|---|"]
        for row in audit["pools"][pool]:
            reasons = "; ".join(c["field"] + ": " + c["status"] + " (" + c["reason"] + ")" for c in row["checks"])
            lines.append("| " + " | ".join(md(x) for x in (
                row["title"], row["id"], row["fit_score"], reasons)) + " |")
        if not audit["pools"][pool]:
            lines += ["| — | — | — | 尚无记录 |"]
        lines += [""]
    lines += ["### 待人工复核的建议顺序", "",
              "、".join(audit["shortlist"]["ids"]) or "暂无同时具备完整硬约束证据和适配评估的候选。",
              "", "同出版社展示上限：" + str(audit["shortlist"]["publisher_cap"]) +
              "；被延后或未评分的期刊仍保留在完整候选池。", ""]
    lines += ["## 主张、假设与实验", "", "| 类型 | ID | 内容 | 状态 |", "|---|---|---|---|"]
    for pool in ("claims", "hypotheses", "experiments", "decisions"):
        for r in state["records"][pool]:
            lines.append("| " + " | ".join(md(v) for v in (pool, r["id"], r["text"], r["status"])) + " |")
    lines += ["", "## 检索边界", ""]
    if not state["records"]["searches"]:
        lines += ["尚未记录检索。不能据此声称已覆盖某个领域。", ""]
    else:
        lines += ["| 检索 | 来源 | 查询 | 时间 | 完整性 |", "|---|---|---|---|---|"]
        for r in state["records"]["searches"]:
            lines.append("| " + " | ".join(md(v) for v in (
                r["id"], r["provider"], r["query"], r["retrieved_at"],
                r.get("coverage_proof") if r.get("exhaustive") else "有边界；不声称穷尽")) + " |")
        lines += [""]
    lines += ["## 证据来源", "", "| ID | 来源 | 类型 | 访问日期 | 记录核实状态 |", "|---|---|---|---|---|"]
    for source in state["records"]["sources"]:
        if source.get("url"):
            location = "<" + source["url"].replace(">", "%3E").replace("|", "%7C") + ">"
        else:
            location = "local: " + md(source["path"]) + " (sha256: " + source["sha256"] + ")"
        lines.append("| " + " | ".join([
            md(source["id"]), md(source["title"]) + " — " + location,
            md(source["type"]), md(source["accessed_at"]), "已记录核实" if source.get("verified") else "未核实"]) + " |")
    lines += ["", "## 当前边界", "",
              "- 报告保留事实来源和缺失项；科学主张是否成立、期刊是否真实适配仍需阅读原始证据。",
              "- first_decision、external_review、acceptance、publication 时间不得混用；历史统计不是截止时间保证。",
              "- 任何尚未实际执行的实验、提交、发表或通信均不能由本报告自动变成已完成。",
              "- 研究关系见 MAP.md；规范化记录及历史见 project.json；引文元数据见 references.bib。", ""]
    return "\n".join(lines)


def export_project(project: str | Path) -> dict:
    project = Path(project).expanduser().resolve()
    with locked(project):
        state = load_project(project)
        audit = assess(state)
        output = io.StringIO(newline="")
        writer = csv.writer(output)
        writer.writerow(["id", "title", "status", "fit_score", "publisher", "reasons"])
        for rows in audit["pools"].values():
            for row in rows:
                values = [row["id"], row["title"], row["status"], row["fit_score"], row["publisher"],
                          "; ".join(c["reason"] for c in row["checks"])]
                writer.writerow(["'" + v if isinstance(v, str) and v.lstrip().startswith(("=", "+", "-", "@")) else v for v in values])
        files = {
            "REPORT.md": report_markdown(state, audit), "MAP.md": map_markdown(state),
            "journals.csv": output.getvalue(), "references.bib": bibtex(state),
            "assessment.json": json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
        }
        for filename in files:
            if (project / filename).is_symlink():
                raise ValueError("Refusing a symlinked output: " + filename)
        for filename, content in files.items():
            _write(project / filename, content)
    return {"project_revision": state["revision"], "fingerprint": fingerprint(state),
            "files": [str(project / name) for name in files]}
