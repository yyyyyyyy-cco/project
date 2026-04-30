# 交通标志识别系统

基于 YOLOv8 + PyQt5 的中国交通标志实时检测桌面应用，使用 TT100K 数据集训练。

## 功能

- 单张图片检测
- 视频文件逐帧检测
- 摄像头实时检测
- 批量文件夹检测
- 检测结果保存
- 221 类交通标志识别（限速/限重/禁令/指示/警告）

## 环境要求

- Python 3.10
- CUDA 11.8+（GPU 推理加速，可选）

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yyyyyyyy-cco/project.git
cd project
```

### 2. 创建 conda 环境并激活

```bash
conda env create -f environment.yml
conda activate traffic-sign
```

> 如果 `environment.yml` 安装失败，可以手动创建：
>
> ```bash
> conda create -n traffic-sign python=3.10 -y
> conda activate traffic-sign
> pip install -r requirements.txt
> ```

### 3. 验证环境

```bash
python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'); import ultralytics; print('YOLOv8:', ultralytics.__version__)"
```

预期输出 `CUDA: True`。如果显示 `False`，说明 PyTorch 安装的是 CPU 版本，需要重新安装：

```bash
pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu121
```

> 如需编辑 `.ui` 界面文件，可额外安装 `pip install pyqt5-tools`，运行时不需要。

### 4. 训练模型

首次训练会自动下载 TT100K 数据集（约 18GB），无需手动操作。

```bash
# 默认参数训练（YOLOv8s, 300 epochs, 640px）
python train.py

# 自定义参数
python train.py --epochs 100 --batch 8 --imgsz 1280

# 使用 CPU 训练（不推荐，非常慢）
python train.py --device cpu
```

训练完成后，`best.pt` 会自动复制到 `models/best.pt`。

### 5. 运行应用

```bash
# GUI 桌面应用
python MainProgram.py

# 或使用独立测试脚本
python imgTest.py       # 单图检测
python VideoTest.py     # 视频检测
python CameraTest.py    # 摄像头检测
```

## 项目结构

```text
project/
├── MainProgram.py               # 主程序入口（PyQt5 主窗口）
├── Config.py                    # 配置文件（模型路径、类别名称）
├── detect_tools.py              # 检测工具函数
├── imgTest.py                   # 单图测试脚本
├── CameraTest.py                # 摄像头实时检测脚本
├── VideoTest.py                 # 视频文件检测脚本
├── requirements.txt             # Python 依赖
├── UIProgram/
│   ├── UiMain.ui                # Qt Designer 界面文件
│   ├── UiMain.py                # pyuic5 编译后的 UI 代码
│   ├── style.css                # QSS 样式表
│   ├── QssLoader.py             # 样式加载器
│   └── precess_bar.py           # 进度条对话框
├── datasets/
│   └── dataset/
│       ├── data.yaml            # YOLO 数据集配置（训练时自动下载 TT100K）
│       ├── TT100K/              # 数据集（训练时自动生成）
│       ├── images/              # 划分后的图片（自动生成）
│       └── labels/              # 划分后的标签（自动生成）
├── models/
│   └── best.pt                  # 训练好的模型权重（需训练）
├── Font/
│   └── platech.ttf              # 中文字体文件
├── save_data/                   # 检测结果保存目录
└── test-file/                   # 测试图片/视频
```

## 数据集

使用 [TT100K](https://cg.cs.tsinghua.edu.cn/traffic-sign/)（清华-腾讯交通标志数据集），221 类。训练时自动下载。

| 分组 | 类别数 | 示例 |
| ---- | ---- | ---- |
| 限速标志 | 10 | pl20, pl30, ..., pl120 |
| 限重标志 | 4 | pm10, pm20, pm30, pm55 |
| 禁令/指示 | 13 | pn, pne, ps, io, ip, ... |
| 警告标志 | 18 | w1, w3, w8, w10, w13, ... |

## UI 界面

![UI Layout](docs/ui_layout.png)

- 左侧：图片/视频显示区域 + 检测详情表
- 右侧：输入方式选择、检测结果信息、各类别占比进度条

## 许可证

本项目仅供学习和研究使用。TT100K 数据集的使用请遵循其官方协议。
