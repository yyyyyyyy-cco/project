"""
CCTSDB 数据集快速下载脚本（多线程并发）

使用方法：
    python download_cctsdb_fast.py
"""

import os
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, 'CCTSDB')
IMG_DIR = os.path.join(SAVE_DIR, 'JPEGImages')
GT_DIR = os.path.join(SAVE_DIR, 'Annotations')

GITHUB_RAW = "https://raw.githubusercontent.com/csust7zhangjm/CCTSDB/master"
GITHUB_API = "https://api.github.com/repos/csust7zhangjm/CCTSDB/contents"

IMAGE_DIRS = [
    'image0000-0999', 'image1000-1999', 'image2000-2999', 'image3000-3999',
    'image4000-4999', 'image5000-5999', 'image6000-6999', 'image7000-7999',
    'image8000-8999', 'image9000-9999', 'image10000-10999', 'image11000-11999',
    'image12000-12999', 'image13000-13999', 'image14000-14999', 'image15000-15999',
]


def download_one(args):
    """下载单个文件"""
    url, save_path = args
    if os.path.exists(save_path):
        return True
    try:
        urllib.request.urlretrieve(url, save_path)
        return True
    except Exception:
        return False


def get_file_list(dir_name):
    """获取目录中的文件列表"""
    url = f'{GITHUB_API}/{dir_name}'
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'CCTSDB-Downloader')
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f'Error fetching {dir_name}: {e}')
        return []


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(GT_DIR, exist_ok=True)

    # 下载 ground truth
    print('Downloading ground truth...')
    gt_file = 'groundtruth0000-9999.txt'
    gt_path = os.path.join(GT_DIR, gt_file)
    if not os.path.exists(gt_path):
        urllib.request.urlretrieve(f'{GITHUB_RAW}/GroundTruth/{gt_file}', gt_path)
        print('  Ground truth downloaded.')
    else:
        print('  Ground truth already exists.')

    # 收集所有下载任务
    print('\nCollecting file lists...')
    tasks = []
    for img_dir in IMAGE_DIRS:
        files = get_file_list(img_dir)
        for f in files:
            if f['name'].endswith('.png'):
                url = f'{GITHUB_RAW}/{img_dir}/{f["name"]}'
                save_path = os.path.join(IMG_DIR, f['name'])
                tasks.append((url, save_path))
        print(f'  {img_dir}: {len(files)} files')

    print(f'\nTotal files to download: {len(tasks)}')
    print('Starting concurrent download (8 threads)...\n')

    # 多线程下载
    success = 0
    failed = 0
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(download_one, t): t for t in tasks}
        for i, future in enumerate(as_completed(futures)):
            if future.result():
                success += 1
            else:
                failed += 1

            if (i + 1) % 500 == 0:
                elapsed = time.time() - start_time
                rate = (i + 1) / elapsed
                remaining = (len(tasks) - i - 1) / rate / 60
                print(f'  Progress: {i + 1}/{len(tasks)} '
                      f'(Success: {success}, Failed: {failed}) '
                      f'[{rate:.1f} files/s, ~{remaining:.0f} min remaining]')

    elapsed = time.time() - start_time
    print(f'\nDownload complete!')
    print(f'Time: {elapsed / 60:.1f} minutes')
    print(f'Success: {success}')
    print(f'Failed: {failed}')
    print(f'Saved to: {IMG_DIR}')


if __name__ == '__main__':
    main()
