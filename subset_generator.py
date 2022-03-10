from shutil import copy2
from pathlib import Path

# with open("./with_intersection.txt","w") as f:
#     for i in range(10000):
#         cross = np.load(f"./intersections/{i+1}.npy", allow_pickle=True)
#         if cross.size != 0:
#             f.writelines(f"{i+1}\n")
# scolor = "#{:06X}".format(16777215 - int(PLOT_COLOR.split("#")[1], 16))


with open("./with_intersection.txt") as f:
    for id in f.readlines():
        id = id.split('\n')[0]
        src = Path(f"./source_cv/s_{id}.jpg")
        trg = Path(f"./mask/s_{id}.jpg")
        copy2(src, f"../../../New/source")
        copy2(trg, f"../../../New/mask")
