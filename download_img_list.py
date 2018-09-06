from img_downloader import google_images_download
from matplotlib import pyplot as plt
import pandas as pd
import shutil
import os

def clean_pic_folder(directory):
    '''Loops through images in a directory, and deletes those that couldn't be opened to check if files are correct.'''
    files = os.listdir(directory)
    counter = 0
    for f in files:
        currentfile = directory + f
        try: 
            img = plt.imread(currentfile)
        except (OSError, ValueError):
            counter += 1
            os.remove(currentfile)
            print('Removed: ' + currentfile)
    print(f'{counter} files removed in total.')
    
def move_all(files, src_dir, dest_dir):
    for f in files:
        shutil.move(f'{src_dir}{f}', f'{dest_dir}{f}')
    return None

def download_img_list(key_list, dest_dir, n = 5, temp_dir = 'temp_img/'):
    
    '''Downloads n images for every element in key_list, puts them in dest_dir, and creates a pd dataframe
    that maps image filenames to elements in key_list'''
    
    err_list = []
    
    os.makedirs(temp_dir)
    
    response = google_images_download.googleimagesdownload()
    download_options = {'limit':n, 'format':'jpg', 'output_directory':temp_dir, 'no_directory':True}
    
    file_list = []
    label_list = []
    
    i = 0

    for im in key_list:
        
        print('\nProcessing element '+str(i))
        i += 1
    
        try:
            response.download({**download_options, **{'keywords':im}})
        except:
            err_list.append(im)
        
        clean_pic_folder(temp_dir)
        
        # Rename files
        j = 0
        for f in os.listdir(temp_dir):
            new_name = im.replace(' ', '_') + str(j) + '.jpg'
            os.rename(temp_dir+f, temp_dir+new_name)
            j += 1
    
        current_files = os.listdir(temp_dir)
        file_list = file_list + current_files
        label_list = label_list + [im.replace(' ', '_')] * len(current_files)
    
        move_all(current_files, temp_dir, dest_dir) 

    os.rmdir(temp_dir)  
    
    labels = pd.DataFrame({'id':file_list, 'label':label_list})
    
    return labels, err_list