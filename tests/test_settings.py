from pathlib import Path
from typing import Dict, Any, List, Tuple
import json
import os
import sys

sys.path.append(os.getcwd())
from src.utils.operate_tsv import get_header_from_tsv


project_dirs_root: Path = Path("projects")


def test_descriptions_tsv():
    """
    :return:
    """
    for project_dir in project_dirs_root.iterdir():
        project_name: str = project_dir.name
        project_descriptions_tsv: Path = project_dir / "descriptions.tsv"
        pass


class TestJson:
    def test_project_jsons(self):
        """
        check sum of each layer's height is total height
        :return:
        """
        for project_dir in project_dirs_root.iterdir():
            json_path = project_dir / "setting.json"

            with open(json_path, "r", encoding="utf-8") as f:
                setting_dict: Dict[str, Any] = json.load(f)
                total_height: int = setting_dict["description_image"]["height"]
                heights: List[Tuple[int, int]] = []
                for layer, layer_dict in setting_dict["description_image"]["layers"].items():
                    height: Tuple[int, int] = tuple(layer_dict["height"])
                    heights.append(height)
            heights.sort()

            # check coordinates
            for i, (y1, y2) in enumerate(heights):
                assert y1 < y2, f'[JSON: {json_path}] ({y1, y2}) is not y1 < y2'

            # duplicate check
            for i in range(len(heights) - 1):
                assert heights[i][1] <= heights[i+1][0], f'[JSON:{json_path}] {heights[i]}, {heights[i+1]} is Duplicate'

            # total height
            assert heights[-1][1] <= total_height, \
                f'[JSON: {json_path}] total_height: {total_height} < sum of layers height: {heights[-1][1]}'


class TestJsonAndTsv:
    def test_layer_json_and_descriptions_tsv(self):
        """
        check Consistency of layer names json has and header name tsv has
        :return:
        """
        for project_dir_path in project_dirs_root.iterdir():
            json_path = project_dir_path / "setting.json"
            tsv_path = project_dir_path / "descriptions.tsv"

            with open(json_path, "r", encoding="utf-8") as f:
                setting_dict: Dict[str, Any] = json.load(f)

                # key error
                assert (
                    "description_image" in setting_dict
                ), f"description_image not in {str(json_path)}"
                assert (
                    "layers" in setting_dict["description_image"]
                ), f"layers not in the lower layer of description_image in {str(json_path)}"

                # layer error
                header = get_header_from_tsv(tsv_path)
                assert len(header) == len(
                    setting_dict["description_image"]["layers"].keys()
                ), (
                    f"len(header) = {len(header)}, "
                    f'len(layers) of json = {len(setting_dict["description_image"]["layers"].keys())}'
                )
                for column_name, layer_name in zip(
                    header, setting_dict["description_image"]["layers"].keys()
                ):
                    assert column_name == layer_name, f"{column_name} != {layer_name}"
