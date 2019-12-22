import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cmx
from heatmap.ann_sample import yunyan, kuanzhai
from base_py.generic import varname


def coco_box_to_bbox(box):
    # xywh -> x1y1x2y2
    bbox = np.array([box[0], box[1], box[0] + box[2], box[1] + box[3]],
                    dtype=np.float32)
    return bbox


def gaussian_radius(det_size, min_overlap=0.7):
    height, width = det_size

    # ax^2 + bx + c = 0
    a1 = 1
    b1 = (height + width)
    c1 = width * height * (1 - min_overlap) / (1 + min_overlap)
    sq1 = np.sqrt(b1 ** 2 - 4 * a1 * c1)
    r1 = (b1 + sq1) / 2

    a2 = 4
    b2 = 2 * (height + width)
    c2 = (1 - min_overlap) * width * height
    sq2 = np.sqrt(b2 ** 2 - 4 * a2 * c2)
    r2 = (b2 + sq2) / 2

    a3 = 4 * min_overlap
    b3 = -2 * min_overlap * (height + width)
    c3 = (min_overlap - 1) * width * height
    sq3 = np.sqrt(b3 ** 2 - 4 * a3 * c3)
    r3 = (b3 + sq3) / 2

    return min(r1, r2, r3)


def gaussian2D(shape, sigma=1.0):
    m, n = [(ss - 1.) / 2. for ss in shape]
    y, x = np.ogrid[-m:m + 1, -n:n + 1]

    h = np.exp(-(x * x + y * y) / (2 * sigma * sigma))
    h[h < np.finfo(h.dtype).eps * h.max()] = 0
    return h


def draw_umich_gaussian(heatmap, center, radius, k=1):  # k>1 会带来更多 peak 值，超过 255
    radius = math.ceil(radius)
    diameter = 2 * radius + 1
    gaussian = gaussian2D((diameter, diameter), sigma=diameter / 6)  # 3 sigma 原则

    x, y = int(center[0]), int(center[1])  # 转成 int
    height, width = heatmap.shape[0:2]

    # 4 direction bounds
    left, right = min(x, radius), min(width - x, radius + 1)
    top, bottom = min(y, radius), min(height - y, radius + 1)

    # get this rect from heatmap
    masked_heatmap = heatmap[y - top:y + bottom, x - left:x + right]
    # get this rect from gaussian
    masked_gaussian = gaussian[radius - top:radius + bottom, radius - left:radius + right]

    if min(masked_gaussian.shape) > 0 and min(masked_heatmap.shape) > 0:  # TODO debug
        # out the max of (heatmap, gaussian) to heatmap
        np.maximum(masked_heatmap, masked_gaussian * k, out=masked_heatmap)

    return heatmap  # add a new obj's gaussian range


cmap = plt.get_cmap('jet')  # qualitative cmaps, >18
cNorm = mcolors.Normalize(vmin=0, vmax=255)
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cmap)


def get_rgb(val):
    if val == 0:  # 改变 0 默认的 蓝色 0,0,127
        return 255, 255, 255
    else:
        rgba = scalarMap.to_rgba(val)
        return int(255 * rgba[0]), int(255 * rgba[1]), int(255 * rgba[2])


# 将 jet 样式 hm 转成 rgb
def cvt_hm_2_rgb(hm):
    hm = (hm * 255).astype(np.uint8)
    rgb = np.zeros(hm.shape + (3,), dtype=np.uint8)
    color_vals = np.unique(hm)
    for val in color_vals:
        rgb[hm == val] = get_rgb(val)
    return rgb


from shapely.geometry.polygon import Polygon


def get_polygon_center(segmentation):  # coco segmentation
    segmentation = segmentation[0]
    segmentation = [x // 4 for x in segmentation]  # 1/4
    points = [(segmentation[i], segmentation[i + 1]) for i in range(0, len(segmentation), 2)]
    polygon = Polygon(points)
    x, y = polygon.centroid.xy  # x_array, y_array
    return x[0], y[0]


if __name__ == '__main__':
    img_anns = kuanzhai
    img_name = 'kuanzhai'
    img_path = 'imgs/{}.jpg'.format(img_name)
    img = cv2.imread(img_path)
    img = cv2.resize(img, (640, 352))  # input size
    img = cv2.resize(img, (160, 88))  # 1/4
    img_h, img_w = img.shape[:2]
    hm = np.zeros((img_h, img_w))  # default float64

    for ann in img_anns:
        bbox = ann['bbox']
        bbox = [x // 4 for x in bbox]  # downsample 1/4
        w, h = bbox[2:]
        radius = gaussian_radius(det_size=(h, w))
        radius = max(0, math.ceil(radius / 3))  # r/3
        box_center = (bbox[0] + w / 2, bbox[1] + h / 2)  # rect center
        print(box_center)
        polygon_center = get_polygon_center(ann['segmentation'])  # polygon center
        print(polygon_center)
        center = polygon_center
        draw_umich_gaussian(hm, center, radius)

    hm_rgb = cvt_hm_2_rgb(hm)
    trans = 0.5
    res = img[:, :, ::-1] * trans + hm_rgb * (1 - trans)
    res = res.astype(np.uint8)

    plt.axis('off')
    plt.imshow(res)
    # 先 save 再 show
    plt.savefig('imgs/{}_hm.png'.format(img_name), bbox_inches='tight', pad_inches=0.0)
    # plt.show()
