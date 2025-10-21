import requests
from pathlib import Path
import zipfile
import json

def try_update():
    
    owner = "Danb106632"
    repo = "escape-nuke-enviroment"

    # GitHub API URL for the latest release
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

    print("UPDATER: Querying GitHub...")

    # Get latest release info
    try:
        response = requests.get(api_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print ("Oops: Something Else",err)
        return
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        return
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        return
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        return
    
    
    release_data = response.json()

    # Get the ZIP archive URL of the source code
    try: 
        zip_url = release_data["zipball_url"]
        tag_name = release_data["tag_name"]
    except KeyError as e:
        print("URL and values not found. Check github response")
        return

    # Skip if not a release version
    if "release" not in tag_name:
        return

    # Download the ZIP
    zip_response = requests.get(zip_url)

    # Create Directory to download to
    dirReleaseFolder = str(Path(__file__).resolve().parent) + "/files"
    Path(dirReleaseFolder).mkdir(parents=False, exist_ok=True) 

    # Set variables
    gitFileVersion = f"{repo}-{tag_name}"
    filename = dirReleaseFolder + f"/{gitFileVersion}.zip"

    version = get_downloaded_version()
    
    # See if zip is download, already latest version
    if version == gitFileVersion:
        print("UPDATER: No new version found, skipping...")
        return

    # Update Version
    write_downloaded_version(gitFileVersion)
    
    # Save the file
    with open(filename, "wb") as f:
        f.write(zip_response.content)

    print(f"UPDATER: New version found: {gitFileVersion} \nExtracting......")

    
    extract_update(filename, str(Path("X:\.nuke").resolve()))

    print("UPDATER: Done!")



def get_downloaded_version():

    version_file = str(Path(__file__).resolve().parent) + '/version.json'
    
    try:
        with open(version_file, 'r') as f:
            data = json.load(f)
            return data["version"]
    
    except json.decoder.JSONDecodeError:
        # JSON file exists but is malformed — overwrite it
        data = {"version": ""}
        with open(version_file, 'w') as f:  # Open in write mode
            json.dump(data, f, indent=4)
        return ""

    except FileNotFoundError:
        # File does not exist — create it with default data
        data = {"version": ""}
        with open(version_file, 'w') as f:
            json.dump(data, f, indent=4)
        return ""

    except KeyError:
        # "version" key missing in JSON — reset file
        data = {"version": ""}
        with open(version_file, 'w') as f:
            json.dump(data, f, indent=4)
        return ""


def write_downloaded_version(version):

    with open(str(Path(__file__).resolve().parent) + '/version.json', 'w') as f:
        data = {"version": version}
        json_str = json.dumps(data, indent=4)

        f.write(json_str)


def extract_update(zip_path, extract_to):
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