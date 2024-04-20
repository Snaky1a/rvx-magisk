import tomllib
from typing import Any
import requests
from bs4 import BeautifulSoup


def get_config() -> dict[str, Any]:
    with open("config.toml", "rb") as f:
        return tomllib.load(f)

def download_from_apkmirror(link: str, version: str, output: str, arch: str, dpi: str):
    original_url = "https://apkmirror.com"
    resp = requests.get(f"{link}/youtube-{version}-release/", headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(resp.text, "html.parser")
    selected = soup.select_one("#downloads > div:nth-child(7) > div > div:nth-child(3) > div:nth-child(5) > a")
    # print(selected["href"])
    print(selected)
    download_url = original_url + selected["href"]
    
    resp = requests.get(download_url, headers={"User-Agent": "Mozilla/5.0"})
    soup2 = BeautifulSoup(resp.text, "html.parser")
    selector = soup2.select_one("#file > div.row.d-flex.f-a-start > div.center.f-sm-50 > div > a")
    key_url = original_url + selector["href"]

    resp = requests.get(key_url, headers={"User-Agent": "Mozilla/5.0"})
    soup3 = BeautifulSoup(resp.text, "html.parser")
    selector = soup3.select_one("#post-5966750 > div.card-with-tabs > div > div > div:nth-child(1) > p:nth-child(3) > span > a")
    print(selector.attrs)
    download_url = original_url + selector["href"]
    
    resp = requests.get(download_url, headers={"User-Agent": "Mozilla/5.0"})
    with open(output, "wb") as f:
        f.write(resp.content)
    
    return f"Done. {output}"