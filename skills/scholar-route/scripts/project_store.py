"""Validated, revisioned local evidence records. No network or model calls."""
from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import math
import os
import re
import tempfile
import uuid
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import unquote, urlsplit

from route_core import route

KINDS = {
    "source": "sources", "paper": "papers", "journal": "journals",
    "claim": "claims", "hypothesis": "hypotheses", "experiment": "experiments",
    "decision": "decisions", "search": "searches",
}
MAX_JSON_BYTES = 16 * 1024 * 1024
SOURCE_TYPES = {"publisher", "index", "registry", "metadata", "paper", "community", "other"}
VENUE_TYPES = {"journal", "conference", "preprint", "book", "repository", "book-series", "other", "unknown"}
FACT_FIELDS = {
    "venue_type", "indexing", "publisher", "mandatory_fee", "languages",
    "first_decision_days", "external_review_days", "acceptance_days",
    "publication_days", "article_types", "scope", "oa_route",
}
SECRET_KEY = re.compile(r"^(?:api[_-]?key|access[_-]?token|authorization|password|secret|token)$", re.I)
IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,159}$")


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def read_json(path: str | Path):
    path = Path(path)
    if path.stat().st_size > MAX_JSON_BYTES:
        raise ValueError("JSON file exceeds the 16 MiB limit.")
    def no_constant(_):
        raise ValueError("JSON must not contain NaN or Infinity.")
    return json.loads(path.read_text(encoding="utf-8"), parse_constant=no_constant)


def atomic_json(path: Path, data) -> None:
    if path.is_symlink():
        raise ValueError("Refusing to replace a symlinked project file.")
    payload = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if len(payload.encode("utf-8")) > MAX_JSON_BYTES:
        raise ValueError("Project exceeds the 16 MiB limit; archive a copy before continuing.")
    fd, temp = tempfile.mkstemp(prefix=".scholar-route-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


@contextmanager
def locked(project: Path):
    lock = project / ".scholar-route.lock"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError("Project is locked by another writer. Check that writer before removing a stale lock.") from None
    try:
        os.write(fd, str(os.getpid()).encode("ascii"))
        os.close(fd)
        fd = None
        yield
    finally:
        if fd is not None:
            os.close(fd)
        lock.unlink(missing_ok=True)


def _object(value, label):
    if not isinstance(value, dict):
        raise ValueError(label + " must be an object.")


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label + " must be a nonempty string.")


def _number(value, label, minimum=0):
    if (isinstance(value, bool) or not isinstance(value, (int, float)) or
            (isinstance(value, float) and not math.isfinite(value)) or value < minimum):
        raise ValueError(label + " must be a finite number >= " + str(minimum) + ".")


def _date(value, label):
    _text(value, label)
    try:
        dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError(label + " must be an ISO date or timestamp.") from None
    if dt.date.fromisoformat(value[:10]) > dt.datetime.now(dt.timezone.utc).date():
        raise ValueError(label + " must not be in the future.")


def _url(value):
    _text(value, "url")
    if any(c.isspace() or ord(c) < 32 or ord(c) == 127 or c in '<>"\\' for c in value):
        raise ValueError("Source URLs must encode whitespace, control and markup characters.")
    parsed = urlsplit(value)
    if parsed.scheme not in {"https", "http"} or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Source URLs must be HTTP(S), with a hostname and no credentials.")
    # Accessing port performs urllib's malformed-port and range validation.
    _ = parsed.port
    from urllib.parse import parse_qsl
    if any(SECRET_KEY.match(k) for k, _ in parse_qsl(parsed.query)):
        raise ValueError("Do not store credential-bearing URLs.")


def _no_secrets(value):
    if isinstance(value, dict):
        for key, val in value.items():
            if SECRET_KEY.match(str(key)):
                raise ValueError("Do not store credentials in project records.")
            _no_secrets(val)
    elif isinstance(value, list):
        for item in value:
            _no_secrets(item)


def normalize_doi(value: str) -> str:
    _text(value, "doi")
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value.strip(), flags=re.I)
    value = re.sub(r"^doi:\s*", "", value, flags=re.I)
    value = unquote(value).strip().lower()
    if not re.fullmatch(r"10\.\d{4,9}/\S+", value):
        raise ValueError("DOI must be a complete observed identifier.")
    return value


def normalize_issn(value: str) -> str:
    _text(value, "issn")
    compact = value.strip().replace("-", "").upper()
    if not re.fullmatch(r"\d{7}[\dX]", compact):
        raise ValueError("ISSN must have eight characters.")
    check = (11 - sum(int(v) * w for v, w in zip(compact[:7], range(8, 1, -1))) % 11) % 11
    actual = 10 if compact[-1] == "X" else int(compact[-1])
    if check != actual:
        raise ValueError("ISSN checksum is invalid.")
    return compact[:4] + "-" + compact[4:]


def validate_constraints(value: dict) -> None:
    _object(value, "constraints")
    _no_secrets(value)
    allowed = {"require_journal", "required_index", "max_mandatory_fee", "excluded_publishers",
               "allowed_languages", "quartile", "max_fact_age_days"}
    unknown = set(value) - allowed
    if unknown:
        raise ValueError("Unknown constraint fields: " + ", ".join(sorted(unknown)))
    if "require_journal" in value and not isinstance(value["require_journal"], bool):
        raise ValueError("require_journal must be boolean.")
    if "required_index" in value:
        _text(value["required_index"], "required_index")
    for field in ("excluded_publishers", "allowed_languages"):
        if field in value and (not isinstance(value[field], list) or any(not isinstance(x, str) for x in value[field])):
            raise ValueError(field + " must be a list of strings.")
    if "max_fact_age_days" in value:
        if isinstance(value["max_fact_age_days"], bool) or not isinstance(value["max_fact_age_days"], int) or value["max_fact_age_days"] < 1:
            raise ValueError("max_fact_age_days must be a positive integer.")
    if "max_mandatory_fee" in value:
        fee = value["max_mandatory_fee"]
        _object(fee, "max_mandatory_fee")
        _number(fee.get("amount"), "max_mandatory_fee.amount")
        if not re.fullmatch(r"[A-Z]{3}", str(fee.get("currency", ""))):
            raise ValueError("Fee currency must be a three-letter uppercase code.")
    if "quartile" in value:
        q = value["quartile"]
        _object(q, "quartile")
        for f in ("system", "category"):
            _text(q.get(f), "quartile." + f)
        if q["system"] not in {"JCR", "SJR", "CAS"}:
            raise ValueError("Quartile system must be JCR, SJR or CAS.")
        if isinstance(q.get("year"), bool) or not isinstance(q.get("year"), int):
            raise ValueError("Quartile year must be explicit.")
        permitted = {"1", "2", "3", "4"} if q["system"] == "CAS" else {"Q1", "Q2", "Q3", "Q4"}
        if (not isinstance(q.get("allowed"), list) or not q["allowed"] or
                any(not isinstance(v, str) for v in q["allowed"]) or not set(q["allowed"]) <= permitted):
            raise ValueError("Quartile allowed values do not match the specified system.")


def _ids(record: dict, field: str, available: set[str], required=False):
    values = record.get(field, [])
    if not isinstance(values, list) or any(not isinstance(i, str) for i in values):
        raise ValueError(field + " must be a list of record IDs.")
    if required and not values:
        raise ValueError(field + " needs at least one evidence record.")
    if set(values) - available:
        raise ValueError(field + " refers to missing records: " + ", ".join(sorted(set(values) - available)))


def validate_record(kind: str, record: dict, state: dict):
    if not isinstance(kind, str) or kind not in KINDS:
        raise ValueError("Unknown record kind.")
    _object(record, kind)
    _no_secrets(record)
    if not isinstance(record.get("id"), str) or not IDENTIFIER.fullmatch(record["id"]):
        raise ValueError("Record id must use 1–160 ASCII letters, digits, dot, underscore, colon or hyphen.")
    records = state["records"]
    source_ids = {s["id"] for s in records["sources"]}
    if kind == "source":
        _text(record.get("title"), "source.title")
        if not record.get("url") and not record.get("path"):
            raise ValueError("A source needs a public URL or a local path with SHA-256.")
        if record.get("url"):
            _url(record["url"])
        if "path" in record:
            _text(record["path"], "source.path")
            if any(ord(c) < 32 for c in record["path"]):
                raise ValueError("Local source paths must not contain control characters.")
            if not isinstance(record.get("sha256"), str) or not re.fullmatch(r"[a-fA-F0-9]{64}", record["sha256"]):
                raise ValueError("Local evidence requires the observed file SHA-256.")
        if record.get("origin_url"):
            _url(record["origin_url"])
        _text(record.get("type"), "source.type")
        if record.get("type") not in SOURCE_TYPES:
            raise ValueError("Source type is not recognized.")
        _date(record.get("accessed_at"), "source.accessed_at")
        if not isinstance(record.get("verified", False), bool):
            raise ValueError("source.verified must be boolean.")
        return
    if "source_ids" in record:
        _ids(record, "source_ids", source_ids)
    for field, pool in (("paper_ids", "papers"), ("claim_ids", "claims"),
                        ("hypothesis_ids", "hypotheses"), ("experiment_ids", "experiments"),
                        ("journal_ids", "journals")):
        if field in record:
            _ids(record, field, {x["id"] for x in records[pool]})
    if kind in {"paper", "journal"}:
        _text(record.get("title"), kind + ".title")
    if kind == "paper":
        if record.get("doi") is not None:
            record["doi"] = normalize_doi(record["doi"])
        if record.get("url"):
            _url(record["url"])
        _text(record.get("venue_type", "unknown"), "paper.venue_type")
        if record.get("venue_type", "unknown") not in VENUE_TYPES:
            raise ValueError("Invalid paper venue_type.")
        _text(record.get("read_status", "metadata"), "paper.read_status")
        if record.get("read_status", "metadata") not in {"metadata", "abstract", "full_text"}:
            raise ValueError("read_status must be metadata, abstract or full_text.")
        if "authors" in record and (not isinstance(record["authors"], list) or any(not isinstance(a, str) for a in record["authors"])):
            raise ValueError("Paper authors must be a list of names.")
        if record.get("year") is not None and (isinstance(record["year"], bool) or not isinstance(record["year"], int) or not 1000 <= record["year"] <= 9999):
            raise ValueError("Paper year must be an integer year.")
    elif kind == "journal":
        if not isinstance(record.get("issns", []), list):
            raise ValueError("journal.issns must be a list.")
        record["issns"] = sorted(set(normalize_issn(i) for i in record.get("issns", [])))
        facts = record.setdefault("facts", {})
        _object(facts, "facts")
        if set(facts) - FACT_FIELDS:
            raise ValueError("Unknown journal facts: " + ", ".join(sorted(set(facts) - FACT_FIELDS)))
        for field, fact in facts.items():
            _object(fact, "fact." + field)
            _text(fact.get("verification", "unverified"), "fact.verification")
            if fact.get("verification", "unverified") not in {"verified", "unverified", "conflicted"}:
                raise ValueError("Invalid fact verification state.")
            _ids(fact, "source_ids", source_ids, required=fact.get("verification") == "verified")
            if fact.get("checked_at"):
                _date(fact["checked_at"], field + ".checked_at")
            elif fact.get("verification") == "verified":
                raise ValueError("Verified facts require checked_at.")
            val = fact.get("value")
            if val is None:
                if fact.get("verification") == "verified":
                    raise ValueError("An unknown fact cannot be verified.")
                continue
            if field == "venue_type":
                _text(val, "venue_type.value")
                if val not in VENUE_TYPES:
                    raise ValueError("Invalid journal venue_type.")
            if field in {"publisher", "scope", "oa_route"}:
                _text(val, field + ".value")
            if field in {"indexing", "languages", "article_types"} and (not isinstance(val, list) or any(not isinstance(i, str) for i in val)):
                raise ValueError(field + " fact value must be a list of strings.")
            if field == "mandatory_fee":
                _number(val, "mandatory_fee")
                if not re.fullmatch(r"[A-Z]{3}", str(fact.get("currency", ""))):
                    raise ValueError("Mandatory fee requires a currency.")
                if "includes_all_mandatory" in fact and not isinstance(fact["includes_all_mandatory"], bool):
                    raise ValueError("includes_all_mandatory must be boolean.")
                if "conditional" in fact and not isinstance(fact["conditional"], bool):
                    raise ValueError("conditional must be boolean.")
            if field.endswith("_days"):
                _number(val, field)
        metrics = record.get("metrics", [])
        if not isinstance(metrics, list):
            raise ValueError("metrics must be a list.")
        for metric in metrics:
            _object(metric, "metric")
            for field in ("system", "category", "value"):
                _text(metric.get(field), "metric." + field)
            if metric["system"] not in {"JCR", "SJR", "CAS"}:
                raise ValueError("Metric system must be JCR, SJR or CAS.")
            permitted = {"1", "2", "3", "4"} if metric["system"] == "CAS" else {"Q1", "Q2", "Q3", "Q4"}
            if metric["value"] not in permitted:
                raise ValueError("Metric value does not match its system.")
            if isinstance(metric.get("year"), bool) or not isinstance(metric.get("year"), int):
                raise ValueError("Metric requires edition year.")
            _ids(metric, "source_ids", source_ids, required=metric.get("verification") == "verified")
            _text(metric.get("verification", "unverified"), "metric.verification")
            if metric.get("verification", "unverified") not in {"verified", "unverified", "conflicted"}:
                raise ValueError("Invalid metric verification state.")
            if metric.get("checked_at"):
                _date(metric["checked_at"], "metric.checked_at")
            elif metric.get("verification") == "verified":
                raise ValueError("Verified metrics require checked_at.")
        conflicts = record.setdefault("conflicts", [])
        if not isinstance(conflicts, list):
            raise ValueError("journal.conflicts must be a list.")
        for conflict in conflicts:
            _object(conflict, "conflict")
            _text(conflict.get("field"), "conflict.field")
            if conflict["field"] not in FACT_FIELDS:
                raise ValueError("Conflict must refer to a recognized journal fact.")
            if conflict.get("status") not in ("unresolved", "resolved"):
                raise ValueError("Conflict status must be unresolved or resolved.")
            _object(conflict.get("previous"), "conflict.previous")
            _object(conflict.get("incoming"), "conflict.incoming")
            _date(conflict.get("recorded_at"), "conflict.recorded_at")
            if conflict["status"] == "resolved":
                _text(conflict.get("resolution"), "conflict.resolution")
                _date(conflict.get("resolved_at"), "conflict.resolved_at")
                _ids(conflict, "source_ids", source_ids, required=True)
        if "fit" in record:
            fit = record["fit"]
            _object(fit, "fit")
            _number(fit.get("score"), "fit.score")
            if fit["score"] > 5:
                raise ValueError("fit.score is a qualitative 0–5 assessment, not probability.")
            _text(fit.get("rationale"), "fit.rationale")
            _date(fit.get("assessed_at"), "fit.assessed_at")
            _ids(fit, "source_ids", source_ids, required=True)
            _ids(fit, "paper_ids", {p["id"] for p in records["papers"]}, required=True)
        for field in ("acceptance_probability", "acceptance_prediction", "predicted_acceptance"):
            if field in record:
                raise ValueError("Do not store a predicted manuscript acceptance probability.")
    elif kind in {"claim", "hypothesis", "experiment", "decision"}:
        _text(record.get("text"), kind + ".text")
        statuses = {
            "claim": {"proposed", "supported", "contested", "unsupported"},
            "hypothesis": {"proposed", "planned", "tested", "rejected", "inconclusive"},
            "experiment": {"planned", "running", "completed", "failed", "blocked"},
            "decision": {"proposed", "accepted", "superseded"},
        }
        _text(record.get("status"), kind + ".status")
        if record.get("status") not in statuses[kind]:
            raise ValueError("Invalid " + kind + " status.")
        if kind == "claim" and record["status"] == "supported":
            _ids(record, "source_ids", source_ids, required=True)
        if kind == "experiment" and record["status"] == "completed":
            _text(record.get("artifact"), "Completed experiment artifact")
            _text(record.get("outcome"), "Completed experiment outcome")
    elif kind == "search":
        for field in ("query", "provider", "retrieved_at"):
            _text(record.get(field), "search." + field)
        _date(record["retrieved_at"], "search.retrieved_at")
        if not isinstance(record.get("exhaustive", False), bool):
            raise ValueError("search.exhaustive must be boolean.")
        if record.get("exhaustive"):
            _text(record.get("coverage_proof"), "Exhaustive search coverage_proof")


def validate_state(state: dict) -> dict:
    _object(state, "project")
    if type(state.get("schema_version")) is not int or state["schema_version"] != 1:
        raise ValueError("Unsupported project schema_version.")
    _text(state.get("topic"), "topic")
    for field in ("project_id", "language", "stage", "region"):
        _text(state.get(field), field)
    for field in ("created_at", "updated_at"):
        _date(state.get(field), field)
    if not isinstance(state.get("domains"), list) or not state["domains"]:
        raise ValueError("Project domains must be a nonempty list.")
    route(state["topic"], state["domains"], state["stage"], state["region"])
    revision = state.get("revision")
    if isinstance(revision, bool) or not isinstance(revision, int) or revision < 0:
        raise ValueError("Project revision must be a nonnegative integer.")
    history = state.get("history")
    if not isinstance(history, list) or len(history) != revision:
        raise ValueError("Project history must contain one entry per revision.")
    for index, entry in enumerate(history, 1):
        _object(entry, "history entry")
        if type(entry.get("revision")) is not int or entry["revision"] != index:
            raise ValueError("History revisions must be consecutive starting from one.")
        _date(entry.get("at"), "history.at")
        _text(entry.get("action"), "history.action")
    validate_constraints(state.get("constraints"))
    _object(state.get("records"), "records")
    warnings = []
    # Validate every collection's shape and IDs before following cross-record links.
    for kind, pool in KINDS.items():
        values = state["records"].get(pool)
        if not isinstance(values, list):
            raise ValueError("Missing project collection: " + pool)
        if any(not isinstance(v, dict) or not isinstance(v.get("id"), str) or
               not IDENTIFIER.fullmatch(v["id"]) for v in values):
            raise ValueError("Invalid record IDs in " + pool)
        ids = [v["id"] for v in values]
        if len(ids) != len(set(ids)):
            raise ValueError("Invalid or duplicate IDs in " + pool)
    for kind, pool in KINDS.items():
        for value in state["records"][pool]:
            validate_record(kind, copy.deepcopy(value), state)
    for journal in state["records"]["journals"]:
        if not journal.get("issns"):
            warnings.append(journal["id"] + ": no ISSN identity evidence.")
        if any(c.get("status") == "unresolved" for c in journal.get("conflicts", [])):
            warnings.append(journal["id"] + ": unresolved fact conflict.")
    _no_secrets(state)
    return {"valid": True, "revision": state.get("revision", 0),
            "counts": {pool: len(state["records"][pool]) for pool in KINDS.values()},
            "warnings": warnings}


def load_project(project: str | Path) -> dict:
    path = Path(project).expanduser().resolve() / "project.json"
    if path.is_symlink():
        raise ValueError("Refusing a symlinked project.json.")
    state = read_json(path)
    validate_state(state)
    return state


def init_project(project: str | Path, topic: str, domains=None, stage="full",
                 region="international", language="zh-CN", constraints=None) -> dict:
    _text(topic, "topic")
    _text(language, "language")
    if constraints is not None:
        validate_constraints(constraints)
    routing = route(topic, domains, stage, region)
    project = Path(project).expanduser().resolve()
    project.mkdir(parents=True, exist_ok=True)
    path = project / "project.json"
    with locked(project):
        if path.exists() or path.is_symlink():
            old = load_project(project)
            if old["topic"] != topic.strip():
                raise ValueError("Project already exists with another topic. Choose a new directory or resume it.")
            return {"created": False, "resumed": True, "project": str(project), "revision": old["revision"]}
        constraints = {"require_journal": True, **(constraints or {})}
        validate_constraints(constraints)
        state = {
            "schema_version": 1, "project_id": str(uuid.uuid4()), "topic": topic.strip(),
            "language": language, "domains": routing["domains"], "region": region,
            "stage": routing["stage"], "constraints": constraints,
            "created_at": now(), "updated_at": now(), "revision": 0,
            "records": {p: [] for p in KINDS.values()}, "history": [],
        }
        validate_state(state)
        atomic_json(path, state)
    return {"created": True, "resumed": False, "project": str(project), "revision": 0}


def _same_identity(kind, old, new) -> bool:
    if kind == "journal":
        return bool(set(old.get("issns", [])) & set(new.get("issns", [])))
    if kind == "paper":
        if not old.get("doi") or old["doi"] != new.get("doi"):
            return False
        if old.get("venue_type", "unknown") != new.get("venue_type", "unknown"):
            return False
        if old.get("venue_type") == "preprint":
            return bool(old.get("url") and old["url"] == new.get("url")
                        and old.get("version") == new.get("version"))
        return old.get("version") == new.get("version")
    return False


def _merge(kind: str, old: dict, incoming: dict) -> dict:
    _object(incoming, kind)
    if "source_ids" in incoming and (not isinstance(incoming["source_ids"], list) or
                                    any(not isinstance(s, str) for s in incoming["source_ids"])):
        raise ValueError("source_ids must be a list of record IDs.")
    if kind == "journal":
        if "facts" in incoming:
            _object(incoming["facts"], "facts")
            for field, value in incoming["facts"].items():
                _object(value, "fact." + str(field))
        for field in ("metrics", "conflicts"):
            if field in incoming and (not isinstance(incoming[field], list) or
                                      any(not isinstance(item, dict) for item in incoming[field])):
                raise ValueError("journal." + field + " must be a list of objects.")
    merged = {**copy.deepcopy(old), **copy.deepcopy(incoming), "id": old["id"]}
    if "source_ids" in old or "source_ids" in incoming:
        merged["source_ids"] = list(dict.fromkeys(old.get("source_ids", []) + incoming.get("source_ids", [])))
    if kind == "journal":
        before, after = set(old.get("issns", [])), set(incoming.get("issns", []))
        if before and after and not before & after:
            raise ValueError("Same journal ID has disjoint ISSNs; resolve identity before updating.")
        merged["issns"] = sorted(before | after)
        if "metrics" in old or "metrics" in incoming:
            merged["metrics"] = []
            for metric in old.get("metrics", []) + incoming.get("metrics", []):
                if metric not in merged["metrics"]:
                    merged["metrics"].append(copy.deepcopy(metric))
        merged["facts"] = copy.deepcopy(old.get("facts", {}))
        merged["conflicts"] = copy.deepcopy(old.get("conflicts", []))
        for key, new_fact in incoming.get("facts", {}).items():
            old_fact = merged["facts"].get(key)
            semantic_fields = ("value", "currency", "conditional", "includes_all_mandatory")
            changed = old_fact and old_fact.get("value") is not None and any(
                old_fact.get(field) is not None and old_fact[field] != new_fact.get(field)
                for field in semantic_fields)
            if changed:
                merged["conflicts"].append({
                    "field": key, "previous": old_fact, "incoming": copy.deepcopy(new_fact),
                    "status": "unresolved", "recorded_at": now(),
                })
                new_fact = {**new_fact, "verification": "conflicted"}
            elif any(c.get("field") == key and c.get("status") == "unresolved" for c in merged["conflicts"]):
                new_fact = {**new_fact, "verification": "conflicted"}
            merged["facts"][key] = copy.deepcopy(new_fact)
    if kind == "paper" and old.get("doi") and incoming.get("doi") and old["doi"] != incoming["doi"]:
        raise ValueError("Same paper ID has conflicting DOIs; keep distinct versions until identity is resolved.")
    if kind == "paper":
        if "read_status" in incoming:
            _text(incoming["read_status"], "paper.read_status")
        old_type = old.get("venue_type", "unknown")
        new_type = incoming.get("venue_type", old_type)
        if old_type != "unknown" and new_type not in ("unknown", old_type):
            raise ValueError("Keep papers with distinct observed venue types in separate records.")
        if new_type == "unknown" and old_type != "unknown":
            merged["venue_type"] = old_type
        if old.get("version") is not None and incoming.get("version", old["version"]) != old["version"]:
            raise ValueError("Keep distinct observed paper versions in separate records.")
        if old_type == "preprint" and old.get("url") and incoming.get("url") and old["url"] != incoming["url"]:
            raise ValueError("Keep distinct preprint version URLs in separate records.")
        if old.get("doi") and incoming.get("doi") is None:
            merged["doi"] = old["doi"]
        levels = {"metadata": 0, "abstract": 1, "full_text": 2}
        if levels.get(old.get("read_status"), 0) > levels.get(merged.get("read_status"), 0):
            merged["read_status"] = old["read_status"]
    return merged


def record(project: str | Path, kind: str, incoming: dict) -> dict:
    if not isinstance(kind, str) or kind not in KINDS:
        raise ValueError("Unknown record kind.")
    _object(incoming, kind)
    if not isinstance(incoming.get("id"), str) or not IDENTIFIER.fullmatch(incoming["id"]):
        raise ValueError("Record id must use 1–160 ASCII letters, digits, dot, underscore, colon or hyphen.")
    project = Path(project).expanduser().resolve()
    with locked(project):
        state = load_project(project)
        incoming = copy.deepcopy(incoming)
        values = state["records"][KINDS[kind]]
        # Normalize identity before looking for aliases.
        if kind == "journal" and "issns" in incoming:
            if not isinstance(incoming["issns"], list):
                raise ValueError("journal.issns must be a list.")
            incoming["issns"] = sorted(set(normalize_issn(i) for i in incoming["issns"]))
        if kind == "paper" and incoming.get("doi"):
            incoming["doi"] = normalize_doi(incoming["doi"])
        matches = [i for i, old in enumerate(values)
                   if old.get("id") == incoming.get("id") or _same_identity(kind, old, incoming)]
        if len(matches) > 1:
            raise ValueError("Incoming identity matches multiple records; reconcile them explicitly.")
        old = values[matches[0]] if matches else None
        merged = _merge(kind, old, incoming) if old else incoming
        validate_record(kind, merged, state)
        if old == merged:
            return {"changed": False, "id": merged["id"], "revision": state["revision"]}
        if old:
            values[matches[0]] = merged
        else:
            values.append(merged)
        state["history"].append({
            "revision": state["revision"] + 1, "at": now(), "action": "record",
            "kind": kind, "id": merged["id"], "previous": copy.deepcopy(old),
        })
        state["revision"] += 1
        state["updated_at"] = now()
        validate_state(state)
        atomic_json(project / "project.json", state)
    return {"changed": True, "id": merged["id"], "revision": state["revision"]}


def set_constraints(project, constraints: dict):
    validate_constraints(constraints)
    project = Path(project).expanduser().resolve()
    with locked(project):
        state = load_project(project)
        old = copy.deepcopy(state["constraints"])
        new = {**old, **constraints}
        validate_constraints(new)
        if new == old:
            return {"changed": False, "revision": state["revision"]}
        state["constraints"] = new
        state["revision"] += 1
        state["updated_at"] = now()
        state["history"].append({"revision": state["revision"], "at": now(),
                                 "action": "constraints", "previous": old})
        atomic_json(project / "project.json", state)
    return {"changed": True, "revision": state["revision"]}


def resolve_fact(project, journal_id: str, field: str, reason: str, source_ids: list[str]):
    """Adopt the currently recorded incoming value after an explained source review."""
    _text(reason, "resolution reason")
    project = Path(project).expanduser().resolve()
    with locked(project):
        state = load_project(project)
        journal = next((j for j in state["records"]["journals"] if j["id"] == journal_id), None)
        if journal is None or field not in journal.get("facts", {}):
            raise ValueError("Journal or fact was not found.")
        unresolved = [c for c in journal.get("conflicts", []) if c["field"] == field and c["status"] == "unresolved"]
        if not unresolved:
            raise ValueError("No unresolved conflict for this fact.")
        _ids({"source_ids": source_ids}, "source_ids", {s["id"] for s in state["records"]["sources"]}, required=True)
        old = copy.deepcopy(journal)
        for conflict in unresolved:
            conflict.update(status="resolved", resolution=reason, resolved_at=now(), source_ids=source_ids)
        journal["facts"][field].update(verification="verified", source_ids=source_ids,
                                        checked_at=now(), resolution=reason)
        validate_record("journal", journal, state)
        state["revision"] += 1
        state["updated_at"] = now()
        state["history"].append({"revision": state["revision"], "at": now(), "action": "resolve",
                                 "kind": "journal", "id": journal_id, "previous": old})
        atomic_json(project / "project.json", state)
    return {"resolved": True, "id": journal_id, "field": field, "revision": state["revision"]}


def fingerprint(state: dict) -> str:
    return hashlib.sha256(json.dumps(state, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
