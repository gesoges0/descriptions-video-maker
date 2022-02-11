import copy
import json
from typing import Dict, Any, List, Tuple, NamedTuple
from src.utils.operate_tsv import read_tsv, get_list_of_ordered_dict_from_tsv
from src.utils.operate_json import load_json_as_dict
from src.utils import LAYER_JSON_PATH, DESCRIPTION_TSV_PATH
from pathlib import Path
from dataclasses import dataclass, field
from src.structures.project_objects import ProjectDir
from enum import Enum
from collections import OrderedDict


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
class Layer:
    """
    Layer is a piece of image that has height, width, (y0, x0), image/string
    """
    name: str
    coordinate: Coordinate
    height: int
    width: int
    description_type: DescriptionType
    _image_path: Path = None
    _string: str = None
    _img = None

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
            self._image_path = Path(layer_val)
        elif self.description_type == DescriptionType.string:
            self._string = layer_val

    def set_img(self):
        """
        :return:
        """
        self._img = None


@dataclass
class DescriptionImage:
    """
    DescriptionImage includes Layer that is ImageLayer or StringLayer
    """
    height: int
    width: int
    layers: List[Layer]

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
        layers_by_name: Dict[str, Layer] = {l.name: l for l in self.layers}
        for layer_name, layer_val in row_ordered_dict.items():
            layers_by_name[layer_name].set_layer(layer_val)

    def output(self):
        """
        output DescriptionImage
        :return:
        """
        # output each layers
        for i, layer in enumerate(self.layers):
            layer.set_img()
        # concatenate layers to DescriptionImage
        # 座標と画像オブジェクトを引数とする
        # concatenate_images()
        # output this DescriptionImage
        # ファイルとして出力


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
        for description_image in self._description_images:
            description_image.output()


def make_description_images(args):
    """
    :param args:
    :return:
    """
    # set project directory path
    project_path: Path = Path(f'projects/{args.project}')

    # initialize project object by project directory path
    description_images_project: DescriptionImagesProject\
        = DescriptionImagesProject.generate_by_project_dir_path_object(project_path)

    # read setting.json and initialize a description image
    description_images_project.initialize_description_image()

    # read descriptions.tsv and set description images
    description_images_project.set_values()

    # make each description image
    description_images_project.make_images()
