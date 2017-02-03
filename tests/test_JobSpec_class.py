"""Test the JobSpec class."""

import pytest


def test_JobSpec_initialisation():
    from jobarchitect import JobSpec
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
    from jobarchitect import JobSpec
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


# Functional test.
def test_JobSpec_works_with_generate_bash_job_backend():
    from jobarchitect import JobSpec
    from jobarchitect.backends import generate_bash_job

    jobspec = JobSpec(
        program_template="echo {input_file} > {output_file}",
        dataset_path="/path/to/dataset",
        output_root="/tmp",
        hash_ids=[1, 2, 3])

    job = generate_bash_job(jobspec)
    assert job.find("_analyse_by_ids") != -1