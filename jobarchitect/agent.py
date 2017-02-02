"""Jobarchitect agent."""

import subprocess

from dtool import DataSet

from jobarchitect import path_from_hash, output_path_from_hash


class Agent(object):
    """Class to create commands to analyse data."""

    def __init__(self, program_template, dataset_path, output_root="/tmp"):
        self.program_template = program_template
        self.dataset_path = dataset_path
        self.output_root = output_root

    def create_command(self, hash_str):
        input_file = path_from_hash(self.dataset_path, hash_str)
        output_file = output_path_from_hash(
            self.dataset_path, hash_str, self.output_root)
        return self.program_template.format(
            input_file=input_file,
            output_file=output_file)

    def run_analysis(self, hash_str):
        """Run the analysis on an item in the dataset."""
        command = self.create_command(hash_str)
        subprocess.call(command, shell=True)


def analyse_by_identifier(program_template, dataset_path, output_root, identifiers):
    """Run analysis on identifiers."""
    agent = Agent(program_template, dataset_path, output_root)
    for i in identifiers:
        agent.run_analysis(i)
