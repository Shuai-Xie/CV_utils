# set class_mapping as constant, so trainval and test has same label_idx
names2class = {
    'aeroplane': 0,
    'bicycle': 1,
    'bird': 2,
    'boat': 3,
    'bottle': 4,
    'bus': 5,
    'car': 6,
    'cat': 7,
    'chair': 8,
    'cow': 9,
    'diningtable': 10,
    'dog': 11,
    'horse': 12,
    'motorbike': 13,
    'person': 14,
    'pottedplant': 15,
    'sheep': 16,
    'sofa': 17,
    'train': 18,
    'tvmonitor': 19
}

class2names = list(names2class.keys())

ann_sample = {
    'boxes': [[263, 211, 324, 339],  # np.array
              [165, 264, 253, 372],
              [241, 194, 295, 299]],
    'filepath': '/nfs/xs/Codes/VIPA_ASM/datasets/../data/VOC2007/JPEGImages/000005.jpg',
    'height': 375,
    'labels': [8, 8, 8],  # np.array
    'width': 500
}

# stats
total_instances = {
    'voc2007': {
        'trainval': 5011,
        'test': 4592
    },
    'voc2012': {
        'trainval': 11540
    }
}

voc2007_class_counts = {
    'trainval': {'aeroplane': 331,
                 'bicycle': 418,
                 'bird': 599,
                 'boat': 398,
                 'bottle': 634,
                 'bus': 272,
                 'car': 1644,
                 'cat': 389,
                 'chair': 1432,
                 'cow': 356,
                 'diningtable': 310,
                 'dog': 538,
                 'horse': 406,
                 'motorbike': 390,
                 'person': 5447,  # too many!
                 'pottedplant': 625,
                 'sheep': 353,
                 'sofa': 425,
                 'train': 328,
                 'tvmonitor': 367},
    'test': {'aeroplane': 311,
             'bicycle': 389,
             'bird': 576,
             'boat': 393,
             'bottle': 657,
             'bus': 254,
             'car': 1541,
             'cat': 370,
             'chair': 1374,
             'cow': 329,
             'diningtable': 299,
             'dog': 530,
             'horse': 395,
             'motorbike': 369,
             'person': 5227,
             'pottedplant': 592,
             'sheep': 311,
             'sofa': 396,
             'train': 302,
             'tvmonitor': 361}
}

voc2012_class_counts = {
    'trainval': {'aeroplane': 954,
                 'bicycle': 790,
                 'bird': 1221,
                 'boat': 999,
                 'bottle': 1482,
                 'bus': 637,
                 'car': 2364,
                 'cat': 1227,
                 'chair': 2906,
                 'cow': 702,
                 'diningtable': 747,
                 'dog': 1541,
                 'horse': 750,
                 'motorbike': 751,
                 'person': 10129,  # too many!
                 'pottedplant': 1099,
                 'sheep': 994,
                 'sofa': 786,
                 'train': 656,
                 'tvmonitor': 826}
}
