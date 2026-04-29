"""
CCTSDB 数据集下载脚本
从 GitHub 逐个下载图片和标注文件。

使用方法：
    python download_cctsdb.py

注意：下载约 15,000 张图片需要较长时间（约 1-2 小时，取决于网速）
"""

import os
import urllib.request
import time

# 配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, 'CCTSDB')
IMG_DIR = os.path.join(SAVE_DIR, 'JPEGImages')
GT_DIR = os.path.join(SAVE_DIR, 'Annotations')

# GitHub raw 文件基础 URL
GITHUB_RAW = "https://raw.githubusercontent.com/csust7zhangjm/CCTSDB/master"

# 图片目录列表
IMAGE_DIRS = [
    'image0000-0999', 'image1000-1999', 'image2000-2999', 'image3000-3999',
    'image4000-4999', 'image5000-5999', 'image6000-6999', 'image7000-7999',
    'image8000-8999', 'image9000-9999', 'image10000-10999', 'image11000-11999',
    'image12000-12999', 'image13000-13999', 'image14000-14999', 'image15000-15999',
]

# Ground truth 文件
GT_FILES = [
    'groundtruth0000-9999.txt',
]


def download_file(url, save_path, retries=3):
    """下载单个文件，支持重试"""
    for attempt in range(retries):
        try:
            urllib.request.urlretrieve(url, save_path)
            return True
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1)
            else:
                print(f'Failed to download {url}: {e}')
                return False
    return False


def download_ground_truth():
    """下载标注文件"""
    print('Downloading ground truth files...')
    os.makedirs(GT_DIR, exist_ok=True)

    for gt_file in GT_FILES:
        url = f'{GITHUB_RAW}/GroundTruth/{gt_file}'
        save_path = os.path.join(GT_DIR, gt_file)
        if os.path.exists(save_path):
            print(f'  Already exists: {gt_file}')
            continue
        print(f'  Downloading: {gt_file}')
        download_file(url, save_path)
    print('Ground truth download complete.\n')


def download_images():
    """下载所有图片"""
    print('Downloading images...')
    os.makedirs(IMG_DIR, exist_ok=True)

    total = 0
    failed = 0

    for img_dir in IMAGE_DIRS:
        # 获取目录中的文件列表
        api_url = f'https://api.github.com/repos/csust7zhangjm/CCTSDB/contents/{img_dir}'
        try:
            req = urllib.request.Request(api_url)
            with urllib.request.urlopen(req) as resp:
                import json
                files = json.loads(resp.read())
        except Exception as e:
            print(f'Error fetching file list for {img_dir}: {e}')
            continue

        print(f'\nProcessing {img_dir} ({len(files)} files)...')

        for i, f in enumerate(files):
            if not f['name'].endswith('.png'):
                continue

            save_path = os.path.join(IMG_DIR, f['name'])
            if os.path.exists(save_path):
                total += 1
                continue

            url = f'{GITHUB_RAW}/{img_dir}/{f["name"]}'
            if download_file(url, save_path):
                total += 1
            else:
                failed += 1

            if (i + 1) % 100 == 0:
                print(f'  Progress: {i + 1}/{len(files)} in {img_dir} (Total: {total})')

    print(f'\nImage download complete!')
    print(f'Total downloaded: {total}')
    print(f'Failed: {failed}')


if __name__ == '__main__':
    print('=' * 50)
    print('CCTSDB Dataset Downloader')
    print('=' * 50)
    print(f'Save directory: {SAVE_DIR}')
    print()

    download_ground_truth()
    download_images()

    print('\nDone! Dataset saved to:', SAVE_DIR)
