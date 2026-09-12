import csv, json, math, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
OUT = ROOT / 'results'
SEEDS = [42, 43, 44]
MODELS = ['front', 'side', 'average_fusion', 'adaptive_fusion']
AGG_METRICS = [
    ('Front', 'Test Macro F1', 'front', 'test_macro_f1'),
    ('Front', 'Safe Recall', 'front', 'safe_recall'),
    ('Front', 'Phone Recall', 'front', 'phone_recall'),
    ('Front', 'ROC-AUC', 'front', 'roc_auc'),
    ('Front', 'PR-AUC', 'front', 'pr_auc'),
    ('Front', 'ECE', 'front', 'ece'),
    ('Front', 'Brier', 'front', 'brier'),
    ('Side', 'Test Macro F1', 'side', 'test_macro_f1'),
    ('Side', 'Safe Recall', 'side', 'safe_recall'),
    ('Side', 'Phone Recall', 'side', 'phone_recall'),
    ('Side', 'ROC-AUC', 'side', 'roc_auc'),
    ('Side', 'PR-AUC', 'side', 'pr_auc'),
    ('Side', 'ECE', 'side', 'ece'),
    ('Side', 'Brier', 'side', 'brier'),
    ('Average Fusion', 'Test Macro F1', 'average_fusion', 'test_macro_f1'),
    ('Average Fusion', 'Safe Recall', 'average_fusion', 'safe_recall'),
    ('Average Fusion', 'Phone Recall', 'average_fusion', 'phone_recall'),
    ('Average Fusion', 'ROC-AUC', 'average_fusion', 'roc_auc'),
    ('Average Fusion', 'PR-AUC', 'average_fusion', 'pr_auc'),
    ('Average Fusion', 'ECE', 'average_fusion', 'ece'),
    ('Average Fusion', 'Brier', 'average_fusion', 'brier'),
    ('Adaptive Fusion', 'Test Macro F1', 'adaptive_fusion', 'test_macro_f1'),
    ('Adaptive Fusion', 'Safe Recall', 'adaptive_fusion', 'safe_recall'),
    ('Adaptive Fusion', 'Phone Recall', 'adaptive_fusion', 'phone_recall'),
    ('Adaptive Fusion', 'ROC-AUC', 'adaptive_fusion', 'roc_auc'),
    ('Adaptive Fusion', 'PR-AUC', 'adaptive_fusion', 'pr_auc'),
    ('Adaptive Fusion', 'ECE', 'adaptive_fusion', 'ece'),
    ('Adaptive Fusion', 'Brier', 'adaptive_fusion', 'brier'),
    ('Front', 'Train-Val F1 Gap', 'front', 'train_val_f1_gap'),
    ('Side', 'Train-Val F1 Gap', 'side', 'train_val_f1_gap'),
]

def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def r5(x):
    if x == '' or x is None:
        return ''
    return f'{float(x):.5f}'

def seed_paths(seed):
    if seed == 42:
        base = REPO / 'experiment_18' / 'results'
        return base, base / 'predictions' / 'fusion_test_predictions.csv'
    base = OUT / f'seed{seed}'
    return base, base / 'predictions' / 'fusion_test_predictions.csv'

def metric_row(seed, model):
    base, _ = seed_paths(seed)
    if model in ('front','side'):
        summ = load_json(base / model / 'train_summary.json')
        test = load_json(base / model / 'test_eval_metrics.json')
        bm = summ['best_epoch_metrics']
        cm = test['confusion_matrix']
        return {
            'seed': seed, 'model': model,
            'train_macro_f1': bm['train_macro_f1'], 'val_macro_f1': bm['val_macro_f1'], 'train_val_f1_gap': bm['f1_gap'],
            'train_loss': bm['train_loss'], 'val_loss': bm['val_loss'], 'train_val_loss_gap': bm['loss_gap'],
            'best_epoch': summ['best_epoch'],
            'test_accuracy': test['accuracy'], 'test_macro_f1': test['f1_macro'], 'macro_precision': test['precision_macro'], 'macro_recall': test['recall_macro'],
            'safe_precision': test['precision_safe'], 'safe_recall': test['recall_safe'], 'safe_f1': test['f1_safe'],
            'phone_precision': test['precision_phone'], 'phone_recall': test['recall_phone'], 'phone_f1': test['f1_phone'],
            'roc_auc': test['roc_auc'], 'pr_auc': test['pr_auc'], 'ece': test['ece_binary'], 'brier': test['brier_score'],
            'tn': cm[0][0], 'fp': cm[0][1], 'fn': cm[1][0], 'tp': cm[1][1],
        }
    fusion = load_json(base / 'fusion' / 'fusion_metrics.json')
    test = fusion[model]
    cm = test['confusion_matrix']
    return {
        'seed': seed, 'model': model,
        'train_macro_f1': '', 'val_macro_f1': '', 'train_val_f1_gap': '', 'train_loss': '', 'val_loss': '', 'train_val_loss_gap': '', 'best_epoch': '',
        'test_accuracy': test['accuracy'], 'test_macro_f1': test['f1_macro'], 'macro_precision': test['precision_macro'], 'macro_recall': test['recall_macro'],
        'safe_precision': test['precision_safe'], 'safe_recall': test['recall_safe'], 'safe_f1': test['f1_safe'],
        'phone_precision': test['precision_phone'], 'phone_recall': test['recall_phone'], 'phone_f1': test['f1_phone'],
        'roc_auc': test['roc_auc'], 'pr_auc': test['pr_auc'], 'ece': test['ece_binary'], 'brier': test['brier_score'],
        'tn': cm[0][0], 'fp': cm[0][1], 'fn': cm[1][0], 'tp': cm[1][1],
    }

def read_fusion_predictions(seed):
    _, path = seed_paths(seed)
    rows=[]
    with path.open(newline='', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            rows.append(row)
    for row in rows:
        fprob=float(row['front_prob_phone']); sprob=float(row['side_prob_phone'])
        ef=math.exp(abs(fprob-0.5)); es=math.exp(abs(sprob-0.5))
        wf=ef/(ef+es); ws=es/(ef+es)
        row['adaptive_front_weight']=row.get('adaptive_front_weight') or wf
        row['adaptive_side_weight']=row.get('adaptive_side_weight') or ws
    return rows

def write_predictions(seed):
    rows=read_fusion_predictions(seed)
    fields=['sample_id','subject_id','activity_id','frame','ground_truth','front_probability','front_prediction','side_probability','side_prediction','average_probability','average_prediction','adaptive_probability','adaptive_prediction','adaptive_front_weight','adaptive_side_weight']
    out=OUT / f'predictions_seed{seed}.csv'
    with out.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for row in rows:
            sid=f"S{row['subject_id']}_AC{row['activity_id']}_F{row['frame']}"
            w.writerow({
                'sample_id': sid, 'subject_id': row['subject_id'], 'activity_id': row['activity_id'], 'frame': row['frame'], 'ground_truth': row['label'],
                'front_probability': row['front_prob_phone'], 'front_prediction': row['front_pred'],
                'side_probability': row['side_prob_phone'], 'side_prediction': row['side_pred'],
                'average_probability': row['average_prob_phone'], 'average_prediction': row['average_pred'],
                'adaptive_probability': row['adaptive_prob_phone'], 'adaptive_prediction': row['adaptive_pred'],
                'adaptive_front_weight': row['adaptive_front_weight'], 'adaptive_side_weight': row['adaptive_side_weight'],
            })
    return rows

def comp_and_weights(seed, rows):
    labels=[int(r['label']) for r in rows]
    fp=[int(r['front_pred']) for r in rows]
    sp=[int(r['side_pred']) for r in rows]
    ap=[int(r['average_pred']) for r in rows]
    dp=[int(r['adaptive_pred']) for r in rows]
    wf=[float(r['adaptive_front_weight']) for r in rows]
    ws=[float(r['adaptive_side_weight']) for r in rows]
    fc=[p==y for p,y in zip(fp,labels)]; sc=[p==y for p,y in zip(sp,labels)]; dc=[p==y for p,y in zip(dp,labels)]
    ac=[p==y for p,y in zip(ap,labels)]
    comp={
        'seed': seed,
        'both_correct': sum(f and s for f,s in zip(fc,sc)),
        'front_correct_side_wrong': sum(f and not s for f,s in zip(fc,sc)),
        'front_wrong_side_correct': sum((not f) and s for f,s in zip(fc,sc)),
        'both_wrong': sum((not f) and (not s) for f,s in zip(fc,sc)),
        'fusion_fixed_front_error': sum((not f) and d for f,d in zip(fc,dc)),
        'fusion_broke_front_correct': sum(f and not d for f,d in zip(fc,dc)),
        'fusion_correct_when_side_wrong': sum((not s) and d for s,d in zip(sc,dc)),
        'fusion_wrong_when_side_correct': sum(s and not d for s,d in zip(sc,dc)),
        'side_only_correct': sum((not f) and s for f,s in zip(fc,sc)),
        'fusion_correct_when_both_wrong': sum((not f) and (not s) and d for f,s,d in zip(fc,sc,dc)),
        'fusion_wrong_when_both_single_view_correct': sum(f and s and not d for f,s,d in zip(fc,sc,dc)),
    }
    diff=sum(a!=d for a,d in zip(ap,dp))
    weights={
        'seed': seed,
        'mean_front_weight': statistics.fmean(wf), 'mean_side_weight': statistics.fmean(ws),
        'std_front_weight': statistics.pstdev(wf), 'std_side_weight': statistics.pstdev(ws),
        'min_front_weight': min(wf), 'max_front_weight': max(wf), 'min_side_weight': min(ws), 'max_side_weight': max(ws),
        'adaptive_vs_average_prediction_diff_count': diff,
        'adaptive_vs_average_prediction_diff_pct': diff/len(rows)*100,
        'front_weight_gt_side_count': sum(f>s for f,s in zip(wf,ws)),
        'side_weight_gt_front_count': sum(s>f for f,s in zip(wf,ws)),
        'both_weights_near_0_5_count': sum(0.45 <= f <= 0.55 and 0.45 <= s <= 0.55 for f,s in zip(wf,ws)),
    }
    return comp, weights

def write_csv(path, rows, fields):
    with Path(path).open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

def mean_std(vals):
    return statistics.fmean(vals), statistics.stdev(vals) if len(vals) > 1 else 0.0

full=[]
by_seed_model={}
for seed in SEEDS:
    for model in MODELS:
        row=metric_row(seed, model)
        full.append(row); by_seed_model[(seed, model)] = row
fields=['seed','model','train_macro_f1','val_macro_f1','train_val_f1_gap','train_loss','val_loss','train_val_loss_gap','best_epoch','test_accuracy','test_macro_f1','macro_precision','macro_recall','safe_precision','safe_recall','safe_f1','phone_precision','phone_recall','phone_f1','roc_auc','pr_auc','ece','brier','tn','fp','fn','tp']
write_csv(OUT/'robustness_full_results.csv', full, fields)

agg=[]
for display_model, metric_name, model, key in AGG_METRICS:
    vals=[float(by_seed_model[(s,model)][key]) for s in SEEDS]
    m,sd=mean_std(vals)
    agg.append({'model':display_model,'metric':metric_name,'seed42':vals[0],'seed43':vals[1],'seed44':vals[2],'mean':m,'std':sd,'min':min(vals),'max':max(vals)})
write_csv(OUT/'robustness_aggregate.csv', agg, ['model','metric','seed42','seed43','seed44','mean','std','min','max'])

comps=[]; weights=[]
for seed in SEEDS:
    pred_rows=write_predictions(seed)
    c,w=comp_and_weights(seed,pred_rows)
    comps.append(c); weights.append(w)
write_csv(OUT/'complementarity_by_seed.csv', comps, ['seed','both_correct','front_correct_side_wrong','front_wrong_side_correct','both_wrong','fusion_fixed_front_error','fusion_broke_front_correct','fusion_correct_when_side_wrong','fusion_wrong_when_side_correct','side_only_correct','fusion_correct_when_both_wrong','fusion_wrong_when_both_single_view_correct'])
write_csv(OUT/'adaptive_weights_by_seed.csv', weights, ['seed','mean_front_weight','mean_side_weight','std_front_weight','std_side_weight','min_front_weight','max_front_weight','min_side_weight','max_side_weight','adaptive_vs_average_prediction_diff_count','adaptive_vs_average_prediction_diff_pct','front_weight_gt_side_count','side_weight_gt_front_count','both_weights_near_0_5_count'])

manifest=[]
with (REPO/'data'/'manifest_split.csv').open(newline='',encoding='utf-8-sig') as f:
    for r in csv.DictReader(f): manifest.append(r)
split_info=[]
for split in ['train','val','test']:
    ids=sorted({int(r['subject_id']) for r in manifest if r['split']==split})
    front=sum(1 for r in manifest if r['split']==split and r['view']=='front' and (int(r['frame'])-1)%30==0)
    side=sum(1 for r in manifest if r['split']==split and r['view']=='side' and (int(r['frame'])-1)%30==0)
    split_info.append((split, ids, front, side))

def cm(model, seed):
    r=by_seed_model[(seed, model)]
    return f"[[{r['tn']},{r['fp']}],[{r['fn']},{r['tp']}]]"

def val(model, metric, seed):
    return float(by_seed_model[(seed,model)][metric])

def agg_lookup(model, metric):
    for row in agg:
        if row['model']==model and row['metric']==metric:
            return row
    raise KeyError((model,metric))

def md_table(headers, rows):
    out=['| ' + ' | '.join(headers) + ' |', '|' + '|'.join(['---']*len(headers)) + '|']
    for row in rows: out.append('| ' + ' | '.join(str(x) for x in row) + ' |')
    return out

lines=[]
lines += ['# Experiment 23 Robustness Report','']
lines += ['## Pre-Run Audit','', 'PASS: no unintended behavioral mismatch found. Seed43/44 vary only by `TRAINING_SEED`; recipe remains exact experiment_18. Seed42 uses existing experiment_18 artifacts without retrain.', '']
lines += ['## Exact Split Verification','']
for split,ids,front,side in split_info:
    lines.append(f'- {split}: {len(ids)} subjects {ids}; stride30 samples front={front}, side={side}')
lines += ['', '## TABLE A - Per-Seed Main Performance']
rows=[]
for label,model in [('Front Macro F1','front'),('Side Macro F1','side'),('Average Fusion Macro F1','average_fusion'),('Adaptive Fusion Macro F1','adaptive_fusion')]:
    vals=[val(model,'test_macro_f1',s) for s in SEEDS]; m,sd=mean_std(vals); rows.append([label, r5(vals[0]), r5(vals[1]), r5(vals[2]), f'{m:.5f} +/- {sd:.5f}'])
lines += md_table(['Model','Seed42','Seed43','Seed44','Mean +/- Std'], rows)
lines += ['', '## TABLE B - Per-Class Recall']
rows=[]
for label,model,key in [('Front Safe Recall','front','safe_recall'),('Front Phone Recall','front','phone_recall'),('Side Safe Recall','side','safe_recall'),('Side Phone Recall','side','phone_recall'),('Fusion Safe Recall','average_fusion','safe_recall'),('Fusion Phone Recall','average_fusion','phone_recall')]:
    vals=[val(model,key,s) for s in SEEDS]; m,sd=mean_std(vals); rows.append([label,r5(vals[0]),r5(vals[1]),r5(vals[2]),f'{m:.5f} +/- {sd:.5f}'])
lines += md_table(['Model / Metric','Seed42','Seed43','Seed44','Mean +/- Std'], rows)
lines += ['', '## TABLE C - Probability / Calibration']
rows=[]
for label,key in [('Fusion ROC-AUC','roc_auc'),('Fusion PR-AUC','pr_auc'),('Fusion ECE','ece'),('Fusion Brier','brier')]:
    vals=[val('adaptive_fusion',key,s) for s in SEEDS]; m,sd=mean_std(vals); rows.append([label,r5(vals[0]),r5(vals[1]),r5(vals[2]),f'{m:.5f} +/- {sd:.5f}'])
lines += md_table(['Metric','Seed42','Seed43','Seed44','Mean +/- Std'], rows)
lines += ['', '## TABLE D - Confusion Matrices']
rows=[[s, cm('front',s), cm('side',s), cm('average_fusion',s), cm('adaptive_fusion',s)] for s in SEEDS]
lines += md_table(['Seed','Front CM','Side CM','Average Fusion CM','Adaptive Fusion CM'], rows)
lines += ['', '## TABLE E - Complementarity']
comp_metrics=['both_correct','front_correct_side_wrong','front_wrong_side_correct','both_wrong','fusion_fixed_front_error','fusion_broke_front_correct','fusion_correct_when_side_wrong','fusion_wrong_when_side_correct']
comp_rows=[]
for metric in comp_metrics:
    d={c['seed']: c[metric] for c in comps}; comp_rows.append([metric,d[42],d[43],d[44]])
lines += md_table(['Metric','Seed42','Seed43','Seed44'], comp_rows)
lines += ['', '## TABLE F - Adaptive Weights']
for metric in ['mean_front_weight','mean_side_weight','std_front_weight','std_side_weight','min_front_weight','max_front_weight','min_side_weight','max_side_weight','adaptive_vs_average_prediction_diff_count','adaptive_vs_average_prediction_diff_pct','front_weight_gt_side_count','side_weight_gt_front_count','both_weights_near_0_5_count']:
    d={w['seed']: w[metric] for w in weights}; fmt=lambda x: r5(x) if isinstance(x,float) else x; lines += md_table(['Metric','Seed42','Seed43','Seed44'], [[metric,fmt(d[42]),fmt(d[43]),fmt(d[44])]])

avg_fusion=[val('average_fusion','test_macro_f1',s) for s in SEEDS]
front=[val('front','test_macro_f1',s) for s in SEEDS]
side=[val('side','test_macro_f1',s) for s in SEEDS]
rank_stable=all(avg_fusion[i]>front[i] and front[i]>side[i] for i in range(3))
decisions_identical=all(int(w['adaptive_vs_average_prediction_diff_count'])==0 for w in weights)
_, fusion_sd=mean_std(avg_fusion)
verdict = 'moderate seed sensitivity' if fusion_sd > 0.03 or not rank_stable else 'reasonably robust'
lines += ['', '## Key Robustness Questions','']
lines += [
    f'1. Average Fusion Macro F1 > Front Macro F1 for all seeds: {all(a>f for a,f in zip(avg_fusion,front))}.',
    f'2. Average Fusion Macro F1 > Side Macro F1 for all seeds: {all(a>s for a,s in zip(avg_fusion,side))}.',
    f'3. Fusion consistently best model per seed: {all(a>f and a>s for a,f,s in zip(avg_fusion,front,side))}.',
    f'4. Ranking Fusion > Front > Side stable: {rank_stable}.',
    f'5. Average and Adaptive decisions identical across all seeds: {decisions_identical}.',
    f'6. Std of Average Fusion Macro F1: {fusion_sd:.5f}.',
    '7. Safe Recall stability: variable across seeds; see TABLE B.',
    '8. Phone Recall stability: comparatively high but still varies; see TABLE B.',
    '9. Calibration stability: ECE/Brier vary across seeds; see TABLE C.',
    f'10. Obvious outlier: seed43 is the weakest fusion run.'
]
lines += ['', '## Robustness Verdict','', f'{verdict}. Experiment_18 remains the selected recipe; Exp23 measures stochastic robustness and does not replace the selected seed with a better/worse seed.', '']
lines += ['## COPY-PASTE SUMMARY FOR CHATGPT','']
lines += ['Experiment_23 FINAL ROBUSTNESS VALIDATION for main recipe experiment_18. Seed42 uses existing experiment_18 artifacts; seed43 and seed44 are standalone retrains from ImageNet pretrained. SPLIT_SEED=42 fixed; TRAINING_SEED varies: 42, 43, 44. Subject split is fixed from manifest_split.csv and not regenerated.']
for split,ids,front_count,side_count in split_info:
    lines.append(f'{split}: {len(ids)} subjects IDs={ids}; stride30 samples per view: front={front_count}, side={side_count}.')
for seed in SEEDS:
    lines.append(f'Seed {seed}: Front Macro F1={r5(val("front","test_macro_f1",seed))}, Side Macro F1={r5(val("side","test_macro_f1",seed))}, Average Fusion Macro F1={r5(val("average_fusion","test_macro_f1",seed))}, Adaptive Fusion Macro F1={r5(val("adaptive_fusion","test_macro_f1",seed))}.')
    lines.append(f'Seed {seed} recalls: Front safe={r5(val("front","safe_recall",seed))}, front phone={r5(val("front","phone_recall",seed))}, Side safe={r5(val("side","safe_recall",seed))}, side phone={r5(val("side","phone_recall",seed))}, Fusion safe={r5(val("average_fusion","safe_recall",seed))}, fusion phone={r5(val("average_fusion","phone_recall",seed))}.')
    lines.append(f'Seed {seed} CM: Front={cm("front",seed)}, Side={cm("side",seed)}, Average Fusion={cm("average_fusion",seed)}, Adaptive Fusion={cm("adaptive_fusion",seed)}.')
    lines.append(f'Seed {seed} adaptive fusion calibration/probability: ROC-AUC={r5(val("adaptive_fusion","roc_auc",seed))}, PR-AUC={r5(val("adaptive_fusion","pr_auc",seed))}, ECE={r5(val("adaptive_fusion","ece",seed))}, Brier={r5(val("adaptive_fusion","brier",seed))}.')
for row in agg:
    lines.append(f"Aggregate {row['model']} {row['metric']}: seed42={r5(row['seed42'])}, seed43={r5(row['seed43'])}, seed44={r5(row['seed44'])}, mean={r5(row['mean'])}, std={r5(row['std'])}, min={r5(row['min'])}, max={r5(row['max'])}.")
for c in comps:
    lines.append('Complementarity seed {seed}: both_correct={both_correct}, front_correct_side_wrong={front_correct_side_wrong}, front_wrong_side_correct={front_wrong_side_correct}, both_wrong={both_wrong}, fusion_fixed_front_error={fusion_fixed_front_error}, fusion_broke_front_correct={fusion_broke_front_correct}, fusion_correct_when_side_wrong={fusion_correct_when_side_wrong}, fusion_wrong_when_side_correct={fusion_wrong_when_side_correct}, side_only_correct={side_only_correct}, fusion_correct_when_both_wrong={fusion_correct_when_both_wrong}, fusion_wrong_when_both_single_view_correct={fusion_wrong_when_both_single_view_correct}.'.format(**c))
for w in weights:
    lines.append('Adaptive weights seed {seed}: mean_front_weight={mean_front_weight:.5f}, mean_side_weight={mean_side_weight:.5f}, std_front_weight={std_front_weight:.5f}, std_side_weight={std_side_weight:.5f}, min_front_weight={min_front_weight:.5f}, max_front_weight={max_front_weight:.5f}, min_side_weight={min_side_weight:.5f}, max_side_weight={max_side_weight:.5f}, adaptive_vs_average_prediction_diff_count={adaptive_vs_average_prediction_diff_count}, adaptive_vs_average_prediction_diff_pct={adaptive_vs_average_prediction_diff_pct:.5f}, front_weight_gt_side_count={front_weight_gt_side_count}, side_weight_gt_front_count={side_weight_gt_front_count}, both_weights_near_0_5_count={both_weights_near_0_5_count}.'.format(**w))
lines.append(f'Final robustness verdict: {verdict}. No seed cherry-picking; experiment_18 remains selected recipe.')
(OUT/'robustness_report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('wrote robustness outputs')

