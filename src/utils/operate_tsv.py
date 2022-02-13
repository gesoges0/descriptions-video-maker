from typing import List, Iterable, Any, Dict
from pathlib import Path
import csv
from collections import OrderedDict


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


def write_tsv_including_json(tsv_path: Path, rows: List[List[Any]]) -> None:
    """
    :param tsv_path:
    :param rows:
    :return:
    """
    with open(tsv_path, 'w') as f:
        for row in rows:
            f.write('\t'.join(map(str, row)))
            f.write('\n')


def add_tsv_including_json(tsv_path: Path, row: List[Any]) -> None:
    """
    :param tsv_path:
    :param row:
    :return:
    """
    with open(tsv_path, 'a') as f:
        f.write('\t'.join(map(str, row)))
        f.write('\n')


def get_header_from_tsv(tsv_path: Path) -> List[str]:
    """
    :param tsv_path:
    :return:
    """
    header: List[str] = next(read_tsv(tsv_path, read_header=True))
    return header


def get_list_of_dict_from_tsv(tsv_path: Path) -> List[Dict[str, str]]:
    """
    :param tsv_path:
    :return:
    """
    res: List[Dict[str, str]] = []
    header = get_header_from_tsv(tsv_path)
    for row in read_tsv(tsv_path, read_header=False):
        res.append({k: v for k, v in zip(header, row)})
    return res


def get_list_of_ordered_dict_from_tsv(tsv_path: Path) -> List[OrderedDict]:
    """
    :param tsv_path:
    :return:
    """
    res: List[OrderedDict[str, str]] = []
    header = get_header_from_tsv(tsv_path)
    for row in read_tsv(tsv_path, read_header=False):
        res.append(OrderedDict({k: v for k, v in zip(header, row)}))
    return res
