from PIL import ImageGrab
import numpy as np
import cv2

"""
only used in MacOS and Windows, linux can't use ImageGrab!
"""

# can set a bbox=(100, 100, 800, 600)
im = ImageGrab.grab()  # bbox = total screen 1920,1080
w, h = im.size
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 15
delay = int(1000 / fps)
vw = cv2.VideoWriter('test1.avi', fourcc, 15, (w, h))  # 1920,1080

# 原始图片太大，设置窗口大小和位置
winname = '360 camera'
cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
cv2.resizeWindow(winname, 640, 360)
cv2.moveWindow(winname, 100, 100)

while True:
    im = ImageGrab.grab()
    imm = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    cv2.imshow(winname, imm)

    if cv2.waitKey(delay) & 0xFF == 27:  # esc 退出
        break
    vw.write(imm)

vw.release()
cv2.destroyAllWindows()
