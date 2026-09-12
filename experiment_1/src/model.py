"""EfficientNetV2-S single-logit model untuk konfigurasi eksperimen biner."""

import logging

import timm
import torch.nn as nn

from src.config import DROPOUT_FRONT, MODEL_NAME

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


def build_model(pretrained=True, num_stages_to_freeze=0, dropout_rate=None):
    if dropout_rate is None:
        dropout_rate = DROPOUT_FRONT
    backbone = timm.create_model(MODEL_NAME, pretrained=pretrained, num_classes=0)
    in_features = backbone.num_features
    classifier = nn.Sequential(nn.Dropout(p=dropout_rate), nn.Linear(in_features, 1))
    model = _EfficientNetBinary(backbone, classifier)
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    log.info("Model: %s | Total params: %s | Trainable: %s", MODEL_NAME, f"{total_params:,}", f"{trainable_params:,}")
    return model


class _EfficientNetBinary(nn.Module):
    def __init__(self, backbone, classifier):
        super().__init__()
        self.backbone = backbone
        self.classifier = classifier

    def forward(self, x):
        features = self.backbone(x)
        return self.classifier(features).squeeze(1)

