import cv2
import numpy as np


def long_edge_extraction(img, res):
    # 将图像转换为灰度图像
    img = cv2.resize(img, res)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # 计算图像的梯度
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    # 计算梯度的幅度和方向
    mag, angle = cv2.cartToPolar(sobelx, sobely, angleInDegrees=True)

    # 对幅度进行局部归一化
    kernel_size = 2
    # kernel_size = 5
    mag_norm = cv2.boxFilter(mag, -1, (kernel_size, kernel_size), normalize=True)

    # 对局部归一化的幅度进行阈值处理得到二值图像
    threshold_value = 200
    # threshold_value = 50
    _, edge = cv2.threshold(mag_norm, threshold_value, 255, cv2.THRESH_BINARY)

    # 对边缘进行形态学操作，去除噪声
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    edge = cv2.morphologyEx(edge, cv2.MORPH_CLOSE, kernel)

    # 对边缘进行曲率加权归一化
    # curvature_weight = 0.7
    curvature_weight = 0.5
    curvature_kernel_size = 1
    # curvature_kernel_size = 3
    edge_curvature = cv2.Laplacian(edge, cv2.CV_64F, ksize=curvature_kernel_size)
    edge_curvature = cv2.convertScaleAbs(edge_curvature)
    edge_curvature_norm = cv2.boxFilter(
        edge_curvature, -1, (kernel_size, kernel_size), normalize=True
    )
    edge_norm = cv2.multiply(
        mag_norm, edge_curvature_norm, scale=curvature_weight, dtype=cv2.CV_8UC3
    )
    return edge_norm


def canny(img, res):
    img = cv2.resize(img, res)
    # Convert to graycsale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)

    # Sobel Edge Detection
    sobelx = cv2.Sobel(
        src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5
    )  # Sobel Edge Detection on the X axis
    sobely = cv2.Sobel(
        src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5
    )  # Sobel Edge Detection on the Y axis
    sobelxy = cv2.Sobel(
        src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5
    )  # Combined X and Y Sobel Edge Detection

    # Canny Edge Detection
    edges = cv2.Canny(
        image=img_blur, threshold1=100, threshold2=200
    )  # Canny Edge Detection
    return edges
