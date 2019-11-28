import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

import pycocotools.mask


def plt_polygon():
    fig, ax = plt.subplots()
    polygons = []
    gemfield_polygons = [[125.12, 539.69, 140.94, 522.43, 100, 200]]
    gemfield_polygon = gemfield_polygons[0]
    max_value = max(gemfield_polygon) * 1.3

    gemfield_polygon = [i * 1.0 / max_value for i in gemfield_polygon]

    poly = np.array(gemfield_polygon).reshape((int(len(gemfield_polygon) / 2), 2))  # x,y

    polygons.append(Polygon(poly, True))
    p = PatchCollection(polygons, cmap=matplotlib.cm.jet, alpha=0.4)
    colors = 100 * np.random.rand(1)
    p.set_array(np.array(colors))

    ax.add_collection(p)
    plt.show()


def test_coco_mask():
    mask = np.ones(shape=(480, 640), dtype=np.float32)
    gemfield_polygons = [[100, 200, 300, 200, 200, 300]]
    rle = pycocotools.mask.frPyObjects(gemfield_polygons, mask.shape[0], mask.shape[1])

    dd = pycocotools.mask.decode(rle)  # mask=1, bg=0
    dd = dd.squeeze(2)

    print(len(np.where(dd == 0)[0]))  # 297300, bg
    print(len(np.where(dd == 1)[0]))  # 9900, person

    # why reverse?
    mask[dd > 0.5] = 0  # person change to zero

    print(len(np.where(mask == 0)[0]))  # 9900
    print(len(np.where(mask == 1)[0]))  # 297300

    plt.imshow(mask)
    plt.show()


def test_coco_mask2():
    mask = np.zeros(shape=(480, 640), dtype=np.float32)
    gemfield_polygons = [[100, 200, 300, 200, 200, 300]]
    rle = pycocotools.mask.frPyObjects(gemfield_polygons, mask.shape[0], mask.shape[1])

    dd = pycocotools.mask.decode(rle)  # mask=1, bg=0
    dd = dd.squeeze(2)

    print(len(np.where(dd == 0)[0]))  # 297300, bg
    print(len(np.where(dd == 1)[0]))  # 9900, person

    # why reverse?
    mask[dd > 0.5] = 1  # person change to zero

    print(len(np.where(mask == 0)[0]))  # 9900
    print(len(np.where(mask == 1)[0]))  # 297300

    plt.imshow(mask)
    plt.show()


def generate_mask(mask, img_anns):  # no use self.attrs, so static
    segmentations = [ann['segmentation'] for ann in img_anns]
    for segmentation in segmentations:  # polygon, bbox, or uncompressed RLE
        rle = pycocotools.mask.frPyObjects(segmentation, mask.shape[0], mask.shape[1])
        rle = pycocotools.mask.decode(rle)  # for each person there has a mask
        rle = np.transpose(rle, (2, 0, 1))  # (num_person, h, w)
        for p_mask in rle:
            mask[p_mask > 0.5] = 0  # 0/1 reverse mask?
    return mask


if __name__ == '__main__':
    test_coco_mask()
    test_coco_mask2()
