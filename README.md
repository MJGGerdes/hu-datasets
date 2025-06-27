# datasets
Repository for downloading datasets. Project related to my thesis.

# CLEVR 

This project uses a subset of the [CLEVR dataset](https://cs.stanford.edu/people/jcjohns/clevr/).


## Original CLEVR Dataset

The full dataset consists of:

- A training set of **70000 images**
- A validation set of **15000 images**
- A test set of **15000 images**
- **Questions and answers** for training and validation sets
- **Scene graph annotations** for training and validation images, providing:
  - Ground-truth **locations** of objects
  - Object **attributes** (e.g., color, size, material)
  - **Relationships** between objects

## Limited data setup

Since this project focuses on limited data, the following steps are applied:

1. The original **CLEVR_v1.0.zip** is downloaded from the official source.
2. Only the **training set images** and corresponding **scene annotations** are extracted.
3. The number of objects per image is determined based on the `CLEVR_train_scenes.json` file.
4. Subfolders are created for each **unique object count** (e.g., `3`, `4`, ..., `10`).
5. Images are **moved to the correct subfolder** based on the number of objects in the image.
6. The **original ZIP file** is deleted to save space.
7. The **temporary extraction directory** is removed after processing.


# RSNA Pneumonia Detection

This project uses a subset of [RSNA Pneumonia Detection Challenge dataset](https://www.kaggle.com/datasets/iamtapendu/rsna-pneumonia-processed-dataset). This dataset enhanced the original dataset by converting the images in DICOM format to PNG format.

## Original RSNA Dataset

The full dataset consists of:
- A training set of **24124 images**
- A validation set of **2560 images**


## Limited data setup

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

# TACO Dataset downloader and preprocessor

A simplified version of the [TACO dataset](http://tacodataset.org/), focusing only on images that contain **exactly one annotated object**.

## What it does

1. **Create Dataset Directory**  
   Ensures the dataset directory (passed as parameter) exists.

2. **Load `annotations.json`**
   - If the file doesn't exist in the dataset folder, it is copied from the current source directory.

3. **Parse Annotations**
   - Extracts `images`, `categories`, and `annotations`.
   - Creates a mapping of `category_id` to `supercategory`.
   - Creates a mapping of `image_id` to its annotations.

4. **Filter**
   - Keeps only images that contain **exactly one object** (i.e., one annotation).
   - Combines each valid image with:
     - Its `file_name`
     - Its `flickr_url`
     - The supercategory of the object it contains

5. **Download Images**
   - Downloads each valid image from its `flickr_url` (if not already downloaded).
   - Saves the image in a folder named after its supercategory.
   - The file is saved using only the image filename (e.g., `000006.jpg` instead of `batch_1/000006.jpg`).



