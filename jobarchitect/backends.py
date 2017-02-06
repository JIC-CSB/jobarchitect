"""Job output backends."""

from jinja2 import Environment, PackageLoader

ENV = Environment(loader=PackageLoader('jobarchitect', 'templates'),
                  keep_trailing_newline=True)


def generate_bash_job(jobspec):
    """Return bash job script job as a string.

    The script contains code to run all analysis on all data in one chunk from
    a split dataset.

    :param jobspec: job specification as a :class:`jobarchitect.JobSpec`
    :returns: bash job script as a string
    """
    template = ENV.get_template("bash_job.sh.j2")
    return template.render(jobspec)


def generate_docker_job(jobspec):
    """Return docker job script as a string.

    The script contains code to run a docker container to analyse data.

    :param jobspec: job specification as a :class:`jobarchitect.JobSpec`
    :returns: docker job script as a string
    """

    output = """#!/bin/bash
IMAGE_NAME={image_name}
docker run  \
  --rm  \
  -v {dataset_path}:/input_dataset:ro  \
  -v {output_root}:/output  \
  $IMAGE_NAME  \
  _analyse_by_ids  \
    --program_template {program_template}  \
    --input_dataset_path=/input_dataset  \
    --output_root=/output  \
    {hash_ids}
 """.format(**jobspec)

    return output


def render_script(template_name, variables):
    """Return script as a string.
    """
    template = ENV.get_template(template_name)
    return template.render(variables)
