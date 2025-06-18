from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import pydicom
from PIL import Image


def save_dicom_as_resized_png(dcm_path, save_path, size=(224, 224)):
    dcm = pydicom.dcmread(dcm_path)
    img = dcm.pixel_array.astype(np.float32)
    img -= np.min(img)
    img = img / np.max(img) if np.max(img) > 0 else np.zeros_like(img)
    img = cv2.resize(img, size)
    Image.fromarray((img * 255).astype(np.uint8)).save(save_path)


def download_and_prepare_rsna():
    ROOT = Path("/kaggle/input/rsna-pneumonia-detection-challenge")
    IMAGES = ROOT / "stage_2_train_images"
    LABELS_CSV = ROOT / "stage_2_train_labels.csv"
    SAVE_PATH = Path("datasets/rsna/processed")
    POS, NEG = SAVE_PATH / "positive", SAVE_PATH / "negative"

    if POS.exists() and any(POS.glob("*.png")):
        print("RSNA dataset already prepared.")
        return

    print("Preparing RSNA dataset...")
    POS.mkdir(parents=True, exist_ok=True)
    NEG.mkdir(parents=True, exist_ok=True)

    labels = pd.read_csv(LABELS_CSV).drop_duplicates("patientId")

    for _, row in labels.iterrows():
        pid = row["patientId"]
        label = row["Target"]
        dcm_file = IMAGES / f"{pid}.dcm"
        out_dir = POS if label == 1 else NEG
        out_path = out_dir / f"{pid}.png"
        if not out_path.exists():
            try:
                save_dicom_as_resized_png(dcm_file, out_path)
            except Exception as e:
                print(f"Error processing {pid}: {e}")

    print("RSNA dataset ready at", SAVE_PATH)


if __name__ == "__main__":
    download_and_prepare_rsna()
