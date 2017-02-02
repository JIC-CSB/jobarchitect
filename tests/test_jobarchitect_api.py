"""Test the jobarchitect package."""

import os
import json

import pytest

from . import TEST_SAMPLE_DATASET
from . import tmp_dir_fixture  # NOQA


def test_version_is_string():
    import jobarchitect
    assert isinstance(jobarchitect.__version__, str)


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
