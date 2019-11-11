# CV_utils

collect some useful **cv-related python programs**.


import libs

- opencv-python
- pillow
- numpy
- mss: 较快的录屏方式, win/linux/mac 都支持
- pyscreenshot: PIL.ImageGrab replacement for linux 比较慢

---

### capture_screen

compare **FPS** of 3 ways to capture screen
- mss >  PIL.ImageGrab > pyscreenshot

```
# 窗口 left-top, right-bottom 坐标
(0, 0, 1920, 1080),  # 4.6 > 2.4 > 0.7
(0, 0, 1440, 900),  # 6.0 > 2.2 > 0.6
(0, 0, 800, 600),  # 18.7 > 2.4 > 1.4
(0, 0, 640, 360),  # 40.5 > 2.3 > 2.3 
```