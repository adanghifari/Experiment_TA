"""
Konfigurasi terpusat untuk pipeline eksperimen.

Semua path, mapping view, dan mapping label didefinisikan di sini SEKALI SAJA.
Script lain (build_manifest, dataset, training) mengimpor dari sini agar tidak
ada risiko salah asumsi (mis. RGB1/RGB2 tertukar) tersebar di banyak file.
"""

import os
from pathlib import Path

# --------------------------------------------------------------------------
# Path dasar proyek
# --------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = Path(os.environ.get("DRIVER_DATA_RAW_DIR", r"D:\Skripsi\Experiment_TA\data\raw"))
MANIFEST_DIR = PROJECT_ROOT.parent / "data"
CHECKPOINT_DIR = PROJECT_ROOT / "checkpoints"
RESULTS_DIR = PROJECT_ROOT / "results"
# --------------------------------------------------------------------------
# Output default per view
# --------------------------------------------------------------------------
FRONT_CHECKPOINT_PATH = CHECKPOINT_DIR / "front" / "best.pt"
SIDE_CHECKPOINT_PATH = CHECKPOINT_DIR / "side" / "best.pt"
FRONT_HISTORY_PATH = RESULTS_DIR / "front" / "history.json"
SIDE_HISTORY_PATH = RESULTS_DIR / "side" / "history.json"
FRONT_SUMMARY_PATH = RESULTS_DIR / "front" / "train_summary.json"
SIDE_SUMMARY_PATH = RESULTS_DIR / "side" / "train_summary.json"

# --------------------------------------------------------------------------
# Default training yang perlu diaudit per eksperimen
# --------------------------------------------------------------------------
CHECKPOINT_MONITOR_FRONT = 'val_macro_f1'
CHECKPOINT_MONITOR_SIDE = 'val_macro_f1'
CLASS_WEIGHT_GAMMA_FRONT = 1.0
# Gamma hanya memengaruhi bobot kelas pada CrossEntropyLoss; tidak dipakai pada average/adaptive fusion.
CLASS_WEIGHT_GAMMA_SIDE = 1.0

MANIFEST_FULL_PATH = MANIFEST_DIR / "manifest_full.csv"       # semua 16 kelas
MANIFEST_BINARY_PATH = MANIFEST_DIR / "manifest_binary.csv"   # hanya A1 + A5-A9
MANIFEST_PAIRED_PATH = MANIFEST_DIR / "manifest_paired.csv"   # pasangan front-side tersinkronisasi
MANIFEST_SPLIT_PATH = MANIFEST_DIR / "manifest_split.csv"     # manifest_binary + kolom split

# --------------------------------------------------------------------------
# Mapping folder RGB -> sudut pandang (view)
# Mapping view: RGB1 = side view, RGB2 = front view
# --------------------------------------------------------------------------
VIEW_FOLDER_MAP = {
    "RGB1": "side",
    "RGB2": "front",
}

# --------------------------------------------------------------------------
# Mapping kelas aktivitas 3MDAD (AC1..AC16) ke label biner
# Mapping kelas untuk setup biner:
#   A1        -> safe_driving      (label 0)
#   A5 - A9   -> phone_use         (label 1)
#   lainnya   -> tidak digunakan (di-drop saat filtering ke manifest_binary)
# --------------------------------------------------------------------------
ACTIVITY_LABEL_NAMES = {
    1: "safe_driving",
    2: "doing_hair_makeup",
    3: "adjusting_radio",
    4: "gps_operating",
    5: "writing_message_right",
    6: "writing_message_left",
    7: "talking_phone_right",
    8: "talking_phone_left",
    9: "having_picture",
    10: "talking_passenger",
    11: "singing_dancing",
    12: "fatigue_somnolence",
    13: "drinking_right",
    14: "drinking_left",
    15: "reaching_behind",
    16: "smoking",
}

SAFE_DRIVING_CLASSES = {1}
PHONE_USE_CLASSES = {5, 6, 7, 8, 9}
BINARY_CLASSES = SAFE_DRIVING_CLASSES | PHONE_USE_CLASSES

# --------------------------------------------------------------------------
# Koreksi metadata yang diketahui (known data issues)
# --------------------------------------------------------------------------
# Bug folder AC9/AC10 tertukar untuk subjek S31 pernah dilaporkan komunitas
# untuk modalitas Depth (lihat: github.com/kevinsu628/3MDAD, catatan
# "side_view_day_data/Depth1/S31/AC10 and AC9 should be swapped"). Verifikasi
# visual manual pada RGB mengonfirmasi swap yang sama terjadi pada RGB1
# (side view) untuk subjek ini. Isi folder AC9 sebenarnya AC10, dan
# sebaliknya. Dikoreksi di level manifest (bukan rename file mentah) agar
# hasil tetap konsisten jika dataset di-extract ulang.
#
# Format: (view, subject_id) -> {activity_id_di_folder: activity_id_sebenarnya}
KNOWN_ACTIVITY_CORRECTIONS = {
    ("side", 31): {9: 10, 10: 9},
}

BINARY_LABEL_MAP = {
    "safe_driving": 0,
    "phone_use": 1,
}


def activity_id_to_binary_label(activity_id: int):
    """Kembalikan nama label biner ('safe_driving'/'phone_use') atau None jika
    activity_id tidak termasuk kelas yang dipakai di eksperimen ini."""
    if activity_id in SAFE_DRIVING_CLASSES:
        return "safe_driving"
    if activity_id in PHONE_USE_CLASSES:
        return "phone_use"
    return None


# --------------------------------------------------------------------------
# Parameter split subject-based
# --------------------------------------------------------------------------
N_SUBJECTS_TOTAL = 50
SPLIT_SEED = 42
SPLIT_RATIOS = {"train": 0.70, "val": 0.15, "test": 0.15}

# --------------------------------------------------------------------------
# Parameter preprocessing & training (Bab 3)
# --------------------------------------------------------------------------
IMAGE_SIZE = 224
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

MODEL_NAME = "tf_efficientnetv2_s"      # identifier timm untuk EfficientNetV2-S
PRETRAINED = True
LOSS_FUNCTION = 'CrossEntropyLoss'
BATCH_SIZE = 32
LEARNING_RATE_FRONT = 0.000005
LEARNING_RATE_SIDE = 0.000005
DROPOUT_FRONT = 0.6
DROPOUT_SIDE = 0.6
EARLY_STOPPING_PATIENCE_FRONT = 5
EARLY_STOPPING_PATIENCE_SIDE = 5
MAX_EPOCHS = 30
DECISION_THRESHOLD = 0.5

# Konfigurasi eksperimen
WEIGHT_DECAY = 0.01
WEIGHT_DECAY_FRONT = 0.01
WEIGHT_DECAY_SIDE = 0.01
NUM_STAGES_TO_FREEZE_FRONT = 5
NUM_STAGES_TO_FREEZE_SIDE = 3
LABEL_SMOOTHING = 0.1
CLASS_WEIGHTS = [5.15, 1.0]
LR_SCHEDULER_FACTOR = 0.5
LR_SCHEDULER_PATIENCE_FRONT = 2
LR_SCHEDULER_PATIENCE_SIDE = 2

# Intensitas augmentasi training
# Front view
AUG_ROTATION_DEGREE_FRONT = 20
AUG_COLOR_JITTER_FACTOR_FRONT = 0.4

# Side view
AUG_ROTATION_DEGREE_SIDE = 20
AUG_COLOR_JITTER_FACTOR_SIDE = 0.4

# --------------------------------------------------------------------------
# Frame subsampling
# Ambil 1 dari setiap FRAME_STRIDE frame per sekuens untuk mengurangi
# redundansi temporal pada video 30Hz. Diterapkan pada SEMUA split
# (train/val/test) agar konsisten. Formula: (frame - 1) % FRAME_STRIDE == 0
# menghasilkan frame ke-1, 6, 11, 16, ... (selalu dimulai dari frame pertama).
# Set ke 1 untuk menonaktifkan subsampling (pakai semua frame).
# --------------------------------------------------------------------------
FRAME_STRIDE = 15

# Preset CLI opsional. Runner standar tidak memakai preset ini.
EXPERIMENT_CONFIGS = {}
SEED_TRAINING = True
SORT_DATAFRAME = False
SORT_PAIRED = False
EXPERIMENT_NAME = 'experiment_7'






