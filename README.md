# datasets
Repository for downloading datasets.


# RSNA Pneumonia Detection downloader and preprocessor

This script automates the process of downloading, extracting, cleaning, and organizing the [RSNA Pneumonia Detection Challenge dataset](https://www.kaggle.com/datasets/iamtapendu/rsna-pneumonia-processed-dataset).

## What It Does

1. **Download**
   - Downloads the dataset zip file from a Google Drive link (via `gdown`) if not already present.

2. **Extract**
   - Extracts only the relevant files:
     - `stage2_train_metadata.csv`
     - All image files in `Training/Images/`

3. **Process CSV**
   - Reads the metadata CSV.
   - Removes duplicate patient IDs, prioritizing rows where `Target == 1`.

4. **Reorganize Images**
   - Moves each image into a folder based on its class label:
     - `"No Lung Opacity / Not Normal"` → `no_opacity/`
     - `"Lung Opacity"` → `lung_opacity/`
     - `"Normal"` → `normal/`

5. **Clean up**
   - Removes the old `Training/` directory (optional).
   - Optionally removes the downloaded zip file (commented out).



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



