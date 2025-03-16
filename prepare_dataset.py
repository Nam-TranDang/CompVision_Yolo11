import os
from PIL import Image
from tqdm import tqdm
import shutil

# Paths
dataset_root = "F:\\yolo_11\\VisDrone-VID"  # Verify this path
dataset = "dataset"
images_root = os.path.join(dataset, "images")
labels_root = os.path.join(dataset, "labels")

def get_image_size(image_path):
    with Image.open(image_path) as img:
        return img.size  # width, height

def convert_to_yolo(annotations, image_size):
    width, height = image_size
    yolo_labels = []
    for category, bbox in annotations:
        left, top, w, h = bbox
        x_center = (left + w / 2) / width
        y_center = (top + h / 2) / height
        w_norm = w / width
        h_norm = h / height
        yolo_labels.append(f"{category} {x_center} {y_center} {w_norm} {h_norm}")
    return yolo_labels

# Create directories
os.makedirs(images_root, exist_ok=True)
os.makedirs(labels_root, exist_ok=True)

for split in ["train", "val"]:
    sequences_dir = os.path.join(dataset_root, split, "sequences")
    annotations_dir = os.path.join(dataset_root, split, "annotations")
    images_split_dir = os.path.join(images_root, split)
    labels_split_dir = os.path.join(labels_root, split)
    os.makedirs(images_split_dir, exist_ok=True)
    os.makedirs(labels_split_dir, exist_ok=True)

    # Create symlinks or copy images
    for video_name in os.listdir(sequences_dir):
        video_dir = os.path.join(sequences_dir, video_name)
        if os.path.isdir(video_dir):
            dst_dir = os.path.join(images_split_dir, video_name)
            if not os.path.exists(dst_dir):
                try:
                    os.symlink(video_dir, dst_dir, target_is_directory=True)
                except OSError:
                    shutil.copytree(video_dir, dst_dir)  # Fallback to copy

    # Process annotations
    for ann_file in os.listdir(annotations_dir):
        if ann_file.endswith(".txt"):
            video_name = ann_file.replace(".txt", "")
            ann_path = os.path.join(annotations_dir, ann_file)
            video_dir = os.path.join(sequences_dir, video_name)
            frames = sorted([f for f in os.listdir(video_dir) if f.endswith(".jpg")])
            if not frames:
                continue
            image_size = get_image_size(os.path.join(video_dir, frames[0]))
            video_labels_dir = os.path.join(labels_split_dir, video_name)
            os.makedirs(video_labels_dir, exist_ok=True)

            # Parse annotations
            with open(ann_path, "r") as f:
                lines = [line.strip().split(",") for line in f]
            frame_annotations = {}
            for line in lines:
                frame_idx = int(line[0]) - 1  # 0-based
                obj_cat = int(line[7])
                if obj_cat == 0:  # Skip ignored regions
                    continue
                category = obj_cat - 1  # Map 1-10 to 0-9
                bbox = list(map(int, line[2:6]))
                if frame_idx not in frame_annotations:
                    frame_annotations[frame_idx] = []
                frame_annotations[frame_idx].append((category, bbox))

            # Generate label files
            for frame_idx in tqdm(frame_annotations, desc=f"Processing {video_name}"):
                frame_name = f"{frame_idx + 1:07d}.jpg"  # Match 7-digit naming
                label_path = os.path.join(video_labels_dir, frame_name.replace(".jpg", ".txt"))
                yolo_labels = convert_to_yolo(frame_annotations[frame_idx], image_size)
                with open(label_path, "w") as f:
                    for label in yolo_labels:
                        f.write(label + "\n")