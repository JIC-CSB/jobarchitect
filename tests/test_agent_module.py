"""Tests for agent module."""

import sys
import os
import subprocess

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


def test_create_command():
    from jobarchitect.agent import Agent

    program_template = "shasum {input_file} > {output_file}"
    agent = Agent(dataset_path=TEST_SAMPLE_DATASET,
                  program_template=program_template,
                  output_root="/tmp/output")

    from jobarchitect.utils import path_from_hash, output_path_from_hash
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

    from jobarchitect.utils import output_path_from_hash
    expected_output_path = output_path_from_hash(
        TEST_SAMPLE_DATASET,
        'c827a1a1a61e734828f525ae7715d9c5be591496',
        tmp_dir_fixture)

    assert not os.path.isfile(expected_output_path)

    agent.run_analysis('c827a1a1a61e734828f525ae7715d9c5be591496')

    assert os.path.isfile(expected_output_path)
    with open(expected_output_path, "r") as fh:
        contents = fh.read()
    hash_from_output = contents.strip().split()[0]
    assert hash_from_output == 'c827a1a1a61e734828f525ae7715d9c5be591496'


def test_analyse_by_identifiers(tmp_dir_fixture):  # NOQA
    from jobarchitect.agent import analyse_by_identifiers

    from jobarchitect.utils import output_path_from_hash
    expected_output_path = output_path_from_hash(
        TEST_SAMPLE_DATASET,
        'c827a1a1a61e734828f525ae7715d9c5be591496',
        tmp_dir_fixture)
    assert not os.path.isfile(expected_output_path)

    program_name = "sha1sum"
    if sys.platform == "darwin":
        program_name = "shasum"
    program_template = program_name + " {input_file} > {output_file}"

    analyse_by_identifiers(
        program_template=program_template,
        dataset_path=TEST_SAMPLE_DATASET,
        output_root=tmp_dir_fixture,
        identifiers=['c827a1a1a61e734828f525ae7715d9c5be591496'])

    assert os.path.isfile(expected_output_path)
    with open(expected_output_path, "r") as fh:
        contents = fh.read()
    hash_from_output = contents.strip().split()[0]
    assert hash_from_output == 'c827a1a1a61e734828f525ae7715d9c5be591496'


def test_analyse_by_identifiers_with_multiple_identifiers(tmp_dir_fixture):  # NOQA
    from jobarchitect.agent import analyse_by_identifiers

    from jobarchitect.utils import output_path_from_hash

    identifiers = ['c827a1a1a61e734828f525ae7715d9c5be591496',
                   '290d3f1a902c452ce1c184ed793b1d6b83b59164']
    expected_output_paths = [output_path_from_hash(
        TEST_SAMPLE_DATASET, h, tmp_dir_fixture)
        for h in identifiers]
    assert not os.path.isfile(expected_output_paths[0])
    assert not os.path.isfile(expected_output_paths[1])

    program_name = "sha1sum"
    if sys.platform == "darwin":
        program_name = "shasum"
    program_template = program_name + " {input_file} > {output_file}"

    analyse_by_identifiers(
        program_template=program_template,
        dataset_path=TEST_SAMPLE_DATASET,
        output_root=tmp_dir_fixture,
        identifiers=identifiers)

    for i in [0, 1]:
        assert os.path.isfile(expected_output_paths[i])
        with open(expected_output_paths[i], "r") as fh:
            contents = fh.read()
        hash_from_output = contents.strip().split()[0]
        assert hash_from_output == identifiers[i]


def test_command_line_invocation(tmp_dir_fixture):  # NOQA
    program_name = "sha1sum"
    if sys.platform == "darwin":
        program_name = "shasum"

    program_template = program_name + " {input_file} > {output_file}"

    identifiers = ['c827a1a1a61e734828f525ae7715d9c5be591496',
                   '290d3f1a902c452ce1c184ed793b1d6b83b59164']

    cmd = ['_analyse_by_ids',
           '--program_template={}'.format(program_template),
           '--input_dataset_path={}'.format(TEST_SAMPLE_DATASET),
           '--output_root={}'.format(tmp_dir_fixture),
           ]

    cmd.extend(identifiers)

    from jobarchitect.utils import output_path_from_hash

    expected_output_paths = [output_path_from_hash(
        TEST_SAMPLE_DATASET, h, tmp_dir_fixture)
        for h in identifiers]
    assert not os.path.isfile(expected_output_paths[0])
    assert not os.path.isfile(expected_output_paths[1])

    subprocess.check_call(cmd)

    assert os.path.isfile(expected_output_paths[0])
    assert os.path.isfile(expected_output_paths[1])

    for i in [0, 1]:
        assert os.path.isfile(expected_output_paths[i])
        with open(expected_output_paths[i], "r") as fh:
            contents = fh.read()
        hash_from_output = contents.strip().split()[0]
        assert hash_from_output == identifiers[i]
