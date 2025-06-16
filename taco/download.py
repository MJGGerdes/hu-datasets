'''
This script downloads TACO's images from Flickr given an annotation json file
Code written by Pedro F. Proenza, 2019, adjusted for my configuration
'''

import os.path
import argparse
import json
from PIL import Image
import requests
from io import BytesIO
import sys
from pathlib import Path
from loguru import logger

def download_and_prepare_taco():
    current_file_path = Path(__file__)
    base_directory = current_file_path.parent.parent
    logger.info(f"Base directory is: {base_directory.absolute()}")
    
    annotations_dir = Path(base_directory / "dataset/taco/annotations.json").resolve()
        
    dataset_dir = os.path.dirname(annotations_dir)
    
    logger.info('Note. If for any reason the connection is broken. Just call me again and I will start where I left.')
    
    logger.info(f'Load annotations from file {annotations_dir}')
    with open(annotations_dir, 'r') as f:
        annotations = json.loads(f.read())
    
        nr_images = len(annotations['images'])
        for i in range(nr_images):
    
            image = annotations['images'][i]
    
            file_name = image['file_name']
            url_original = image['flickr_url']
            url_resized = image['flickr_640_url']
    
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
            logger.info("%s[%s%s] - %i/%i\r" % ('Loading: ', "=" * x, "." * (bar_size - x), i, nr_images))
            sys.stdout.flush()
            i+=1
    
        logger.info('Finished downlaoding images')
