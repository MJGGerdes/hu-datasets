"""
This script downloads TACO's images from Flickr given an annotation json file
Code written by Pedro F. Proenza, 2019, adjusted for my configuration
"""

import json
import os.path
from io import BytesIO
from pathlib import Path

import requests
from loguru import logger
from PIL import Image
from tqdm import tqdm


def download_and_prepare_taco(dataset_path: Path) -> None:

    

    # current_file_path = Path(__file__)
    # base_directory = current_file_path.parent
    logger.info(f"Base directory is: {dataset_path.absolute()}")
    
    annotations_dir = Path(__file__).parent / "annotations.json"
    logger.info(f"Annotations directory is: {annotations_dir.absolute()}")
    if annotations_dir.exists():
        logger.info("Annotations.json found in source directory.")
    
    # download annotations.json from the source directory to the dataset path
    #annotations_dir = Path(base_directory / "annotations.json").resolve()

    download_to_path_annotations = dataset_path / "annotations.json"
    if not download_to_path_annotations.exists():
        logger.info(f"annotations.json not downloaded yet. Downloading from {annotations_dir}")
        try:
            with ( 
                open(annotations_dir, "rb") as src,
                open(download_to_path_annotations, "wb") as dst,
            ):
                dst.write(src.read())
                logger.info("Annotations.json downloaded successfully.")
        except Exception as e:
            logger.error(f"Failed to download annotations.json: {e}")
            return

    logger.info(
        "Note. If for any reason the connection is broken. Just call me again and I will start where I left."
    )


    logger.info(f"Load annotations from file {download_to_path_annotations} to {dataset_path}")
    dataset_dir = os.path.dirname(dataset_path)
    logger.info(f"Dataset download directory is: {dataset_dir}")
    with open(download_to_path_annotations, "r") as f:
        annotations = json.loads(f.read())

        images = annotations["images"]
        nr_images = len(images)

        # Check if all images already are downloaded
        all_exist = True
        for image in images:
            file_name = image["file_name"]
            file_path = os.path.join(dataset_dir, file_name)
            if not os.path.isfile(file_path):
                all_exist = False
                break

        if all_exist:
            logger.info("All images already downloaded. Skipping download.")
            return
        else:
            logger.info("Not all images are downloaded. Proceeding with download.")

        logger.info("Start downloading images")
        logger.info(f"Found {nr_images} images to download")
        for image in tqdm(images, desc="downloading image"):

            file_name = image["file_name"]
            url_original = image["flickr_url"]

            file_path = os.path.join(dataset_dir, file_name)
            logger.info(f"File path: {file_path}")
            # Create subdir if necessary
            subdir = os.path.dirname(file_path)
            if not os.path.isdir(subdir):
                os.mkdir(subdir)

            if not os.path.isfile(file_path):
                # Load and Save Image
                try:
                    response = requests.get(url_original, stream=True, timeout=30)
                    img = Image.open(BytesIO(response.content))
                    img.save(file_path, exif=img.info.get("exif"))
                except requests.exceptions.RequestException as e:
                    logger.error(f"Failed to download {url_original}: {e}")

        logger.info("Finished downloading images")


if __name__ == "__main__":
    current_file_path = Path(__file__)
    download_directory = current_file_path.parent.parent.parent / "data/taco"
    logger.info(f"Download directory is: {download_directory.absolute()}")
    download_and_prepare_taco(download_directory)
