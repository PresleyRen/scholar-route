"""Offline task-level journal routing and backward-compatible report tests."""
import tempfile
import unittest
from pathlib import Path

from project_store import init_project, record
from reports import export_project
from route_core import route


class JournalTrackTests(unittest.TestCase):
    def test_bilingual_database_systems_and_interfaces(self):
        cases = [
            ("AI4DB cardinality estimation and physical database query optimization", "ai4db"),
            ("用学习型索引优化数据库查询延迟", "ai4db"),
            ("论文用语言模型预测数据库连接的基数；有一个聊天 Agent 用来展示，主表是 q-error 和查询执行时长。", "ai4db"),
            ("An unsupervised database model evaluated by Q-error", "ai4db"),
            ("Text‑to‑SQL with execution accuracy on unseen schemas", "text-to-sql"),
            ("在跨表数据库上比较自然语言转SQL方法", "text-to-sql"),
        ]
        for topic, track in cases:
            with self.subTest(topic=topic):
                result = route(topic, stage="选刊")
                self.assertIn("computer-science", result["domains"])
                self.assertEqual(result["journal_tracks"]["primary"], track)

    def test_database_dependency_is_not_a_database_research_contribution(self):
        for topic in ("Tool selection for an agent that uses an SQL database for storage",
                      "历史记录存入SQL数据库，主表是工具选择准确率",
                      "Tool routing with the chat history stored in a SQL database"):
            with self.subTest(topic=topic):
                result = route(topic, stage="journal")
                self.assertNotIn("humanities", result["domains"])
                tracks = result["journal_tracks"]
                self.assertEqual(tracks["primary"], "tool-routing")
                self.assertNotIn("ai4db", [c["id"] for c in tracks["candidates"]])
                self.assertNotIn("text-to-sql", [c["id"] for c in tracks["candidates"]])
        self.assertIn("humanities", route("历史文献研究，聊天历史记录存入SQL数据库")["domains"])

    def test_task_outcome_distinguishes_classification_and_end_to_end_agents(self):
        cases = [
            ("LLM for multi-intent classification and slot filling", "intent-nlu"),
            ("Intent classification in an end-to-end agent, measured by intent F1", "intent-nlu"),
            ("在意图识别和工具路由基础上，测端到端任务完成率", "agent-systems"),
        ]
        for topic, expected in cases:
            with self.subTest(topic=topic):
                tracks = route(topic, stage="dossier")["journal_tracks"]
                self.assertEqual(tracks["primary"], expected)
                self.assertTrue(all(c["signals"] for c in tracks["candidates"]))

    def test_mixed_ontology_rag_or_competing_outcomes_needs_manuscript(self):
        for topic, expected in (
            ("跨文档 RAG 与本体复用", {"ontology", "rag-retrieval"}),
            ("Tool selection accuracy and task completion rate for an LLM agent",
             {"tool-routing", "agent-systems"}),
        ):
            with self.subTest(topic=topic):
                tracks = route(topic, stage="journal")["journal_tracks"]
                self.assertIsNone(tracks["primary"])
                self.assertEqual({r["id"] for r in tracks["candidates"]}, expected)

    def test_domain_application_requires_ai_and_application_context(self):
        self.assertEqual(route("medical imaging classification")["journal_tracks"]["primary"],
                         "domain-application")
        for topic in ["临床药物研究", "A garage and a reagent used for a clinical trial",
                      "clinical database of 300 patients", "SQL", "AI agent",
                      "Network latency and a Q-error statistic"]:
            with self.subTest(topic=topic):
                tracks = route(topic, stage="journal")["journal_tracks"]
                self.assertEqual(tracks["candidates"], [])
                self.assertIsNone(tracks["primary"])

    def test_explicit_domain_preserved_while_existing_project_can_get_finer_route(self):
        topic = "Learned index for cardinality estimation"
        result = route(topic, ["general"], stage="journal")
        self.assertEqual(result["domains"], ["general"])
        self.assertEqual(result["signals"], {})
        self.assertEqual(result["journal_tracks"]["primary"], "ai4db")
        with tempfile.TemporaryDirectory() as path:
            dest = Path(path)
            init_project(dest, topic, domains=["general"], stage="journal")
            before = (dest / "project.json").read_bytes()
            export_project(dest)
            report = (dest / "REPORT.md").read_text(encoding="utf-8")
            self.assertIn("ai4db", report)
            self.assertIn("cardinality estimation", report)
            self.assertEqual(before, (dest / "project.json").read_bytes())

    def test_broad_dbai_requires_a_more_specific_task(self):
        result = route("DBAI", stage="journal")
        self.assertIn("computer-science", result["domains"])
        self.assertIsNone(result["journal_tracks"]["primary"])

    def test_earlier_project_stage_with_a_journal_record_shows_tracks(self):
        with tempfile.TemporaryDirectory() as path:
            dest = Path(path)
            init_project(dest, "Paper on learned indexes", ["general"], stage="explore")
            record(dest, "journal", {"id": "example", "title": "Fixture Journal"})
            before = (dest / "project.json").read_bytes()
            export_project(dest)
            report = (dest / "REPORT.md").read_text(encoding="utf-8")
            self.assertIn("阶段：explore", report)
            self.assertIn("ai4db", report)
            self.assertEqual(before, (dest / "project.json").read_bytes())

    def test_chinese_workflow_aliases_and_plain_llm(self):
        for alias in ["审刊", "查单刊"]:
            self.assertEqual(route("topic", stage=alias)["stage"], "dossier")
        self.assertEqual(route("topic", stage="核稿")["stage"], "audit")
        self.assertEqual(route("LLM for intent classification")["domains"], ["computer-science"])
