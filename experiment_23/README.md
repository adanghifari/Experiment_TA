# Experiment 23

FINAL robustness validation for the selected main recipe: experiment_18.

This is not hyperparameter tuning. Recipe, split, stride, threshold, checkpoint monitors, augmentation, fusion equations, and all training hyperparameters remain exact experiment_18. Only TRAINING_SEED varies for new runs.

Seeds:
- 42: existing experiment_18 artifacts, no retrain
- 43: standalone retrain from ImageNet pretrained
- 44: standalone retrain from ImageNet pretrained
