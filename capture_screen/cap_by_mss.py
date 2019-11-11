from mss import mss
from PIL import ImageGrab, Image
import numpy as np
import cv2

"""
唯一符合录屏需求，fps > 15
"""

bbox = (0, 0, 800, 600)  # 定义窗口 left-top, right-bottom 坐标
monitor = {
    'left': bbox[0],
    'top': bbox[1],
    'width': bbox[2] - bbox[0],
    'height': bbox[3] - bbox[1],
}

# 视频属性
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 15
delay = int(1000 / fps)
w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
vw = cv2.VideoWriter('test1.avi', fourcc, fps, (w, h))  # mac 上 w,h 都要 *2

with mss() as mss:
    while True:
        mss_img = mss.grab(monitor=monitor)
        # mss_img = mss.grab(monitor=mss.monitors[0])  # 0 所有屏幕, 1/2 设置某个扩展屏
        frame = np.array(Image.frombytes('RGB', mss_img.size, mss_img.rgb, 'raw', 'BGR'))  # set BGR mode

        cv2.imshow('capture', frame)
        if cv2.waitKey(delay) & 0xFF == 27:  # esc 退出
            break

        vw.write(frame)

vw.release()
cv2.destroyAllWindows()
