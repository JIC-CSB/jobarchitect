"""Jobarchitect agent."""

from dtool import DataSet


class Agent(object):
    """Class to create commands to analyse data."""

    def __init__(self, dataset_path, program_template):
        self.dataset_path = dataset_path
        self.program_template = program_template

        self.dataset = DataSet.from_path(self.dataset_path)


def create_command(program_name, input_file, output_file):
    """Return list representing command to execute.

    This is a placeholder for a function that does this properly."""

    return [program_name, input_file, output_file]
