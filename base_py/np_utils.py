"""
https://www.jianshu.com/p/5076a98db2d7
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn import preprocessing

np.set_printoptions(linewidth=1000)


def plt_read():
    # png value normal ~ [0,1], other img format still [0-255], jpg hasn't 16bits
    img = plt.imread('imgs/rgb.jpg')
    print(img.shape, (np.max(img), np.min(img)), img.dtype)  # (530, 730, 3) (255, 3) uint8
    # png
    img = plt.imread('imgs/rgb.png')
    print(img.shape, (np.max(img), np.min(img)), img.dtype)  # (530, 730, 3) (1.0, 0.011764706) float32
    img = plt.imread('imgs/depth.png')
    print(img.shape, (np.max(img), np.min(img)), img.dtype)  # (530, 730) (0.80042726, 0.13403524) float32


def flat_one_dim():
    img = plt.imread('imgs/rgb.jpg')
    print(img.shape)  # (530, 730, 3)
    img_h, img_w = img.shape[:2]
    print(img[4][50])  # [216 228 224]
    img = img.reshape((-1, img.shape[2]))  # 将 hxw 拉成一维
    print(img.shape)  # (386900, 3)
    print(img[4 * img_w + 50])  # [216 228 224]


def add_one_dim():
    img = plt.imread('imgs/depth.png')
    print(img.shape)
    img = img[np.newaxis, :]  # 可以添加在任何位置
    print(img.shape)


def cnt_same_elem():
    a = np.array([1, 2, 3, 4, 82, 24]).reshape((2, 3))
    b = np.array([2, 2, 3, 3, 0, 24]).reshape((2, 3))

    same = np.where(a == b)  # shape should same!
    print('same:', len(same[0]))
    print('value:', a[same])


def set_arr_val():
    # 指定多个 idx 位置 并给 np array 赋值
    # x = np.diag([2, 3, 4])  # 对角阵，其他位置为0
    # print(x)
    # idx = [1, 2]
    # x[0, idx] = 1  # 第 1 行，idx 指定要赋值的 列
    # print(x)
    # x[idx, 0] = 1  # 列赋值
    # print(x)

    # 3D arr
    x = np.arange(1, 25).reshape((2, 3, 4))
    print(x)
    # 这样其实通过 数组的形式，分离了 要指定位置各自维度，竖向拼接就是指定的位置
    dim1 = np.array([0, 1])
    dim2 = np.array([0, 2])
    dim3 = np.array([1, 3])
    x[dim1, dim2, dim3] = 0
    print(x)


def get_mat_eig(descend=True):
    x = np.diag((10, 2, 3))  # 对角阵
    print(x)
    if descend:
        eigen_vals, eigen_vecs = np.linalg.eigh(x)  # 默认降序，一般需要按照 eig_val 升序，如 PCA
        eigen_vals, eigen_vecs = eigen_vals[::-1], eigen_vecs[::-1]  # reverse
    else:
        eigen_vals, eigen_vecs = np.linalg.eig(x)
    print(eigen_vals)
    print(eigen_vecs)


def get_mat_inv():
    a = np.random.rand(30).reshape((3, 10))
    # a.* a.T 得到方阵
    b = np.linalg.inv(np.matmul(a, a.T))  # (3,10) * (10,3)
    print(b)
    b = np.linalg.inv(a @ a.T)  # 矩阵乘法
    print(b)


def relu():
    a = np.random.rand(2, 3) - 0.5
    print(a)
    a_relu = np.maximum(0, a)  # <0 -> =0
    print(a_relu)


def softmax():
    z = np.array([1.0, 2.0, 3.0, 4.0, 1.0, 2.0, 3.0])
    print(np.exp(z) / sum(np.exp(z)))


def sort_idx():
    # random choose k vals in [0,499]
    k = 10
    a = np.random.permutation(500)[:k]
    print(a)
    b = np.argsort(a)
    print(b)  # 默认得到升序排列的 idx
    print(a[b])
    print(a[b[::-1]])


def cnt_int_num_in_arr():
    # 统计数组中 某个整数的个数
    a = np.array([1, 3, 3, 8, 10, 12]).reshape((1, 2, 3))
    cnts = np.bincount(a.flatten())  # 只能处理 1D，higher D needs flatten
    for val, num in enumerate(cnts):
        print('val:{}, num:{}'.format(val, num))


def get_arr_min():
    a = np.array([[2, 5, 7, 8, 9, 89],
                  [6, 7, 5, 4, 6, 4]])  # 返回第1个最小值所在位置
    b = np.argmin(a, axis=1)  # 每行中最小值所在位置
    print(b)


def get_arr_mode():
    a = np.array([[6, 8, 3, 0],
                  [3, 2, 1, 7],
                  [8, 1, 8, 4],
                  [3, 3, 0, 5],
                  [4, 7, 5, 9]])
    # 指定计算 mode 范围
    # print(stats.mode(a))  # 默认 axis=0，沿行取出
    # print(stats.mode(a, axis=1))  # 沿着列
    # print(stats.mode(a, axis=None))  # 全局

    b = stats.mode(a, axis=1)
    # mode, count = b[0], b[1]
    b = (e.flatten() for e in b)  # 拉平 b 里面每个 array
    for m, c in zip(*b):
        print(m, c)


def stack():
    a = np.ones((1, 5))
    X = np.hstack((a, 2 * a, 3 * a))  # 水平
    print(X)
    X = np.vstack((a, 2 * a, 3 * a))  # 竖直
    print(X)


def random_choose():
    a = np.arange(1, 25).reshape((2, 3, 4))
    print(a)
    # 随机选出数字 形成 2x2，无放回
    c = np.random.choice(a.flatten(), (2, 2))  # arr must be 1D
    print(c)


def self_norm(b):
    a = b.copy()
    # 沿行，将每列数据 都标准化到 标准正态分布 N~(0,1)
    avgs = np.mean(a, axis=0)
    stds = np.std(a, axis=0)
    # print(avgs)
    # print(stds)

    for i in range(a.shape[1]):
        a[:, i] = (a[:, i] - avgs[i]) / stds[i]
    print(a)
    print(np.mean(a, axis=0))
    print(np.std(a, axis=0))


def sklearn_norm(a):
    b = preprocessing.scale(a)
    print(b)
    print(np.mean(b, axis=0))
    print(np.std(b, axis=0))


def normalize():
    a = np.arange(1, 16).reshape(3, 5).astype('float32')
    print(a)
    print('self norm')
    self_norm(a)  # 此函数 先 copy，没有改变 a
    print('sklearn norm')
    sklearn_norm(a)


if __name__ == '__main__':
    # cnt_same_elem()
