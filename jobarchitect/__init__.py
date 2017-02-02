"""jobarchitect package."""

__version__ = "0.1.0"


def generate_bash_job(jobspec):
    """Return bash script to run all analysis on all data in one chunk from a
    split dataset.

    jobspec should include:

    dataset_path: Path to dataset
    output_root: Root of path in which output will be written
    program_template: Template to specify analysis program to execute
    chunks: List of hashes to analyse
    """

    output = """#!/bin/bash
_analyse_by_ids \
  --program_template={program_template} \
  --input_dataset_path={dataset_path} \
  --output_root={output_root} \
  {hash_ids}
    """.format(**jobspec._asdict())

    return output
