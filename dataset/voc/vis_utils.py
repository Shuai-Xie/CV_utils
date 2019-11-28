from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cmx
import torch

# use cmap color | tab20, tab20b, hsv
cmap = plt.get_cmap('tab20')  # qualitative cmaps, >18
cNorm = mcolors.Normalize(vmin=0, vmax=19)
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cmap)


def cvt_tensor_np(a):
    if isinstance(a, torch.Tensor):
        a = a.numpy().astype(int)  # plt
    return a


def plt_bbox(ann, class2names, img=None):
    boxes, labels = ann['boxes'], ann['labels']
    boxes = cvt_tensor_np(boxes)
    labels = cvt_tensor_np(labels)
    if img is None:
        img = Image.open(ann['filepath']).convert("RGB")
    else:  # detect idx mode
        img = img.numpy().transpose((1, 2, 0))
        labels = labels - 1

    plt.figure(figsize=(8, 6))
    plt.title(ann['filepath'])
    plt.imshow(img)

    for label_id, box in zip(labels, boxes):
        # label, box = result['labels'][idx], result['boxes'][idx]  # label idx
        # box
        plt.gca().add_patch(plt.Rectangle(xy=(box[0], box[1]),
                                          width=box[2] - box[0],
                                          height=box[3] - box[1],
                                          edgecolor=scalarMap.to_rgba(label_id),
                                          fill=False, linewidth=2))
        # name
        plt.annotate(class2names[label_id],
                     xy=(box[0], box[1]), fontsize=10,
                     xycoords='data', xytext=(2, 5), textcoords='offset points',
                     bbox=dict(boxstyle='round, pad=0.3',  # linewidth=0 可以不显示边框
                               facecolor=scalarMap.to_rgba(label_id), lw=0),
                     color='w')
    plt.show()
