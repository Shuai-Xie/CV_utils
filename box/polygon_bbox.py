import cv2
import numpy as np
from box.box_coords import pt_float2int


def test_one_img():
    img_info = {
        "content": "9491abae-8c82-464c-abef-82517ba372a5___images_9_1_2cqh2390.jpg",
        "annotation": [
            {"label": ["娇子_D"],
             "shape": "polygon",
             "points": [[0.0609375, 0.7138888888888889],
                        [0.3671875, 0.5083333333333333],
                        [0.4921875, 0.5694444444444444],
                        [0.4921875, 0.6972222222222222],
                        [0.1625, 0.9972222222222222],
                        [0.0953125, 0.9972222222222222],
                        [0.06875, 0.8583333333333333]],
             "notes": "",
             "imageWidth": 640,
             "imageHeight": 360}
        ]
    }
    ann = img_info['annotation'][0]
    points, img_w, img_h = ann['points'], ann['imageWidth'], ann['imageHeight']
    # points = points[::-1]   # cvt clock-wise to anti, result is same
    poly_pts = np.array([pt_float2int(pt, img_w, img_h) for pt in points])
    rect = cv2.minAreaRect(poly_pts)  # center_pts, angle
    # print(rect)

    img = cv2.imread(img_info['content'])

    # draw ori polygon
    polygon = np.array(poly_pts).astype(np.int)
    cv2.drawContours(img, contours=[polygon], contourIdx=0, color=(0, 255, 1), thickness=3)

    # draw rotated box
    rbox = cv2.boxPoints(rect)
    rbox = np.array(rbox).astype(np.int)
    cv2.drawContours(img, contours=[rbox], contourIdx=0, color=(0, 0, 255), thickness=3)

    # show points around the shape
    print(polygon)
    print(rbox)

    cv2.imwrite('rbox.png', img)


if __name__ == '__main__':
    test_one_img()
