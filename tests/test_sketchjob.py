"""Test jobarchitect CLI (sketchjob)"""

import sys
import os
import subprocess

from . import TEST_SAMPLE_DATASET
from . import tmp_dir_fixture  # NOQA


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
    assert jobspecs[0].hash_ids[0] ==  \
        "290d3f1a902c452ce1c184ed793b1d6b83b59164"


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
    from jobarchitect.sketchjob import JobSketcher, generate_jobspecs
    from jobarchitect.backends import generate_bash_job

    jobsketcher = JobSketcher(
        program_template='shasum {input_file} > {output_file}',
        dataset_path=TEST_SAMPLE_DATASET,
        output_root='/tmp/output')

    bash_lines = list(jobsketcher.sketch(backend=generate_bash_job, nchunks=1))

    jobspec_generator = generate_jobspecs(
        program_template='shasum {input_file} > {output_file}',
        dataset_path=TEST_SAMPLE_DATASET,
        output_root='/tmp/output',
        nchunks=1)

    expected_lines = [generate_bash_job(jobspec)
                      for jobspec in jobspec_generator]

    assert bash_lines == expected_lines


# This is a functional test.
def test_sketchjob(tmp_dir_fixture):  # NOQA
    from jobarchitect.sketchjob import sketchjob

    program_template_path = os.path.join(tmp_dir_fixture, "job.tmpl")

    program_name = "sha1sum"
    if sys.platform == "darwin":
        program_name = "shasum"
    program_template = program_name + " {input_file} > {output_file}\n"

    with open(program_template_path, "w") as fh:
        fh.write(program_template)

    bash_lines = sketchjob(
        template_path=program_template_path,
        dataset_path=TEST_SAMPLE_DATASET,
        output_root=tmp_dir_fixture,
        nchunks=1)

    for line in bash_lines:
        p = subprocess.Popen(['bash'], stdin=subprocess.PIPE)
        out, err = p.communicate(line)

    from dtool import DataSet
    from jobarchitect.utils import output_path_from_hash
    dataset = DataSet.from_path(TEST_SAMPLE_DATASET)
    for entry in dataset.manifest["file_list"]:
        output_path = output_path_from_hash(
            TEST_SAMPLE_DATASET,
            entry["hash"],
            tmp_dir_fixture)
        assert os.path.isfile(output_path)
        with open(output_path, "r") as fh:
            contents = fh.read()
        hash_from_output = contents.strip().split()[0]
        assert hash_from_output == entry["hash"]


def test_sketchjob_cli():

    cmd = ['sketchjob']

    subprocess.check_call(cmd)

    cmd = ['sketchjob', '--help']

    output = subprocess.check_output(cmd)

    assert len(output.decode('utf8')) > 0
