import cv2
import numpy as np

"""
ostu 图像二值化
代码：https://www.jianshu.com/p/c7fb9be02412
原理：https://www.cnblogs.com/xiaomanon/p/4110006.html
"""


def ostu_thre(img):
    """
    :param img: gray img
    :return: threshold
    """
    # gray-level histogram 灰度直方图
    MAX_VALUE = 256
    hist = np.zeros(MAX_VALUE)
    for i in range(MAX_VALUE):
        hist[i] = len(np.where(img == i)[0])

    s_max = (0, -1)  # thre, 方差
    for thre in range(MAX_VALUE):
        w0, w1 = sum(hist[:thre]), sum(hist[thre:])  # thre 上下 pixel 总数
        u0 = sum([i * hist[i] for i in range(0, thre)]) / w0 if w0 > 0 else 0  # 下平均
        u1 = sum([i * hist[i] for i in range(thre, MAX_VALUE)]) / w1 if w1 > 0 else 0  # 上平均
        u = (u0 * w0 + u1 * w1) / (w0 + w1)
        # 类间方差 由 类间均值 衡量
        # g = w0 * (u0 - u) ** 2 + w1 * (u1 - u) **2  # 原式
        g = w0 * w1 * (u0 - u1) ** 2  # 推导式
        if g > s_max[1]:
            s_max = (thre, g)

    return s_max[0]


if __name__ == '__main__':
    gray_img = cv2.imread('imgs/ticket.png', cv2.IMREAD_GRAYSCALE)
    thre = ostu_thre(gray_img)
    # 二值化
    gray_img[gray_img > thre] = 255
    gray_img[gray_img <= thre] = 0
    cv2.imwrite(f'imgs/ostu_thre_{thre}.png', gray_img)
