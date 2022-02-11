from pathlib import Path
from dataclasses import dataclass


@dataclass
class ProjectDir:
    project_dir_path: Path
    _descriptions_tsv_path: Path = None
    _project_json_path: Path = None

    def __post_init__(self):
        self._project_json_path = self.project_dir_path / 'setting.json'
        self._descriptions_tsv_path = self.project_dir_path / 'descriptions.tsv'

    @property
    def descriptions_tsv_path(self):
        return self._descriptions_tsv_path

    @property
    def project_json_path(self):
        return self._project_json_path
