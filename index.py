import re
import constants
import os
import requests
import pandas as pd
import multiprocessing
import time
from time import time as timer
from tqdm import tqdm
import numpy as np
from pathlib import Path
from functools import partial
import requests
import urllib
from PIL import Image
from collections import defaultdict

def download_image(image_link, save_folder, retries=3, delay=3):
    if not isinstance(image_link, str):
        return

    filename = Path(image_link).name
    image_save_path = os.path.join(save_folder, filename)

    if os.path.exists(image_save_path):
        return

    for _ in range(retries):
        try:
            urllib.request.urlretrieve(image_link, image_save_path)
            return
        except:
            time.sleep(delay)

    create_placeholder_image(image_save_path) #Create a black placeholder image for invalid links/images

def create_placeholder_image(image_save_path):
    try:
        placeholder_image = Image.new('RGB', (100, 100), color='black')
        placeholder_image.save(image_save_path)
    except Exception as e:
        return

def download_images(image_links, download_folder, allow_multiprocessing=True):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    if allow_multiprocessing:
        download_image_partial = partial(
            download_image, save_folder=download_folder, retries=3, delay=3)

        with multiprocessing.Pool(64) as pool:
            list(tqdm(pool.imap(download_image_partial, image_links), total=len(image_links)))
            pool.close()
            pool.join()
    else:
        for image_link in tqdm(image_links, total=len(image_links)):
            download_image(image_link, save_folder=download_folder, retries=3, delay=3)

def save_images_in_entity_folders(data,datatype):
    grps = defaultdict(list)
    for i,r in data.iterrows():
        image_link = r['image_link']
        entity_name = r['entity_name']
        grps[entity_name].append(image_link)

    for e,i in grps.items():
        save_folder = f'/home/eshan/Eshan/CodeLinux/AmazonML2024/Code/Dataset/{datatype}/{e}'
        os.makedirs(save_folder, exist_ok=True)
        # img = i.split('/')[-1]
        # img_save_path = os.path.join(save_folder, img)
        # if not os.path.exists(img_save_path):
        download_images(i,save_folder)

def save_images(data, datatype):
    t = []
    save_folder = '/home/eshan/Eshan/CodeLinux/AmazonML2024/Code/Dataset/test2'
    for i,r in data.iterrows():
        image_link = r['image_link']
        entity_name = r['entity_name']
        t.append(image_link)
    download_images(t,save_folder)

dataTrain = pd.read_csv('/home/eshan/Eshan/CodeLinux/AmazonML2024/66e31d6ee96cd_student_resource_3/student_resource 3/dataset/train.csv')
dataTest = pd.read_csv('/home/eshan/Eshan/CodeLinux/AmazonML2024/66e31d6ee96cd_student_resource_3/student_resource 3/dataset/test.csv')

# save_images_in_entity_folders(dataTrain, 'train')
save_images(dataTest, 'test')
# save_images_in_entity_folders(dataTest, 'test')
