# Checkpoint and model-health audit

## 1. Scope

Read-only audit of artifacts under D:\Skripsi\Experiment_TA. The historical repository D:\Skripsi\Experiment was not accessed. No retraining, new inference, source modification, checkpoint modification, paper modification, overwrite, or Git commit was performed. Only existing histories, summaries, metadata, checkpoint files, and test metric artifacts were read; this report and audit figures were created.

## 2. Artifact verification

| run | protocol | criterion | selected epoch | hash matches summary | checkpoint SHA-256 |
|---|---|---|---|---|---|
| Front original | Original experiment_18 | val_macro_f1/max | 9 | YES | 1e8036ddb330649d7e51a7dc56cc697c915fb44a7e9873abb7dd440062b6ba35 |
| Front standardized val-loss | experiment_18_standardized_checkpoint_val_loss | val_loss/min | 12 | YES | 16d0f46c6e75a295c5ca18f3a2d8258420ce99f1ee359d5392e58e63efd2181b |
| Side original | Original experiment_18 | val_loss/min | 26 | YES | a37aedc2a5f5c3a02877a370ac67964663a409789134b949966d6c52802023fc |
| Side standardized val-loss | experiment_18_standardized_checkpoint_val_loss | val_loss/min | 26 | YES | a3494d74bdfac0ca2de936b5b1dfb7197312fc0bd4891b56166235f34421f7a9 |
| Front standardized Macro-F1 | experiment_18_standardized_checkpoint_selection | val_macro_f1/max | 9 | YES | 5dc3aec44d17dd23cb9296d9a95d09564ccbd60528ccef85d3dacbb7ecbcc2f6 |
| Side standardized Macro-F1 | experiment_18_standardized_checkpoint_selection | val_macro_f1/max | 15 | YES | 0264b6c81744c65aee5dfdb18fe6943bda2b5fc04f727b63acb42334b0f52712 |

The full two-view standardized-Macro-F1 candidate is experiment_18_standardized_checkpoint_selection. Its resolved config, Front/Side histories, train summaries, test metric artifacts, physical checkpoints, and matching SHA-256 values are present. The Side-only archive candidate was not needed for the primary comparison.

## 3. Metric definitions

loss_gap = val_loss - train_loss at the same epoch. abs_loss_gap = absolute value of loss_gap. checkpoint_improvement is reconstructed from history using strict max/min direction. train_macro_f1 is used only because it is already stored in history; no train-set inference was run. Test Macro F1 is an independent outcome and is not used as model-health evidence.

## 4. Front original health

Assessment: **POSSIBLE OVERFITTING SIGNAL**.
Train loss turun terus setelah epoch 9, validation loss membaik sampai epoch 12 lalu naik pada epoch 13, dan loss gap naik dari 0.04383 pada checkpoint ke 0.13310 pada epoch terakhir.
Selected epoch 9 by val_macro_f1/max; executed epochs 13.
Minimum validation loss: epoch 12 (0.50961); maximum validation Macro F1: epoch 9 (0.72581); minimum absolute gap: epoch 2 (0.01137); maximum gap: epoch 13 (0.13310); final epoch 13.
Gap statistics: mean 0.04410, median 0.04053, min -0.05601, max 0.13310, mean absolute 0.05447, final 0.13310; first >0.05: 10; first >0.10: 11.
Trajectory: train loss start/selected/end = 0.68932/0.47353/0.38726; validation loss start/minimum/selected/end = 0.63331/0.50961/0.51736/0.52036; validation Macro F1 start/maximum/selected/end = 0.57331/0.72581/0.72581/0.71666; gap start/selected/end = -0.05601/0.04383/0.13310.

Local checkpoint window:
| epoch | train_loss | val_loss | loss_gap | val_macro_f1 | learning_rate |
|---|---|---|---|---|---|
| 6 | 0.50284 | 0.54337 | 0.04053 | 0.69549 | 0.00003000 |
| 7 | 0.50961 | 0.52457 | 0.01496 | 0.71596 | 0.00003000 |
| 8 | 0.48857 | 0.52586 | 0.03729 | 0.70060 | 0.00003000 |
| 9 | 0.47353 | 0.51736 | 0.04383 | 0.72581 | 0.00003000 |
| 10 | 0.44571 | 0.53340 | 0.08769 | 0.68375 | 0.00003000 |
| 11 | 0.41193 | 0.51456 | 0.10263 | 0.72000 | 0.00001500 |
| 12 | 0.41722 | 0.50961 | 0.09239 | 0.71892 | 0.00001500 |

Figures: [loss](figures/model_health/front_original_loss.png), [loss-gap](figures/model_health/front_original_loss_gap.png).

Complete per-epoch health table:


| epoch | train_loss | val_loss | loss_gap | abs_loss_gap | val_macro_f1 | train_macro_f1 | learning_rate | checkpoint_improvement | selected_checkpoint |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.68932 | 0.63331 | -0.05601 | 0.05601 | 0.57331 | 0.50305 | 0.00003000 | YES | NO |
| 2 | 0.62853 | 0.61716 | -0.01137 | 0.01137 | 0.60011 | 0.54428 | 0.00003000 | YES | NO |
| 3 | 0.59312 | 0.61332 | 0.02020 | 0.02020 | 0.64747 | 0.55390 | 0.00003000 | YES | NO |
| 4 | 0.54896 | 0.59023 | 0.04127 | 0.04127 | 0.64845 | 0.61574 | 0.00003000 | YES | NO |
| 5 | 0.52988 | 0.55668 | 0.02680 | 0.02680 | 0.65328 | 0.63962 | 0.00003000 | YES | NO |
| 6 | 0.50284 | 0.54337 | 0.04053 | 0.04053 | 0.69549 | 0.70085 | 0.00003000 | YES | NO |
| 7 | 0.50961 | 0.52457 | 0.01496 | 0.01496 | 0.71596 | 0.66568 | 0.00003000 | YES | NO |
| 8 | 0.48857 | 0.52586 | 0.03729 | 0.03729 | 0.70060 | 0.68505 | 0.00003000 | NO | NO |
| 9 | 0.47353 | 0.51736 | 0.04383 | 0.04383 | 0.72581 | 0.69929 | 0.00003000 | YES | YES |
| 10 | 0.44571 | 0.53340 | 0.08769 | 0.08769 | 0.68375 | 0.74887 | 0.00003000 | NO | NO |
| 11 | 0.41193 | 0.51456 | 0.10263 | 0.10263 | 0.72000 | 0.74970 | 0.00001500 | NO | NO |
| 12 | 0.41722 | 0.50961 | 0.09239 | 0.09239 | 0.71892 | 0.76318 | 0.00001500 | NO | NO |
| 13 | 0.38726 | 0.52036 | 0.13310 | 0.13310 | 0.71666 | 0.76779 | 0.00000750 | NO | NO |

## 5. Front standardized-val-loss health

Assessment: **POSSIBLE OVERFITTING SIGNAL**.
Validation loss minimum pada epoch 12; sesudahnya naik, train loss tetap turun, dan loss gap mencapai 0.13310 pada epoch terakhir.
Selected epoch 12 by val_loss/min; executed epochs 13.
Minimum validation loss: epoch 12 (0.50961); maximum validation Macro F1: epoch 9 (0.72581); minimum absolute gap: epoch 2 (0.01137); maximum gap: epoch 13 (0.13310); final epoch 13.
Gap statistics: mean 0.04410, median 0.04053, min -0.05601, max 0.13310, mean absolute 0.05447, final 0.13310; first >0.05: 10; first >0.10: 11.
Trajectory: train loss start/selected/end = 0.68932/0.41722/0.38726; validation loss start/minimum/selected/end = 0.63331/0.50961/0.50961/0.52036; validation Macro F1 start/maximum/selected/end = 0.57331/0.72581/0.71892/0.71666; gap start/selected/end = -0.05601/0.09239/0.13310.

Local checkpoint window:
| epoch | train_loss | val_loss | loss_gap | val_macro_f1 | learning_rate |
|---|---|---|---|---|---|
| 9 | 0.47353 | 0.51736 | 0.04383 | 0.72581 | 0.00003000 |
| 10 | 0.44571 | 0.53340 | 0.08769 | 0.68375 | 0.00003000 |
| 11 | 0.41193 | 0.51456 | 0.10263 | 0.72000 | 0.00001500 |
| 12 | 0.41722 | 0.50961 | 0.09239 | 0.71892 | 0.00001500 |
| 13 | 0.38726 | 0.52036 | 0.13310 | 0.71666 | 0.00000750 |

Figures: [loss](figures/model_health/front_std_val_loss_loss.png), [loss-gap](figures/model_health/front_std_val_loss_loss_gap.png).

Complete per-epoch health table:


| epoch | train_loss | val_loss | loss_gap | abs_loss_gap | val_macro_f1 | train_macro_f1 | learning_rate | checkpoint_improvement | selected_checkpoint |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.68932 | 0.63331 | -0.05601 | 0.05601 | 0.57331 | 0.50305 | 0.00003000 | YES | NO |
| 2 | 0.62853 | 0.61716 | -0.01137 | 0.01137 | 0.60011 | 0.54428 | 0.00003000 | YES | NO |
| 3 | 0.59312 | 0.61332 | 0.02020 | 0.02020 | 0.64747 | 0.55390 | 0.00003000 | YES | NO |
| 4 | 0.54896 | 0.59023 | 0.04127 | 0.04127 | 0.64845 | 0.61574 | 0.00003000 | YES | NO |
| 5 | 0.52988 | 0.55668 | 0.02680 | 0.02680 | 0.65328 | 0.63962 | 0.00003000 | YES | NO |
| 6 | 0.50284 | 0.54337 | 0.04053 | 0.04053 | 0.69549 | 0.70085 | 0.00003000 | YES | NO |
| 7 | 0.50961 | 0.52457 | 0.01496 | 0.01496 | 0.71596 | 0.66568 | 0.00003000 | YES | NO |
| 8 | 0.48857 | 0.52586 | 0.03729 | 0.03729 | 0.70060 | 0.68505 | 0.00003000 | NO | NO |
| 9 | 0.47353 | 0.51736 | 0.04383 | 0.04383 | 0.72581 | 0.69929 | 0.00003000 | YES | NO |
| 10 | 0.44571 | 0.53340 | 0.08769 | 0.08769 | 0.68375 | 0.74887 | 0.00003000 | NO | NO |
| 11 | 0.41193 | 0.51456 | 0.10263 | 0.10263 | 0.72000 | 0.74970 | 0.00001500 | YES | NO |
| 12 | 0.41722 | 0.50961 | 0.09239 | 0.09239 | 0.71892 | 0.76318 | 0.00001500 | YES | YES |
| 13 | 0.38726 | 0.52036 | 0.13310 | 0.13310 | 0.71666 | 0.76779 | 0.00000750 | NO | NO |

## 6. Side original health

Assessment: **NO CLEAR OVERFITTING SIGNAL**.
Validation loss membaik sampai epoch 26 lalu hanya berosilasi pada sisa epoch; gap positif besar dicatat sebagai fakta, bukan diagnosis tunggal.
Selected epoch 26 by val_loss/min; executed epochs 30.
Minimum validation loss: epoch 26 (0.50217); maximum validation Macro F1: epoch 15 (0.75724); minimum absolute gap: epoch 6 (0.00472); maximum gap: epoch 29 (0.11361); final epoch 30.
Gap statistics: mean 0.04820, median 0.05763, min -0.06799, max 0.11361, mean absolute 0.05820, final 0.10480; first >0.05: 11; first >0.10: 22.
Trajectory: train loss start/selected/end = 0.68783/0.39480/0.39814; validation loss start/minimum/selected/end = 0.61984/0.50217/0.50217/0.50294; validation Macro F1 start/maximum/selected/end = 0.45783/0.75724/0.68238/0.70060; gap start/selected/end = -0.06799/0.10737/0.10480.

Local checkpoint window:
| epoch | train_loss | val_loss | loss_gap | val_macro_f1 | learning_rate |
|---|---|---|---|---|---|
| 23 | 0.41379 | 0.51441 | 0.10062 | 0.68684 | 0.00000250 |
| 24 | 0.40627 | 0.51341 | 0.10714 | 0.67510 | 0.00000125 |
| 25 | 0.40850 | 0.50241 | 0.09391 | 0.68684 | 0.00000125 |
| 26 | 0.39480 | 0.50217 | 0.10737 | 0.68238 | 0.00000125 |
| 27 | 0.42705 | 0.50756 | 0.08051 | 0.67086 | 0.00000063 |
| 28 | 0.41742 | 0.50466 | 0.08724 | 0.68983 | 0.00000063 |
| 29 | 0.40019 | 0.51380 | 0.11361 | 0.66667 | 0.00000063 |

Figures: [loss](figures/model_health/side_original_loss.png), [loss-gap](figures/model_health/side_original_loss_gap.png).

Complete per-epoch health table:


| epoch | train_loss | val_loss | loss_gap | abs_loss_gap | val_macro_f1 | train_macro_f1 | learning_rate | checkpoint_improvement | selected_checkpoint |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.68783 | 0.61984 | -0.06799 | 0.06799 | 0.45783 | 0.51503 | 0.00002000 | YES | NO |
| 2 | 0.66351 | 0.61456 | -0.04895 | 0.04895 | 0.45122 | 0.50487 | 0.00002000 | YES | NO |
| 3 | 0.62094 | 0.61117 | -0.00977 | 0.00977 | 0.47671 | 0.52726 | 0.00002000 | YES | NO |
| 4 | 0.61543 | 0.60593 | -0.00950 | 0.00950 | 0.45255 | 0.54298 | 0.00002000 | YES | NO |
| 5 | 0.60473 | 0.59085 | -0.01388 | 0.01388 | 0.45783 | 0.56949 | 0.00002000 | YES | NO |
| 6 | 0.57667 | 0.58139 | 0.00472 | 0.00472 | 0.45652 | 0.59157 | 0.00001000 | YES | NO |
| 7 | 0.56428 | 0.57795 | 0.01367 | 0.01367 | 0.58836 | 0.58905 | 0.00001000 | YES | NO |
| 8 | 0.56642 | 0.57338 | 0.00696 | 0.00696 | 0.53354 | 0.60596 | 0.00001000 | YES | NO |
| 9 | 0.54957 | 0.56865 | 0.01908 | 0.01908 | 0.62212 | 0.63911 | 0.00001000 | YES | NO |
| 10 | 0.54512 | 0.56729 | 0.02217 | 0.02217 | 0.71715 | 0.62075 | 0.00001000 | YES | NO |
| 11 | 0.50576 | 0.56054 | 0.05478 | 0.05478 | 0.71447 | 0.65306 | 0.00001000 | YES | NO |
| 12 | 0.53423 | 0.54875 | 0.01452 | 0.01452 | 0.74270 | 0.64151 | 0.00001000 | YES | NO |
| 13 | 0.49931 | 0.55967 | 0.06036 | 0.06036 | 0.71241 | 0.65973 | 0.00001000 | NO | NO |
| 14 | 0.51615 | 0.53427 | 0.01812 | 0.01812 | 0.73666 | 0.64368 | 0.00001000 | YES | NO |
| 15 | 0.48501 | 0.53991 | 0.05490 | 0.05490 | 0.75724 | 0.70578 | 0.00001000 | NO | NO |
| 16 | 0.48325 | 0.53097 | 0.04772 | 0.04772 | 0.72282 | 0.67023 | 0.00001000 | YES | NO |
| 17 | 0.46293 | 0.52459 | 0.06166 | 0.06166 | 0.73468 | 0.71876 | 0.00001000 | YES | NO |
| 18 | 0.43267 | 0.51556 | 0.08289 | 0.08289 | 0.74572 | 0.75228 | 0.00000500 | YES | NO |
| 19 | 0.44828 | 0.51429 | 0.06601 | 0.06601 | 0.70533 | 0.74876 | 0.00000500 | YES | NO |
| 20 | 0.42200 | 0.50778 | 0.08578 | 0.08578 | 0.72282 | 0.76351 | 0.00000500 | YES | NO |
| 21 | 0.42589 | 0.50681 | 0.08092 | 0.08092 | 0.68983 | 0.75345 | 0.00000250 | YES | NO |
| 22 | 0.40914 | 0.51567 | 0.10653 | 0.10653 | 0.67799 | 0.78061 | 0.00000250 | NO | NO |
| 23 | 0.41379 | 0.51441 | 0.10062 | 0.10062 | 0.68684 | 0.74524 | 0.00000250 | NO | NO |
| 24 | 0.40627 | 0.51341 | 0.10714 | 0.10714 | 0.67510 | 0.76351 | 0.00000125 | NO | NO |
| 25 | 0.40850 | 0.50241 | 0.09391 | 0.09391 | 0.68684 | 0.75457 | 0.00000125 | YES | NO |
| 26 | 0.39480 | 0.50217 | 0.10737 | 0.10737 | 0.68238 | 0.79013 | 0.00000125 | YES | YES |
| 27 | 0.42705 | 0.50756 | 0.08051 | 0.08051 | 0.67086 | 0.75911 | 0.00000063 | NO | NO |
| 28 | 0.41742 | 0.50466 | 0.08724 | 0.08724 | 0.68983 | 0.73287 | 0.00000063 | NO | NO |
| 29 | 0.40019 | 0.51380 | 0.11361 | 0.11361 | 0.66667 | 0.74998 | 0.00000063 | NO | NO |
| 30 | 0.39814 | 0.50294 | 0.10480 | 0.10480 | 0.70060 | 0.75783 | 0.00000031 | NO | NO |

## 7. Side Macro-F1 candidate health

Assessment: **POSSIBLE OVERFITTING SIGNAL**.
Validation Macro F1 maksimum pada epoch 15, tetapi validation loss membaik hingga epoch 20 dan loss gap meningkat dari 0.05490 menjadi 0.08578.
Selected epoch 15 by val_macro_f1/max; executed epochs 30.
Minimum validation loss: epoch 26 (0.50217); maximum validation Macro F1: epoch 15 (0.75724); minimum absolute gap: epoch 6 (0.00472); maximum gap: epoch 29 (0.11361); final epoch 30.
Gap statistics: mean 0.04820, median 0.05763, min -0.06799, max 0.11361, mean absolute 0.05820, final 0.10480; first >0.05: 11; first >0.10: 22.
Trajectory: train loss start/selected/end = 0.68783/0.48501/0.39814; validation loss start/minimum/selected/end = 0.61984/0.50217/0.53991/0.50294; validation Macro F1 start/maximum/selected/end = 0.45783/0.75724/0.75724/0.70060; gap start/selected/end = -0.06799/0.05490/0.10480.

Local checkpoint window:
| epoch | train_loss | val_loss | loss_gap | val_macro_f1 | learning_rate |
|---|---|---|---|---|---|
| 12 | 0.53423 | 0.54875 | 0.01452 | 0.74270 | 0.00001000 |
| 13 | 0.49931 | 0.55967 | 0.06036 | 0.71241 | 0.00001000 |
| 14 | 0.51615 | 0.53427 | 0.01812 | 0.73666 | 0.00001000 |
| 15 | 0.48501 | 0.53991 | 0.05490 | 0.75724 | 0.00001000 |
| 16 | 0.48325 | 0.53097 | 0.04772 | 0.72282 | 0.00001000 |
| 17 | 0.46293 | 0.52459 | 0.06166 | 0.73468 | 0.00001000 |
| 18 | 0.43267 | 0.51556 | 0.08289 | 0.74572 | 0.00000500 |

Figures: [loss](figures/model_health/side_std_f1_loss.png), [loss-gap](figures/model_health/side_std_f1_loss_gap.png).

Complete per-epoch health table:


| epoch | train_loss | val_loss | loss_gap | abs_loss_gap | val_macro_f1 | train_macro_f1 | learning_rate | checkpoint_improvement | selected_checkpoint |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.68783 | 0.61984 | -0.06799 | 0.06799 | 0.45783 | 0.51503 | 0.00002000 | YES | NO |
| 2 | 0.66351 | 0.61456 | -0.04895 | 0.04895 | 0.45122 | 0.50487 | 0.00002000 | NO | NO |
| 3 | 0.62094 | 0.61117 | -0.00977 | 0.00977 | 0.47671 | 0.52726 | 0.00002000 | YES | NO |
| 4 | 0.61543 | 0.60593 | -0.00950 | 0.00950 | 0.45255 | 0.54298 | 0.00002000 | NO | NO |
| 5 | 0.60473 | 0.59085 | -0.01388 | 0.01388 | 0.45783 | 0.56949 | 0.00002000 | NO | NO |
| 6 | 0.57667 | 0.58139 | 0.00472 | 0.00472 | 0.45652 | 0.59157 | 0.00001000 | NO | NO |
| 7 | 0.56428 | 0.57795 | 0.01367 | 0.01367 | 0.58836 | 0.58905 | 0.00001000 | YES | NO |
| 8 | 0.56642 | 0.57338 | 0.00696 | 0.00696 | 0.53354 | 0.60596 | 0.00001000 | NO | NO |
| 9 | 0.54957 | 0.56865 | 0.01908 | 0.01908 | 0.62212 | 0.63911 | 0.00001000 | YES | NO |
| 10 | 0.54512 | 0.56729 | 0.02217 | 0.02217 | 0.71715 | 0.62075 | 0.00001000 | YES | NO |
| 11 | 0.50576 | 0.56054 | 0.05478 | 0.05478 | 0.71447 | 0.65306 | 0.00001000 | NO | NO |
| 12 | 0.53423 | 0.54875 | 0.01452 | 0.01452 | 0.74270 | 0.64151 | 0.00001000 | YES | NO |
| 13 | 0.49931 | 0.55967 | 0.06036 | 0.06036 | 0.71241 | 0.65973 | 0.00001000 | NO | NO |
| 14 | 0.51615 | 0.53427 | 0.01812 | 0.01812 | 0.73666 | 0.64368 | 0.00001000 | NO | NO |
| 15 | 0.48501 | 0.53991 | 0.05490 | 0.05490 | 0.75724 | 0.70578 | 0.00001000 | YES | YES |
| 16 | 0.48325 | 0.53097 | 0.04772 | 0.04772 | 0.72282 | 0.67023 | 0.00001000 | NO | NO |
| 17 | 0.46293 | 0.52459 | 0.06166 | 0.06166 | 0.73468 | 0.71876 | 0.00001000 | NO | NO |
| 18 | 0.43267 | 0.51556 | 0.08289 | 0.08289 | 0.74572 | 0.75228 | 0.00000500 | NO | NO |
| 19 | 0.44828 | 0.51429 | 0.06601 | 0.06601 | 0.70533 | 0.74876 | 0.00000500 | NO | NO |
| 20 | 0.42200 | 0.50778 | 0.08578 | 0.08578 | 0.72282 | 0.76351 | 0.00000500 | NO | NO |
| 21 | 0.42589 | 0.50681 | 0.08092 | 0.08092 | 0.68983 | 0.75345 | 0.00000250 | NO | NO |
| 22 | 0.40914 | 0.51567 | 0.10653 | 0.10653 | 0.67799 | 0.78061 | 0.00000250 | NO | NO |
| 23 | 0.41379 | 0.51441 | 0.10062 | 0.10062 | 0.68684 | 0.74524 | 0.00000250 | NO | NO |
| 24 | 0.40627 | 0.51341 | 0.10714 | 0.10714 | 0.67510 | 0.76351 | 0.00000125 | NO | NO |
| 25 | 0.40850 | 0.50241 | 0.09391 | 0.09391 | 0.68684 | 0.75457 | 0.00000125 | NO | NO |
| 26 | 0.39480 | 0.50217 | 0.10737 | 0.10737 | 0.68238 | 0.79013 | 0.00000125 | NO | NO |
| 27 | 0.42705 | 0.50756 | 0.08051 | 0.08051 | 0.67086 | 0.75911 | 0.00000063 | NO | NO |
| 28 | 0.41742 | 0.50466 | 0.08724 | 0.08724 | 0.68983 | 0.73287 | 0.00000063 | NO | NO |
| 29 | 0.40019 | 0.51380 | 0.11361 | 0.11361 | 0.66667 | 0.74998 | 0.00000063 | NO | NO |
| 30 | 0.39814 | 0.50294 | 0.10480 | 0.10480 | 0.70060 | 0.75783 | 0.00000031 | NO | NO |

## 8. Front standardized-Macro-F1 reference

Assessment: **POSSIBLE OVERFITTING SIGNAL**.
Validation Macro F1 maksimum pada epoch 9, validation loss minimum pada epoch 12, dan loss gap meningkat dari 0.04383 menjadi 0.13310 pada epoch 13.
Selected epoch 9 by val_macro_f1/max; executed epochs 13.
Minimum validation loss: epoch 12 (0.50961); maximum validation Macro F1: epoch 9 (0.72581); minimum absolute gap: epoch 2 (0.01137); maximum gap: epoch 13 (0.13310); final epoch 13.
Gap statistics: mean 0.04410, median 0.04053, min -0.05601, max 0.13310, mean absolute 0.05447, final 0.13310; first >0.05: 10; first >0.10: 11.
Trajectory: train loss start/selected/end = 0.68932/0.47353/0.38726; validation loss start/minimum/selected/end = 0.63331/0.50961/0.51736/0.52036; validation Macro F1 start/maximum/selected/end = 0.57331/0.72581/0.72581/0.71666; gap start/selected/end = -0.05601/0.04383/0.13310.

Local checkpoint window:
| epoch | train_loss | val_loss | loss_gap | val_macro_f1 | learning_rate |
|---|---|---|---|---|---|
| 6 | 0.50284 | 0.54337 | 0.04053 | 0.69549 | 0.00003000 |
| 7 | 0.50961 | 0.52457 | 0.01496 | 0.71596 | 0.00003000 |
| 8 | 0.48857 | 0.52586 | 0.03729 | 0.70060 | 0.00003000 |
| 9 | 0.47353 | 0.51736 | 0.04383 | 0.72581 | 0.00003000 |
| 10 | 0.44571 | 0.53340 | 0.08769 | 0.68375 | 0.00003000 |
| 11 | 0.41193 | 0.51456 | 0.10263 | 0.72000 | 0.00001500 |
| 12 | 0.41722 | 0.50961 | 0.09239 | 0.71892 | 0.00001500 |

Figures: [loss](figures/model_health/front_std_f1_loss.png), [loss-gap](figures/model_health/front_std_f1_loss_gap.png).

Complete per-epoch health table:


| epoch | train_loss | val_loss | loss_gap | abs_loss_gap | val_macro_f1 | train_macro_f1 | learning_rate | checkpoint_improvement | selected_checkpoint |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.68932 | 0.63331 | -0.05601 | 0.05601 | 0.57331 | 0.50305 | 0.00003000 | YES | NO |
| 2 | 0.62853 | 0.61716 | -0.01137 | 0.01137 | 0.60011 | 0.54428 | 0.00003000 | YES | NO |
| 3 | 0.59312 | 0.61332 | 0.02020 | 0.02020 | 0.64747 | 0.55390 | 0.00003000 | YES | NO |
| 4 | 0.54896 | 0.59023 | 0.04127 | 0.04127 | 0.64845 | 0.61574 | 0.00003000 | YES | NO |
| 5 | 0.52988 | 0.55668 | 0.02680 | 0.02680 | 0.65328 | 0.63962 | 0.00003000 | YES | NO |
| 6 | 0.50284 | 0.54337 | 0.04053 | 0.04053 | 0.69549 | 0.70085 | 0.00003000 | YES | NO |
| 7 | 0.50961 | 0.52457 | 0.01496 | 0.01496 | 0.71596 | 0.66568 | 0.00003000 | YES | NO |
| 8 | 0.48857 | 0.52586 | 0.03729 | 0.03729 | 0.70060 | 0.68505 | 0.00003000 | NO | NO |
| 9 | 0.47353 | 0.51736 | 0.04383 | 0.04383 | 0.72581 | 0.69929 | 0.00003000 | YES | YES |
| 10 | 0.44571 | 0.53340 | 0.08769 | 0.08769 | 0.68375 | 0.74887 | 0.00003000 | NO | NO |
| 11 | 0.41193 | 0.51456 | 0.10263 | 0.10263 | 0.72000 | 0.74970 | 0.00001500 | NO | NO |
| 12 | 0.41722 | 0.50961 | 0.09239 | 0.09239 | 0.71892 | 0.76318 | 0.00001500 | NO | NO |
| 13 | 0.38726 | 0.52036 | 0.13310 | 0.13310 | 0.71666 | 0.76779 | 0.00000750 | NO | NO |

## 9. Loss-gap comparison

| run | selected gap | selected abs gap | mean gap | median gap | min gap | max gap | mean abs gap | final gap | first >0.05 | first >0.10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Front original | 0.04383 | 0.04383 | 0.04410 | 0.04053 | -0.05601 | 0.13310 | 0.05447 | 0.13310 | 10 | 11 |
| Front standardized val-loss | 0.09239 | 0.09239 | 0.04410 | 0.04053 | -0.05601 | 0.13310 | 0.05447 | 0.13310 | 10 | 11 |
| Side original | 0.10737 | 0.10737 | 0.04820 | 0.05763 | -0.06799 | 0.11361 | 0.05820 | 0.10480 | 11 | 22 |
| Side standardized val-loss | 0.10737 | 0.10737 | 0.04820 | 0.05763 | -0.06799 | 0.11361 | 0.05820 | 0.10480 | 11 | 22 |
| Front standardized Macro-F1 | 0.04383 | 0.04383 | 0.04410 | 0.04053 | -0.05601 | 0.13310 | 0.05447 | 0.13310 | 10 | 11 |
| Side standardized Macro-F1 | 0.05490 | 0.05490 | 0.04820 | 0.05763 | -0.06799 | 0.11361 | 0.05820 | 0.10480 | 11 | 22 |

A positive loss gap is a recorded train/validation relationship; it is not by itself an overfitting diagnosis.

## 10. Checkpoint-window comparison

The local windows are reported in each run section. Front Macro-F1 selection is epoch 9 and Front val-loss selection is epoch 12. Side Macro-F1 selection is epoch 15 and Side val-loss selection is epoch 26. These are descriptive positions in the recorded trajectories, not causal explanations.

## 11. Overfit/underfit assessment

Front runs receive POSSIBLE OVERFITTING SIGNAL because train loss continues falling while late validation loss/gap deteriorates. Side val-loss runs receive NO CLEAR OVERFITTING SIGNAL because validation loss reaches its minimum late and then oscillates over the remaining epochs, although their positive gaps are relatively large. Side Macro-F1 selection receives POSSIBLE OVERFITTING SIGNAL because selection precedes later validation-loss improvement and the gap increases afterward. No run is labeled STRONG OVERFITTING SIGNAL or POSSIBLE UNDERFITTING SIGNAL from these artifacts.

## 12. Original vs standardized comparison
### Front

Under the recorded runs, original and standardized-Macro-F1 Front select epoch 9 with validation Macro F1 0.72581 and loss gap 0.04383. Standardized-val-loss Front selects epoch 12 with validation loss 0.50961, validation Macro F1 0.71892, and loss gap 0.09239. The latter has lower validation loss by its criterion and a larger selected gap; this does not establish superiority.
### Side

Original and standardized-val-loss Side select epoch 26 with validation loss 0.50217, validation Macro F1 0.68238, and loss gap 0.10738. Verified standardized-Macro-F1 Side selects epoch 15 with validation Macro F1 0.75724, validation loss 0.53991, and loss gap 0.05490. This is a descriptive comparison across recorded runs, not a causal claim.

## 13. Training-health vs test-outcome distinction

Test Macro F1 may be listed in the summary table as an outcome, but it is not used to claim that a model is healthy, not overfit, more generalizable, or that one criterion is better.

Summary table:


| model/run | criterion | selected epoch | train loss | val loss | loss gap | val Macro F1 | train Macro F1 | F1 gap | test Macro F1 | health assessment |
|---|---|---|---|---|---|---|---|---|---|---|
| Front original | val_macro_f1/max | 9 | 0.47353 | 0.51736 | 0.04383 | 0.72581 | 0.69929 | -0.02652 | 0.76626 | POSSIBLE OVERFITTING SIGNAL |
| Front standardized val-loss | val_loss/min | 12 | 0.41722 | 0.50961 | 0.09239 | 0.71892 | 0.76318 | 0.04426 | 0.77256 | POSSIBLE OVERFITTING SIGNAL |
| Side original | val_loss/min | 26 | 0.39480 | 0.50217 | 0.10737 | 0.68238 | 0.79013 | 0.10775 | 0.67468 | NO CLEAR OVERFITTING SIGNAL |
| Side standardized val-loss | val_loss/min | 26 | 0.39480 | 0.50217 | 0.10737 | 0.68238 | 0.79013 | 0.10775 | 0.67468 | NO CLEAR OVERFITTING SIGNAL |
| Front standardized Macro-F1 | val_macro_f1/max | 9 | 0.47353 | 0.51736 | 0.04383 | 0.72581 | 0.69929 | -0.02652 | 0.76626 | POSSIBLE OVERFITTING SIGNAL |
| Side standardized Macro-F1 | val_macro_f1/max | 15 | 0.48501 | 0.53991 | 0.05490 | 0.75724 | 0.70578 | -0.05146 | 0.63045 | POSSIBLE OVERFITTING SIGNAL |


## 14. FACT

Original Front selected epoch 9 by validation Macro F1; original Side selected epoch 26 by validation loss. Standardized-val-loss selected Front epoch 12 and Side epoch 26 by validation loss. Verified standardized-Macro-F1 selected Front epoch 9 and Side epoch 15 by validation Macro F1. Train Macro F1 is present in all audited histories. Front selected gap is 0.04383 for Macro-F1 selection versus 0.09239 for val-loss selection. Side selected gap is 0.10738 for val-loss selection versus 0.05490 for Macro-F1 selection. Original and standardized-val-loss Side histories and checkpoint hash match in the audited artifacts.

## 15. INTERPRETATION

The curves support a limited descriptive interpretation: criteria select different positions in the validation trajectory. Front Macro-F1 selection precedes the validation-loss minimum; Side Macro-F1 selection also precedes the later validation-loss minimum. Loss-gap evidence supports different observed view-specific checkpoint behavior only PARTIALLY: the selected positions and gaps differ, but artifacts do not establish causality, superiority, or historical rationale.

## 16. LIMITATIONS

These are recorded runs, not a new causal experiment. Loss gaps can reflect regularization, augmentation, class weighting, dropout, and train/validation construction. Test metrics are not health evidence. No new inference was run to fill missing metrics. The audit does not infer why a criterion was originally chosen.

## Required final summary

FRONT ORIGINAL:
criterion: val_macro_f1/max
selected epoch: 9
train loss: 0.47353
val loss: 0.51736
loss gap: 0.04383
val Macro F1: 0.72581
health assessment: POSSIBLE OVERFITTING SIGNAL

FRONT STANDARDIZED VAL-LOSS:
criterion: val_loss/min
selected epoch: 12
train loss: 0.41722
val loss: 0.50961
loss gap: 0.09239
val Macro F1: 0.71892
health assessment: POSSIBLE OVERFITTING SIGNAL

SIDE ORIGINAL:
criterion: val_loss/min
selected epoch: 26
train loss: 0.39480
val loss: 0.50217
loss gap: 0.10737
val Macro F1: 0.68238
health assessment: NO CLEAR OVERFITTING SIGNAL

SIDE STANDARDIZED MACRO-F1:
criterion: val_macro_f1/max
selected epoch: 15
train loss: 0.48501
val loss: 0.53991
loss gap: 0.05490
val Macro F1: 0.75724
health assessment: POSSIBLE OVERFITTING SIGNAL

SIDE MACRO-F1 CANDIDATE: AVAILABLE

FRONT HEALTH DIFFERENCE: Under the recorded runs, val-loss selection moves from epoch 9 to epoch 12, lowers validation loss from 0.51736 to 0.50961, and increases selected loss gap from 0.04383 to 0.09239; descriptive only.

SIDE HEALTH DIFFERENCE: Under the recorded runs, val-loss selection is later (epoch 26 vs epoch 15), has lower validation loss (0.50217 vs 0.53991), and a larger selected gap (0.10738 vs 0.05490).

DOES LOSS-GAP EVIDENCE SUPPORT DIFFERENT VIEW-SPECIFIC CHECKPOINT BEHAVIOR: PARTIALLY SUPPORTED
reason: Recorded trajectories show different criterion-selected positions and selected gaps, but not causality or superiority.

FACT: Sections 2, 4-9, and 14 are computed from stored histories and metadata.

INTERPRETATION: Health categories are cautious interpretations of joint train/validation behavior, not causal explanations.

LIMITATIONS: No retraining, new inference, source modification, manuscript modification, or Git commit.
