import random
import cv2
import numpy as np
from typing import Tuple
from pathlib import Path


def get_blank_image(height: int, width: int, rgb: Tuple[int, int, int] = None):
    blank = np.zeros((height, width, 3))
    if rgb:
        r, g, b = rgb
        blank += [r, g, b][::-1]
    return blank


def get_random_blank_image(height: int, width: int):
    blank = np.zeros((height, width, 3))
    r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    blank += [r, g, b][::-1]
    return blank


def get_synthetic_image(under_image, over_image, yx: Tuple[int, int]):
    y, x = yx
    over_image_height, over_image_width = over_image.shape[0], over_image.shape[1]
    under_image[y: y + over_image_height, x: x + over_image_width] = over_image
    return under_image


def output_image(image, image_path: Path):
    cv2.imwrite(str(image_path), image)
