# -*- encoding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    video.py
   Description :
   Author :       Wings DH
   Time：         2020/11/8 9:11 上午
-------------------------------------------------
   Change Activity:
                   2020/11/8: Create
-------------------------------------------------
"""

# 导入所需要的库
import os

import cv2
import numpy as np

from utils.similar import classify_hist_with_split


def __get_video_info(video_capture):
    # CAP_PROP_POS_MSEC       视频文件的当前位置（播放）以毫秒为单位。
    # CAP_PROP_POS_FRAMES     基于以0开始的被捕获或解码的帧索引
    # CAP_PROP_POS_AVI_RATIO  视频文件的相对位置（播放）：0 = 电影开始，1 = 影片的结尾。
    # CAP_PROP_FRAME_WIDTH    在视频流的帧的宽度。
    # CAP_PROP_FRAME_HEIGHT   在视频流的帧的高度。
    # CAP_PROP_FPS            帧速率
    # CAP_PROP_FOURCC         编解码的4字 - 字符代码
    # CAP_PROP_FRAME_COUNT 视频文件中的帧数
    # CAP_PROP_FORMAT 返回对象的格式
    # CAP_PROP_MODE 返回后端特定的值，该值指示当前捕获模式
    # CAP_PROP_BRIGHTNESS 图像的亮度(仅适用于照相机)
    # CAP_PROP_CONTRAST 图像的对比度(仅适用于照相机)。
    # CAP_PROP_SATURATION 图像的饱和度(仅适用于照相机)。
    # CAP_PROP_HUE 色调图像(仅适用于照相机)
    # CAP_PROP_GAIN 图像增益(仅适用于照相机)（Gain在摄影中表示白平衡提升）
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    return fps


def iter_video_frame_builder(video_f_path, interval=10):
    """
    build a iteration for each frame in a video file.
    :param video_f_path: video file path
    :param interval: unit - second
    :return:
    """
    if not os.path.exists(video_f_path):
        raise FileNotFoundError(f'Please check video exist, "{video_f_path}"')

    msec_interval = interval * 1000

    def _iter_video_frame():
        video_capture = cv2.VideoCapture(video_f_path)
        next_frame_msec = 0
        while video_capture.isOpened():
            ret, frame = video_capture.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            pos_msec = video_capture.get(cv2.CAP_PROP_POS_MSEC)
            if pos_msec > next_frame_msec:
                next_frame_msec += msec_interval
                yield frame, pos_msec

    return _iter_video_frame
