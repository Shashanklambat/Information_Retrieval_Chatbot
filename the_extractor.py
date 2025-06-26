# This will have everything that has to be done with extracting the data from files.
# This will be run before anything is done to make sure the database has the latest information

import os
import json


current_dir                 = os.path.dirname(os.path.abspath(__file__))
MATERIAL_DIRECTORY_NAME     = "material"
MATERIAL_DIRECTORY_PATH     = os.path.join(current_dir, MATERIAL_DIRECTORY_NAME)
METADATA_FILE_NAME          = "metadata.json"
METADATA_FILE_PATH          = os.path.join(current_dir, METADATA_FILE_NAME)


if os.path.exists(MATERIAL_DIRECTORY_PATH) and os.path.isdir(MATERIAL_DIRECTORY_PATH):
    if not os.listdir(MATERIAL_DIRECTORY_PATH):
        print("FATAL-MISTAKE: Material directory empty, please add material before using this application!")
        exit()
    else:
        print("CHECK: Material directory--good to go!")
else:
    os.mkdir(MATERIAL_DIRECTORY_PATH)
    print(f"Directory {MATERIAL_DIRECTORY_NAME} created at path {MATERIAL_DIRECTORY_PATH}")
    print("FATAL-MISTAKE: Material directory empty, please add material before using this application!")
    exit()


if os.path.exists(METADATA_FILE_PATH):
    print(f"CHECK: File {METADATA_FILE_NAME} exists in path {METADATA_FILE_PATH}")
else:
    with open(METADATA_FILE_PATH, 'w') as f:
        print(f"CHECK: File {METADATA_FILE_NAME} created in path {METADATA_FILE_PATH}")
        json.dump({}, f)


def get_material_modf() -> dict: 
    file_time_history = {}
    for root, _, files in os.walk(MATERIAL_DIRECTORY_PATH):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_time_history[file_path] = os.path.getmtime(file_path)
            
    return file_time_history


def update_metadata(latest_time_history) -> None:
    with open(METADATA_FILE_PATH, 'w') as json_file:
        json.dump(latest_time_history, json_file)
    
    return


def read_metadata_file() -> dict:
    with open(METADATA_FILE_PATH, 'r') as json_file:
        return json.load(json_file)


def check_metadata_modf() -> bool:
    latest_time_history = get_material_modf()
    
    if latest_time_history == read_metadata_file():
        return False
    else:
        update_metadata(latest_time_history)
        return True


def get_file_contents() -> list:
    file_contents = []
    
    for root, _, files in os.walk(MATERIAL_DIRECTORY_PATH):
        for filename in files:
            file_path = os.path.join(root, filename)
            with open(file_path, 'r') as f:
                file_content = f.read()
            file_contents.append(file_content)
    
    return file_contents