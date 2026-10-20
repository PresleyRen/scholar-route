"""Atomic import of a bounded search result into a local evidence project."""
from __future__ import annotations

import copy
import hashlib
from pathlib import Path

from project_store import (KINDS, _merge, _same_identity, atomic_json, load_project,
                           locked, normalize_doi, now, validate_record, validate_state)


def _key(prefix, value):
    return prefix + "-" + hashlib.sha256(value.encode("utf-8")).hexdigest()[:20]


def import_search(project: str | Path, envelope: dict) -> dict:
    if not isinstance(envelope, dict):
        raise ValueError("Search envelope must be an object.")
    for key in ("provider", "query", "retrieved_at", "source_url"):
        if not isinstance(envelope.get(key), str) or not envelope[key].strip():
            raise ValueError("Search envelope needs " + key + ".")
    entries = envelope.get("records", [])
    if not isinstance(entries, list) or len(entries) > 100:
        raise ValueError("A bounded search import supports at most 100 records.")
    if envelope.get("error") and entries:
        raise ValueError("A failed search must not contain successful records.")
    provider = envelope["provider"]
    if provider not in {"openalex", "crossref", "dblp", "arxiv"}:
        raise ValueError("Use record imports for providers without a bundled adapter.")
    source_id = _key("source", envelope["source_url"])
    source = {
        "id": source_id, "title": provider + " metadata search",
        "url": envelope["source_url"], "type": "metadata",
        "accessed_at": envelope["retrieved_at"], "verified": False,
        "note": "Machine-retrieved discovery metadata; verify primary evidence before a scientific or journal decision.",
    }
    incoming = [("source", source)]
    for entry in entries:
        if not isinstance(entry, dict) or not entry.get("id"):
            raise ValueError("Every search record needs an observed provider identity.")
        paper = copy.deepcopy(entry)
        observed_id = str(paper["id"])
        if paper.get("doi"):
            paper["doi"] = normalize_doi(paper["doi"])
        identity = (paper.get("doi") or observed_id) + "|" + str(paper.get("venue_type", "unknown"))
        if paper.get("venue_type") == "preprint":
            identity += "|" + observed_id
        paper.update(id=_key("paper", identity), provider_record_id=observed_id,
                     source_ids=[source_id], read_status="metadata")
        incoming.append(("paper", paper))
    project = Path(project).expanduser().resolve()
    with locked(project):
        state = load_project(project)
        previous = copy.deepcopy(state["records"])
        canonical = []
        for kind, item in incoming:
            pool = state["records"][KINDS[kind]]
            matches = [i for i, old in enumerate(pool)
                       if old["id"] == item["id"] or _same_identity(kind, old, item)]
            if len(matches) > 1:
                raise ValueError("Search identity matches multiple project records.")
            if matches:
                merged = _merge(kind, pool[matches[0]], item)
                validate_record(kind, merged, state)
                pool[matches[0]] = merged
            else:
                merged = item
                validate_record(kind, merged, state)
                pool.append(merged)
            if kind == "paper":
                canonical.append(merged["id"])
        search_record = {
            "id": _key("search", envelope["source_url"] + "|" + envelope["retrieved_at"]),
            "query": envelope["query"], "provider": provider, "retrieved_at": envelope["retrieved_at"],
            "source_ids": [source_id], "paper_ids": list(dict.fromkeys(canonical)),
            "exhaustive": False, "completeness": envelope.get("completeness", {}),
            "warnings": envelope.get("warnings", []),
            "status": "failed" if envelope.get("error") else "completed_bounded",
        }
        if envelope.get("error"):
            # Only defined, sanitized fields emitted by the adapter.
            search_record["error_code"] = envelope["error"].get("code", "provider_error")
        validate_record("search", search_record, state)
        searches = state["records"]["searches"]
        existing = next((i for i, row in enumerate(searches) if row["id"] == search_record["id"]), None)
        if existing is None:
            searches.append(search_record)
        else:
            searches[existing] = search_record
        validate_state(state)
        changed = previous != state["records"]
        if changed:
            state["revision"] += 1
            state["updated_at"] = now()
            # Keep only changed previous records, not an entire project snapshot.
            prior_changes = []
            for kind, pool_name in KINDS.items():
                before = {r["id"]: r for r in previous[pool_name]}
                for item in state["records"][pool_name]:
                    if before.get(item["id"]) != item:
                        prior_changes.append({"kind": kind, "id": item["id"], "previous": before.get(item["id"])})
            state["history"].append({"revision": state["revision"], "at": now(),
                                     "action": "import_search", "changes": prior_changes})
            atomic_json(project / "project.json", state)
    return {"changed": changed, "revision": state["revision"], "search_id": search_record["id"],
            "paper_ids": canonical, "imported_records": len(canonical), "exhaustive": False}
