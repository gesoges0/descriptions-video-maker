from pathlib import Path
from dataclasses import dataclass

OUTPUT_ROOT_PATH = Path('output')


@dataclass
class OutputDir:
    output_dir_path: Path
    _concat: Path = None
    _each: Path = None
    _video: Path = None
    _tmp: Path = None
    _concatenated_image: Path = None

    def __post_init__(self):
        self._each = self.output_dir_path / 'each'
        self._concat = self.output_dir_path / 'concat'
        self._video = self.output_dir_path / 'video'
        self._tmp = self._video / 'tmp'
        self._concatenated_image = self._concat / 'output.png'

    @property
    def concat(self):
        return self._concat

    @property
    def each(self):
        return self._each

    @property
    def video(self):
        return self._video

    @property
    def tmp(self):
        return self._tmp

    @property
    def concatenated_image(self):
        return self._concatenated_image

@dataclass
class ProjectDir:
    project_dir_path: Path
    _descriptions_tsv_path: Path = None
    _project_json_path: Path = None
    _output_dir: OutputDir = None

    def __post_init__(self):
        self._project_json_path = self.project_dir_path / 'setting.json'
        self._descriptions_tsv_path = self.project_dir_path / 'descriptions.tsv'
        project_name: str = str(self.project_dir_path).split('/')[-1]
        self._output_dir = OutputDir(OUTPUT_ROOT_PATH / f'{project_name}')

    @property
    def descriptions_tsv_path(self):
        return self._descriptions_tsv_path

    @property
    def project_json_path(self):
        return self._project_json_path

    @property
    def output_dir(self):
        return self._output_dir
