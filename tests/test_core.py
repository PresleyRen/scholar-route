"""Offline regressions for project integrity, routing, evidence and exports.

All names, URLs and identifiers below are fictional test fixtures. Tests use
temporary directories; no scholarly provider or other network service is called.
Run with PYTHONPATH=skills/scholar-route/scripts python -m unittest discover -s tests.
"""
from __future__ import annotations

import copy
import csv
import datetime as dt
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from project_store import (
    KINDS, atomic_json, fingerprint, init_project, load_project, locked,
    normalize_doi, normalize_issn, read_json, record, resolve_fact,
    set_constraints, validate_constraints, validate_state,
)
from reports import bibtex, export_project, map_markdown
from route_core import route
from venue_audit import assess, shortlist


TODAY = dt.datetime.now(dt.timezone.utc).date()
RECENT = (TODAY - dt.timedelta(days=1)).isoformat()
STALE = (TODAY - dt.timedelta(days=365)).isoformat()
FUTURE = (TODAY + dt.timedelta(days=2)).isoformat()
# Checksum-valid synthetic identity fixtures, never used for live lookups.
ISSNS = ("9999-9994", "9999-9986", "9999-9978", "9999-996X")


def source(source_id="publisher", source_type="publisher", **updates):
    result = {
        "id": source_id, "title": "Fictional evidence " + source_id,
        "url": "https://evidence.invalid/" + source_id,
        "type": source_type, "accessed_at": RECENT, "verified": True,
    }
    result.update(updates)
    return result


def fact(value, source_id="publisher", **updates):
    result = {"value": value, "source_ids": [source_id],
              "verification": "verified", "checked_at": RECENT}
    result.update(updates)
    return result


def paper(paper_id="paper-1", **updates):
    result = {
        "id": paper_id, "title": "Fictional benchmark study",
        "doi": "10.99999/fixture.study", "venue_type": "journal",
        "read_status": "abstract", "source_ids": ["publisher"],
        "authors": ["A. Example", "B. Fiction"], "year": 2024,
    }
    result.update(updates)
    return result


def journal(journal_id="journal-1", **updates):
    result = {
        "id": journal_id, "title": "Fictional Journal of Evidence",
        "issns": [ISSNS[0]], "source_ids": ["publisher"],
        "facts": {
            "venue_type": fact("journal"),
            "indexing": fact(["Fixture Index"], "index"),
            "publisher": fact("Example Publishing"),
            "mandatory_fee": fact(50, currency="USD", includes_all_mandatory=True),
            "languages": fact(["English"]),
        },
        "metrics": [{"system": "JCR", "year": 2024, "category": "Fictional Studies",
                     "value": "Q2", "verification": "verified", "checked_at": RECENT,
                     "source_ids": ["index"]}],
        "fit": {"score": 4, "rationale": "Recorded overlap with the fictional study.",
                "assessed_at": RECENT, "source_ids": ["publisher"],
                "paper_ids": ["paper-1"]},
    }
    result.update(updates)
    return result


def constraints():
    return {
        "require_journal": True, "required_index": "Fixture Index",
        "max_mandatory_fee": {"amount": 100, "currency": "USD"},
        "excluded_publishers": ["Excluded Example"], "allowed_languages": ["english"],
        "quartile": {"system": "JCR", "year": 2024, "category": "Fictional Studies",
                     "allowed": ["Q1", "Q2"]},
        "max_fact_age_days": 180,
    }


class ProjectCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="scholar-route-test-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "project"
        init_project(self.project, "Fictional evidence project", domains=["general"])

    def add_evidence(self):
        for source_id, source_type in (("publisher", "publisher"), ("index", "index"),
                                       ("registry", "registry"), ("community", "community")):
            record(self.project, "source", source(source_id, source_type))
        record(self.project, "paper", paper())

    def state(self):
        return load_project(self.project)

    def bytes(self):
        return (self.project / "project.json").read_bytes()

    def assert_unchanged_after_error(self, call):
        before = self.bytes()
        with self.assertRaises(ValueError):
            call()
        self.assertEqual(self.bytes(), before)
        self.assertFalse((self.project / ".scholar-route.lock").exists())


class ProjectLifecycleTests(ProjectCase):
    def test_create_resume_and_wrong_topic_preserve_project(self):
        state = self.state()
        self.assertEqual(state["revision"], 0)
        self.assertEqual(state["history"], [])
        self.assertEqual(set(state["records"]), set(KINDS.values()))
        self.assertEqual(state["constraints"], {"require_journal": True})
        before = self.bytes()
        result = init_project(self.project, " Fictional evidence project ", domains=["humanities"])
        self.assertFalse(result["created"])
        self.assertTrue(result["resumed"])
        self.assertEqual(self.bytes(), before)
        self.assert_unchanged_after_error(lambda: init_project(self.project, "Different fictional topic"))

    def test_identical_source_and_journal_imports_are_revision_noops(self):
        self.add_evidence()
        record(self.project, "journal", journal())
        before = self.bytes()
        revision = self.state()["revision"]
        for kind, value in (("source", source()), ("journal", journal())):
            result = record(self.project, kind, value)
            self.assertFalse(result["changed"], kind)
            self.assertEqual(result["revision"], revision)
        self.assertEqual(self.bytes(), before)

    def test_constraints_merge_history_and_noop(self):
        first = set_constraints(self.project, {"required_index": "Fixture Index"})
        self.assertEqual(first, {"changed": True, "revision": 1})
        state = self.state()
        self.assertTrue(state["constraints"]["require_journal"])
        self.assertEqual(state["history"][0]["previous"], {"require_journal": True})
        before = self.bytes()
        self.assertFalse(set_constraints(self.project, {"required_index": "Fixture Index"})["changed"])
        self.assertEqual(self.bytes(), before)
        self.assert_unchanged_after_error(lambda: set_constraints(self.project, {"max_fact_age_days": 0}))

    def test_invalid_update_is_atomic_and_releases_lock(self):
        record(self.project, "source", source())
        self.assert_unchanged_after_error(lambda: record(self.project, "source", {"id": "publisher", "title": ""}))
        self.assert_unchanged_after_error(lambda: record(self.project, "unknown", {}))
        self.assertTrue(record(self.project, "source", {"id": "publisher", "title": "Rechecked fictional source"})["changed"])
        self.assertEqual(self.state()["history"][-1]["previous"]["title"], source()["title"])

    def test_record_does_not_mutate_caller_payload(self):
        incoming = source()
        before = copy.deepcopy(incoming)
        record(self.project, "source", incoming)
        self.assertEqual(incoming, before)
        record(self.project, "source", source("index", "index"))
        incoming_paper = paper(doi="https://doi.org/10.99999/Fixture%2EStudy")
        before = copy.deepcopy(incoming_paper)
        record(self.project, "paper", incoming_paper)
        self.assertEqual(incoming_paper, before)

    def test_lock_contention_and_exception_cleanup(self):
        lock = self.project / ".scholar-route.lock"
        lock.write_text("fictional other writer", encoding="utf-8")
        before = self.bytes()
        with self.assertRaisesRegex(ValueError, "locked"):
            record(self.project, "source", source())
        self.assertEqual(lock.read_text(encoding="utf-8"), "fictional other writer")
        self.assertEqual(self.bytes(), before)
        lock.unlink()
        with self.assertRaisesRegex(RuntimeError, "fixture failure"):
            with locked(self.project):
                raise RuntimeError("fixture failure")
        self.assertFalse(lock.exists())

    def test_project_symlink_is_rejected_without_changing_target(self):
        target = Path(self.temp.name) / "external.json"
        target.write_bytes(self.bytes())
        original = target.read_bytes()
        (self.project / "project.json").unlink()
        (self.project / "project.json").symlink_to(target)
        with self.assertRaisesRegex(ValueError, "symlink"):
            load_project(self.project)
        with self.assertRaisesRegex(ValueError, "symlink"):
            record(self.project, "source", source())
        self.assertEqual(target.read_bytes(), original)


class IdentityAndConflictTests(ProjectCase):
    def setUp(self):
        super().setUp()
        self.add_evidence()

    def test_doi_alias_merges_evidence_and_retains_read_depth(self):
        record(self.project, "paper", {"id": "paper-1", "read_status": "full_text"})
        result = record(self.project, "paper", paper("paper-alias", doi="DOI: 10.99999/FIXTURE.STUDY",
                                                       source_ids=["index"], read_status="metadata"))
        self.assertEqual(result["id"], "paper-1")
        papers = self.state()["records"]["papers"]
        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]["doi"], "10.99999/fixture.study")
        self.assertEqual(papers[0]["read_status"], "full_text")
        self.assertEqual(papers[0]["source_ids"], ["publisher", "index"])

    def test_preprint_and_distinct_versions_remain_separate(self):
        record(self.project, "paper", paper("preprint-v1", venue_type="preprint",
                                             url="https://papers.invalid/fixture/v1", version="v1"))
        record(self.project, "paper", paper("preprint-v2", venue_type="preprint",
                                             url="https://papers.invalid/fixture/v2", version="v2"))
        record(self.project, "paper", paper("publication-v2", version="v2"))
        ids = {p["id"] for p in self.state()["records"]["papers"]}
        self.assertEqual(ids, {"paper-1", "preprint-v1", "preprint-v2", "publication-v2"})

    def test_preprint_version_tag_prevents_merge_even_at_same_landing_page(self):
        common = {"venue_type": "preprint", "url": "https://papers.invalid/fixture"}
        record(self.project, "paper", paper("preprint-v1", version="v1", **common))
        record(self.project, "paper", paper("preprint-v2", version="v2", **common))
        self.assertEqual(len(self.state()["records"]["papers"]), 3)

    def test_same_id_cannot_overwrite_doi_type_or_observed_version(self):
        changes = [
            ({"venue_type": "journal"}, {"venue_type": "preprint"}),
            ({"venue_type": "preprint"}, {"venue_type": "journal"}),
            ({"venue_type": "journal"}, {"venue_type": "conference"}),
            ({"version": "v1"}, {"version": "v2"}),
            ({"venue_type": "preprint", "url": "https://papers.invalid/v1"},
             {"url": "https://papers.invalid/v2"}),
            ({}, {"doi": "10.99999/other"}),
        ]
        for index, (initial, update) in enumerate(changes):
            with self.subTest(change=index):
                paper_id = "version-case-" + str(index)
                record(self.project, "paper", paper(paper_id, doi="10.99999/identity." + str(index), **initial))
                self.assert_unchanged_after_error(lambda: record(self.project, "paper", {"id": paper_id, **update}))

    def test_overlapping_issn_aliases_merge_but_disjoint_identity_is_rejected(self):
        record(self.project, "journal", journal(issns=[ISSNS[0]]))
        result = record(self.project, "journal", journal("alias", issns=[ISSNS[0].replace("-", ""), ISSNS[1]],
                                                           source_ids=["index"]))
        self.assertEqual(result["id"], "journal-1")
        stored = self.state()["records"]["journals"]
        self.assertEqual(len(stored), 1)
        self.assertEqual(stored[0]["issns"], sorted(ISSNS[:2]))
        self.assertEqual(stored[0]["source_ids"], ["publisher", "index"])
        self.assert_unchanged_after_error(lambda: record(self.project, "journal", {"id": "journal-1", "issns": [ISSNS[2]]}))

    def test_bridging_two_existing_identities_requires_explicit_reconciliation(self):
        record(self.project, "journal", journal("first", issns=[ISSNS[0]]))
        record(self.project, "journal", journal("second", issns=[ISSNS[1]]))
        self.assert_unchanged_after_error(lambda: record(self.project, "journal", journal("bridge", issns=list(ISSNS[:2]))))

    def test_changed_fact_stays_conflicted_until_explained_resolution(self):
        set_constraints(self.project, {"max_mandatory_fee": {"amount": 100, "currency": "USD"}})
        record(self.project, "journal", journal())
        update = {"id": "journal-1", "facts": {"mandatory_fee": fact(80, currency="USD", includes_all_mandatory=True)}}
        record(self.project, "journal", update)
        before = self.state()
        old_journal = before["records"]["journals"][0]
        self.assertEqual(old_journal["facts"]["mandatory_fee"]["verification"], "conflicted")
        self.assertEqual(len(old_journal["conflicts"]), 1)
        self.assertEqual(old_journal["conflicts"][0]["previous"]["value"], 50)
        self.assertEqual(old_journal["conflicts"][0]["incoming"]["value"], 80)
        self.assertEqual(assess(before)["pools"]["unverified"][0]["id"], "journal-1")
        self.assertFalse(record(self.project, "journal", update)["changed"])
        self.assert_unchanged_after_error(lambda: resolve_fact(self.project, "journal-1", "mandatory_fee", "", ["publisher"]))
        self.assert_unchanged_after_error(lambda: resolve_fact(self.project, "journal-1", "mandatory_fee", "Reviewed source", ["missing"]))
        result = resolve_fact(self.project, "journal-1", "mandatory_fee", "Reviewed the corrected fictional fee page", ["publisher"])
        self.assertEqual(result["revision"], before["revision"] + 1)
        state = self.state()
        self.assertEqual(state["records"]["journals"][0]["conflicts"][0]["status"], "resolved")
        self.assertEqual(state["history"][-1]["previous"], old_journal)
        self.assertEqual(len(assess(state)["pools"]["eligible"]), 1)
        self.assert_unchanged_after_error(lambda: resolve_fact(self.project, "journal-1", "mandatory_fee", "Already resolved", ["publisher"]))

    def test_changed_fee_conditions_are_preserved_as_conflicts(self):
        for field, before, after in (("conditional", True, False), ("includes_all_mandatory", False, True)):
            with self.subTest(field=field):
                venue = journal(field, issns=[ISSNS[0] if field == "conditional" else ISSNS[1]])
                venue["facts"]["mandatory_fee"][field] = before
                record(self.project, "journal", venue)
                new_fee = copy.deepcopy(venue["facts"]["mandatory_fee"])
                new_fee[field] = after
                record(self.project, "journal", {"id": field, "facts": {"mandatory_fee": new_fee}})
                stored = next(j for j in self.state()["records"]["journals"] if j["id"] == field)
                self.assertEqual(stored["facts"]["mandatory_fee"]["verification"], "conflicted")
                self.assertEqual(stored["conflicts"][0]["previous"][field], before)

    def test_completed_work_and_supported_claims_require_recorded_evidence(self):
        self.assert_unchanged_after_error(lambda: record(self.project, "claim", {"id": "claim", "text": "Fictional claim", "status": "supported"}))
        self.assert_unchanged_after_error(lambda: record(self.project, "experiment", {"id": "exp", "text": "Fictional test", "status": "completed"}))
        record(self.project, "claim", {"id": "claim", "text": "Fictional claim", "status": "supported", "source_ids": ["publisher"], "paper_ids": ["paper-1"]})
        record(self.project, "hypothesis", {"id": "hyp", "text": "Fictional hypothesis", "status": "planned", "claim_ids": ["claim"]})
        record(self.project, "experiment", {"id": "exp", "text": "Fictional test", "status": "completed", "hypothesis_ids": ["hyp"],
                                             "artifact": "fixture-results.json", "outcome": "Fictional observed test outcome"})
        self.assert_unchanged_after_error(lambda: record(self.project, "decision", {"id": "decision", "text": "Fictional choice", "status": "accepted", "experiment_ids": ["absent"]}))
        record(self.project, "decision", {"id": "decision", "text": "Fictional choice", "status": "accepted", "experiment_ids": ["exp"]})
        self.assertTrue(validate_state(self.state())["valid"])


class MalformedInputTests(ProjectCase):
    def test_invalid_record_shapes_raise_value_error_without_mutation(self):
        cases = [("source", None), ("source", []), ("source", "fixture"),
                 ("source", {**source(), "id": 123}), ("source", {**source(), "id": ["bad"]}),
                 ("source", source(type=[])), ("journal", {"id": "j", "title": "Fictional", "issns": None}),
                 ("journal", {"id": "j", "title": "Fictional", "facts": []}),
                 ("journal", {"id": "j", "title": "Fictional", "conflicts": ["bad"]})]
        for kind, payload in cases:
            with self.subTest(kind=kind, payload=payload):
                self.assert_unchanged_after_error(lambda: record(self.project, kind, payload))

    def test_partial_updates_and_identity_aliases_cannot_bypass_validation(self):
        self.add_evidence()
        record(self.project, "journal", journal())
        cases = [("paper", {"id": "paper-1", "read_status": []}),
                 ("paper", {"id": "paper-1", "read_status": {}}),
                 ("paper", {**paper(), "id": 123}),
                 ("journal", {**journal(), "id": 123}),
                 ("journal", {"id": "journal-1", "source_ids": "publisher"}),
                 ("journal", {"id": "journal-1", "facts": {"venue_type": []}}),
                 ("journal", {"id": "journal-1", "metrics": {}})]
        for kind, payload in cases:
            with self.subTest(kind=kind, payload=payload):
                self.assert_unchanged_after_error(lambda: record(self.project, kind, payload))
        self.assert_unchanged_after_error(lambda: set_constraints(self.project, {
            "max_mandatory_fee": {"amount": 10, "currency": "USD", "api_key": "fictional-secret"}}))

    def test_project_envelope_and_collection_validation(self):
        baseline = self.state()
        cases = [
            ("schema_version", True), ("revision", True), ("revision", -1),
            ("revision", "0"), ("history", None), ("history", ["bad"]),
            ("stage", "missing-stage"), ("domains", "agent-ai"),
            ("domains", ["missing-domain"]), ("region", "missing-region"),
            ("language", None), ("created_at", "yesterday"), ("updated_at", FUTURE),
            ("project_id", None), ("constraints", None), ("records", []),
        ]
        for field, value in cases:
            with self.subTest(field=field, value=value):
                state = copy.deepcopy(baseline)
                state[field] = value
                with self.assertRaises(ValueError):
                    validate_state(state)
        for values in ([{"id": ["bad"]}], [{"id": "duplicate"}, {"id": "duplicate"}], [None]):
            with self.subTest(records=values):
                state = copy.deepcopy(baseline)
                state["records"]["sources"] = values
                with self.assertRaises(ValueError):
                    validate_state(state)
        state = copy.deepcopy(baseline)
        del state["records"]["sources"]
        with self.assertRaises(ValueError):
            validate_state(state)

    def test_invalid_constraints_raise_value_error(self):
        cases = [None, [], {"unknown": True}, {"require_journal": 1},
                 {"required_index": " "}, {"max_fact_age_days": True},
                 {"allowed_languages": "English"},
                 {"max_mandatory_fee": {"amount": True, "currency": "USD"}},
                 {"max_mandatory_fee": {"amount": -1, "currency": "USD"}},
                 {"max_mandatory_fee": {"amount": float("nan"), "currency": "USD"}},
                 {"quartile": {"system": "JCR", "category": "Fiction", "year": 2024, "allowed": [["Q1"]]}},
                 {"quartile": {"system": "CAS", "category": "Fiction", "year": 2024, "allowed": ["Q1"]}}]
        for value in cases:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_constraints(value)

    def test_bad_initialization_values_do_not_create_a_project_file(self):
        cases = [{"topic": None}, {"topic": " "}, {"constraints": []}, {"language": None}, {"domains": "agent-ai"}]
        for index, changes in enumerate(cases):
            with self.subTest(changes=changes):
                location = Path(self.temp.name) / ("bad-" + str(index))
                arguments = {"topic": "Fictional project", **changes}
                with self.assertRaises(ValueError):
                    init_project(location, **arguments)
                self.assertFalse((location / "project.json").exists())

    def test_credentials_malformed_urls_and_future_dates_are_rejected(self):
        cases = [source(url="https://user:password@evidence.invalid/"),
                 source(url="https://evidence.invalid/?api_key=fixture"),
                 source(url="file:///fixture"), source(url="https://evidence.invalid/\nmalformed"),
                 source(url="https://evidence.invalid/<markup>"),
                 source(accessed_at=FUTURE), source(accessed_at="not-a-date"),
                 source(verified="true"), source(notes={"access_token": "fictional-secret"})]
        for value in cases:
            with self.subTest(value=value):
                self.assert_unchanged_after_error(lambda: record(self.project, "source", value))

    def test_unverified_or_unknown_facts_cannot_claim_verification(self):
        self.add_evidence()
        cases = [fact(None), fact("journal", source_ids=[]), fact("journal", source_ids=["absent"]),
                 fact("journal", checked_at=None), fact("journal", verification="definitely")]
        for value in cases:
            with self.subTest(value=value):
                self.assert_unchanged_after_error(lambda: record(self.project, "journal", journal(facts={"venue_type": value})))

    def test_search_exhaustiveness_requires_explicit_coverage_record(self):
        value = {"id": "search", "query": "fictional query", "provider": "fixture-provider",
                 "retrieved_at": RECENT, "exhaustive": True}
        self.assert_unchanged_after_error(lambda: record(self.project, "search", value))
        value["coverage_proof"] = "Fixture contained exactly two pages; both were read."
        self.assertTrue(record(self.project, "search", value)["changed"])

    def test_json_rejects_nonfinite_truncated_and_oversized_content(self):
        location = Path(self.temp.name) / "input.json"
        for content in ('{"value": NaN}', '{"value": Infinity}', '{"value": -Infinity}', '{"unfinished":'):
            with self.subTest(content=content):
                location.write_text(content, encoding="utf-8")
                with self.assertRaises(ValueError):
                    read_json(location)
        location.write_text('{"fixture": "long enough"}', encoding="utf-8")
        with patch("project_store.MAX_JSON_BYTES", 8):
            with self.assertRaisesRegex(ValueError, "limit"):
                read_json(location)
            before = self.bytes()
            with self.assertRaisesRegex(ValueError, "limit"):
                atomic_json(self.project / "project.json", {"fixture": "long enough"})
            self.assertEqual(self.bytes(), before)

    def test_identifier_normalization_and_checksums(self):
        self.assertEqual(normalize_doi(" https://DX.DOI.ORG/10.99999/Fiction%2ETest "), "10.99999/fiction.test")
        self.assertEqual(normalize_issn("9999996x"), "9999-996X")
        for value in ("", "10.999/short-prefix", "not-a-doi", "10.99999/has space"):
            with self.subTest(doi=value):
                with self.assertRaises(ValueError):
                    normalize_doi(value)
        for value in ("9999-9995", "short", "abcdefgh"):
            with self.subTest(issn=value):
                with self.assertRaises(ValueError):
                    normalize_issn(value)


class VenueAuditTests(ProjectCase):
    def setUp(self):
        super().setUp()
        self.add_evidence()

    def audit_state(self, venue=None, restrictions=None):
        state = self.state()
        state["constraints"] = constraints() if restrictions is None else restrictions
        state["records"]["journals"] = [journal() if venue is None else venue]
        return state

    def row(self, state):
        result = assess(state)
        return next(row for rows in result["pools"].values() for row in rows)

    def check(self, row, field):
        return next(item for item in row["checks"] if item["field"] == field)

    def test_primary_evidence_passes_constraints_without_predicting_acceptance(self):
        result = assess(self.audit_state())
        row = result["pools"]["eligible"][0]
        self.assertEqual(row["evidence_coverage"], {"passed": 7, "required": 7})
        self.assertTrue(all(c["source_ids"] for c in row["checks"]))
        self.assertEqual(row["fit_score"], 4)
        self.assertEqual(result["shortlist"]["ids"], ["journal-1"])
        self.assertIsNone(result["acceptance_probability"])
        self.assertEqual(result["pools"]["excluded"], [])
        self.assertEqual(result["pools"]["unverified"], [])

    def test_confirmed_violation_excludes_even_when_another_fact_is_unknown(self):
        venue = journal()
        del venue["facts"]["indexing"]
        venue["facts"]["mandatory_fee"]["value"] = 101
        row = self.row(self.audit_state(venue))
        self.assertEqual(row["status"], "excluded")
        self.assertEqual(self.check(row, "indexing")["status"], "unknown")
        self.assertEqual(self.check(row, "mandatory_fee")["status"], "fail")

    def test_unknown_venue_type_is_unverified_and_known_conference_is_excluded(self):
        for venue_type, expected in (("unknown", "unverified"), ("conference", "excluded")):
            with self.subTest(venue_type=venue_type):
                venue = journal()
                venue["facts"]["venue_type"]["value"] = venue_type
                self.assertEqual(self.row(self.audit_state(venue))["status"], expected)

    def test_issn_requires_current_verified_primary_identity_provenance(self):
        for updates in ({"issns": []}, {"source_ids": []}, {"source_ids": ["community"]}):
            with self.subTest(updates=updates):
                row = self.row(self.audit_state(journal(**updates)))
                self.assertEqual(row["status"], "unverified")
                self.assertEqual(self.check(row, "identity")["status"], "unknown")

    def test_indexing_does_not_use_publisher_or_community_assertions(self):
        for source_id in ("publisher", "community"):
            with self.subTest(source_id=source_id):
                venue = journal()
                venue["facts"]["indexing"]["source_ids"] = [source_id]
                row = self.row(self.audit_state(venue))
                self.assertEqual(row["status"], "unverified")
                self.assertEqual(self.check(row, "indexing")["reason"], "no_current_primary_evidence")

    def test_stale_or_unverified_evidence_does_not_satisfy_hard_constraints(self):
        for mode in ("source_stale", "source_unverified", "fact_stale", "fact_unverified"):
            with self.subTest(mode=mode):
                state = self.audit_state()
                if mode.startswith("source"):
                    item = next(s for s in state["records"]["sources"] if s["id"] == "index")
                    item["accessed_at" if mode == "source_stale" else "verified"] = STALE if mode == "source_stale" else False
                else:
                    item = state["records"]["journals"][0]["facts"]["indexing"]
                    item["checked_at" if mode == "fact_stale" else "verification"] = STALE if mode == "fact_stale" else "unverified"
                row = self.row(state)
                self.assertEqual(row["status"], "unverified")
                self.assertEqual(self.check(row, "indexing")["status"], "unknown")

    def test_fee_caps_distinguish_zero_cost_waivers_completeness_and_currency(self):
        cases = [
            ({"value": 0, "currency": "EUR"}, "pass"),
            ({"value": 0, "conditional": True}, "unknown"),
            ({"includes_all_mandatory": False}, "unknown"),
            ({"currency": "EUR"}, "unknown"),
            ({"value": 100}, "pass"), ({"value": 101}, "fail"),
        ]
        for updates, expected in cases:
            with self.subTest(updates=updates):
                venue = journal()
                venue["facts"]["mandatory_fee"].update(updates)
                row = self.row(self.audit_state(venue))
                self.assertEqual(self.check(row, "mandatory_fee")["status"], expected)

    def test_quartiles_require_exact_system_year_category_and_consistent_values(self):
        cases = [({"system": "SJR"}, "unknown"), ({"year": 2023}, "unknown"),
                 ({"category": "Another category"}, "unknown"), ({"value": "Q4"}, "fail")]
        for updates, expected in cases:
            with self.subTest(updates=updates):
                venue = journal()
                venue["metrics"][0].update(updates)
                self.assertEqual(self.check(self.row(self.audit_state(venue)), "quartile")["status"], expected)
        venue = journal()
        venue["metrics"].append({**venue["metrics"][0], "value": "Q3"})
        row = self.row(self.audit_state(venue))
        self.assertEqual(self.check(row, "quartile")["status"], "unknown")
        self.assertIn("Contradictory", self.check(row, "quartile")["reason"])

    def test_fit_requires_read_paper_current_assessment_and_current_verified_source(self):
        for mode in ("metadata_only", "stale_assessment", "unverified_source", "stale_source"):
            with self.subTest(mode=mode):
                state = self.audit_state(restrictions={"require_journal": True})
                venue = state["records"]["journals"][0]
                venue["fit"]["source_ids"] = ["community"]
                if mode == "metadata_only":
                    state["records"]["papers"][0]["read_status"] = "metadata"
                elif mode == "stale_assessment":
                    venue["fit"]["assessed_at"] = STALE
                else:
                    item = next(s for s in state["records"]["sources"] if s["id"] == "community")
                    item["verified" if mode == "unverified_source" else "accessed_at"] = False if mode == "unverified_source" else STALE
                result = assess(state)
                self.assertIsNone(result["pools"]["eligible"][0]["fit_score"])
                self.assertEqual(result["shortlist"]["ids"], [])
                self.assertEqual(result["shortlist"]["unranked_eligible"], ["journal-1"])

    def test_unverified_publishers_do_not_create_false_diversity(self):
        state = self.audit_state(restrictions={"require_journal": True})
        state["records"]["journals"] = []
        for index in range(3):
            venue = journal("j" + str(index), issns=[ISSNS[index]])
            venue["facts"]["publisher"] = fact("Unverified publisher " + str(index), verification="unverified")
            state["records"]["journals"].append(venue)
        result = assess(state)
        self.assertTrue(all(row["publisher"] is None for row in result["pools"]["eligible"]))
        self.assertEqual(result["shortlist"]["ids"], ["j0", "j1"])
        self.assertEqual(result["shortlist"]["deferred_for_diversity"], ["j2"])

    def test_shortlist_retains_pools_and_applies_fit_order_and_publisher_cap(self):
        rows = [
            {"id": "a", "title": "Alpha", "status": "eligible", "fit_score": 5, "publisher": "Example"},
            {"id": "b", "title": "Beta", "status": "eligible", "fit_score": 4.5, "publisher": "EXAMPLE"},
            {"id": "c", "title": "Gamma", "status": "eligible", "fit_score": 4, "publisher": "Example"},
            {"id": "d", "title": "Delta", "status": "eligible", "fit_score": 3, "publisher": "Other"},
            {"id": "e", "title": "Unread", "status": "eligible", "fit_score": None, "publisher": "Other"},
            {"id": "f", "title": "Excluded", "status": "excluded", "fit_score": 5, "publisher": "Other"},
        ]
        before = copy.deepcopy(rows)
        result = shortlist(rows, limit=3)
        self.assertEqual(result["ids"], ["a", "b", "d"])
        self.assertEqual(result["deferred_for_diversity"], ["c"])
        self.assertEqual(result["unranked_eligible"], ["e"])
        self.assertEqual(rows, before)

    def test_shortlist_rejects_invalid_limits_and_caps(self):
        for field in ("limit", "publisher_cap"):
            for value in (True, 0, -1, "2", 1.5):
                with self.subTest(field=field, value=value):
                    with self.assertRaises(ValueError):
                        shortlist([], **{field: value})


class RoutingTests(unittest.TestCase):
    def test_interdisciplinary_agent_clinical_topic_loads_both_evidence_profiles(self):
        result = route("LLM agents for clinical patient decisions", stage="design")
        self.assertEqual(set(result["domains"]), {"agent-ai", "computer-science", "biomedicine"})
        self.assertIn("PubMed", result["sources"])
        self.assertIn("DBLP", result["sources"])
        self.assertIn("agent-capabilities", result["modules"])
        self.assertTrue(result["warnings"])
        self.assertEqual(result["selection"], "keyword_suggestion")

    def test_multilingual_topics_and_word_boundaries(self):
        self.assertIn("biomedicine", route("临床药物研究")["domains"])
        self.assertEqual(route("A garage with a millimeter marking")["domains"], ["general"])
        self.assertNotIn("agent-capabilities", route("A garage with a millimeter marking")["modules"])

    def test_explicit_domains_override_keyword_routing_without_duplicates(self):
        result = route("clinical patient study", ["general", "humanities", "humanities"], stage="review")
        self.assertEqual(result["domains"], ["humanities"])
        self.assertEqual(result["selection"], "explicit")
        self.assertEqual(result["signals"], {})
        self.assertNotIn("PubMed", result["sources"])
        self.assertEqual(route("Fictional", ["agent-ai"])["domains"], ["agent-ai", "computer-science"])

    def test_stage_alias_and_region_filter_modules_and_sources(self):
        china = route("Fictional", ["general"], stage="选刊", region="china")
        self.assertEqual(china["stage"], "journal")
        self.assertIn("regional-indexing", china["modules"])
        self.assertIn("CNKI", china["sources"])
        international = route("Fictional", ["general"], stage="journal")
        self.assertNotIn("regional-indexing", international["modules"])
        self.assertIn({"id": "regional-indexing", "reason": "regional_only"}, international["skipped"])
        self.assertNotIn("manuscript-writing", international["modules"])
        turkey = route("Fictional", ["general"], stage="submit", region="turkey")
        self.assertIn("TR Dizin", turkey["sources"])
        self.assertEqual(route("Fictional", stage="全流程")["stage"], "full")

    def test_routing_results_do_not_leak_mutations_between_calls(self):
        result = route("Fictional", ["general"])
        result["module_details"][0]["stages"].clear()
        result["sources"].append("Injected fixture")
        again = route("Fictional", ["general"])
        self.assertTrue(again["module_details"][0]["stages"])
        self.assertNotIn("Injected fixture", again["sources"])

    def test_malformed_routing_inputs_raise_value_error(self):
        for updates in ({"topic": None}, {"topic": " "}, {"domains": "agent-ai"},
                        {"domains": [None]}, {"domains": [["general"]]},
                        {"domains": ["unknown"]}, {"stage": []}, {"region": "unknown"}):
            with self.subTest(updates=updates):
                with self.assertRaises(ValueError):
                    route(**{"topic": "Fictional", **updates})


class ReportTests(ProjectCase):
    def setUp(self):
        super().setUp()
        self.add_evidence()
        record(self.project, "journal", journal(title="=Fictional | Journal <test>"))
        record(self.project, "claim", {"id": "claim", "text": 'Fictional "claim"; [x] <tag>',
                                       "status": "supported", "source_ids": ["publisher"], "paper_ids": ["paper-1"]})

    def test_export_has_traceable_audit_csv_bibtex_and_map_without_revision_change(self):
        before = self.bytes()
        state = self.state()
        result = export_project(self.project)
        self.assertEqual(result["project_revision"], state["revision"])
        self.assertEqual(result["fingerprint"], fingerprint(state))
        self.assertEqual(self.bytes(), before)
        self.assertEqual({Path(p).name for p in result["files"]},
                         {"REPORT.md", "MAP.md", "journals.csv", "references.bib", "assessment.json"})
        audit = read_json(self.project / "assessment.json")
        self.assertEqual(audit, assess(state))
        report_text = (self.project / "REPORT.md").read_text(encoding="utf-8")
        self.assertIn(result["fingerprint"], report_text)
        self.assertIn("https://evidence.invalid/publisher", report_text)
        self.assertIn(r"\| Journal &lt;test&gt;", report_text)
        rows = list(csv.DictReader(io.StringIO((self.project / "journals.csv").read_text(encoding="utf-8"))))
        self.assertEqual(rows[0]["title"], "'=Fictional | Journal <test>")
        self.assertEqual(rows[0]["status"], "eligible")
        self.assertIn("@article{", (self.project / "references.bib").read_text(encoding="utf-8"))
        graph = (self.project / "MAP.md").read_text(encoding="utf-8")
        self.assertIn("P1 --> C1", graph)
        self.assertIn("P1 --> J1", graph)
        self.assertNotIn("C1 --> P1", graph)

    def test_export_checks_all_symlinks_before_replacing_any_existing_report(self):
        export_project(self.project)
        report_before = (self.project / "REPORT.md").read_bytes()
        target = Path(self.temp.name) / "untouched.txt"
        target.write_text("Fictional external content", encoding="utf-8")
        (self.project / "references.bib").unlink()
        (self.project / "references.bib").symlink_to(target)
        with self.assertRaisesRegex(ValueError, "symlink"):
            export_project(self.project)
        self.assertEqual((self.project / "REPORT.md").read_bytes(), report_before)
        self.assertEqual(target.read_text(encoding="utf-8"), "Fictional external content")
        self.assertFalse((self.project / ".scholar-route.lock").exists())

    def test_bibtex_preserves_venue_types_escapes_data_and_avoids_key_collisions(self):
        state = self.state()
        state["records"]["papers"] = [
            paper("p:a", title=r"Fictional {A} & 50%_ # $ ~ ^ \command", venue_type="conference", venue="Fixture Meeting"),
            paper("p.a", venue_type="preprint", venue="Fictional repository"),
        ]
        result = bibtex(state)
        self.assertIn("@inproceedings{", result)
        self.assertIn("booktitle = {Fixture Meeting}", result)
        self.assertIn("@misc{", result)
        self.assertIn("howpublished = {Fictional repository}", result)
        self.assertIn(r"\{A\} \& 50\%\_ \# \$", result)
        keys = [line.split("{", 1)[1].rstrip(",") for line in result.splitlines() if line.startswith("@")]
        self.assertEqual(len(set(keys)), 2)

    def test_map_only_contains_recorded_links_and_sanitizes_mermaid_labels(self):
        state = self.state()
        graph = map_markdown(state)
        diagram = graph.split("```mermaid", 1)[1].split("```", 1)[0]
        self.assertNotIn("<tag>", diagram)
        self.assertNotIn('"claim";', diagram)
        expected_edges = {"S1 --> P1", "S1 --> C1", "P1 --> C1",
                          "S1 --> J1", "S2 --> J1", "P1 --> J1"}
        actual_edges = {line.strip() for line in diagram.splitlines() if " --> " in line}
        self.assertEqual(actual_edges, expected_edges)
        empty = self.state()
        empty["records"] = {pool: [] for pool in KINDS.values()}
        self.assertNotIn("```mermaid", map_markdown(empty))

    def test_fingerprint_is_key_order_independent_and_changes_with_evidence(self):
        state = self.state()
        reordered = dict(reversed(list(state.items())))
        self.assertEqual(fingerprint(state), fingerprint(reordered))
        record(self.project, "source", {"id": "publisher", "title": "Updated fictional evidence"})
        self.assertNotEqual(fingerprint(state), fingerprint(self.state()))


if __name__ == "__main__":
    unittest.main()
