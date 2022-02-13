from typing import List, Dict, Any
from pathlib import Path
from dataclasses import dataclass
from src.structures.project_objects import ProjectDir
from src.utils.operate_img import *
import subprocess
import shutil


@dataclass
class Video:
    project_dir: ProjectDir
    _width: int = 1280
    _height: int = 720

    def __post_init__(self):
        if not self.project_dir.output_dir.video.exists():
            self.project_dir.output_dir.video.mkdir()

    def make_tmp_dir(self):
        if not self.project_dir.output_dir.tmp.exists():
            self.project_dir.output_dir.tmp.mkdir()

    def delete_tmp_dir(self):
        if self.project_dir.output_dir.tmp.exists():
            shutil.rmtree(self.project_dir.output_dir.tmp)


    def make(self, encoding_type='.mp4'):
        # make tmp dir
        self.make_tmp_dir()

        # read concatenated image
        concatenated_image = read_image(image_path=self.project_dir.output_dir.concatenated_image)

        # focus frame and slide right
        concatenated_image_width = concatenated_image.shape[1]
        for x in range(concatenated_image_width - self._width):
            captured_image = concatenated_image[0: self._height, x: x + self._width]
            output_path = self.project_dir.output_dir.tmp / f'{x:04}.png'
            write_image(image=captured_image, image_path=output_path)
        print('output tmp dir')

        # 連番画像 -> ffmpeg
        cmd = ['ffmpeg', '-r', '30', '-i', f'{str(self.project_dir.output_dir.tmp)}/%04d.png', '-vcodec', 'libx264', '-pix_fmt', 'yuv420p', '-r', '60', f'{str(self.project_dir.output_dir.video)}/output.mp4']
        print(' '.join(cmd))
        subprocess.run(cmd)

        # convert mp4 to gif
        # cmd = ['ffmpeg', '-i', f'{str(self.project_dir.output_dir.video / "output.mp4")}', f'{str(self.project_dir.output_dir.video / "output.gif")}']
        # print(' '.join(cmd))
        # subprocess.run(cmd)

        # ffmpeg -i input.mov -vf "palettegen" -y palette.png
        cmd = ['ffmpeg', '-i', f'{str(self.project_dir.output_dir.video / "output.mp4")}', '-vf', 'palettegen', '-y', f'{str(self.project_dir.output_dir.video / "palette.png")}']
        print(' '.join(cmd))
        subprocess.run(cmd)

        # ffmpeg -i input.mov -i palette.png -lavfi "fps=12,scale=900:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" -y output.gif
        cmd = ['ffmpeg', '-i', f'{str(self.project_dir.output_dir.video / "output.mp4")}', '-i', f'{str(self.project_dir.output_dir.video / "palette.png")}', '-y', f'{str(self.project_dir.output_dir.video / "output.gif")}']
        print(' '.join(cmd))
        subprocess.run(cmd)

        # delete tmp dir
        self.delete_tmp_dir()


def make_video(args):
    """
    :param args:
    :return:
    """
    project_name: str = args.project
    project_path: Path = Path(project_name)

    encoding_type: str = args.type

    video: Video = Video(project_dir=ProjectDir(project_path))
    video.make()
