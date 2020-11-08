# -*- encoding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    extract_video.py
   Description :
   Author :       Wings DH
   Time：         2020/11/8 9:14 上午
-------------------------------------------------
   Change Activity:
                   2020/11/8: Create
-------------------------------------------------
"""
import os
import sys

import cv2

from utils.rect_detect import detect_max_rect, curve_rect
from utils.similar import classify_hist_with_split
from utils.video import iter_video_frame_builder


def save_image(image, tgt_d_path, msec_pos):
    n_sec = msec_pos / 1000
    min_pos = int(n_sec // 60)
    sec_pos = int(n_sec % 60)
    p = os.path.join(tgt_d_path, 'screen_{}m{}s.jpg'.format(min_pos, sec_pos))
    cv2.imwrite(p, image)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    video_f_path = '/Users/handeng/Downloads/语言与智能大会3.mp4'
    tgt_d_path = './output/'
    interal = 10

    if not os.path.exists(tgt_d_path):
        os.makedirs(tgt_d_path)

    it_func = iter_video_frame_builder(video_f_path, interal)
    prev_frame = None
    for idx, (frame, pos_msec) in enumerate(it_func()):

        rect = detect_max_rect(frame)
        if rect is None:
            continue

        frame = curve_rect(frame, rect)
        if prev_frame is not None:
            similar = classify_hist_with_split(prev_frame, frame)
            if similar < 0.7:
                prev_frame = frame
                save_image(frame, tgt_d_path, pos_msec)
        else:
            save_image(frame, tgt_d_path, pos_msec)
            prev_frame = frame


if __name__ == "__main__":
    sys.exit(main())
