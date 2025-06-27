import json
from collections import defaultdict
from io import BytesIO
from pathlib import Path

import requests
from loguru import logger
from PIL import Image
from tqdm import tqdm
from DatasetDownloader import is_already_downloaded, register_is_downloaded

ANNOTATION_FILE = "annotations.json"


def download_and_prepare_taco(dataset_path: Path) -> None:
    logger.info(f"In download_and_prepare_taco with dir: {dataset_path.absolute()}")
    dataset_path.mkdir(parents=True, exist_ok=True)

    download_to_path_annotations = get_annotation_file(dataset_path)

    with open(download_to_path_annotations, "r") as f:
        dataset_json = json.loads(f.read())

        # Get 3 main components from the dataset JSON
        categories = dataset_json["categories"]
        # We only use the supercategories and not the categories from the dataset.
        # Each category has a supercategory, which is a higher-level grouping.
        # This is a dictionary mapping category IDs to their supercategories.
        supercategory_lookup = {cat["id"]: cat["supercategory"] for cat in categories}

        images = dataset_json["images"]
        # lookup for image
        image_lookup = {image["id"]: image for image in images}

        logger.info(f"Found {len(images)} images in the original dataset")
        annotations = dataset_json["annotations"]

        # Create dict for each image ->  dict(image_id, list(annotation))
        image_annotation_dict = defaultdict(list)
        for annotation in annotations:
            image_annotation_dict[annotation["image_id"]].append(annotation)

        # Combine everything, so we have the image_id, supercategory and filename, filter on images with one object only
        image_info_dict = {
            image_id: {
                "category": supercategory_lookup[anns[0]["category_id"]],
                "file_name": image_lookup[image_id]["file_name"],
                "url_original": image_lookup[image_id].get("flickr_url"),
            }
            for image_id, anns in image_annotation_dict.items()
            if len(anns) == 1
            and image_id in image_lookup
            and anns[0]["category_id"] in supercategory_lookup
        }

        logger.info("Start downloading images")
        logger.info(f"Found {len(image_info_dict)} images to download")
        for image_info in tqdm(image_info_dict.values(), desc="downloading image"):
            process_image(image_info, dataset_path)
        logger.info("Finished downloading images")


def process_image(image_info: dict, dataset_path: Path) -> None:
    """
    Process the image dictionary to ensure the file name is valid and the image exists.
    If the image file does not exist, it will be downloaded.
    """
    file_name = image_info["file_name"]
    url_original = image_info["url_original"]
    category = image_info["category"]

    # Save image directly to category folder
    destination_dir = dataset_path / category
    # Names of images are for example batch_1/000006.jpg and we only want the imagename itself
    file_path = destination_dir / Path(file_name).name 
    if not file_path.is_file():
        # Create the category directory if it does not exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            response = requests.get(url_original, stream=True, timeout=30)
            img = Image.open(BytesIO(response.content))

            if "exif" in img.info:
                img.save(file_path, exif=img.info["exif"])
            else:
                img.save(file_path)

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download {url_original}: {e}")


def get_annotation_file(dataset_path: Path) -> Path:
    # This function is used to download the annotations.json file from the source directory
    annotations_dir = Path(__file__).parent / ANNOTATION_FILE
    logger.info(f"Annotations directory is: {annotations_dir.absolute()}")
    logger.info(f"Download to directory is: {dataset_path.absolute()}")

    if annotations_dir.exists():
        logger.info("Annotations.json found in source directory.")

    # Check if the annotations.json file already exists in the dataset path
    download_to_path_annotations = dataset_path / ANNOTATION_FILE
    if not download_to_path_annotations.exists():
        logger.info(
            f"annotations.json not downloaded yet. Downloading from {annotations_dir} to {download_to_path_annotations}"
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
        f"Load annotations from file {annotations_dir} to {download_to_path_annotations}"
    )

    return download_to_path_annotations


if __name__ == "__main__":
    current_file_path = Path(__file__)
    download_directory = current_file_path.parent / "data/taco"
    logger.info(f"Download directory is: {download_directory.absolute()}")
    download_and_prepare_taco(download_directory)
