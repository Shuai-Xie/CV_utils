import skimage.io
import skimage.transform
import numpy as np
import matplotlib.pyplot as plt
import cv2


def cut_patches(img, patch_size, stride_x, stride_y):
    """
    cut one img into sub imgs with patch_size
    :param img: src img
    :param patch_size: sub img size, eg (160, 160) h, w
    :param stride_x: stride along x axis, eg 160
    :param stride_y: stride along y axis, eg 160
    :return: res: np.(patches_num, patch_w, patch_h, channels)
    """
    assert isinstance(patch_size, tuple) and len(patch_size) == 2
    img_h, img_w = img.shape[0], img.shape[1]
    # begin (x,y) left_top
    range_x = np.arange(0, img_w - patch_size[0], step=stride_x)
    range_y = np.arange(0, img_h - patch_size[1], step=stride_y)

    if range_x[-1] < img_w - patch_size[0]:  # stride 可能使得 arange 不能取到最右点，补充1个
        range_x = np.append(range_x, img_w - patch_size[0])
    if range_y[-1] < img_h - patch_size[1]:
        range_y = np.append(range_y, img_h - patch_size[1])

    patches = len(range_x) * len(range_y)  # sub imgs num

    res = None
    if len(img.shape) == 2:
        res = np.zeros((patches, patch_size[0], patch_size[1]))
    if len(img.shape) == 3:
        res = np.zeros((patches, patch_size[0], patch_size[1], img.shape[2]))

    index = 0
    for y in range_y:
        for x in range_x:
            patch = img[y:y + patch_size[1], x:x + patch_size[0]]
            res[index] = patch
            index += 1
    return res


# plt 做出图片还是有很大的白色 board
def plt_patches(img_patches, patch_size, img_size):
    patches_num = img_patches.shape[0]
    rows = int(img_size[0] / patch_size[0])
    cols = int(img_size[1] / patch_size[1])

    # plt 作图需要 img val [0,1]
    divider = 255  # rgb
    if len(img_patches.shape) == 3:  # gray
        divider = 65535

    for i in range(patches_num):
        plt.subplot(rows, cols, i + 1)
        plt.imshow(img_patches[i] / divider)
        plt.axis('off')
    plt.subplots_adjust(wspace=0.02, hspace=0.02)
    plt.show()


# space 精确控制 patches 边界
def cv2_patches(img_patches, patch_size, img_size, space, filename):  # space 两个 patch 之间的像素数
    rows = int(img_size[0] / patch_size[0])
    cols = int(img_size[1] / patch_size[1])

    res = None
    res_h = img_size[0] + (rows - 1) * space
    res_w = img_size[1] + (cols - 1) * space

    if len(img_patches.shape) == 3:  # gray
        res = 65535 * np.ones((res_h, res_w)).astype(np.uint16)  # 先置为全白，再填充
    if len(img_patches.shape) == 4:  # rgb
        res = 255 * np.ones((res_h, res_w, 3)).astype(np.uint8)

    index = 0
    for i in range(rows):
        for j in range(cols):
            begin_h = (patch_size[0] + space) * i
            begin_w = (patch_size[1] + space) * j
            res[begin_h:begin_h + patch_size[0], begin_w:begin_w + patch_size[1]] = img_patches[index]
            index += 1

    if len(img_patches.shape) == 4:
        res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename, res)


def test_plt():
    img_size = (480, 640)
    # read
    rgb = skimage.io.imread('rgb.jpg')
    depth = skimage.io.imread('depth.png')
    label = skimage.io.imread('label.png')
    # transform
    rgb = skimage.transform.resize(rgb, img_size,
                                   order=1, mode='reflect', preserve_range=True, anti_aliasing=True)
    depth = skimage.transform.resize(depth, img_size,
                                     order=0, mode='reflect', preserve_range=True, anti_aliasing=True)
    label = skimage.transform.resize(label, img_size,
                                     order=0, mode='reflect', preserve_range=True, anti_aliasing=True)

    patch_size = (160, 160)

    rgb_patches = cut_patches(rgb, patch_size, stride_x=patch_size[1], stride_y=patch_size[0])
    plt_patches(rgb_patches, patch_size, img_size)

    depth_patches = cut_patches(depth, patch_size, stride_x=patch_size[1], stride_y=patch_size[0])
    plt_patches(depth_patches, patch_size, img_size)

    label_patches = cut_patches(label, patch_size, stride_x=patch_size[1], stride_y=patch_size[0])
    plt_patches(label_patches, patch_size, img_size)


def test_cv2():
    img_size = (480, 640)
    # read
    rgb = skimage.io.imread('rgb.jpg')
    depth = skimage.io.imread('depth.png')
    label = skimage.io.imread('label.png')
    # transform
    rgb = skimage.transform.resize(rgb, img_size,
                                   order=1, mode='reflect', preserve_range=True, anti_aliasing=True)
    depth = skimage.transform.resize(depth, img_size,
                                     order=0, mode='reflect', preserve_range=True, anti_aliasing=True)
    label = skimage.transform.resize(label, img_size,
                                     order=0, mode='reflect', preserve_range=True, anti_aliasing=True)

    patch_size = (160, 160)

    rgb_patches = cut_patches(rgb, patch_size, stride_x=patch_size[1], stride_y=patch_size[0])
    cv2_patches(rgb_patches, patch_size, img_size, space=5, filename='rgb_patches.jpg')

    depth_patches = cut_patches(depth, patch_size, stride_x=patch_size[1], stride_y=patch_size[0])
    cv2_patches(depth_patches, patch_size, img_size, space=5, filename='depth_patches.png')

    label_patches = cut_patches(label, patch_size, stride_x=patch_size[1], stride_y=patch_size[0])
    cv2_patches(label_patches, patch_size, img_size, space=5, filename='label_patches.png')


if __name__ == '__main__':
    test_cv2()
