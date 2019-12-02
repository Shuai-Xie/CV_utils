"""
https://www.jianshu.com/p/5076a98db2d7
"""
import numpy as np
import matplotlib.pyplot as plt


def flat_one_dim():
    img = plt.imread('imgs/depth.png')
    print(type(img))
    exit(0)
    img = (plt.imread('1.gif')).astype(np.float64)
    print(img.shape)
    print(img[4][50])  # 老矩阵任取一点

    img = img.reshape((1, img.shape[0] * img.shape[1], img.shape[2])).squeeze()
    print(img.shape)
    print(img[4 * 64 + 50])  # 新矩阵取同一点


if __name__ == '__main__':
    flat_one_dim()
