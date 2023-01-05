from shutil import copy2
from pathlib import Path


with open("./with_intersection.txt") as f:
    for id in f.readlines():
        id = id.split('\n')[0]
        src = Path(f"./source_cv/s_{id}.jpg")
        trg = Path(f"./mask/s_{id}.jpg")
        copy2(src, f"../../../New/source")
        copy2(trg, f"../../../New/mask")
