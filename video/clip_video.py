import cv2
from video.bg_subtractor import filter_mask, valid_mask


def clip_videos(in_video, bg_subtractor, fg_thre=1000, write_clip_videos=False):
    # read video
    cap = cv2.VideoCapture(in_video)
    video_w, video_h = int(cap.get(3)), int(cap.get(4))


    # bg kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    print('\nrecord valid frame idx...')

    frame_idx = 0
    valid_idxs = []
    while True:
        retval, frame = cap.read()
        if not retval:
            break

        frame_mask = bg_subtractor.apply(frame, None, 0)
        frame_mask = filter_mask(frame_mask, kernel)  # 形态学操作 去掉小白点

        if valid_mask(frame_mask, fg_thre):
            valid_idxs.append(frame_idx)

        frame_idx += 1

    cap.release()

    # link valid clips by valid frame_idxs
    print('\nlink valid clips...')
    valid_clips = link_clips(valid_idxs)

    if write_clip_videos:
        # read again
        print('\nwrite valid clips')
        cap = cv2.VideoCapture(in_video)
        # write video, cv2.CAP_PROP_FRAME_COUNT = 7
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        vw_cut = cv2.VideoWriter(in_video.replace('.mp4', '_cut.mp4'), fourcc,
                                 int(cap.get(cv2.CAP_PROP_FPS)), (video_w, video_h))
        frame_idx = 0
        while True:
            retval, frame = cap.read()
            if not retval:
                break

            if len(valid_clips) > 0:
                # (begin, end)
                clip_begin_idx, clip_end_idx = valid_clips[0]
                if clip_begin_idx <= frame_idx <= clip_end_idx:
                    vw_cut.write(frame)
                # move to the next clip
                if frame_idx == clip_end_idx:
                    valid_clips.pop(0)
            else:
                break  # use up all valid clips

            frame_idx += 1

        cap.release()
        vw_cut.release()

    return valid_clips


def link_clips(frame_idxs, max_gap=10, min_clip_len=30):
    """
    link discrete valid frame_idxs to (begin, end) clips
    :param frame_idxs: valid frame idx list
    :param max_gap: if gap btw 2 valid_idxs < max_gap, assign them in one clip
    :param min_clip_len: if len(clip) < min_clip_len, discard it
    :return: clips of [(begin,end),...]
    """
    begin, end = 0, 0
    clips = []

    i = 0
    while i < len(frame_idxs) - 1:
        # clip begin idx
        while i < len(frame_idxs) - 1:
            if frame_idxs[i + 1] - frame_idxs[i] < max_gap:
                begin = i
                print('\nbegin:', frame_idxs[begin])
                break
            i += 1
        # clip end idx
        while i < len(frame_idxs) - 1:
            if frame_idxs[i + 1] - frame_idxs[i] > max_gap:
                end = i
                print('\nend:', frame_idxs[end])
                break
            # middle frame idxs
            i += 1
            print(frame_idxs[i], end=',')
            # another end signal
            if i == len(frame_idxs) - 1:
                end = i
                print('\nend:', frame_idxs[end])

        if end - begin > min_clip_len:
            clips.append((frame_idxs[begin], frame_idxs[end]))

    print('\nvalid clips')
    print(clips)

    return clips


def rewrite_video(in_video,
                  scale=0.5, pads=(0, 0, 0, 0),
                  fps=None,
                  visualize=False,
                  save_vis_video=False,
                  save_crop_video=True):
    """
    :param in_video: read video path
    :param scale: scale video
    :param pads: pad after scale (left,top,right,bottom)
    :param fps: out video fps
    :param visualize: whether to show window
    :param save_vis_video: whether to save vis video with roi drawed red box
    :param save_crop_video: whether to save crop video
    :return:
    """
    cap = cv2.VideoCapture(in_video)
    fps = int(cap.get(cv2.CAP_PROP_FPS)) if not fps else fps
    out_video = in_video.replace('.mp4', '_{}_{}.mp4'.format(scale, fps))  # add scale_fps

    resize_w, resize_h = int(cap.get(3) * scale), int(cap.get(4) * scale)  # 1920,1080 -> 960,540
    crop_pt1 = (pads[0], pads[1])
    crop_pt2 = (resize_w - pads[2], resize_h - pads[3])
    crop_w, crop_h = int(crop_pt2[0] - crop_pt1[0]), int(crop_pt2[1] - crop_pt1[1])

    fourcc = cv2.VideoWriter_fourcc(*'X264')
    vw_vis, vw_crop = None, None

    if save_vis_video:
        vw_vis = cv2.VideoWriter(out_video.replace('.mp4', '_vis.mp4'), fourcc, fps, (resize_w, resize_h))
    if save_crop_video:
        vw_crop = cv2.VideoWriter(out_video.replace('.mp4', '_crop.mp4'), fourcc, fps, (crop_w, crop_h))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, dsize=(resize_w, resize_h))

        if visualize:
            frame_vis = frame.copy()
            cv2.rectangle(frame_vis, crop_pt1, crop_pt2, (0, 0, 255), 3)
            cv2.imshow("vis", frame_vis)  # draw red roi on frame
            if cv2.waitKey(5) == ord('q') & 0xff:
                break

        if save_vis_video:
            vw_vis.write(frame_vis)

        if save_crop_video:
            frame_crop = frame[crop_pt1[1]:crop_pt2[1], crop_pt1[0]:crop_pt2[0]]
            vw_crop.write(frame_crop)

    cap.release()

    if save_vis_video:
        vw_vis.release()

    if save_crop_video:
        vw_crop.release()

    if visualize:
        cv2.destroyAllWindows()


if __name__ == '__main__':
    rewrite_video(in_video='../app/static/videos/1.mp4')
