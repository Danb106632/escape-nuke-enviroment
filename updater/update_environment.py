"""
GitHub Release Updater for Nuke Environment
Downloads and extracts the latest release from a GitHub repository.
"""

import requests
import nuke
import zipfile
import json
from pathlib import Path


# Configuration
GITHUB_OWNER = "Danb106632"
GITHUB_REPO = "escape-nuke-enviroment"


def try_update():
    """
    Check for and download the latest release from GitHub if a new version is available.
    Only runs in GUI mode, skips on render farm/command line execution.
    """
    # Skip update check if not running in GUI mode (e.g., on Deadline render farm)
    if not nuke.expression("$gui"):
        return
    
    print("UPDATER: Querying GitHub...")
    
    # Get latest release information
    release_data = _fetch_latest_release()
    if not release_data:
        return
    
    # Extract release details
    try:
        zip_url = release_data["zipball_url"]
        tag_name = release_data["tag_name"]
    except KeyError:
        print("UPDATER: URL and values not found in GitHub response")
        return
    
    # Skip if not a release version
    if "release" not in tag_name:
        print("UPDATER: Tag is not a release version, skipping...")
        return
    
    # Check if already up to date
    current_version = get_downloaded_version()
    git_file_version = f"{GITHUB_REPO}-{tag_name}"
    
    if current_version == git_file_version:
        print("UPDATER: No new version found, skipping...")
        return
    
    print(f"UPDATER: New version found: {git_file_version}")
    
    # Download and extract the update
    if _download_and_extract_release(zip_url, git_file_version):
        write_downloaded_version(git_file_version)
        print("UPDATER: Done!")
    else:
        print("UPDATER: Update failed")


def _fetch_latest_release():
    """
    Fetch the latest release data from GitHub API.
    
    Returns:
        dict or None: Release data if successful, None otherwise
    """
    api_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
    
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"UPDATER: HTTP Error: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"UPDATER: Connection Error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"UPDATER: Timeout Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"UPDATER: Request Error: {e}")
    except json.JSONDecodeError as e:
        print(f"UPDATER: Invalid JSON response: {e}")
    
    return None


def _download_and_extract_release(zip_url, version_name):
    """
    Download and extract a release ZIP file.
    
    Args:
        zip_url (str): URL to download the ZIP from
        version_name (str): Version identifier for the download
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Download the ZIP file
    try:
        print("UPDATER: Downloading...")
        zip_response = requests.get(zip_url, timeout=30)
        zip_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"UPDATER: Failed to download release: {e}")
        return False
    
    # Create release folder
    dir_release_folder = Path(__file__).resolve().parent / "files"
    dir_release_folder.mkdir(parents=False, exist_ok=True)
    
    # Save the ZIP file
    filename = dir_release_folder / f"{version_name}.zip"
    try:
        with open(filename, "wb") as f:
            f.write(zip_response.content)
    except IOError as e:
        print(f"UPDATER: Failed to save ZIP file: {e}")
        return False
    
    print("UPDATER: Extracting...")
    
    # Extract to parent directory
    extract_path = Path(__file__).parent.parent.resolve()
    return extract_update(filename, extract_path)


def get_downloaded_version():
    """
    Get the currently downloaded version from version.json.
    
    Returns:
        str: Version string, empty string if not found or invalid
    """
    version_file = Path(__file__).resolve().parent / 'version.json'
    
    try:
        with open(version_file, 'r') as f:
            data = json.load(f)
            return data.get("version", "")
    
    except json.JSONDecodeError:
        # JSON file exists but is malformed - reset it
        _write_version_file(version_file, "")
        return ""
    
    except FileNotFoundError:
        # File does not exist - create it
        _write_version_file(version_file, "")
        return ""
    
    except Exception as e:
        print(f"UPDATER: Error reading version file: {e}")
        return ""


def write_downloaded_version(version):
    """
    Write the current version to version.json.
    
    Args:
        version (str): Version string to write
    
    Returns:
        bool: True if successful, False otherwise
    """
    version_file = Path(__file__).resolve().parent / 'version.json'
    return _write_version_file(version_file, version)


def _write_version_file(filepath, version):
    """
    Internal function to write version data to file.
    
    Args:
        filepath (Path): Path to version.json file
        version (str): Version string to write
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filepath, 'w') as f:
            data = {"version": version}
            json.dump(data, f, indent=4)
        return True
    except IOError as e:
        print(f"UPDATER: Failed to write version file: {e}")
        return False


def extract_update(zip_path, extract_to):
    """
    Extract ZIP archive, skipping the top-level folder.
    
    Args:
        zip_path (Path or str): Path to the ZIP file
        extract_to (Path or str): Destination directory
    
    Returns:
        bool: True if extraction successful, False otherwise
    """
    zip_path = Path(zip_path)
    extract_to = Path(extract_to)
    
    if not zip_path.exists():
        print(f"UPDATER: ZIP file not found: {zip_path}")
        return False
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            all_members = zip_ref.namelist()
            
            # Identify single top-level folder
            top_dirs = {member.split('/')[0] for member in all_members if '/' in member}
            
            if len(top_dirs) != 1:
                print("UPDATER: ZIP must contain exactly one top-level folder")
                return False
            
            top_folder = next(iter(top_dirs))
            
            success_count = 0
            skip_count = 0
            
            for member in all_members:
                # Skip directory entries
                if member.endswith('/'):
                    continue
                
                # Only process files inside the top folder
                if not member.startswith(top_folder + '/'):
                    continue
                
                # Calculate target path (removing top-level folder)
                relative_path = Path(member).relative_to(top_folder)
                target_path = extract_to / relative_path
                
                try:
                    # Create parent directories if needed
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Extract file
                    with zip_ref.open(member) as source, open(target_path, 'wb') as target:
                        target.write(source.read())
                    
                    success_count += 1
                
                except PermissionError:
                    print(f"UPDATER: Permission denied - {target_path}")
                    skip_count += 1
                
                except Exception as e:
                    print(f"UPDATER: Error extracting {target_path}: {e}")
                    skip_count += 1
            
            print(f"UPDATER: Extracted {success_count} files, skipped {skip_count}")
            return success_count > 0
    
    except zipfile.BadZipFile:
        print(f"UPDATER: Invalid ZIP file: {zip_path}")
        return False
    
    except Exception as e:
        print(f"UPDATER: Extraction failed: {e}")
        return False