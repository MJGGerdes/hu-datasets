import zipfile
from pathlib import Path

import gdown
from loguru import logger
from tqdm import tqdm

ZIP_FILE = "trashnet.zip"
URL = (
    "https://drive.google.com/file/d/1oJtdbuhJDWD56Rx-WDqJhTTQelXb1T2b/view?usp=sharing"
)


def download_zip(dataset_path: Path):
    zip_path = dataset_path / ZIP_FILE
    if not zip_path.exists():
        logger.info("Downloading dataset with gdown... to {zip_path}")
        gdown.download(URL, output=str(zip_path), fuzzy=True, quiet=False)
    else:
        logger.info("Zipfile already exists. Skipping download.")


def extract_zip(dataset_path: Path):
    logger.info("extract_zip...")
    zip_path = dataset_path / ZIP_FILE
    with zipfile.ZipFile(zip_path, "r") as zip_ref:

        for file in tqdm(zip_ref.namelist(), desc="Extracting zipfile"):
            zip_ref.extract(file, dataset_path)


def download_and_prepare_trashnet(dataset_path: Path):
    dataset_path.mkdir(parents=True, exist_ok=True)
    download_zip(dataset_path)
    extract_zip(dataset_path)


if __name__ == "__main__":

    current_file_path = Path(__file__)
    download_directory = current_file_path.parent / "data/trashnet"
    logger.info(f"Download directory is: {download_directory.absolute()}")
    download_and_prepare_trashnet(download_directory)
