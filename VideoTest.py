# -*- coding: utf-8 -*-
"""
视频文件检测脚本
独立运行，不依赖 GUI。

使用方法：
    python VideoTest.py
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

    # 视频路径（修改为实际路径）
    video_path = 'test-file/videos/test.mp4'

    print(f'Loading video: {video_path}')
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f'Error: Cannot open video {video_path}')
        exit(1)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f'Video: {total_frames} frames, {fps:.1f} FPS')
    print('Press "q" to quit')

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        t1 = time.time()
        results = model(frame)[0]
        t2 = time.time()

        now_img = results.plot()

        # 显示帧数和推理时间
        inference_fps = 1.0 / (t2 - t1)
        cv2.putText(now_img, f'Frame: {frame_count}/{total_frames}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(now_img, f'FPS: {inference_fps:.1f}', (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow('Traffic Sign Detection', now_img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f'Processed {frame_count} frames')
