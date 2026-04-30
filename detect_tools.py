# encoding: utf-8
import cv2
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import csv
import os


def cv_show(name, img):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def drawRectBox(image, rect, addText, fontC, color):
    """
    绘制矩形框与结果
    :param image: 原始图像
    :param rect: 矩形框坐标, int类型
    :param addText: 类别名称
    :param fontC: 字体
    :param color: 颜色 (B, G, R)
    :return: 绘制后的图像
    """
    cv2.rectangle(image, (rect[0], rect[1]),
                  (rect[2], rect[3]),
                  color, 2)
    cv2.rectangle(image, (rect[0] - 1, rect[1] - 25),
                  (rect[0] + 60, rect[1]), color, -1, cv2.LINE_AA)

    img = Image.fromarray(image)
    draw = ImageDraw.Draw(img)
    draw.text((rect[0] + 2, rect[1] - 27), addText, (255, 255, 255), font=fontC)
    imagex = np.array(img)
    return imagex


def img_cvread(path):
    """读取含中文名的图片文件"""
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    return img


def cvimg_to_qpiximg(cvimg):
    """OpenCV 图像转 QPixmap"""
    height, width, depth = cvimg.shape
    cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
    qimg = QImage(cvimg.data, width, height, width * depth, QImage.Format_RGB888)
    qpix_img = QPixmap(qimg)
    return qpix_img


def cv2AddChineseText(img, text, position, textColor=(0, 255, 0), textSize=50):
    """图片上显示中文"""
    if isinstance(img, np.ndarray):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontStyle = ImageFont.truetype("Font/platech.ttf", textSize, encoding="utf-8")
    draw.text(position, text, textColor, font=fontStyle)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


class Colors:
    """用于绘制不同颜色"""
    def __init__(self):
        hexs = ('FF3838', 'FF9D97', 'FF701F', 'FFB21D', 'CFD231', '48F90A',
                '92CC17', '3DDB86', '1A9334', '00D4BB', '2C99A8', '00C2FF',
                '344593', '6473FF', '0018EC', '8438FF', '520085', 'CB38FF',
                'FF95C8', 'FF37C7')
        self.palette = [self.hex2rgb(f'#{c}') for c in hexs]
        self.n = len(self.palette)

    def __call__(self, i, bgr=False):
        c = self.palette[int(i) % self.n]
        return (c[2], c[1], c[0]) if bgr else c

    @staticmethod
    def hex2rgb(h):
        return tuple(int(h[1 + i:1 + i + 2], 16) for i in (0, 2, 4))


def yolo_to_location(w, h, yolo_data):
    """YOLO 格式转两点坐标"""
    x_, y_, w_, h_ = yolo_data
    x1 = int(w * x_ - 0.5 * w * w_)
    x2 = int(w * x_ + 0.5 * w * w_)
    y1 = int(h * y_ - 0.5 * h * h_)
    y2 = int(h * y_ + 0.5 * h * h_)
    return [x1, y1, x2, y2]


def location_to_yolo(w, h, locations):
    """两点坐标转 YOLO 格式"""
    x1, y1, x2, y2 = locations
    x_ = (x1 + x2) / 2 / w
    y_ = (y1 + y2) / 2 / h
    w_ = (x2 - x1) / w
    h_ = (y2 - y1) / h
    return [float(f'{x_:.5f}'), float(f'{y_:.5f}'),
            float(f'{w_:.5f}'), float(f'{h_:.5f}')]
