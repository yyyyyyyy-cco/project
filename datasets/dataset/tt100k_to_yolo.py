"""
TT100K JSON → YOLO TXT 格式转换脚本
将 TT100K 数据集的 JSON 标注转换为 YOLO TXT 格式。

使用方法：
    1. 下载 TT100K 数据集，解压到 TT100K/ 目录
    2. 运行本脚本：python tt100k_to_yolo.py
    3. 转换后的标签保存在 labels_temp/ 目录
    4. 再运行 split_data.py 划分 train/val/test
"""

import json
import os
import cv2
import numpy as np

# TT100K 过滤后的 45 类（Ultralytics 标准，去掉样本数 < 100 的类别）
CLASSES = [
    'pl100', 'pl120', 'pl20', 'pl30', 'pl40', 'pl5', 'pl50', 'pl60', 'pl70', 'pl80',
    'pm10', 'pm20', 'pm30', 'pm55',
    'p11', 'p12', 'p19', 'p23', 'p26', 'p27', 'p3', 'p5', 'p6',
    'pn', 'pne', 'ps', 'pw3',
    'w1', 'w10', 'w12', 'w13', 'w14', 'w15', 'w16', 'w18', 'w19',
    'w20', 'w21', 'w22', 'w3', 'w30', 'w32', 'w34', 'w35', 'w55',
]

# 类别中文名映射
CLASS_NAMES_CN = {
    'pl100': '限速100', 'pl120': '限速120', 'pl20': '限速20', 'pl30': '限速30',
    'pl40': '限速40', 'pl5': '限速5', 'pl50': '限速50', 'pl60': '限速60',
    'pl70': '限速70', 'pl80': '限速80',
    'pm10': '限重10', 'pm20': '限重20', 'pm30': '限重30', 'pm55': '限重55',
    'p11': '自行车通行', 'p12': '步行', 'p19': '掉头', 'p23': '直行',
    'p26': '右转', 'p27': '左转', 'p3': '机动车进入', 'p5': '靠右行驶',
    'p6': '靠左行驶',
    'pn': '禁止通行', 'pne': '禁止驶入', 'ps': '停车让行', 'pw3': '鸣笛',
    'w1': '交叉路口', 'w10': '信号灯', 'w12': '路拱', 'w13': '注意行人',
    'w14': '注意儿童', 'w15': '自行车', 'w16': '注意动物', 'w18': '注意落石',
    'w19': '注意横风', 'w20': '易滑', 'w21': '傍山险路', 'w22': '施工路段',
    'w3': '连续弯路', 'w30': '注意危险', 'w32': '隧道', 'w34': '铁道路口',
    'w35': '路面不平', 'w55': '减速让行',
}


def get_image_size(img_path):
    """获取图片尺寸"""
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return None, None
    h, w = img.shape[:2]
    return w, h


def convert_bbox_to_yolo(bbox, img_w, img_h):
    """
    将 TT100K 的 [x, y, w, h] 绝对坐标转换为 YOLO 归一化格式
    TT100K bbox: [x, y, w, h] 其中 (x, y) 是左上角
    YOLO: <x_center> <y_center> <width> <height> 归一化到 [0, 1]
    """
    x, y, w, h = bbox
    x_center = (x + w / 2) / img_w
    y_center = (y + h / 2) / img_h
    norm_w = w / img_w
    norm_h = h / img_h
    return x_center, y_center, norm_w, norm_h


def convert_split(annotations_path, images_dir, output_dir):
    """转换一个数据集划分（train 或 test）的标注"""
    with open(annotations_path, 'r', encoding='utf-8') as f:
        annotations = json.load(f)

    os.makedirs(output_dir, exist_ok=True)

    converted = 0
    skipped_class = 0
    skipped_img = 0
    skipped_small = 0
    min_size = 6  # 过滤过小的标注框

    for img_name, objects in annotations.items():
        img_path = os.path.join(images_dir, img_name)
        if not os.path.exists(img_path):
            skipped_img += 1
            continue

        img_w, img_h = get_image_size(img_path)
        if img_w is None:
            skipped_img += 1
            continue

        yolo_lines = []
        for obj in objects:
            category = obj['category']
            if category not in CLASSES:
                skipped_class += 1
                continue

            cls_id = CLASSES.index(category)
            bbox = obj['bbox']

            # 过滤过小的标注框
            if bbox[2] < min_size or bbox[3] < min_size:
                skipped_small += 1
                continue

            x_c, y_c, w, h = convert_bbox_to_yolo(bbox, img_w, img_h)

            # 确保坐标在 [0, 1] 范围内
            x_c = max(0, min(1, x_c))
            y_c = max(0, min(1, y_c))
            w = max(0, min(1, w))
            h = max(0, min(1, h))

            yolo_lines.append(f'{cls_id} {x_c:.6f} {y_c:.6f} {w:.6f} {h:.6f}')

        if yolo_lines:
            txt_name = os.path.splitext(img_name)[0] + '.txt'
            txt_path = os.path.join(output_dir, txt_name)
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(yolo_lines))
            converted += 1

    return converted, skipped_class, skipped_img, skipped_small


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    tt100k_dir = os.path.join(base_dir, 'TT100K')

    if not os.path.exists(tt100k_dir):
        print(f'Error: TT100K directory not found: {tt100k_dir}')
        print('Please download TT100K dataset and place it in this directory.')
        print('Download: https://cg.cs.tsinghua.edu.cn/traffic-sign/')
        exit(1)

    output_dir = os.path.join(base_dir, 'labels_temp')

    total_converted = 0
    total_skipped_class = 0
    total_skipped_img = 0
    total_skipped_small = 0

    # 转换 train 集
    train_ann = os.path.join(tt100k_dir, 'train', 'annotations.json')
    train_img = os.path.join(tt100k_dir, 'train', 'images')
    if os.path.exists(train_ann):
        print(f'Converting train set: {train_ann}')
        c, sc, si, ss = convert_split(train_ann, train_img, output_dir)
        total_converted += c
        total_skipped_class += sc
        total_skipped_img += si
        total_skipped_small += ss
        print(f'  Converted: {c} images')
    else:
        print(f'Warning: {train_ann} not found')

    # 转换 test 集
    test_ann = os.path.join(tt100k_dir, 'test', 'annotations.json')
    test_img = os.path.join(tt100k_dir, 'test', 'images')
    if os.path.exists(test_ann):
        print(f'Converting test set: {test_ann}')
        c, sc, si, ss = convert_split(test_ann, test_img, output_dir)
        total_converted += c
        total_skipped_class += sc
        total_skipped_img += si
        total_skipped_small += ss
        print(f'  Converted: {c} images')
    else:
        print(f'Warning: {test_ann} not found')

    print(f'\nConversion complete!')
    print(f'Total converted: {total_converted} images')
    print(f'Skipped (unknown class): {total_skipped_class} objects')
    print(f'Skipped (image not found): {total_skipped_img} images')
    print(f'Skipped (bbox too small): {total_skipped_small} objects')
    print(f'Classes: {len(CLASSES)}')
    print(f'Output: {output_dir}')
    print(f'\nNext step: run python split_data.py')
