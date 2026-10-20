"""Deterministic tests. All papers, authors, identifiers, and numbers are fixtures."""

import io
import json
import unittest
import urllib.error
import urllib.parse
from unittest.mock import patch

import scholarly_sources as sources


def payload(value):
    return json.dumps(value).encode("utf-8")


def transport(body):
    return lambda url, headers, timeout, max_bytes: body


def oa_work(**updates):
    return {"id": "https://openalex.org/W9999999999", "display_name": "Fixture agent experiment",
            "doi": "https://doi.org/10.5555/Fixture.1", "publication_year": 2025, "type": "article",
            "primary_location": {"source": {"display_name": "Fixture Journal", "type": "journal",
                                              "issn": ["1234-5678"]}},
            "authorships": [{"author": {"display_name": "Fixture Author"}}], **updates}


def crossref_work(**updates):
    return {"DOI": "10.5555/FIXTURE.2", "title": ["Fixture systems paper"],
            "container-title": ["Fixture Conference"], "type": "proceedings-article",
            "published": {"date-parts": [[2024]]},
            "author": [{"given": "Fixture", "family": "Author"}], **updates}


ARXIV = b'''<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
 xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/"
 xmlns:arxiv="http://arxiv.org/schemas/atom">
<opensearch:totalResults>25</opensearch:totalResults>
<entry><id>http://arxiv.org/abs/2601.99999v2</id>
<title>Fixture\n  agent preprint</title><published>2026-01-01T00:00:00Z</published>
<updated>2026-02-01T00:00:00Z</updated><author><name>Fixture Author</name></author>
<arxiv:journal_ref>Fixture Journal 1 (2026)</arxiv:journal_ref>
<arxiv:doi>10.5555/fixture.3</arxiv:doi></entry></feed>'''


class SearchTests(unittest.TestCase):
    def test_openalex_normalizes_observed_metadata_and_provenance(self):
        result = sources.search("openalex", "agent", transport=transport(payload(
            {"results": [oa_work()], "meta": {"count": 40}})))
        work = result["records"][0]
        self.assertEqual(work["doi"], "10.5555/fixture.1")
        self.assertEqual(work["authors"], ["Fixture Author"])
        self.assertEqual(work["venue_type"], "journal")
        self.assertEqual(work["source_url"], result["source_url"])
        self.assertEqual(result["completeness"]["provider_reported_total"], 40)
        self.assertFalse(result["completeness"]["exhaustive"])

    def test_crossref_conference_is_not_a_journal(self):
        result = sources.search("crossref", "agent", transport=transport(payload(
            {"status": "ok", "message": {"items": [crossref_work()], "total-results": 9}})))
        self.assertEqual(result["records"][0]["venue_type"], "conference")
        self.assertEqual(result["records"][0]["year"], 2024)
        self.assertEqual(result["records"][0]["id"], "doi:10.5555/fixture.2")

    def test_dblp_single_hit_and_single_author_shapes(self):
        body = payload({"result": {"hits": {"@total": "1", "hit": {"info": {
            "title": "Fixture paper", "key": "journals/fixture/item", "year": "2023",
            "type": "Journal Articles", "venue": "Fixture Journal",
            "url": "https://dblp.org/rec/journals/fixture/item",
            "authors": {"author": {"text": "Fixture Author"}}}}}}})
        result = sources.search("dblp", "agent", transport=transport(body))
        self.assertEqual(result["records"][0]["authors"], ["Fixture Author"])
        self.assertEqual(result["records"][0]["venue_type"], "journal")
        self.assertEqual(result["records"][0]["year"], 2023)

    def test_arxiv_keeps_preprint_identity_despite_journal_reference(self):
        result = sources.search("arxiv", "agent", transport=transport(ARXIV))
        record = result["records"][0]
        self.assertEqual(record["title"], "Fixture agent preprint")
        self.assertEqual(record["venue_type"], "preprint")
        self.assertEqual(record["venue"], "arXiv")
        self.assertIn("v2", record["id"])
        self.assertEqual(record["doi"], "10.5555/fixture.3")
        self.assertEqual(record["journal_reference"], "Fixture Journal 1 (2026)")

    def test_arxiv_advanced_query_round_trip_and_encoded_separators(self):
        query = 'ti:"agent memory" AND cat:cs.AI'
        result = sources.search("arxiv", query, arxiv_advanced=True, transport=transport(ARXIV))
        params = urllib.parse.parse_qs(urllib.parse.urlsplit(result["source_url"]).query)
        self.assertEqual(params["search_query"], [query])
        self.assertEqual(params["max_results"], ["10"])

    def test_plain_arxiv_query_is_documented_as_phrase(self):
        result = sources.search("arxiv", "agent memory", transport=transport(ARXIV))
        params = urllib.parse.parse_qs(urllib.parse.urlsplit(result["source_url"]).query)
        self.assertEqual(params["search_query"], ['all:"agent memory"'])
        self.assertTrue(any("phrase" in v for v in result["warnings"]))

    def test_missing_fields_stay_unknown(self):
        body = payload({"results": [oa_work(publication_year=None, primary_location=None, doi=None)]})
        record = sources.search("openalex", "agent", transport=transport(body))["records"][0]
        self.assertIsNone(record["year"])
        self.assertIsNone(record["doi"])
        self.assertIsNone(record["venue"])
        self.assertEqual(record["venue_type"], "unknown")

    def test_openalex_preprint_is_not_reclassified_as_journal(self):
        body = payload({"results": [oa_work(type="preprint")]})
        record = sources.search("openalex", "agent", transport=transport(body))["records"][0]
        self.assertEqual(record["venue_type"], "preprint")

    def test_valid_empty_results_are_distinct_from_failure(self):
        fixtures = {
            "openalex": {"results": [], "meta": {"count": 0}},
            "crossref": {"status": "ok", "message": {"items": [], "total-results": 0}},
            "dblp": {"result": {"hits": {"@total": "0"}}},
        }
        for provider, body in fixtures.items():
            with self.subTest(provider=provider):
                result = sources.search(provider, "fixture-no-hits", transport=transport(payload(body)))
                self.assertNotIn("error", result)
                self.assertEqual(result["records"], [])
                self.assertFalse(result["completeness"]["exhaustive"])

    def test_http_200_error_bodies_do_not_create_papers(self):
        fixtures = {
            "openalex": payload({"error": "quota", "results": []}),
            "crossref": payload({"status": "failed", "message": "bad"}),
            "dblp": payload({"error": "bad"}),
            "arxiv": ARXIV.replace(b"http://arxiv.org/abs/2601.99999v2", b"http://arxiv.org/api/errors#invalid"),
        }
        for provider, body in fixtures.items():
            with self.subTest(provider=provider):
                result = sources.search(provider, "agent", transport=transport(body))
                self.assertIn("error", result)
                self.assertEqual(result["records"], [])

    def test_arxiv_non_feed_and_entity_documents_rejected(self):
        for body in (b"<html>login</html>", b'<!DOCTYPE f [<!ENTITY x "boom">]><f>&x;</f>'):
            with self.subTest(body=body):
                result = sources.search("arxiv", "agent", transport=transport(body))
                self.assertEqual(result["error"]["code"], "invalid_response")

    def test_json_nonfinite_nonobject_or_html_rejected(self):
        for body in (b"[]", b"<html>Sign in</html>", b'{"results":[],"bad":NaN}'):
            with self.subTest(body=body):
                result = sources.search("openalex", "agent", transport=transport(body))
                self.assertEqual(result["error"]["code"], "invalid_response")

    def test_partial_bad_record_retains_good_records_and_warns(self):
        result = sources.search("openalex", "agent", transport=transport(payload(
            {"results": [{"display_name": "No identifier"}, oa_work()]})))
        self.assertEqual(len(result["records"]), 1)
        self.assertTrue(any("Skipped 1" in w for w in result["warnings"]))

    def test_malformed_optional_type_does_not_crash_parser(self):
        result = sources.search("crossref", "agent", transport=transport(payload(
            {"status": "ok", "message": {"items": [crossref_work(type={"bad": "shape"})]}})))
        self.assertEqual(result["records"][0]["venue_type"], "unknown")

    def test_deduplication_and_limit_enforced_even_when_server_ignores_limit(self):
        result = sources.search("openalex", "agent", limit=2, transport=transport(payload(
            {"results": [oa_work(), oa_work(), oa_work(id="https://openalex.org/W9999999998"),
                         oa_work(id="https://openalex.org/W9999999997")]})))
        self.assertEqual(len(result["records"]), 2)
        self.assertEqual(len({r["id"] for r in result["records"]}), 2)
        self.assertEqual(result["completeness"]["returned"], 2)

    def test_credentials_are_only_in_header(self):
        requests = []

        def capture(url, headers, timeout, max_bytes):
            requests.append((url, headers))
            return payload({"results": []})

        with patch.dict("os.environ", {"OPENALEX_API_KEY": "fixture-secret-key"}):
            result = sources.search("openalex", "agent", transport=capture)
        self.assertNotIn("fixture-secret-key", json.dumps(result))
        self.assertNotIn("fixture-secret-key", requests[0][0])
        self.assertEqual(requests[0][1]["Authorization"], "Bearer fixture-secret-key")

    def test_no_key_required_for_basic_openalex(self):
        headers_seen = []

        def capture(url, headers, timeout, max_bytes):
            headers_seen.append(headers)
            return payload({"results": []})

        with patch.dict("os.environ", {}, clear=True):
            result = sources.search("openalex", "agent", transport=capture)
        self.assertNotIn("Authorization", headers_seen[0])
        self.assertNotIn("error", result)

    def test_network_exception_details_do_not_leak(self):
        error = urllib.error.URLError("https://private?api_key=fixture-secret-key")
        with patch("urllib.request.OpenerDirector.open", side_effect=error):
            result = sources.search("openalex", "agent")
        self.assertEqual(result["error"]["code"], "network_error")
        self.assertNotIn("fixture-secret-key", json.dumps(result))
        self.assertIn("do not mean zero", result["completeness"]["reason"])

    def test_http_error_safe_code_and_retryability(self):
        error = urllib.error.HTTPError("https://private?api_key=fixture-secret-key", 429,
                                       "fixture-secret-key", {}, io.BytesIO(b"private body"))
        with patch("urllib.request.OpenerDirector.open", side_effect=error):
            result = sources.search("crossref", "agent")
        self.assertEqual(result["error"]["code"], "http_429")
        self.assertTrue(result["error"]["retryable"])
        self.assertNotIn("fixture-secret-key", json.dumps(result))

    def test_response_size_bound_applies_to_injected_transport(self):
        result = sources.search("openalex", "agent", max_bytes=12, transport=transport(b"x" * 13))
        self.assertEqual(result["error"]["code"], "response_too_large")

    def test_no_untrusted_redirects_are_followed(self):
        self.assertIsNone(sources._NoRedirect().redirect_request(None, None, 302, "", {}, "https://other.invalid"))

    def test_invalid_inputs_rejected_before_network(self):
        cases = [
            (("pubmed", "agent"), {}), (("openalex", ""), {}),
            (("openalex", "x" * 1025), {}), (("openalex", "agent"), {"limit": 101}),
            (("openalex", "agent"), {"limit": True}), (("openalex", "agent"), {"timeout": 61}),
            (("openalex", "agent"), {"timeout": float("nan")}),
            (("openalex", "agent"), {"max_bytes": 2097153}),
            (("openalex", "agent"), {"url": "https://untrusted.invalid"}),
            (("openalex", "agent"), {"arxiv_advanced": "yes"}),
            (("openalex", "agent"), {"transport": False}),
        ]
        with patch("scholarly_sources._download", side_effect=AssertionError("network should not run")):
            for args, kwargs in cases:
                with self.subTest(args=args, kwargs=kwargs), self.assertRaises(ValueError):
                    sources.search(*args, **kwargs)

    def test_doi_normalization_does_not_guess_invalid_identifier(self):
        self.assertEqual(sources.normalize_doi("https://doi.org/10.5555%2FFixture.A"), "10.5555/fixture.a")
        self.assertEqual(sources.normalize_doi("doi:10.5555/Fixture.A"), "10.5555/fixture.a")
        self.assertIsNone(sources.normalize_doi("unknown"))

    def test_invalid_api_key_header_rejected_without_exposing_value(self):
        with patch.dict("os.environ", {"OPENALEX_API_KEY": "secret\r\nheader"}):
            with self.assertRaises(ValueError) as exc:
                sources.search("openalex", "agent", transport=transport(payload({"results": []})))
        self.assertNotIn("secret", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
