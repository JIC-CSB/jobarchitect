"""Test jobarchitect CLI (sketchjob)"""

import subprocess

from . import TEST_SAMPLE_DATASET

def test_sketchjob():
    from jobarchitect.sketchjob import sketchjob


def test_jobsketcher_initialisation():
    from jobarchitect.sketchjob import JobSketcher

    jobsketcher = JobSketcher(
        program_template='shasum {input_file} > {output_file}',
        dataset_path='/path/to/dataset',
        output_root='/tmp/output')

    assert jobsketcher.program_template == \
        'shasum {input_file} > {output_file}'
    assert jobsketcher.dataset_path == '/path/to/dataset'
    assert jobsketcher.output_root == '/tmp/output'


def test_jobsketcher_sketch():
    from jobarchitect.sketchjob import JobSketcher
    from jobarchitect.backends import generate_bash_job

    jobsketcher = JobSketcher(
        program_template='shasum {input_file} > {output_file}',
        dataset_path=TEST_SAMPLE_DATASET,
        output_root='/tmp/output')

    bash_lines = jobsketcher.sketch(backend=generate_bash_job, nchunks=1)


def test_sketchjob_cli():

    cmd = ['sketchjob']

    subprocess.check_call(cmd)

    cmd = ['sketchjob', '--help']

    output = subprocess.check_output(cmd)

    assert len(output.decode('utf8')) > 0
