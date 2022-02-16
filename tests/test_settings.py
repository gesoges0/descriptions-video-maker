from pathlib import Path
from typing import Dict, Any
import json
import os
import sys

sys.path.append(os.getcwd())
from src.utils.operate_tsv import get_header_from_tsv


project_dirs_root: Path = Path("projects")


def test_project_jsons():
    """
    :return:
    """
    for project_dir in project_dirs_root.iterdir():
        project_name: str = project_dir.name
        project_json: Path = project_dir / "projectX.json"
        pass


def test_descriptions_tsv():
    """
    :return:
    """
    for project_dir in project_dirs_root.iterdir():
        project_name: str = project_dir.name
        project_descriptions_tsv: Path = project_dir / "descriptions.tsv"
        pass


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
