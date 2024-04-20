import tomllib
from typing import Any, NoReturn
import requests
from bs4 import BeautifulSoup


def get_config() -> dict[str, Any]:
    with open("config.toml", "rb") as f:
        return tomllib.load(f)


def download_file(url: str, output: str):
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if resp.ok:
        with open(output, "wb") as f:
            f.write(resp.content)
            print(f"Successfully downloaded {output}")
            print(f"File size: {round(len(resp.content) / 1024 / 1024, 2)} MB")
    else:
        print(f"Failed to download: {url}")


def download_youtube_from_apkmirror(output: str) -> NoReturn:
    config = get_config()

    # Get youtube from config
    link_url = config["YouTube"]["apkmirror-dlurl"]
    version = config["YouTube"]["version"]

    original_url = "https://apkmirror.com"

    print(f"Downloading Youtube version {version}")
    print("Fetching YouTube APK releases...")
    resp = requests.get(
        f"{link_url}/youtube-{version}-release/", headers={"User-Agent": "Mozilla/5.0"}
    )
    if not resp.ok:
        print(f"Failed to fetch YouTube APK releases\nStatus code: {resp.status_code}")
        exit(1)

    soup = BeautifulSoup(resp.text, "html.parser")
    selected = soup.select_one(
        "#downloads > div:nth-child(7) > div > div:nth-child(3) > div:nth-child(5) > a"
    )

    print("Selected download link\n", selected)
    download_url = original_url + selected["href"]

    resp = requests.get(download_url, headers={"User-Agent": "Mozilla/5.0"})
    if resp.ok:
        soup2 = BeautifulSoup(resp.text, "html.parser")
        selector = soup2.select_one(
            "#file > div.row.d-flex.f-a-start > div.center.f-sm-50 > div > a"
        )
        print("Found file selector\n", selector)
        key_url = original_url + selector["href"]

    resp = requests.get(key_url, headers={"User-Agent": "Mozilla/5.0"})
    soup3 = BeautifulSoup(resp.text, "html.parser")
    selector = soup3.select_one(
        "#post-5966750 > div.card-with-tabs > div > div > div:nth-child(1) > p:nth-child(3) > span > a"
    )

    if resp.ok:
        print("Found key url\n", selector)
        download_url = original_url + selector["href"]

        print("Downloading apk...")
        download_file(download_url, output)

    print(f"Done. {output}")
    return output
