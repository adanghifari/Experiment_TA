
import json, statistics, hashlib
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(r"D:\Skripsi\Experiment_TA")
OUT = ROOT / "paper_audit"
FIG = OUT / "figures" / "model_health"
FIG.mkdir(parents=True, exist_ok=True)

def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8-sig"))

def sha256(p):
    h = hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()

def fmt(x, n=5):
    return "N/A" if x is None else f"{float(x):.{n}f}"

def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    out += ["| " + " | ".join(str(x) for x in r) + " |" for r in rows]
    return "\n".join(out)

def getrow(rows, epoch):
    return next(r for r in rows if r["epoch"] == epoch)

specs = [
("front_original","Front original","Original experiment_18",ROOT/"experiment_18/results/front/history.json",ROOT/"experiment_18/results/front/train_summary.json",ROOT/"experiment_18/results/front/test_eval_metrics.json",ROOT/"experiment_18/checkpoints/front/best.pt","val_macro_f1","max","POSSIBLE OVERFITTING SIGNAL","Train loss turun terus setelah epoch 9, validation loss membaik sampai epoch 12 lalu naik pada epoch 13, dan loss gap naik dari 0.04383 pada checkpoint ke 0.13310 pada epoch terakhir."),
("front_std_val_loss","Front standardized val-loss","experiment_18_standardized_checkpoint_val_loss",ROOT/"experiment_18_standardized_checkpoint_val_loss/results/standardized_val_loss/front/history.json",ROOT/"experiment_18_standardized_checkpoint_val_loss/results/standardized_val_loss/front/train_summary.json",ROOT/"experiment_18_standardized_checkpoint_val_loss/results/standardized_val_loss/front/test_eval_metrics.json",ROOT/"experiment_18_standardized_checkpoint_val_loss/checkpoints/standardized_val_loss/front/best.pt","val_loss","min","POSSIBLE OVERFITTING SIGNAL","Validation loss minimum pada epoch 12; sesudahnya naik, train loss tetap turun, dan loss gap mencapai 0.13310 pada epoch terakhir."),
("side_original","Side original","Original experiment_18",ROOT/"experiment_18/results/side/history.json",ROOT/"experiment_18/results/side/train_summary.json",ROOT/"experiment_18/results/side/test_eval_metrics.json",ROOT/"experiment_18/checkpoints/side/best.pt","val_loss","min","NO CLEAR OVERFITTING SIGNAL","Validation loss membaik sampai epoch 26 lalu hanya berosilasi pada sisa epoch; gap positif besar dicatat sebagai fakta, bukan diagnosis tunggal."),
("side_std_val_loss","Side standardized val-loss","experiment_18_standardized_checkpoint_val_loss",ROOT/"experiment_18_standardized_checkpoint_val_loss/results/standardized_val_loss/side/history.json",ROOT/"experiment_18_standardized_checkpoint_val_loss/results/standardized_val_loss/side/train_summary.json",ROOT/"experiment_18_standardized_checkpoint_val_loss/results/standardized_val_loss/side/test_eval_metrics.json",ROOT/"experiment_18_standardized_checkpoint_val_loss/checkpoints/standardized_val_loss/side/best.pt","val_loss","min","NO CLEAR OVERFITTING SIGNAL","History dan checkpoint sama dengan Side original pada epoch 26; validation loss membaik sampai checkpoint dan hanya berosilasi sesudahnya."),
("front_std_f1","Front standardized Macro-F1","experiment_18_standardized_checkpoint_selection",ROOT/"experiment_18_standardized_checkpoint_selection/results/front/history.json",ROOT/"experiment_18_standardized_checkpoint_selection/results/front/train_summary.json",ROOT/"experiment_18_standardized_checkpoint_selection/results/front/test_eval_metrics.json",ROOT/"experiment_18_standardized_checkpoint_selection/checkpoints/front/best.pt","val_macro_f1","max","POSSIBLE OVERFITTING SIGNAL","Validation Macro F1 maksimum pada epoch 9, validation loss minimum pada epoch 12, dan loss gap meningkat dari 0.04383 menjadi 0.13310 pada epoch 13."),
 ("side_std_f1","Side standardized Macro-F1","experiment_18_standardized_checkpoint_selection",ROOT/"experiment_18_standardized_checkpoint_selection/results/side/history.json",ROOT/"experiment_18_standardized_checkpoint_selection/results/side/train_summary.json",ROOT/"experiment_18_standardized_checkpoint_selection/results/side/test_eval_metrics.json",ROOT/"experiment_18_standardized_checkpoint_selection/checkpoints/side/best.pt","val_macro_f1","max","POSSIBLE OVERFITTING SIGNAL","Validation Macro F1 maksimum pada epoch 15, tetapi validation loss membaik hingga epoch 20 dan loss gap meningkat dari 0.05490 menjadi 0.08578."),
]

runs=[]
for sid,label,protocol,hpath,spath,tpath,cpath,criterion,mode,health,basis in specs:
    hist=load(hpath); summary=load(spath); test=load(tpath) if tpath else {}
    selected=int(summary["best_epoch"]); best=None; rows=[]
    for original in hist:
        r=dict(original); r["loss_gap"]=float(r["val_loss"])-float(r["train_loss"]); r["abs_loss_gap"]=abs(r["loss_gap"])
        score=float(r[criterion]); improved=(best is None or (score>best if mode=="max" else score<best))
        if improved: best=score
        r["checkpoint_improvement"]=improved; r["selected_checkpoint"]=int(r["epoch"])==selected; rows.append(r)
    sr=getrow(rows,selected); fl=min(rows,key=lambda r:r["val_loss"]); mf=max(rows,key=lambda r:r["val_macro_f1"]); ma=min(rows,key=lambda r:r["abs_loss_gap"]); mg=max(rows,key=lambda r:r["loss_gap"]); last=rows[-1]
    stats={"mean":statistics.mean(r["loss_gap"] for r in rows),"median":statistics.median(r["loss_gap"] for r in rows),"min":min(r["loss_gap"] for r in rows),"max":max(r["loss_gap"] for r in rows),"mean_abs":statistics.mean(r["abs_loss_gap"] for r in rows),"final":last["loss_gap"],"first05":next((r["epoch"] for r in rows if r["loss_gap"]>0.05),None),"first10":next((r["epoch"] for r in rows if r["loss_gap"]>0.10),None)}
    digest=sha256(cpath)
    runs.append({"id":sid,"label":label,"protocol":protocol,"history":rows,"summary":summary,"test":test,"criterion":criterion,"mode":mode,"selected":selected,"selected_row":sr,"min_loss":fl,"max_f1":mf,"min_abs":ma,"max_gap":mg,"last":last,"stats":stats,"f1_gap":None if sr.get("train_macro_f1") is None else float(sr["train_macro_f1"])-float(sr["val_macro_f1"]),"health":health,"basis":basis,"hash":digest,"hash_match":digest.lower()==str(summary.get("checkpoint_sha256","")).lower()})

for run in runs:
    rows=run["history"]; x=[r["epoch"] for r in rows]; e=run["selected"]
    fig,ax=plt.subplots(figsize=(8,4.5)); ax.plot(x,[r["train_loss"] for r in rows],marker="o",label="train loss"); ax.plot(x,[r["val_loss"] for r in rows],marker="o",label="validation loss"); ax.axvline(e,color="black",linestyle="--",label=f"selected epoch {e}"); ax.set_title(run["label"]+" loss trajectory"); ax.set_xlabel("Epoch"); ax.set_ylabel("Loss"); ax.grid(alpha=.25); ax.legend(); fig.tight_layout(); fig.savefig(FIG/(run["id"]+"_loss.png"),dpi=180); plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4.5)); ax.plot(x,[r["loss_gap"] for r in rows],marker="o",label="validation loss - train loss"); ax.axhline(0,color="gray"); ax.axvline(e,color="black",linestyle="--",label=f"selected epoch {e}"); ax.set_title(run["label"]+" loss-gap trajectory"); ax.set_xlabel("Epoch"); ax.set_ylabel("Loss gap"); ax.grid(alpha=.25); ax.legend(); fig.tight_layout(); fig.savefig(FIG/(run["id"]+"_loss_gap.png"),dpi=180); plt.close(fig)

def full_table(run):
    data=[]
    for r in run["history"]:
        data.append([r["epoch"],fmt(r["train_loss"]),fmt(r["val_loss"]),fmt(r["loss_gap"]),fmt(r["abs_loss_gap"]),fmt(r["val_macro_f1"]),fmt(r.get("train_macro_f1")),fmt(r["learning_rate"],8),"YES" if r["checkpoint_improvement"] else "NO","YES" if r["selected_checkpoint"] else "NO"])
    return md_table(["epoch","train_loss","val_loss","loss_gap","abs_loss_gap","val_macro_f1","train_macro_f1","learning_rate","checkpoint_improvement","selected_checkpoint"],data)

def window(run):
    lo=max(1,run["selected"]-3); hi=min(run["history"][-1]["epoch"],run["selected"]+3)
    data=[[r["epoch"],fmt(r["train_loss"]),fmt(r["val_loss"]),fmt(r["loss_gap"]),fmt(r["val_macro_f1"]),fmt(r["learning_rate"],8)] for r in run["history"] if lo<=r["epoch"]<=hi]
    return md_table(["epoch","train_loss","val_loss","loss_gap","val_macro_f1","learning_rate"],data)

def health(run):
    s=run["stats"]; r=run["history"]
    return "\n".join(["Assessment: **"+run["health"]+"**.",run["basis"],f"Selected epoch {run['selected']} by {run['criterion']}/{run['mode']}; executed epochs {len(r)}.",f"Minimum validation loss: epoch {run['min_loss']['epoch']} ({fmt(run['min_loss']['val_loss'])}); maximum validation Macro F1: epoch {run['max_f1']['epoch']} ({fmt(run['max_f1']['val_macro_f1'])}); minimum absolute gap: epoch {run['min_abs']['epoch']} ({fmt(run['min_abs']['abs_loss_gap'])}); maximum gap: epoch {run['max_gap']['epoch']} ({fmt(run['max_gap']['loss_gap'])}); final epoch {run['last']['epoch']}.",f"Gap statistics: mean {fmt(s['mean'])}, median {fmt(s['median'])}, min {fmt(s['min'])}, max {fmt(s['max'])}, mean absolute {fmt(s['mean_abs'])}, final {fmt(s['final'])}; first >0.05: {s['first05'] if s['first05'] is not None else 'never'}; first >0.10: {s['first10'] if s['first10'] is not None else 'never'}.",f"Trajectory: train loss start/selected/end = {fmt(r[0]['train_loss'])}/{fmt(run['selected_row']['train_loss'])}/{fmt(run['last']['train_loss'])}; validation loss start/minimum/selected/end = {fmt(r[0]['val_loss'])}/{fmt(run['min_loss']['val_loss'])}/{fmt(run['selected_row']['val_loss'])}/{fmt(run['last']['val_loss'])}; validation Macro F1 start/maximum/selected/end = {fmt(r[0]['val_macro_f1'])}/{fmt(run['max_f1']['val_macro_f1'])}/{fmt(run['selected_row']['val_macro_f1'])}/{fmt(run['last']['val_macro_f1'])}; gap start/selected/end = {fmt(r[0]['loss_gap'])}/{fmt(run['selected_row']['loss_gap'])}/{fmt(run['last']['loss_gap'])}.","","Local checkpoint window:",window(run),"",f"Figures: [loss](figures/model_health/{run['id']}_loss.png), [loss-gap](figures/model_health/{run['id']}_loss_gap.png)."])

summary=[]
for run in runs:
    r=run["selected_row"]; summary.append([run["label"],run["criterion"]+"/"+run["mode"],run["selected"],fmt(r["train_loss"]),fmt(r["val_loss"]),fmt(r["loss_gap"]),fmt(r["val_macro_f1"]),fmt(r.get("train_macro_f1")),fmt(run["f1_gap"]),fmt(run["test"].get("f1_macro")),run["health"]])

report=[]
report += ["# Checkpoint and model-health audit\n","## 1. Scope\n","Read-only audit of artifacts under D:\\Skripsi\\Experiment_TA. The historical repository D:\\Skripsi\\Experiment was not accessed. No retraining, new inference, source modification, checkpoint modification, paper modification, overwrite, or Git commit was performed. Only existing histories, summaries, metadata, checkpoint files, and test metric artifacts were read; this report and audit figures were created.\n"]
report += ["## 2. Artifact verification\n",md_table(["run","protocol","criterion","selected epoch","hash matches summary","checkpoint SHA-256"],[[r["label"],r["protocol"],r["criterion"]+"/"+r["mode"],r["selected"],"YES" if r["hash_match"] else "NO",r["hash"]] for r in runs]),"\nThe full two-view standardized-Macro-F1 candidate is experiment_18_standardized_checkpoint_selection. Its resolved config, Front/Side histories, train summaries, test metric artifacts, physical checkpoints, and matching SHA-256 values are present. The Side-only archive candidate was not needed for the primary comparison.\n"]
report += ["## 3. Metric definitions\n","loss_gap = val_loss - train_loss at the same epoch. abs_loss_gap = absolute value of loss_gap. checkpoint_improvement is reconstructed from history using strict max/min direction. train_macro_f1 is used only because it is already stored in history; no train-set inference was run. Test Macro F1 is an independent outcome and is not used as model-health evidence.\n"]
for title,index in [("## 4. Front original health",0),("## 5. Front standardized-val-loss health",1),("## 6. Side original health",2),("## 7. Side Macro-F1 candidate health",5),("## 8. Front standardized-Macro-F1 reference",4)]:
    report += [title+"\n",health(runs[index])+"\n","Complete per-epoch health table:\n\n",full_table(runs[index])+"\n"]
report += ["## 9. Loss-gap comparison\n",md_table(["run","selected gap","selected abs gap","mean gap","median gap","min gap","max gap","mean abs gap","final gap","first >0.05","first >0.10"],[[r["label"],fmt(r["selected_row"]["loss_gap"]),fmt(r["selected_row"]["abs_loss_gap"]),fmt(r["stats"]["mean"]),fmt(r["stats"]["median"]),fmt(r["stats"]["min"]),fmt(r["stats"]["max"]),fmt(r["stats"]["mean_abs"]),fmt(r["stats"]["final"]),r["stats"]["first05"] if r["stats"]["first05"] is not None else "never",r["stats"]["first10"] if r["stats"]["first10"] is not None else "never"] for r in runs]),"\nA positive loss gap is a recorded train/validation relationship; it is not by itself an overfitting diagnosis.\n"]
report += ["## 10. Checkpoint-window comparison\n","The local windows are reported in each run section. Front Macro-F1 selection is epoch 9 and Front val-loss selection is epoch 12. Side Macro-F1 selection is epoch 15 and Side val-loss selection is epoch 26. These are descriptive positions in the recorded trajectories, not causal explanations.\n"]
report += ["## 11. Overfit/underfit assessment\n","Front runs receive POSSIBLE OVERFITTING SIGNAL because train loss continues falling while late validation loss/gap deteriorates. Side val-loss runs receive NO CLEAR OVERFITTING SIGNAL because validation loss reaches its minimum late and then oscillates over the remaining epochs, although their positive gaps are relatively large. Side Macro-F1 selection receives POSSIBLE OVERFITTING SIGNAL because selection precedes later validation-loss improvement and the gap increases afterward. No run is labeled STRONG OVERFITTING SIGNAL or POSSIBLE UNDERFITTING SIGNAL from these artifacts.\n"]
report += ["## 12. Original vs standardized comparison\n### Front\n","Under the recorded runs, original and standardized-Macro-F1 Front select epoch 9 with validation Macro F1 0.72581 and loss gap 0.04383. Standardized-val-loss Front selects epoch 12 with validation loss 0.50961, validation Macro F1 0.71892, and loss gap 0.09239. The latter has lower validation loss by its criterion and a larger selected gap; this does not establish superiority.\n### Side\n","Original and standardized-val-loss Side select epoch 26 with validation loss 0.50217, validation Macro F1 0.68238, and loss gap 0.10738. Verified standardized-Macro-F1 Side selects epoch 15 with validation Macro F1 0.75724, validation loss 0.53991, and loss gap 0.05490. This is a descriptive comparison across recorded runs, not a causal claim.\n"]
report += ["## 13. Training-health vs test-outcome distinction\n","Test Macro F1 may be listed in the summary table as an outcome, but it is not used to claim that a model is healthy, not overfit, more generalizable, or that one criterion is better.\n","Summary table:\n\n",md_table(["model/run","criterion","selected epoch","train loss","val loss","loss gap","val Macro F1","train Macro F1","F1 gap","test Macro F1","health assessment"],summary),"\n"]
report += ["## 14. FACT\n","Original Front selected epoch 9 by validation Macro F1; original Side selected epoch 26 by validation loss. Standardized-val-loss selected Front epoch 12 and Side epoch 26 by validation loss. Verified standardized-Macro-F1 selected Front epoch 9 and Side epoch 15 by validation Macro F1. Train Macro F1 is present in all audited histories. Front selected gap is 0.04383 for Macro-F1 selection versus 0.09239 for val-loss selection. Side selected gap is 0.10738 for val-loss selection versus 0.05490 for Macro-F1 selection. Original and standardized-val-loss Side histories and checkpoint hash match in the audited artifacts.\n"]
report += ["## 15. INTERPRETATION\n","The curves support a limited descriptive interpretation: criteria select different positions in the validation trajectory. Front Macro-F1 selection precedes the validation-loss minimum; Side Macro-F1 selection also precedes the later validation-loss minimum. Loss-gap evidence supports different observed view-specific checkpoint behavior only PARTIALLY: the selected positions and gaps differ, but artifacts do not establish causality, superiority, or historical rationale.\n"]
report += ["## 16. LIMITATIONS\n","These are recorded runs, not a new causal experiment. Loss gaps can reflect regularization, augmentation, class weighting, dropout, and train/validation construction. Test metrics are not health evidence. No new inference was run to fill missing metrics. The audit does not infer why a criterion was originally chosen.\n"]
report += ["## Required final summary\n"]
for run in [runs[0],runs[1],runs[2],runs[5]]:
    r=run["selected_row"]; report += [f"{run['label'].upper()}:\ncriterion: {run['criterion']}/{run['mode']}\nselected epoch: {run['selected']}\ntrain loss: {fmt(r['train_loss'])}\nval loss: {fmt(r['val_loss'])}\nloss gap: {fmt(r['loss_gap'])}\nval Macro F1: {fmt(r['val_macro_f1'])}\nhealth assessment: {run['health']}\n"]
report += ["SIDE MACRO-F1 CANDIDATE: AVAILABLE\n","FRONT HEALTH DIFFERENCE: Under the recorded runs, val-loss selection moves from epoch 9 to epoch 12, lowers validation loss from 0.51736 to 0.50961, and increases selected loss gap from 0.04383 to 0.09239; descriptive only.\n","SIDE HEALTH DIFFERENCE: Under the recorded runs, val-loss selection is later (epoch 26 vs epoch 15), has lower validation loss (0.50217 vs 0.53991), and a larger selected gap (0.10738 vs 0.05490).\n","DOES LOSS-GAP EVIDENCE SUPPORT DIFFERENT VIEW-SPECIFIC CHECKPOINT BEHAVIOR: PARTIALLY SUPPORTED\nreason: Recorded trajectories show different criterion-selected positions and selected gaps, but not causality or superiority.\n","FACT: Sections 2, 4-9, and 14 are computed from stored histories and metadata.\n","INTERPRETATION: Health categories are cautious interpretations of joint train/validation behavior, not causal explanations.\n","LIMITATIONS: No retraining, new inference, source modification, manuscript modification, or Git commit.\n"]
(OUT/"checkpoint_model_health_audit.md").write_text("\n".join(report),encoding="utf-8")
print("REPORT_WRITTEN",OUT/"checkpoint_model_health_audit.md")
print("FIGURES_WRITTEN",len(list(FIG.glob("*.png"))))
