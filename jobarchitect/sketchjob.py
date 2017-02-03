"""Tool to create jobs to carry out analyses on datasets."""

import os
import argparse
import collections

from jobarchitect import JobSpec
from jobarchitect.utils import split_dataset
from jobarchitect.backends import generate_bash_job

def generate_jobspecs(program_template, dataset_path, output_root, nchunks):
    for file_entry_list in split_dataset(dataset_path, nchunks):
        identifiers = [entry['hash'] for entry in file_entry_list]
        yield JobSpec(
            program_template,
            dataset_path,
            output_root,
            identifiers
        )


class JobSketcher(object):
    """Class to build up jobs to analyse a dataset."""

    def __init__(self, program_template, dataset_path, output_root):
        self.program_template = program_template
        self.dataset_path = dataset_path
        self.output_root = output_root

    def _generate_jobspecs(self, nchunks):
        for jobspec in generate_jobspecs(self.program_template,
                                         self.dataset_path,
                                         self.output_root,
                                         nchunks):
            yield jobspec

    def sketch(self, backend, nchunks):
        for jobspec in self._generate_jobspecs(nchunks):
            yield backend(jobspec)


def sketchjob(template_path, dataset_path, output_root,
              nchunks, backend=generate_bash_job):
    """Return list of jobs as strings."""
    with open(template_path, "r") as fh:
        program_template = fh.read().strip()
    program_template = '"{}"'.format(program_template)
    jobsketcher = JobSketcher(
        program_template=program_template,
        dataset_path=dataset_path,
        output_root=output_root)
    for job in jobsketcher.sketch(backend, nchunks):
        yield job


def cli():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_description_file", help="Template describing job")
    parser.add_argument("dataset_path", help="Path to dataset to be analysed")
    parser.add_argument("output_path", help="Path to where output will be written")
    parser.add_argument(
        "-n",
        "--nchunks",
        default=1,
        type=int,
        help="Number of chunks the job should be split up into")
    args = parser.parse_args()

    if not os.path.isfile(args.job_description_file):
        parser.error("Job description file does not exist: {}".format(
            args.job_description_file))

    if not os.path.isdir(args.dataset_path):
        parser.error("Dataset path does not exist: {}".format(
            args.dataset_path))

    for job in sketchjob(args.job_description_file,
                         args.dataset_path,
                         args.output_path,
                         args.nchunks):
        print(job)
