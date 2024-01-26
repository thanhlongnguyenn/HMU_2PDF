import os
import requests
from PIL import Image
import shutil

def get_url(linkSach):
    a = linkSach.replace("FullBookReader.aspx?Url=/pages/cms/", "")
    return a[:-49]

def download_images(start, end, returnUrl):
    if not os.path.exists('imgs'):
        os.makedirs('imgs')

    for i in range(start, end+1):
        generated_url = (returnUrl + f'FullPreview/{str(i).zfill(6)}.jpg') 
        response = requests.get(generated_url)            
        if response.status_code == 200:
            with open(f'imgs/{str(i).zfill(6)}.jpg', 'wb') as handle:
                handle.write(response.content)

def convert_imgs_folder_to_pdf(start, end, destination):
    img_list = []

    for i in range(start, end+1):
        with Image.open(f'imgs/{str(i).zfill(6)}.jpg') as image:
            img_list.append(image.convert('RGB'))

    img_list[0].save(destination, save_all=True, append_images=img_list[1:])

    # Clean up the imgs folder after converting to PDF
    shutil.rmtree('imgs')

    return destination
