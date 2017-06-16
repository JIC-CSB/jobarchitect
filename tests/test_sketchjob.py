"""Test jobarchitect CLI (sketchjob)"""

import sys
import os
import subprocess

from . import TEST_SAMPLE_DATASET
from . import tmp_dir_fixture, local_tmp_dir_fixture  # NOQA
from . import shasum_smart_tool
from . import shasum_smart_import_tool


def test_generate_jobspecs():
    from jobarchitect.backends import JobSpec
    from jobarchitect.sketchjob import generate_jobspecs
    jobspecs = list(generate_jobspecs(
        tool_path="smart_tool.py",
        dataset_path=TEST_SAMPLE_DATASET,
        output_root="/tmp",
        nchunks=1))
    assert len(jobspecs) == 1
    assert isinstance(jobspecs[0], JobSpec)
    assert jobspecs[0].tool_path == "smart_tool.py"
    assert jobspecs[0].dataset_path == TEST_SAMPLE_DATASET
    assert jobspecs[0].output_root == "/tmp"
    assert len(jobspecs[0].hash_ids.split()) == 7

    jobspecs = list(generate_jobspecs(
        tool_path="smart_tool.py",
        dataset_path=TEST_SAMPLE_DATASET,
        output_root="/tmp",
        nchunks=2))
    assert len(jobspecs) == 2

    jobspecs = list(generate_jobspecs(
        tool_path="smart_tool.py",
        dataset_path=TEST_SAMPLE_DATASET,
        output_root="/tmp",
        nchunks=7))
    assert len(jobspecs) == 7
    assert len(jobspecs[0].hash_ids.split()) == 1
    assert jobspecs[0].hash_ids ==  \
        "290d3f1a902c452ce1c184ed793b1d6b83b59164"


def test_jobsketcher_initialisation():
    from jobarchitect.sketchjob import JobSketcher

    jobsketcher = JobSketcher(
        tool_path='smart_tool.py',
        dataset_path='/path/to/dataset',
        output_root='/tmp/output')

    assert jobsketcher.tool_path == 'smart_tool.py'
    assert jobsketcher.dataset_path == '/path/to/dataset'
    assert jobsketcher.output_root == '/tmp/output'


def test_jobsketcher_generate_jobspecs():
    from jobarchitect.sketchjob import JobSketcher

    jobsketcher = JobSketcher(
        tool_path='smart_tool.py',
        dataset_path=TEST_SAMPLE_DATASET,
        output_root='/tmp/output')

    jobspecs = list(jobsketcher._generate_jobspecs(nchunks=1))
    assert len(jobspecs) == 1
    from jobarchitect.backends import JobSpec
    assert isinstance(jobspecs[0], JobSpec)


def test_jobsketcher_sketch():
    from jobarchitect.sketchjob import JobSketcher, generate_jobspecs
    from jobarchitect.backends import generate_bash_job

    jobsketcher = JobSketcher(
        tool_path='smart_tool.py',
        dataset_path=TEST_SAMPLE_DATASET,
        output_root='/tmp/output')

    bash_lines = list(jobsketcher.sketch(backend=generate_bash_job, nchunks=1))

    jobspec_generator = generate_jobspecs(
        tool_path='smart_tool.py',
        dataset_path=TEST_SAMPLE_DATASET,
        output_root='/tmp/output',
        nchunks=1)

    expected_lines = [generate_bash_job(jobspec)
                      for jobspec in jobspec_generator]

    assert bash_lines == expected_lines


# This is a functional test.
def test_sketchjob(tmp_dir_fixture):  # NOQA
    from jobarchitect.sketchjob import sketchjob
    from jobarchitect.backends import generate_bash_job

    bash_lines = sketchjob(
        tool_path=shasum_smart_tool,
        dataset_path=TEST_SAMPLE_DATASET,
        output_root=tmp_dir_fixture,
        nchunks=1,
        backend=generate_bash_job)

    for line in bash_lines:
        p = subprocess.Popen(
            ['bash'],
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = p.communicate(line.encode())
        assert err.decode('utf-8') == ""

    from dtoolcore import DataSet
    from jobarchitect.utils import output_path_from_hash
    dataset = DataSet.from_path(TEST_SAMPLE_DATASET)
    for entry in dataset.manifest["file_list"]:
        output_path = output_path_from_hash(
            TEST_SAMPLE_DATASET,
            entry["hash"],
            tmp_dir_fixture)
        assert os.path.isdir(output_path)
        output_file = os.path.join(
            output_path,
            os.path.basename(entry["path"]))
        assert os.path.isfile(output_file)
        with open(output_file, "r") as fh:
            contents = fh.read()
        hash_from_output = contents.strip().split()[0]
        assert hash_from_output == entry["hash"]


# This is a functional test.
def test_sketchjob_with_docker_backend(local_tmp_dir_fixture):  # NOQA
    from jobarchitect.sketchjob import sketchjob
    from jobarchitect.backends import generate_docker_job

    bash_lines = sketchjob(
        tool_path=shasum_smart_tool,
        dataset_path=TEST_SAMPLE_DATASET,
        output_root=local_tmp_dir_fixture,
        nchunks=1,
        backend=generate_docker_job,
        image_name="jicscicomp/jobarchitect")

    for line in bash_lines:
        p = subprocess.Popen(['bash'], stdin=subprocess.PIPE)
        out, err = p.communicate(line.encode())

    from dtoolcore import DataSet
    from jobarchitect.utils import output_path_from_hash
    dataset = DataSet.from_path(TEST_SAMPLE_DATASET)
    for entry in dataset.manifest["file_list"]:
        output_path = output_path_from_hash(
            TEST_SAMPLE_DATASET,
            entry["hash"],
            local_tmp_dir_fixture)
        assert os.path.isdir(output_path)
        output_file = os.path.join(
            output_path,
            os.path.basename(entry["path"]))
        assert os.path.isfile(output_file)
        with open(output_file, "r") as fh:
            contents = fh.read()
        hash_from_output = contents.strip().split()[0]
        assert hash_from_output == entry["hash"]


def test_sketchjob_cli(tmp_dir_fixture):  # NOQA

    # Run sketchjob and capture stdout.
    cmd = [
        "sketchjob",
        shasum_smart_tool,
        TEST_SAMPLE_DATASET,
        tmp_dir_fixture,
        # "--nchunks=1",  # Default is 1.
    ]
    script_calling_analyse_by_ids = subprocess.check_output(cmd)

    assert script_calling_analyse_by_ids.decode(
        'utf-8').find("_analyse_by_ids") != -1

    # Run the script produced by sketchjob.
    p = subprocess.Popen(
        ["bash"],
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print script_calling_analyse_by_ids
    out, err = p.communicate(script_calling_analyse_by_ids)
    assert err.decode('utf-8') == ""

    # Check that the script generated by sketchjob produces the correct output.
    from dtoolcore import DataSet
    from jobarchitect.utils import output_path_from_hash
    dataset = DataSet.from_path(TEST_SAMPLE_DATASET)
    for entry in dataset.manifest["file_list"]:
        output_path = output_path_from_hash(
            TEST_SAMPLE_DATASET,
            entry["hash"],
            tmp_dir_fixture)
        assert os.path.isdir(output_path)
        output_file = os.path.join(
            output_path,
            os.path.basename(entry["path"]))
        assert os.path.isfile(output_file)
        with open(output_file, "r") as fh:
            contents = fh.read()
        hash_from_output = contents.strip().split()[0]
        assert hash_from_output == entry["hash"]


def test_sketchjob_cli_with_docker_backend(local_tmp_dir_fixture):  # NOQA

    # Run sketchjob and capture stdout.
    cmd = [
        "sketchjob",
        shasum_smart_tool,
        TEST_SAMPLE_DATASET,
        local_tmp_dir_fixture,
        # "--nchunks=1",  # Default is 1.
        "--backend=docker",
        "--image-name=jicscicomp/jobarchitect"
    ]
    script_calling_analyse_by_ids = subprocess.check_output(cmd)

    assert script_calling_analyse_by_ids.decode(
        'utf-8').find("_analyse_by_ids") != -1

    # Run the script produced by sketchjob.
    p = subprocess.Popen(
        ["bash"],
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = p.communicate(script_calling_analyse_by_ids)
    assert err.decode('utf-8') == ""

    # Check that the script generated by sketchjob produces the correct output.
    from dtoolcore import DataSet
    from jobarchitect.utils import output_path_from_hash
    dataset = DataSet.from_path(TEST_SAMPLE_DATASET)
    for entry in dataset.manifest["file_list"]:
        output_path = output_path_from_hash(
            TEST_SAMPLE_DATASET,
            entry["hash"],
            local_tmp_dir_fixture)
        assert os.path.isdir(output_path)
        output_file = os.path.join(
            output_path,
            os.path.basename(entry["path"]))
        assert os.path.isfile(output_file)
        with open(output_file, "r") as fh:
            contents = fh.read()
        hash_from_output = contents.strip().split()[0]
        assert hash_from_output == entry["hash"]


def test_sketchjob_cli_with_docker_backend_with_imports(local_tmp_dir_fixture):  # NOQA

    # Run sketchjob and capture stdout.
    cmd = [
        "sketchjob",
        shasum_smart_import_tool,
        TEST_SAMPLE_DATASET,
        local_tmp_dir_fixture,
        # "--nchunks=1",  # Default is 1.
        "--backend=docker",
        "--image-name=jicscicomp/jobarchitect"
    ]
    script_calling_analyse_by_ids = subprocess.check_output(cmd)

    assert script_calling_analyse_by_ids.decode(
        'utf-8').find("_analyse_by_ids") != -1

    # Run the script produced by sketchjob.
    p = subprocess.Popen(
        ["bash"],
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print(script_calling_analyse_by_ids)
    out, err = p.communicate(script_calling_analyse_by_ids)
    assert err.decode('utf-8') == ""

    # Check that the script generated by sketchjob produces the correct output.
    from dtoolcore import DataSet
    from jobarchitect.utils import output_path_from_hash
    dataset = DataSet.from_path(TEST_SAMPLE_DATASET)
    for entry in dataset.manifest["file_list"]:
        output_path = output_path_from_hash(
            TEST_SAMPLE_DATASET,
            entry["hash"],
            local_tmp_dir_fixture)
        assert os.path.isdir(output_path)
        output_file = os.path.join(
            output_path,
            os.path.basename(entry["path"]))
        assert os.path.isfile(output_file)
        with open(output_file, "r") as fh:
            contents = fh.read()
        hash_from_output = contents.strip().split()[0]
        assert hash_from_output == entry["hash"]


def test_sketchjob_slurm_wrapper_script(tmp_dir_fixture):  # NOQA

    # Create a job description file.
    program_template_path = os.path.join(tmp_dir_fixture, "job.tmpl")
    program_name = "sha1sum"
    if sys.platform == "darwin":
        program_name = "shasum"
    program_template = program_name + " {input_file} > {output_file}\n"
    with open(program_template_path, "w") as fh:
        fh.write(program_template)

    # Run sketchjob and capture stdout.
    cmd = [
        "sketchjob",
        program_template_path,
        TEST_SAMPLE_DATASET,
        tmp_dir_fixture,
        # "--nchunks=1",  # Default is 1.
        '--wrapper-script=slurm-single'
    ]
    script_calling_analyse_by_ids = subprocess.check_output(cmd)

    assert script_calling_analyse_by_ids.decode(
        'utf-8').find("_analyse_by_ids") != -1

    assert script_calling_analyse_by_ids.decode(
        'utf-8').find("#SBATCH") != -1


def test_sketchjob_singularity_job_command(tmp_dir_fixture):  # NOQA

    # Create a job description file.
    program_template_path = os.path.join(tmp_dir_fixture, "job.tmpl")
    program_name = "sha1sum"
    if sys.platform == "darwin":
        program_name = "shasum"
    program_template = program_name + " {input_file} > {output_file}\n"
    with open(program_template_path, "w") as fh:
        fh.write(program_template)

    # Run sketchjob and capture stdout.
    cmd = [
        "sketchjob",
        program_template_path,
        TEST_SAMPLE_DATASET,
        tmp_dir_fixture,
        # "--nchunks=1",  # Default is 1.
        '--backend=singularity',
        '--image-name=someimage'
    ]
    script_calling_analyse_by_ids = subprocess.check_output(cmd)

    assert script_calling_analyse_by_ids.decode(
        'utf-8').find("_analyse_by_ids") != -1

    assert script_calling_analyse_by_ids.decode(
        'utf-8').find("singularity exec") != -1
