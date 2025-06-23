import shutil
import zipfile
from collections import Counter
from pathlib import Path

import gdown
import pandas as pd
from loguru import logger
from tqdm import tqdm

URL = "https://drive.google.com/file/d/1FaWb6Kq7GRBu9J5EvoBNIDqNMMG_46W5/view?usp=drive_link"

CLASS_MAPPING = {
    "No Lung Opacity / Not Normal": "no_opacity",
    "Lung Opacity": "lung_opacity",
    "Normal": "normal",
}

ZIP_FILE = "rsna_dataset.zip"


def download_zip(dataset_path: Path):
    zip_path = dataset_path / ZIP_FILE
    if not zip_path.exists():
        logger.info("Downloading dataset with gdown...")
        gdown.download(URL, output=str(zip_path), fuzzy=True, quiet=False)
    else:
        logger.info("Zipfile already exists. Skipping download.")


def extract_zip(dataset_path: Path):
    zip_path = dataset_path / ZIP_FILE
    logger.info("extract_zip...all *.png and stage2_train_metadata.csv files will be extracted")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        relevant_files = [
            f
            for f in zip_ref.namelist()
            if "stage2_train_metadata.csv" in f or "Training/Images/" in f
        ]

        for file in tqdm(relevant_files, desc="Extracting"):
            zip_ref.extract(file, dataset_path)


def get_unique_patientIds(extract_dir: Path) -> pd.DataFrame:
    csv_path = next(extract_dir.rglob("stage2_train_metadata.csv"), None)
    assert csv_path, "Could not find stage2_train_metadata.csv"
    logger.info(f"Reading CSV: {csv_path}")
    df = pd.read_csv(csv_path)
    logger.info(f"Total rows in csv: {len(df)}")

    logger.info("Removing duplicate patient IDs, preferring those with Target == 1...")
    if "Target" in df.columns:
        df = df.sort_values("Target", ascending=False).drop_duplicates("patientId")
    else:
        logger.warning(
            "Target column not found. Duplicates will be removed arbitrarily."
        )
        df = df.drop_duplicates("patientId")

    logger.info(f"Unique patientIds remaining: {len(df)}")
    
    return df


def reorder_images(dataset_path: Path) -> None:

    df = get_unique_patientIds(dataset_path)

    # Create subdirectories for each class
    for folder in CLASS_MAPPING.values():
        (dataset_path / folder).mkdir(exist_ok=True)

    logger.info("Moving images to class folders...")
    for _, row in tqdm(df.iterrows(), total=len(df)):
        patient_id = row["patientId"]
        class_name = row["class"]
        dst_folder = CLASS_MAPPING.get(class_name, "unknown")
        dst_path = dataset_path / dst_folder / f"{patient_id}.png"

        src_path = find_file_recursive(dataset_path, f"{patient_id}.png")
        if src_path:
            shutil.move(str(src_path), str(dst_path))
        else:
            logger.warning(f"File not found: {patient_id}.png in {dataset_path}")


def find_file_recursive(root_dir: Path, filename: str) -> Path | None:
    matches = list(root_dir.rglob(filename))
    return matches[0] if matches else None

def cleanup_files(root_path: Path):
    # zip_file = root_path / ZIP_FILE
    # if zip_file.exists():
    #     zip_file.unlink()
    #     logger.info("Zipfile removed after successful processing.")
    old_dir = root_path / "Training"
    if old_dir.exists():
        shutil.rmtree(old_dir)
        logger.info("Old 'Training' directory removed after reordering images.")


def download_and_prepare_rsna(dataset_path: Path) -> None:
    dataset_path.mkdir(parents=True, exist_ok=True)
    download_zip(dataset_path)
    # extract_zip(dataset_path)
    # reorder_images(dataset_path)
    cleanup_files(dataset_path)
    logger.success("Done! RSNA dataset is ready for use.")


if __name__ == "__main__":
    current_file_path = Path(__file__)
    download_directory = current_file_path.parent.parent.parent / "data/rsna"
    logger.info(f"Download directory is: {download_directory.absolute()}")
    download_and_prepare_rsna(download_directory)
