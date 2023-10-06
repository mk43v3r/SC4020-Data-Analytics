import wget
import os
import sys
import re
import zipfile

REPO_NAME = "SC4020-Data-Analytics"
DATA_DIR = "./data/"
DOWNLOAD_DICT = {
    "t48k.txt": "https://cs.joensuu.fi/sipu/datasets/t4.8k.txt",
    "nested.zip": "https://cs.joensuu.fi/sipu/datasets/nested.zip",
    "worms.zip": "http://cs.uef.fi/sipu/datasets/worms.zip",
    "r15.txt": "https://cs.joensuu.fi/sipu/datasets/R15.txt",
    "jain.txt": "https://cs.joensuu.fi/sipu/datasets/jain.txt",
    "pathbased.txt": "https://cs.joensuu.fi/sipu/datasets/pathbased.txt",
    "Compound.txt": "https://cs.joensuu.fi/sipu/datasets/Compound.txt",
    "unbalance2.txt": "https://cs.joensuu.fi/sipu/datasets/unbalance2.txt",
    "skewed.txt": "https://cs.joensuu.fi/sipu/datasets/skewed.txt"
}

if (os.path.basename(os.getcwd()) != REPO_NAME):
    print("Make sure you are in the directory of the repository before running the script.")
    sys.exit()

# Download file if they don't already exist, to DATA_DIR
# Unzip the file if they are a zip file
for filename, url in DOWNLOAD_DICT.items():
    if os.path.exists(DATA_DIR + filename):
        print(f"{filename} already exists. Skipping download.")
        continue

    wget.download(url, DATA_DIR + filename)

    if re.search(r"\.zip", filename) is None: continue

    with zipfile.ZipFile(DATA_DIR + filename, "r") as zip_ref:
        zip_ref.extractall(DATA_DIR)
        
