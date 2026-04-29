# -*- coding: utf-8 -*-
"""
摄像头实时检测脚本
独立运行，不依赖 GUI。

使用方法：
    python CameraTest.py
    按 'q' 退出
"""

import cv2
import time
from ultralytics import YOLO
import Config

if __name__ == '__main__':
    # 加载模型
    print('Loading model...')
    model = YOLO(Config.model_path, task='detect')

    # 自动检测可用摄像头
    cap = None
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f'Camera found at index {i}')
            break
        cap.release()
        cap = None

    if cap is None:
        print('Error: No camera found!')
        exit(1)

    print('Press "q" to quit')

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        t1 = time.time()
        results = model(frame)[0]
        t2 = time.time()

        # 绘制结果
        now_img = results.plot()

        # 显示推理时间
        fps = 1.0 / (t2 - t1)
        cv2.putText(now_img, f'FPS: {fps:.1f}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Traffic Sign Detection', now_img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
