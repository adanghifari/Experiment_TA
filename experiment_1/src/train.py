import argparse, csv, json, logging, os, random, time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from src.config import *
from src.dataset import get_all_dataloaders
from src.metrics import env_metadata, sha256_file, write_json
from src.model import build_model

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


def seed_everything(seed=42):
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def metrics(labels, preds):
    return {
        "accuracy": accuracy_score(labels, preds),
        "macro_f1": f1_score(labels, preds, average="macro", zero_division=0),
        "precision_macro": precision_score(labels, preds, average="macro", zero_division=0),
        "recall_macro": recall_score(labels, preds, average="macro", zero_division=0),
    }


def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train(); loss_sum=0.0; n=0; labels_all=[]; preds_all=[]
    for images, labels in loader:
        images=images.to(device); y=labels.float().to(device)
        optimizer.zero_grad(); logits=model(images); loss=criterion(logits,y); loss.backward(); optimizer.step()
        probs=torch.sigmoid(logits).detach().cpu(); preds=(probs>=DECISION_THRESHOLD).long().tolist()
        labels_all.extend(labels.tolist()); preds_all.extend(preds); loss_sum+=loss.item()*images.size(0); n+=images.size(0)
    return loss_sum/n, metrics(labels_all,preds_all)

@torch.no_grad()
def validate(model, loader, criterion, device):
    model.eval(); loss_sum=0.0; n=0; labels_all=[]; preds_all=[]
    for images, labels in loader:
        images=images.to(device); y=labels.float().to(device); logits=model(images); loss=criterion(logits,y)
        probs=torch.sigmoid(logits).cpu(); preds=(probs>=DECISION_THRESHOLD).long().tolist()
        labels_all.extend(labels.tolist()); preds_all.extend(preds); loss_sum+=loss.item()*images.size(0); n+=images.size(0)
    return loss_sum/n, metrics(labels_all,preds_all)

class EarlyStopping:
    def __init__(self, patience):
        self.patience=patience; self.best=-1.0; self.counter=0; self.should_stop=False
    def step(self, score):
        if score > self.best:
            self.best=score; self.counter=0; return True
        self.counter+=1; self.should_stop=self.counter>=self.patience; return False


def abspath(path):
    p=Path(path); return p if p.is_absolute() else Path.cwd()/p


def write_history(rows, path):
    path=abspath(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(rows,indent=2),encoding="utf-8")
    with path.with_suffix(".csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)


def run_training(view, max_epochs=MAX_EPOCHS, exp_id="", lr=None, experiment="", class_weight_gamma=None, checkpoint_path=None, history_path=None, summary_path=None, frame_stride=FRAME_STRIDE, checkpoint_monitor=None):
    if SEED_TRAINING:
        seed_everything(SPLIT_SEED)
    lr = lr if lr is not None else (LEARNING_RATE_FRONT if view == "front" else LEARNING_RATE_SIDE)
    dropout = DROPOUT_FRONT if view == "front" else DROPOUT_SIDE
    patience = EARLY_STOPPING_PATIENCE_FRONT if view == "front" else EARLY_STOPPING_PATIENCE_SIDE
    device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
    log.info("")
    log.info("=============================================")
    log.info("Experiment Configuration")
    log.info("=============================================")
    log.info("  Experiment     : %s", EXPERIMENT_NAME)
    log.info("  View           : %s", view)
    log.info("  Optimizer      : Adam")
    log.info("  Learning Rate  : %.1e", lr)
    log.info("  Weight Decay   : %.1e", 0.0)
    log.info("  Scheduler      : None")
    log.info("  Dropout        : %s", dropout)
    log.info("  Frozen Stages  : %s", 0)
    log.info("  EarlyStopping  : patience=%s", patience)
    log.info("  Loss           : BCEWithLogitsLoss")
    log.info("  Seed           : %s", SPLIT_SEED if SEED_TRAINING else None)
    log.info("=============================================")
    log.info("Device: %s", device)
    if torch.cuda.is_available():
        log.info("GPU: %s", torch.cuda.get_device_name(0))
    loaders=get_all_dataloaders(view,frame_stride=frame_stride)
    for split_name, split_loader in loaders.items():
        if frame_stride > 1:
            log.info("Frame subsampling diterapkan (stride=%s): %s frame tersisa untuk view=%s split=%s", frame_stride, len(split_loader.dataset), view, split_name)
        log.info("DataLoader dibuat: view=%s split=%s n=%s batch_size=%s shuffle=%s", view, split_name, len(split_loader.dataset), split_loader.batch_size, split_name=="train")
    model=build_model(PRETRAINED,0,dropout).to(device)
    criterion=nn.BCEWithLogitsLoss()
    optimizer=torch.optim.Adam(model.parameters(),lr=lr)
    early=EarlyStopping(patience)
    ckpt=abspath(checkpoint_path or (FRONT_CHECKPOINT_PATH if view=="front" else SIDE_CHECKPOINT_PATH))
    hist=abspath(history_path or (FRONT_HISTORY_PATH if view=="front" else SIDE_HISTORY_PATH))
    summ=abspath(summary_path or (FRONT_SUMMARY_PATH if view=="front" else SIDE_SUMMARY_PATH))
    ckpt.parent.mkdir(parents=True,exist_ok=True); hist.parent.mkdir(parents=True,exist_ok=True); summ.parent.mkdir(parents=True,exist_ok=True)
    resolved={"view":view,"run_type":"experiment_run","loss_function":"BCEWithLogitsLoss","optimizer":"Adam","learning_rate":lr,"weight_decay":0.0,"dropout":dropout,"freeze_stages":0,"class_weights":None,"label_smoothing":0.0,"scheduler":None,"frame_stride":frame_stride,"threshold":DECISION_THRESHOLD,"seed":SPLIT_SEED if SEED_TRAINING else None,"seed_training":SEED_TRAINING,"batch_size":BATCH_SIZE,"checkpoint_monitor":"val_macro_f1","checkpoint_monitor_mode":"max","backbone":"EfficientNetV2-S","pretrained":PRETRAINED,"output_logits":1}
    rows=[]; best_epoch=0; start=time.time()
    for epoch in range(1,max_epochs+1):
        epoch_start=time.time()
        tr_loss,tr=train_one_epoch(model,loaders["train"],criterion,optimizer,device)
        va_loss,va=validate(model,loaders["val"],criterion,device)
        row={"epoch":epoch,"train_loss":round(tr_loss,5),"train_accuracy":round(tr["accuracy"],5),"train_macro_f1":round(tr["macro_f1"],5),"val_loss":round(va_loss,5),"val_accuracy":round(va["accuracy"],5),"val_macro_f1":round(va["macro_f1"],5),"f1_gap":round(tr["macro_f1"]-va["macro_f1"],5),"loss_gap":round(va_loss-tr_loss,5),"learning_rate":optimizer.param_groups[0]["lr"],"epoch_seconds":round(time.time()-epoch_start,2)}
        rows.append(row); is_best=early.step(va["macro_f1"])
        if is_best:
            best_epoch=epoch; torch.save({"epoch":epoch,"model_state_dict":model.state_dict(),"optimizer_state_dict":optimizer.state_dict(),"val_macro_f1":va["macro_f1"],"val_loss":va_loss,"view":view,"hyperparameters":resolved,"checkpoint_selection":{"monitored_metric":"val_macro_f1","mode":"max","best_epoch":epoch}},ckpt)
        status = "* BEST" if is_best else f"  wait {early.counter}/{patience}"
        log.info("Epoch %02d/%02d | train_loss=%.4f | val_loss=%.4f | val_F1=%.4f | val_acc=%.4f | lr=%.1e | %s | %.0fs", epoch, max_epochs, tr_loss, va_loss, va["macro_f1"], va["accuracy"], optimizer.param_groups[0]["lr"], status, row["epoch_seconds"])
        if early.should_stop: break
    write_history(rows,hist); summary={"view":view,"best_epoch":best_epoch,"checkpoint_path":str(ckpt),"checkpoint_sha256":sha256_file(ckpt),"history_path":str(hist),"history_csv_path":str(hist.with_suffix(".csv")),"checkpoint_selection":{"monitored_metric":"val_macro_f1","mode":"max"},"resolved_config":resolved,"best_epoch_metrics":rows[best_epoch-1] if best_epoch else None,"environment":env_metadata(),"elapsed_seconds":round(time.time()-start,2),"elapsed_minutes":round((time.time()-start)/60,3)}; write_json(summ,summary); log.info("TRAIN DONE | view=%s | best_epoch=%s | elapsed=%.2fs",view.upper(),best_epoch,time.time()-start); return rows


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--view",required=True,choices=["front","side"]); ap.add_argument("--epochs",type=int,default=MAX_EPOCHS); a=ap.parse_args(); run_training(a.view,a.epochs)
if __name__=="__main__": main()






