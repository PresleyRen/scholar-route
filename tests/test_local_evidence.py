"""Local manuscript/brief evidence must not require an invented public URL."""
import datetime as dt
import hashlib
import tempfile
import unittest
from pathlib import Path

from project_store import init_project, load_project, record
from reports import export_project, map_markdown


class LocalEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name) / "project"
        init_project(self.project, "Local manuscript review", ["computer-science"])
        self.brief = Path(self.temp.name) / "brief.md"
        self.brief.write_text("Unmeasured Agent idea, supplied locally.", encoding="utf-8")
        self.source = {
            "id": "local-brief", "title": "User supplied research brief",
            "path": str(self.brief), "sha256": hashlib.sha256(self.brief.read_bytes()).hexdigest(),
            "type": "other", "accessed_at": dt.date.today().isoformat(), "verified": True,
        }

    def tearDown(self):
        self.temp.cleanup()

    def test_local_file_is_evidence_without_fake_http_url(self):
        record(self.project, "source", self.source)
        record(self.project, "claim", {"id": "observation", "text": "The brief describes an unmeasured idea.",
                                      "status": "supported", "source_ids": ["local-brief"]})
        state = load_project(self.project)
        self.assertNotIn("url", state["records"]["sources"][0])
        self.assertEqual(state["records"]["sources"][0]["sha256"], self.source["sha256"])

    def test_local_source_exports_location_and_fingerprint(self):
        record(self.project, "source", self.source)
        export_project(self.project)
        report = (self.project / "REPORT.md").read_text()
        self.assertIn(self.source["sha256"], report)
        self.assertIn("local: ", report)

    def test_local_source_requires_sha256_and_valid_path(self):
        for change in ({"sha256": "not-a-hash"}, {"path": []}, {"path": "x\nbad.md"}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                record(self.project, "source", {**self.source, **change})
        self.assertEqual(load_project(self.project)["revision"], 0)

    def test_archived_source_can_retain_its_official_origin(self):
        record(self.project, "source", {**self.source, "origin_url": "https://example.org/fixture-policy"})
        self.assertEqual(load_project(self.project)["records"]["sources"][0]["origin_url"],
                         "https://example.org/fixture-policy")

    def test_evidence_map_keeps_local_source_to_claim_relationship(self):
        record(self.project, "source", self.source)
        record(self.project, "claim", {"id": "brief-observation", "text": "The brief contains an unmeasured idea.",
                                      "status": "supported", "source_ids": ["local-brief"]})
        diagram = map_markdown(load_project(self.project))
        self.assertIn('来源: User supplied research brief', diagram)
        self.assertIn('S1 --> C1', diagram)
        self.assertIn('| 来源 | local-brief |', diagram)

    def test_map_includes_searches_and_nested_venue_evidence_without_claiming_journal_type(self):
        record(self.project, "source", self.source)
        record(self.project, "search", {"id": "fixture-query", "provider": "fixture",
                                      "query": "bounded agent query", "retrieved_at": dt.date.today().isoformat(),
                                      "source_ids": ["local-brief"], "exhaustive": False})
        record(self.project, "journal", {"id": "conference-fixture", "title": "Fictional Conference",
                                         "facts": {"venue_type": {"value": "conference", "verification": "unverified",
                                                                  "source_ids": ["local-brief"],
                                                                  "checked_at": dt.date.today().isoformat()}}})
        diagram = map_markdown(load_project(self.project))
        self.assertIn('S1 --> Q1', diagram)
        self.assertIn('S1 --> J1', diagram)
        self.assertIn('投稿候选: Fictional Conference', diagram)
        self.assertNotIn('期刊: Fictional Conference', diagram)
        self.assertIn('| 检索 | fixture-query | bounded agent query |', diagram)


if __name__ == "__main__":
    unittest.main()
