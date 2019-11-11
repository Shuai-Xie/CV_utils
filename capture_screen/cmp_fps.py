from mss import mss
import pyscreenshot as pss  # substitue of PIL.ImageGrab on linux
from PIL import Image, ImageGrab
import numpy as np
import cv2


def cvt_bbox_to_monitor(bbox):
    # Each monitor is a dict with:
    return {
        'left': bbox[0],
        'top': bbox[1],
        'width': bbox[2] - bbox[0],
        'height': bbox[3] - bbox[1],
    }


# init mss
mss = mss()


def cap_by_mss(bbox):
    mss_img = mss.grab(monitor=cvt_bbox_to_monitor(bbox))
    # mss_img = mss.grab(monitor=mss.monitors[0])  # 0 所有屏幕, 1/2 设置某个扩展屏
    frame = np.array(Image.frombytes('RGB', mss_img.size, mss_img.rgb, 'raw', 'BGR'))  # set BGR mode
    return frame


def cap_by_ImageGrab(bbox):
    # 如果不设定 bbox，默认截取整个屏幕
    # 当有多个显示器时，可以按照显示器的排列设置 bbox 坐标，如左边显示器 (0,0,1920,1080)
    img = ImageGrab.grab(bbox=bbox)
    frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return frame


def cap_by_pss(bbox):
    img = pss.grab(bbox=bbox)
    frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return frame


def cal_capture_fps(cap_fuc, bbox, s=10):
    """
    传入截屏函数 cap_fuc，计算 s 秒内 fps 的均值
    """
    print('{}:'.format(cap_fuc.__name__))  # 打印函数名称
    cnt_time = cnt_frames = 0
    tick_frequency = cv2.getTickFrequency()  # 1000000000.0
    while True:
        t1 = cv2.getTickCount()
        cap_fuc(bbox=bbox)
        t2 = cv2.getTickCount()

        cnt_frames += 1
        cnt_time += (t2 - t1) / tick_frequency
        print('\r{}/{}'.format(cnt_frames, cnt_time), end='')

        if cnt_time >= s:
            fps = cnt_frames / s
            print('\navg fps:', fps)
            return fps


if __name__ == '__main__':
    bboxes = [
        # 窗口 left-top, right-bottom 坐标
        # mss > ImageGrab > pss
        (0, 0, 1920, 1080),  # 4.6 > 2.4 > 0.7
        (0, 0, 1440, 900),  # 6.0 > 2.2 > 0.6
        (0, 0, 800, 600),  # 18.7 > 2.4 > 1.4
        (0, 0, 640, 360),  # 40.5 > 2.3 > 2.3
    ]

    for bbox in bboxes:
        print(bbox)
        cal_capture_fps(cap_by_mss, bbox)
        cal_capture_fps(cap_by_ImageGrab, bbox)
        cal_capture_fps(cap_by_pss, bbox)
