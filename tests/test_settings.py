from pathlib import Path

project_json_paths_dir: Path = Path("projects")


def test_project_jsons():
    """
    :return:
    """
    for project_dir in project_json_paths_dir.iterdir():
        project_name: str = project_dir.name
        project_json: Path = project_dir / "projectX.json"
        pass


def test_descriptions_tsv():
    """
    :return:
    """
    for project_dir in project_json_paths_dir.iterdir():
        project_name: str = project_dir.name
        project_descriptions_tsv: Path = project_dir / "descriptions.tsv"
        pass


def test_layer_json_and_descriptions_tsv():
    """
    :return:
    """
    for project_dir in project_json_paths_dir.iterdir():
        pass
