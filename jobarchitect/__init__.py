"""jobarchitect package."""

import os

from dtool import DataSet

__version__ = "0.1.0"


def path_from_hash(dataset_path, hash_str):
    """Return absolute path from a dataset given a hash."""
    dataset_path = os.path.abspath(dataset_path)
    dataset = DataSet.from_path(dataset_path)
    data_path = os.path.join(dataset_path, dataset.data_directory)
    for item in dataset.manifest["file_list"]:
        if item["hash"] == hash_str:
            return os.path.join(data_path, item["path"])
    raise(KeyError("File hash not in dataset"))


def split_dataset(dataset_path, nchunks):
    """Return list of list of file entries."""
    dataset_path = os.path.abspath(dataset_path)
    dataset = DataSet.from_path(dataset_path)

    file_list = dataset.manifest["file_list"]
    num_files = len(file_list)
    chunk_size = num_files // nchunks
    left_over_files = num_files % nchunks
    index = 0
    for n in range(nchunks, 0, -1):
        chunk = []
        for i in range(chunk_size):
            chunk.append(file_list[index])
            index += 1
        if n <= left_over_files:
            chunk.append(file_list[index])
            index += 1
        yield chunk
