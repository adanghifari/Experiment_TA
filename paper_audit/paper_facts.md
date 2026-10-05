# Paper Facts Audit - Targeted Repair

Status: repaired existing audit only. No training, no model inference, no experiment artifact edit, no Paper_TA edit.

## Blocking Issues First
No blocking issue for descriptive paper writing. Wording caveats remain in unresolved_items.csv.

## Dataset Counts

table,rows,unique_subjects,view_counts,activity_counts,safe_count,phone_count,phone_pct

manifest_full,222034,50,"{""side"": 111017, ""front"": 111017}","{""1"": 13522, ""2"": 12906, ""3"": 13068, ""4"": 15314, ""5"": 12674, ""6"": 12720, ""7"": 14746, ""8"": 14974, ""9"": 14554, ""10"": 16758, ""11"": 14486, ""12"": 13668, ""13"": 12774, ""14"": 12792, ""15"": 11602, ""16"": 15476}",,,

manifest_binary,83190,50,"{""side"": 41595, ""front"": 41595}","{""1"": 13522, ""5"": 12674, ""6"": 12720, ""7"": 14746, ""8"": 14974, ""9"": 14554}",13522.0,69668.0,0.83746

manifest_split,83190,50,"{""side"": 41595, ""front"": 41595}","{""1"": 13522, ""5"": 12674, ""6"": 12720, ""7"": 14746, ""8"": 14974, ""9"": 14554}",13522.0,69668.0,0.83746

manifest_paired,41595,50,,"{""1"": 6761, ""5"": 6337, ""6"": 6360, ""7"": 7373, ""8"": 7487, ""9"": 7277}",6761.0,34834.0,0.83746



## Split And Final Post-Stride Counts

split,subject_count,subjects,stride,front_safe,front_phone,front_total,side_safe,side_phone,side_total,paired_safe_per_view,paired_phone_per_view,paired_total_per_view,front_side_identity_match,front_side_identity_symmetric_difference,final_master_sample_count,status,evidence

train,35,5 6 7 9 12 13 14 16 18 19 23 24 25 26 28 29 30 31 32 33 34 35 36 37 38 39 40 43 44 45 46 47 48 49 50,30,176,908,1084,176,908,1084,176,908,1084,True,0,1084,VERIFIED_PASS,manifest_split filtered (frame-1)%30==0

val,8,1 2 3 15 20 22 27 41,30,34,191,225,34,191,225,34,191,225,True,0,225,VERIFIED_PASS,manifest_split filtered (frame-1)%30==0

test,7,4 8 10 11 17 21 42,30,40,180,220,40,180,220,40,180,220,True,0,220,VERIFIED_PASS,manifest_split filtered (frame-1)%30==0



## Main Results

model,accuracy,macro_f1,macro_precision,macro_recall,safe_recall,phone_recall,roc_auc,pr_auc,ece,brier,confusion_matrix,source

Front,0.86364,0.76626,0.77183,0.76111,0.6,0.92222,0.88014,0.97075,0.12513,0.11311,"[[24,16],[14,166]]",front/test_eval_metrics.json

Side,0.80455,0.67468,0.67305,0.67639,0.475,0.87778,0.75444,0.92515,0.16761,0.15333,"[[19,21],[22,158]]",side/test_eval_metrics.json

Average Fusion,0.89545,0.81113,0.83868,0.79028,0.625,0.95556,0.86292,0.96236,0.17916,0.12341,"[[25,15],[8,172]]",fusion/average_fusion_metrics.json

Adaptive Fusion,0.89545,0.81113,0.83868,0.79028,0.625,0.95556,0.865,0.96329,0.17159,0.12028,"[[25,15],[8,172]]",fusion/adaptive_fusion_metrics.json



## Per-Class Results

model,class,precision,recall,f1,support

Front,safe_driving,0.63158,0.6,0.61538,40.0

Front,phone_use,0.91209,0.92222,0.91713,180.0

Side,safe_driving,0.46341,0.475,0.46914,40.0

Side,phone_use,0.88268,0.87778,0.88022,180.0

Average Fusion,safe_driving,0.75758,0.625,0.68493,40.0

Average Fusion,phone_use,0.91979,0.95556,0.93733,180.0

Adaptive Fusion,safe_driving,0.75758,0.625,0.68493,40.0

Adaptive Fusion,phone_use,0.91979,0.95556,0.93733,180.0



## Training Behavior

model,best_epoch,actual_epochs,selected_train_loss,selected_val_loss,selected_train_macro_f1,selected_val_macro_f1,train_val_loss_gap,train_val_f1_gap,test_macro_f1,health_flag,status

Front,9,NA,0.47353,0.51736,0.69929,0.72581,0.04383,-0.02652,0.76626,no overfit by F1 gap,DESCRIPTIVE_NOT_CAUSAL

Side,26,NA,0.3948,0.50217,0.79013,0.68238,0.10737,0.10775,0.67468,overfit risk,DESCRIPTIVE_NOT_CAUSAL



## Complementarity

subset,n,both_correct,both_wrong,front_only_correct,side_only_correct,average_fixed_front_error,average_broke_front_correct,adaptive_fixed_front_error,adaptive_broke_front_correct,both_correct_pct,both_wrong_pct,front_only_correct_pct,side_only_correct_pct,average_fixed_front_error_pct,average_broke_front_correct_pct,adaptive_fixed_front_error_pct,adaptive_broke_front_correct_pct,status

all,220,164,17,26,13,13,6,13,6,0.74545,0.07727,0.11818,0.05909,0.05909,0.02727,0.05909,0.02727,VERIFIED

safe_driving,40,15,12,9,4,4,3,4,3,0.375,0.3,0.225,0.1,0.1,0.075,0.1,0.075,VERIFIED

phone_use,180,149,5,17,9,9,3,9,3,0.82778,0.02778,0.09444,0.05,0.05,0.01667,0.05,0.01667,VERIFIED



## Corrected Adaptive Weight Statistics

subset,formula,n,max_abs_recomputed_adaptive_prob_error,front_weight_mean,front_weight_std,front_weight_median,front_weight_q1,front_weight_q3,front_weight_min,front_weight_max,side_weight_mean,side_weight_std,side_weight_median,side_weight_q1,side_weight_q3,side_weight_min,side_weight_max,front_weight_0_45_to_0_55_count,front_weight_0_40_to_0_60_count,front_weight_gt_0_60_count,front_weight_lt_0_40_count,average_vs_adaptive_prediction_diff_count,average_vs_adaptive_prediction_diff_pct,mean_abs_prob_diff_average_adaptive,max_abs_prob_diff_average_adaptive,exp23_seed42_max_front_weight_diff,exp23_seed42_max_adaptive_prob_diff,root_cause_previous_audit_error,status,mean_front_weight,mean_side_weight,std_front_weight,std_side_weight,min_front_weight,max_front_weight,min_side_weight,max_side_weight,adaptive_vs_average_prediction_diff_count,adaptive_vs_average_prediction_diff_pct,front_weight_gt_side_count,side_weight_gt_front_count,both_weights_near_0_5_count

Exp18 test,w=exp(abs(p-0.5))/(exp(abs(p_front-0.5))+exp(abs(p_side-0.5))),220,0.0,0.5126,0.03923,0.51096,0.48638,0.53951,0.41105,0.61037,0.4874,0.03923,0.48904,0.46049,0.51362,0.38963,0.58895,173.0,219.0,1.0,0.0,0.0,0.0,0.00757,0.05103,0.0,0.0,"previous audit used linear confidence normalization abs/(abs_front+abs_side), not implementation softmax over confidence",CORRECTED_VERIFIED,,,,,,,,,,,,,

Exp23 seed42,stored by experiment_23 fusion.py,220,,,,,,,,,,,,,,,,,,,,,,,,,,,REFERENCE_FROM_EXP23,0.5126,0.4874,0.03914,0.03914,0.41105,0.61037,0.38963,0.58895,0.0,0.0,139.0,81.0,173.0

Exp23 seed43,stored by experiment_23 fusion.py,220,,,,,,,,,,,,,,,,,,,,,,,,,,,REFERENCE_FROM_EXP23,0.51439,0.48561,0.03382,0.03382,0.41015,0.59623,0.40377,0.58985,0.0,0.0,143.0,77.0,181.0

Exp23 seed44,stored by experiment_23 fusion.py,220,,,,,,,,,,,,,,,,,,,,,,,,,,,REFERENCE_FROM_EXP23,0.50368,0.49632,0.03877,0.03877,0.40256,0.60711,0.39289,0.59744,0.0,0.0,120.0,100.0,174.0



## Probability Pipeline
Images -> logits. Training uses CrossEntropyLoss(logits, labels). Evaluation/fusion applies softmax and uses p(phone_use). Fusion inputs are raw softmax probabilities. ECE/Brier are evaluation-only; no temperature scaling found.

## Seed Control
Python random, PYTHONHASHSEED, NumPy, torch CPU/CUDA, cudnn deterministic=True, cudnn benchmark=False are set. DataLoader generator, worker_init_fn, torch.use_deterministic_algorithms not found. Do not claim bitwise determinism.

## Proposal Vs Actual

item,proposal_or_planned_value,actual_repo_value,status,evidence,paper_action

task definition,NOT_AVAILABLE_FROM_REPO,binary classification: safe driving vs phone use,SUPPORTED,config/results,USE_ACTUAL_VALUE

included activities,NOT_AVAILABLE_FROM_REPO,"A1,A5,A6,A7,A8,A9",SUPPORTED,config.py,USE_ACTUAL_VALUE

binary mapping,NOT_AVAILABLE_FROM_REPO,safe_driving=0; phone_use=1,SUPPORTED,config.py,USE_ACTUAL_VALUE

positive class,NOT_AVAILABLE_FROM_REPO,phone_use,SUPPORTED,prob_phone columns,USE_ACTUAL_VALUE

raw synchronized pair count,NOT_AVAILABLE_FROM_REPO,41595,SUPPORTED,manifest_paired.csv,USE_ACTUAL_VALUE

safe count manifest_split before stride,NOT_AVAILABLE_FROM_REPO,13522,SUPPORTED,manifest_split.csv,USE_ACTUAL_VALUE

phone count manifest_split before stride,NOT_AVAILABLE_FROM_REPO,69668,SUPPORTED,manifest_split.csv,USE_ACTUAL_VALUE

view mapping,NOT_AVAILABLE_FROM_REPO,RGB1=side; RGB2=front,SUPPORTED,config.py,USE_ACTUAL_VALUE

dataset correction,NOT_AVAILABLE_FROM_REPO,RGB1/S31 AC9-AC10 correction implemented; separate visual proof not found,PARTIAL_SUPPORTED,config.py; dataset_integrity.csv,WORD_WITH_CAVEAT

subject split counts,NOT_AVAILABLE_FROM_REPO,train=35; val=8; test=7,SUPPORTED,table_split.csv,USE_ACTUAL_VALUE

subject IDs,NOT_AVAILABLE_FROM_REPO,train: 5 6 7 9 12 13 14 16 18 19 23 24 25 26 28 29 30 31 32 33 34 35 36 37 38 39 40 43 44 45 46 47 48 49 50 | val: 1 2 3 15 20 22 27 41 | test: 4 8 10 11 17 21 42,SUPPORTED,table_split.csv,USE_ACTUAL_VALUE

stride,NOT_AVAILABLE_FROM_REPO,30,SUPPORTED,resolved_config,USE_ACTUAL_VALUE

post-stride counts,NOT_AVAILABLE_FROM_REPO,train safe/phone/total=176/908/1084; val=34/191/225; test=40/180/220 per view,SUPPORTED,table_split.csv,USE_ACTUAL_VALUE

input size,NOT_AVAILABLE_FROM_REPO,224,SUPPORTED,config.py,USE_ACTUAL_VALUE

normalization,NOT_AVAILABLE_FROM_REPO,ImageNet mean/std,SUPPORTED,config.py,USE_ACTUAL_VALUE

augmentation,NOT_AVAILABLE_FROM_REPO,front rot=68 jitter=1.2; side rot=45 jitter=0.8; hflip default p=0.5,SUPPORTED,dataset.py/config.py,USE_ACTUAL_VALUE

backbone,NOT_AVAILABLE_FROM_REPO,timm tf_efficientnetv2_s / EfficientNetV2-S,SUPPORTED,model.py/config.py,USE_ACTUAL_VALUE

pretrained initialization,NOT_AVAILABLE_FROM_REPO,True,SUPPORTED,train metadata,USE_ACTUAL_VALUE

classifier,NOT_AVAILABLE_FROM_REPO,"Dropout -> Linear(in_features,2)",SUPPORTED,model.py,USE_ACTUAL_VALUE

loss,NOT_AVAILABLE_FROM_REPO,CrossEntropyLoss with class weights and label smoothing,SUPPORTED,train.py,USE_ACTUAL_VALUE

optimizer,NOT_AVAILABLE_FROM_REPO,AdamW,SUPPORTED,train.py,USE_ACTUAL_VALUE

Front LR,NOT_AVAILABLE_FROM_REPO,3e-05,SUPPORTED,checkpoint metadata,USE_ACTUAL_VALUE

Side LR,NOT_AVAILABLE_FROM_REPO,2e-05,SUPPORTED,checkpoint metadata,USE_ACTUAL_VALUE

Front weight decay,NOT_AVAILABLE_FROM_REPO,0.0005,SUPPORTED,checkpoint metadata,USE_ACTUAL_VALUE

Side weight decay,NOT_AVAILABLE_FROM_REPO,0.001,SUPPORTED,checkpoint metadata,USE_ACTUAL_VALUE

batch size,NOT_AVAILABLE_FROM_REPO,32,SUPPORTED,checkpoint metadata,USE_ACTUAL_VALUE

max epochs,NOT_AVAILABLE_FROM_REPO,30,SUPPORTED,config/final_master,USE_ACTUAL_VALUE

dropout,NOT_AVAILABLE_FROM_REPO,Front=0.4; Side=0.4,SUPPORTED,checkpoint metadata,USE_ACTUAL_VALUE

freeze stages,NOT_AVAILABLE_FROM_REPO,Front=5; Side=4,SUPPORTED,checkpoint metadata,USE_ACTUAL_VALUE

class weights,NOT_AVAILABLE_FROM_REPO,"[2.5,1.0] order safe,phone",SUPPORTED,checkpoint metadata,USE_ACTUAL_VALUE

scheduler,NOT_AVAILABLE_FROM_REPO,ReduceLROnPlateau factor=0.5,SUPPORTED,train metadata,USE_ACTUAL_VALUE

early stopping,NOT_AVAILABLE_FROM_REPO,Front patience=4; Side patience=5,SUPPORTED,checkpoint metadata,USE_ACTUAL_VALUE

checkpoint criterion,NOT_AVAILABLE_FROM_REPO,Front val_macro_f1 max; Side val_loss min,SUPPORTED,checkpoint metadata,USE_ACTUAL_VALUE

Average formula,NOT_AVAILABLE_FROM_REPO,0.5*p_front+0.5*p_side,SUPPORTED,fusion.py,USE_ACTUAL_VALUE

Adaptive formula,NOT_AVAILABLE_FROM_REPO,softmax over abs(p-0.5) confidence,SUPPORTED,fusion.py/adaptive_analysis.csv,USE_ACTUAL_VALUE

decision threshold,NOT_AVAILABLE_FROM_REPO,0.5,SUPPORTED,config.py,USE_ACTUAL_VALUE

evaluation metrics,NOT_AVAILABLE_FROM_REPO,"Accuracy, macro P/R/F1, per-class, ROC-AUC, PR-AUC, ECE, Brier, CM",SUPPORTED,metric_definition_audit.csv,USE_ACTUAL_VALUE



## RQ Evidence

rq,evidence,support_status,source,caveat

RQ1 Front vs Side,Front Macro F1 0.76626 vs Side 0.67468; Side gap +0.10775,SUPPORTED_DESCRIPTIVE,main/training/per-class tables,No visual-cause claim without review.

RQ2 Fusion vs best single-view,Fusion Macro F1 0.81113 vs Front 0.76626; cluster CI crosses zero vs Front but not vs Side,SUPPORTED_WITH_STATISTICAL_CAVEAT,main/statistics tables,Point-estimate improvement vs Front.

RQ3 Average vs Adaptive,Identical hard predictions and Macro F1; probabilities differ,SUPPORTED,adaptive/main tables,Adaptive did not change decisions.

Complementarity,Front-only correct=26; Side-only correct=13; both wrong=17,SUPPORTED_DESCRIPTIVE,table_complementarity.csv,Quantitative only.



## Claim Support

claim,support_status,evidence,allowed_wording

Subject-independent split,SUPPORTED,table_split.csv,The manifests use a subject-independent split.

Actual split is 35/8/7 subjects,SUPPORTED,table_split.csv,"The verified subject split is 35 train, 8 validation, 7 test."

Adaptive modifies probabilities although hard predictions are identical,SUPPORTED,adaptive_analysis.csv,Adaptive changes probabilities/calibration metrics but produces identical hard decisions to average.

Adaptive weight distribution relative to equal weighting,SUPPORTED,adaptive_analysis.csv,Adaptive weights are close to equal weighting and bounded by the softmax-confidence formula.

Front/Side quantitative complementarity,SUPPORTED_DESCRIPTIVE,table_complementarity.csv,Front and Side make partly complementary errors.

Occlusion explanations explain failures,NEEDS_MANUAL_VISUAL_REVIEW,qualitative_candidates.csv,Use only as candidate qualitative cases.

Fusion vs Front significant,NOT_SUPPORTED_AS_STRONG_CLAIM,table_statistics.csv,Fusion is a point-estimate improvement; cluster-bootstrap CI crosses zero.

Fusion vs Side cluster CI does not cross zero,SUPPORTED,table_statistics.csv,Fusion improvement over Side is supported by cluster-bootstrap CI above zero.



## Unresolved Items

item,severity,status,needed_action

Separate visual evidence file for RGB1/S31 AC9-AC10 correction,NON_BLOCKING_FOR_METRICS_BUT_WORDING_CARE,NOT_FOUND_IN_REPO,Do not overclaim visual proof.

Interpolation mode in Resize,MINOR_METHOD_DETAIL,NOT_EXPLICIT_IN_REPO,Do not name interpolation unless verified.

DataLoader generator / worker_init_fn / torch.use_deterministic_algorithms,REPRODUCIBILITY_WORDING,NOT_FOUND_IN_EXP18,Do not claim bitwise determinism.

Qualitative visual failure causes,WORDING_RISK,NEEDS_MANUAL_VISUAL_REVIEW,Use qualitative candidates only.

DeLong ROC-AUC test,OPTIONAL,NOT_RUN,Only needed for inferential ROC-AUC claims.

Exp20-22 test-informed exploration,METHODOLOGY_TRANSPARENCY,VERIFIED_CAVEAT,Frame as exploratory controlled follow-up.



## COPY-PASTE PAPER FACT SHEET
```text
Dataset/protocol: subject-independent split 35 train / 8 validation / 7 test subjects. Exp18 stride=30 post-stride per-view counts: train safe=176 phone=908 total=1084; validation safe=34 phone=191 total=225; test safe=40 phone=180 total=220. Front/Side identities match after sampling. RGB1=Side, RGB2=Front. Labels: safe_driving=0, phone_use=1, positive class=phone_use.

Correction: RGB1/S31 AC9-AC10 correction is implemented at config/manifest level; separate visual proof file was not found.

Preprocessing: RGB conversion, Resize(224,224), train HFlip default p=0.5, Front rotation=68 and ColorJitter(brightness=1.2, contrast=1.2, saturation=1.2, hue=0 default); Side rotation=45 and ColorJitter(brightness=0.8, contrast=0.8, saturation=0.8, hue=0 default), ToTensor, ImageNet Normalize. Val/test: Resize, ToTensor, Normalize. Interpolation not explicit. No TTA found.

Architecture/training: EfficientNetV2-S timm tf_efficientnetv2_s, pretrained ImageNet=True, classifier Dropout -> Linear(...,2), CrossEntropyLoss, AdamW, batch=32, max_epochs=30. Front LR=3e-5 WD=5e-4 dropout=0.4 freeze=5 checkpoint=val_macro_f1 max. Side LR=2e-5 WD=1e-3 dropout=0.4 freeze=4 checkpoint=val_loss min. Class weights=[2.5,1.0], gamma=1.0.

Adaptive repair: implementation uses exp(abs(p-0.5)) softmax confidence, not linear abs normalization. Max recomputation error=0.0. Front weight stats={'mean': 0.5126, 'std': 0.03914, 'median': 0.51096, 'q1': 0.48638, 'q3': 0.53951, 'min': 0.41105, 'max': 0.61037}. Side weight stats={'mean': 0.4874, 'std': 0.03914, 'median': 0.48904, 'q1': 0.46049, 'q3': 0.51362, 'min': 0.38963, 'max': 0.58895}. Counts={'front_weight_0_45_to_0_55_count': 173, 'front_weight_0_40_to_0_60_count': 219, 'front_weight_gt_0_60_count': 1, 'front_weight_lt_0_40_count': 0}. Exp18 and Exp23 seed42 reconcile: max weight diff=0.0.

Results: Front Macro F1=0.76626; Side Macro F1=0.67468; Average Fusion Macro F1=0.81113; Adaptive Fusion Macro F1=0.81113. Average and Adaptive hard predictions/confusion matrix identical: [[25,15],[8,172]].

Training behavior: Front train/val F1=0.69929/0.72581 gap=-0.02652. Side train/val F1=0.79013/0.68238 gap=+0.10775, overfit-risk pattern descriptively stronger.

Statistics: cluster bootstrap B=10000, n_clusters=7. Fusion vs Front is point-estimate improvement but CI crosses zero. Fusion vs Side CI does not cross zero. Zero-exceedance p-values are reported as finite-resample bounds, not p=0.

Caveats: Exp20-22 exploratory/test-informed; qualitative visual explanations require manual inspection; no bitwise determinism claim.
```

## Final Consistency Repair Notes
- Post-stride counts canonicalized from table_split.csv: train safe/phone/total=176/908/1084; val=34/191/225; test=40/180/220 per view.
- Adaptive weight std standardized to population standard deviation, ddof=0, to match Exp23 aggregate convention.
- Exact ColorJitter call: transforms.ColorJitter(brightness=jit, contrast=jit, saturation=jit); local signature confirms hue default is 0.
