"""jobarchitect package."""

import os
import errno

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


def output_path_from_hash(dataset_path, hash_str, output_root):
    """Return the absolute path to which output data should be written for the
    datum specified by the given hash. This function is not responsible for
    creating the directory."""

    dataset_path = os.path.abspath(dataset_path)
    dataset = DataSet.from_path(dataset_path)

    for item in dataset.manifest["file_list"]:
        if item["hash"] == hash_str:
            return os.path.join(output_root, item["path"])
    raise(KeyError("File hash not in dataset"))


def generate_bash_job(jobspec):
    """Return bash script to run all analysis on all data in one chunk from a
    split dataset.

    jobspec should include:

    dataset_path: Path to dataset
    output_root: Root of path in which output will be written
    program_template: Template to specify analysis program to execute
    chunks: List of hashes to analyse
    """

    output = """#!/bin/bash
_analyse_by_ids \
  --program_template={program_template} \
  --input_dataset_path={dataset_path} \
  --output_root={output_root} \
  {hash_ids}
    """.format(**jobspec._asdict())

    return output
