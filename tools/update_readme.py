"""Regenerate the three README registry tables; --check is read-only for CI."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "skills" / "scholar-route" / "assets"


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def render(text):
    modules = json.loads((ASSETS / "modules.json").read_text(encoding="utf-8"))
    domains = json.loads((ASSETS / "domains.json").read_text(encoding="utf-8"))
    sources = json.loads((ASSETS / "upstreams.json").read_text(encoding="utf-8"))["sources"]
    blocks = {
        "DOMAINS": ["| 配置 ID | 领域 | 首选来源路线（原生与宿主来源合并列示） |",
                    "|---|---|---|"],
        "CAPABILITIES": ["| 能力 ID | 能力 | 具体产物与边界 |", "|---|---|---|"],
        "SOURCES": ["| 来源仓库 | 映射条目 | 参考提交 | 许可证声明 |", "|---|---:|---|---|"],
    }
    for domain in domains:
        blocks["DOMAINS"].append("| `" + domain["id"] + "` | " + cell(domain["title"]) +
                                 " | " + cell("、".join(domain["sources"])) + " |")
    for module in modules:
        if not module.get("description"):
            raise ValueError("Missing capability description: " + module["id"])
        blocks["CAPABILITIES"].append("| `" + module["id"] + "` | [" + cell(module["title"]) +
                                      "](skills/scholar-route/" + module["reference"] + ") | " +
                                      cell(module["description"]) + " |")
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
