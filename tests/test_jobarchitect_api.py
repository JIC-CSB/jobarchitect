"""Test the jobarchitect package."""

import os
import json

import pytest

from . import TEST_SAMPLE_DATASET
from . import tmp_dir_fixture  # NOQA


def test_version_is_string():
    import jobarchitect
    assert isinstance(jobarchitect.__version__, str)


def test_path_from_hash():
    from jobarchitect import path_from_hash

    expected_path = os.path.join(
        TEST_SAMPLE_DATASET, "data", "real_text_file.txt")

    actual_path = path_from_hash(
        dataset_path=TEST_SAMPLE_DATASET,
        hash_str="c827a1a1a61e734828f525ae7715d9c5be591496")
    assert expected_path == actual_path

    with pytest.raises(KeyError):
        path_from_hash(TEST_SAMPLE_DATASET, "nonsense")


def test_split_dataset():
    from jobarchitect import split_dataset

    # The function returns an iterable.
    import collections
    assert isinstance(
        split_dataset(dataset_path=TEST_SAMPLE_DATASET,
                      nchunks=1),
        collections.Iterable)

    manifest_path = os.path.join(
        TEST_SAMPLE_DATASET, ".dtool", "manifest.json")
    with open(manifest_path) as fh:
        manifest = json.load(fh)
    file_list = manifest["file_list"]

    assert len(file_list) == 7

    tmp_iter = split_dataset(TEST_SAMPLE_DATASET, 7)
    assert next(tmp_iter) == [file_list[0]]
    assert next(tmp_iter) == [file_list[1]]
    assert next(tmp_iter) == [file_list[2]]
    assert next(tmp_iter) == [file_list[3]]
    assert next(tmp_iter) == [file_list[4]]
    assert next(tmp_iter) == [file_list[5]]
    assert next(tmp_iter) == [file_list[6]]

    tmp_iter = split_dataset(TEST_SAMPLE_DATASET, 6)
    assert next(tmp_iter) == [file_list[0]]
    assert next(tmp_iter) == [file_list[1]]
    assert next(tmp_iter) == [file_list[2]]
    assert next(tmp_iter) == [file_list[3]]
    assert next(tmp_iter) == [file_list[4]]
    assert next(tmp_iter) == [file_list[5], file_list[6]]

    tmp_iter = split_dataset(TEST_SAMPLE_DATASET, 5)
    assert next(tmp_iter) == [file_list[0]]
    assert next(tmp_iter) == [file_list[1]]
    assert next(tmp_iter) == [file_list[2]]
    assert next(tmp_iter) == [file_list[3], file_list[4]]
    assert next(tmp_iter) == [file_list[5], file_list[6]]

    tmp_iter = split_dataset(TEST_SAMPLE_DATASET, 4)
    assert next(tmp_iter) == [file_list[0]]
    assert next(tmp_iter) == [file_list[1], file_list[2]]
    assert next(tmp_iter) == [file_list[3], file_list[4]]
    assert next(tmp_iter) == [file_list[5], file_list[6]]

    tmp_iter = split_dataset(TEST_SAMPLE_DATASET, 3)
    assert next(tmp_iter) == [file_list[0], file_list[1]]
    assert next(tmp_iter) == [file_list[2], file_list[3]]
    assert next(tmp_iter) == [file_list[4], file_list[5], file_list[6]]

    tmp_iter = split_dataset(TEST_SAMPLE_DATASET, 2)
    assert next(tmp_iter) == [file_list[0], file_list[1], file_list[2]]
    assert next(tmp_iter) == [file_list[3], file_list[4], file_list[5],
                              file_list[6]]

    tmp_iter = split_dataset(TEST_SAMPLE_DATASET, 1)
    assert next(tmp_iter) == [file_list[0], file_list[1], file_list[2],
                              file_list[3], file_list[4], file_list[5],
                              file_list[6]]


def test_output_path_from_hash():
    from jobarchitect import output_path_from_hash

    actual_path = output_path_from_hash(
        dataset_path=TEST_SAMPLE_DATASET,
        hash_str='c827a1a1a61e734828f525ae7715d9c5be591496',
        output_root='/output')

    expected_path = os.path.join('/output', 'real_text_file.txt')

    assert actual_path == expected_path

    with pytest.raises(KeyError):
        output_path_from_hash(TEST_SAMPLE_DATASET, 'nonsense', '/output')


def test_generate_bash_job_single_line():
    from jobarchitect import generate_bash_job
    from collections import namedtuple

    JobSpec = namedtuple(
        'JobSpec',
        ['program_template',
         'dataset_path',
         'output_root',
         'hash_ids'
         ]
    )

    parameters = dict(
        program_template='shasum',
        dataset_path='/data',
        output_root='/output',
        hash_ids='c827a1a1a61e734828f525ae7715d9c5be591496',

    )
    expected_output = """#!/bin/bash
_analyse_by_ids \
  --program_template={program_template} \
  --input_dataset_path={dataset_path} \
  --output_root={output_root} \
  {hash_ids}
    """.format(**parameters)

    input_job = JobSpec(
        'shasum',
        '/data',
        '/output',
        'c827a1a1a61e734828f525ae7715d9c5be591496')

    actual_output = generate_bash_job(input_job)
    assert expected_output == actual_output


def test_generate_bash_job_multi_line():
    from jobarchitect import generate_bash_job
    from collections import namedtuple

    JobSpec = namedtuple(
        'JobSpec',
        ['program_template',
         'dataset_path',
         'output_root',
         'hash_ids'
         ]
    )

    parameters = dict(
        program_template='shasum',
        dataset_path='/data',
        output_root='/output',
        hash_ids='1 2',

    )
    expected_output = """#!/bin/bash
_analyse_by_ids \
  --program_template={program_template} \
  --input_dataset_path={dataset_path} \
  --output_root={output_root} \
  {hash_ids}
    """.format(**parameters)

    input_job = JobSpec(
        'shasum',
        '/data',
        '/output',
        '1 2')

    actual_output = generate_bash_job(input_job)
    assert expected_output == actual_output
