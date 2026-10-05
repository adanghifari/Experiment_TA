import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIELDS = [
    'Experiment', 'Run Type', 'Stride', 'Seed Training',
    'Front Train Eval F1', 'Front Val Eval F1', 'Front F1 Gap', 'Front Test Macro F1', 'Front Best Epoch',
    'Side Train Eval F1', 'Side Val Eval F1', 'Side F1 Gap', 'Side Test Macro F1', 'Side Best Epoch',
    'Average Fusion Macro F1', 'Adaptive Fusion Macro F1', 'Safe Recall', 'Phone Recall',
    'Checkpoint Criterion Front', 'Checkpoint Criterion Side', 'Notes'
]

def load(path):
    path = Path(path)
    return json.loads(path.read_text(encoding='utf-8-sig')) if path.exists() else {}

def get(d, *keys):
    for key in keys:
        if not isinstance(d, dict):
            return None
        d = d.get(key)
    return d

def first_present(*values):
    for value in values:
        if value is not None:
            return value
    return None

def delta(a, b):
    if a is None or b is None:
        return None
    try:
        return round(float(a) - float(b), 5)
    except Exception:
        return None

rows = []
experiments = sorted(
    [p for p in ROOT.glob('experiment_*') if p.is_dir() and p.name.split('_')[-1].isdigit()],
    key=lambda p: int(p.name.split('_')[1])
)

for exp in experiments:
    resolved = load(exp / 'config' / 'resolved_config.json')
    front_summary = load(exp / 'results/front/train_summary.json')
    side_summary = load(exp / 'results/side/train_summary.json')
    front_train = load(exp / 'results/front/train_eval_metrics.json')
    front_val = load(exp / 'results/front/val_eval_metrics.json')
    front_test = load(exp / 'results/front/test_eval_metrics.json')
    side_train = load(exp / 'results/side/train_eval_metrics.json')
    side_val = load(exp / 'results/side/val_eval_metrics.json')
    side_test = load(exp / 'results/side/test_eval_metrics.json')
    fusion = load(exp / 'results/fusion/fusion_metrics.json')
    front_resolved = get(front_summary, 'resolved_config') or get(front_test, 'hyperparameters') or {}
    side_resolved = get(side_summary, 'resolved_config') or get(side_test, 'hyperparameters') or {}
    rows.append({
        'Experiment': exp.name,
        'Run Type': first_present(front_resolved.get('run_type'), side_resolved.get('run_type'), resolved.get('run_type'), 'experiment_run'),
        'Stride': first_present(front_resolved.get('frame_stride'), side_resolved.get('frame_stride'), resolved.get('frame_stride')),
        'Seed Training': first_present(front_resolved.get('seed_training'), side_resolved.get('seed_training'), resolved.get('seed_training')),
        'Front Train Eval F1': front_train.get('f1_macro'),
        'Front Val Eval F1': front_val.get('f1_macro'),
        'Front F1 Gap': delta(front_train.get('f1_macro'), front_val.get('f1_macro')),
        'Front Test Macro F1': front_test.get('f1_macro'),
        'Front Best Epoch': get(front_summary, 'best_epoch'),
        'Side Train Eval F1': side_train.get('f1_macro'),
        'Side Val Eval F1': side_val.get('f1_macro'),
        'Side F1 Gap': delta(side_train.get('f1_macro'), side_val.get('f1_macro')),
        'Side Test Macro F1': side_test.get('f1_macro'),
        'Side Best Epoch': get(side_summary, 'best_epoch'),
        'Average Fusion Macro F1': get(fusion, 'average_fusion', 'f1_macro'),
        'Adaptive Fusion Macro F1': get(fusion, 'adaptive_fusion', 'f1_macro'),
        'Safe Recall': get(fusion, 'average_fusion', 'recall_safe'),
        'Phone Recall': get(fusion, 'average_fusion', 'recall_phone'),
        'Checkpoint Criterion Front': get(front_summary, 'checkpoint_selection', 'monitored_metric'),
        'Checkpoint Criterion Side': get(side_summary, 'checkpoint_selection', 'monitored_metric'),
        'Notes': None,
    })

with (ROOT / 'master_experiment_summary.csv').open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)

(ROOT / 'master_experiment_summary.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
md = ['# Master Experiment Summary', '', '| ' + ' | '.join(FIELDS) + ' |', '|' + '|'.join(['---'] * len(FIELDS)) + '|']
for row in rows:
    md.append('| ' + ' | '.join(str(row.get(field, '') if row.get(field, '') is not None else '') for field in FIELDS) + ' |')
(ROOT / 'master_experiment_summary.md').write_text('\n'.join(md), encoding='utf-8')
print('Wrote master summaries')
