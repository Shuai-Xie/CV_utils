import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import rotate


def gaussian2D(shape, sigma=1.0):
    m, n = [(ss - 1.) / 2. for ss in shape]  # rx, ry
    y, x = np.ogrid[-m:m + 1, -n:n + 1]  # 正交网格
    # y: (2m, 1)
    # x: (1, 2n)

    # 计算 x,y 范围内 高斯值, 广播机制
    # 2*x^2 + y^2 -> 椭圆方程，长短轴
    h = np.exp(-(x * x + y * y) / (2 * sigma * sigma))  # (2n,2m)

    h[h < np.finfo(h.dtype).eps * h.max()] = 0  # 确保剩下区域都=0
    # print(np.finfo(h.dtype).eps)  # 2.220446049250313e-16 获得 h.dtype 类型的非负最小值
    return h


def ellipse2D(a=1, b=1, angle=0):
    """
    :param a: 长轴
    :param b: 短轴
    :param angle: 逆时针旋转角度
    :return:
    """
    y, x = np.ogrid[-b:b + 1, -a:a + 1]  # h, w

    # 计算 x,y 范围内 高斯值, 广播机制
    # x^2 + y^2 正圆
    h = np.exp(-((x / a) ** 2 + (y / b) ** 2))
    h_min = h[b][0]  # 长轴边缘值

    h = rotate(h, angle)  # 会扩大原始图像

    # beign_x = (h.shape[1] - 2 * a - 1) // 2
    # beign_y = (h.shape[0] - 2 * b - 1) // 2
    # h = h[beign_y:beign_y + 2 * b + 1, beign_x:beign_x + 2 * a + 1]

    h[h < h_min] = 0  # 确保椭圆之外区域 = 0
    # h[h < np.finfo(h.dtype).eps * h.max()] = 0
    return h


if __name__ == '__main__':
    radius = 50
    diameter = 2 * radius + 1
    # heat = gaussian2D((diameter, diameter), sigma=diameter / 6)  # 3 sigma 原则
    # 长短轴 对应 长宽比
    heat = ellipse2D(a=30, b=20, angle=20)
    plt.imshow(heat, cmap='jet')
    plt.show()
