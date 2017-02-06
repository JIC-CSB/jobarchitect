
def test_generate_bash_job_single_line():
    from jobarchitect.backends import generate_bash_job
    from jobarchitect import JobSpec

    parameters = dict(
        program_template='shasum',
        dataset_path='/data',
        output_root='/output',
        hash_ids='c827a1a1a61e734828f525ae7715d9c5be591496',

    )
    expected_starts = [
        "_analyse_by_ids",
        "--program_template={program_template}".format(**parameters),
        "--input_dataset_path={dataset_path}".format(**parameters),
        "--output_root={output_root}".format(**parameters),
        "{hash_ids}".format(**parameters)
    ]

    input_job = JobSpec(
        'shasum',
        '/data',
        '/output',
        ['c827a1a1a61e734828f525ae7715d9c5be591496'])

    actual_output = generate_bash_job(input_job)
    actual_output_lines = actual_output.split("\n")
    assert len(expected_starts) == len(actual_output_lines)

    for actual, expected_start in zip(actual_output_lines, expected_starts):
        actual = actual.strip()
        assert actual.startswith(expected_start)


def test_generate_bash_job_multi_line():
    from jobarchitect.backends import generate_bash_job
    from jobarchitect import JobSpec

    parameters = dict(
        program_template='shasum',
        dataset_path='/data',
        output_root='/output',
        hash_ids="1 2",

    )
    expected_starts = [
        "_analyse_by_ids",
        "--program_template={program_template}".format(**parameters),
        "--input_dataset_path={dataset_path}".format(**parameters),
        "--output_root={output_root}".format(**parameters),
        "{hash_ids}".format(**parameters)
    ]

    input_job = JobSpec(
        'shasum',
        '/data',
        '/output',
        [1, 2])

    actual_output = generate_bash_job(input_job)
    actual_output_lines = actual_output.split("\n")
    assert len(expected_starts) == len(actual_output_lines)

    for actual, expected_start in zip(actual_output_lines, expected_starts):
        actual = actual.strip()
        assert actual.startswith(expected_start)


def test_generate_docker_job_single_line():
    from jobarchitect import JobSpec
    from jobarchitect.backends import generate_docker_job

    parameters = dict(
        program_template='sha1sum',
        dataset_path='/outside/container/data',
        output_root='/outside/container/output',
        hash_ids="1 2",
        image_name="ubuntu")

    expected_starts = [
        "IMAGE_NAME={image_name}".format(**parameters),
        "docker run",
        "--rm",
        "-v {dataset_path}:/input_dataset:ro".format(**parameters),
        "-v {output_root}:/output".format(**parameters),
        "$IMAGE_NAME",
        "_analyse_by_ids",
        "--program_template {program_template}".format(**parameters),
        "--input_dataset_path=/input_dataset".format(**parameters),
        "--output_root=/output".format(**parameters),
        "{hash_ids}".format(**parameters),
    ]

    input_job = JobSpec(
        'sha1sum',
        '/outside/container/data',
        '/outside/container/output',
        [1, 2],
        image_name='ubuntu')

    actual_output = generate_docker_job(input_job)
    actual_output_lines = actual_output.split("\n")
    assert len(actual_output_lines) == len(expected_starts)

    for actual, expected_start in zip(actual_output_lines, expected_starts):
        actual = actual.strip()
        assert actual.startswith(expected_start)


def test_render_script():
    from jobarchitect.backends import render_script
    variables = {"jobs": ["echo 1", "echo 2"]}
    expected_output = """#!/bin/bash

echo 1
echo 2
"""
    script = render_script(
        template_name="basic_bash_script.sh.j2",
        variables=variables)
    assert script == expected_output


def test_render_slurm_script_single():
    from jobarchitect.backends import render_script
    variables = {"jobs": ["echo 1", "echo 2"],
                 "partition": "short",
                 "jobmem": 3000}
    expected_lines = [
        "#!/bin/bash",
        "#SBATCH --partition=short",
        "#SBATCH --mem=3000",
        "srun echo 1",
        "srun echo 2",
    ]
    script = render_script("slurm_script_single.slurm.j2", variables)
    for line in expected_lines:
        assert script.find(line) != -1


def test_render_slurm_script_multiple():
    from jobarchitect.backends import render_script
    variables = {"jobs": ["echo 1", "echo 2", "echo 3"],
                 "partition": "short",
                 "jobmem": 3000}

    script = render_script("slurm_script_multiple.slurm.j2", variables)
    assert script.count('#!/bin/bash') == 3
