"""Test the jobarchitect package."""

import os

import pytest

HERE = os.path.dirname(__file__)
TEST_SAMPLE_DATASET = os.path.join(HERE, "data", "sample_data")


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
