import json
from collections import defaultdict
from io import BytesIO
from pathlib import Path
import wget
import requests
from loguru import logger
from PIL import Image
from tqdm import tqdm
import zipfile
import shutil
from DatasetDownloader import is_already_downloaded

ANNOTATION_FILE = "annotations.json"

URL = "https://dl.fbaipublicfiles.com/clevr/CLEVR_v1.0.zip"




def download_zip(dataset_path: Path):
    zip_path = dataset_path / Path(URL).name 
    logger.info(f"Location downloaded zipfile: {zip_path}")
    if zip_path.exists():
        logger.info(f"Zip already exists")
        return
    
    logger.info("Downloading dataset...")
    try:
        filename = wget.download(URL, out=str(zip_path))
        print(f"File downloaded: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")


def extract_zip(dataset_path: Path):
    zip_path = dataset_path / Path(URL).name 
    print(f"Extract zip: {zip_path}")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        relevant_files = [
            f
            for f in zip_ref.namelist()
            if "train_scenes.json" in f or "images/train" in f
        ]

        for file in tqdm(relevant_files, desc="Extracting"):
            zip_ref.extract(file, dataset_path)
            
def reorder_images(dataset_path: Path):
    scene_path = "dataset/clevr/CLEVR_v1.0/scenes/CLEVR_train_scenes.json"
    # Load scenes from JSON
    scenes = json.load(open(scene_path))["scenes"]
    # Each image is specified including it's objects on the images, so we can count them
    image_objects = {scene["image_filename"]: len(scene["objects"]) for scene in scenes}
    
    unique_counts = set(image_objects.values())
    # Create subdirectories for count_value, so this will be the class label of the image
    for count in unique_counts:
        (dataset_path / count).mkdir(exist_ok=True)
        
    logger.info(f"Total images in dataset: {len(image_objects.keys())}")
    for image_object in image_objects:
        
        image = image_object[0]
        count = image_object[1]
        if Path(image).exists():
            # Create the destination for the file: use only the name itself instead of the full path
            dst_path = dataset_path / count / Path(image).name
            shutil.move(image, str(dst_path))
        
                

def download_and_prepare_clevr_count(dataset_path: Path) -> None:
    logger.info(f"In download_and_prepare_clevr_count with dir: {dataset_path.absolute()}")
    dataset_path.mkdir(parents=True, exist_ok=True)
    
    if not is_already_downloaded(dataset_path):
    
        download_zip(dataset_path)
        extract_zip(dataset_path)
        reorder_images(dataset_path)
        # cleanup_files(dataset_path)
        # logger.success("Done! RSNA dataset is ready for use.")
        



# def count_objects_in_scenes(scenes_json_path):
#     scenes = json.load(open(scenes_json_path))
#     counts = Counter(len(scene["objects"]) for scene in scenes["scenes"])
#     return counts

# self.image_dir = "dataset/clevr/CLEVR_v1.0/images/train"
#         # self.image_dir = "dataset/clevr/images"

#         # Scene file path, describing the images
#         self.scene_path = "dataset/clevr/CLEVR_v1.0/scenes/CLEVR_train_scenes.json"
#         # self.scene_path = "dataset/clevr/scenes/CLEVR_scenes_filtered.json"

#         self.img_dir = Path(self.image_dir)

#         self.filenames, self.labels, self.label_texts = (
#             self.extract_count_labels(self.scene_path, self.image_dir)
#             if countTask
#             else self.extract_distance_labels(self.scene_path)
#         )
#         logger.info(f"Number of images: {len(self.filenames)}")
#         logger.info(f"Number of classes: {len(self.label_texts)}")
        
        
#          # Load scenes from JSON
#         scenes = json.load(open(scene_path))["scenes"]

#         # Mapping imagenames to their object counts
#         # The list of objects is in the scene file, so we can count them
#         count_labels = {s["image_filename"]: len(s["objects"]) for s in scenes}

#         # Create mapping for class labels (should start with 0): for example. 3→0, 4→1, ..., 10→7
#         unique_counts = sorted(set(count_labels.values()))
#         self.count_to_index = {count: idx for idx, count in enumerate(unique_counts)}

#         # Convert count labels to indices
#         count_labels_indexed = {filename: self.count_to_index[count] for filename, count in count_labels.items()}

#         # Create a list of image filenames
#         filenames = list(count_labels_indexed.keys())
#         # Create a list of labels (indices) for the images
#         labels = [count_labels_indexed[fname] for fname in filenames]

#         # Create list of text labels for the labels (like "3 objects", "4 objects", ...)
#         unique_label_texts = [f"{count} objects" for count in unique_counts]

#         return filenames, labels, unique_label_texts


if __name__ == "__main__":
    current_file_path = Path(__file__)
    download_directory = current_file_path.parent / "data/clevr_count"
    logger.info(f"Download directory is: {download_directory.absolute()}")
    download_and_prepare_clevr_count(download_directory)
    
    

