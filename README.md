# datasets
Repository for downloading datasets. Project related to my thesis.

<p align="center">
  <a href="#clevr-dataset"><strong>CLEVR dataset</strong></a> &nbsp;|&nbsp;
  <a href="#rsna-pneumonia-detection"><strong>RSNA dataset</strong></a> &nbsp;|&nbsp;
  <a href="#taco"><strong>TACO dataset</strong></a> &nbsp;|&nbsp;
  <a href="#cifar10"><strong>CIFAR10 dataset</strong></a> &nbsp;|&nbsp;
  <a href="#trashnet"><strong>Trashnet dataset</strong></a>
</p>


## CLEVR dataset 
[🔝 Back to top](#datasets)

This project uses a subset of the [CLEVR dataset](https://cs.stanford.edu/people/jcjohns/clevr/).


### Original CLEVR Dataset

The full dataset consists of:

- A training set of **70000 images**
- A validation set of **15000 images**
- A test set of **15000 images**
- **Questions and answers** for training and validation sets
- **Scene graph annotations** for training and validation images, providing:
  - Ground-truth **locations** of objects
  - Object **attributes** (e.g., color, size, material)
  - **Relationships** between objects

### Data setup

Since this project focuses on limited data, the following steps are applied:

1. The original **CLEVR_v1.0.zip** is downloaded from the official source.
2. Only the **training set images** and corresponding **scene annotations** are extracted.
3. The number of objects per image is determined based on the `CLEVR_train_scenes.json` file.
4. Subfolders are created for each **unique object count** (e.g., `3`, `4`, ..., `10`).
5. Images are **moved to the correct subfolder** based on the number of objects in the image.
6. The **original ZIP file** is deleted to save space.
7. The **temporary extraction directory** is removed after processing.


## RSNA Pneumonia Detection 
[🔝 Back to top](#datasets)

This project uses a subset of [RSNA Pneumonia Detection Challenge dataset](https://www.kaggle.com/datasets/iamtapendu/rsna-pneumonia-processed-dataset). This dataset enhanced the original dataset by converting the images in DICOM format to PNG format.

### Original RSNA Dataset

The full dataset consists of:
- A training set of **24124 images**
- A validation set of **2560 images**


### Data setup

Since this project focuses on limited data and the structure will follow the ImageFolder dataset structure, the following steps are applied :


1. The dataset ZIP file is downloaded from a Google Drive link using `gdown` if it doesn't already exist.
2. Only the necessary files are extracted:
   - `stage2_train_metadata.csv`
   - All image files in `Training/Images/`
3. The metadata CSV is processed by removing duplicate patient IDs, keeping entries where `Target == 1`.
4. Images are moved into subfolders based on their class label:
   - `"No Lung Opacity / Not Normal"` → `no_opacity/`
   - `"Lung Opacity"` → `lung_opacity/`
   - `"Normal"` → `normal/`
5. The original `Training/` folder is deleted.
6. The downloaded ZIP file is removed.

## TACO 
[🔝 Back to top](#datasets)

A simplified version of the [TACO dataset](http://tacodataset.org/), focusing only on images that contain **exactly one annotated object**.

### Original TACO Dataset

- Set of 1500 images
- Annotations which label images in 60 categories which belong to 28 super (top) categories.
- Multi object images


### Data setup

Since this project focusses on only single-object images, the following steps are applied:

1. `annotations.json` is loaded from the dataset directory or copied from the source if missing.
2. Annotations are parsed to extract `images`, `categories`, and `annotations`.
3. A mapping is created from `category_id` to `supercategory`, and from `image_id` to its annotations.
4. Only images with **exactly one object** are kept, and paired with their `file_name`, `flickr_url`, and supercategory.
5. Each valid image is downloaded (if not already present) and saved in a folder named after its supercategory, using only the image filename.


## CIFAR10 
[🔝 Back to top](#datasets)

A simplified version of the [TACO dataset](http://tacodataset.org/), focusing only on images that contain **exactly one annotated object**.

### Original TACO Dataset

- A training set of **50000 images**
- A test set of **10000 images**


### Data setup

Since this project focusses on only single-object images, the following steps are applied:

1. Only the test set is downloaded.


## Trashnet 
[🔝 Back to top](#datasets)


The trashnet dataset is used: https://github.com/garythung/trashnet?tab=readme-ov-file

### Original Trashnet Dataset

- A set of **2527 images**


### Data setup

1. The dataset ZIP file is downloaded from a Google Drive link using `gdown` if it doesn't already exist.
2. All files are extracted. The classes are subfolders already, so nothing to adjust there.

