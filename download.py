import os
from pathlib import Path

from ultralytics.utils.downloads import download
#approx = 10mins 


def visdrone2yolo(dir):
    """Convert VisDrone annotations to YOLO format, creating label files with normalized bounding box coordinates."""
    from PIL import Image
    from tqdm import tqdm

    def convert_box(size, box):
        # Convert VisDrone box to YOLO xywh box
        dw = 1.0 / size[0]
        dh = 1.0 / size[1]
        return (box[0] + box[2] / 2) * dw, (box[1] + box[3] / 2) * dh, box[2] * dw, box[3] * dh

    (dir / "labels").mkdir(parents=True, exist_ok=True)  # make labels directory
    pbar = tqdm((dir / "annotations").glob("*.txt"), desc=f"Converting {dir}")
    for f in pbar:
        img_size = Image.open((dir / "images" / f.name).with_suffix(".jpg")).size
        lines = []
        with open(f, encoding="utf-8") as file:  # read annotation.txt
            for row in [x.split(",") for x in file.read().strip().splitlines()]:
                if row[4] == "0":  # VisDrone 'ignored regions' class 0
                    continue
                cls = int(row[5]) - 1
                box = convert_box(img_size, tuple(map(int, row[:4])))
                lines.append(f"{cls} {' '.join(f'{x:.6f}' for x in box)}\n")
                with open(str(f).replace(f"{os.sep}annotations{os.sep}", f"{os.sep}labels{os.sep}"), "w", encoding="utf-8") as fl:
                    fl.writelines(lines)  # write label.txt


# Download
dir = Path("F:\yolo_11")  # dataset root dir
urls = [
    "https://github.com/ultralytics/assets/releases/download/v0.0.0/VisDrone2019-DET-train.zip",
    "https://github.com/ultralytics/assets/releases/download/v0.0.0/VisDrone2019-DET-val.zip",
    "https://github.com/ultralytics/assets/releases/download/v0.0.0/VisDrone2019-DET-test-dev.zip",
    "https://github.com/ultralytics/assets/releases/download/v0.0.0/VisDrone2019-DET-test-challenge.zip",
]
download(urls, dir=dir, curl=True, threads=4)

# Convert
for d in "VisDrone2019-DET-train", "VisDrone2019-DET-val", "VisDrone2019-DET-test-dev":
    visdrone2yolo(dir / d)  # convert VisDrone annotations to YOLO labels