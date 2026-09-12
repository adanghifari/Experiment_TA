import argparse, csv, json, logging, os, random, time
from pathlib import Path
import numpy as np, torch, torch.nn as nn
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from src.config import *
try:
    WEIGHT_DECAY_FRONT
except NameError:
    WEIGHT_DECAY_FRONT=WEIGHT_DECAY; WEIGHT_DECAY_SIDE=WEIGHT_DECAY
from src.dataset import get_all_dataloaders, load_split_dataframe
from src.metrics import env_metadata, sha256_file, write_json
from src.model import build_model

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
log=logging.getLogger(__name__)

def seed_everything(seed=42):
    random.seed(seed); os.environ['PYTHONHASHSEED']=str(seed); np.random.seed(seed); torch.manual_seed(seed); torch.cuda.manual_seed_all(seed); torch.backends.cudnn.deterministic=True; torch.backends.cudnn.benchmark=False

def resolve_class_weights(view, exp_config=None, gamma=1.0):
    if exp_config:
        raw = exp_config['class_weights']
    else:
        per_view_name = 'CLASS_WEIGHTS_FRONT' if view == 'front' else 'CLASS_WEIGHTS_SIDE'
        raw = globals().get(per_view_name, CLASS_WEIGHTS)
    if raw!='balanced': return raw
    df=load_split_dataframe(view,'train'); counts={v:int((df['binary_label']==k).sum()) for k,v in BINARY_LABEL_MAP.items()}; total=sum(counts.values())
    return [float((total/(len(counts)*counts[i]))**gamma) for i in range(len(counts))]

def basic_metrics(labels,preds):
    return {'accuracy':accuracy_score(labels,preds),'macro_f1':f1_score(labels,preds,average='macro',zero_division=0),'precision_macro':precision_score(labels,preds,average='macro',zero_division=0),'recall_macro':recall_score(labels,preds,average='macro',zero_division=0)}

def train_one_epoch(model, loader, criterion, optimizer, device, epoch=None, log_every=0):
    model.train(); loss_sum=0; n=0; labels_all=[]; preds_all=[]; start=time.time(); total_batches=len(loader)
    for batch_idx,(images,labels) in enumerate(loader, start=1):
        images=images.to(device); y=labels.long().to(device); optimizer.zero_grad(); logits=model(images); loss=criterion(logits,y); loss.backward(); optimizer.step()
        preds=torch.argmax(logits,dim=1).detach().cpu().tolist(); labels_all.extend(labels.tolist()); preds_all.extend(preds); loss_sum+=loss.item()*images.size(0); n+=images.size(0)
        if log_every and (batch_idx==1 or batch_idx%log_every==0 or batch_idx==total_batches):
            prefix=f'Epoch {epoch:02d} TRAIN' if epoch is not None else 'TRAIN'
            log.info('%s batch %s/%s elapsed=%.2fs', prefix, batch_idx, total_batches, time.time()-start)
    return loss_sum/n, basic_metrics(labels_all,preds_all)
@torch.no_grad()
def validate(model, loader, criterion, device, epoch=None, log_every=0):
    model.eval(); loss_sum=0; n=0; labels_all=[]; preds_all=[]; start=time.time(); total_batches=len(loader)
    for batch_idx,(images,labels) in enumerate(loader, start=1):
        images=images.to(device); y=labels.long().to(device); logits=model(images); loss=criterion(logits,y); probs=torch.softmax(logits,dim=1)[:,1]; preds=(probs>=DECISION_THRESHOLD).long().cpu().tolist()
        labels_all.extend(labels.tolist()); preds_all.extend(preds); loss_sum+=loss.item()*images.size(0); n+=images.size(0)
        if log_every and (batch_idx==1 or batch_idx%log_every==0 or batch_idx==total_batches):
            prefix=f'Epoch {epoch:02d} VAL' if epoch is not None else 'VAL'
            log.info('%s batch %s/%s elapsed=%.2fs', prefix, batch_idx, total_batches, time.time()-start)
    return loss_sum/n, basic_metrics(labels_all,preds_all)
class EarlyStopping:
    def __init__(self, patience, mode='max'):
        self.patience=patience; self.mode=mode; self.best=-float('inf') if mode=='max' else float('inf'); self.counter=0; self.should_stop=False
    def step(self, score):
        ok=score>self.best if self.mode=='max' else score<self.best
        if ok: self.best=score; self.counter=0; return True
        self.counter+=1; self.should_stop=self.counter>=self.patience; return False

def abspath(path):
    p=Path(path); return p if p.is_absolute() else Path.cwd()/p

def write_history(rows, path):
    path=abspath(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(rows,indent=2),encoding='utf-8')
    with path.with_suffix('.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

def run_training(view, max_epochs=MAX_EPOCHS, exp_id='', lr=None, experiment='', class_weight_gamma=None, checkpoint_path=None, history_path=None, summary_path=None, frame_stride=FRAME_STRIDE, checkpoint_monitor=None):
    if SEED_TRAINING:
        seed_everything(SPLIT_SEED)
    exp_config = EXPERIMENT_CONFIGS.get(experiment) if experiment else None
    lr = lr if lr is not None else (LEARNING_RATE_FRONT if view == 'front' else LEARNING_RATE_SIDE)
    wd = WEIGHT_DECAY_FRONT if view == 'front' else WEIGHT_DECAY_SIDE
    dropout = DROPOUT_FRONT if view == 'front' else DROPOUT_SIDE
    freeze = NUM_STAGES_TO_FREEZE_FRONT if view == 'front' else NUM_STAGES_TO_FREEZE_SIDE
    patience = EARLY_STOPPING_PATIENCE_FRONT if view == 'front' else EARLY_STOPPING_PATIENCE_SIDE
    sched_pat = LR_SCHEDULER_PATIENCE_FRONT if view == 'front' else LR_SCHEDULER_PATIENCE_SIDE
    checkpoint_monitor = checkpoint_monitor or (CHECKPOINT_MONITOR_FRONT if view == 'front' else CHECKPOINT_MONITOR_SIDE)
    class_weight_gamma = class_weight_gamma if class_weight_gamma is not None else (CLASS_WEIGHT_GAMMA_FRONT if view == 'front' else CLASS_WEIGHT_GAMMA_SIDE)
    ls = LABEL_SMOOTHING
    weights = resolve_class_weights(view, exp_config, class_weight_gamma)
    mode = 'min' if checkpoint_monitor == 'val_loss' else 'max'
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    log.info('')
    log.info('=============================================')
    log.info('Experiment Configuration')
    log.info('=============================================')
    log.info('  Experiment     : %s', EXPERIMENT_NAME)
    log.info('  View           : %s', view)
    log.info('  Optimizer      : AdamW')
    log.info('  Learning Rate  : %.1e', lr)
    log.info('  Weight Decay   : %.1e', wd)
    log.info('  Scheduler      : ReduceLROnPlateau')
    log.info('  Dropout        : %s', dropout)
    log.info('  Frozen Stages  : %s', freeze)
    log.info('  EarlyStopping  : patience=%s', patience)
    log.info('  Loss           : CrossEntropyLoss')
    log.info('  Label Smoothing: %.2f', ls)
    log.info('  Class Weights  : %s', weights)
    log.info('  Seed           : %s', SPLIT_SEED if SEED_TRAINING else None)
    log.info('=============================================')
    log.info('Device: %s', device)
    if torch.cuda.is_available():
        log.info('GPU: %s', torch.cuda.get_device_name(0))
    loaders=get_all_dataloaders(view,frame_stride=frame_stride)
    for split_name, split_loader in loaders.items():
        if frame_stride > 1:
            log.info('Frame subsampling diterapkan (stride=%s): %s frame tersisa untuk view=%s split=%s', frame_stride, len(split_loader.dataset), view, split_name)
        log.info('DataLoader dibuat: view=%s split=%s n=%s batch_size=%s shuffle=%s', view, split_name, len(split_loader.dataset), split_loader.batch_size, split_name=='train')
    model=build_model(PRETRAINED,freeze,dropout).to(device); criterion=nn.CrossEntropyLoss(weight=torch.tensor(weights,dtype=torch.float).to(device),label_smoothing=ls); opt=torch.optim.AdamW(model.parameters(),lr=lr,weight_decay=wd); sch=torch.optim.lr_scheduler.ReduceLROnPlateau(opt,mode='max',factor=LR_SCHEDULER_FACTOR,patience=sched_pat); early=EarlyStopping(patience,mode)
    ckpt_default = FRONT_CHECKPOINT_PATH if view=='front' else SIDE_CHECKPOINT_PATH
    hist_default = FRONT_HISTORY_PATH if view=='front' else SIDE_HISTORY_PATH
    summ_default = FRONT_SUMMARY_PATH if view=='front' else SIDE_SUMMARY_PATH
    ckpt=abspath(checkpoint_path or ckpt_default); hist=abspath(history_path or hist_default); summ=abspath(summary_path or summ_default); ckpt.parent.mkdir(parents=True,exist_ok=True); hist.parent.mkdir(parents=True,exist_ok=True); summ.parent.mkdir(parents=True,exist_ok=True)
    resolved={'view':view,'run_type':'experiment_run','learning_rate':lr,'weight_decay':wd,'dropout':dropout,'label_smoothing':ls,'class_weights':weights,'class_weight_gamma':class_weight_gamma,'freeze_stages':freeze,'early_stopping_patience':patience,'lr_scheduler_patience':sched_pat,'lr_scheduler_factor':LR_SCHEDULER_FACTOR,'frame_stride':frame_stride,'threshold':DECISION_THRESHOLD,'seed':SPLIT_SEED if SEED_TRAINING else None,'seed_training':SEED_TRAINING,'batch_size':BATCH_SIZE,'checkpoint_monitor':checkpoint_monitor,'checkpoint_monitor_mode':mode,'optimizer':'AdamW','scheduler':'ReduceLROnPlateau','scheduler_monitor':'val_macro_f1','scheduler_step_timing':'after_validation','backbone':'EfficientNetV2-S','pretrained':PRETRAINED,'loss_function':LOSS_FUNCTION,'augmentation_train':{'random_horizontal_flip':True,'random_rotation_degree':AUG_ROTATION_DEGREE_FRONT if view=='front' else AUG_ROTATION_DEGREE_SIDE,'color_jitter_factor':AUG_COLOR_JITTER_FACTOR_FRONT if view=='front' else AUG_COLOR_JITTER_FACTOR_SIDE},'augmentation_eval':{'random_horizontal_flip':False,'random_rotation_degree':0,'color_jitter_factor':0},'class_weight_gamma_scope':'training_class_weights_only_not_fusion'}
    rows=[]; best_epoch=0; start=time.time()
    for epoch in range(1,max_epochs+1):
        epoch_start=time.time()
        tr_loss,tr=train_one_epoch(model,loaders['train'],criterion,opt,device,epoch)
        va_loss,va=validate(model,loaders['val'],criterion,device,epoch); sch.step(va['macro_f1'])
        row={'epoch':epoch,'train_loss':round(tr_loss,5),'train_accuracy':round(tr['accuracy'],5),'train_macro_f1':round(tr['macro_f1'],5),'train_precision_macro':round(tr['precision_macro'],5),'train_recall_macro':round(tr['recall_macro'],5),'val_loss':round(va_loss,5),'val_accuracy':round(va['accuracy'],5),'val_macro_f1':round(va['macro_f1'],5),'val_precision_macro':round(va['precision_macro'],5),'val_recall_macro':round(va['recall_macro'],5),'f1_gap':round(tr['macro_f1']-va['macro_f1'],5),'loss_gap':round(va_loss-tr_loss,5),'learning_rate':opt.param_groups[0]['lr'],'epoch_seconds':round(time.time()-epoch_start,2)}
        rows.append(row); score=row[checkpoint_monitor]; is_best=early.step(score)
        if is_best:
            best_epoch=epoch; torch.save({'epoch':epoch,'model_state_dict':model.state_dict(),'optimizer_state_dict':opt.state_dict(),'val_macro_f1':va['macro_f1'],'val_loss':va_loss,'train_loss':tr_loss,'train_accuracy':tr['accuracy'],'train_macro_f1':tr['macro_f1'],'train_precision_macro':tr['precision_macro'],'train_recall_macro':tr['recall_macro'],'val_accuracy':va['accuracy'],'val_precision_macro':va['precision_macro'],'val_recall_macro':va['recall_macro'],'train_val_loss_gap':va_loss-tr_loss,'train_val_f1_gap':tr['macro_f1']-va['macro_f1'],'view':view,'experiment':experiment,'num_stages_to_freeze':freeze,'hyperparameters':resolved,'checkpoint_selection':{'monitored_metric':checkpoint_monitor,'mode':mode,'best_epoch':epoch,'reason':f'Best validation {checkpoint_monitor} so far.'}},ckpt)
        status = '* BEST' if is_best else f'  wait {early.counter}/{patience}'
        log.info('Epoch %02d/%02d | train_loss=%.4f | val_loss=%.4f | val_F1=%.4f | val_acc=%.4f | lr=%.1e | %s | %.0fs', epoch, max_epochs, tr_loss, va_loss, va['macro_f1'], va['accuracy'], opt.param_groups[0]['lr'], status, row['epoch_seconds'])
        if early.should_stop: break
    write_history(rows,hist); log.info('TRAIN DONE | view=%s | best_epoch=%s | elapsed=%.2fs | checkpoint=%s | history=%s', view.upper(), best_epoch, time.time()-start, ckpt, hist); summary={'view':view,'best_epoch':best_epoch,'checkpoint_path':str(ckpt),'checkpoint_sha256':sha256_file(ckpt),'history_path':str(hist),'history_csv_path':str(hist.with_suffix('.csv')),'checkpoint_selection':{'monitored_metric':checkpoint_monitor,'mode':mode,'reason':f'Selected by validation {checkpoint_monitor}.'},'resolved_config':resolved,'best_epoch_metrics':rows[best_epoch-1] if best_epoch else None,'environment':env_metadata(),'elapsed_seconds':round(time.time()-start,2),'elapsed_minutes':round((time.time()-start)/60,3)}; write_json(summ,summary); return rows

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--view',required=True,choices=['front','side']); ap.add_argument('--epochs',type=int,default=MAX_EPOCHS); ap.add_argument('--exp_id',default=''); ap.add_argument('--lr',type=float); ap.add_argument('--experiment',default='',choices=sorted(EXPERIMENT_CONFIGS.keys())); ap.add_argument('--class-weight-gamma',type=float,default=None); ap.add_argument('--checkpoint-path'); ap.add_argument('--history-path'); ap.add_argument('--summary-path'); ap.add_argument('--frame-stride',type=int,default=FRAME_STRIDE); ap.add_argument('--checkpoint-monitor',choices=['val_macro_f1','val_loss'],default=None); a=ap.parse_args(); run_training(a.view,a.epochs,a.exp_id,a.lr,a.experiment,a.class_weight_gamma,a.checkpoint_path,a.history_path,a.summary_path,a.frame_stride,a.checkpoint_monitor)
if __name__=='__main__': main()


















