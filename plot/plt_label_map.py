import os
import cv2
import csv
import numpy as np
import matplotlib.pyplot as plt


def get_label_name_colors(csv_path):
    """
    read csv_file and save as label names and colors list
    :param csv_path: csv color file path
    :return: lable name list, label color list
    """
    label_names = []
    label_colors = []
    with open(csv_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for i, row in enumerate(reader):
            if i > 0:  # 跳过第一行
                label_names.append(row[0])
                label_colors.append([int(row[1]), int(row[2]), int(row[3])])

    return label_names, label_colors


def create_label_map(label_colors, rows, cols, row_height, col_width):
    """
    create a colorful label image for plt to annotate
    :param label_colors: label color list
    :param rows: num of figure rows
    :param cols: num of figure cols
    :param row_height: height of each row
    :param col_width: width of each col
    :return:
    """
    label_map = np.ones((row_height * rows, col_width * cols, 3), dtype='uint8') * 255
    cnt = 0
    for i in range(rows):  # 1st row is black = background
        for j in range(cols):
            if cnt >= len(label_colors):  # in case, num of lables < rows * cols
                break
            beg_pix = (i * row_height, j * col_width)
            end_pix = (beg_pix[0] + 20, beg_pix[1] + 20)  # 20 is color square side
            label_map[beg_pix[0]:end_pix[0], beg_pix[1]:end_pix[1]] = label_colors[cnt][::-1]  # RGB->BGR
            cnt += 1
    cv2.imwrite('label_map%dx%d.png' % (rows, cols), label_map)


def plt_label_map(label_names, label_colors, rows, cols, row_height, col_width, figsize=(10, 8), fig_title='color map'):
    """
    read cv2 saved colorful label image and use plt to annotate the label names
    :param label_names: lable name list
    :param label_colors: label color list
    :param rows: num of figure rows
    :param cols: num of figure cols
    :param row_height: height of each row
    :param col_width: width of each col
    :param figsize: overall figure size, like (10, 8)
    :param fig_title: figure title, like ADE20K-150class
    :return:
    """
    # create origin map
    if os.path.exists('label_map%dx%d.png' % (rows, cols)):
        os.remove('label_map%dx%d.png' % (rows, cols))
    create_label_map(label_colors, rows, cols, row_height, col_width)
    label_map = plt.imread('label_map%dx%d.png' % (rows, cols))

    # show origin map
    plt.figure(figsize=figsize)
    plt.axis('off')
    plt.title(fig_title + '\n', fontweight='black')  # 上移一段距离，哈哈
    plt.imshow(label_map)

    cnt = 0
    for i in range(rows):  # 1st row is black = background
        for j in range(cols):
            if cnt >= len(label_names):  # in case, num of lables < rows * cols
                break
            beg_pix = (j * col_width, i * row_height)  # note! (y,x)
            plt.annotate('%s' % label_names[cnt],
                         xy=beg_pix, xycoords='data', xytext=(+13, -8), textcoords='offset points',
                         color='k')
            cnt += 1
    plt.savefig('img/{}.png'.format(fig_title), bbox_inches='tight', pad_inches=0.1)
    # plt.show()

    # rm tmp color label img
    os.remove('label_map%dx%d.png' % (rows, cols))


if __name__ == '__main__':
    # ADE20K
    label_names, label_colors = get_label_name_colors(csv_path='csv/ade150.csv')
    plt_label_map(label_names, label_colors, rows=10, cols=15, row_height=30, col_width=200, figsize=(22, 4), fig_title='ADE20K-150class')
    # SUN-RGBD
    label_names, label_colors = get_label_name_colors(csv_path='csv/sun37.csv')
    plt_label_map(label_names, label_colors, rows=4, cols=10, row_height=30, col_width=200, figsize=(14, 3), fig_title='SUNRGBD-37class')
    # CamVid
    label_names, label_colors = get_label_name_colors(csv_path='csv/camvid32.csv')
    plt_label_map(label_names, label_colors, rows=4, cols=10, row_height=30, col_width=200, figsize=(16, 3), fig_title='CamVid-32class')
