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


def download_and_prepare_taco(path):
    download_to_path = Path(path)
    download_to_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"download_to_path directory is: {download_to_path.absolute()}")

    current_file_path = Path(__file__)
    base_directory = current_file_path.parent
    logger.info(f"Base directory is: {base_directory.absolute()}")

    annotations_dir = Path(base_directory / "annotations.json").resolve()

    download_to_path_annotations = download_to_path / "annotations.json"
    if not download_to_path_annotations.exists():
        logger.info(
            f"annotations.json not downloaded yet. Downloading from {annotations_dir}"
        )
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

    logger.info(f"Load annotations from file {download_to_path_annotations}")
    dataset_dir = os.path.dirname(download_to_path_annotations)
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
        for i in range(nr_images):

            image = images[i]

            file_name = image["file_name"]
            url_original = image["flickr_url"]
            url_resized = image["flickr_640_url"]

            file_path = os.path.join(dataset_dir, file_name)
            logger.info(file_path)
            # Create subdir if necessary
            subdir = os.path.dirname(file_path)
            if not os.path.isdir(subdir):
                os.mkdir(subdir)

            if not os.path.isfile(file_path):
                # Load and Save Image
                response = requests.get(url_original)
                img = Image.open(BytesIO(response.content))
                if img._getexif():
                    img.save(file_path, exif=img.info["exif"])
                else:
                    img.save(file_path)

            # Show loading bar
            bar_size = 30
            x = int(bar_size * i / nr_images)
            logger.info(
                "%s[%s%s] - %i/%i\r"
                % ("Loading: ", "=" * x, "." * (bar_size - x), i, nr_images)
            )
            i += 1

        logger.info("Finished downloading images")


if __name__ == "__main__":
    download_and_prepare_taco("data/taco")
