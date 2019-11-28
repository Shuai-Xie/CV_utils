import torch
from torch.utils.data.dataset import Dataset
from PIL import Image
from dataset.voc.voc_parser import load_data
from dataset.transforms import get_transform
from dataset.voc.vis_utils import plt_bbox


class VOC_Dataset(Dataset):
    def __init__(self, data, split, transforms=None):
        if isinstance(data, list):  # directly pass in ann list, no need to load
            self.anns = data
        else:
            self.anns = load_data(data, split)  # load
        # self.anns = self.anns[:10]  # test
        self.transforms = transforms

    def __getitem__(self, idx):
        ann = self.anns[idx]
        img = Image.open(ann['filepath']).convert("RGB")
        boxes, labels = ann['boxes'], ann['labels'] + 1  # bg=0

        # convert everything into a torch.Tensor
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        labels = torch.as_tensor(labels, dtype=torch.int64)
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])  # cal area by box, return vector
        iscrowd = torch.zeros((labels.size(0),), dtype=torch.int64)  # set 0

        target = {
            'image_id': torch.as_tensor([idx]),
            # 'filepath': ann['filepath'],  # for vis
            'boxes': boxes,  # [x0, y0, x1, y1] ~ [0,W], [0,H]
            'labels': labels,  # class label
            'area': area,  # used in COCO metric, AP_small,medium,large
            'iscrowd': iscrowd,  # if True, ignored during eval
        }

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.anns)


if __name__ == '__main__':
    dataset = VOC_Dataset('VOC2007', 'trainval',
                          transforms=get_transform(train=True))
    print(len(dataset))

    for idx, (img, target) in enumerate(dataset):
        # pprint(target)
        plt_bbox(target, img)

        if idx > 3:
            break
