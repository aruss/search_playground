import os
import requests
from dotenv import load_dotenv
from os import walk

load_dotenv()

inputfiles = []
for (dirpath, dirnames, filenames) in walk("./input"):
    inputfiles.extend(filenames)
    break

print(onlyfiles)