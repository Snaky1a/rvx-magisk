import os
from utils import *

config = get_config()

youtube = config["YouTube"]
youtube_music = config["YouTube-Music"]

d = download_from_apkmirror(youtube["apkmirror-dlurl"], "19-11-38", "youtube.apk", ["both"], "")
print(d)