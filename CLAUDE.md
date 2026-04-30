# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Traffic Sign Detection System (交通标志识别系统) — a PyQt5 desktop application for real-time detection and classification of Chinese traffic signs using YOLOv8. Architecture follows the `class_Detection` reference project (student classroom behavior recognition system).

## Tech Stack

- **Model**: Ultralytics YOLOv8 (v8.0.199), PyTorch with CUDA
- **GUI**: PyQt5 5.15.2 with Qt Designer (.ui files compiled via pyuic5)
- **Image processing**: OpenCV + Pillow (PIL for Chinese text rendering)
- **Dataset**: TT100K (Tsinghua-Tencent 100K), 221 classes, auto-downloads on first training
- **Label format**: YOLO TXT (`<class_id> <x_center> <y_center> <width> <height>`, normalized 0-1)

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the GUI application
python MainProgram.py

# Standalone detection scripts (no GUI required)
python imgTest.py          # Single image test
python VideoTest.py        # Video file detection
python CameraTest.py       # Real-time camera detection

# Dataset auto-downloads on first training run
python -c "from ultralytics import YOLO; YOLO('yolov8s.pt').train(data='datasets/dataset/data.yaml', epochs=1)"
```

## Architecture

```
MainProgram.py          — Entry point. MainWindow(QMainWindow) loads YOLO model, handles all detection modes
├── Config.py           — Model path, class names (EN/CH), category groups, save path
├── detect_tools.py     — Utilities: drawRectBox(), img_cvread(), cvimg_to_qpiximg(), Colors class
├── UIProgram/
│   ├── UiMain.py       — pyuic5-compiled UI (auto-generated from UiMain.ui, do not edit manually)
│   ├── style.css       — QSS stylesheet
│   ├── QssLoader.py    — Reads QSS files
│   └── precess_bar.py  — Progress bar dialog for video save
└── datasets/dataset/   — Data pipeline scripts and dataset files
```

**Data flow**: Input (image/video/camera frame) → YOLO model inference → `results.boxes` parsed (xyxy coords, class IDs, confidences) → OpenCV/PIL rendering → QPixmap display in QLabel.

**Key patterns**:
- Model is loaded once in `MainWindow.initMain()` and warmed up with a dummy inference
- Video/camera uses `QTimer` + `open_frame()` loop; video saving uses `btn2Thread(QThread)` with `pyqtSignal(int, int)` for progress
- Chinese file paths handled via `cv2.imdecode(np.fromfile(...))` in `detect_tools.img_cvread()`
- Detection results reference `Config.names` (English) and `Config.CH_names` (Chinese) by class ID index
- Category percentages calculated from `Config.category_groups` mapping (限速 0-9, 限重 10-13, 禁令指示 14-26, 警告 27-44)

## Dataset: TT100K

- **Source**: [Tsinghua-Tencent 100K](https://cg.cs.tsinghua.edu.cn/traffic-sign/)
- **221 classes** (Ultralytics standard)
- **Auto-download**: Training with `data='datasets/dataset/data.yaml'` auto-downloads and converts the dataset
- **Download URL**: `https://cg.cs.tsinghua.edu.cn/traffic-sign/data_model_code/data.zip`
- **Output**: `datasets/dataset/TT100K/images/{train,val,test}/` + `labels/{train,val,test}/`

## Key Files to Modify When Adding/Changing Classes

1. `Config.py` — `names` dict, `CH_names` dict, `category_groups` dict
2. `datasets/dataset/data.yaml` — class names list and `nc` count

## UI Notes

- `UiMain.py` is auto-generated from `UiMain.ui` — edit the `.ui` file in Qt Designer, then recompile: `pyuic5 -o UiMain.py UiMain.ui`
- Fixed window size: 1250x830
- Display area: 770x480, aspect-ratio preserved via `get_resize_size()`
