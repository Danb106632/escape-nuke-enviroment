import nuke

import gdown
import csv
import os
import zipfile
from pathlib import Path


def try_update():

    print("CATTERY UPDATER: Querying GDrive...")

    csv_file_id = "1onNo5672gHahZfAWaXXO8OhEyth-JimE"
    url = f"https://drive.google.com/uc?id={csv_file_id}"

    catteryPath = Path(__file__).parent
    csvPath = catteryPath.joinpath("cattery_list.csv")

    try:
        # quiet=False enables gdown’s progress bar
        content = gdown.download(url, output=str(csvPath), quiet=True)  # str
        print(f"Downloaded: {output_path}")
    except (Exception, SystemExit) as e:
        print(f"Failed to download CSV list: Try again later")
        pass

    data_dict = {}

    with open(str(csvPath), newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name, file_id = row  # unpack each row
            data_dict.update({name: file_id})

    # Download each file with gdown
    for name, file_id in data_dict.items():
        output_path = catteryPath.joinpath(f"{name}.zip")
        output_folder = catteryPath.joinpath(f"{name}")

        if os.path.exists(output_folder):
            print(f"Skipping {name}: file already exists")
            continue

        url = f"https://drive.google.com/uc?id={file_id}"
        try:
            # quiet=False enables gdown’s progress bar
            gdown.download(url, str(output_path), quiet=False)
            print(f"Downloaded: {output_path}")
        except (Exception, SystemExit) as e:
            print(f"Failed to download {name}: Try again later")
            pass

        if os.path.exists(output_path):
            Path(output_folder).mkdir(parents=False, exist_ok=True)
            extract_cattery(output_path, output_folder)

            os.remove(output_path)


def extract_cattery(zip_path, extract_to):
    zip_path = Path(zip_path)
    extract_to = Path(extract_to)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        all_members = zip_ref.namelist()

        # Identify single top-level folder
        top_dirs = {member.split('/')[0] for member in all_members if '/' in member}
        if len(top_dirs) != 1:
            raise ValueError("ZIP must contain exactly one top-level folder.")
        top_folder = next(iter(top_dirs))

        for member in all_members:
            if member.endswith('/'):
                continue  # skip directories

            if member.startswith(top_folder + '/'):
                relative_path = Path(member).relative_to(top_folder)
                target_path = extract_to / relative_path

                try:
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    with zip_ref.open(member) as source, open(target_path, 'wb') as target:
                        target.write(source.read())

                except PermissionError:
                    print(f"Permission denied when extracting {target_path}. Skipping.")
                except Exception as e:
                    print(f"Error extracting {target_path}: {e}. Skipping.")