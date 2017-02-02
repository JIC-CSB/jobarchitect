"""Tests for agent module."""

import sys

from . import TEST_SAMPLE_DATASET


def test_import_agent():
    from jobarchitect.agent import Agent


def test_create_command():
    from jobarchitect.agent import create_command

    if sys.platform == 'darwin':
        program_name = 'shasum'
    else:
        program_name = 'sha1sum'

    # e.g.:
    # shasum /path/to/file > /path/to/output
    expected_output = [program_name,
                       "/input/data/myfile.txt",
                       ">/output/data/myfile.txt"]

    actual_output = create_command(
        program_name=program_name,
        input_file="/input/data/myfile.txt",
        output_file=">/output/data/myfile.txt")

    assert expected_output == actual_output


def test_agent_initialisation():
    from jobarchitect.agent import Agent

    program_template = "shasum {input_file} > {output_file}"
    agent = Agent(dataset_path=TEST_SAMPLE_DATASET,
                  program_template=program_template)

    expected_string = "shasum /input/test.txt > /output/test.txt"
    dummy_dict = {"input_file": "/input/test.txt",
                  "output_file": "/output/test.txt"}
    assert agent.program_template.format(**dummy_dict) == expected_string

    from dtool import DataSet
    assert isinstance(agent.dataset, DataSet)
