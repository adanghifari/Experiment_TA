import argparse, csv, logging, time
from pathlib import Path
import numpy as np, pandas as pd, torch
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from src.config import BATCH_SIZE, BINARY_LABEL_MAP, DECISION_THRESHOLD, FRAME_STRIDE, MANIFEST_PAIRED_PATH, MANIFEST_SPLIT_PATH, SORT_PAIRED
from src.dataset import get_transforms
from src.evaluate import load_trained_model
from src.metrics import compute_metrics, write_json
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
log=logging.getLogger(__name__)

class PairedDataset(Dataset):
    def __init__(self,df,transform): self.df=df.reset_index(drop=True); self.transform=transform
    def __len__(self): return len(self.df)
    def __getitem__(self,idx):
        r=self.df.iloc[idx]; return self.transform(Image.open(r['filepath_front']).convert('RGB')), self.transform(Image.open(r['filepath_side']).convert('RGB')), BINARY_LABEL_MAP[r['binary_label']]

def load_paired_df(frame_stride=FRAME_STRIDE):
    split=pd.read_csv(MANIFEST_SPLIT_PATH); subjects=set(split[split['split']=='test']['subject_id'].unique()); df=pd.read_csv(MANIFEST_PAIRED_PATH); df=df[df['subject_id'].isin(subjects)].copy()
    if frame_stride>1: df=df[(df['frame']-1)%frame_stride==0].copy()
    if SORT_PAIRED:
        df=df.sort_values(['subject_id','activity_id','frame'])
    df=df.reset_index(drop=True)
    if df.empty: raise ValueError('Paired test set kosong')
    if df.duplicated(['subject_id','activity_id','frame']).any(): raise ValueError('Duplicate paired sample id')
    if (df['filepath_front']==df['filepath_side']).any(): raise ValueError('Front dan side filepath identik')
    return df

def loader(df): return DataLoader(PairedDataset(df,get_transforms('front','test',eval_mode=True)),batch_size=BATCH_SIZE,shuffle=False,num_workers=0,pin_memory=True)
def average_fusion(f,s): return 0.5*f+0.5*s
def adaptive_fusion(f,s,threshold=DECISION_THRESHOLD):
    df=np.abs(f-threshold); ds=np.abs(s-threshold); ef=np.exp(df); es=np.exp(ds); return (ef/(ef+es))*f+(es/(ef+es))*s
@torch.no_grad()
def scores(model_f,model_s,ld,device):
    sf=[]; ss=[]; labels=[]
    for img_f,img_s,y in ld:
        pf=torch.softmax(model_f(img_f.to(device)),dim=1)[:,1].cpu().numpy(); ps=torch.softmax(model_s(img_s.to(device)),dim=1)[:,1].cpu().numpy(); sf.extend(pf.tolist()); ss.extend(ps.tolist()); labels.extend(y.tolist())
    return np.array(sf),np.array(ss),np.array(labels)
def comp(labels,pf,ps,pfu):
    fc=pf==labels; sc=ps==labels; uc=pfu==labels
    return {'both_correct':int(np.sum(fc&sc)),'both_wrong':int(np.sum(~fc&~sc)),'front_correct_side_wrong':int(np.sum(fc&~sc)),'front_wrong_side_correct':int(np.sum(~fc&sc)),'side_only_correct':int(np.sum(~fc&sc)),'fusion_fixed_front_error':int(np.sum(~fc&uc)),'fusion_broke_front_correct':int(np.sum(fc&~uc)),'support':int(len(labels))}
def write_preds(path,df,labels,sf,ss,sa,sd):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); pf=(sf>=DECISION_THRESHOLD).astype(int); ps=(ss>=DECISION_THRESHOLD).astype(int); pa=(sa>=DECISION_THRESHOLD).astype(int); pdp=(sd>=DECISION_THRESHOLD).astype(int)
    fields=['row_index','subject_id','activity_id','frame','label','front_prob_phone','side_prob_phone','average_prob_phone','adaptive_prob_phone','front_pred','side_pred','average_pred','adaptive_pred','filepath_front','filepath_side']
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for i,r in df.iterrows(): w.writerow({'row_index':i,'subject_id':r['subject_id'],'activity_id':r['activity_id'],'frame':r['frame'],'label':int(labels[i]),'front_prob_phone':float(sf[i]),'side_prob_phone':float(ss[i]),'average_prob_phone':float(sa[i]),'adaptive_prob_phone':float(sd[i]),'front_pred':int(pf[i]),'side_pred':int(ps[i]),'average_pred':int(pa[i]),'adaptive_pred':int(pdp[i]),'filepath_front':r['filepath_front'],'filepath_side':r['filepath_side']})

def main():
    start=time.time()
    log.info('FUSION START | average + adaptive fusion')
    ap=argparse.ArgumentParser(); ap.add_argument('--front-checkpoint',required=True); ap.add_argument('--side-checkpoint',required=True); ap.add_argument('--output',default='results/fusion/fusion_metrics.json'); ap.add_argument('--predictions-output',default='results/predictions/fusion_predictions.csv'); ap.add_argument('--frame-stride',type=int,default=FRAME_STRIDE); a=ap.parse_args()
    device=torch.device('cuda' if torch.cuda.is_available() else 'cpu'); log.info('Device | %s', device); log.info('Checkpoints | front=%s | side=%s', a.front_checkpoint, a.side_checkpoint); mf,_,_=load_trained_model('front',device,checkpoint_path=a.front_checkpoint); ms,_,_=load_trained_model('side',device,checkpoint_path=a.side_checkpoint); df=load_paired_df(a.frame_stride); log.info('Data | paired_test samples=%s | stride=%s', len(df), a.frame_stride); sf,ss,labels=scores(mf,ms,loader(df),device)
    if len(df)!=len(labels): raise ValueError(f'Paired mismatch df={len(df)} labels={len(labels)}')
    savg=average_fusion(sf,ss); sad=adaptive_fusion(sf,ss); pf=(sf>=DECISION_THRESHOLD).astype(int); ps=(ss>=DECISION_THRESHOLD).astype(int); pa=(savg>=DECISION_THRESHOLD).astype(int); pdp=(sad>=DECISION_THRESHOLD).astype(int)
    res={'paired_validation':{'sample_count':int(len(labels)),'unique_sample_count':int(len(df.drop_duplicates(["subject_id","activity_id","frame"]))),'sample_order':'subject_id, activity_id, frame' if SORT_PAIRED else 'manifest_paired_csv_order'},'single_front':compute_metrics(labels,pf,sf,'Single-view FRONT paired'),'single_side':compute_metrics(labels,ps,ss,'Single-view SIDE paired'),'average_fusion':compute_metrics(labels,pa,savg,'Average Fusion 50:50'),'adaptive_fusion':compute_metrics(labels,pdp,sad,'Adaptive Fusion confidence softmax'),'complementarity_average':comp(labels,pf,ps,pa),'complementarity_adaptive':comp(labels,pf,ps,pdp)}
    out=Path(a.output); out=out if out.is_absolute() else Path.cwd()/out; write_json(out,res); write_json(out.parent/'average_fusion_metrics.json',res['average_fusion']); write_json(out.parent/'adaptive_fusion_metrics.json',res['adaptive_fusion']); write_json(out.parent/'front_paired_metrics.json',res['single_front']); write_json(out.parent/'side_paired_metrics.json',res['single_side']); write_json(out.parent/'complementarity_analysis.json',{'average_fusion':res['complementarity_average'],'adaptive_fusion':res['complementarity_adaptive']}); write_preds(a.predictions_output,df,labels,sf,ss,savg,sad); log.info('FUSION DONE | avg_f1=%.4f | adaptive_f1=%.4f | elapsed=%.2fs | output=%s', res['average_fusion']['f1_macro'], res['adaptive_fusion']['f1_macro'], time.time()-start, out)
if __name__=='__main__': main()




