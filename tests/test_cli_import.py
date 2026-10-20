"""Atomic search imports and real CLI boundaries using fictional metadata."""
import contextlib
import copy
import datetime as dt
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from project_store import init_project, load_project, record
from search_import import import_search
from scholar_route import main

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "skills/scholar-route/scripts/scholar_route.py"


def envelope():
    return {
        "provider": "crossref", "query": "fictional agent recovery",
        "retrieved_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "source_url": "https://api.crossref.org/works?query.bibliographic=fixture",
        "records": [
            {"id": "doi:10.5555/fixture-import", "title": "Fictional Agent Recovery Study",
             "doi": "10.5555/fixture-import", "venue_type": "journal", "year": 2025,
             "authors": ["Fixture Author"], "url": "https://doi.org/10.5555/fixture-import"}],
        "completeness": {"returned": 1, "requested": 5, "exhaustive": False},
        "warnings": [],
    }


class ImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name) / "project"
        init_project(self.project, "Fictional import task", ["agent-ai"])

    def tearDown(self):
        self.temp.cleanup()

    def test_import_is_atomic_and_has_search_provenance(self):
        raw = envelope()
        prior = copy.deepcopy(raw)
        result = import_search(self.project, raw)
        state = load_project(self.project)
        self.assertEqual(raw, prior)
        self.assertEqual(result["revision"], 1)
        self.assertEqual(state["records"]["papers"][0]["read_status"], "metadata")
        self.assertFalse(state["records"]["sources"][0]["verified"])
        self.assertEqual(state["records"]["searches"][0]["paper_ids"], result["paper_ids"])
        self.assertEqual(state["history"][-1]["action"], "import_search")

    def test_invalid_second_paper_rolls_back_every_record(self):
        raw = envelope()
        raw["records"].append({"id": "bad-provider-id", "title": None})
        before = (self.project / "project.json").read_bytes()
        with self.assertRaises(ValueError):
            import_search(self.project, raw)
        self.assertEqual((self.project / "project.json").read_bytes(), before)
        self.assertFalse((self.project / ".scholar-route.lock").exists())

    def test_reimport_is_noop_and_preserves_reading_depth(self):
        raw = envelope()
        first = import_search(self.project, raw)
        again = import_search(self.project, raw)
        self.assertFalse(again["changed"])
        record(self.project, "paper", {"id": first["paper_ids"][0], "read_status": "full_text"})
        updated_revision = load_project(self.project)["revision"]
        final = import_search(self.project, raw)
        self.assertFalse(final["changed"])
        self.assertEqual(load_project(self.project)["records"]["papers"][0]["read_status"], "full_text")
        self.assertEqual(final["revision"], updated_revision)

    def test_preprint_and_publication_with_same_doi_stay_separate(self):
        raw = envelope()
        import_search(self.project, raw)
        raw["provider"] = "arxiv"
        raw["source_url"] = "https://export.arxiv.org/api/query?search_query=fixture"
        raw["records"][0].update(id="https://arxiv.org/abs/2601.99999v2",
                                  url="https://arxiv.org/abs/2601.99999v2", venue_type="preprint")
        import_search(self.project, raw)
        self.assertEqual({p["venue_type"] for p in load_project(self.project)["records"]["papers"]},
                         {"journal", "preprint"})

    def test_failed_request_is_not_a_successful_zero_result_search(self):
        raw = envelope()
        raw["records"] = []
        raw["error"] = {"code": "network_error", "message": "Safe provider failure", "retryable": True}
        result = import_search(self.project, raw)
        state = load_project(self.project)
        self.assertEqual(result["imported_records"], 0)
        self.assertEqual(state["records"]["searches"][0]["status"], "failed")
        self.assertFalse(state["records"]["searches"][0]["exhaustive"])
        self.assertEqual(state["records"]["papers"], [])

    def test_failure_with_records_is_rejected(self):
        raw = envelope()
        raw["error"] = {"code": "network_error"}
        with self.assertRaises(ValueError):
            import_search(self.project, raw)
        self.assertEqual(load_project(self.project)["revision"], 0)

    def test_oversized_record_batch_is_rejected(self):
        raw = envelope()
        raw["records"] = raw["records"] * 101
        with self.assertRaises(ValueError):
            import_search(self.project, raw)

    def test_provider_error_has_cli_status_three_and_is_logged(self):
        raw = envelope()
        raw["records"] = []
        raw["error"] = {"code": "network_error", "message": "Network unavailable", "retryable": True}
        output = io.StringIO()
        with patch("scholarly_sources.search", return_value=raw), contextlib.redirect_stdout(output):
            status = main(["search", "--provider", "crossref", "--query", "fixture",
                           "--project", str(self.project)])
        self.assertEqual(status, 3)
        result = json.loads(output.getvalue())
        self.assertEqual(result["records"], [])
        self.assertIn("project_import", result)
        self.assertEqual(load_project(self.project)["records"]["searches"][0]["status"], "failed")

    def test_cli_handles_missing_file_without_traceback(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = main(["record", "--project", str(self.project), "--kind", "paper",
                           "--input", str(self.project / "missing.json")])
        self.assertEqual(status, 2)
        self.assertIn("error", json.loads(output.getvalue()))
        self.assertNotIn("Traceback", output.getvalue())

    def test_cli_runs_from_another_directory(self):
        completed = subprocess.run(
            [sys.executable, str(CLI), "route", "--topic", "clinical LLM agent",
             "--stage", "design"], cwd=self.temp.name, text=True, capture_output=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertIn("biomedicine", result["domains"])
        self.assertIn("agent-ai", result["domains"])
        self.assertIn("experiment-plan", result["modules"])


if __name__ == "__main__":
    unittest.main()
