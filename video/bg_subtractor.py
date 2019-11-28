import cv2
from tqdm import tqdm
import numpy as np


def train_bg_subtractor(cap, model, model_history, learn_rate,
                        img_w, img_h, crop_pt1, crop_pt2):
    """
    train a bg_subtractor to filter invalid frame, no checking empty frame
        - cap: frame stream
        - model: MOG
        - model_history: frames used to train bg_subtractor
        - learn_rate: 0.005
    """
    iters = min(model_history, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    print('train bg_subtractor, iters:', iters)
    for _ in tqdm(range(iters)):
        retval, frame = cap.read()
        if not retval:
            print('use up frames!')
            break
        else:
            frame = cv2.resize(frame, dsize=(img_w, img_h))
            frame = frame[crop_pt1[1]:crop_pt2[1], crop_pt1[0]:crop_pt2[0]]  # y-row, x-col
            model.apply(frame, None, learn_rate)  # mog update bg


def filter_mask(frame, kernel=None):
    if kernel is None:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    closing = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel, iterations=2)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    dilate = cv2.dilate(opening, kernel, iterations=2)
    erode = cv2.erode(dilate, kernel)

    # 清除低于阀值噪点, 因为可能还存在灰色像素
    threshold = cv2.threshold(erode, 240, 255, cv2.THRESH_BINARY)[1]

    return threshold


def valid_mask(frame, fg_thre=1000):
    return len(np.where(frame == 255)[0]) > fg_thre
