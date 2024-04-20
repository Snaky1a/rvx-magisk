import tomllib
from typing import Any, NoReturn
import requests
from bs4 import BeautifulSoup


def get_config() -> dict[str, Any]:
    with open("config.toml", "rb") as f:
        return tomllib.load(f)

def download_file(url: str, output: str) -> None:
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if resp.ok:
        with open(output, "wb") as f:
            f.write(resp.content)
            print("Downloaded successfully:", output)
    else:
        print("Failed to download:", url)

def download_youtube_from_apkmirror(output: str) -> None:
    config = get_config()
    link_url = config.get("YouTube", {}).get("apkmirror-dlurl")
    version = config.get("YouTube", {}).get("version")

    if not link_url or not version:
        print("YouTube link or version not found in config")
        return

    print(f"Downloading YouTube version {version}")
    url = f"{link_url}/youtube-{version}-release/"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if not resp.ok:
        print("Failed to fetch YouTube APK releases")
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    download_link = soup.select_one("#downloads a[href*='download/apk']")
    if not download_link:
        print("Download link not found")
        return

    download_url = download_link["href"]
    key_url = download_url.replace("download", "download/key")
    download_file(key_url, output)
