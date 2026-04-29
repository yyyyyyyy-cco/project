# -*- coding: utf-8 -*-
"""
单图测试脚本
用于快速验证模型检测效果，不依赖 GUI。

使用方法：
    python imgTest.py
"""

import cv2
import time
from ultralytics import YOLO
import Config

if __name__ == '__main__':
    # 加载模型
    print('Loading model...')
    model = YOLO(Config.model_path, task='detect')

    # 测试图片路径（修改为实际路径）
    img_path = 'test-file/images/test.jpg'

    print(f'Testing image: {img_path}')
    t1 = time.time()
    results = model(img_path)[0]
    t2 = time.time()
    print(f'Inference time: {t2 - t1:.3f} s')

    # 解析结果
    location_list = results.boxes.xyxy.tolist()
    cls_list = results.boxes.cls.tolist()
    conf_list = results.boxes.conf.tolist()

    print(f'Detected {len(location_list)} objects:')
    for i, (loc, cls, conf) in enumerate(zip(location_list, cls_list, conf_list)):
        cls_id = int(cls)
        print(f'  {i + 1}. {Config.CH_names[cls_id]} ({Config.names[cls_id]}) '
              f'- Confidence: {conf:.2%} - Location: {list(map(int, loc))}')

    # 显示结果图片
    now_img = results.plot()
    cv2.imshow('Detection Result', now_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
