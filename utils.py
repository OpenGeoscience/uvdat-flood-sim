import requests


def download_file(url, path):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f'Downloaded file to {path}.')
