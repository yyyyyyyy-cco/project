"""
数据集划分脚本
将图片和标签按 70% 训练 / 10% 验证 / 20% 测试 的比例划分。

使用方法：
    1. 先运行 xml2txt.py 生成 YOLO TXT 标签
    2. 运行本脚本：python split_data.py
    3. 划分结果会自动复制到 images/ 和 labels/ 目录
"""

import os
import shutil
import random
import numpy as np

random.seed(0)

# 划分比例
val_size = 0.1
test_size = 0.2

# 路径配置
base_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(base_dir, 'CCTSDB', 'JPEGImages')
txt_path = os.path.join(base_dir, 'CCTSDB', 'txt')
postfix = 'jpg'

# 创建输出目录
for split in ['train', 'val', 'test']:
    os.makedirs(os.path.join(base_dir, 'images', split), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'labels', split), exist_ok=True)

# 获取所有标签文件
txt_files = np.array([f for f in os.listdir(txt_path) if f.endswith('.txt')])
random.shuffle(txt_files)

# 划分数据集
n = len(txt_files)
n_train = int(n * (1 - val_size - test_size))
n_val = int(n * val_size)

train_files = txt_files[:n_train]
val_files = txt_files[n_train:n_train + n_val]
test_files = txt_files[n_train + n_val:]

print(f'Total: {n}')
print(f'Train: {len(train_files)}')
print(f'Val:   {len(val_files)}')
print(f'Test:  {len(test_files)}')

# 复制文件
for split_name, file_list in [('train', train_files), ('val', val_files), ('test', test_files)]:
    for txt_file in file_list:
        img_name = '{}.{}'.format(txt_file[:-4], postfix)
        src_img = os.path.join(img_path, img_name)
        src_txt = os.path.join(txt_path, txt_file)
        dst_img = os.path.join(base_dir, 'images', split_name, img_name)
        dst_txt = os.path.join(base_dir, 'labels', split_name, txt_file)

        if os.path.exists(src_img):
            shutil.copy(src_img, dst_img)
            shutil.copy(src_txt, dst_txt)
        else:
            print(f'Warning: Image not found: {src_img}')

print('\nDataset split complete!')
print(f'Output: {base_dir}/images/ and {base_dir}/labels/')
