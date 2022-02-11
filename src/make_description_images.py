import json
from typing import Dict, Any, List, Tuple, NamedTuple
from src.utils.operate_tsv import read_tsv
from src.utils import LAYER_JSON_PATH, DESCRIPTION_TSV_PATH
from pathlib import Path
from dataclasses import dataclass, field
from src.structures.project_objects import ProjectDir
from enum import Enum


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
    name: str
    coordinate: Coordinate
    height: int
    width: int
    description_type: DescriptionType

    @classmethod
    def generate_by_2_coordinate(cls, name: str, c0: Coordinate, c1: Coordinate, description_type: DescriptionType):
        name: str = name
        height: int = (c1 - c0).y
        width: int = (c1 - c0).x
        return Layer(name, c0, height, width, description_type)


@dataclass
class DescriptionImage:
    height: int
    width: int
    layers: List[Layer]

    @classmethod
    def generate_by_project_json(cls, json_path: Path):
        with open(json_path, 'r', encoding='utf-8') as f:
            project_dict: Dict[str, Any] = json.load(f)
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


@dataclass
class DescriptionImageProject:
    project_dir: ProjectDir
    _project_name: str = None
    _description_image: DescriptionImage = None

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
        self._description_image = DescriptionImage.generate_by_project_json(json_path)

    def set_description(self) -> None:
        """
        read description.tsv and set description to the layers
        :return:
        """
        pass

def make_description_images(args):
    """
    :param args:
    :return:
    """
    # set project directory path
    project_path: Path = Path(f'projects/{args.project}')

    # initialize project object by project directory path
    description_image_project: DescriptionImageProject\
        = DescriptionImageProject.generate_by_project_dir_path_object(project_path)

    # read setting.json and initialize a description image
    description_image_project.initialize_description_image()

    # read descriptions.tsv and make description images




