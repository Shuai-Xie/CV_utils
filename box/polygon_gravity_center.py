import cv2
import numpy as np
from base_py.box_utils import pt_float2int, pt_in_img

img_info = {
    "content": "imgs/4aa64d97-a95b-4594-a19a-f5705ba4b1f9___2019-09-18_214748_cloud_video_999.jpg",
    "annotation": [
        {"label": ["宽窄_a"],
         "shape": "polygon",
         "points": [[0.3704909663400285, 0.8411909178615503], [0.510218987931125, 0.8703597304495906], [0.5245093537756689, 0.811081175835186],
                    [0.5250386265847261, 0.7518026212207815], [0.39430824274760173, 0.7292203147010083], [0.366256783867571, 0.7847351515621174]],
         "imageWidth": 640, "imageHeight": 360},
        {"label": ["宽窄_a"],
         "shape": "polygon",
         "points": [[0.32724985681172436, 0.7907655655428937], [0.36696464525974914, 0.7935897282769755],
                    [0.36934753256663067, 0.8430125761234063], [0.48054894022110006, 0.8670179593631013],
                    [0.4821375317590211, 0.8910233426027963], [0.3153354202773169, 0.8853750171346327],
                    [0.31136394143251445, 0.858545471160856]],
         "imageWidth": 640, "imageHeight": 360}
    ],
}

mean_value = [122.7717, 115.9465, 102.9801]


def cal_bbox_of_rbox(rbox):
    """
    :param rbox: np array 4 pts of a rotated box
    """
    x_min, x_max = np.min(rbox[:, 0]), np.max(rbox[:, 0])
    y_min, y_max = np.min(rbox[:, 1]), np.max(rbox[:, 1])

    return [x_min, y_min, x_max, y_max]


def cal_offset_and_pad_img(img, rbox, mode='edge'):
    """
    :param img: original image
    :param rbox: rotated box
    :param mode: pad mode, edge 边缘; linear_ramp: 边缘递减; symmetric 边缘对称;
    """
    img_h, img_w = img.shape[:2]
    img_bounds = [0, 0, img_w, img_h]
    box_bounds = cal_bbox_of_rbox(rbox)
    pad = [b - i for b, i in zip(box_bounds, img_bounds)]  # left, top, right, bottom
    pad[0] = abs(pad[0]) if pad[0] < 0 else 0  # exceed left
    pad[1] = abs(pad[1]) if pad[1] < 0 else 0  # exceed top
    pad[2] = pad[2] if pad[2] > 0 else 0  # exceed right
    pad[3] = pad[3] if pad[3] > 0 else 0  # exceed bottom

    # axis_1: rows=(t,b), axis_2: cols=(l,r), axis_3: (0,0), no pad
    img = np.pad(img, ((pad[1], pad[3]), (pad[0], pad[2]), (0, 0)), mode=mode)
    offset = pad[0], pad[1]

    return offset, img


from base_py.box_utils import cvt_poly_fpts_to_xywh, cal_area


def polygon2rbox(pad_mode=None):
    """
    :param pad_mode: 'edge', whether padding img when rbox exceeds ori img bounds
    """
    img = cv2.imread(img_info['content'])

    for ann in img_info['annotation']:
        points, img_w, img_h = ann['points'], ann['imageWidth'], ann['imageHeight']
        # points = points[::-1]   # cvt clock-wise to anti, result is same
        print('area:', cal_area(points, img_w, img_h))

        poly_pts = np.array([pt_float2int(pt, img_w, img_h) for pt in points])
        rect = cv2.minAreaRect(poly_pts)  # center_xy,wh, angle
        polygon = np.array(poly_pts).astype(np.int)

        # cal rotated box
        rbox = cv2.boxPoints(rect)
        rbox = np.array(rbox).astype(np.int)
        print(rbox)

        if pad_mode:
            offset, img = cal_offset_and_pad_img(img, rbox, mode=pad_mode)
            polygon += offset
            rbox += offset

        # draw ori polygon, rotated box
        # cv2.drawContours(img, contours=[polygon], contourIdx=0, color=(0, 255, 0), thickness=2)
        cv2.drawContours(img, contours=[rbox], contourIdx=0, color=(0, 0, 255), thickness=2)
        # draw diagonal line of rbox
        # cv2.line(img, tuple(rbox[0]), tuple(rbox[2]), color=(0, 0, 255), thickness=2)
        # cv2.line(img, tuple(rbox[1]), tuple(rbox[3]), color=(0, 0, 255), thickness=2)

        # cal bbox
        x, y, w, h = cvt_poly_fpts_to_xywh(points, img_w, img_h)
        print(x, y, w, h)
        cv2.rectangle(img, (x, y), (x + w, y + h), color=(255, 0, 0), thickness=2)
        # draw diagonal line of box
        # cv2.line(img, (x, y), (x + w, y + h), color=(255, 0, 0), thickness=2)
        # cv2.line(img, (x, y + h), (x + w, y), color=(255, 0, 0), thickness=2)

    # draw rbox

    if pad_mode:
        cv2.imwrite('imgs/grav_{}.png'.format(pad_mode), img)
    else:
        cv2.imwrite('imgs/grav.png', img)


a_rbox = (
    (182.0570068359375, 266.25909423828125),  # center x, y
    (292.0228271484375, 118.38426971435547),  # w, h
    -20.684080123901367  # angle, [-90°, 90°]
)

if __name__ == '__main__':
    # polygon2rbox(pad_mode='linear_ramp')
    polygon2rbox(pad_mode='edge')
