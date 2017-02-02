"""Tests for agent module."""

import sys


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

    Agent(
        path_to_dataset='/path/to/dataset',
        program_string='shasum')
