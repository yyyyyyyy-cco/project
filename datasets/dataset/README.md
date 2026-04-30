# TT100K 数据集说明

## 概述

使用 [TT100K](https://cg.cs.tsinghua.edu.cn/traffic-sign/)（清华-腾讯交通标志数据集），221 类交通标志。

## 自动下载

训练时 Ultralytics 会自动下载并转换数据集，无需手动操作：

```bash
python -c "from ultralytics import YOLO; YOLO('yolov8s.pt').train(data='datasets/dataset/data.yaml', epochs=1)"
```

下载地址：`https://cg.cs.tsinghua.edu.cn/traffic-sign/data_model_code/data.zip`（约 18GB）

## 自动生成的目录结构

```text
datasets/dataset/TT100K/
├── images/
│   ├── train/          # 训练集图片（6105 张）
│   ├── val/            # 验证集图片（7641 张）
│   └── test/           # 测试集图片（3071 张）
└── labels/
    ├── train/          # 训练集标签（YOLO TXT）
    ├── val/            # 验证集标签
    └── test/           # 测试集标签
```

## 手动下载（可选）

如果自动下载失败，可手动下载：

1. 访问 [TT100K 官方页面](https://cg.cs.tsinghua.edu.cn/traffic-sign/)
2. 下载 `data.zip` 并解压到 `datasets/dataset/TT100K/`
3. 运行训练命令，Ultralytics 会自动转换标注格式
