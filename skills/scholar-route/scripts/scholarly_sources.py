"""Bounded, read-only scholarly metadata search using the Python standard library.

No records are generated when a provider fails. Results are discovery leads, not
proof of indexing, journal quality, acceptance likelihood, or an exhaustive review.
The optional ``transport`` callable is for tests; application callers normally omit it.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import math
import os
import re
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any, Callable


PROVIDERS = ("openalex", "crossref", "dblp", "arxiv")
MAX_RESPONSE_BYTES = 2 * 1024 * 1024
MAX_QUERY_CHARS = 1024
ENDPOINTS = {
    "openalex": "https://api.openalex.org/works",
    "crossref": "https://api.crossref.org/works",
    "dblp": "https://dblp.org/search/publ/api",
    "arxiv": "https://export.arxiv.org/api/query",
}
DOCS = {
    "openalex": "https://help.openalex.org/api/",
    "crossref": "https://www.crossref.org/documentation/retrieve-metadata/rest-api/",
    "dblp": "https://dblp.org/faq/How%2Bto%2Buse%2Bthe%2Bdblp%2Bsearch%2BAPI.html",
    "arxiv": "https://info.arxiv.org/help/api/user-manual.html",
}
_ATOM = "{http://www.w3.org/2005/Atom}"
_ARXIV = "{http://arxiv.org/schemas/atom}"
_OPENSEARCH = "{http://a9.com/-/spec/opensearch/1.1/}"
_LAST_ARXIV_REQUEST = 0.0


class SourceError(Exception):
    """A safe error containing no response body, URL credentials, or raw exception."""

    def __init__(self, code: str, message: str, retryable: bool = False):
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    # In particular, do not forward an Authorization header across a redirect.
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _text(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    return " ".join(html.unescape(value).split()) or None


def _url(value: Any) -> str | None:
    value = _text(value)
    if not value:
        return None
    try:
        parsed = urllib.parse.urlsplit(value)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            return None
        if parsed.username is not None or parsed.password is not None:
            return None
    except ValueError:
        return None
    return value


def normalize_doi(value: Any) -> str | None:
    """Normalize an observed DOI, without completing or guessing a partial one."""
    value = _text(value)
    if not value:
        return None
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value, flags=re.I)
    value = re.sub(r"^doi:\s*", "", value, flags=re.I)
    value = urllib.parse.unquote(value).strip()
    return value.lower() if re.fullmatch(r"10\.\d{4,9}/\S+", value) else None


def _year(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, str) and re.fullmatch(r"\d{4}", value):
        value = int(value)
    if isinstance(value, int) and 1000 <= value <= 9999:
        return value
    return None


def _dict(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list:
    return value if isinstance(value, list) else []


def _names(values: list) -> list[str]:
    names = []
    for value in values:
        if isinstance(value, dict):
            value = value.get("text") or value.get("name")
        name = _text(value)
        if name and name not in names:
            names.append(name)
    return names


def _record(provider: str, source_url: str, identity: str, title: str,
            doi: str | None, url: str | None, year: int | None,
            venue: str | None, venue_type: str, authors: list[str], **extra) -> dict:
    return {
        "id": identity,
        "title": title,
        "doi": doi,
        "url": url,
        "year": year,
        "venue": venue,
        "venue_type": venue_type,
        "authors": authors,
        "source_provider": provider,
        "source_url": source_url,
        **extra,
    }


def _decode_json(body: bytes) -> dict:
    try:
        obj = json.loads(body.decode("utf-8-sig"),
                         parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (UnicodeError, ValueError, RecursionError):
        raise SourceError("invalid_response", "Provider returned malformed JSON.") from None
    if not isinstance(obj, dict):
        raise SourceError("invalid_response", "Provider JSON root is not an object.")
    return obj


def _parse_openalex(body: bytes, source_url: str) -> tuple[list[dict], list[str], int | None]:
    obj = _decode_json(body)
    if obj.get("error") or not isinstance(obj.get("results"), list):
        raise SourceError("invalid_response", "OpenAlex returned an error or no results array.")
    records, skipped = [], 0
    for item in obj["results"]:
        item = _dict(item)
        identity, title = _url(item.get("id")), _text(item.get("display_name") or item.get("title"))
        if not identity or not title:
            skipped += 1
            continue
        doi = normalize_doi(item.get("doi"))
        location = _dict(item.get("primary_location"))
        source = _dict(location.get("source"))
        venue_type = {
            "journal": "journal", "conference": "conference",
            "repository": "repository", "book series": "book-series",
        }.get(_text(source.get("type")), "unknown")
        # A preprint retains its repository type even if metadata cites a later journal.
        if item.get("type") == "preprint":
            venue_type = "preprint"
        authors = _names([_dict(_dict(a).get("author")).get("display_name")
                          for a in _list(item.get("authorships"))])
        records.append(_record("openalex", source_url, identity, title, doi,
                               _url(location.get("landing_page_url")) or identity,
                               _year(item.get("publication_year")),
                               _text(source.get("display_name")), venue_type, authors,
                               provider_work_type=_text(item.get("type")),
                               issns=[v for v in _list(source.get("issn")) if isinstance(v, str)]))
    return records, _skip_warning(skipped), _count(_dict(obj.get("meta")).get("count"))


def _parse_crossref(body: bytes, source_url: str) -> tuple[list[dict], list[str], int | None]:
    obj = _decode_json(body)
    message = _dict(obj.get("message"))
    if obj.get("status") != "ok" or not isinstance(message.get("items"), list):
        raise SourceError("invalid_response", "Crossref returned an error or no items array.")
    records, skipped = [], 0
    for item in message["items"]:
        item = _dict(item)
        doi = normalize_doi(item.get("DOI"))
        title = next((t for t in (_text(t) for t in _list(item.get("title"))) if t), None)
        if not doi or not title:
            skipped += 1
            continue
        venue = next((v for v in (_text(v) for v in _list(item.get("container-title"))) if v), None)
        venue_type = {"journal-article": "journal", "proceedings-article": "conference",
                      "posted-content": "preprint", "book-chapter": "book"}.get(_text(item.get("type")), "unknown")
        year = None
        for field in ("published", "published-print", "published-online", "issued"):
            date_parts = _list(_dict(item.get(field)).get("date-parts"))
            if date_parts and isinstance(date_parts[0], list) and date_parts[0]:
                year = _year(date_parts[0][0])
                if year is not None:
                    break
        authors = []
        for author in _list(item.get("author")):
            author = _dict(author)
            name = _text(author.get("name")) or _text(" ".join(
                p for p in (_text(author.get("given")), _text(author.get("family"))) if p))
            if name:
                authors.append(name)
        records.append(_record("crossref", source_url, "doi:" + doi, title, doi,
                               _url(item.get("URL")) or "https://doi.org/" + doi,
                               year, venue, venue_type, authors,
                               provider_work_type=_text(item.get("type")),
                               issns=[v for v in _list(item.get("ISSN")) if isinstance(v, str)]))
    return records, _skip_warning(skipped), _count(message.get("total-results"))


def _parse_dblp(body: bytes, source_url: str) -> tuple[list[dict], list[str], int | None]:
    obj = _decode_json(body)
    result = _dict(obj.get("result"))
    hits = _dict(result.get("hits"))
    if not hits or "@total" not in hits:
        raise SourceError("invalid_response", "DBLP returned an error or no hits metadata.")
    total = _count(hits.get("@total"))
    if total is None:
        raise SourceError("invalid_response", "DBLP returned a malformed result count.")
    raw = hits.get("hit", [])
    if isinstance(raw, dict):
        raw = [raw]
    if not isinstance(raw, list) or (total and not raw):
        raise SourceError("invalid_response", "DBLP returned inconsistent hit data.")
    records, skipped = [], 0
    for hit in raw:
        item = _dict(_dict(hit).get("info"))
        title, url = _text(item.get("title")), _url(item.get("url"))
        key = _text(item.get("key"))
        if not title or not (url or key):
            skipped += 1
            continue
        author_data = _dict(item.get("authors")).get("author", [])
        authors = _names(author_data if isinstance(author_data, list) else [author_data])
        venue_type = {"Journal Articles": "journal", "Conference and Workshop Papers": "conference",
                      "Informal Publications": "preprint", "Books and Theses": "book"}.get(_text(item.get("type")), "unknown")
        records.append(_record("dblp", source_url, "dblp:" + key if key else url,
                               title, normalize_doi(item.get("doi")), url,
                               _year(item.get("year")), _text(item.get("venue")),
                               venue_type, authors, provider_work_type=_text(item.get("type"))))
    return records, _skip_warning(skipped), total


def _parse_arxiv(body: bytes, source_url: str) -> tuple[list[dict], list[str], int | None]:
    # Reject DTD/entity declarations; this client needs only a plain Atom document.
    if re.search(br"<!\s*(?:DOCTYPE|ENTITY)", body, flags=re.I):
        raise SourceError("invalid_response", "arXiv returned unsupported XML declarations.")
    try:
        feed = ET.fromstring(body)
    except (ET.ParseError, ValueError, RecursionError):
        raise SourceError("invalid_response", "arXiv returned malformed XML.") from None
    if feed.tag != _ATOM + "feed":
        raise SourceError("invalid_response", "arXiv did not return an Atom feed.")
    total = _count(feed.findtext(_OPENSEARCH + "totalResults"))
    if total is None:
        raise SourceError("invalid_response", "arXiv feed lacks result count metadata.")
    records, skipped = [], 0
    for entry in feed.findall(_ATOM + "entry"):
        identity = _url(entry.findtext(_ATOM + "id"))
        title = _text(entry.findtext(_ATOM + "title"))
        if identity and "/api/errors" in identity:
            raise SourceError("provider_error", "arXiv reported a query error; review query syntax.")
        if not identity or not title:
            skipped += 1
            continue
        records.append(_record("arxiv", source_url, identity, title,
                               normalize_doi(entry.findtext(_ARXIV + "doi")), identity,
                               _year((entry.findtext(_ATOM + "published") or "")[:4]),
                               "arXiv", "preprint",
                               _names([a.findtext(_ATOM + "name") for a in entry.findall(_ATOM + "author")]),
                               journal_reference=_text(entry.findtext(_ARXIV + "journal_ref")),
                               updated=_text(entry.findtext(_ATOM + "updated"))))
    return records, _skip_warning(skipped), total


def _count(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, str) and value.isdigit():
        value = int(value)
    return value if isinstance(value, int) and value >= 0 else None


def _skip_warning(skipped: int) -> list[str]:
    return [f"Skipped {skipped} malformed record(s) with missing identity or title."] if skipped else []


def _download(url: str, headers: dict[str, str], timeout: float, max_bytes: int) -> bytes:
    request = urllib.request.Request(url, headers=headers, method="GET")
    opener = urllib.request.build_opener(_NoRedirect())
    try:
        with opener.open(request, timeout=timeout) as response:
            if response.status != 200:
                raise SourceError("http_error", "Provider returned a non-success status.")
            body = response.read(max_bytes + 1)
    except urllib.error.HTTPError as exc:
        code = int(exc.code)
        # Never serialize exc: it can contain credentials, raw response data, or private queries.
        exc.close()
        raise SourceError(f"http_{code}", f"Provider returned HTTP {code}.", code == 429 or code >= 500) from None
    except (urllib.error.URLError, OSError, TimeoutError, socket.timeout):
        raise SourceError("network_error", "Provider could not be reached within the request limits.", True) from None
    if len(body) > max_bytes:
        raise SourceError("response_too_large", "Provider response exceeded the configured byte limit.")
    return body


def search(provider: str, query: str, limit: int = 10, timeout: float = 20, **options) -> dict:
    """Search one bounded first page, returning metadata and explicit incompleteness.

    Options: ``transport`` (test-only callable accepting url, headers, timeout,
    max_bytes), ``max_bytes`` (1..2 MiB), ``arxiv_advanced`` (bool; default false).
    Plain arXiv queries are searched as one quoted phrase in the all field. Set
    arxiv_advanced=True for an explicit arXiv boolean/field query. Other providers
    receive the query unchanged. Read OPENALEX_API_KEY from the process environment
    when present; no accounts are created and no key or contact email is invented.

    Invalid arguments raise ValueError. Provider/network failures return an error
    envelope with zero records. No retries or pagination happen implicitly.
    """
    if not isinstance(provider, str) or provider.lower() not in PROVIDERS:
        raise ValueError("provider must be one of: " + ", ".join(PROVIDERS))
    provider = provider.lower()
    if not isinstance(query, str) or not query.strip() or len(query) > MAX_QUERY_CHARS:
        raise ValueError(f"query must contain 1..{MAX_QUERY_CHARS} characters")
    query = query.strip()
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 100:
        raise ValueError("limit must be an integer from 1 to 100")
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or not 1 <= timeout <= 60:
        raise ValueError("timeout must be a finite number from 1 to 60 seconds")
    unknown = set(options) - {"transport", "max_bytes", "arxiv_advanced"}
    if unknown:
        raise ValueError("unsupported search option")
    max_bytes = options.get("max_bytes", MAX_RESPONSE_BYTES)
    if isinstance(max_bytes, bool) or not isinstance(max_bytes, int) or not 1 <= max_bytes <= MAX_RESPONSE_BYTES:
        raise ValueError(f"max_bytes must be an integer from 1 to {MAX_RESPONSE_BYTES}")
    advanced = options.get("arxiv_advanced", False)
    if not isinstance(advanced, bool):
        raise ValueError("arxiv_advanced must be a boolean")
    transport: Callable = options.get("transport", _download)
    if not callable(transport):
        raise ValueError("transport must be callable")
    params = {
        "openalex": {"search": query, "per_page": limit, "page": 1},
        "crossref": {"query.bibliographic": query, "rows": limit},
        "dblp": {"q": query, "format": "json", "h": limit, "f": 0, "c": 0},
        "arxiv": {"search_query": query if advanced else 'all:"' + query.replace('"', " ") + '"',
                  "start": 0, "max_results": limit, "sortBy": "relevance", "sortOrder": "descending"},
    }[provider]
    source_url = ENDPOINTS[provider] + "?" + urllib.parse.urlencode(params)
    headers = {"User-Agent": "ScholarRoute/1.0 (scholarly metadata discovery)",
               "Accept": "application/atom+xml" if provider == "arxiv" else "application/json",
               "Accept-Encoding": "identity"}
    api_key = os.environ.get("OPENALEX_API_KEY", "").strip() if provider == "openalex" else ""
    if api_key:
        if any(ord(c) < 32 or ord(c) == 127 for c in api_key):
            raise ValueError("OPENALEX_API_KEY contains invalid header characters")
        headers["Authorization"] = "Bearer " + api_key
    envelope = {
        "provider": provider, "query": query, "retrieved_at": _utc_now(),
        "source_url": source_url, "documentation_url": DOCS[provider], "records": [],
        "completeness": {"returned": 0, "requested": limit, "exhaustive": False,
                         "reason": "A bounded first page from one provider; no systematic-review completeness claim."},
        "warnings": [],
    }
    if provider == "arxiv" and not advanced:
        envelope["warnings"].append("arXiv plain query uses an all-field phrase; use arxiv_advanced for explicit boolean syntax.")
    try:
        if provider == "arxiv" and transport is _download:
            global _LAST_ARXIV_REQUEST
            # Only repeated calls in this process are spaced; callers coordinating
            # multiple processes must also honor the provider's current usage rules.
            pause = 3.0 - (time.monotonic() - _LAST_ARXIV_REQUEST)
            if pause > 0:
                time.sleep(pause)
            _LAST_ARXIV_REQUEST = time.monotonic()
        body = transport(source_url, headers, float(timeout), max_bytes)
        if not isinstance(body, bytes):
            raise SourceError("invalid_response", "Transport must return response bytes.")
        if len(body) > max_bytes:
            raise SourceError("response_too_large", "Provider response exceeded the configured byte limit.")
        parser = {"openalex": _parse_openalex, "crossref": _parse_crossref,
                  "dblp": _parse_dblp, "arxiv": _parse_arxiv}[provider]
        records, warnings, total = parser(body, source_url)
        seen, selected = set(), []
        for record in records:
            identity = record["id"]
            if identity in seen:
                continue
            seen.add(identity)
            selected.append(record)
            if len(selected) >= limit:
                break
        envelope["records"] = selected
        envelope["warnings"].extend(warnings)
        envelope["completeness"].update(returned=len(selected), provider_reported_total=total)
        if records and len(seen) < len(records):
            envelope["warnings"].append("Duplicate or excess records were removed within this response.")
    except SourceError as exc:
        envelope["error"] = {"code": exc.code, "message": exc.message, "retryable": exc.retryable}
        envelope["completeness"]["reason"] = "Request failed; zero returned records do not mean zero relevant publications."
    return envelope
