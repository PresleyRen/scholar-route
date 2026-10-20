#!/usr/bin/env python3
"""ScholarRoute command line: routing, evidence, venue checks and bounded search."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from project_store import (KINDS, init_project, load_project, read_json, record,
                           resolve_fact, set_constraints, validate_state)
from reports import export_project
from route_core import REGIONS, SKILL_ROOT, STAGES, asset, route
from search_import import import_search
from venue_audit import assess

VERSION = "1.0.0"


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False))


def doctor():
    modules = asset("modules.json")
    refs = sorted({m["reference"] for m in modules})
    missing = [r for r in refs if not (SKILL_ROOT / r).is_file()]
    upstream = asset("upstreams.json")
    return {
        "version": VERSION, "python": sys.version.split()[0],
        "python_supported": sys.version_info >= (3, 11), "skill_root": str(SKILL_ROOT),
        "module_count": len(modules), "domain_count": len(asset("domains.json")),
        "missing_references": missing, "provenance_manifest_present": bool(upstream),
        "native_search_adapters": ["openalex", "crossref", "dblp", "arxiv"],
        "optional_local_tools": {t: bool(shutil.which(t)) for t in ("pandoc", "pdflatex", "xelatex")},
        "live_network_tested": False,
        "note": "Tool discovery is not a connectivity check or proof of scholarly correctness.",
        "ok": not missing and sys.version_info >= (3, 11),
    }


def parser():
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--version", action="version", version=VERSION)
    commands = root.add_subparsers(dest="command", required=True)
    for name in ("route", "init"):
        p = commands.add_parser(name)
        p.add_argument("--topic", required=True)
        p.add_argument("--domains", help="Comma-separated domain IDs; omit for a keyword suggestion.")
        p.add_argument("--stage", default="full", help="Research stage: " + ", ".join(STAGES) + "; Chinese aliases are also accepted.")
        p.add_argument("--region", choices=REGIONS, default="international")
        if name == "init":
            p.add_argument("--project", required=True)
            p.add_argument("--language", default="zh-CN")
            p.add_argument("--constraints", help="JSON constraints file.")
    p = commands.add_parser("record")
    p.add_argument("--project", required=True)
    p.add_argument("--kind", choices=KINDS, required=True)
    p.add_argument("--input", required=True, help="One JSON record; existing IDs receive a versioned merge.")
    p = commands.add_parser("constraints")
    p.add_argument("--project", required=True)
    p.add_argument("--input", required=True, help="JSON fields to merge into current constraints.")
    p = commands.add_parser("resolve")
    p.add_argument("--project", required=True)
    p.add_argument("--journal", required=True)
    p.add_argument("--field", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--sources", required=True, help="Comma-separated reviewed source IDs; adopts current incoming value.")
    for name in ("assess", "validate", "report"):
        p = commands.add_parser(name)
        p.add_argument("--project", required=True)
        if name == "assess":
            p.add_argument("--limit", type=int, default=5)
    p = commands.add_parser("search")
    p.add_argument("--provider", choices=("openalex", "crossref", "dblp", "arxiv"), required=True)
    p.add_argument("--query", required=True)
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--timeout", type=float, default=20)
    p.add_argument("--arxiv-advanced", action="store_true")
    p.add_argument("--project", help="Optionally import records and the search log into an existing project.")
    p = commands.add_parser("import-search")
    p.add_argument("--project", required=True)
    p.add_argument("--input", required=True, help="JSON envelope emitted by search.")
    commands.add_parser("doctor")
    commands.add_parser("capabilities")
    return root


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command in {"route", "init"}:
            domains = [d.strip() for d in args.domains.split(",") if d.strip()] if args.domains else None
            if args.command == "route":
                result = route(args.topic, domains, args.stage, args.region)
            else:
                constraints = read_json(args.constraints) if args.constraints else None
                result = init_project(args.project, args.topic, domains, args.stage,
                                      args.region, args.language, constraints)
        elif args.command == "record":
            result = record(args.project, args.kind, read_json(args.input))
        elif args.command == "constraints":
            result = set_constraints(args.project, read_json(args.input))
        elif args.command == "resolve":
            result = resolve_fact(args.project, args.journal, args.field, args.reason,
                                  [s.strip() for s in args.sources.split(",") if s.strip()])
        elif args.command == "validate":
            result = validate_state(load_project(args.project))
        elif args.command == "assess":
            result = assess(load_project(args.project), args.limit)
        elif args.command == "report":
            result = export_project(args.project)
        elif args.command == "search":
            from scholarly_sources import search
            result = search(args.provider, args.query, args.limit, args.timeout,
                            arxiv_advanced=args.arxiv_advanced)
            if args.project:
                result["project_import"] = import_search(args.project, result)
            emit(result)
            return 3 if result.get("error") else 0
        elif args.command == "import-search":
            result = import_search(args.project, read_json(args.input))
        elif args.command == "capabilities":
            result = {"domains": asset("domains.json"), "modules": asset("modules.json")}
        elif args.command == "doctor":
            result = doctor()
            emit(result)
            return 0 if result["ok"] else 2
        emit(result)
        return 0
    except (ValueError, OSError, TypeError, KeyError, RecursionError) as exc:
        # Do not echo raw external provider errors, payloads or credential values.
        message = str(exc) if isinstance(exc, ValueError) and not isinstance(exc, json.JSONDecodeError) else "Input or local project could not be read or validated."
        emit({"error": {"type": type(exc).__name__, "message": message}})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
