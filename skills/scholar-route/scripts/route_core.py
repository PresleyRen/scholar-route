"""Domain and stage routing for ScholarRoute. Suggestions, never semantic certainty."""
from __future__ import annotations

import json
import re
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
STAGES = ("explore", "review", "design", "experiment", "journal", "dossier",
          "write", "audit", "submit", "revise", "disseminate", "full")
REGIONS = ("international", "china", "turkey")
STAGE_ALIASES = {
    "探索": "explore", "综述": "review", "设计": "design", "实验": "experiment",
    "选刊": "journal", "单刊": "dossier", "写作": "write", "审查": "audit",
    "投稿": "submit", "返修": "revise", "传播": "disseminate", "全流程": "full",
    "all": "full",
}


def asset(name: str):
    return json.loads((SKILL_ROOT / "assets" / name).read_text(encoding="utf-8"))


def _matches(topic: str, word: str) -> bool:
    if re.fullmatch(r"[a-zA-Z0-9 -]+", word):
        return re.search(r"(?<![a-z0-9])" + re.escape(word.lower()) +
                         r"(?![a-z0-9])", topic.lower()) is not None
    return word.casefold() in topic.casefold()


def route(topic: str, domains: list[str] | None = None,
          stage: str = "full", region: str = "international") -> dict:
    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("A nonempty research topic is required.")
    if not isinstance(stage, str):
        raise ValueError("Stage must be a string.")
    if not isinstance(region, str):
        raise ValueError("Region must be a string.")
    if domains is not None and (not isinstance(domains, list) or
                                any(not isinstance(d, str) or not d.strip() for d in domains)):
        raise ValueError("Domains must be a list of domain identifiers.")
    stage = STAGE_ALIASES.get(stage, stage)
    if stage not in STAGES:
        raise ValueError("Unknown stage. Choose: " + ", ".join(STAGES))
    if region not in REGIONS:
        raise ValueError("Unknown region. Choose: " + ", ".join(REGIONS))
    profiles = asset("domains.json")
    modules = asset("modules.json")
    available = {d["id"]: d for d in profiles}
    signals = {}
    explicit = bool(domains)
    if explicit:
        unknown = set(domains) - available.keys()
        if unknown:
            raise ValueError("Unknown domain(s): " + ", ".join(sorted(unknown)))
        selected = list(dict.fromkeys(domains))
    else:
        for domain in profiles:
            hits = [word for word in domain["keywords"] if _matches(topic, word)]
            if hits:
                signals[domain["id"]] = hits
        selected = list(signals) or ["general"]
    if "agent-ai" in selected and "computer-science" not in selected:
        selected.append("computer-science")
    # General is a fallback, not a reason to load every specialist profile.
    if len(selected) > 1 and "general" in selected:
        selected.remove("general")
    chosen, skipped = [], []
    for module in modules:
        reason = None
        if stage != "full" and stage not in module["stages"]:
            reason = "outside_requested_stage"
        elif module.get("domains") and not set(selected).intersection(module["domains"]):
            reason = "domain_specific"
        elif module.get("regions") and region not in module["regions"]:
            reason = "regional_only"
        if reason:
            skipped.append({"id": module["id"], "reason": reason})
        else:
            chosen.append(module)
    source_names = list(dict.fromkeys(
        source for d in selected for source in available[d]["sources"]))
    if region == "china":
        source_names.extend(["NPPA", "CNKI", "Wanfang", "VIP", "CSSCI/CSCD catalogs"])
    elif region == "turkey":
        source_names.extend(["TR Dizin", "DergiPark"])
    warnings = []
    if not explicit:
        warnings.append("Keyword routing is a suggestion; confirm the actual research object and methods.")
    if len(selected) > 1:
        warnings.append("Apply every selected domain's relevant evidence standards; designate a primary contribution.")
    return {
        "topic": topic.strip(), "stage": stage, "region": region,
        "domains": selected, "selection": "explicit" if explicit else "keyword_suggestion",
        "signals": signals, "modules": [m["id"] for m in chosen],
        "module_details": chosen,
        "references": list(dict.fromkeys(m["reference"] for m in chosen)),
        "sources": list(dict.fromkeys(source_names)), "skipped": skipped,
        "warnings": warnings,
    }
