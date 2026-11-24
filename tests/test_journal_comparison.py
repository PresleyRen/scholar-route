"""Journal evidence shown in the regular offline report using fictional records."""
from pathlib import Path

from project_store import record
from reports import export_project
from test_core import ProjectCase, STALE, fact, journal, source


class JournalComparisonTests(ProjectCase):
    def render(self):
        before = self.bytes()
        files = export_project(self.project)["files"]
        self.assertEqual(self.bytes(), before)
        path = next(Path(name) for name in files if Path(name).name == "REPORT.md")
        return path.read_text(encoding="utf-8")

    def comparison(self):
        return self.render().split("### 期刊证据对照", 1)[1].split("### 待人工复核", 1)[0]

    def test_report_shows_fee_rank_fit_and_separate_endpoints_without_constraints(self):
        self.add_evidence()
        candidate = journal()
        candidate["facts"].update({
            "scope": fact("Tool selection"),
            "oa_route": fact("Subscription"),
            "first_decision_days": fact(7),
            "publication_days": fact(18, notes="Acceptance to first online, median for 2025."),
        })
        record(self.project, "journal", candidate)
        result = self.comparison()
        for expected in ("Tool selection", "10.99999/fixture.study", "50 USD", "Subscription",
                         "Fixture Index", "JCR 2024 Fictional Studies Q2 [index]", "首次决定 7 天",
                         "未记录起止点", "录用 待核实", "首次上线 待核实", "编入期次 待核实",
                         "发表（原记录口径） 18 天", "Acceptance to first online"):
            self.assertIn(expected, result)
        self.assertNotIn("录用 18", result)

    def test_first_online_issue_and_legacy_facts_keep_their_own_sources_and_intervals(self):
        self.add_evidence()
        record(self.project, "source", source("article-history", "paper"))
        candidate = journal()
        candidate["facts"].update({
            "first_online_days": fact(17, "article-history", notes="Accepted to first online, one paper."),
            "issue_publication_days": fact(99, notes="Receipt to issue, publisher median."),
            "publication_days": fact(65, notes="Historical aggregate with unspecified endpoint."),
        })
        record(self.project, "journal", candidate)
        result = self.comparison()
        self.assertIn("首次上线 17 天（已发表论文的日期观察）（Accepted to first online, one paper.） [article-history", result)
        self.assertIn("编入期次 99 天（Receipt to issue, publisher median.） [publisher", result)
        self.assertIn("发表（原记录口径） 65 天（Historical aggregate with unspecified endpoint.） [publisher", result)
        self.assertIn("录用 待核实", result)

    def test_unknown_fees_stale_sources_and_conflicting_quartiles_remain_visible(self):
        self.add_evidence()
        candidate = journal()
        candidate["facts"].update({
            "mandatory_fee": fact(0, currency="USD", includes_all_mandatory=False, conditional=True),
            "scope": fact("Unsupported scope", "community"),
            "acceptance_days": fact(29, checked_at=STALE),
        })
        metric = candidate["metrics"][0]
        candidate["metrics"].extend([{**metric, "value": "Q4"}, {**metric, "category": "Other category"}])
        record(self.project, "journal", candidate)
        result = self.comparison()
        for expected in ("总额待核实，记录金额 0 USD", "优惠或适用条件待确认", "必付项目未核全",
                         "录用 待核实（核查已过期）", "待核实（缺当前一手证据）",
                         "Fictional Studies 待核实（来源冲突）", "Other category Q2 [index]"):
            self.assertIn(expected, result)
        self.assertNotIn("Unsupported scope", result)
        self.assertNotIn("29 天", result)

    def test_section_only_expands_current_journal_candidates(self):
        self.assertNotIn("### 期刊证据对照", self.render())
        self.add_evidence()
        candidate = journal(title="Proceedings fixture")
        candidate["facts"]["venue_type"] = fact("conference")
        record(self.project, "journal", candidate)
        self.assertNotIn("### 期刊证据对照", self.render())
        record(self.project, "journal", {"id": "lead", "title": "Unverified | lead"})
        result = self.comparison()
        self.assertNotIn("Proceedings fixture", result)
        self.assertIn(r"Unverified \| lead", result)
        self.assertIn("类型待核实", result)
        self.assertIn("分区待核实", result)
        self.assertIn("首次决定、外审、录用、首次上线、编入期次均待核实", result)
