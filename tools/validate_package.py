"""Portable packaging and provenance integrity checks; no third-party imports."""
import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "scholar-route"


def validate():
    errors = []
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    front = text.split("---", 2)
    if len(front) != 3 or not text.startswith("---\n"):
        errors.append("SKILL.md needs frontmatter.")
    else:
        fields = {line.split(":", 1)[0].strip() for line in front[1].splitlines() if ":" in line}
        if fields != {"name", "description"}:
            errors.append("Frontmatter must contain only name and description.")
        if "name: scholar-route" not in front[1]:
            errors.append("Skill name mismatch.")
    if len(text.splitlines()) >= 500:
        errors.append("Main skill must stay below 500 lines.")
    if re.search(r"\[TODO[^\]]*\]", text):
        errors.append("Unfinished initializer text.")
    modules = json.loads((SKILL / "assets/modules.json").read_text())
    ids = [m["id"] for m in modules]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate capability IDs.")
    for m in modules:
        path = SKILL / m["reference"]
        if not path.is_file():
            errors.append("Missing module reference: " + m["reference"])
        if m["reference"] not in text:
            errors.append("Main skill does not directly expose " + m["reference"])
    upstreams = json.loads((SKILL / "assets/upstreams.json").read_text())
    used = set()
    for source in upstreams["sources"]:
        if not re.fullmatch(r"[a-f0-9]{40}", source.get("reference_commit", "")):
            errors.append("Source lacks a pinned commit: " + source["id"])
        if source.get("upstream_runtime_tested") is not False:
            errors.append("Do not imply upstream packages were run: " + source["id"])
        for m in source["modules"]:
            used.update(m["capability_ids"])
    if used != set(ids):
        errors.append("Provenance/capability mapping mismatch.")
    for path in SKILL.rglob("*.py"):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for path in [ROOT / "README.md", ROOT / "LICENSE", ROOT / "docs/source-audit.md",
                 ROOT / "docs/VALIDATION.md", SKILL / "agents/openai.yaml"]:
        if not path.is_file():
            errors.append("Missing deliverable: " + str(path.relative_to(ROOT)))
    for path in [SKILL / "SKILL.md", *list((SKILL / "references").glob("*.md")), ROOT / "README.md"]:
        if not path.is_file():
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if target.startswith(("http:", "https:", "#", "mailto:")):
                continue
            target = target.split("#", 1)[0]
            if target and not (path.parent / target).exists():
                errors.append("Broken local link in " + str(path.relative_to(ROOT)) + ": " + target)
    metadata = (SKILL / "agents/openai.yaml").read_text(encoding="utf-8")
    if "$scholar-route" not in metadata:
        errors.append("Agent default prompt must name the skill.")
    conflicts = (SKILL / "references/conflicts.md").read_text(encoding="utf-8")
    conflict_ids = re.findall(r"\| (CF\d+) \|", conflicts)
    if len(conflict_ids) != len(set(conflict_ids)):
        errors.append("Duplicate conflict IDs.")
    return {"ok": not errors, "errors": errors, "modules": len(ids),
            "domains": len(json.loads((SKILL / "assets/domains.json").read_text())),
            "source_repositories": len(upstreams["sources"]),
            "source_mappings": sum(len(s["modules"]) for s in upstreams["sources"]),
            "conflict_rules": len(conflict_ids)}


if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["ok"] else 1)
