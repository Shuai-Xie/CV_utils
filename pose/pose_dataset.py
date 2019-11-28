dataset_joints = {
    # mpii as baseline order
    'mpii': {  # 16
        'name': (
            'R_ankle', 'R_knee', 'R_hip', 'L_hip', 'L_knee', 'L_ankle',  # legs, [0-5]
            'Pelvis', 'Thorax', 'Neck', 'Head',  # middle body, [6-9]
            'R_wrist', 'R_elbow', 'R_shoulder', 'L_shoulder', 'L_elbow', 'L_wrist'  # arms, [10-15]
        ),
        'links': [
            [0, 1], [1, 2], [2, 6], [6, 3], [3, 4], [4, 5],  # legs
            [10, 11], [11, 12], [12, 8], [8, 13], [13, 14], [14, 15],  # arms
            [6, 7], [7, 8], [8, 9]  # middle body
        ],
        'order': list(range(16)),
        'num_joints': 16
    },
    'coco': {  # 17
        'name': (
            'Nose',
            'L_eye', 'R_eye', 'L_ear', 'R_ear',  # 1-5, face
            'L_shoulder', 'R_shoulder', 'L_elbow', 'R_elbow', 'L_wrist', 'R_wrist',  # 6-11, arms
            'L_hip', 'R_hip', 'L_knee', 'R_knee', 'L_ankle', 'R_ankle'  # 12-17, legs
        ),
        'links': [
            [0, 1], [1, 3], [0, 2], [2, 4],  # face
            [5, 6], [5, 7], [7, 9], [6, 8], [8, 10],  # arms
            [5, 11], [6, 12],  # middle body
            [11, 13], [13, 15], [12, 14], [14, 16]  # legs
        ],
        'order': [16, 14, 12, 11, 13, 15, -1, -1, -1, -1, 10, 8, 6, 5, 7, 9],
        'num_joints': 17
    },
    'openpose': {  # 19
        'name': (
            'Nose', 'Neck',  # 0-1, face
            'R_shoulder', 'R_elbow', 'R_wrist', 'L_shoulder', 'L_elbow', 'L_wrist',  # 2-7, arms
            'R_hip', 'R_knee', 'R_ankle', 'L_hip', 'L_knee', 'L_ankle',  # 8-13, legs
            'R_eye', 'L_eye', 'R_ear', 'L_ear',  # 14-17, face
            'Pelvis'  # 18, body
        ),
        'links': [
            [0, 1], [0, 14], [14, 16], [0, 15], [15, 17],  # face
            [1, 2], [2, 3], [3, 4], [1, 5], [5, 6], [6, 7],  # arms
            [1, 18],  # middle
            [18, 8], [8, 9], [9, 10], [18, 11], [11, 12], [12, 13]  # legs
        ],
        'order': [10, 9, 8, 11, 12, 13, 18, -1, 1, -1, 4, 3, 2, 5, 6, 7],
        'num_joints': 19
    }
}

baseline_joints_name = dataset_joints['mpii']['name']
num_joints = dataset_joints['mpii']['num_joints']

OCCLUDE = 0
VISIBLE = 1
NO_THIS = 2


def remap_joints_order(dataset='mpii'):
    """
    remap other dataset's joints order relative to mpii
    """
    joints_order = [-1] * num_joints
    if dataset == 'mpii':
        return list(range(num_joints))
    else:
        remap_joints_name = dataset_joints[dataset]['name']
        print('missing joints:')
        for idx, joint in enumerate(baseline_joints_name):
            if joint in remap_joints_name:
                joints_order[idx] = remap_joints_name.index(joint)
            else:
                print(idx, joint)
        return joints_order


def judge_keypoint_vis(keypoint, w, h):
    """
    judge vis by x,y of keypoint
    """
    if keypoint[0] == keypoint[1] == 0:  # not record
        return NO_THIS
    elif keypoint[0] < 0 or keypoint[0] >= w or keypoint[1] < 0 or keypoint[1] >= h:  # out of image
        return NO_THIS
    else:
        return keypoint[2]


def judge_generate_keypoint_vis(keypoint, pt1, pt2, w, h):
    """
    judge vis by x,y of keypoint and father pts [p1, p2]
    """
    if pt1[2] == pt2[2] == NO_THIS:
        return NO_THIS
    elif pt1[2] == pt2[2] == VISIBLE:
        return VISIBLE
    elif pt1[2] == pt2[2] == OCCLUDE:
        return OCCLUDE
    else:
        return judge_keypoint_vis(keypoint, w, h)


def map2mpii(keypoints, w, h, dataset):
    if dataset == 'mpii':
        return keypoints
    else:
        remap_order = dataset_joints[dataset]['order']
        # to mpii order
        remap_keypoints = [keypoints[idx] if idx > -1 else [0, 0, 0] for idx in remap_order]  # len=16

        if dataset == 'coco':
            miss_idx = [6, 8, 7, 9]  # generate order
            for idx in miss_idx:
                if idx == 6:  # 'Pelvis'
                    pt1, pt2 = remap_keypoints[2], remap_keypoints[3]  # R_hip, L_hip
                    miss_pt = [(pt1[0] + pt2[0]) / 2, (pt1[1] + pt2[1]) / 2, 0]
                    miss_pt[2] = judge_generate_keypoint_vis(miss_pt, pt1, pt2, w, h)
                    remap_keypoints[idx] = miss_pt
                elif idx == 8:  # 'Neck'
                    pt1, pt2 = remap_keypoints[12], remap_keypoints[13]  # R_shoulder, L_shoulder
                    miss_pt = [(pt1[0] + pt2[0]) / 2, (pt1[1] + pt2[1]) / 2, 0]
                    miss_pt[2] = judge_generate_keypoint_vis(miss_pt, pt1, pt2, w, h)
                    remap_keypoints[idx] = miss_pt
                elif idx == 7:  # Thorax
                    pt1, pt2 = remap_keypoints[6], remap_keypoints[8]  # Pelvis, Neck
                    miss_pt = [(pt1[0] + pt2[0]) / 2, (pt1[1] + pt2[1]) / 2, 0]
                    miss_pt[2] = judge_generate_keypoint_vis(miss_pt, pt1, pt2, w, h)
                    remap_keypoints[idx] = miss_pt
                elif idx == 9:  # Head
                    Nose, L_eye, R_eye, L_ear, R_ear = keypoints[0], keypoints[1], keypoints[2], keypoints[3], keypoints[4]
                    # eyes vis
                    if Nose[2] < 2 and L_eye[2] < 2 and R_eye[2] < 2:
                        head_x = (L_eye[0] + R_eye[0]) / 2
                        mid_y = (L_eye[1] + R_eye[1]) / 2
                        head_y = mid_y - (Nose[1] - mid_y)
                        miss_pt = [head_x, head_y, 0]
                        miss_pt[2] = judge_keypoint_vis(miss_pt, w, h)

        return remap_keypoints


def convert2mpii(sample, dataset):
    label = sample['label']
    h, w, _ = sample['image'].shape
    keypoints = label['keypoints']

    # remark visibility of keypoints
    for keypoint in keypoints:
        keypoint[2] = judge_keypoint_vis(keypoint, w, h)
    for other_label in label['processed_other_annotations']:
        keypoints = other_label['keypoints']
        for keypoint in keypoints:
            keypoint[2] = judge_keypoint_vis(keypoint, w, h)

    # remap order to mpii
    if dataset == 'mpii':
        return sample
    elif dataset == 'coco':
        label['keypoints'] = map2mpii(label['keypoints'], w, h, dataset=dataset)
        for other_label in label['processed_other_annotations']:
            other_label['keypoints'] = map2mpii(other_label['keypoints'], w, h, dataset=dataset)
        return sample
