import numpy as np
import cv2
import os, shutil
from datetime import datetime, date, time
from mss import mss
from PIL import Image


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def rmdir(path):
    if os.path.exists(path):
        shutil.rmtree(path)


# video attr
bbox = (0, 0, 1920, 1080)  # 扩展屏幕360相机直播在左边
monitor = {
    'left': bbox[0],
    'top': bbox[1],
    'width': bbox[2] - bbox[0],
    'height': bbox[3] - bbox[1],
}
fps = 5
fourcc = cv2.VideoWriter_fourcc(*'XVID')
save_dir = 'videos'
video_path = ''
mkdir(save_dir)

# begin/end of a day
begin_dt = datetime.combine(date=date(2019, 11, 13), time=time(7, 30, 0))
end_dt = datetime.combine(date=date(2019, 11, 13), time=time(22, 5, 59))
# 每周清理一次本地视频
begin_week = int(begin_dt.strftime('%W'))

# use mss
mss = mss()

if __name__ == '__main__':
    while True:
        # judge whether to begin a new week recording
        # and clean local saved videos
        cur_week = int(datetime.now().strftime('%W'))
        if cur_week > begin_week:
            # clean one week videos here!
            print('clean {} week records'.format(begin_week))
            rmdir(save_dir)
            # make new save dir
            print('{} week begins recording!'.format(cur_week))
            mkdir(save_dir)
            # update begin_week
            begin_week = cur_week

        cur_dt = datetime.now()
        if begin_dt.time() < cur_dt.time() < end_dt.time():

            video_name = cur_dt.strftime('%Y%m%d-%H%M%S') + '.avi'
            print('begin record:', video_name)
            print('current time:', datetime.now())

            video_path = os.path.join(save_dir, video_name)
            vw = cv2.VideoWriter(video_path, fourcc, fps, bbox[-2:])

            # first, train a bg_subtractor, just capture moved frames!

            while True:
                mss_img = mss.grab(monitor)
                frame = np.array(Image.frombytes('RGB', mss_img.size, mss_img.rgb, 'raw', 'BGR'))

                # todo: use bg_subtractor to filter frame 街上人来人往的车流
                vw.write(frame)
                # finish 1 day video record
                if datetime.now().time() > end_dt.time():
                    break
            vw.release()

            print('end record', video_name)
            print('current time:', datetime.now())

            # todo: upload captured video to nfs
            # os.system('scp %d sontal@10.214.211.205:/nfs/xs/retail_videos' % (video_path))
