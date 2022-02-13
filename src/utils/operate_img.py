import copy
import os.path
import random
import cv2
import numpy as np
from typing import Tuple, Union, NamedTuple, List
from pathlib import Path
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont


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
    under_image[y : y + over_image_height, x : x + over_image_width] = over_image
    return under_image


def write_image(image, image_path: Path):
    cv2.imwrite(str(image_path), image)


def get_h_concatenate_image(left_image, right_image):
    left_image_height, left_image_width = left_image.shape[:2]
    right_image_height, right_image_width = right_image.shape[:2]
    assert (
        left_image_height == right_image_height
    ), f"{left_image_height} != {right_image_height}"
    return cv2.hconcat([left_image, right_image])


def read_image(image_path: Union[Path, str]):
    if type(image_path) == Path:
        assert image_path.exists(), f"{image_path} does not exists"
    if type(image_path) == str:
        assert os.path.exists(image_path), f"{image_path} does not exists"
    image = cv2.imread(str(image_path))
    return image


def resize_image(image, height: int, width: int):
    return cv2.resize(image, dsize=(height, width))


def put_text_on_image(image, text):
    text_on_image = TextOnImage(image, text)
    text_on_image.put_text_on_image()
    return text_on_image.image


def cv2_to_pillow(image: np.ndarray):
    # rgb image
    if image.shape[2] == 3:
        res = cv2.cvtColor(image.astype(np.float32), cv2.COLOR_BGR2RGB)
    return Image.fromarray(res.astype(np.uint8))


def pillow_to_cv2(pil_image):
    res = np.array(pil_image, dtype=np.uint8)
    res = cv2.cvtColor(res, cv2.COLOR_RGB2BGR)
    return res


class Font(NamedTuple):
    font: str = "kalimati.ttf"
    size: int = 50


@dataclass
class TextOnImage:
    image: np.ndarray
    text: str
    font_object: str = Font()
    _rows: List[str] = None

    def __post_init__(self):
        rows = []
        n = 9
        for i in range(0, len(self.text), n):
            row = self.text[i : i + n]
            rows.append(row)
        self._rows = rows

    def put_text_on_image(self):
        """
        :return:
        """
        font = ImageFont.truetype(
            font=self.font_object.font, size=self.font_object.size
        )
        pil_image = cv2_to_pillow(self.image)
        image_draw = ImageDraw.Draw(pil_image)
        for i, row in enumerate(self._rows):
            image_draw.text((10, 10 + 40 * i), row, fill=(255, 255, 255), font=font)
        self.image = pillow_to_cv2(pil_image)
