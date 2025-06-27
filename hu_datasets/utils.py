from enum import Enum
from pathlib import Path
import shutil
from loguru import logger

CHECK_FILE = "downloaded.txt"

def is_already_downloaded(dataset_path: Path):
    check_path = dataset_path / CHECK_FILE
    if check_path.exists():
        return True
    return False

def register_is_downloaded(dataset_path: Path):
    check_path = dataset_path / CHECK_FILE
    check_path.write_bytes(b"Download finished!")
    logger.success(f"Done! dataset {dataset_path} is ready for use!")
    
def delete_zip(zip_file: Path):
    if zip_file.exists():
        zip_file.unlink()
        logger.info(f"Zipfile {zip_file} removed after successful processing.")
    else:
        logger.info(f"Zipfile {zip_file} could not be removed.")
        
        
def delete_dir(dir_path):
    if dir_path.exists():
        shutil.rmtree(dir_path)
        logger.info(f"{dir_path} directory removed.")
    else:
        logger.info(f"Directory {dir_path} could not be removed.")