import os, shutil
import sys

path = r'C:\Users\kotav\OneDrive\Documents\Data Analysis Project\Python- Automated File Sorter'

'''
1. Go into the path - done
2. Are there folders in here already? if not create a folder
3. Check each file individually and identify file type
4. Move that file to correct folder
'''
dir_list = os.listdir(path)

print(dir_list)

def switching(source_file, f_extension):
    match f_extension:
        case ".txt":
            if not os.path.exists(path + '\TextFiles'):
                os.mkdir(path + '\TextFiles', 0o777)
                print("Text files Directory created")
                dest_file = os.path.basename(source_file)
                dest_path = path+'\TextFiles\\'+dest_file
                shutil.move(source_file, dest_path)
                print(os.listdir(path+'\TextFiles\\'))
        case ".xlsx":
            if not os.path.exists(path + '\ExcelFiles'):
                os.mkdir(path + '\ExcelFiles', 0o777)
                print("Excel files Directory created")
                dest_file = os.path.basename(source_file)
                dest_path = path+'\ExcelFiles\\'+dest_file
                shutil.move(source_file, dest_path)
                print(os.listdir(path+'\ExcelFiles\\'))
        case ".jpg":
            if not os.path.exists(path + '\JPGFiles'):
                os.mkdir(path + '\JPGFiles', 0o777)
                print("JPG files Directory created")
                dest_file = os.path.basename(source_file)
                dest_path = path+'\JPGFiles\\'+dest_file
                shutil.move(source_file, dest_path)
                print(os.listdir(path+'\JPGFiles\\'))
        case ".pdf":
            if not os.path.exists(path + '\PDFFiles'):
                os.mkdir(path + '\PDFFiles', 0o777)
                print("PDF files Directory created")
                dest_file = os.path.basename(source_file)
                dest_path = path+'\PDFFiles\\'+dest_file
                shutil.move(source_file, dest_path)
                print(os.listdir(path+'\PDFFiles\\'))
        case _:
            print("This file is unrecognizable.")


for filename in os.listdir(path):
    f = os.path.join(path, filename)
    if os.path.isfile(f):
        file_name, file_extension = os.path.splitext(f)
        switching(f, file_extension)