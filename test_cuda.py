# down CUDA match with GTX 1650 PyTorch with CUDA 11.8 - pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# pip install ultralytics for YOLO11
# annotation format: <frame_index>,<target_id>,<bbox_left>,<bbox_top>,<bbox_width>,<bbox_height>,<score>,<object_category>,<truncation>,<occlusion>
# object_category: 0 (ignored), 1 (pedestrian), ..., 10 (motor).
# pip install ultralytics pillow tqdm

import torch
print(torch.cuda.is_available())  # Should print True