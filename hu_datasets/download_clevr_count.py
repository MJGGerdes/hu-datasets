import json
import shutil
import zipfile
from pathlib import Path

import wget
from loguru import logger
from tqdm import tqdm
from .utils import (delete_dir, delete_zip, is_already_downloaded,
                   register_is_downloaded)

ANNOTATION_FILE = "annotations.json"
CLEVR_BASE = "CLEVR_v1.0"
SCENES_FILE = "scenes/CLEVR_train_scenes.json"

URL = "https://dl.fbaipublicfiles.com/clevr/CLEVR_v1.0.zip"


def download_zip(dataset_path: Path):
    zip_path = dataset_path / Path(URL).name
    logger.info(f"Location downloaded zipfile: {zip_path}")
    if zip_path.exists():
        logger.info("Zip already exists")
        return

    logger.info("Downloading dataset...")
    try:
        filename = wget.download(URL, out=str(zip_path))
        logger.info(f"File downloaded: {filename}")
    except Exception as e:
        logger.info(f"An error occurred: {e}")


def extract_zip(dataset_path: Path):
    zip_path = dataset_path / Path(URL).name
    print(f"Extract zip: {zip_path}")
    
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        relevant_files = [
            f for f in zip_ref.namelist() if SCENES_FILE in f or "images/train" in f
        ]

        for file in tqdm(relevant_files, desc="Extracting"):
            zip_ref.extract(file, dataset_path)
            if SCENES_FILE in file:
                break


def reorder_images(dataset_path: Path):
    scene_path = dataset_path / CLEVR_BASE / SCENES_FILE
    # Load scenes from JSON

    with open(scene_path, "r") as f:
        scenes_json = json.loads(f.read())

        scenes = scenes_json["scenes"]
        # Each image is specified including it's objects on the images, so we can count them
        image_objects = {
            scene["image_filename"]: len(scene["objects"]) for scene in scenes
        }

        unique_counts = set(image_objects.values())
        # Create subdirectories for count_value, so this will be the class label of the image
        for count in unique_counts:
            label_dir = Path(dataset_path / str(count))
            logger.info(f"Create subfolder for count items: {count}")
            (label_dir).mkdir(exist_ok=True)
        logger.info(f"Total images in dataset: {len(image_objects.keys())}")
        for file_name, count in image_objects.items():
            image_full_path = dataset_path / CLEVR_BASE / "images/train" / file_name
            if Path(image_full_path).exists():
                # Create the destination for the file: use only the name itself instead of the full path
                dst_path = dataset_path / str(count) / Path(file_name).name
                shutil.move(str(image_full_path), str(dst_path))


def cleanup_files(root_path: Path):
    zip_file = root_path / Path(URL).name
    #delete_zip(zip_file)
    old_dir = root_path / CLEVR_BASE
    delete_dir(old_dir)


def download_and_prepare_clevr_count(dataset_path: Path) -> None:
    dataset_path.mkdir(parents=True, exist_ok=True)
    if not is_already_downloaded(dataset_path):
        download_zip(dataset_path)
        extract_zip(dataset_path)
        reorder_images(dataset_path)
        cleanup_files(dataset_path)
        register_is_downloaded(dataset_path)
    else:
        logger.info(f"{dataset_path} already downloaded!")


if __name__ == "__main__":
    current_file_path = Path(__file__)
    download_directory = current_file_path.parent / "data/clevr_count"
    logger.info(f"Download directory is: {download_directory.absolute()}")
    download_and_prepare_clevr_count(download_directory)
    
    #TODO:   image = Image.open(img_path).convert("RGB")?????? 
