import cv2

# 原始图片太大，设置窗口大小和位置
winname = '360 camera'
cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
cv2.resizeWindow(winname, 640, 360)  # 大小，当要显示的图片太大时，可用这个属性
cv2.moveWindow(winname, 100, 100)  # 移动

# 在定义的窗口显示图片
# cv2.imshow(winname, img)
