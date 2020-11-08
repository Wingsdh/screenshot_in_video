# -*- encoding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    rect_detect.py
   Description :
   Author :       Wings DH
   Time：         2020/11/8 11:29 上午
-------------------------------------------------
   Change Activity:
                   2020/11/8: Create
-------------------------------------------------
"""
import math

import cv2


# calculate angle
def angle(pt1, pt2, pt0):
    dx1 = pt1[0][0] - pt0[0][0]
    dy1 = pt1[0][1] - pt0[0][1]
    dx2 = pt2[0][0] - pt0[0][0]
    dy2 = pt2[0][1] - pt0[0][1]
    return float((dx1 * dx2 + dy1 * dy2)) / math.sqrt(float((dx1 * dx1 + dy1 * dy1)) * (dx2 * dx2 + dy2 * dy2) + 1e-10)


def detect_rect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # contours
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    for i in range(0, len(contours)):
        approx = cv2.approxPolyDP(contours[i], cv2.arcLength(contours[i], True) * 0.02, True)

        # Skip small or non-convex objects
        if (abs(cv2.contourArea(contours[i])) < 100 or not (cv2.isContourConvex(approx))):
            continue

        if (len(approx) == 4):
            # nb vertices of a polygonal curve
            # Use the degrees obtained above and the number of vertices
            # to determine the shape of the contour
            x, y, w, h = cv2.boundingRect(contours[i])
            if h > image.shape[0] / 2 and w > image.shape[1] / 2:
                start_point = tuple(approx[1][0])
                end_point = tuple(approx[3][0])
                rects.append((start_point, end_point))

    return rects


def detect_max_rect(image):
    rects = detect_rect(image)
    if rects:
        if len(rects) == 1:
            return rects[0]
        else:
            # 按照面积排序
            return max(rects, key=lambda x: (x[1][0] - x[0][0]) * (x[1][1] - x[0][1]))
    else:
        return None


def curve_rect(image, rect):
    start_x, start_y = rect[0]
    end_x, end_y = rect[1]
    return image[start_y:end_y, start_x:end_x]
