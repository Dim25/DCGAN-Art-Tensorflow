# -*- coding: utf-8 -*-

# Libraries 
# Python 2+3 compatible
import sys
if sys.version_info[0] >= 3:
    from urllib.request import urlretrieve
else:
    # Likely to be Python 2
    from urllib import urlretrieve

import os
import threading

project_directory_prefix="" # for local deployment
# project_directory_prefix="/content/drive/My Drive/dcgan_01/" # Google Drive on Colab

categories = [
    # Picasso
    {   
        "name": "Picasso",
        "data_directory": "data/raw/picasso", 
        "sources": [
            # By style
            "https://www.wikiart.org/en/pablo-picasso/by-Style/surrealism",
            "https://www.wikiart.org/en/pablo-picasso/by-Style/synthetic-cubism",
            "https://www.wikiart.org/en/pablo-picasso/by-Style/analytical-cubism", 
            # By period 
            "https://www.wikiart.org/en/pablo-picasso/by-period/cubist-period",
            # By genre
            "https://www.wikiart.org/en/pablo-picasso/by-Genre/still-life",
            # By media
            "https://www.wikiart.org/en/pablo-picasso/by-Media/collage",
        ]
    },
    
    # Cubism
    {   
        "name": "Cubism",
        "data_directory": "data/raw/cubism", 
        "sources": [
            # All paintings by Style
            "https://www.wikiart.org/en/paintings-by-style/cubism",
        ]
    }, 

    # Nude
    {   
        "name": "NudeArt",
        "data_directory": "data/raw/nude", 
        "sources": [
            # All paintings by Style
            "https://www.wikiart.org/en/paintings-by-genre/nude-painting-nu",
        ]
    }, 

    # Portrait
    {   
        "name": "Portrait",
        "data_directory": "data/raw/portrait", 
        "sources": [
            # All paintings by Style
            "https://www.wikiart.org/en/paintings-by-genre/portrait",
        ]
    }, 

]

# directory = "data/raw/cubism"
# if not os.path.exists(data_directory):
#     os.makedirs(data_directory)

# Cubism data 
target = "https://www.wikiart.org/en/paintings-by-style/cubism"

# Pretty print
import pprint
pp = pprint.PrettyPrinter(indent=4)

import requests
import os.path


def download_file(image_url, file_path):
    # urlretrieve(image_url, file_path)
    try:
        # Check if data directory exists, makes dirs if not 
        if not os.path.isfile(file_path) or True: # os.path.exists(file_path):
            urlretrieve(image_url, file_path)
        else:
            print("already processed", file_path)
    except Exception as e:
        print("-"*42)
        print(image_url)
        print(e) 
        print("-"*42)
        # pass 

# Processing categories
for category in categories:
    category_name = category['name'].lower()
    data_directory = category['data_directory'].lower()

    # Check if data directory exists, makes dirs if not 
    if not os.path.exists(project_directory_prefix + data_directory):
        os.makedirs(project_directory_prefix + data_directory)


    # Processing sources (sub-categories)
    for source in category['sources']:
        print(source)

        # Iterating pages
        all_paintings_count = 3600 # Default paintings count 
        page_size = 60 # Default page size 

        for page in range(1,int(all_paintings_count/page_size)):
            url = "{source}?style=featured&json=2&layout=new&page={page}&resultType=masonry".format(source=source, page=page)

            # url = "https://www.wikiart.org/en/pablo-picasso/all-works" + "?select=surrealism&json=2&layout=new&page=1&resultType=masonry"

            print("Processing url",url)
            r = requests.get(url)

            # # pp.pprint(r.content)
            response = r.json()
            # pp.pprint(response) 

            # Update paintings count for current source
            all_paintings_count = int(response['AllPaintingsCount'])

            # Continue if no data
            if not response['Paintings']: 
                continue
                
            if not len(response['Paintings']): 
                continue

            # Iterate paintings
            for painting in response['Paintings']:
                image_url = painting['image']
                filename = painting['id'] + ".png"
                file_path = "{prefix}{data_directory}/{filename}".format(prefix=project_directory_prefix, data_directory=data_directory, filename=filename)
                print("Processing", filename, image_url, "to", file_path)

                # Non threding solution
                download_file(image_url, file_path)

                # # Threading to speed up downloading process
                # threading.Thread(target=download_file, args=(image_url, file_path)).start()