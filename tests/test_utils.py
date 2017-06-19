"""Test jobarchitect utils."""

import os
import json

import pytest

from dtoolcore import DataSet

from . import tmp_dir_fixture  # NOQA
from . import TEST_SAMPLE_DATASET


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


def test_split_iterable():
    from jobarchitect.utils import split_iterable

    iterable = [1, 2, 3, 4, 5, 6, 7]

    tmp_iter = split_iterable(iterable, 7)
    assert next(tmp_iter) == [1]
    assert next(tmp_iter) == [2]
    assert next(tmp_iter) == [3]
    assert next(tmp_iter) == [4]
    assert next(tmp_iter) == [5]
    assert next(tmp_iter) == [6]
    assert next(tmp_iter) == [7]

    tmp_iter = split_iterable(iterable, 6)
    assert next(tmp_iter) == [iterable[0]]
    assert next(tmp_iter) == [iterable[1]]
    assert next(tmp_iter) == [iterable[2]]
    assert next(tmp_iter) == [iterable[3]]
    assert next(tmp_iter) == [iterable[4]]
    assert next(tmp_iter) == [iterable[5], iterable[6]]

    tmp_iter = split_iterable(iterable, 5)
    assert next(tmp_iter) == [iterable[0]]
    assert next(tmp_iter) == [iterable[1]]
    assert next(tmp_iter) == [iterable[2]]
    assert next(tmp_iter) == [iterable[3], iterable[4]]
    assert next(tmp_iter) == [iterable[5], iterable[6]]

    tmp_iter = split_iterable(iterable, 4)
    assert next(tmp_iter) == [iterable[0]]
    assert next(tmp_iter) == [iterable[1], iterable[2]]
    assert next(tmp_iter) == [iterable[3], iterable[4]]
    assert next(tmp_iter) == [iterable[5], iterable[6]]

    tmp_iter = split_iterable(iterable, 3)
    assert next(tmp_iter) == [iterable[0], iterable[1]]
    assert next(tmp_iter) == [iterable[2], iterable[3]]
    assert next(tmp_iter) == [iterable[4], iterable[5], iterable[6]]

    tmp_iter = split_iterable(iterable, 2)
    assert next(tmp_iter) == [iterable[0], iterable[1], iterable[2]]
    assert next(tmp_iter) == [iterable[3], iterable[4], iterable[5],
                              iterable[6]]

    tmp_iter = split_iterable(iterable, 1)
    assert next(tmp_iter) == [iterable[0], iterable[1], iterable[2],
                              iterable[3], iterable[4], iterable[5],
                              iterable[6]]


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


def test_are_identifiers_in_dataset():
    from jobarchitect.utils import are_identifiers_in_dataset

    # Empty list returns True
    assert are_identifiers_in_dataset(TEST_SAMPLE_DATASET, [])

    bad_identifier = 'a1237a1a1a61e734828f525ae7715d9c5be591496'
    assert not are_identifiers_in_dataset(
        TEST_SAMPLE_DATASET, [bad_identifier])

    dataset = DataSet.from_path(TEST_SAMPLE_DATASET)
    actual_identifiers = dataset.identifiers

    assert are_identifiers_in_dataset(TEST_SAMPLE_DATASET, actual_identifiers)

    extended_identifiers = actual_identifiers + [bad_identifier]

    assert not are_identifiers_in_dataset(
        TEST_SAMPLE_DATASET, extended_identifiers)

    identifiers = DataSet.from_path(TEST_SAMPLE_DATASET).identifiers
    identifiers.append('garbage')

    assert not are_identifiers_in_dataset(TEST_SAMPLE_DATASET, identifiers)
