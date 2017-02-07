"""Test the JobSpec class."""

import os

import pytest

from . import chdir_fixture  # NOQA


def test_JobSpec_initialisation():
    from jobarchitect.backends import JobSpec
    jobspec = JobSpec(
        program_template="echo {input_file} > {output_file}",
        dataset_path="/path/to/dataset",
        output_root="/tmp",
        hash_ids=[1, 2, 3])

    assert jobspec.program_template == "echo {input_file} > {output_file}"
    assert jobspec.dataset_path == "/path/to/dataset"
    assert jobspec.output_root == "/tmp"
    assert jobspec.hash_ids == "1 2 3"

    with pytest.raises(AttributeError):
        jobspec.docker_image_name

    jobspec = JobSpec(
        program_template="echo {input_file} > {output_file}",
        dataset_path="/path/to/dataset",
        output_root="/tmp",
        hash_ids=[1, 2, 3],
        image_name="ubuntu")

    assert jobspec.image_name == "ubuntu"


def test_JobSpec_getattr():
    from jobarchitect.backends import JobSpec
    jobspec = JobSpec(
        program_template="echo {input_file} > {output_file}",
        dataset_path="/path/to/dataset",
        output_root="/tmp",
        hash_ids=[1, 2, 3])

    assert jobspec["program_template"] == "echo {input_file} > {output_file}"
    assert jobspec["dataset_path"] == "/path/to/dataset"
    assert jobspec["output_root"] == "/tmp"
    assert jobspec["hash_ids"] == "1 2 3"

    with pytest.raises(KeyError):
        jobspec["docker_image_name"]

    jobspec = JobSpec(
        program_template="echo {input_file} > {output_file}",
        dataset_path="/path/to/dataset",
        output_root="/tmp",
        hash_ids=[1, 2, 3],
        image_name="ubuntu")

    assert jobspec["image_name"] == "ubuntu"


def test_JobSpec_creates_abspaths(chdir_fixture):  # NOQA
    from jobarchitect.backends import JobSpec

    jobspec = JobSpec(
        program_template="echo {input_file} > {output_file}",
        dataset_path="dataset",
        output_root="tmp",
        hash_ids=[1, 2, 3])

    assert os.path.isabs(jobspec.dataset_path)
    assert os.path.isabs(jobspec.output_root)


# Functional test.
def test_JobSpec_works_with_generate_bash_job_backend():
    from jobarchitect.backends import JobSpec, generate_bash_job

    jobspec = JobSpec(
        program_template="echo {input_file} > {output_file}",
        dataset_path="/path/to/dataset",
        output_root="/tmp",
        hash_ids=[1, 2, 3])

    job = generate_bash_job(jobspec)
    assert job.find("_analyse_by_ids") != -1
