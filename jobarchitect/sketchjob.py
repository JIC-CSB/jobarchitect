"""Tool to create jobs to carry out analyses on datasets."""

import argparse
import collections

from jobarchitect.utils import split_dataset

_JobSpec = collections.namedtuple(
    '_JobSpec',
    ['program_template',
     'dataset_path',
     'output_root',
     'hash_ids'
     ]
)


def generate_jobspecs(program_template, dataset_path, output_root, nchunks):
    for file_entry_list in split_dataset(dataset_path, nchunks):
        identifiers = [entry['hash'] for entry in file_entry_list]
        yield _JobSpec(
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
        for jobspec in generate_jobspecs(
            self.program_template,
            self.dataset_path,
            self.output_root,
            nchunks):
            yield jobspec

    def sketch(self, backend, nchunks):
        for jobspec in self._generate_jobspecs(nchunks):
            yield backend(jobspec)


def sketchjob():
    """Return list of job THINGS."""


def cli():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.parse_args()
