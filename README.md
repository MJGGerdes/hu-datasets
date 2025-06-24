# datasets
Repository for downloading datasets





# TACO Dataset downloader and preprocessor

This script downloads and prepares a simplified version of the [TACO dataset](http://tacodataset.org/), focusing only on images that contain **exactly one annotated object**.

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



