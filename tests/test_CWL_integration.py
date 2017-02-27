"""Test CWL integration."""

import os
import sys
import subprocess

from . import tmp_dir_fixture  # NOQA
from . import TEST_SAMPLE_DATASET
from . import shasum_cwl_tool_wrapper, sha1sum_cwl_tool_wrapper


def test_agent_initialisation():
    from jobarchitect.agent import Agent

    cwl_tool_wrapper_path = shasum_cwl_tool_wrapper

    agent = Agent(dataset_path=TEST_SAMPLE_DATASET,
                  cwl_tool_wrapper_path=cwl_tool_wrapper_path)

    assert agent.output_root == "/tmp"


def test_cwl_dependency():
    import cwltool


def test_agent_cwl_job_generation():
    from jobarchitect.agent import Agent

    # program_template = "shasum {input_file} > {output_file}"
    agent = Agent(dataset_path=TEST_SAMPLE_DATASET,
                  cwl_tool_wrapper_path=shasum_cwl_tool_wrapper,
                  output_root="/tmp/output")

    from jobarchitect.utils import path_from_hash, output_path_from_hash
    expected_input_path = path_from_hash(
        TEST_SAMPLE_DATASET,
        'c827a1a1a61e734828f525ae7715d9c5be591496')
    # Expected output paths are RELATIVE paths to the current working directory
    # because CWL cannot cope with redirecting stdout to an absolute file path
    expected_output_path = output_path_from_hash(
        TEST_SAMPLE_DATASET,
        'c827a1a1a61e734828f525ae7715d9c5be591496',
        '.')

    cwl_job = agent.create_cwl_job(
        hash_str='c827a1a1a61e734828f525ae7715d9c5be591496')

    assert isinstance(cwl_job, dict)

    assert cwl_job["input_file"] == expected_input_path
    assert cwl_job["output_file"] == expected_output_path


def test_run_analysis_with_cwl(tmp_dir_fixture):  # NOQA
    from jobarchitect.agent import Agent

    cwl_tool_wrapper_path = sha1sum_cwl_tool_wrapper
    if sys.platform == "darwin":
        cwl_tool_wrapper_path = shasum_cwl_tool_wrapper

    agent = Agent(dataset_path=TEST_SAMPLE_DATASET,
                  cwl_tool_wrapper_path=cwl_tool_wrapper_path,
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


def test_analyse_by_identifiers_with_cwl(tmp_dir_fixture):  # NOQA
    from jobarchitect.agent import analyse_by_identifiers

    from jobarchitect.utils import output_path_from_hash
    expected_output_path = output_path_from_hash(
        TEST_SAMPLE_DATASET,
        'c827a1a1a61e734828f525ae7715d9c5be591496',
        tmp_dir_fixture)
    assert not os.path.isfile(expected_output_path)

    cwl_tool_wrapper_path = sha1sum_cwl_tool_wrapper
    if sys.platform == "darwin":
        cwl_tool_wrapper_path = shasum_cwl_tool_wrapper

    analyse_by_identifiers(
        cwl_tool_wrapper_path=cwl_tool_wrapper_path,
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

    cwl_tool_wrapper_path = sha1sum_cwl_tool_wrapper
    if sys.platform == "darwin":
        cwl_tool_wrapper_path = shasum_cwl_tool_wrapper

    analyse_by_identifiers(
        cwl_tool_wrapper_path=cwl_tool_wrapper_path,
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
    cwl_tool_wrapper_path = sha1sum_cwl_tool_wrapper
    if sys.platform == "darwin":
        cwl_tool_wrapper_path = shasum_cwl_tool_wrapper

    identifiers = ['c827a1a1a61e734828f525ae7715d9c5be591496',
                   '290d3f1a902c452ce1c184ed793b1d6b83b59164']

    cmd = ['_analyse_by_ids',
           '--cwl_tool_wrapper_path={}'.format(cwl_tool_wrapper_path),
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
