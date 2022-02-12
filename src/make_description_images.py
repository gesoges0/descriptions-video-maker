import copy
import json
from typing import Dict, Any, List, Tuple, NamedTuple, Union
from src.utils.operate_tsv import read_tsv, get_list_of_ordered_dict_from_tsv
from src.utils.operate_json import load_json_as_dict
from src.utils.operate_img import (
    get_blank_image,
    get_random_blank_image,
    get_synthetic_image,
    write_image,
    get_h_concatenate_image,
    read_image,
    resize_image
)
from src.utils import LAYER_JSON_PATH, DESCRIPTION_TSV_PATH
from pathlib import Path
from dataclasses import dataclass, field
from src.structures.project_objects import ProjectDir
from enum import Enum
from collections import OrderedDict
from abc import ABC, abstractmethod


class DescriptionType(Enum):
    string = 1
    image = 2


class Coordinate(NamedTuple):
    y: int
    x: int

    def __add__(self, other):
        return Coordinate(self.y + other.y, self.x + other.x)

    def __sub__(self, other):
        return Coordinate(self.y - other.y, self.x - other.x)


@dataclass
class ImageLayer:
    image_path: Path
    height: int
    width: int
    _img = None

    def __post_init__(self):
        under_img = get_random_blank_image(self.height, self.width)
        over_img = resize_image(read_image(self.image_path), height=self.height, width=self.width)
        self._img = get_synthetic_image(under_image=under_img, over_image=over_img, yx=(0, 0))


@dataclass
class StringLayer:
    string: str
    height: int
    width: int
    _img = None

    def __post_init__(self):
        # mock
        self._img = get_random_blank_image(self.height, self.width)


@dataclass
class Layer:
    """
    This class knows where it will be placed in DescriptionImage, because this has coordinates.
    """
    name: str
    coordinate: Coordinate
    height: int
    width: int
    description_type: DescriptionType
    _img: Union[ImageLayer, StringLayer] = None

    @classmethod
    def generate_by_2_coordinate(cls, name: str, c0: Coordinate, c1: Coordinate, description_type: DescriptionType):
        name: str = name
        height: int = (c1 - c0).y
        width: int = (c1 - c0).x
        return Layer(name, c0, height, width, description_type)

    def set_layer(self, layer_val: str):
        """
        add string to layer / add image to layer
        :param layer_val:
        :return:
        """
        if self.description_type == DescriptionType.image:
            self._img = ImageLayer(layer_val, self.height, self.width)
        elif self.description_type == DescriptionType.string:
            self._img = StringLayer(layer_val, self.height, self.width)


@dataclass
class DescriptionImage:
    """
    DescriptionImage includes Layer that is ImageLayer or StringLayer
    """
    height: int
    width: int
    layers: List[Layer]
    _img = None

    @classmethod
    def generate_by_project_json(cls, json_path: Path):
        project_dict: Dict[str, Any] = load_json_as_dict(json_path)
        description_image_dict: Dict[str, Any] = project_dict['description_image']
        height = description_image_dict['height']
        width = description_image_dict['width']

        layers: List[Layer] = []
        for layer_name, layer_setting_dict in description_image_dict['layers'].items():
            name: str = layer_name
            description_type: DescriptionType = getattr(DescriptionType, layer_setting_dict['description_type'])
            y0, y1 = layer_setting_dict['height']
            x0, x1 = layer_setting_dict['width']
            c0, c1 = Coordinate(y=y0, x=x0), Coordinate(y=y1, x=x1)
            layer: Layer = Layer.generate_by_2_coordinate(name, c0, c1, description_type)
            layers.append(layer)

        return DescriptionImage(height, width, layers)

    def set_description_to_layers(self, row_ordered_dict: OrderedDict):
        """
        set each row of tsv to each layer
        :return:
       """
        layers_by_name: Dict[str, Layer] = {layer.name: layer for layer in self.layers}
        for layer_name, layer_val in row_ordered_dict.items():
            layers_by_name[layer_name].set_layer(layer_val)

    def make(self):
        """
        :return: DescriptionImage
        """
        # make frame
        frame = get_blank_image(height=self.height, width=self.width)

        # concatenate all layers to one description image
        for layer in self.layers:
            frame = get_synthetic_image(under_image=frame,
                                        over_image=layer._img._img,
                                        yx=(layer.coordinate.y, layer.coordinate.x),
                                        )
        self._img = frame
        return frame

    @property
    def img(self):
        return self._img


@dataclass
class DescriptionImagesProject:
    """
    DescriptionImagesProject includes DescriptionImages that is a picture configured by a few of layers.
    This class has methods to make videos, so I don't name 'DescriptionImagesProject' , but 'DescriptionImages'.
    """
    project_dir: ProjectDir
    _project_name: str = None
    _description_image_base: DescriptionImage = None
    _description_images: List[DescriptionImage] = field(default_factory=list)
    _padding: int = 1

    def __post_init__(self):
        self._project_name = self.project_dir.project_dir_path.name

    @classmethod
    def generate_by_project_dir_path_object(cls, project_path: Path):
        project_dir_path_object: ProjectDir = ProjectDir(project_path)
        return cls(project_dir_path_object)

    def initialize_description_image(self) -> None:
        """
        read setting.json and initialize DescriptionImage Instance
        :return: None
        """
        json_path: Path = self.project_dir.project_json_path
        self._description_image_base = DescriptionImage.generate_by_project_json(json_path)

    def set_values(self) -> None:
        """
        read description.tsv and set description to the layers
        :return:
        """
        tsv_path = self.project_dir.descriptions_tsv_path

        # generate base description images
        for _ in read_tsv(tsv_path, read_header=False):
            description_image: DescriptionImage = copy.deepcopy(self._description_image_base)
            self._description_images.append(description_image)

        # set each row value to each description image
        for description_index, row_ordered_dict in enumerate(get_list_of_ordered_dict_from_tsv(tsv_path)):
            self._description_images[description_index].set_description_to_layers(row_ordered_dict)

    def make_images(self):
        """
        make each DescriptionImage and output {project_name}/each
        :return:
        """
        # each description image
        for i, description_image in enumerate(self._description_images):
            image_object = description_image.make()
            write_image(image_object, self.project_dir.output_dir.each / f'{i}.png')

        # concatenate description images to one image
        concatenated_image = self._description_images[0].img
        if len(self._description_images) > 1:
            for description_image in self._description_images[1:]:
                padding_image = get_blank_image(
                    height=description_image.height,
                    width=self._padding,
                    rgb=(255, 255, 255)
                )
                # padding
                concatenated_image = get_h_concatenate_image(concatenated_image, padding_image)
                concatenated_image = get_h_concatenate_image(concatenated_image, description_image.img)

        # output concatenated image
        output_path = self.project_dir.output_dir.concat / 'output.png'
        write_image(concatenated_image, output_path)


def make_description_images(args):
    """
    :param args:
    :return:
    """
    # set project directory path
    project_name: str = args.project
    project_path: Path = Path(f'projects/{project_name}')

    # initialize project object by project directory path
    description_images_project: DescriptionImagesProject\
        = DescriptionImagesProject.generate_by_project_dir_path_object(project_path)

    # read setting.json and initialize a description image
    description_images_project.initialize_description_image()

    # read descriptions.tsv and set description images
    description_images_project.set_values()

    # make each description image
    description_images_project.make_images()
