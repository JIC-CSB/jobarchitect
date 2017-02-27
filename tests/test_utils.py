"""Test jobarchitect utils."""

import os
import json

import pytest

from . import tmp_dir_fixture  # NOQA
from . import TEST_SAMPLE_DATASET


def test_tmp_dir_context():
    from jobarchitect.utils import tmp_dir_context

    with tmp_dir_context() as d:
        assert os.path.isdir(d)

    assert not os.path.isdir(d)


def test_mkdir_parents(tmp_dir_fixture):  # NOQA
    from jobarchitect.utils import mkdir_parents

    partial_path_a = os.path.join(tmp_dir_fixture, 'a')
    assert not os.path.isdir(partial_path_a)
    partial_path_b = os.path.join(partial_path_a, 'b')
    assert not os.path.isdir(partial_path_b)
    dir_path_with_parents = os.path.join(tmp_dir_fixture, 'a', 'b', 'c')
    assert not os.path.isdir(dir_path_with_parents)

    mkdir_parents(dir_path_with_parents)

    assert os.path.isdir(partial_path_a)
    assert os.path.isdir(partial_path_b)
    assert os.path.isdir(dir_path_with_parents)

    # This should not raise error about already existing
    mkdir_parents(dir_path_with_parents)


def test_path_from_hash():
    from jobarchitect.utils import path_from_hash

    expected_path = os.path.join(
        TEST_SAMPLE_DATASET, "data", "real_text_file.txt")

    actual_path = path_from_hash(
        dataset_path=TEST_SAMPLE_DATASET,
        hash_str="c827a1a1a61e734828f525ae7715d9c5be591496")
    assert expected_path == actual_path

    with pytest.raises(KeyError):
        path_from_hash(TEST_SAMPLE_DATASET, "nonsense")


def test_split_dataset():
    from jobarchitect.utils import split_dataset

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
    from jobarchitect.utils import output_path_from_hash

    actual_path = output_path_from_hash(
        dataset_path=TEST_SAMPLE_DATASET,
        hash_str='c827a1a1a61e734828f525ae7715d9c5be591496',
        output_root='/output')

    expected_path = os.path.join('/output', 'real_text_file.txt')

    assert actual_path == expected_path

    with pytest.raises(KeyError):
        output_path_from_hash(TEST_SAMPLE_DATASET, 'nonsense', '/output')
