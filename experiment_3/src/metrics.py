import hashlib, json, platform, subprocess, sys
from datetime import datetime
from pathlib import Path
import numpy as np
from sklearn.metrics import accuracy_score, average_precision_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score

CLASS_NAMES = ['safe_driving', 'phone_use']

def rf(x, n=5):
    if x is None: return None
    try: return round(float(x), n)
    except Exception: return x

def ece_binary(probs, labels, n_bins=10):
    probs=np.asarray(probs,float); labels=np.asarray(labels,int); edges=np.linspace(0,1,n_bins+1); out=0.0
    for i in range(n_bins):
        lo,hi=edges[i],edges[i+1]
        mask=(probs>=lo)&(probs<=hi if i==n_bins-1 else probs<hi)
        if mask.sum(): out += (mask.sum()/len(probs))*abs(labels[mask].mean()-probs[mask].mean())
    return float(out)

def brier(probs, labels):
    probs=np.asarray(probs,float); labels=np.asarray(labels,int)
    return float(np.mean((probs-labels)**2))

def compute_metrics(labels, preds, probs=None, method=None):
    labels=np.asarray(labels,int); preds=np.asarray(preds,int)
    rep=classification_report(labels,preds,labels=[0,1],target_names=CLASS_NAMES,zero_division=0,output_dict=True)
    m={
        'method':method,
        'accuracy':rf(accuracy_score(labels,preds)),
        'precision_macro':rf(precision_score(labels,preds,average='macro',zero_division=0)),
        'recall_macro':rf(recall_score(labels,preds,average='macro',zero_division=0)),
        'f1_macro':rf(f1_score(labels,preds,average='macro',zero_division=0)),
        'precision_safe':rf(rep['safe_driving']['precision']),
        'recall_safe':rf(rep['safe_driving']['recall']),
        'f1_safe':rf(rep['safe_driving']['f1-score']),
        'support_safe':int(rep['safe_driving']['support']),
        'precision_phone':rf(rep['phone_use']['precision']),
        'recall_phone':rf(rep['phone_use']['recall']),
        'f1_phone':rf(rep['phone_use']['f1-score']),
        'support_phone':int(rep['phone_use']['support']),
        'support_total':int(len(labels)),
        'confusion_matrix':confusion_matrix(labels,preds,labels=[0,1]).tolist(),
        'classification_report':rep,
    }
    if probs is not None:
        probs=np.asarray(probs,float)
        try: m['roc_auc']=rf(roc_auc_score(labels,probs))
        except ValueError: m['roc_auc']=None
        try: m['pr_auc']=rf(average_precision_score(labels,probs))
        except ValueError: m['pr_auc']=None
        m['ece_binary']=rf(ece_binary(probs,labels)); m['brier_score']=rf(brier(probs,labels))
    return m

def sha256_file(path):
    path=Path(path)
    if not path.exists(): return None
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()

def git_commit(cwd='.'):
    try: return subprocess.check_output(['git','rev-parse','--verify','HEAD'],cwd=cwd,text=True,stderr=subprocess.DEVNULL).strip()
    except Exception: return None

def env_metadata():
    import torch
    try:
        import timm; tv=timm.__version__
    except Exception: tv=None
    return {'timestamp':datetime.now().isoformat(timespec='seconds'),'python_version':sys.version,'platform':platform.platform(),'pytorch_version':torch.__version__,'timm_version':tv,'cuda_available':bool(torch.cuda.is_available()),'cuda_version':torch.version.cuda,'gpu':torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,'git_commit':git_commit(Path.cwd()),'cudnn_deterministic':bool(torch.backends.cudnn.deterministic),'cudnn_benchmark':bool(torch.backends.cudnn.benchmark)}

def write_json(path, data):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(data,indent=2),encoding='utf-8')

