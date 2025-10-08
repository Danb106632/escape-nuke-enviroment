import requests
from pathlib import Path as p

def download():
    owner = "Danb106632"
    repo = "escape-nuke-enviroment"

    # GitHub API URL for the latest release
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

    # Get latest release info
    response = requests.get(api_url)
    release_data = response.json()

    # Get the ZIP archive URL of the source code
    zip_url = release_data["zipball_url"]
    tag_name = release_data["tag_name"]

    # Download the ZIP
    zip_response = requests.get(zip_url)

    # Save the file

    dir = str(p(__file__).resolve().parent) + "/files/"
    filename = dir + f"{repo}-{tag_name}.zip"
    print(filename)
    with open(filename, "wb") as f:
        f.write(zip_response.content)

    print(f"Downloaded latest release: {filename}")

