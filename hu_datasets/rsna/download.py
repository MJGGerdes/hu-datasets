import os
import zipfile
import shutil
from collections import Counter
from pathlib import Path

import pandas as pd
from loguru import logger
from tqdm import tqdm
import gdown

URL = "https://drive.google.com/file/d/1FaWb6Kq7GRBu9J5EvoBNIDqNMMG_46W5/view?usp=drive_link"

CLASS_MAPPING = {
    "No Lung Opacity / Not Normal": "no_opacity",
    "Lung Opacity": "lung_opacity",
    "Normal": "normal"
}

def download_zip(zip_path: Path):
    if not zip_path.exists():
        logger.info("Downloading dataset with gdown...")
        gdown.download(URL, output=str(zip_path), fuzzy=True, quiet=False)
    else:
        logger.info("Zipfile already exists. Skipping download.")

def extract_zip(zip_path: Path, extract_dir: Path):
    logger.info("extract_zip...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        relevant_files = [f for f in zip_ref.namelist() if "stage2_train_metadata.csv" in f or f.endswith(".png")]

        for file in tqdm(relevant_files, desc="Extracting"):
            zip_ref.extract(file, extract_dir)


def prepare_dataframe(extract_dir: Path) -> pd.DataFrame:
    csv_path = next(extract_dir.rglob("stage2_train_metadata.csv"), None)
    assert csv_path, "Could not find stage_2_detailed_class_info.csv"
    logger.info(f"Reading CSV: {csv_path}")
    df = pd.read_csv(csv_path)
    logger.info(f"Total rows in csv: {len(df)}")

    logger.info("Removing duplicate patient IDs, preferring those with Target == 1...")
    if 'Target' in df.columns:
        df = df.sort_values('Target', ascending=False).drop_duplicates('patientId')
    else:
        logger.warning("Target column not found. Duplicates will be removed arbitrarily.")
        df = df.drop_duplicates('patientId')

    logger.info(f"Unique patientIds remaining: {len(df)}")
    return df

def reorder_images(extract_dir: Path, output_dir: Path) -> Counter:
    
    csv_path = next(extract_dir.rglob("stage2_train_metadata.csv"), None)
    assert csv_path, "Could not find stage_2_detailed_class_info.csv"
    logger.info(f"Reading CSV: {csv_path}")
    df = pd.read_csv(csv_path)
    logger.info(f"Total rows in csv: {len(df)}")

    logger.info("Removing duplicate patient IDs, preferring those with Target == 1...")
    if 'Target' in df.columns:
        df = df.sort_values('Target', ascending=False).drop_duplicates('patientId')
    else:
        logger.warning("Target column not found. Duplicates will be removed arbitrarily.")
        df = df.drop_duplicates('patientId')

    logger.info(f"Unique patientIds remaining: {len(df)}")
    
    # Create output directories for each class
    for folder in CLASS_MAPPING.values():
        (output_dir / folder).mkdir(exist_ok=True)

    image_dir = extract_dir / "stage_2_train_images"
    class_counter = Counter()

    logger.info("Moving images to class folders...")
    for _, row in tqdm(df.iterrows(), total=len(df)):
        patient_id = row['patientId']
        class_name = row['class']
        dst_folder = CLASS_MAPPING.get(class_name, "unknown")

        src_path = image_dir / f"{patient_id}.png"
        dst_path = output_dir / dst_folder / f"{patient_id}.png"

        if src_path.exists():
            shutil.move(str(src_path), str(dst_path))
            class_counter[dst_folder] += 1
        else:
            logger.warning(f"File not found: {src_path}")

    return class_counter

def print_stats(class_counter: Counter):
    logger.info("Image distribution summary:")
    for cls, count in class_counter.items():
        logger.info(f"{cls}: {count} images")

def cleanup_zip(zip_path: Path):
    if zip_path.exists():
        zip_path.unlink()
        logger.info("Zipfile removed after successful processing.")

def download_and_prepare_rsna(dataset_path: Path):
    
    dataset_path.mkdir(parents=True, exist_ok=True)
    
    zip_file = dataset_path / "rsna_dataset.zip"
    #extract_dir = path / "rsna_dataset"
    #output_dir = path / "rsna_sorted"

    download_zip(zip_file)
    extract_zip(zip_file, dataset_path)
    df = prepare_dataframe(dataset_path)
    counter = reorder_images(extract_dir, output_dir)
    # print_stats(counter)
    #cleanup_zip(zip_path)
    logger.success("Done.")

if __name__ == "__main__":
    
    current_file_path = Path(__file__)
    download_directory = current_file_path.parent.parent.parent / "data/rsna"
    logger.info(f"Download directory is: {download_directory.absolute()}")
    download_and_prepare_rsna(download_directory)
