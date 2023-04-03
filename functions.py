import sys
import os

import cv2
import numpy as np

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.getcwd()
    return os.path.join(base_path, relative_path)

def nonlinear_filter(img, kernel_size, statistics_function):

    img = cv2.copyMakeBorder(img, kernel_size // 2, kernel_size // 2, kernel_size // 2, kernel_size // 2,
                             cv2.BORDER_CONSTANT)

    filtered_img = np.zeros_like(img)

    for i in range(kernel_size // 2, img.shape[0] - kernel_size // 2):
        for j in range(kernel_size // 2, img.shape[1] - kernel_size // 2):
            window = img[i - kernel_size // 2:i + kernel_size // 2 + 1, j - kernel_size // 2:j + kernel_size // 2 + 1]

            filtered_img[i, j] = statistics_function(window)

    filtered_img = filtered_img[kernel_size // 2:-kernel_size // 2, kernel_size // 2:-kernel_size // 2]

    return filtered_img

def linear_contrast(image, contrast=1.0, brightness=0):
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contrast_image = cv2.convertScaleAbs(image, alpha=float(contrast), beta=brightness)

    return contrast_image

def histogram_equalization_RGB(image):
    r, g, b = cv2.split(image)

    r_eq = cv2.equalizeHist(r)
    g_eq = cv2.equalizeHist(g)
    b_eq = cv2.equalizeHist(b)

    image_eq = cv2.merge((r_eq, g_eq, b_eq))

    return image_eq

def histogram_equalization_HSV(image):
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(img_hsv)

    v_eq = cv2.equalizeHist(v)

    image_hsv_eq = cv2.merge((h, s, v_eq))
    image_eq = cv2.cvtColor(image_hsv_eq, cv2.COLOR_HSV2BGR)

    return image_eq
