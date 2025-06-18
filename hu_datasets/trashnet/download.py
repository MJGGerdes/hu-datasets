import os
import os.path
import zipfile
from pathlib import Path

from loguru import logger


def download_and_prepare_trashnet(path):
    download_to_path = Path(path)
    download_to_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"download_to_path directory is: {download_to_path.absolute()}")


    current_file_path = Path(__file__)
    base_directory = current_file_path.parent
    logger.info(f"Base directory is: {base_directory.absolute()}")

    zip_path = Path(base_directory / "trashnet.zip").resolve()

    # Target directory to extract to
    extract_dir = download_to_path 

    # Function to check if directory exists and is not empty
    def is_extracted(dir_path):
        return os.path.isdir(dir_path) and len(os.listdir(dir_path)) > 0

    # Only extract if not already done
    if is_extracted(extract_dir):
        print(f"Dataset already extracted at {extract_dir}. Skipping extraction.")
    else:
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
        print(f"Extracted {zip_path} to {extract_dir}")


if __name__ == "__main__":
    download_and_prepare_trashnet("data/trashnet")
