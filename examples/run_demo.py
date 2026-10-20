"""Create a small fictional evidence project. Never use these as journal facts."""
import argparse
import copy
import datetime as dt
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "scholar-route" / "scripts"))
from project_store import init_project, record
from reports import export_project
from venue_audit import assess
from project_store import load_project


def build(destination):
    dest = Path(destination)
    if (dest / "project.json").exists():
        raise ValueError("Demo requires a fresh directory to keep existing projects unchanged.")
    day = dt.datetime.now(dt.timezone.utc).date().isoformat()
    init_project(dest, "FICTIONAL DEMO — Agent recovery research", ["agent-ai", "computer-science"],
                 constraints={"required_index": "SCIE", "max_mandatory_fee": {"amount": 0, "currency": "USD"}})
    for sid, kind in [("fixture-publisher", "publisher"), ("fixture-index", "index"), ("fixture-paper", "paper")]:
        record(dest, "source", {"id": sid, "title": "Fictional test evidence — " + kind,
                               "url": "https://example.org/fixtures/" + kind, "type": kind,
                               "accessed_at": day, "verified": True,
                               "note": "SYNTHETIC FIXTURE: not an observed publisher, index or paper."})
    record(dest, "paper", {"id": "paper-one", "title": "Fictional equal-budget Agent recovery study",
                           "doi": "10.5555/scholarroute-fixture-1", "year": 2025,
                           "venue": "Fictional Journal A", "venue_type": "journal",
                           "read_status": "abstract", "authors": ["Fixture Author"],
                           "source_ids": ["fixture-paper"]})
    def fact(value, source="fixture-publisher", **extra):
        return {"value": value, "verification": "verified", "source_ids": [source],
                "checked_at": day, **extra}
    journal = {"id": "journal-a", "title": "Fictional Journal A", "issns": ["1234-5679"],
               "source_ids": ["fixture-publisher"],
               "facts": {"venue_type": fact("journal"), "publisher": fact("Fictional Publisher A"),
                         "indexing": fact(["SCIE"], "fixture-index"),
                         "mandatory_fee": fact(0, currency="USD", includes_all_mandatory=True)},
               "fit": {"score": 4, "rationale": "Fixture only: mechanism and readership align.",
                       "assessed_at": day, "source_ids": ["fixture-paper"], "paper_ids": ["paper-one"]}}
    record(dest, "journal", journal)
    missing = copy.deepcopy(journal)
    missing.update(id="journal-b", title="Fictional Journal B", issns=["2049-3630"])
    missing["facts"].pop("mandatory_fee")
    record(dest, "journal", missing)
    excluded = copy.deepcopy(journal)
    excluded.update(id="venue-c", title="Fictional Conference C", issns=["2434-561X"])
    excluded["facts"]["venue_type"] = fact("conference")
    record(dest, "journal", excluded)
    record(dest, "claim", {"id": "claim-one", "text": "Selective retries may improve recovery under a fixed budget.",
                           "status": "proposed", "paper_ids": ["paper-one"]})
    record(dest, "hypothesis", {"id": "hypothesis-one", "text": "Failure-aware retry beats fixed retry at equal calls.",
                                "status": "planned", "claim_ids": ["claim-one"]})
    record(dest, "experiment", {"id": "experiment-one", "text": "Compare recovery policies on held-out fault traces.",
                                "status": "planned", "hypothesis_ids": ["hypothesis-one"]})
    report = export_project(dest)
    audit = assess(load_project(dest))
    return {"synthetic": True, "pools": {k: [r["id"] for r in v] for k, v in audit["pools"].items()},
            "exports": report["files"]}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project", required=True)
    print(json.dumps(build(p.parse_args().project), ensure_ascii=False, indent=2))
