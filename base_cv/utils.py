import cv2
import os

img_ext = {
    'jpg': ['jpg', 'jpeg', 'JPG', 'JPEG'],
    'png': ['png', 'PNG']
}


def cvt_jpg_png(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_ANYDEPTH)  # any depth
    ext = img_path[-3:]
    if ext in img_ext['jpg']:  # jpg -> png
        cv2.imwrite(img_path.replace('.jpg', '.png'), img)
    elif ext in img_ext['png']:  # png -> jpg, 注意不存在 16位 jpg, 16位还是存成 png
        cv2.imwrite(img_path.replace('.png', '.jpg'), img)


if __name__ == '__main__':
    # cvt_jpg_png(img_path='../base_py/imgs/rgb.jpg')
    cvt_jpg_png(img_path='../base_py/imgs/depth.png')
