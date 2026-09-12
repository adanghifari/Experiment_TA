import logging
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from src.config import MANIFEST_SPLIT_PATH, IMAGE_SIZE, IMAGENET_MEAN, IMAGENET_STD, BATCH_SIZE, BINARY_LABEL_MAP, FRAME_STRIDE, AUG_ROTATION_DEGREE_FRONT, AUG_COLOR_JITTER_FACTOR_FRONT, AUG_ROTATION_DEGREE_SIDE, AUG_COLOR_JITTER_FACTOR_SIDE, SORT_DATAFRAME

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
log=logging.getLogger(__name__)

class DriverViewDataset(Dataset):
    def __init__(self, df, transform): self.df=df.reset_index(drop=True); self.transform=transform
    def __len__(self): return len(self.df)
    def __getitem__(self, idx):
        row=self.df.iloc[idx]
        image=self.transform(Image.open(row['filepath']).convert('RGB'))
        return image, BINARY_LABEL_MAP[row['binary_label']]

def get_transforms(view, split, eval_mode=False):
    if split=='train' and not eval_mode:
        rot=AUG_ROTATION_DEGREE_FRONT if view=='front' else AUG_ROTATION_DEGREE_SIDE
        jit=AUG_COLOR_JITTER_FACTOR_FRONT if view=='front' else AUG_COLOR_JITTER_FACTOR_SIDE
        return transforms.Compose([transforms.Resize((IMAGE_SIZE,IMAGE_SIZE)),transforms.RandomHorizontalFlip(),transforms.RandomRotation(rot),transforms.ColorJitter(brightness=jit,contrast=jit,saturation=jit),transforms.ToTensor(),transforms.Normalize(mean=IMAGENET_MEAN,std=IMAGENET_STD)])
    return transforms.Compose([transforms.Resize((IMAGE_SIZE,IMAGE_SIZE)),transforms.ToTensor(),transforms.Normalize(mean=IMAGENET_MEAN,std=IMAGENET_STD)])

def load_split_dataframe(view, split, frame_stride=FRAME_STRIDE):
    df=pd.read_csv(MANIFEST_SPLIT_PATH)
    out=df[(df['view']==view)&(df['split']==split)].copy()
    if out.empty: raise ValueError(f'Tidak ada data view={view} split={split}')
    if frame_stride>1: out=out[(out['frame']-1)%frame_stride==0].copy()
    if SORT_DATAFRAME:
        out=out.sort_values(['subject_id','activity_id','frame','filepath'])
    return out.reset_index(drop=True)

def get_dataloader(view, split, batch_size=BATCH_SIZE, num_workers=0, shuffle=None, frame_stride=FRAME_STRIDE, eval_mode=False):
    df=load_split_dataframe(view,split,frame_stride)
    if shuffle is None: shuffle=(split=='train' and not eval_mode)
    return DataLoader(DriverViewDataset(df,get_transforms(view,split,eval_mode)),batch_size=batch_size,shuffle=shuffle,num_workers=num_workers,pin_memory=True,drop_last=(split=='train' and not eval_mode))

def get_eval_dataloader(view, split, batch_size=BATCH_SIZE, num_workers=0, frame_stride=FRAME_STRIDE):
    return get_dataloader(view,split,batch_size,num_workers,shuffle=False,frame_stride=frame_stride,eval_mode=True)

def get_all_dataloaders(view, batch_size=BATCH_SIZE, num_workers=0, frame_stride=FRAME_STRIDE):
    return {s:get_dataloader(view,s,batch_size,num_workers,frame_stride=frame_stride) for s in ('train','val','test')}

