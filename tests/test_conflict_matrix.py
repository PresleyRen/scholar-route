"""Cross-module regressions and source/repair-index integrity.

All journal facts are synthetic. Route tests exercise 288 combinations; workflow
review cases are maintained separately and are not counted as model benchmarks.
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import coverage_audit as coverage
from project_store import init_project, load_project, record, resolve_fact, set_constraints
from route_core import REGIONS, STAGES, asset, route
from venue_audit import assess, shortlist
from test_core import ProjectCase, fact, journal, constraints, ISSNS, STALE


class ConflictMatrixTests(ProjectCase):
    def setUp(self):
        super().setUp()
        self.add_evidence()

    def test_domain_stage_region_matrix(self):
        modules = asset('modules.json')
        count = 0
        for domain in asset('domains.json'):
            for stage in STAGES:
                for region in REGIONS:
                    with self.subTest(domain=domain['id'], stage=stage, region=region):
                        selected = {domain['id']}
                        if domain['id'] == 'agent-ai':
                            selected.add('computer-science')
                        expected = {m['id'] for m in modules
                                    if (stage == 'full' or stage in m['stages'])
                                    and (not m.get('domains') or selected.intersection(m['domains']))
                                    and (not m.get('regions') or region in m['regions'])}
                        actual = route('Synthetic topic', [domain['id']], stage, region)
                        self.assertEqual(set(actual['modules']), expected)
                        self.assertEqual(set(actual['modules']) | {x['id'] for x in actual['skipped']},
                                         {m['id'] for m in modules})
                        self.assertFalse(set(actual['modules']) & {x['id'] for x in actual['skipped']})
                        count += 1
        self.assertEqual(count, 288)

    def test_full_agent_china_route_can_reach_every_registered_capability(self):
        result = route('Synthetic topic', ['agent-ai'], 'full', 'china')
        self.assertEqual(set(result['modules']), {m['id'] for m in asset('modules.json')})

    def test_agent_medical_and_food_routes_keep_complementary_sources(self):
        result = route('LLM nutrition clinical study', ['agent-ai', 'biomedicine', 'food-agriculture'])
        self.assertTrue({'PubMed', 'DBLP', 'AGRICOLA', 'arXiv'} <= set(result['sources']))
        self.assertTrue({'agent-capabilities', 'agent-systems', 'evidence-review'} <= set(result['modules']))
        self.assertEqual(len(result['sources']), len(set(result['sources'])))

    def test_plain_biomedical_agent_does_not_force_llm_profile(self):
        result = route('clinical drug study with antimicrobial agents')
        self.assertEqual(result['domains'], ['biomedicine'])
        self.assertNotIn('agent-capabilities', result['modules'])
        self.assertNotIn('DBLP', result['sources'])

    def test_journal_stage_keeps_discovery_dossier_and_constraints_together(self):
        result = route('LLM Agent recovery', stage='journal')
        expected = {'manuscript-profile', 'venue-discovery', 'journal-dossier', 'indexing-metrics',
                    'costs-timelines', 'fit-comparison', 'submission-plan', 'state-map'}
        self.assertTrue(expected <= set(result['modules']))
        self.assertNotIn('proof-check', result['modules'])

    def test_resume_preserves_language_and_constraints(self):
        with tempfile.TemporaryDirectory() as folder:
            dest = Path(folder) / 'case'
            init_project(dest, 'Research', ['agent-ai'], language='zh-CN',
                         constraints={'max_mandatory_fee': {'amount': 0, 'currency': 'USD'}})
            before = (dest / 'project.json').read_bytes()
            init_project(dest, 'Research', ['biomedicine'], language='en')
            self.assertEqual((dest / 'project.json').read_bytes(), before)
            state = load_project(dest)
            self.assertEqual(state['language'], 'zh-CN')
            self.assertEqual(state['constraints']['max_mandatory_fee']['amount'], 0)

    def test_turnaround_endpoints_remain_separate(self):
        value = journal()
        for field, days in [('first_decision_days', 2), ('external_review_days', 50),
                            ('acceptance_days', 110), ('publication_days', 125)]:
            value['facts'][field] = fact(days)
        record(self.project, 'journal', value)
        observed = self.state()['records']['journals'][0]['facts']
        self.assertEqual([observed[x]['value'] for x in ('first_decision_days', 'external_review_days',
                                                        'acceptance_days', 'publication_days')],
                         [2, 50, 110, 125])

    def test_shortlist_does_not_pad_to_requested_size(self):
        rows = [{'id': 'one', 'title': 'One', 'status': 'eligible', 'fit_score': 4, 'publisher': 'P'}]
        result = shortlist(rows, limit=5)
        self.assertEqual(result['ids'], ['one'])
        self.assertEqual(len(rows), 1)

    def test_smallest_verified_failure_wins_over_high_fit_and_unknowns(self):
        value = journal()
        value['facts']['mandatory_fee']['value'] = 101
        del value['facts']['indexing']
        value['fit']['score'] = 5
        record(self.project, 'journal', value)
        set_constraints(self.project, constraints())
        result = assess(self.state())
        self.assertEqual([x['id'] for x in result['pools']['excluded']], ['journal-1'])
        self.assertEqual(result['shortlist']['ids'], [])
        self.assertIn('unknown', [x['status'] for x in result['pools']['excluded'][0]['checks']])

    def test_optional_oa_route_does_not_override_mandatory_fee(self):
        value = journal()
        value['facts']['oa_route'] = fact('Optional open access; subscription route available')
        value['facts']['mandatory_fee'] = fact(0, currency='USD', includes_all_mandatory=True)
        record(self.project, 'journal', value)
        set_constraints(self.project, {'max_mandatory_fee': {'amount': 0, 'currency': 'USD'}})
        result = assess(self.state())
        self.assertEqual(len(result['pools']['eligible']), 1)

    def test_contradictory_quartile_updates_keep_both_sources(self):
        record(self.project, 'journal', journal())
        other = copy.deepcopy(journal()['metrics'][0])
        other['value'] = 'Q3'
        record(self.project, 'journal', {'id': 'journal-1', 'metrics': [other]})
        set_constraints(self.project, constraints())
        state = self.state()
        self.assertEqual(len(state['records']['journals'][0]['metrics']), 2)
        self.assertEqual(len(assess(state)['pools']['unverified']), 1)

    def test_conflict_reimport_is_idempotent_then_explained_resolution_passes(self):
        record(self.project, 'journal', journal())
        changed = {'id': 'journal-1', 'facts': {'mandatory_fee': fact(75, currency='USD', includes_all_mandatory=True)}}
        record(self.project, 'journal', changed)
        before = self.bytes()
        self.assertFalse(record(self.project, 'journal', changed)['changed'])
        self.assertEqual(self.bytes(), before)
        set_constraints(self.project, constraints())
        self.assertEqual(len(assess(self.state())['pools']['unverified']), 1)
        resolve_fact(self.project, 'journal-1', 'mandatory_fee', 'Reviewed updated synthetic policy', ['publisher'])
        self.assertEqual(len(assess(self.state())['pools']['eligible']), 1)
        conflict = self.state()['records']['journals'][0]['conflicts'][0]
        self.assertEqual(conflict['previous']['value'], 50)
        self.assertEqual(conflict['incoming']['value'], 75)
        self.assertEqual(conflict['status'], 'resolved')

    def test_stale_high_fit_does_not_displace_current_candidate(self):
        old = journal('old', issns=[ISSNS[0]])
        old['fit'].update(score=5, assessed_at=STALE)
        current = journal('current', issns=[ISSNS[1]])
        record(self.project, 'journal', old)
        record(self.project, 'journal', current)
        result = assess(self.state(), limit=1)
        self.assertEqual(result['shortlist']['ids'], ['current'])
        self.assertIn('old', result['shortlist']['unranked_eligible'])
        self.assertEqual(len(result['pools']['eligible']), 2)

    def test_ties_have_deterministic_order_independent_of_input_order(self):
        rows = [{'id': i, 'title': title, 'status': 'eligible', 'fit_score': 4, 'publisher': i}
                for i, title in [('b', 'Beta'), ('a', 'Alpha'), ('c', 'Gamma')]]
        self.assertEqual(shortlist(rows)['ids'], shortlist(list(reversed(rows)))['ids'])
        self.assertEqual(shortlist(rows)['ids'], ['a', 'b', 'c'])

    def test_unscored_candidate_remains_in_pool_without_zero_imputation(self):
        value = journal()
        del value['fit']
        record(self.project, 'journal', value)
        result = assess(self.state())
        self.assertIsNone(result['pools']['eligible'][0]['fit_score'])
        self.assertEqual(result['shortlist']['unranked_eligible'], ['journal-1'])


class CoverageAuditTests(unittest.TestCase):
    def cloned_root(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        dest = Path(temp.name) / 'repo'
        shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns('.git', '__pycache__', 'work'))
        return dest

    def mutate(self, root, fn):
        path = root / coverage.SKILL / 'assets/upstreams.json'
        value = json.loads(path.read_text(encoding='utf-8'))
        fn(value)
        path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')

    def test_all_prior_sources_and_features_have_actionable_mappings(self):
        result = coverage.inventory()
        self.assertEqual(result['errors'], [])
        self.assertEqual((result['source_repositories'], result['source_features'], result['capabilities']), (17, 139, 41))
        self.assertTrue(all(result['coverage'].values()))

    def test_removed_source_is_detected(self):
        root = self.cloned_root()
        self.mutate(root, lambda x: x['sources'].pop())
        self.assertFalse(coverage.inventory(root)['ok'])

    def test_empty_feature_mapping_is_detected(self):
        root = self.cloned_root()
        self.mutate(root, lambda x: x['sources'][0]['modules'][0].update(capability_ids=[]))
        self.assertTrue(any('empty feature mapping' in e for e in coverage.inventory(root)['errors']))

    def test_unknown_capability_is_detected(self):
        root = self.cloned_root()
        self.mutate(root, lambda x: x['sources'][0]['modules'][0]['capability_ids'].append('nonexistent'))
        self.assertTrue(any('unknown capability' in e for e in coverage.inventory(root)['errors']))

    def test_unpinned_source_evidence_is_detected(self):
        root = self.cloned_root()
        self.mutate(root, lambda x: x['sources'][0]['modules'][0]['upstream_evidence'][0].update(url='https://example.org/main'))
        self.assertTrue(any('not commit/path pinned' in e for e in coverage.inventory(root)['errors']))

    def test_missing_workflow_file_is_detected(self):
        root = self.cloned_root()
        (root / coverage.SKILL / 'references/publication.md').unlink()
        self.assertTrue(any('missing workflow reference' in e for e in coverage.inventory(root)['errors']))

    def test_missing_test_selector_is_detected(self):
        with patch.object(coverage, 'CONFLICTS', [*coverage.CONFLICTS[:-1], ('CF33', 'case', 'intake', 'missing.test')]):
            self.assertTrue(any('missing executable test' in e for e in coverage.inventory()['errors']))

    def test_symptom_and_upstream_search_point_to_repair_files(self):
        for query, expected in [('费用', 'costs-timelines'), ('agent-systems', 'agent-systems'),
                                ('journal-recommender', 'venue-discovery')]:
            with self.subTest(query=query):
                rows = coverage.locate(query)
                row = next(r for r in rows if r['id'] == expected)
                self.assertTrue((ROOT / row['workflow']).is_file())
                self.assertTrue(row['sources'])

    def test_empty_and_unknown_queries_are_distinct(self):
        with self.assertRaises(ValueError):
            coverage.locate('   ')
        self.assertEqual(coverage.locate('this-feature-does-not-exist-93871'), [])

    def test_program_and_workflow_checks_have_separate_counts(self):
        result = coverage.inventory()
        self.assertEqual(result['conflicts'], result['behavioral_conflicts'] + result['workflow_review_conflicts'])
        self.assertGreater(result['behavioral_conflicts'], 0)
        self.assertGreater(result['workflow_review_conflicts'], 0)

    def test_generated_index_links_every_capability_and_conflict(self):
        text = coverage.render()
        for module in asset('modules.json'):
            self.assertIn('`' + module['id'] + '`', text)
        for cid, _, _, _ in coverage.CONFLICTS:
            self.assertIn('| ' + cid + ' |', text)

    def test_query_cli_reports_no_match_with_exit_three(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(coverage.main(['--find', 'this-feature-does-not-exist-93871']), 3)

    def test_duplicate_source_feature_names_are_detected(self):
        root = self.cloned_root()
        self.mutate(root, lambda x: x['sources'][0]['modules'].append(copy.deepcopy(x['sources'][0]['modules'][0])))
        self.assertTrue(any('duplicate feature names' in e for e in coverage.inventory(root)['errors']))

    def test_missing_workflow_review_is_detected(self):
        root = self.cloned_root()
        (root / 'docs/WORKFLOW-REVIEW.md').unlink()
        result = coverage.inventory(root)
        self.assertEqual(sum('workflow review scenario' in e for e in result['errors']), 15)
