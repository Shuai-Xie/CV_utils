"""
通过 迭代式减去边缘，将粗线变细
"""
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np

img_dir = 'match_road/examples'

examples = [
    '13039-3431',
    '13039-3433',
    '13040-3431',
    '13040-3432'
]

for eg in examples:
    img = cv2.imread(f'{img_dir}/{eg}_img.png', cv2.IMREAD_UNCHANGED)
    msk = cv2.imread(f'{img_dir}/{eg}_msk.png', cv2.IMREAD_UNCHANGED)

    # img = cv2.GaussianBlur(img, (3, 3), 0)
    for _ in range(20):
        plt.imshow(img, cmap='gray')
        plt.show()
        edges = cv2.Canny(img, threshold1=50, threshold2=150, apertureSize=7)
        # plt.imshow(edges, cmap='gray')
        # plt.show()
        tmp = np.zeros_like(img, dtype='uint8')
        tmp[(img > 0) & (img != edges)] = 255  # 是前景，并且不是边界
        img = tmp

    # # msk = cv2.GaussianBlur(msk, (3, 3), 0)
    # plt.imshow(msk, cmap='gray')
    # plt.show()
    # msk = cv2.Canny(msk, threshold1=50, threshold2=150, apertureSize=3)
    # plt.imshow(msk, cmap='gray')
    # plt.show()
    #
    # exit(0)
