"""Test jobarchitect CLI (sketchjob)"""

import subprocess

from . import TEST_SAMPLE_DATASET

def test_sketchjob():
    from jobarchitect.sketchjob import sketchjob


def test_generate_jobspecs():
    from jobarchitect.sketchjob import generate_jobspecs, _JobSpec
    jobspecs = list(generate_jobspecs(
        program_template="program",
        dataset_path=TEST_SAMPLE_DATASET,
        output_root="/tmp",
        nchunks=1))
    assert len(jobspecs) == 1
    assert isinstance(jobspecs[0], _JobSpec)
    assert jobspecs[0].program_template == "program"
    assert jobspecs[0].dataset_path == TEST_SAMPLE_DATASET
    assert jobspecs[0].output_root == "/tmp"
    assert len(jobspecs[0].hash_ids) == 7

    jobspecs = list(generate_jobspecs(
        program_template="program",
        dataset_path=TEST_SAMPLE_DATASET,
        output_root="/tmp",
        nchunks=2))
    assert len(jobspecs) == 2

    jobspecs = list(generate_jobspecs(
        program_template="program",
        dataset_path=TEST_SAMPLE_DATASET,
        output_root="/tmp",
        nchunks=7))
    assert len(jobspecs) == 7
    assert len(jobspecs[0].hash_ids) == 1
    assert jobspecs[0].hash_ids[0] == "290d3f1a902c452ce1c184ed793b1d6b83b59164"


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


def test_jobsketcher_generate_jobspecs():
    from jobarchitect.sketchjob import JobSketcher

    jobsketcher = JobSketcher(
        program_template='shasum {input_file} > {output_file}',
        dataset_path=TEST_SAMPLE_DATASET,
        output_root='/tmp/output')

    jobspecs = list(jobsketcher._generate_jobspecs(nchunks=1))
    assert len(jobspecs) == 1
    from jobarchitect.sketchjob import _JobSpec
    assert isinstance(jobspecs[0], _JobSpec)


def test_jobsketcher_sketch():
    from jobarchitect.sketchjob import JobSketcher
    from jobarchitect.backends import generate_bash_job

    jobsketcher = JobSketcher(
        program_template='shasum {input_file} > {output_file}',
        dataset_path=TEST_SAMPLE_DATASET,
        output_root='/tmp/output')

    # bash_lines = jobsketcher.sketch(backend=generate_bash_job, nchunks=1)


def test_sketchjob_cli():

    cmd = ['sketchjob']

    subprocess.check_call(cmd)

    cmd = ['sketchjob', '--help']

    output = subprocess.check_output(cmd)

    assert len(output.decode('utf8')) > 0
