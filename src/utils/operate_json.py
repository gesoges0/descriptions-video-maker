from typing import List, Iterable, Any
from pathlib import Path
import csv


def read_tsv(tsv_path: Path, read_header: bool = True) -> Iterable[List[str]]:
    """
    :param tsv_path:
    :param read_header:
    :return:
    """
    assert tsv_path.exists(), f'{tsv_path} does not exists !'
    with open(tsv_path, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)
        if read_header:
            yield header
        for row in reader:
            yield row


def write_tsv(tsv_path: Path, rows: List[List[Any]]) -> None:
    """
    :param tsv_path:
    :param rows:
    :return:
    """
    with open(tsv_path, 'w') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        for row in rows:
            writer.writerow(row)


def add_tsv(tsv_path: Path, row: List[Any]) -> None:
    """
    :param tsv_path:
    :param row:
    :return:
    """
    with open(tsv_path, 'a') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(row)
