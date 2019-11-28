import cv2
import numpy as np
from math import sqrt
from operator import attrgetter  # sort class object

"""
draw obj trail in object tracking tasks.
"""

cat_names = [
    'bg', 'cigar_A', 'cigar_a', 'bread', 'yili', 'chunzhen'
]
cat_colors = [
    [0, 0, 0], [246, 126, 15], [219, 0, 28],
    [62, 163, 44], [56, 118, 180], [113, 104, 207]
]


def create_empty_obj_dict():
    obj_dict = {}
    for cat in cat_names[1:]:  # no bg
        obj_dict[cat] = []
    return obj_dict


def cvt_obj_dict_to_list(obj_dict):
    total_obj_list = []
    for cat in cat_names[1:]:  # has order
        total_obj_list.extend(obj_dict[cat])

    # sort by (frame_idx, label_id)
    total_obj_list = sorted(total_obj_list, key=attrgetter('frame_idx', 'label'))
    return total_obj_list


def cvt_obj_list_to_dict(obj_list):
    total_obj_dict = create_empty_obj_dict()
    for obj in obj_list:
        total_obj_dict[cat_names[obj.label]].append(obj)
    return total_obj_dict


def draw_frame(frame, total_obj_list, frame_obj_list, str_and_coords):
    if isinstance(total_obj_list, dict):
        total_obj_list = cvt_obj_dict_to_list(total_obj_list)
    if isinstance(frame_obj_list, dict):
        frame_obj_list = cvt_obj_dict_to_list(frame_obj_list)

    height, width = frame.shape[:2]
    show_frame = np.zeros((height + 160, width, 3), dtype=np.uint8)
    # top ori img
    show_frame[:height, :] = frame

    # draw obj box and curve for each frame
    for obj in frame_obj_list:
        # 1.draw box
        newbox, label = obj.rect, obj.label
        label_id = cat_names.index(label)
        # newbox = recover_offset_box(list(newbox), crop_pt1) # frame_s, no need recover
        p1, p2 = (newbox[0], newbox[1]), (newbox[2], newbox[3])
        cv2.rectangle(show_frame, p1, p2, cat_colors[label_id][::-1], 2, 1)

        # 2.draw curve
        pts_num = len(obj.points)
        if pts_num >= 2:
            for i in range(pts_num - 1):
                thickness = int(sqrt((i + 1) * 2.5))  # 运动轨迹线条粗细，越来越粗
                cv2.line(show_frame, obj.points[i], obj.points[i + 1], (0, 0, 255), thickness)
        else:
            cv2.circle(show_frame, obj.points[0], 1, (0, 0, 255), 1)

    # 3.draw all detected obj thumbnail with label_name
    draw_objs = total_obj_list
    if len(draw_objs) > 6:
        draw_objs = draw_objs[-6:]
    begin_idx = 6 - len(draw_objs)
    for i, obj in enumerate(draw_objs):
        show_frame[height:, (begin_idx + i) * 160:(begin_idx + i + 1) * 160] = obj.thumbnail
        label_id = cat_names.index(obj.label)
        cv2.putText(show_frame,
                    text=obj.label,
                    org=((begin_idx + i) * 160 + 20, height + 20),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8,
                    color=cat_colors[label_id][::-1], thickness=2)

    # draw in/out, fps, compress_ratio, valid_flag
    for s, coord in str_and_coords:
        if s == 'checking':  # valid_flag
            color = (0, 255, 0)  # green
            fontScale = 0.8
        elif 'CR' in s:  # compress_ratio
            color = (0, 0, 255)  # red
            fontScale = 0.8
        else:  # in/out, fps
            color = (0, 0, 255)  # red
            fontScale = 1
        cv2.putText(show_frame, s, coord, cv2.FONT_HERSHEY_SIMPLEX, fontScale, color, 2)

    return show_frame
