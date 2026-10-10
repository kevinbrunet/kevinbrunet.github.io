#!/usr/bin/env python3
"""Recompute the oracle articles from public DeepSWE trials and Epoch's review.

Python standard library; offline inputs, no missing trials synthesized. The
chronological early-stop replay is a simulation, not an actual adaptive run.
"""
import argparse
import collections
import csv
import gzip
import hashlib
import html
import json
import math
import pathlib
import re


def load(path):
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt', encoding='utf-8') as handle:
        return json.load(handle)


def mean(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else None


def success(row):
    if row['reward'] is None and not row['passed']:
        return False
    if row['reward'] not in (0, 1) or bool(row['reward']) != row['passed']:
        raise ValueError(f"Inconsistent binary result: {row['trial_name']}")
    return row['passed']


def display_cost(row):
    # Uniform proportional tariff changes in the official JS dated 2026-10-06.
    # The raw cost is kept separately; never label this an actual invoice.
    factor = {'gpt-5-6-luna': 0.2, 'glm-5-3-flash': 0.5}.get(row['model'], 1)
    return None if row['cost_usd'] is None else row['cost_usd'] * factor


def paired_test(a, b, universe):
    a_only, b_only = len((a-b)&universe), len((b-a)&universe)
    discordant = a_only+b_only
    p = min(1, 2*sum(math.comb(discordant, i) for i in range(min(a_only,b_only)+1))/2**discordant) if discordant else 1
    return {'both_pass': len(a&b&universe), 'a_only': a_only, 'b_only': b_only,
            'both_fail': len(universe-(a|b)), 'exact_mcnemar_p': p}


def replay(sequence, grouped, universe):
    remaining = set(universe)
    stages = []
    for config in sequence:
        received = len(remaining)
        recovered, attempts, cost = set(), 0, 0.0
        for task in sorted(remaining):
            for row in grouped[config].get(task, []):
                attempts += 1
                value = display_cost(row)
                if value is None:
                    raise ValueError('Replay cost missing')
                cost += value
                if success(row):
                    recovered.add(task)
                    break
        remaining -= recovered
        stages.append({'config': config, 'tasks_received': received, 'recovered': len(recovered),
                       'attempts': attempts, 'cost_usd_repriced': cost})
    return {'stages': stages, 'remaining_tasks': sorted(remaining),
            'attempts': sum(s['attempts'] for s in stages),
            'cost_usd_repriced': sum(s['cost_usd_repriced'] for s in stages)}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--trials', type=pathlib.Path, required=True)
    ap.add_argument('--tasks', type=pathlib.Path, required=True)
    ap.add_argument('--epoch', type=pathlib.Path, required=True)
    ap.add_argument('--output', type=pathlib.Path, default=pathlib.Path('analysis/deepswe-oracle'))
    args=ap.parse_args()
    universe={r['id'] for r in load(args.tasks)['rows']}
    if len(universe)!=113:
        raise ValueError('Unexpected task cohort')
    if args.epoch.suffix == '.gz':
        with gzip.open(args.epoch, 'rt', encoding='utf-8') as handle:
            epoch_html = handle.read()
    else:
        epoch_html=args.epoch.read_text(encoding='utf-8')
    epoch=[]
    for tr in re.findall(r'<tr\b[^>]*>(.*?)</tr>',epoch_html,re.S):
        cells=re.findall(r'<td\b[^>]*>(.*?)</td>',tr,re.S)
        if cells:
            tid=html.unescape(re.sub('<[^>]+>',' ',cells[0])).strip()
            if tid in universe: epoch.append(tid)
    if len(set(epoch))!=23:
        raise ValueError('Epoch task table changed; review parser and evidence')
    rows=[r for r in load(args.trials)['rows'] if r['source']=='deep-swe' and r.get('eval_scope')=='full']
    grouped=collections.defaultdict(lambda:collections.defaultdict(list))
    trial_ids=set()
    for row in rows:
        if row['trial_name'] in trial_ids:
            raise ValueError('Duplicate trial')
        trial_ids.add(row['trial_name'])
        if row['harness']!='mini-swe-agent' or row['task_name'] not in universe:
            raise ValueError('Unexpected harness or task scope')
        success(row)
        grouped[row['config']][row['task_name']].append(row)
    for tasks in grouped.values():
        for trials in tasks.values():
            if len(trials)>4: raise ValueError('More than four trials; do not truncate')
            trials.sort(key=lambda r:(r['started_at'],r['trial_name']))
    luna='mini_swe_agent_gpt_5_6_luna_max'
    astra='mini_swe_agent_gpt_6_astra_xhigh'
    flash='mini_swe_agent_glm_5_3_flash_max'
    glm='mini_swe_agent_glm_5_2_max'
    if any(k not in grouped for k in [luna,astra,flash,glm]):
        raise ValueError('Reference config unavailable')
    sets={k:{t for t,rs in tasks.items() if any(success(r) for r in rs)} for k,tasks in grouped.items()}
    failures=universe-sets[luna]
    clean=universe-set(epoch)
    metrics=[]
    for config,tasks in grouped.items():
        all_rows=[r for rs in tasks.values() for r in rs]
        scored=[r for r in all_rows if r['included_in_score']]
        first=all_rows[0]
        metrics.append({'config': config,'model':first['model'],'effort':first['reasoning_effort'],
                        'harness':first['harness'],'n_trials':len(all_rows),'n_scored':len(scored),
                        'n_errored':sum(r['errored'] for r in all_rows),'tasks_with_trials':len(tasks),
                        'n_missing_rewards':sum(r['reward'] is None for r in all_rows),
                        'trial_count_distribution':dict(collections.Counter(len(rs) for rs in tasks.values())),
                        'mean_single_trial_pass_rate':mean([r['score_value'] for r in scored]),
                        'observed_up_to_four_union':len(sets[config]),
                        'mean_cost_usd_raw':mean([r['cost_usd'] for r in all_rows]),
                        'mean_cost_usd_repriced':mean([display_cost(r) for r in all_rows]),
                        'mean_steps':mean([r['n_agent_steps'] for r in all_rows]),
                        'mean_duration_seconds':mean([r['agent_duration_seconds'] for r in all_rows]),
                        'luna_failures_recovered':len(sets[config]&failures),
                        'recovered_task_ids':sorted(sets[config]&failures),
                        'epoch_flagged_recovered':sorted(sets[config]&failures&set(epoch)),
                        'clean_union_out_of_90':len(sets[config]&clean),
                        'clean_luna_failures_recovered':len((sets[config]-sets[luna])&clean)})
    metrics.sort(key=lambda m:(-m['luna_failures_recovered'],m['config']))
    # Frontier of displayed/repriced single-trial economics; not a hypothesis test.
    # Only Luna and Flash pricing are adjusted; other models use their raw prices.
    # Include this restriction in output, so no current-price frontier is claimed.
    frontier=[m for m in metrics if not any(
        x['mean_cost_usd_repriced']<=m['mean_cost_usd_repriced'] and x['mean_single_trial_pass_rate']>=m['mean_single_trial_pass_rate']
        and (x['mean_cost_usd_repriced']<m['mean_cost_usd_repriced'] or x['mean_single_trial_pass_rate']>m['mean_single_trial_pass_rate']) for x in metrics)]
    forward=replay([flash,luna,glm],grouped,universe)
    reverse=replay([luna,flash,glm],grouped,universe)
    claude_metrics=[m for m in metrics if m['model'].startswith('claude-')]
    best_claude=max(claude_metrics,key=lambda m:m['mean_single_trial_pass_rate'])
    best_claude_budget=len(universe)*best_claude['mean_cost_usd_repriced']
    best_claude_baseline={
        'config':best_claude['config'],
        'model':best_claude['model'],
        'effort':best_claude['effort'],
        'tasks':len(universe),
        'mean_single_trial_pass_rate':best_claude['mean_single_trial_pass_rate'],
        'mean_cost_usd_repriced':best_claude['mean_cost_usd_repriced'],
        'estimated_single_attempt_budget_usd':best_claude_budget,
        'saving_vs_flash_luna_glm_usd':best_claude_budget-forward['cost_usd_repriced'],
        'relative_saving_vs_flash_luna_glm':1-forward['cost_usd_repriced']/best_claude_budget,
        'comparison_basis':'Mean single-attempt cost multiplied by task count; chain cost from retrospective replay.'
    }
    most_expensive_claude=max(claude_metrics,key=lambda m:m['mean_cost_usd_repriced'])
    claude_first_rows=[trials[0] for trials in grouped[most_expensive_claude['config']].values()]
    if len(claude_first_rows)!=len(universe) or any(display_cost(r) is None for r in claude_first_rows):
        raise ValueError('Most expensive Claude first-attempt baseline is incomplete')
    claude_first_cost=sum(display_cost(r) for r in claude_first_rows)
    claude_first_baseline={
        'config':most_expensive_claude['config'],
        'model':most_expensive_claude['model'],
        'effort':most_expensive_claude['effort'],
        'tasks':len(claude_first_rows),
        'accepted':sum(success(r) for r in claude_first_rows),
        'cost_usd_repriced':claude_first_cost,
        'saving_vs_flash_luna_glm_usd':claude_first_cost-forward['cost_usd_repriced'],
        'relative_saving_vs_flash_luna_glm':1-forward['cost_usd_repriced']/claude_first_cost,
    }
    cumulative=[]
    covered=set()
    for i in range(4):
        before=len(covered)
        covered|={t for t in failures if len(grouped[flash][t])>i and success(grouped[flash][t][i])}
        cumulative.append({'chronological_trial_position':i+1,'new_successes':len(covered)-before,'cumulative_recovered':len(covered)})
    report={'retrieved_at':'2026-10-06','task_count':113,'configuration_count':len(grouped),
            'ordering':'started_at then trial_name within each task/config; no chronological position invented for absent trials',
            'error_policy':'Single-trial mean uses non-null score_value for included_in_score rows. Union uses actual published successes; missing rewards and errored trials yield no recorded success, not a diagnosis of candidate incorrectness. Trials remain in replay cost when cost exists. Missing trials are not synthesized.',
            'cost_policy':'Raw costs retained; Luna multiplied by 0.2, GLM Flash by 0.5, reproducing the official UI proportional tariff updates on 2026-10-06. Other models retain raw prices; the saved frontier is not a fully repriced current-market frontier.',
            'input_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [args.trials,args.tasks,args.epoch]},
            'epoch_flagged_tasks':sorted(epoch),'luna_failures':sorted(failures),
            'luna_failures_flagged_by_epoch':sorted(failures&set(epoch)),
            'sensitivity_scope':{'excluded_task_ids':sorted(epoch),'remaining_tasks':len(clean),'luna_union':len(sets[luna]&clean),'luna_remaining_failures':sorted(clean-sets[luna]),
                                 'luna_flash_union':len((sets[luna]|sets[flash])&clean)},
            'luna_vs_astra_paired':paired_test(sets[luna],sets[astra],universe),
            'flash_vs_opus_medium_on_luna_failures':paired_test(sets[flash],sets['mini_swe_agent_claude_opus_5_medium'],failures),
            'metrics':metrics,'single_trial_frontier_partial_repricing':frontier,
            'flash_recovery_chronological':cumulative,'flash_luna_glm_replay':forward,'luna_flash_glm_replay':reverse,
            'most_expensive_claude_first_attempt_baseline':claude_first_baseline,
            'highest_ranked_claude_mean_attempt_baseline':best_claude_baseline,
            'relative_replay_saving':1-forward['cost_usd_repriced']/reverse['cost_usd_repriced']}
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'analysis.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (args.output/'luna-failures-epoch.csv').open('w',encoding='utf-8',newline='') as h:
        w=csv.DictWriter(h,['task_id','flagged_by_epoch','flash_passed','astra_passed'])
        w.writeheader()
        w.writerows({'task_id':t,'flagged_by_epoch':t in epoch,'flash_passed':t in sets[flash],'astra_passed':t in sets[astra]} for t in sorted(failures))
    print(json.dumps({k:report[k] for k in ['luna_failures_flagged_by_epoch','sensitivity_scope','luna_vs_astra_paired','flash_vs_opus_medium_on_luna_failures','flash_recovery_chronological','flash_luna_glm_replay','luna_flash_glm_replay','most_expensive_claude_first_attempt_baseline']},indent=2))


if __name__=='__main__': main()
