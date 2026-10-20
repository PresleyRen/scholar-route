"""Evidence-aware journal constraint checks, not acceptance predictions."""
from __future__ import annotations

import datetime as dt

from project_store import validate_state


def _age(date: str) -> int:
    return (dt.datetime.now(dt.timezone.utc).date() - dt.date.fromisoformat(date[:10])).days


def _evidence(item: dict, sources: dict, allowed: set[str], max_age: int) -> tuple[bool, str]:
    if item.get("verification") != "verified":
        return False, "record_not_verified"
    if not item.get("checked_at"):
        return False, "missing_check_date"
    if _age(item["checked_at"]) > max_age:
        return False, "stale_fact"
    linked = [sources[s] for s in item.get("source_ids", []) if s in sources]
    suitable = [s for s in linked if s.get("verified") and s.get("type") in allowed
                and _age(s["accessed_at"]) <= max_age]
    if not suitable:
        return False, "no_current_primary_evidence"
    return True, "recorded_primary_evidence"


def _fact(journal: dict, name: str, sources: dict, max_age: int):
    fact = journal.get("facts", {}).get(name)
    if not fact or fact.get("value") is None:
        return None, "missing_value", fact or {}
    if any(c.get("field") == name and c.get("status") == "unresolved"
           for c in journal.get("conflicts", [])):
        return None, "unresolved_conflict", fact
    allowed = {"index"} if name == "indexing" else {"publisher", "registry"}
    valid, reason = _evidence(fact, sources, allowed, max_age)
    return (fact["value"] if valid else None), reason, fact


def _check(field: str, status: str, reason: str, evidence=None):
    return {"field": field, "status": status, "reason": reason,
            "source_ids": (evidence or {}).get("source_ids", [])}


def assess_journal(journal: dict, constraints: dict, sources: dict, papers: dict | None = None) -> dict:
    checks = []
    max_age = constraints.get("max_fact_age_days", 180)
    if not journal.get("issns"):
        checks.append(_check("identity", "unknown", "ISSN identity is missing."))
    else:
        linked = [sources[s] for s in journal.get("source_ids", []) if s in sources]
        good = [s for s in linked if s.get("verified") and s["type"] in {"publisher", "index", "registry"}
                and _age(s["accessed_at"]) <= max_age]
        checks.append(_check("identity", "pass" if good else "unknown",
                             "Recorded ISSN provenance." if good else "ISSN lacks current primary provenance.",
                             {"source_ids": [s["id"] for s in good]}))
    if constraints.get("require_journal", True):
        value, reason, fact = _fact(journal, "venue_type", sources, max_age)
        if value == "unknown":
            value, reason = None, "venue_type_unknown"
        status = "unknown" if value is None else ("pass" if value == "journal" else "fail")
        checks.append(_check("venue_type", status, reason if value is None else str(value), fact))
    if constraints.get("required_index"):
        value, reason, fact = _fact(journal, "indexing", sources, max_age)
        required = constraints["required_index"].casefold()
        status = "unknown" if value is None else ("pass" if required in {i.casefold() for i in value} else "fail")
        checks.append(_check("indexing", status,
                             reason if value is None else "Required " + constraints["required_index"] + "; recorded " + ", ".join(value), fact))
    if "max_mandatory_fee" in constraints:
        cap = constraints["max_mandatory_fee"]
        value, reason, fact = _fact(journal, "mandatory_fee", sources, max_age)
        if value is None:
            status = "unknown"
        elif fact.get("includes_all_mandatory") is not True:
            status, reason = "unknown", "Not all mandatory charges have been checked."
        elif fact.get("conditional"):
            status, reason = "unknown", "Fee depends on an unconfirmed waiver or condition."
        elif fact.get("currency") != cap["currency"] and value != 0:
            status, reason = "unknown", "Currency differs; record an evidenced conversion or a matching-currency budget."
        else:
            status = "pass" if value <= cap["amount"] else "fail"
            reason = "Mandatory total " + str(value) + " " + fact["currency"]
        checks.append(_check("mandatory_fee", status, reason, fact))
    if constraints.get("excluded_publishers"):
        value, reason, fact = _fact(journal, "publisher", sources, max_age)
        status = "unknown" if value is None else (
            "fail" if value.casefold() in {x.casefold() for x in constraints["excluded_publishers"]} else "pass")
        checks.append(_check("publisher", status, reason if value is None else value, fact))
    if constraints.get("allowed_languages"):
        value, reason, fact = _fact(journal, "languages", sources, max_age)
        allowed = {x.casefold() for x in constraints["allowed_languages"]}
        status = "unknown" if value is None else ("pass" if allowed.intersection(x.casefold() for x in value) else "fail")
        checks.append(_check("languages", status, reason if value is None else ", ".join(value), fact))
    if constraints.get("quartile"):
        desired = constraints["quartile"]
        candidates = [m for m in journal.get("metrics", []) if
                      all(m.get(f) == desired[f] for f in ("system", "year", "category"))]
        valid = [m for m in candidates if _evidence(m, sources, {"index"}, max_age)[0]]
        values = {m["value"] for m in valid}
        if len(values) > 1:
            status, reason = "unknown", "Contradictory values for the same system/year/category."
        elif not values:
            status, reason = "unknown", "No current evidence for the exact system/year/category."
        else:
            value = next(iter(values))
            status, reason = ("pass" if value in desired["allowed"] else "fail"), value
        checks.append(_check("quartile", status, reason,
                             {"source_ids": sorted({s for m in valid for s in m.get("source_ids", [])})}))
    statuses = {c["status"] for c in checks}
    status = "excluded" if "fail" in statuses else ("unverified" if "unknown" in statuses else "eligible")
    fit = journal.get("fit")
    papers = papers or {}
    fit_usable = bool(fit and fit.get("source_ids") and fit.get("paper_ids")
                      and _age(fit["assessed_at"]) <= max_age
                      and any(sources[s].get("verified") and _age(sources[s]["accessed_at"]) <= max_age
                              for s in fit["source_ids"] if s in sources)
                      and any(papers[p].get("read_status") in {"abstract", "full_text"}
                              for p in fit["paper_ids"] if p in papers))
    publisher, _, _ = _fact(journal, "publisher", sources, max_age)
    return {
        "id": journal["id"], "title": journal["title"], "status": status, "checks": checks,
        "fit_score": fit["score"] if fit_usable else None,
        "fit_rationale": fit["rationale"] if fit_usable else None,
        "fit_source_ids": fit.get("source_ids", []) if fit_usable else [],
        "fit_paper_ids": fit.get("paper_ids", []) if fit_usable else [],
        "publisher": publisher if isinstance(publisher, str) and publisher else None,
        "evidence_coverage": {"passed": sum(c["status"] == "pass" for c in checks), "required": len(checks)},
        "limits": [
            "Eligibility checks recorded constraints and provenance; the host must verify that sources support the facts.",
            "Fit is a human/host 0–5 judgment, not a calibrated acceptance probability.",
        ],
    }


def shortlist(rows: list[dict], limit: int = 5, publisher_cap: int = 2) -> dict:
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 50:
        raise ValueError("Shortlist limit must be an integer from 1 to 50.")
    if isinstance(publisher_cap, bool) or not isinstance(publisher_cap, int) or not 1 <= publisher_cap <= 50:
        raise ValueError("Publisher cap must be an integer from 1 to 50.")
    candidates = [r for r in rows if r["status"] == "eligible" and r["fit_score"] is not None]
    candidates.sort(key=lambda r: (-r["fit_score"], r["title"].casefold(), r["id"]))
    selected, deferred, counts = [], [], {}
    for row in candidates:
        # Unknown publisher is not treated as an independent publisher.
        key = (row.get("publisher") or "__unknown__").casefold()
        if counts.get(key, 0) >= publisher_cap:
            deferred.append(row["id"])
            continue
        if len(selected) < limit:
            selected.append(row["id"])
            counts[key] = counts.get(key, 0) + 1
    return {
        "ids": selected, "publisher_cap": publisher_cap,
        "deferred_for_diversity": deferred,
        "unranked_eligible": [r["id"] for r in rows if r["status"] == "eligible" and r["fit_score"] is None],
        "note": "A heuristic fit ordering with a soft display diversity cap; all candidates remain in their pools.",
    }


def assess(state: dict, limit: int = 5) -> dict:
    validate_state(state)
    sources = {s["id"]: s for s in state["records"]["sources"]}
    papers = {p["id"]: p for p in state["records"]["papers"]}
    rows = [assess_journal(j, state["constraints"], sources, papers) for j in state["records"]["journals"]]
    return {
        "project_revision": state["revision"],
        "constraints": state["constraints"],
        "pools": {pool: [r for r in rows if r["status"] == pool]
                  for pool in ("eligible", "unverified", "excluded")},
        "shortlist": shortlist(rows, limit),
        "assessed_count": len(rows),
        "acceptance_probability": None,
        "notice": "No acceptance probability is calculated. Missing evidence remains visible.",
    }
