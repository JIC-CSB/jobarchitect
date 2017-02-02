"""Jobarchitect agent."""

import subprocess

from dtool import DataSet

from jobarchitect import path_from_hash, output_path_from_hash


class Agent(object):
    """Class to create commands to analyse data."""

    def __init__(self, dataset_path, program_template, output_root="/tmp"):
        self.dataset_path = dataset_path
        self.program_template = program_template
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
