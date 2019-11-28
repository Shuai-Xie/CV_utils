import os
import numpy as np
import xml.etree.ElementTree as ET
import pickle
from pprint import pprint
from tqdm import tqdm
import time
from dataset.voc.config import names2class
from dataset.voc.vis_utils import plt_bbox

data_root = os.path.join(os.path.dirname(__file__), '..', 'data')


def get_data(data, split='trainval', use_diff=False):
    if data == 'VOC2012' and split == 'test':
        print('VOC2012 has not test file')
        exit(1)

    # save results
    all_anns = []
    classes_count = {}

    # use absolute path as pycharm loading so slow
    data_path = '/nfs/xs/Datasets/{}/VOCdevkit/{}'.format(data, data)
    # data_path = os.path.join(data_root, data)
    anns_path = os.path.join(data_path, 'Annotations')  # xml
    imgs_path = os.path.join(data_path, 'JPEGImages')

    img_files = []
    with open(os.path.join(data_path, 'ImageSets', 'Main', '{}.txt'.format(split))) as f:
        for line in f:  # VOC2012: 2008-2011
            img_files.append(line.strip() + '.jpg')

    for img in tqdm(img_files):
        # print(img)
        et = ET.parse(os.path.join(anns_path, img.replace('.jpg', '.xml')))
        element = et.getroot()
        element_objs = element.findall('object')
        element_width = int(element.find('size').find('width').text)
        element_height = int(element.find('size').find('height').text)
        if len(element_objs) > 0:
            # img attrs
            ann_data = {
                'filepath': os.path.join(imgs_path, img),
                'width': element_width,
                'height': element_height,
            }
            # label attrs
            boxes, labels, difficulties = [], [], []
            for obj in element_objs:
                # label
                class_name = obj.find('name').text
                labels.append(names2class[class_name])
                if class_name not in classes_count:  # stats
                    classes_count[class_name] = 1
                else:
                    classes_count[class_name] += 1
                # box
                obj_bbox = obj.find('bndbox')
                x1 = int(round(float(obj_bbox.find('xmin').text)))
                y1 = int(round(float(obj_bbox.find('ymin').text)))
                x2 = int(round(float(obj_bbox.find('xmax').text)))
                y2 = int(round(float(obj_bbox.find('ymax').text)))
                boxes.append([x1, y1, x2, y2])
                # difficulty
                difficulties.append(int(obj.find('difficult').text))

            boxes, labels, difficulties = np.array(boxes), np.array(labels), np.array(difficulties)

            if not use_diff:
                keep = np.where(np.array(difficulties) == 0)[0]
                # print(keep)
                boxes = boxes[keep]
                labels = labels[keep]

            ann_data['boxes'] = boxes
            ann_data['labels'] = labels
            # pprint(ann_data)
            all_anns.append(ann_data)

    pprint(classes_count)

    out_path = os.path.join(data_root, '{}_{}.pkl'.format(data, split))
    dump_data(all_anns, out_path)


def dump_data(ann_list, out_path):
    with open(out_path, 'wb') as f:
        # pickle.dump((all_anns, classes_count), f)
        pickle.dump(ann_list, f)  # only save anns
        print('write data to', out_path)


def load_data(data, split):
    with open(os.path.join(data_root, '{}_{}.pkl'.format(data, split)), 'rb') as f:
        all_anns = pickle.load(f)
        return all_anns


def load_vis_data(data, split):
    all_anns = load_data(data, split)
    print(len(all_anns))
    pprint(all_anns[0])
    exit(0)
    plt_bbox(all_anns[0])
    plt_bbox(all_anns[1])
    plt_bbox(all_anns[2])
    plt_bbox(all_anns[3])


def parse_data_test(data, split):
    st = time.time()
    get_data(data, split)
    print('time:', time.time() - st)


if __name__ == '__main__':
    load_vis_data(data='VOC2007', split='trainval')
