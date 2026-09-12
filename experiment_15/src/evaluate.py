import argparse, csv, logging, time
from pathlib import Path
import torch
from src.config import CHECKPOINT_DIR, DECISION_THRESHOLD, DROPOUT_FRONT, DROPOUT_SIDE, FRAME_STRIDE, RESULTS_DIR
from src.dataset import get_eval_dataloader, load_split_dataframe
from src.metrics import compute_metrics, sha256_file, write_json
from src.model import build_model
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
log=logging.getLogger(__name__)

def load_trained_model(view, device, exp_id='', dropout_rate=None, checkpoint_path=None):
    ckpt=Path(checkpoint_path) if checkpoint_path else CHECKPOINT_DIR/(f'{view}_{exp_id}_best.pt' if exp_id else f'{view}_best.pt')
    if not ckpt.is_absolute(): ckpt=Path.cwd()/ckpt
    if not ckpt.exists(): raise FileNotFoundError(f'Checkpoint tidak ditemukan: {ckpt}')
    checkpoint=torch.load(ckpt,map_location=device,weights_only=False)
    if dropout_rate is None: dropout_rate=checkpoint.get('hyperparameters',{}).get('dropout',DROPOUT_FRONT if view=='front' else DROPOUT_SIDE)
    from src.config import NUM_STAGES_TO_FREEZE_FRONT, NUM_STAGES_TO_FREEZE_SIDE
    freeze=checkpoint.get('num_stages_to_freeze',NUM_STAGES_TO_FREEZE_FRONT if view=='front' else NUM_STAGES_TO_FREEZE_SIDE)
    model=build_model(False,freeze,dropout_rate); model.load_state_dict(checkpoint['model_state_dict']); model=model.to(device); model.eval(); return model,checkpoint,ckpt

@torch.no_grad()
def predict_loader(model, loader, device):
    labels_all=[]; preds_all=[]; probs_all=[]
    for images,labels in loader:
        logits=model(images.to(device)); probs=torch.softmax(logits,dim=1)[:,1]; preds=(probs>=DECISION_THRESHOLD).long().cpu()
        labels_all.extend(labels.tolist()); preds_all.extend(preds.tolist()); probs_all.extend(probs.cpu().tolist())
    return labels_all,preds_all,probs_all

def write_predictions(path, df, labels, preds, probs):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        fields=['row_index','subject_id','activity_id','frame','filepath','label','prediction','prob_phone']
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for i,(label,pred,prob) in enumerate(zip(labels,preds,probs)):
            r=df.iloc[i]; w.writerow({'row_index':i,'subject_id':r.get('subject_id'),'activity_id':r.get('activity_id'),'frame':r.get('frame'),'filepath':r.get('filepath'),'label':label,'prediction':pred,'prob_phone':prob})

def evaluate_view(view, exp_id='', checkpoint_path=None, output_path=None, split='test', predictions_path=None, frame_stride=FRAME_STRIDE):
    start=time.time()
    log.info('EVAL START | view=%s | split=%s | stride=%s | checkpoint=%s', view.upper(), split, frame_stride, checkpoint_path)
    device=torch.device('cuda' if torch.cuda.is_available() else 'cpu'); model,checkpoint,ckpt=load_trained_model(view,device,exp_id,checkpoint_path=checkpoint_path)
    loader=get_eval_dataloader(view,split,frame_stride=frame_stride); log.info('Data | view=%s split=%s batches=%s samples=%s batch_size=%s', view, split, len(loader), len(loader.dataset), loader.batch_size); labels,preds,probs=predict_loader(model,loader,device); metrics=compute_metrics(labels,preds,probs,method=f'{view}_{split}')
    metrics.update({'view':view,'split':split,'checkpoint_path':str(ckpt),'checkpoint_sha256':sha256_file(ckpt),'best_epoch':checkpoint.get('epoch'),'checkpoint_selection':checkpoint.get('checkpoint_selection'),'hyperparameters':checkpoint.get('hyperparameters')})
    out=Path(output_path) if output_path else RESULTS_DIR/f'{view}_{split}_metrics.json'; out=out if out.is_absolute() else Path.cwd()/out; write_json(out,metrics)
    if predictions_path:
        pred=Path(predictions_path); pred=pred if pred.is_absolute() else Path.cwd()/pred; write_predictions(pred,load_split_dataframe(view,split,frame_stride),labels,preds,probs)
    log.info('EVAL DONE | view=%s | split=%s | macro_f1=%.4f | acc=%.4f | elapsed=%.2fs | output=%s',view.upper(),split,metrics['f1_macro'],metrics['accuracy'],time.time()-start,out); return metrics

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--view',required=True,choices=['front','side']); ap.add_argument('--split',default='test',choices=['train','val','test']); ap.add_argument('--exp_id',default=''); ap.add_argument('--checkpoint'); ap.add_argument('--output'); ap.add_argument('--predictions-output'); ap.add_argument('--frame-stride',type=int,default=FRAME_STRIDE); a=ap.parse_args(); evaluate_view(a.view,a.exp_id,a.checkpoint,a.output,a.split,a.predictions_output,a.frame_stride)
if __name__=='__main__': main()



