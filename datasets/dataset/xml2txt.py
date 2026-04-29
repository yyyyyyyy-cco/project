"""
VOC XML → YOLO TXT 格式转换脚本
将 CCTSDB 数据集的 Pascal VOC XML 标注转换为 YOLO TXT 格式。

使用方法：
    1. 将 CCTSDB 图片放入 CCTSDB/JPEGImages/
    2. 将 CCTSDB 标注放入 CCTSDB/Annotations/
    3. 运行本脚本：python xml2txt.py
"""

import xml.etree.ElementTree as ET
import os
import cv2
import numpy as np

# CCTSDB 交通标志类别（按 GB 5768 国标分类）
# 如果实际数据集类别不同，请根据实际情况修改此列表
CLASSES = [
    # 禁令标志
    'speed_limit_20', 'speed_limit_30', 'speed_limit_40',
    'speed_limit_50', 'speed_limit_60', 'speed_limit_70',
    'speed_limit_80', 'speed_limit_100', 'speed_limit_120',
    'no_entry', 'no_turn_left', 'no_turn_right',
    'no_u_turn', 'no_overtaking', 'no_honking',
    'no_parking', 'no_stopping', 'weight_limit', 'height_limit',
    # 指示标志
    'go_straight', 'turn_left', 'turn_right',
    'turn_left_right', 'u_turn', 'roundabout',
    'pedestrian_crossing', 'bicycle_lane', 'motorway', 'parking',
    # 警告标志
    'crosswalk_warning', 'curve_left', 'curve_right',
    'steep_hill', 'road_work', 'traffic_light_ahead',
    'falling_rocks', 'slippery_road', 'school_zone', 'intersection',
    # 其他标志
    'stop_sign', 'yield_sign', 'guide_sign', 'highway_sign',
]

# 如果 CCTSDB 使用中文类别名或简化类别名，在此建立映射
# 根据实际下载的数据集标注格式修改
CLASS_MAPPING = {
    # CCTSDB 常见标注名 → 标准英文名
    # 示例（需根据实际数据集调整）：
    # 'prohibitory': 'speed_limit_50',
    # 'warning': 'crosswalk_warning',
    # 'mandatory': 'go_straight',
}


def convert(size, box):
    """将 VOC 格式的边界框转换为 YOLO 格式"""
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(xml_path, xml_name, img_path, txt_path, postfix='jpg'):
    """转换单个 XML 标注文件为 YOLO TXT 格式"""
    with open(xml_path, "r", encoding='utf-8') as in_file:
        txt_name = xml_name[:-4] + '.txt'
        txt_file = os.path.join(txt_path, txt_name)
        tree = ET.parse(in_file)
        root = tree.getroot()

        # 读取图片获取尺寸
        img_file = os.path.join(img_path, '{}.{}'.format(xml_name[:-4], postfix))
        img = cv2.imdecode(np.fromfile(img_file, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            print(f'Warning: Cannot read image {img_file}, skipping.')
            return
        h, w = img.shape[:2]

        res = []
        for obj in root.iter('object'):
            cls = obj.find('name').text

            # 应用类别映射（如果需要）
            if cls in CLASS_MAPPING:
                cls = CLASS_MAPPING[cls]

            # 查找类别索引
            if cls in CLASSES:
                cls_id = CLASSES.index(cls)
            else:
                print(f'Warning: Unknown class "{cls}" in {xml_name}, skipping object.')
                continue

            xmlbox = obj.find('bndbox')
            b = (
                float(xmlbox.find('xmin').text),
                float(xmlbox.find('xmax').text),
                float(xmlbox.find('ymin').text),
                float(xmlbox.find('ymax').text)
            )
            bb = convert((w, h), b)
            res.append(str(cls_id) + " " + " ".join([str(a) for a in bb]))

        if len(res) != 0:
            with open(txt_file, 'w+') as f:
                f.write('\n'.join(res))


if __name__ == "__main__":
    # 路径配置
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(base_dir, 'CCTSDB', 'JPEGImages')
    xml_path = os.path.join(base_dir, 'CCTSDB', 'Annotations')
    txt_path = os.path.join(base_dir, 'CCTSDB', 'txt')

    postfix = 'jpg'

    if not os.path.exists(txt_path):
        os.makedirs(txt_path, exist_ok=True)

    xml_list = os.listdir(xml_path)
    error_files = []
    success_count = 0

    for i, xml_name in enumerate(xml_list):
        try:
            full_path = os.path.join(xml_path, xml_name)
            if xml_name.lower().endswith('.xml'):
                convert_annotation(full_path, xml_name, img_path, txt_path, postfix)
                success_count += 1
                if (i + 1) % 100 == 0:
                    print(f'Progress: {i + 1}/{len(xml_list)}')
            else:
                print(f'Skipping non-XML file: {xml_name}')
        except Exception as e:
            print(f'Error converting {xml_name}: {e}')
            error_files.append(xml_name)

    print(f'\nConversion complete!')
    print(f'Success: {success_count}')
    print(f'Errors: {len(error_files)}')
    if error_files:
        print(f'Error files: {error_files}')
    print(f'Dataset classes ({len(CLASSES)}): {CLASSES}')
