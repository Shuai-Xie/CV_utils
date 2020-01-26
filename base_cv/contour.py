import cv2
import numpy as np


def test_contour(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(src=imgray, thresh=127, maxval=255, type=cv2.THRESH_BINARY)

    _, contours, hierarchy = cv2.findContours(image=binary, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    # find contour having max_num pts
    max_pts = contours[0].shape[0]
    max_idx = 0
    for i in range(len(contours)):
        if contours[i].shape[0] > max_pts:
            max_pts = contours[i].shape[0]
            max_idx = i

    cnt = contours[max_idx]  # (386, 1, 2)
    for i in range(cnt.shape[0]):
        cv2.circle(img, center=(cnt[i][0][0], cnt[i][0][1]), radius=1, color=(0, 0, 255), thickness=-1)

    ellipse = cv2.fitEllipse(cnt)

    cv2.ellipse(img, ellipse, color=(0, 255, 0), thickness=2)

    cv2.imshow('fitEllipse', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def test_Ellipse(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(src=imgray, thresh=180, maxval=255, type=cv2.THRESH_BINARY)

    find = np.where(binary == 255)  # return tuple
    cnt = np.vstack(find).T
    cnt = cnt[:, np.newaxis, :][:, :, ::-1]  # (6000, 1, 2)

    # 并不是把所有点都包裹进去
    ellipse = cv2.fitEllipse(cnt)

    # cvt binary to 3-channels
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j] = [binary[i][j], binary[i][j], binary[i][j]]

    cv2.ellipse(img, ellipse, color=(0, 255, 0), thickness=2)
    cv2.imshow('fitEllipse', img)


def test_EllipseAMS(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(src=imgray, thresh=180, maxval=255, type=cv2.THRESH_BINARY)

    find = np.where(binary == 255)  # return tuple
    cnt = np.vstack(find).T
    cnt = cnt[:, np.newaxis, :][:, :, ::-1]  # (6000, 1, 2)

    # 并不是把所有点都包裹进去
    ellipse = cv2.fitEllipseAMS(cnt)

    # cvt binary to 3-channels
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j] = [binary[i][j], binary[i][j], binary[i][j]]

    cv2.ellipse(img, ellipse, color=(0, 255, 0), thickness=2)
    cv2.imshow('fitEllipseAMS', img)


def test_EllipseDirect(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(src=imgray, thresh=180, maxval=255, type=cv2.THRESH_BINARY)

    find = np.where(binary == 255)  # return tuple
    cnt = np.vstack(find).T
    cnt = cnt[:, np.newaxis, :][:, :, ::-1]  # (6000, 1, 2)

    # 并不是把所有点都包裹进去
    ellipse = cv2.fitEllipseDirect(cnt)

    # cvt binary to 3-channels
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j] = [binary[i][j], binary[i][j], binary[i][j]]

    cv2.ellipse(img, ellipse, color=(0, 255, 0), thickness=2)
    cv2.imshow('fitEllipseDirect', img)


if __name__ == '__main__':
    image = cv2.imread('j20.jpeg')
    # 后2种结果基本一致，第1种计算的ellipse较大
    test_Ellipse(image)
    test_EllipseAMS(image)
    test_EllipseDirect(image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
