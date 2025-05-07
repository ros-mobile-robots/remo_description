import os
import yaml
import requests

def download_file(url, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def main():
    config_path = "stl_download_config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    for relative_path, url in config["files"].items():
        print(f"Downloading {relative_path}...")
        download_file(url, relative_path)
    print("Download complete.")

if __name__ == "__main__":
    main()

