import cv2
import numpy as np


def concat_video(in1, in2, out):
    video_w, video_h = 642, 302
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    vw = cv2.VideoWriter(out, fourcc, 20, (video_w * 2, video_h))  # concat 2 video cols

    cap1 = cv2.VideoCapture(in1)
    cap2 = cv2.VideoCapture(in2)
    while cap1.isOpened() and cap2.isOpened():
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        if ret1 and ret2:
            out_frame = np.concatenate((frame1, frame2), axis=1)
            vw.write(out_frame)
        else:
            break
    vw.release()
    cap1.release()
    cap2.release()


def test_cat():
    img1 = cv2.imread('stereo/rgb/1.jpg')
    print(img1.shape)
    img2 = cv2.imread('stereo/seg/1.png')
    # 取完前2个元素，再反转
    img2 = cv2.resize(img2, dsize=img1.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)
    print(img1.shape)
    print(img2.shape)
    out = np.concatenate((img1, img2), axis=1)
    print(out.shape)
    cv2.imshow('out', out)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    concat_video(in1='stereo/rgb.avi',
                 in2='stereo/seg.avi',
                 out='stereo/demo.avi')
