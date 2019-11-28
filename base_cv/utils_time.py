from datetime import datetime, timedelta
import re
import os


def parse_dt_by_video_name(video_name):
    video_name = os.path.basename(video_name)
    m = re.match(r'(?P<ymd>\d{4}-\d{2}-\d{2})_(?P<hms>\d{6})', video_name)
    return datetime.strptime(m.group(), '%Y-%m-%d_%H%M%S')


def parse_Y_m_W_by_dt(dt):
    return dt.strftime('%Y'), dt.strftime('%m'), dt.strftime('%W')  # str


def parse_Y_m_W_by_video_name(video_name):
    return parse_Y_m_W_by_dt(parse_dt_by_video_name(video_name))  # str


def get_current_dt_by_frame_idx(begin_dt, frame_idx, fps):
    return begin_dt + timedelta(seconds=frame_idx / fps)


if __name__ == '__main__':
    year, month, week = parse_Y_m_W_by_dt(datetime.now())
    print(year, month, week)

    dt = datetime.now()
    print(type(dt.date()))
    dts = dt.date().strftime('%Y-%m-%d')
    print(dts)
    print(type(dts))
