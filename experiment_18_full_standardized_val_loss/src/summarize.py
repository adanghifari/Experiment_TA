import argparse, json, logging, time
from pathlib import Path
import matplotlib.pyplot as plt
from src.metrics import env_metadata, sha256_file, write_json
from src.config import CHECKPOINT_DIR, RESULTS_DIR
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
log=logging.getLogger(__name__)

def load(path):
    path=Path(path); return json.loads(path.read_text(encoding='utf-8-sig')) if path.exists() else None

def plot_history(history_path, out_dir, prefix):
    h=load(history_path)
    if not h: return
    out_dir=Path(out_dir); out_dir.mkdir(parents=True,exist_ok=True); ep=[r['epoch'] for r in h]
    for fname,title,tr,va in [('loss_curve.png','Loss','train_loss','val_loss'),('macro_f1_curve.png','Macro F1','train_macro_f1','val_macro_f1'),('accuracy_curve.png','Accuracy','train_accuracy','val_accuracy')]:
        plt.figure(figsize=(7,4)); plt.plot(ep,[r[tr] for r in h],label=f'{prefix} train'); plt.plot(ep,[r[va] for r in h],label=f'{prefix} validation'); plt.xlabel('Epoch'); plt.ylabel(title); plt.title(f'{prefix} {title}'); plt.legend(); plt.tight_layout(); plt.savefig(out_dir/f'{prefix}_{fname}',dpi=160); plt.close()

def main():
    start=time.time()
    log.info('SUMMARY START | building figures and run metadata')
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); a=ap.parse_args(); root=Path(a.root).resolve(); results=RESULTS_DIR; cfg=root/'config'; fig=results/'figures'; ck=CHECKPOINT_DIR; protocol={}
    resolved=load(cfg/'resolved_config.json') or {}
    resolved.update({'run_type':resolved.get('run_type','controlled_variant'),'scenario':protocol.get('scenario'),})
    write_json(cfg/'resolved_config.json',resolved)
    plot_history(results/'front'/'history.json',fig,'front'); plot_history(results/'side'/'history.json',fig,'side')
    write_json(results/'run_metadata.json',{'environment':env_metadata(),'resolved_config_path':str(cfg/'resolved_config.json'),'front_checkpoint_sha256':sha256_file(ck/'front'/'best.pt'),'side_checkpoint_sha256':sha256_file(ck/'side'/'best.pt'),'run_type':resolved.get('run_type','controlled_variant')})
    front_sum=load(results/'front'/'train_summary.json'); side_sum=load(results/'side'/'train_summary.json'); write_json(results/'best_checkpoint_metadata.json',{'front':front_sum,'side':side_sum})
    ft=load(results/'front'/'test_eval_metrics.json') or load(results/'front'/'test_metrics.json') or {}; st=load(results/'side'/'test_eval_metrics.json') or load(results/'side'/'test_metrics.json') or {}; fu=load(results/'fusion'/'fusion_metrics.json') or {}
    write_json(results/'confusion_matrices.json',{'front':ft.get('confusion_matrix'),'side':st.get('confusion_matrix'),'average_fusion':(fu.get('average_fusion') or {}).get('confusion_matrix'),'adaptive_fusion':(fu.get('adaptive_fusion') or {}).get('confusion_matrix')})
    log.info('SUMMARY DONE | elapsed=%.2fs | metadata=%s | figures=%s', time.time()-start, results/'run_metadata.json', fig)
if __name__=='__main__': main()






