"""Domain and stage routing for ScholarRoute. Suggestions, never semantic certainty."""
from __future__ import annotations

import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
STAGES = ("explore", "review", "design", "experiment", "journal", "dossier",
          "write", "audit", "submit", "revise", "disseminate", "full")
REGIONS = ("international", "china", "turkey")
STAGE_ALIASES = {
    "探索": "explore", "综述": "review", "设计": "design", "实验": "experiment",
    "选刊": "journal", "单刊": "dossier", "写作": "write", "审查": "audit",
    "投稿": "submit", "返修": "revise", "传播": "disseminate", "全流程": "full",
    "审刊": "dossier", "查单刊": "dossier", "核稿": "audit", "all": "full",
}


def asset(name: str):
    return json.loads((SKILL_ROOT / "assets" / name).read_text(encoding="utf-8"))


def _matches(topic: str, word: str) -> bool:
    if re.fullmatch(r"[a-zA-Z0-9 -]+", word):
        return re.search(r"(?<![a-z0-9])" + re.escape(word.lower()) +
                         r"(?![a-z0-9])", topic.lower()) is not None
    return word.casefold() in topic.casefold()


def _normalize(text: str) -> str:
    return re.sub(r"[\s\-\u2010-\u2015]+", " ", unicodedata.normalize("NFKC", text).casefold()).strip()


@lru_cache(maxsize=512)
def _track_pattern(word: str):
    normalized = _normalize(word)
    pattern = re.escape(normalized)
    if normalized[0].isascii() and normalized[0].isalnum():
        pattern = r"(?<![a-z0-9])" + pattern
    if normalized[-1].isascii() and normalized[-1].isalnum():
        pattern += r"(?![a-z0-9])"
    return re.compile(pattern)


def journal_tracks(topic: str) -> dict:
    """Suggest audiences from named tasks and metrics. Conflicting endpoints need a main result."""
    topic = _normalize(topic)
    candidates = []
    for track in asset("journal-tracks.json"):
        def hits(field):
            return [word for word in track.get(field, []) if _track_pattern(word).search(topic)]

        context = hits("context")
        if "context" in track and not context:
            continue
        tasks, outcomes = hits("terms"), hits("outcomes")
        metric_context = hits("metric_context")
        extra_outcomes = hits("contextual_outcomes")
        if metric_context and extra_outcomes:
            outcomes.extend(extra_outcomes)
            context.extend(metric_context)
        if tasks or outcomes:
            candidates.append({
                "id": track["id"], "title": track["title"], "domain": track["domain"],
                "signals": list(dict.fromkeys(tasks + outcomes + context)),
                "outcomes": outcomes, "check": track["check"],
            })
    contenders = [item for item in candidates if item["outcomes"]] or candidates
    primary = contenders[0]["id"] if len(contenders) == 1 else None
    return {"primary": primary, "candidates": candidates}


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
    journal_stage = stage in ("full", "journal", "dossier", "submit")
    tracks = journal_tracks(topic) if journal_stage or not domains else None
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
            domain_topic = topic.casefold()
            for phrase in domain.get("ignore_phrases", []):
                domain_topic = domain_topic.replace(phrase.casefold(), " ")
            hits = [word for word in domain["keywords"] if _matches(domain_topic, word)]
            if hits:
                signals[domain["id"]] = hits
        for candidate in tracks["candidates"]:
            found = signals.setdefault(candidate["domain"], [])
            found.extend(word for word in candidate["signals"] if word not in found)
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
        **({"journal_tracks": tracks} if journal_stage else {}),
        "module_details": chosen,
        "references": list(dict.fromkeys(m["reference"] for m in chosen)),
        "sources": list(dict.fromkeys(source_names)), "skipped": skipped,
        "warnings": warnings,
    }
