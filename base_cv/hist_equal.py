"""
参考：https://zhuanlan.zhihu.com/p/44918476
http://www.cs.utah.edu/~sujin/courses/reports/cs6640/project2/ahe.html
直方图均衡化(Histogram Equalization)是一种增强图像对比度(Image Contrast)的方法
其主要思想是将一副图像的直方图分布变成近似均匀分布，从而增强图像的对比度
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps


def plt_hist(img):
    img = np.array(img)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.subplot(1, 2, 2)
    plt.xlim(0, 256)  # x 范围
    plt.hist(img.ravel(), 256)  # 拉成 1 维
    plt.show()


if __name__ == '__main__':
    img = Image.open('imgs/car.png')
    plt_hist(img)
    # 直方图均衡化 HE
    eq_img = ImageOps.equalize(img)  # PIL Image
    plt_hist(eq_img)
