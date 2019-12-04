"""
https://medium.com/mlreview/a-guide-to-receptive-field-arithmetic-for-convolutional-neural-networks-e0f514068807
Assume the two dimensions w,h are the same

Each kernel requires the following parameters:
- k_i: kernel size
- s_i: stride
- p_i: padding (if padding is uneven, right padding will higher than left padding; "SAME" option in tensorflow)
        tf 中，如果 pad 是奇数，会优先 pad right? torch 中自动两边 pad？

Each layer i requires the following parameters to be fully represented:
- n_i: number of feature (data layer has n_1 = imagesize) = 227, w/h
- j_i: distance (projected to image pixel distance) between center of two adjacent features
        保持 fm size 同 input size 一致时，center 和 周围邻接点 的跳数
- r_i: receptive field of a feature in layer i
        第 i 层感受野大小
- start_i: position of the first feature's receptive field in layer i (idx start from 0, negative means the center fall into padding)
        fm 上第1个特征 所在位置, center
"""

import math
from collections import OrderedDict

# Convolution Pose Machine
net = OrderedDict({  # kernel, stride, padding
    'C1': [9, 1, 0],  # stride = 1
    'P1': [2, 2, 0],  # stride = k_size
    'C2': [9, 1, 0],
    'P2': [2, 2, 0],
    'C3': [9, 1, 0],
    'P3': [2, 2, 0],
    'C4': [5, 1, 0],
    'C5': [9, 1, 0],
    'C6': [1, 1, 0],
    'C7': [1, 1, 0],
    'C8': [11, 1, 0],
    'C9': [11, 1, 0],
    'C10': [11, 1, 0],
    'C11': [1, 1, 0],
    'C12': [1, 1, 0],
})

layer_names = list(net.keys())
convnet = list(net.values())
imsize = 512


def cal_outsize():
    insize = imsize
    print('input', insize)
    for l, conv in zip(layer_names, convnet):
        kernel, stride, padding = conv
        outsize = (insize - kernel + 2 * padding) / stride + 1
        print(l, outsize)
        insize = outsize


def outFromIn(conv, layerIn):
    """
    :param conv: from convnet [kernel, stride, padding]
    :param layerIn: [n_feature, jump, RF_size, start]
    :return: layerOut: [n_feature, jump, RF_size, start]
    """
    n_in, j_in, r_in, start_in = layerIn
    k, s, p = conv

    # out size
    n_out = math.floor((n_in - k + 2 * p) / s) + 1  # 向下取整
    actualP = (n_out - 1) * s + k - n_in  # get real padding
    # pad right, left
    pR = math.ceil(actualP / 2)
    pL = math.floor(actualP / 2)

    # j_out = j_in * stride 映射回原 image size 时，两个 feature 之间的 jumps
    j_out = j_in * s  # 可以看到 jump 是 阶乘 stride 的形式
    r_out = r_in + (k - 1) * j_in  # (k-1) kernel 中心点左右的点，点与点之间 对应在原图上的 jumps
    start_out = start_in + ((k - 1) / 2 - pL) * j_in  # start 逐渐从左上角 0.5 移动到图像中心点 113.5

    return n_out, j_out, r_out, start_out


def printLayer(layer, layer_name):
    print("{:<10} {:<10} {:<6} {:<10} {:<6}".format(layer_name, layer[0], layer[1], layer[2], layer[3]))


def cal_RF():
    # first layer is the data layer (image) with
    # n_0 = image size;
    # j_0 = 1;
    # r_0 = 1;
    # start_0 = 0.5
    print("-------Net summary------")
    print('{:<10} {:<10} {:<6} {:<10} {:<6}'.format('layer', 'n_features', 'jump', 'RF_size', 'start'))
    currentLayer = [imsize, 1, 1, 0.5]  # [n_feature, jump, RF_size, start]
    printLayer(currentLayer, "input")

    layerInfos = []
    for i in range(len(convnet)):
        currentLayer = outFromIn(convnet[i], currentLayer)
        layerInfos.append(currentLayer)
        printLayer(currentLayer, '{}_{}x'.format(layer_names[i], convnet[i][0]))

    # print("------------------------")
    #
    # layer_name = input("Layer name where the feature in: ")  # conv1
    # layer_idx = layer_names.index(layer_name)
    # idx_x = int(input("index of the feature in x dimension (from 0): "))  # 10
    # idx_y = int(input("index of the feature in y dimension (from 0): "))  # 10
    #
    # n, j, r, start = layerInfos[layer_idx]  # n: 当前层 fm size
    #
    # assert 0 <= idx_x < n and 0 <= idx_y < n
    #
    # print("receptive field: (%s, %s)" % (r, r))  # 11
    # print("center: (%s, %s)" % (start + idx_x * j, start + idx_y * j))  # 45.5 原图 start 中心点 + 索引位置


if __name__ == '__main__':
    # cal_outsize()
    cal_RF()
