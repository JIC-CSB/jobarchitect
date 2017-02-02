"""Tool to create jobs to carry out analyses on datasets."""

import argparse
import collections

_JobSpec = collections.namedtuple(
    '_JobSpec',
    ['program_template',
     'dataset_path',
     'output_root',
     'hash_ids'
     ]
)


class JobSketcher(object):
    """Class to build up jobs to analyse a dataset."""

    def __init__(self, program_template, dataset_path, output_root):
        self.program_template = program_template
        self.dataset_path = dataset_path
        self.output_root = output_root


def sketchjob():
    """Return list of job THINGS."""


def cli():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.parse_args()
