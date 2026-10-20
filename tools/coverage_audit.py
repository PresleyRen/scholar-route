"""Trace source traits, capabilities, conflict tests and repair locations.

This offline maintenance tool checks provenance and routing contracts. Test links
are classified as executable behavior or host-workflow review, never conflated.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path('skills/scholar-route')

# source ID: distinctive contribution, complementary source IDs
SOURCE_TRAITS = {
    'zero-journal-recommender': ('摘要画像与投稿梯队', ['chinese-research-latex', 'journal-research-plugins']),
    'journal-research-plugins': ('中英文、多数据库发现与权威核验分工', ['sci-select', 'journal-fit-finder']),
    'sci-select': ('相似论文反查期刊、本地索引及选刊模式切换', ['journal-research-plugins', 'chinese-research-latex']),
    'chinese-research-latex': ('从候选发现深入到单刊全景调查', ['journal-research-plugins', 'ai-research-skills']),
    'journal-fit-finder': ('主题、方法、读者、文种与出版商多样性比较', ['zero-journal-recommender', 'journal-atlas']),
    'polish-skill': ('精读、创新审计、论证重构、写作与回复衔接', ['scientific-agent-skills', 'academic-publishing-skills']),
    'academic-publishing-skills': ('投稿前询问至清样、更正的发表生命周期', ['polish-skill', 'superpapers']),
    'superpapers': ('复现驱动的问题发现、实验计划与稳健性', ['ai-research-skills', 'scientific-agent-skills']),
    'researcher': ('研究流水线、代码分析、竞争方法与版本管理', ['superpapers', 'longtable']),
    'scientific-agent-skills': ('论文身份、综述方法、证据批判与模板检查', ['ai-research-skills', 'journal-research-plugins']),
    'ai-research-skills': ('区分 ML 能力贡献与系统设计贡献', ['superpapers', 'academic-publishing-skills']),
    'journal-atlas': ('结构化期刊档案与证据等级、档案更新', ['journal-research-plugins', 'journal-fit-finder']),
    'journal-finder-local': ('由文献定位发表社区、本地索引维护', ['journal-research-plugins', 'chinese-research-latex']),
    'cn-journal-selector': ('中文期刊条件和国内目录路径', ['journal-research-plugins', 'journal-fit-finder']),
    'awesome-journal-skills': ('学科与具体发表场所的写作要求', ['journal-research-plugins', 'academic-publishing-skills']),
    'food-nutrition-skills': ('食品农业专项检索、研究计划和展示流程', ['scientific-agent-skills', 'superpapers']),
    'longtable': ('项目访谈、互补审稿视角与持续证据包', ['researcher', 'polish-skill']),
}

# IDs are stable repair handles. A workflow row is a review scenario, not an
# executable claim about LLM output. Behavioral selectors point at real tests.
CONFLICTS = [
 ('CF01', '按任务按需加载', 'intake field-map', 'test_core.RoutingTests.test_stage_alias_and_region_filter_modules_and_sources'),
 ('CF02', '稿件批评、适配与梯队分工', 'peer-review fit-comparison submission-plan', ''),
 ('CF03', '刊级统计与个人机会分开', 'submission-plan', 'test_core.VenueAuditTests.test_primary_evidence_passes_constraints_without_predicting_acceptance'),
 ('CF04', '缺值进入待核实池', 'fit-comparison indexing-metrics', 'test_core.VenueAuditTests.test_confirmed_violation_excludes_even_when_another_fact_is_unknown'),
 ('CF05', '分区精确到体系年度类别', 'indexing-metrics', 'test_core.VenueAuditTests.test_quartiles_require_exact_system_year_category_and_consistent_values'),
 ('CF06', '动态事实刷新后使用', 'indexing-metrics costs-timelines', 'test_core.VenueAuditTests.test_stale_or_unverified_evidence_does_not_satisfy_hard_constraints'),
 ('CF07', '候选数量随证据变化', 'submission-plan', 'test_conflict_matrix.ConflictMatrixTests.test_shortlist_does_not_pad_to_requested_size'),
 ('CF08', '研究对象决定检索与评价路线', 'field-map evidence-review', 'test_conflict_matrix.ConflictMatrixTests.test_agent_medical_and_food_routes_keep_complementary_sources'),
 ('CF09', '文献证据与投稿载体分开', 'venue-identity identifier-check', 'test_core.VenueAuditTests.test_unknown_venue_type_is_unverified_and_known_conference_is_excluded'),
 ('CF10', '多源召回与出版社多样性', 'venue-discovery fit-comparison', 'test_core.VenueAuditTests.test_shortlist_retains_pools_and_applies_fit_order_and_publisher_cap'),
 ('CF11', '实际可比论文优于粗略数量', 'fit-comparison', ''),
 ('CF12', '必缴费用、可选 OA 与减免分开', 'costs-timelines', 'test_core.VenueAuditTests.test_fee_caps_distinguish_zero_cost_waivers_completeness_and_currency'),
 ('CF13', '四种审稿时间端点分别保存', 'costs-timelines', 'test_conflict_matrix.ConflictMatrixTests.test_turnaround_endpoints_remain_separate'),
 ('CF14', '出版风险按具体证据判断', 'journal-integrity', ''),
 ('CF15', '中文目录和商业平台分开', 'regional-indexing', ''),
 ('CF16', '复用语言与已知偏好', 'intake manuscript-writing', 'test_conflict_matrix.ConflictMatrixTests.test_resume_preserves_language_and_constraints'),
 ('CF17', '论文身份与阅读深度分开', 'identifier-check evidence-review', 'test_core.VenueAuditTests.test_fit_requires_read_paper_current_assessment_and_current_verified_source'),
 ('CF18', '去重同时保留版本', 'identifier-check state-map', 'test_cli_import.ImportTests.test_preprint_and_publication_with_same_doi_stay_separate'),
 ('CF19', '保留检索覆盖记录', 'search-protocol', 'test_core.MalformedInputTests.test_search_exhaustiveness_requires_explicit_coverage_record'),
 ('CF20', '接口失败、空结果与成功分开', 'paper-search', 'test_scholarly_sources.SearchTests.test_http_200_error_bodies_do_not_create_papers'),
 ('CF21', '一个改写负责人、多个核查视角', 'argument-audit manuscript-writing', ''),
 ('CF22', '作者贡献与声明统一登记', 'authorship-credit', ''),
 ('CF23', '模拟审稿归并异议', 'peer-review', ''),
 ('CF24', '准备文件与外部发送分开执行', 'submission-preflight cover-letter', ''),
 ('CF25', '统一项目状态和操作决策', 'state-map intake', ''),
 ('CF26', '续做项目保留历史', 'state-map', 'test_core.ProjectLifecycleTests.test_create_resume_and_wrong_topic_preserve_project'),
 ('CF27', '原生工具、Agent 工作流及外部服务分别标注', 'paper-search implementation', ''),
 ('CF28', '源码、文档和数据的来源分别登记', 'state-map', ''),
 ('CF29', '格式合规与科学审查分工', 'submission-preflight peer-review', ''),
 ('CF30', '适配分与证据完整度分开', 'fit-comparison', 'test_core.VenueAuditTests.test_fit_requires_read_paper_current_assessment_and_current_verified_source'),
 ('CF31', '当前作者指南优先于排版样本', 'venue-formatting', ''),
 ('CF32', '更正材料与编辑决定分开', 'postpublication-correction', ''),
 ('CF33', '文献纳入标准与投稿分区分开', 'evidence-review indexing-metrics', ''),
]

NATIVE = {
 'intake': ['route_core.py', 'project_store.py'],
 'paper-search': ['scholarly_sources.py', 'search_import.py'],
 'identifier-check': ['project_store.py', 'scholarly_sources.py'],
 'state-map': ['project_store.py', 'reports.py'],
 'venue-identity': ['project_store.py', 'venue_audit.py'],
 'indexing-metrics': ['project_store.py', 'venue_audit.py'],
 'costs-timelines': ['project_store.py', 'venue_audit.py'],
 'fit-comparison': ['venue_audit.py'],
 'submission-plan': ['venue_audit.py'],
 'regional-indexing': ['route_core.py'],
}
ALIASES = {
 'costs-timelines': '费用 免费 APC 审稿速度 fee cost waiver turnaround',
 'indexing-metrics': '分区 SCI SCIE ESCI JCR SJR CAS quartile index',
 'state-map': '地图 历史 断点 恢复 去重 map history resume storage',
 'agent-capabilities': '规划 记忆 工具调用 多智能体 planning memory tool',
 'agent-systems': '架构 故障 重试 幂等 state runtime recovery retry',
 'paper-search': '检索 搜不到 API 接口 provider search retrieval',
 'venue-discovery': '候选 期刊 少 漏刊 candidate journal discovery',
 'manuscript-writing': '写作 英文 润色 prose writing English',
 'peer-review': '审稿 质疑 拒稿 review critique',
 'figure-table-audit': '图 表 单位 figure table SVG',
 'venue-formatting': '模板 格式 template formatting',
 'revision-response': '返修 回复 revision response rebuttal',
}


def load(root=ROOT):
    assets = root / SKILL / 'assets'
    return tuple(json.loads((assets / name).read_text(encoding='utf-8'))
                 for name in ('modules.json', 'domains.json', 'upstreams.json'))


def test_catalog(root=ROOT):
    """Read test names without importing or executing test modules."""
    found = {}
    for path in sorted((root / 'tests').glob('test_*.py')):
        tree = ast.parse(path.read_text(encoding='utf-8'))
        for cls in tree.body:
            if isinstance(cls, ast.ClassDef):
                for fn in cls.body:
                    if isinstance(fn, ast.FunctionDef) and fn.name.startswith('test_'):
                        found[f'{path.stem}.{cls.name}.{fn.name}'] = f'tests/{path.name}:{fn.lineno}'
    return found


def inventory(root=ROOT):
    modules, domains, upstream = load(root)
    sources = upstream['sources']
    catalog = test_catalog(root)
    errors = []
    mids = [m['id'] for m in modules]
    sids = [s['id'] for s in sources]
    if len(mids) != len(set(mids)):
        errors.append('duplicate capability IDs')
    if len(sids) != len(set(sids)):
        errors.append('duplicate source IDs')
    if set(sids) != set(SOURCE_TRAITS):
        errors.append('source trait inventory differs from provenance manifest')
    actual_count = sum(len(s['modules']) for s in sources)
    declared = upstream.get('coverage_count', {})
    if declared.get('source_repositories') != len(sources) or declared.get('provenance_entries') != actual_count:
        errors.append('declared source counts differ from actual records')
    coverage = {mid: [] for mid in mids}
    for source in sources:
        sid = source['id']
        sha = source.get('reference_commit', '')
        if not re.fullmatch('[a-f0-9]{40}', sha):
            errors.append(f'{sid}: invalid source commit')
        names = []
        for mapping in source['modules']:
            name = mapping.get('name', '')
            names.append(name)
            caps = mapping.get('capability_ids', [])
            if not name or not caps or not mapping.get('capability_summary', '').strip():
                errors.append(f'{sid}/{name}: empty feature mapping')
            for cap in caps:
                if cap not in coverage:
                    errors.append(f'{sid}/{name}: unknown capability {cap}')
                else:
                    coverage[cap].append({'source': sid, 'feature': name})
            evidence = mapping.get('upstream_evidence', [])
            if not evidence:
                errors.append(f'{sid}/{name}: missing source evidence')
            for item in evidence:
                prefix = source['url'].rstrip('/') + '/blob/' + sha + '/'
                if not item.get('path') or item.get('url') != prefix + item['path']:
                    errors.append(f'{sid}/{name}: source URL is not commit/path pinned')
                if not item.get('inspection_level'):
                    errors.append(f'{sid}/{name}: missing inspection depth')
        if len(names) != len(set(names)):
            errors.append(f'{sid}: duplicate feature names')
        for other in SOURCE_TRAITS.get(sid, ('', []))[1]:
            if other not in sids or other == sid:
                errors.append(f'{sid}: invalid complementary source {other}')
    for module in modules:
        mid = module['id']
        if not coverage[mid]:
            errors.append(f'{mid}: no upstream feature mapped')
        if not (root / SKILL / module['reference']).is_file():
            errors.append(f'{mid}: missing workflow reference')
        for file in NATIVE.get(mid, []):
            if not (root / SKILL / 'scripts' / file).is_file():
                errors.append(f'{mid}: missing implementation {file}')
    text = (root / SKILL / 'references/conflicts.md').read_text(encoding='utf-8')
    rule_ids = re.findall(r'\| (CF\d+) \|', text)
    if len(rule_ids) != len(set(rule_ids)) or set(rule_ids) != {r[0] for r in CONFLICTS}:
        errors.append('conflict register and test/review index differ')
    reviews_path = root / 'docs/WORKFLOW-REVIEW.md'
    reviews = reviews_path.read_text(encoding='utf-8') if reviews_path.is_file() else ''
    for cid, _, caps, test in CONFLICTS:
        if not set(caps.split()) <= set(mids):
            errors.append(f'{cid}: unknown capability in conflict mapping')
        if test and test not in catalog:
            errors.append(f'{cid}: missing executable test {test}')
        if not test and reviews.count(f'<a id="{cid.lower()}"></a>') != 1:
            errors.append(f'{cid}: missing or duplicate workflow review scenario')
    return {
        'ok': not errors, 'errors': errors, 'source_repositories': len(sources),
        'source_features': actual_count, 'capabilities': len(modules), 'domains': len(domains),
        'conflicts': len(CONFLICTS), 'behavioral_conflicts': sum(bool(r[3]) for r in CONFLICTS),
        'workflow_review_conflicts': sum(not bool(r[3]) for r in CONFLICTS),
        'coverage': coverage,
    }


def locate(query, root=ROOT):
    if not isinstance(query, str) or not query.strip():
        raise ValueError('Provide a capability ID, symptom or source name.')
    modules, _, upstream = load(root)
    inv = inventory(root)
    needle = query.casefold().strip()
    out = []
    source_by_id = {s['id']: s for s in upstream['sources']}
    for m in modules:
        mapped = inv['coverage'][m['id']]
        words = [m['id'], m['title'], m['description'], ALIASES.get(m['id'], '')]
        words += [x['feature'] + ' ' + x['source'] + ' ' + source_by_id[x['source']]['repository'] for x in mapped]
        if not any(needle in w.casefold() for w in words):
            continue
        conflicts = [r for r in CONFLICTS if m['id'] in r[2].split()]
        out.append({
            'id': m['id'], 'title': m['title'], 'workflow': str(SKILL / m['reference']),
            'implementation': [str(SKILL / 'scripts' / f) for f in NATIVE.get(m['id'], [])],
            'sources': sorted({x['source'] for x in mapped}),
            'conflicts': [r[0] for r in conflicts],
            'behavior_tests': sorted({r[3] for r in conflicts if r[3]}),
            'workflow_reviews': [r[0] for r in conflicts if not r[3]],
            'registry': str(SKILL / 'assets/modules.json'),
        })
    return out


def render(root=ROOT):
    modules, _, upstream = load(root)
    inv = inventory(root)
    catalog = test_catalog(root)
    lines = ['# 覆盖、互补与扩展定位索引', '',
             '由 `python tools/coverage_audit.py --write` 从注册表生成。', '',
             '## 覆盖摘要', '',
             f"{inv['source_repositories']} 个来源、{inv['source_features']} 条特点映射、{inv['capabilities']} 个能力、{inv['domains']} 个领域。",
             f"{inv['conflicts']} 条冲突中，{inv['behavioral_conflicts']} 条链接程序行为测试；其余 {inv['workflow_review_conflicts']} 条使用工作流审查。",
             '程序测试验证结构化输入的行为；工作流审查检查实际研究/写作产物。两者分别记录。', '',
             '## 来源特点如何互补', '', '| 来源 ID | 保留的特点 | 互补来源 |', '|---|---|---|']
    for sid, (trait, peers) in SOURCE_TRAITS.items():
        lines.append(f"| `{sid}` | {trait} | {', '.join(peers)} |")
    lines += ['', '## 能力到实现的定位', '',
              '每项能力的完整上游子技能映射见 [来源审计](source-audit.md)。', '',
              '| 能力 ID | 工作流文件 | 原生支撑代码 | 冲突/验收入口 |', '|---|---|---|---|']
    for m in modules:
        ref = str(SKILL / m['reference'])
        code = ', '.join(NATIVE.get(m['id'], [])) or 'Agent 按工作流执行'
        conflicts = ', '.join(r[0] for r in CONFLICTS if m['id'] in r[2].split()) or '按该模块具体产物验收'
        lines.append(f"| `{m['id']}` | [{m['reference']}](../{ref}) | {code} | {conflicts} |")
    lines += ['', '## 冲突测试与审查清单', '',
              'CF 编号对应 [冲突规则](../skills/scholar-route/references/conflicts.md)。', '',
              '| ID | 保留的组合方案 | 验证类型 | 定位 |', '|---|---|---|---|']
    for cid, resolution, _, test in CONFLICTS:
        if test:
            where = catalog.get(test, 'MISSING')
            path, _, number = where.partition(':')
            target = f'[{test}](../{path}#L{number})'
            kind = '程序行为测试'
        else:
            target = '[工作流验收场景](WORKFLOW-REVIEW.md#' + cid.lower() + ')'
            kind = '工作流审查'
        lines.append(f'| {cid} | {resolution} | {kind} | {target} |')
    lines += ['', '## 从症状到修改', '', '```text',
              '症状/能力ID/源技能名称', '  -> coverage_audit.py --find QUERY',
              '  -> 工作流文件 + 支撑代码 + CF编号 + 测试入口',
              '  -> 增加失败用例 -> 修改 -> 回归 -> 同步README/索引', '```', '',
              '```bash', 'python tools/coverage_audit.py --find "费用"',
              'python tools/coverage_audit.py --find agent-systems',
              'python tools/coverage_audit.py --find journal-recommender',
              'python tools/coverage_audit.py --write',
              'python tools/coverage_audit.py --check', 'python tests/run.py', '```', '',
              '新增领域：更新 `assets/domains.json` 和 `references/domains.md`，再做领域×阶段路由回归。',
              '新增能力：更新 `assets/modules.json`、工作流正文、`assets/upstreams.json` 和本工具的测试/互补映射。',
              '新增来源：记录完整提交、具体文件和特点，将其映射到现有或新增能力。',
              '新增冲突：在 `conflicts.md` 登记稳定编号；程序行为增加回归，模型工作流增加输入、实际输出和审查记录。',
              '新增接口：补正常、空值、错误、限流、版本、导入回滚和敏感字段检查。', '']
    return '\n'.join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    group = p.add_mutually_exclusive_group()
    group.add_argument('--find')
    group.add_argument('--write', action='store_true')
    group.add_argument('--check', action='store_true')
    args = p.parse_args(argv)
    result = inventory()
    if not result['ok']:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1
    if args.find is not None:
        try:
            rows = locate(args.find)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        print(json.dumps({'query': args.find, 'matches': rows}, ensure_ascii=False, indent=2))
        return 0 if rows else 3
    path = ROOT / 'docs/COVERAGE.md'
    if args.write:
        path.write_text(render(), encoding='utf-8')
    if args.check and (not path.is_file() or path.read_text(encoding='utf-8') != render()):
        print('Coverage index needs regeneration: python tools/coverage_audit.py --write')
        return 1
    print(json.dumps({k: v for k, v in result.items() if k != 'coverage'}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
