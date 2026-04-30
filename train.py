# -*- coding: utf-8 -*-
"""
交通标志识别模型训练脚本

用法:
    python train.py                      # 使用默认参数训练
    python train.py --epochs 100         # 自定义训练轮数
    python train.py --batch 8 --imgsz 1280  # 自定义 batch 和输入尺寸

首次运行会自动下载 TT100K 数据集（约 18GB）。
"""
import argparse
import shutil
import os
from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser(description='Train YOLOv8 on TT100K')
    parser.add_argument('--model', type=str, default='yolov8s.pt',
                        help='预训练模型 (default: yolov8s.pt)')
    parser.add_argument('--data', type=str, default='datasets/dataset/data.yaml',
                        help='数据集配置文件路径')
    parser.add_argument('--epochs', type=int, default=300, help='训练轮数')
    parser.add_argument('--batch', type=int, default=16, help='batch size')
    parser.add_argument('--imgsz', type=int, default=640, help='输入图像尺寸')
    parser.add_argument('--device', type=str, default='0', help='GPU 编号，CPU 用 "cpu"')
    parser.add_argument('--patience', type=int, default=50, help='早停耐心值')
    parser.add_argument('--project', type=str, default='runs/detect', help='训练结果保存目录')
    parser.add_argument('--name', type=str, default='traffic_sign', help='训练实验名称')
    return parser.parse_args()


def main():
    args = parse_args()

    print(f'Loading model: {args.model}')
    model = YOLO(args.model)

    print(f'Starting training for {args.epochs} epochs...')
    results = model.train(
        data=args.data,
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz,
        device=args.device,
        patience=args.patience,
        project=args.project,
        name=args.name,
        optimizer='SGD',
        lr0=0.01,
        lrf=0.01,
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=3.0,
        warmup_momentum=0.8,
        warmup_bias_lr=0.1,
        mosaic=1.0,
        mixup=0.0,
        fliplr=0.5,
        scale=0.5,
        translate=0.1,
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=10.0,
        amp=True,
        workers=8,
        pretrained=True,
        exist_ok=True,
    )

    # Copy best.pt to models/
    best_src = os.path.join(args.project, args.name, 'weights', 'best.pt')
    best_dst = os.path.join('models', 'best.pt')
    if os.path.exists(best_src):
        os.makedirs('models', exist_ok=True)
        shutil.copy2(best_src, best_dst)
        print(f'\nBest model saved to: {best_dst}')
    else:
        print(f'\nWarning: best.pt not found at {best_src}')

    print('Training complete!')


if __name__ == '__main__':
    main()
