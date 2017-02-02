"""Tests for agent module."""

import sys

from . import TEST_SAMPLE_DATASET
from . import tmp_dir_fixture  # NOQA


def test_agent_initialisation():
    from jobarchitect.agent import Agent

    program_template = "shasum {input_file} > {output_file}"
    agent = Agent(dataset_path=TEST_SAMPLE_DATASET,
                  program_template=program_template)

    expected_string = "shasum /input/test.txt > /output/test.txt"
    dummy_dict = {"input_file": "/input/test.txt",
                  "output_file": "/output/test.txt"}
    assert agent.program_template.format(**dummy_dict) == expected_string

    assert agent.output_root == "/tmp"

    from dtool import DataSet
    assert isinstance(agent.dataset, DataSet)


def test_create_command():
    from jobarchitect.agent import Agent

    program_template = "shasum {input_file} > {output_file}"
    agent = Agent(dataset_path=TEST_SAMPLE_DATASET,
                  program_template=program_template,
                  output_root="/tmp/output")

    from jobarchitect import path_from_hash, output_path_from_hash
    expected_input_path = path_from_hash(
        TEST_SAMPLE_DATASET,
        'c827a1a1a61e734828f525ae7715d9c5be591496')
    expected_output_path = output_path_from_hash(
        TEST_SAMPLE_DATASET,
        'c827a1a1a61e734828f525ae7715d9c5be591496',
        '/tmp/output')

    expected_output = program_template.format(
        input_file=expected_input_path,
        output_file=expected_output_path)

    assert expected_output == agent.create_command(
        hash_str='c827a1a1a61e734828f525ae7715d9c5be591496')


def test_run_analysis(tmp_dir_fixture):  # NOQA
    from jobarchitect.agent import Agent

    program_name = "sha1sum"
    if sys.platform == "darwin":
        program_name = "shasum"

    program_template = program_name + " {input_file} > {output_file}"
    agent = Agent(dataset_path=TEST_SAMPLE_DATASET,
                  program_template=program_template,
                  output_root=tmp_dir_fixture)
